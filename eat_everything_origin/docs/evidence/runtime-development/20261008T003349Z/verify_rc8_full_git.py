import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path('eat_everything_origin/docs/evidence/runtime-development/20261007T215509Z')
snapshot = json.loads((root / 'source-snapshot.json').read_text(encoding='utf-8'))
copy = Path('_runtime/heart-of-devouring/runs/20261008T003349Z') / Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__), copy)
for entry in snapshot['files']:
    data = (root / entry['file']).read_bytes()
    assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']
    assert Path(entry['original_source']).read_bytes() == data
paths = sorted(p for p in root.rglob('*') if p.is_file())
requests = ''.join(':' + p.as_posix() + '\n' for p in paths).encode()
raw = subprocess.run(['git','cat-file','--batch'],input=requests,capture_output=True,check=True).stdout
cursor = 0
for path in paths:
    end = raw.index(b'\n',cursor)
    oid,kind,size = raw[cursor:end].decode().split()
    assert kind == 'blob'
    size = int(size)
    assert raw[end+1:end+1+size] == path.read_bytes(), path
    cursor = end+1+size+1
assert cursor == len(raw)
error = root / 'final-logs/error.log'
text = error.read_text(encoding='utf-8-sig',errors='replace')
result = {'status':'PASS','scope':'Immutable full native run and Git bytes; runtime core-deposit failure remains.',
          'source_files':snapshot['source_files'],'source_bytes':snapshot['source_bytes'],
          'git_checked_files':len(paths),'git_checked_bytes':sum(p.stat().st_size for p in paths),
          'normal_stop':not snapshot['stop']['forced'] and not snapshot['stop']['running_after'],
          'final_error_sha256':hashlib.sha256(error.read_bytes()).hexdigest(),
          'wrong_scope_present':'Wrong scope for trigger' in text,
          'native_machine_age_invalid_context_present':'cyberize_pops_effect' in text,
          'runtime_core_deposit_failure_preserved':True,'first_release_acceptance_complete':False}
out = Path('eat_everything_origin/docs/evidence/rc8-full-native-run-git-object-check-2026-10-08.json')
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=True))
