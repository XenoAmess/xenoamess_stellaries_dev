"""At most four native monthly intervals, stop on failure or business boundary."""
import json,os,subprocess,sys
from pathlib import Path
before,proof,execution,raw_count=sys.argv[1:];count=int(raw_count);assert 1<=count<=4
child_env=os.environ.copy();child_env['PYTHONPATH']=str(Path('eat_everything_origin/tools').resolve())+os.pathsep+child_env.get('PYTHONPATH','')
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z');completed=[];halt='finite_interval_limit'
def invoke(stage,helper,args):
 result=subprocess.run([sys.executable,str(run/'record_current_helper.py'),stage,str(run/helper),*args],capture_output=True,env=child_env)
 print(result.stdout.decode('utf-8',errors='replace'),end='',flush=True)
 print(result.stderr.decode('utf-8',errors='replace'),end='',flush=True)
 assert result.returncode==0,'Original actual nonzero retained; no continuation'
for _ in range(count):
 audit=json.loads((run/(before+'.audit.json')).read_text('utf-8'));year,month,day=map(int,audit['date'].split('.'));assert day==1
 month+=1
 if month==13:year+=1;month=1
 end=f'{year:04d}.{month:02d}.01';after=f'terravore-overcap-full-month-{year:04d}{month:02d}01'
 invoke(after+'-calendar','formal_production_native_calendar_checked_v5.py',[before,end,after,'30',proof,execution])
 invoke(after+'-boundary-observation-v4','priority_terravore_construction_boundary_observation_v4.py',[before,after,end,'30'])
 invoke(after+'-campaign-guard-v10','priority_terravore_campaign_guard_v10.py',[before,after])
 proof=after+'-campaign-v10-proof.json';execution=after+'-campaign-guard-v10';state=json.loads((run/proof).read_text('utf-8'));completed.append({'stage':after,'proof':proof,'execution':execution,'save_sha256':state['after_sha256']});before=after
 if not state['native_devour_calendar_ready']:halt='business_boundary_requires_review';break
 if state['new_paid_armies']:halt='native_paid_army_born_collect_CN_UI';break
print(json.dumps({'status':'FINITE_NATIVE_CAMPAIGN_INTERVALS_COMPLETED','completed':completed,'halt_reason':halt,'scope':'Bounded component execution only; not complete route acceptance.'}),flush=True)
