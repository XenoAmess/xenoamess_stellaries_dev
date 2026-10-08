import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime,timezone
source=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
target=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T003349Z-focus-purge-completed')
assert not target.exists()
assert json.loads((source/'rc9-focus-native-purge-final-replay-proof.json').read_text(encoding='utf-8'))['status']=='PASS_SCOPED'
shutil.copyfile(Path(__file__),source/Path(__file__).name)
target.mkdir(parents=True)
(target/'.gitattributes').write_text('* binary\n**/* binary\n',encoding='utf-8')
entries=[]
def take(path,name):
 data=path.read_bytes();out=target/name;out.parent.mkdir(parents=True,exist_ok=True)
 assert not out.exists();out.write_bytes(data)
 digest=hashlib.sha256(data).hexdigest();assert hashlib.sha256(out.read_bytes()).hexdigest()==digest
 entries.append({'path':name,'source':str(path.resolve()),'bytes':len(data),'sha256':digest})
names={'manifest.json','process.json','rc9-original-native-source-preflight.json','rc9-recovery-extra-source-preflight.json','rc9_restore_native_source.py','rc9_forward_native_days.py','rc9_forward_purge_calendar.py','rc9_focus_developed_seed69.py','rc9_waiting_reload_replay.py','rc9_purge_final_replay.py',Path(__file__).name}
for p in sorted(source.rglob('*')):
 if p.is_file() and (p.name.startswith(('rc9-focus','rc9_prepare_focus')) or p.name in names):take(p,p.relative_to(source).as_posix())
take(source/'rc9-focus-purge-final-replay-error-after.log','stage-full-error-through-focus-purge.log')
proofs=['rc9-focus-developed-seed69-precondition-proof.json','rc9-focus-valid-wait-setup-preconditions.json','rc9-focus-wait39-reload-proof.json','rc9-focus-wait39-replay-proof.json','rc9-focus-native-extermination-rights-observed-proof.json','rc9-focus-native-purge-final-proof.json','rc9-focus-native-purge-final-replay-proof.json']
count=0
for n in proofs:
 a=json.loads((source/n).read_text(encoding='utf-8'));assert all(a['checks'].values());count+=len(a['checks'])
meta={'status':'SNAPSHOT_BYTE_VERIFIED','snapshot_at_utc':datetime.now(timezone.utc).isoformat(),'run':source.name,'version':'0.2.0-rc.9','language':'l_simp_chinese','scope':'Completed Scorched Hive controlled waiting39, original reload, actual purge_normal clearance and one settlement only. Excludes external destruction branches and final complete-run log.','original_files':len(entries),'original_bytes':sum(e['bytes'] for e in entries),'checked_points':len(proofs),'checks_passed':count,'first_release_complete':False,'focus_purge_boundary_complete':True,'final_error_log_required_after_normal_stop':True,'preserved_failures':['First source still under colonization and formal begin correctly rejected; no task although foreign1200 created.','Native rights last_changed_purge_type future2234, initial current-day assertion failed.','360-day completion receipt occluded by native event; exact monitor stopped, recovery retained.'],'files':entries}
(target/'source-snapshot.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k!='files'},ensure_ascii=True))
