"""Complete raw source manifest with reuse of committed, frozen evidence only."""
import hashlib, json, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

label, baseline_label, baseline_commit = sys.argv[1:]
assert all(re.fullmatch(r'[A-Za-z0-9-]{1,100}', v) for v in [label, baseline_label])
assert re.fullmatch(r'[0-9a-f]{40}', baseline_commit)
repo = Path.cwd().resolve()
evidence = Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09')
target, baseline = evidence / label, evidence / baseline_label
assert not target.exists()
subprocess.run(['git', 'merge-base', '--is-ancestor', baseline_commit, 'HEAD'], check=True)
manifest_path = baseline / 'source-snapshot.json'
baseline_raw = manifest_path.read_bytes()
committed = subprocess.check_output(['git', 'cat-file', 'blob', baseline_commit + ':' + manifest_path.as_posix()])
assert baseline_raw == committed
base = json.loads(baseline_raw)
assert base['schema'] in {'active-run-partial-checkpoint-v1', 'active-run-partial-checkpoint-v2'}
base_rows = {row['file']: row for row in base['files']}
assert len(base_rows) == len(base['files']) == base['source_files']
def original_path(root, row):
    path = Path(row.get('evidence_path', (root / row['file']).as_posix()))
    assert not path.is_absolute() and '..' not in path.parts
    path.resolve().relative_to(evidence.resolve())
    return path
pointer = json.loads(Path('_runtime/heart-of-devouring/runs/current-run.json').read_text('utf-8'))
run, user = Path(pointer['artifact_dir']), Path(pointer['userdir'])
for source in [Path(__file__), Path('_runtime/heart-of-devouring/verify_priority_delta_checkpoint_git.py')]:
    dest = run / source.name
    if dest.exists(): assert dest.read_bytes() == source.read_bytes()
    else: shutil.copyfile(source, dest)
target.mkdir(parents=True)
files = []
def preserve(source, relative):
    raw = source.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    old = base_rows.get(relative.as_posix())
    reuse = old is not None and old['bytes'] == len(raw) and old['sha256'] == sha
    if reuse:
        dest = original_path(baseline, old)
        assert dest.read_bytes() == raw, 'Frozen baseline bytes changed: ' + str(dest)
    else:
        dest = target / relative
        dest.resolve().relative_to(target.resolve())
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        assert dest.read_bytes() == raw
    files.append({'file': relative.as_posix(), 'source': str(source.resolve()),
                  'bytes': len(raw), 'sha256': sha, 'evidence_path': dest.as_posix(),
                  'storage': 'reused' if reuse else 'copied'})
for source in sorted(run.rglob('*')):
    if source.is_file(): preserve(source, source.relative_to(run))
for source in sorted((user / 'logs').rglob('*')):
    if source.is_file(): preserve(source, Path('logs-at-checkpoint') / source.relative_to(user / 'logs'))
for name in ['settings.txt', 'pdx_settings.txt', 'dlc_load.json', 'user_empire_designs_v3.4.txt']:
    source = user / name
    if source.is_file(): preserve(source, Path('userdir-config') / name)
(target / '.gitattributes').write_text('* binary\n** binary\n', encoding='utf-8', newline='\n')
copied = [row for row in files if row['storage'] == 'copied']
proof = {'schema': 'active-run-partial-checkpoint-v2', 'run_id': run.name, 'label': label,
         'captured_at_utc': datetime.now(timezone.utc).isoformat(),
         'baseline': {'commit': baseline_commit, 'manifest': manifest_path.as_posix(),
                      'manifest_sha256': hashlib.sha256(baseline_raw).hexdigest()},
         'files': files, 'source_files': len(files), 'source_bytes': sum(row['bytes'] for row in files),
         'copied_files': len(copied), 'copied_bytes': sum(row['bytes'] for row in copied),
         'reused_files': len(files) - len(copied),
         'scope': 'Complete active paused-run source manifest. Every source resolves to exact raw bytes in this cut or a committed frozen baseline. Not shutdown, reload or full-route acceptance.'}
(target / 'source-snapshot.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({k: v for k, v in proof.items() if k != 'files'}), flush=True)
