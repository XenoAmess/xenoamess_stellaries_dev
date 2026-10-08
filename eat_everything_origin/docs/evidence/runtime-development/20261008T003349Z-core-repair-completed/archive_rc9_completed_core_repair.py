import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime,timezone
source=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
target=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T003349Z-core-repair-completed')
assert not target.exists()
proof=json.loads((source/'rc9-permanent-core-death-repair-negative-proof.json').read_text(encoding='utf-8'))
assert proof['status']=='PASS_SCOPED'
copy=source/Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__),copy)
target.mkdir(parents=True)
(target/'.gitattributes').write_text('* binary\n**/* binary\n',encoding='utf-8')
entries=[]
def take(path,name):
 data=path.read_bytes()
 out=target/name
 out.parent.mkdir(parents=True,exist_ok=True)
 assert not out.exists()
 out.write_bytes(data)
 digest=hashlib.sha256(data).hexdigest()
 assert hashlib.sha256(out.read_bytes()).hexdigest()==digest
 entries.append({'path':name,'source':str(path.resolve()),'bytes':len(data),'sha256':digest})
for p in sorted(source.rglob('*')):
 if not p.is_file() or p.name.startswith(('rc9-focus','rc9_prepare_focus')):
  continue
 if p.name.startswith(('rc9-','rc9_')) or p.name in ('manifest.json','process.json',Path(__file__).name):
  take(p,p.relative_to(source).as_posix())
original_source=source/'source-snapshot.json'
if original_source.exists():
 take(original_source,'run-source-snapshot.json')
take(source/'rc9-dead-repair-error-after.log','stage-full-error-through-core-repair.log')
meta={'status':'SNAPSHOT_BYTE_VERIFIED','snapshot_at_utc':datetime.now(timezone.utc).isoformat(),'run':source.name,'version':'0.2.0-rc.9','language':'l_simp_chinese','scope':'Completed bound-core terraforming recovery regressions only. Excludes active focus-purge phase; not final complete-run archive.','original_files':len(entries),'original_bytes':sum(e['bytes'] for e in entries),'first_release_complete':False,'affected_core_repair_regression_complete':True,'final_error_log_required_after_normal_stop':True,'preserved_failures':'Initial cold GPU/title readiness, console selected-planet country-event replay error, strict native-zone payment all-stock-equality failure; exact three research stock keys missing and research queues preserved.','files':entries}
(target/'source-snapshot.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k!='files'},ensure_ascii=True))
