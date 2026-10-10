"""Independently resolve every delta-manifest source and check staged raw bytes."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

label = sys.argv[1]
assert re.fullmatch(r'[A-Za-z0-9-]{1,100}', label)
evidence = Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09')
checkpoint = evidence / label
manifest = json.loads((checkpoint / 'source-snapshot.json').read_text('utf-8'))
assert manifest['schema'] == 'active-run-partial-checkpoint-v2'
binding = manifest['baseline']
subprocess.run(['git', 'merge-base', '--is-ancestor', binding['commit'], 'HEAD'], check=True)
base_path = Path(binding['manifest'])
base_path.resolve().relative_to(evidence.resolve())
base_raw = subprocess.check_output(['git', 'cat-file', 'blob', binding['commit'] + ':' + base_path.as_posix()])
assert base_path.read_bytes() == base_raw
assert hashlib.sha256(base_raw).hexdigest() == binding['manifest_sha256']
base = json.loads(base_raw)
base_rows = {row['file']: row for row in base['files']}
assert len(base_rows) == len(base['files']) == base['source_files']
expected = {}
def want(path, sha, size):
    path = Path(path)
    assert not path.is_absolute() and '..' not in path.parts
    name = path.as_posix()
    if name in expected: assert expected[name] == (sha, size)
    expected[name] = (sha, size)
seen = set();copied_files = copied_bytes = reused_files = total_sources = 0
for row in manifest['files']:
    assert row['file'] not in seen
    seen.add(row['file'])
    assert type(row['bytes']) is int and row['bytes'] >= 0
    assert re.fullmatch(r'[0-9a-f]{64}', row['sha256'])
    path = Path(row['evidence_path'])
    path.resolve().relative_to(evidence.resolve())
    if row['storage'] == 'reused':
        previous = base_rows[row['file']]
        old_path = Path(previous.get('evidence_path', (base_path.parent / previous['file']).as_posix()))
        assert path == old_path and row['sha256'] == previous['sha256'] and row['bytes'] == previous['bytes']
        reused_files += 1
    else:
        assert row['storage'] == 'copied' and path == checkpoint / row['file']
        copied_files += 1;copied_bytes += row['bytes']
    total_sources += row['bytes']
    want(path, row['sha256'], row['bytes'])
assert len(seen) == manifest['source_files'] == copied_files + reused_files
assert total_sources == manifest['source_bytes']
assert (copied_files, copied_bytes, reused_files) == (manifest['copied_files'], manifest['copied_bytes'], manifest['reused_files'])
want(base_path, binding['manifest_sha256'], len(base_raw))
preparation = Path('eat_everything_origin/docs/evidence/priority-terravore-preparation-2026-10-09')
prep = json.loads((preparation / 'source-snapshot.json').read_text('utf-8'))
for row in prep['files']: want(preparation / row['file'], row['sha256'], row['bytes'])
for root in [checkpoint, preparation]:
    for name in ['source-snapshot.json', '.gitattributes']:
        path = root / name;raw = path.read_bytes()
        want(path, hashlib.sha256(raw).hexdigest(), len(raw))
for path in Path('eat_everything_origin/docs/evidence').glob('priority-*.json'):
    raw = path.read_bytes();want(path, hashlib.sha256(raw).hexdigest(), len(raw))
p = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
total = 0
try:
    for path, (wanted, size) in expected.items():
        p.stdin.write((':' + path + '\n').encode('utf-8'));p.stdin.flush()
        header = p.stdout.readline().decode('ascii').strip().split()
        assert len(header) == 3 and header[1] == 'blob' and int(header[2]) == size, (path, header)
        remaining = size;sha = hashlib.sha256()
        while remaining:
            raw = p.stdout.read(min(1048576, remaining));assert raw
            sha.update(raw);remaining -= len(raw)
        assert p.stdout.read(1) == b'\n' and sha.hexdigest() == wanted, path
        total += size
    p.stdin.close();assert p.wait(timeout=15) == 0 and p.stderr.read() == b''
finally:
    if p.poll() is None: p.kill();p.wait()
out = Path('eat_everything_origin/docs/evidence') / ('priority-' + label + '-delta-staged-verification-2026-10-11.json')
assert not out.exists()
proof = {'status': 'PASS_STAGED_RAW_PRIORITY_DELTA_CHECKPOINT', 'source_files': len(seen),
         'source_bytes': total_sources, 'copied_files': copied_files, 'copied_bytes': copied_bytes,
         'reused_files': reused_files, 'staged_blobs': len(expected), 'staged_bytes': total,
         'checkpoint': checkpoint.as_posix(), 'baseline': binding,
         'scope': 'All raw source bytes, including frozen reused originals, checked against the actual Git index. Not full-route acceptance.'}
out.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(proof), flush=True)
