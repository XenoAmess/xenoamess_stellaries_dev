import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
run = Path('_runtime/heart-of-devouring/runs/20261007T203412Z')
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
user = Path(manifest['userdir'])
stop = json.loads((run / 'stop.json').read_text(encoding='utf-8'))
assert stop['forced'] is False and stop['running_after'] is False
target = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T203412Z')
assert not target.exists()
target.mkdir(parents=True)
files = []
def copy(source, relative):
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    raw = source.read_bytes()
    assert destination.read_bytes() == raw
    files.append({'file': relative.as_posix(), 'original_source': str(source.resolve()), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
for source in sorted(run.rglob('*')):
    if source.is_file():
        copy(source, source.relative_to(run))
for source in sorted((user / 'logs').rglob('*')):
    if source.is_file():
        copy(source, Path('final-logs') / source.relative_to(user / 'logs'))
for name in ['settings.txt', 'pdx_settings.txt', 'dlc_load.json', 'commands_at_date.txt']:
    source = user / name
    if source.is_file():
        copy(source, Path('userdir-config') / name)
(target / '.gitattributes').write_text('* binary\n** binary\n', encoding='utf-8')
snapshot = {'schema': 'immutable-native-source-snapshot-v1', 'run_id': run.name, 'archived_at_utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Entire normally stopped rc7 affected begin regressions and qualified dual-owner controlled independent-system/core case, reports, exact native no-report reload control and ten monthly callbacks. Full original observer/same-system/raw-reload failures preserved. Numeric/read-only subproofs122/137/57/117 and outpost4 pass; final full log contains production button allow country-scope error requiring rc8 repair. Not full Scorched Hive acceptance or release.', 'stop': stop, 'source_files': len(files), 'source_bytes': sum(value['bytes'] for value in files), 'files': files}
(target / 'source-snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'source_files': len(files), 'source_bytes': snapshot['source_bytes']}))
