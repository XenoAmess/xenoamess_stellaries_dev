"""Archive only immutable control-run additions after its paused snapshot."""
import hashlib,json,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');read=lambda p:json.loads(p.read_text('utf-8'));ptr=read(Path('_runtime/heart-of-devouring/runs/current-run.json'));prod=Path(ptr['artifact_dir']);cp=read(prod/'leader13-control-pointer.json');control=Path(cp['artifact_dir']);assert control.name=='20261009T192111Z' and control!=prod
root=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09');old=read(root/'native-leader-trait-error-control/source-snapshot.json');dest=root/'native-leader-trait-error-control-tail';assert not dest.exists();old_paths={}
for row in old['files']:
 p=Path(row['source'])
 if p.is_relative_to(control):
  assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],str(p)
  old_paths[p.relative_to(control).as_posix()]=row['sha256']
assert read(control/'normal-control-exit.json')['status']=='OBSERVED_NORMAL_GUI_EXIT';assert (control/'logs-final-after-normal-exit/error.log').is_file();dest.mkdir(parents=True);files=[]
def copy(p,rel):
 raw=p.read_bytes();out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);assert out.read_bytes()==raw
 files.append({'file':rel.as_posix(),'source':str(p.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
for p in sorted(control.rglob('*')):
 if p.is_file() and p.relative_to(control).as_posix() not in old_paths:copy(p,p.relative_to(control))
copy(Path(__file__),Path('priority_archive_leader13_control_tail.py'));(dest/'.gitattributes').write_text('* binary\n** binary\n',encoding='utf-8',newline='\n')
p={'schema':'control-exit-tail-original-bytes-v1','run_id':control.name,'label':dest.name,'captured_at_utc':datetime.now(timezone.utc).isoformat(),'prior_control_snapshot':'native-leader-trait-error-control','old_run_artifacts_verified_unchanged':len(old_paths),'files':files,'source_files':len(files),'source_bytes':sum(x['bytes'] for x in files),'scope':'Only new control exit GUI/actions/receipts and final unfiltered logs after paused snapshot. Prior RUN artifacts checked unchanged. No game or pointer mutation.'};(dest/'source-snapshot.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({k:v for k,v in p.items() if k!='files'}),flush=True)
