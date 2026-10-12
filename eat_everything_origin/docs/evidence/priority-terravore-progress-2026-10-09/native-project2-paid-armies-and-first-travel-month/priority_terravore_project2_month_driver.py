"""Finite monthly project2 native driver; every exact saved interval and guard must return0."""
import json,subprocess,sys
from pathlib import Path
before,proof,execution,prefix,rawcount=sys.argv[1:];count=int(rawcount);assert 1<=count<=10
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z');wrapper=run/'record_current_helper.py'
def call(stage,helper,*args):
 print(json.dumps({'phase':stage,'helper':helper}),flush=True)
 subprocess.run([sys.executable,str(wrapper),stage,str(run/helper),*args],check=True,stdout=subprocess.DEVNULL)
 assert json.loads((run/(stage+'-execution.json')).read_text('utf-8-sig'))['returncode']==0
for n in range(1,count+1):
 p=json.loads((run/proof).read_text('utf-8-sig'));assert all(v is True for v in p['checks'].values())
 if p['boundaries'] or not p['native_devour_calendar_ready'] or p['maximum_days_to_native_bite_boundary']<30:
  print(json.dumps({'stopped_before_input':before,'boundaries':p['boundaries']}),flush=True);break
 a=json.loads((run/(before+'.audit.json')).read_text('utf-8-sig'));y,m,d=map(int,a['date'].split('.'));assert d==1;m+=1
 if m>12:y+=1;m=1
 end=f'{y:04}.{m:02}.01';after=f'{prefix}-{n:02}'
 call(after+'-calendar','formal_production_native_calendar_checked_v3.py',before,end,after,'30',proof,execution)
 call(after+'-boundary-observation-v2','priority_terravore_construction_boundary_observation_v2.py',before,after,end,'30')
 call(after+'-month-guard-v2','priority_terravore_project2_month_guard_v2.py',before,after)
 before=after;proof=after+'-project2-month-v2-proof.json';execution=after+'-month-guard-v2';p=json.loads((run/proof).read_text('utf-8-sig'));assert len(p['checks'])==27 and all(v is True for v in p['checks'].values())
 print(json.dumps({'step':n,'date':end,'physics_progress':p['physics_progress'],'population_growth':p['natural_growth'],'after_sha256':p['after_sha256'],'boundaries':p['boundaries']}),flush=True)
print(json.dumps({'status':'PASS_BOUNDED_MONTH_DRIVER','final_stage':before}),flush=True)
