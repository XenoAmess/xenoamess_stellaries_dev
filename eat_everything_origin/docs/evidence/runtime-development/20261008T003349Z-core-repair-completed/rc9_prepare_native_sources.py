import hashlib
import json
from pathlib import Path
import shutil

run = Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
user = Path(manifest['userdir'])
shutil.copyfile(Path(__file__), run / Path(__file__).name)
sources = {
 'hive-before-end': Path('_runtime/heart-of-devouring/runs/20261007T215509Z/rc8-hiveworld-terraform-final-day-before.sav'),
 'hive-missing-core': Path('_runtime/heart-of-devouring/runs/20261007T215509Z/rc8-hiveworld-terraform-natural-complete.sav'),
 'focus-base23': Path('_runtime/heart-of-devouring/runs/20261006T232907Z/hive-scorched-natural23-source-ready.sav'),
 'fleet2-war80': Path('_runtime/heart-of-devouring/runs/20261007T031421Z/native-psi80-natural.sav'),
}
receipts = []
for alias, source in sources.items():
    a = json.loads(source.with_suffix('.audit.json').read_text(encoding='utf-8'))
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    assert sha == a['save_sha256']
    destination = user / 'save games' / 'acceptance-fixtures' / (alias + '.sav')
    assert not destination.exists()
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert hashlib.sha256(destination.read_bytes()).hexdigest() == sha
    receipts.append({'alias':alias,'source':str(source.resolve()),'copy':str(destination),
                     'date':a['date'],'sha256':sha,'bytes':source.stat().st_size})
out = run / 'rc9-original-native-source-preflight.json'
out.write_text(json.dumps({'status':'ORIGINAL_BYTE_COPIES_ONLY','sources':receipts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ORIGINAL_BYTE_COPIES_ONLY','sources':receipts},ensure_ascii=True))
