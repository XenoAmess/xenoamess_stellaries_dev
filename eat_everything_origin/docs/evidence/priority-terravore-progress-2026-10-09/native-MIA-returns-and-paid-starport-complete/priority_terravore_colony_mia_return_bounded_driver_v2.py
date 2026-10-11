"""Bounded documented native MIA return dates; existing calendar and guards only."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

run=Path(__file__).parent
start,proof_name,execution_stage,label=sys.argv[1:]
wrapper=run/'record_current_helper.py'
calendar=run/'formal_production_native_calendar_checked_v2.py'
observer=run/'priority_terravore_construction_boundary_observation.py'
guard=run/'priority_terravore_fourth_colonization_wait_guard_v4.py'
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
assert sha(guard)=='558c68de96a19458c6d87871fc90cdee344892248a9d782e837d8153b52c33be'
assert not list(run.glob(label+'*')),'Unique batch label required'
cap=ordinal('2274.05.05');known_pre={'2274.04.06','2274.04.07','2274.04.14','2274.04.15','2274.04.18','2274.04.19','2274.05.03','2274.05.04'}
steps=[]
for index in range(1,10):
 pre=load(proof_name);exe=load(execution_stage+'-execution.json')
 assert pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values()) and exe['returncode']==0 and exe['helper_sha256']==sha(guard)
 assert pre['after_sha256']==sha(run/(start+'.sav'))
 current=ordinal(pre['date'])
 if current>=cap:break
 maximum=pre['maximum_days_to_colonization_boundary']
 if maximum>0:
  assert pre['native_colonization_calendar_ready'] and not pre['boundaries']
  days=min(maximum,cap-current,90)
 elif pre['date'] in known_pre and not pre['boundaries'] and not pre['actual_pending'] and not pre['active_combat_fleets']:
  days=1
 else:
  print(json.dumps({'stopped':'review_required','date':pre['date'],'boundaries':pre['boundaries']}),flush=True);break
 end=dated(current+days);stage=f'{label}-{index:02d}'
 print(json.dumps({'step':index,'start':pre['date'],'end':end,'days':days}),flush=True)
 invoke(stage+'-calendar',calendar,[start,end,stage,days,proof_name,execution_stage])
 invoke(stage+'-boundary-observation',observer,[start,stage,end,days])
 invoke(stage+'-colonization-wait-guard-v4',guard,[start,stage])
 result=load(stage+'-target523-colonization-wait-v4-proof.json')
 assert all(v is True for v in result['checks'].values())
 item={'stage':stage,'date':result['date'],'checks':len(result['checks']),'boundaries':result['boundaries'],'reviewed_returns':result['reviewed_native_MIA_returns'],'save_sha256':result['after_sha256']}
 steps.append(item);print(json.dumps(item),flush=True)
 start=stage;proof_name=stage+'-target523-colonization-wait-v4-proof.json';execution_stage=stage+'-colonization-wait-guard-v4'
 if result['boundaries']:break
receipt={'status':'PASS_BOUNDED_NATIVE_MIA_RETURN_DRIVER','steps':steps,'final_stage':start,'final_proof':proof_name,'scope':'Bounded orchestration only, not colony completion or route acceptance.'}
(run/(label+'-driver-result.json')).write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps({'status':receipt['status'],'steps':len(steps),'final_stage':start}),flush=True)
