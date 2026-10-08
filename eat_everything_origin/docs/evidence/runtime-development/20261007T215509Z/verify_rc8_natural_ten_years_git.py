import hashlib
import json
from pathlib import Path
import subprocess

root = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T215509Z-natural-terraform-ten-years')
snapshot = json.loads((root / 'source-snapshot.json').read_text(encoding='utf-8'))
changed = []
for entry in snapshot['files']:
    data = (root / entry['path']).read_bytes()
    assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']
    if Path(entry['source']).read_bytes() != data:
        assert entry['path'] == 'stage-full-error-through-ten-natural-years.log'
        changed.append(entry['path'])
paths = sorted(p for p in root.rglob('*') if p.is_file())
requests = ''.join(':' + p.as_posix() + '\n' for p in paths).encode()
raw = subprocess.run(['git', 'cat-file', '--batch'], input=requests, capture_output=True, check=True).stdout
cursor = 0
for path in paths:
    end = raw.index(b'\n', cursor)
    oid, kind, size = raw[cursor:end].decode().split()
    assert kind == 'blob'
    size = int(size)
    assert raw[end + 1:end + 1 + size] == path.read_bytes(), path
    cursor = end + 1 + size + 1
assert cursor == len(raw)
error = root / 'stage-full-error-through-ten-natural-years.log'
content = error.read_text(encoding='utf-8-sig', errors='replace')
result = {'status': 'PASS',
          'scope': 'Original bytes and staged Git blobs of the two completed natural calendar stages; not final run or full Focus acceptance.',
          'source_files': snapshot['original_files'], 'source_bytes': snapshot['original_bytes'],
          'git_checked_files': len(paths), 'git_checked_bytes': sum(p.stat().st_size for p in paths),
          'stage_error_sha256': hashlib.sha256(error.read_bytes()).hexdigest(),
          'wrong_scope_present': 'Wrong scope for trigger' in content,
          'live_stage_error_changed_after_capture': bool(changed),
          'full_terraform_completion': False, 'final_complete_run_log_still_required': True,
          'preserved_helper_failure': snapshot['preserved_helper_failure']}
assert not result['wrong_scope_present']
out = Path('eat_everything_origin/docs/evidence/rc8-natural-ten-year-git-object-check-2026-10-08.json')
assert not out.exists()
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=True))
