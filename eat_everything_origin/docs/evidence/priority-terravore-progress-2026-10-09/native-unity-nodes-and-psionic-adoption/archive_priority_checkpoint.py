"""Original-byte snapshot of an active paused acceptance run, not final exit."""
import hashlib,json,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
label=sys.argv[1];assert label.replace('-','').isalnum()
pointer=json.loads(Path('_runtime/heart-of-devouring/runs/current-run.json').read_text(encoding='utf-8'))
run=Path(pointer['artifact_dir']);user=Path(pointer['userdir'])
target=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09')/label
assert not target.exists()
for source in [Path(__file__),Path('_runtime/heart-of-devouring/verify_priority_checkpoint_git.py')]:
    dest=run/source.name
    if dest.exists():assert dest.read_bytes()==source.read_bytes()
    else:shutil.copyfile(source,dest)
target.mkdir(parents=True);files=[]
def copy(source,rel):
    raw=source.read_bytes();dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(raw);assert dest.read_bytes()==raw
    files.append({'file':rel.as_posix(),'source':str(source.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
for source in sorted(run.rglob('*')):
    if source.is_file():copy(source,source.relative_to(run))
for source in sorted((user/'logs').rglob('*')):
    if source.is_file():copy(source,Path('logs-at-checkpoint')/source.relative_to(user/'logs'))
for name in ['settings.txt','pdx_settings.txt','dlc_load.json','user_empire_designs_v3.4.txt']:
    source=user/name
    if source.is_file():copy(source,Path('userdir-config')/name)
(target/'.gitattributes').write_text('* binary\n** binary\n',encoding='utf-8',newline='\n')
proof={'schema':'active-run-partial-checkpoint-v1','run_id':run.name,'label':label,
       'captured_at_utc':datetime.now(timezone.utc).isoformat(),'files':files,
       'source_files':len(files),'source_bytes':sum(f['bytes'] for f in files),
       'scope':'Active paused-run checkpoint, all current raw artifacts and unfiltered logs at capture. Not final shutdown, reload or full-route acceptance.'}
(target/'source-snapshot.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in proof.items() if k!='files'}),flush=True)
