import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime, timezone

source = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
target = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T215509Z-natural-terraform-ten-years')
assert not target.exists()
end = json.loads((source / 'rc8-hiveworld-terraform-ten-real-years.audit.json').read_text(encoding='utf-8'))
assert end['date'] == '2309.03.12'
checkpoint = json.loads((source / 'rc8-hiveworld-terraform-ten-real-years-native-terraform-checkpoint.json').read_text(encoding='utf-8'))
assert 'progress=3600' in checkpoint['terraform']['terraform_process']
proof = json.loads((source / 'rc8-natural-terraform-checkpoints-3-2309-03-12-proof.json').read_text(encoding='utf-8'))
assert proof['status'] == 'PASS_SCOPED' and not proof['full_terraform_completion']
shutil.copyfile(Path(__file__), source / Path(__file__).name)
target.mkdir(parents=True)
(target / '.gitattributes').write_text('* binary\n**/* binary\n', encoding='utf-8')
entries = []


def take(path, name):
    data = path.read_bytes()
    out = target / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    assert hashlib.sha256(out.read_bytes()).hexdigest() == digest
    entries.append({'path': name, 'source': str(path.resolve()), 'bytes': len(data), 'sha256': digest})


prefixes = ('rc8-hiveworld-terraform-five-real-years', 'rc8-hiveworld-terraform-ten-real-years',
            'rc8-natural-terraform-checkpoints-', 'rc8_recover_natural_ten_year_save',
            'rc8-ten-year-truncated-receipt-')
names = {Path(__file__).name, 'rc8_verify_natural_terraform_checkpoints.py',
         'rc8_verify_natural_terraform_checkpoints_recovered.py', 'rc8_natural_forward_span.py'}
for path in sorted(source.rglob('*')):
    if path.is_file() and (path.name.startswith(prefixes) or path.name in names):
        take(path, path.relative_to(source).as_posix())
error = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T215509Z/logs/error.log')
take(error, 'stage-full-error-through-ten-natural-years.log')
manifest = {'status': 'SNAPSHOT_BYTE_VERIFIED', 'snapshot_at_utc': datetime.now(timezone.utc).isoformat(),
            'run': source.name, 'version': '0.2.0-rc.8', 'language': 'l_simp_chinese',
            'scope': 'Completed natural five- and ten-year stages and read-only proofs. Partial run, not final archive.',
            'original_files': len(entries), 'original_bytes': sum(v['bytes'] for v in entries),
            'full_terraform_completion': False, 'final_error_log_required_after_normal_stop': True,
            'preserved_helper_failure': 'Anonymous-modifier array ValueError, ten-year cropped completion guard, recovery manifest.pid KeyError, Python Manager/worker non-unique first stop guard; original sources and receipts preserved.',
            'files': entries}
(target / 'source-snapshot.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}, ensure_ascii=True))
