import hashlib,json,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
run=Path('_runtime/heart-of-devouring/runs')/sys.argv[1]
m=json.loads((run/'manifest.json').read_text(encoding='utf-8'));user=Path(m['userdir'])
stop=json.loads((run/'stop.json').read_text(encoding='utf-8'))
assert stop['forced'] is False and stop['running_after'] is False
target=Path('eat_everything_origin/docs/evidence/runtime-development')/run.name
assert not target.exists()
for name in [Path(__file__).name,'verify_normally_stopped_formal.py']:
    src=Path('_runtime/heart-of-devouring')/name
    dest=run/name
    assert not dest.exists();shutil.copyfile(src,dest)
target.mkdir(parents=True);files=[]
def copy(src,rel):
    out=target/rel;out.parent.mkdir(parents=True,exist_ok=True)
    raw=src.read_bytes();out.write_bytes(raw);assert out.read_bytes()==raw
    files.append({'file':rel.as_posix(),'original_source':str(src.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
for src in sorted(run.rglob('*')):
    if src.is_file():copy(src,src.relative_to(run))
for src in sorted((user/'logs').rglob('*')):
    if src.is_file():copy(src,Path('final-logs')/src.relative_to(user/'logs'))
for name in ['settings.txt','pdx_settings.txt','dlc_load.json','commands_at_date.txt']:
    src=user/name
    if src.is_file():copy(src,Path('userdir-config')/name)
(target/'.gitattributes').write_text('* binary\n** binary\n',encoding='utf-8')
proof={'schema':'immutable-native-source-snapshot-v1','run_id':run.name,'archived_at_utc':datetime.now(timezone.utc).isoformat(),
 'version':'0.2.0','scope':'Entire normally stopped Simplified Chinese run; all failures and unfiltered final logs retained. Archive integrity is not full government or release acceptance.',
 'stop':stop,'source_files':len(files),'source_bytes':sum(x['bytes'] for x in files),'files':files}
(target/'source-snapshot.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in proof.items() if k!='files'}))
