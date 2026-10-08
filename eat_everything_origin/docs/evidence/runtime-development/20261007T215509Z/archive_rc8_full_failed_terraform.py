import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

run = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
user = Path(manifest['userdir'])
stop = json.loads((run / 'stop.json').read_text(encoding='utf-8'))
assert stop['forced'] is False and stop['running_after'] is False
target = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T215509Z')
assert not target.exists()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
for name in ['verify_rc8_fifteen_defense_git.py', 'verify_rc8_natural_ten_years_git.py']:
    source = Path('_runtime/heart-of-devouring') / name
    out = run / name
    assert not out.exists()
    shutil.copyfile(source, out)
target.mkdir(parents=True)
files = []

def copy(source, relative):
    destination = target / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    destination.write_bytes(raw)
    assert destination.read_bytes() == raw
    files.append({'file': relative.as_posix(), 'original_source': str(source.resolve()),
                  'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})

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
snapshot = {'schema':'immutable-native-source-snapshot-v1', 'run_id':run.name,
    'archived_at_utc':datetime.now(timezone.utc).isoformat(), 'version':'0.2.0-rc.8',
    'scope':'Entire normally stopped rc8 report-scope regressions and natural paid 20-year hive-world conversion. Original helper failures, failed defense attempts, bombardment population losses and actual final core-deposit loss retained. Six-checkpoint proof has 103 successes and one core deposit failure; not full Scorched Hive acceptance or release.',
    'stop':stop,'source_files':len(files),'source_bytes':sum(v['bytes'] for v in files),'files':files}
(target / 'source-snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_files':len(files),'source_bytes':snapshot['source_bytes']},ensure_ascii=True))
