import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

run = Path('_runtime/heart-of-devouring/runs/20261007T201344Z')
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
user = Path(manifest['userdir'])
stop = json.loads((run / 'stop.json').read_text(encoding='utf-8'))
assert stop['forced'] is False and stop['running_after'] is False
target = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T201344Z')
assert not target.exists()
target.mkdir(parents=True)
files = []

def copy(src, relative):
    dest = target / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    data = src.read_bytes()
    assert data == dest.read_bytes()
    files.append({'file': relative.as_posix(), 'original_source': str(src.resolve()),
                  'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})

for src in sorted(run.rglob('*')):
    if src.is_file():
        copy(src, src.relative_to(run))
for src in sorted((user / 'logs').rglob('*')):
    if src.is_file():
        copy(src, Path('final-logs') / src.relative_to(user / 'logs'))
for name in ['settings.txt', 'pdx_settings.txt', 'dlc_load.json', 'commands_at_date.txt']:
    src = user / name
    if src.is_file():
        copy(src, Path('userdir-config') / name)
(target / '.gitattributes').write_text('* binary\n** binary\n', encoding='utf-8')
snapshot = {
    'schema': 'immutable-native-source-snapshot-v1', 'run_id': run.name,
    'archived_at_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Entire normally stopped simplified-Chinese controlled decision conflict EEP first/control last. Exact common zero source bytes, actual native UI and first-month8.5 route, startup frame failures and original wrong-source helper FAIL retained. Complete final unfiltered logs/config. First order only; second order and full Scorched Hive acceptance pending.',
    'stop': stop, 'source_files': len(files), 'source_bytes': sum(value['bytes'] for value in files), 'files': files,
}
(target / 'source-snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'source_files': len(files), 'source_bytes': snapshot['source_bytes']}))
