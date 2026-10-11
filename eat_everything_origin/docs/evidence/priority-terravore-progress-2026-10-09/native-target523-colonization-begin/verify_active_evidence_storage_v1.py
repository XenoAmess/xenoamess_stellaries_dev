"""Readonly, full-byte comparison for the documented single-run storage move."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

source, target, output = map(Path, sys.argv[1:])
logical = Path('D:/workspace/xenoamess_stellaries_dev/_runtime/heart-of-devouring/runs/20261009T044016Z')
backup = logical.with_name(logical.name + '.storage-migration-backup')
physical = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/20261009T044016Z')
assert (source.absolute(), target.absolute()) in {(logical, physical), (backup, logical)}
assert output.parent.absolute() == physical.parent and not output.exists()
if source == backup:
    assert logical.resolve() == physical.resolve()
assert source.is_dir() and target.is_dir() and source.resolve() != target.resolve()

def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_file():
            assert not path.is_symlink(), str(path)
            relative = path.relative_to(root).as_posix()
            data = path.read_bytes()
            result[relative] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return result

before, after = inventory(source), inventory(target)
assert before and before == after, 'Copy differs; retain all copies and stop.'
assert before['terravore-rear-colonizer4-native-birth.sav']['sha256'] == '456b1c2f10ab0e71fb8c258d6ed4dd262f79f79ec4e897b16a86cc7ff8859c39'
assert before['record_current_helper.py']['sha256'] == '7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3'
result = {'status': 'PASS_FULL_RAW_EVIDENCE_STORAGE_COPY', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'source': str(source), 'target': str(target), 'source_resolved': str(source.resolve()),
          'target_resolved': str(target.resolve()), 'files': len(before),
          'bytes': sum(v['bytes'] for v in before.values()), 'inventory': before,
          'scope': 'Exact active evidence bytes only; no game, Mod or acceptance changes.'}
output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k != 'inventory'}), flush=True)
