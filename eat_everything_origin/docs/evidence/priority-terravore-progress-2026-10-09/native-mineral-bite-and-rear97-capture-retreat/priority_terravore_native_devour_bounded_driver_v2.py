"""Bounded documented native devour waiting; existing calendar and guards only."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

run=Path(__file__).parent
start,proof_name,execution_stage,label,limit,raw_steps=sys.argv[1:]
maximum_steps=int(raw_steps);assert 1<=maximum_steps<=6
wrapper=run/'record_current_helper.py'
calendar=run/'formal_production_native_calendar_checked_v2.py'
observer=run/'priority_terravore_construction_boundary_observation.py'
guard=run/'priority_terravore_fourth_native_devour_wait_guard_v3.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda name:json.loads((run/name).read_text('utf-8'))
def ordinal(date):
 y,m,d=map(int,date.split('.'));return y*360+(m-1)*30+d-1
def dated(value):
 y,remainder=divmod(value,360);m,d=divmod(remainder,30);return f'{y:04d}.{m+1:02d}.{d+1:02d}'
def invoke(stage,helper,args):
 cmd=[sys.executable,'-X','utf8',str(wrapper),stage,str(helper),*map(str,args)]
 p=subprocess.run(cmd,capture_output=True)
 receipt=load(stage+'-execution.json')
 assert p.returncode==receipt['returncode']==0,(stage,p.returncode,p.stderr.decode(errors='replace'))
 assert receipt['helper_sha256']==sha(helper)
 return receipt
assert sha(guard)=='ff8e46d30640ff1e49ad0fa3bb6297d4cf1073ee12e6535e379b0e2dd3342813'
assert not list(run.glob(label+'*')),'Unique batch label required'
cap=ordinal(limit);assert cap<=ordinal('2278.01.30')
assert 0<cap-ordinal(load(proof_name)['date'])<=maximum_steps*90
steps=[]
for index in range(1,maximum_steps+1):
 pre=load(proof_name);exe=load(execution_stage+'-execution.json')
 assert pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values()) and exe['returncode']==0 and exe['helper_sha256']==sha(guard)
 assert pre['after_sha256']==sha(run/(start+'.sav'))
 current=ordinal(pre['date'])
 if current>=cap:break
 maximum=pre['maximum_days_to_native_bite_boundary']
 if maximum>0:
  assert pre['native_devour_calendar_ready'] and not pre['boundaries']
  days=min(maximum,cap-current,90)
 else:
  print(json.dumps({'stopped':'review_required','date':pre['date'],'boundaries':pre['boundaries']}),flush=True);break
 end=dated(current+days);stage=f'{label}-{index:02d}'
 print(json.dumps({'step':index,'start':pre['date'],'end':end,'days':days}),flush=True)
 invoke(stage+'-calendar',calendar,[start,end,stage,days,proof_name,execution_stage])
 invoke(stage+'-boundary-observation',observer,[start,stage,end,days])
 invoke(stage+'-native-devour-wait-guard-v3',guard,[start,stage])
 result=load(stage+'-native-devour-wait-v3-proof.json')
 assert all(v is True for v in result['checks'].values())
 item={'stage':stage,'date':result['date'],'checks':len(result['checks']),'boundaries':result['boundaries'],'progress':result['situation_progress'],'mother_population':result['mother_population'],'source_population':result['source_population'],'save_sha256':result['after_sha256']}
 steps.append(item);print(json.dumps(item),flush=True)
 start=stage;proof_name=stage+'-native-devour-wait-v3-proof.json';execution_stage=stage+'-native-devour-wait-guard-v3'
 if result['boundaries']:break
receipt={'status':'PASS_BOUNDED_NATIVE_DEVOUR_WAIT_DRIVER','steps':steps,'final_stage':start,'final_proof':proof_name,'scope':'Bounded orchestration only, not native bite, settlement, Queen C60 or route acceptance.'}
(run/(label+'-driver-result.json')).write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps({'status':receipt['status'],'steps':len(steps),'final_stage':start}),flush=True)
