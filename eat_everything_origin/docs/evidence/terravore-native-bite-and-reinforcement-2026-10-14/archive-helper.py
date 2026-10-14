"""Archive only completed monthly/native-bite and paid-operation stages."""
import hashlib,json,shutil
from datetime import datetime
from pathlib import Path
repo=Path.cwd().resolve()
pointer=json.loads((repo/'_runtime/heart-of-devouring/runs/current-run.json').read_text('utf-8'))
run=Path(pointer['artifact_dir'])
dest=repo/'eat_everything_origin/docs/evidence/terravore-native-bite-and-reinforcement-2026-10-14'
assert not dest.exists()
first=json.loads((run/'hope-route-wait-native-22960301-digest-guard-v5-execution.json').read_text('utf-8'))['finished_at_utc']
last=json.loads((run/'hope-route-feb97-main80-order-guard-v2-20261014-execution.json').read_text('utf-8'))['finished_at_utc']
lower,upper=[datetime.fromisoformat(v).timestamp() for v in (first,last)]
sources={p.name:p for p in run.glob('hope-route-*') if p.is_file() and lower<p.stat().st_mtime<=upper}
sources.update({p.name:p for p in run.glob('hope-route-wait-native-22960301*') if p.is_file()})
executions=[p for p in sources.values() if p.name.endswith('-execution.json')]
for path in executions:
 execution=json.loads(path.read_text('utf-8'))
 name=Path(execution['command'][1]).name
 original=run/name
 assert original.is_file() and hashlib.sha256(original.read_bytes()).hexdigest()==execution['helper_sha256']
 sources[name]=original
sources.update({'record_current_helper.py':run/'record_current_helper.py','support-runtime.py':repo/'eat_everything_origin/tools/runtime.py','support-audit_save.py':repo/'eat_everything_origin/tools/audit_save.py','priority_terravore_native_state.py':repo/'_runtime/heart-of-devouring/priority_terravore_native_state.py','archive-helper.py':Path(__file__).resolve()})
assert all(p.is_file() for p in sources.values())
size=sum(p.stat().st_size for p in sources.values())
assert size<80_000_000 and shutil.disk_usage(repo).free>size*3+220_000_000
dest.mkdir();(dest/'.gitattributes').write_bytes(b'* binary\n');rows=[]
for name,path in sorted(sources.items()):
 data=path.read_bytes();sha=hashlib.sha256(data).hexdigest()
 target=dest/name;target.write_bytes(data)
 assert hashlib.sha256(target.read_bytes()).hexdigest()==sha
 rows.append({'file':name,'bytes':len(data),'sha256':sha,'source':str(path)})
(dest/'source-snapshot.json').write_text(json.dumps({'files':len(rows),'bytes':size,'source_run':pointer,'manifest':rows,'scope':'Completed native months through2297.02.01, normal paid supplies/source armies, reinforcement completion, first native population bite and normal waypoint80 orders. Includes original FAIL/rejected calendar and corrected read-only proofs. Not full civic acceptance.'},indent=2)+'\n','utf-8',newline='\n')
print(json.dumps({'pass':True,'files':len(rows),'bytes':size,'dest':str(dest)}),flush=True)
