"""Documented at most two bounded paid construction core intervals, stop at any boundary."""
import concurrent.futures,json,logging,re,subprocess,sys
from pathlib import Path
start,label,raw_limit=sys.argv[1:];limit=int(raw_limit)
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8'))
assert meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and 1<=limit<=2 and re.fullmatch(r'terravore-[a-z0-9-]{1,80}',label) and not list(run.glob(label+'*'))
record=run/'record_current_helper.py';calendar=run/'formal_production_native_calendar_checked_v2.py';obs=run/'priority_terravore_construction_boundary_observation.py';inv=run/'priority_terravore_rear97_native_inventory_v4.py';guard=run/'priority_terravore_mother_build_monthly_core_guard.py'
assert h.sha256(record)=='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3' and h.sha256(calendar)=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and h.sha256(obs)=='e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678' and h.sha256(inv)=='e6e8ca9f31893549b6990f5ae2db24df49b212da6fdf864b91b585c86a6d4b20' and h.sha256(guard)=='b3804211f7f95c0bb47b81437c2a6cac70f0c32ebb82c45cc3a626e9b207fb9f'
def proof(stage):
 p=load(stage+'-monthly-build-core-proof.json');e=load(stage+'-monthly-build-core-guard-execution.json');a=load(stage+'.audit.json')
 assert e['returncode']==0 and e['helper_sha256']==h.sha256(guard) and len(p['checks'])==24 and all(v is True for v in p['checks'].values()) and p['after_sha256']==a['save_sha256']==h.sha256(run/(stage+'.sav'))
 return p,a

def date_plus(date,days):
 y,m,d=map(int,date.split('.'));n=y*360+(m-1)*30+d-1+days;y,n=divmod(n,360);m,d=divmod(n,30);return f'{y}.{m+1:02d}.{d+1:02d}'

def invoke(stage,helper,*args):
 subprocess.run([sys.executable,'-X','utf8',str(record),stage,str(helper),*map(str,args)],check=True,stdout=subprocess.DEVNULL)

steps=[];current=start;attempt=None;stop='interval_limit'
try:
 for index in range(1,limit+1):
  p,a=proof(current)
  assert p['status']=='PASS_NATIVE_TERRAVORE_MONTHLY_BUILD_CORE_COMPONENT' and p['monthly_build_calendar_ready'] is True and not p['boundaries']
  if a['date']>='2272.11.26':stop='date_limit';break
  span=p['maximum_days_to_monthly_build_boundary'];assert 1<=span<=300
  while date_plus(a['date'],span)>'2272.11.26':span-=1
  assert 1<=span<=30
  end=date_plus(a['date'],span);stage=f'{label}-step{index}';attempt={'stage':stage,'from':a['date'],'to':end,'days':span,'calendar_actual0':False,'observations_actual0':False,'guard_actual0':False}
  invoke(stage+'-calendar',calendar,current,end,stage,span,current+'-monthly-build-core-proof.json',current+'-monthly-build-core-guard');attempt['calendar_actual0']=True
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   futures=[pool.submit(invoke,stage+'-boundary-observation',obs,current,stage,end,span),pool.submit(invoke,stage+'-rear97-native-inventory-v4',inv,current,stage)]
   results=[f.exception() for f in futures]
  assert not any(results),[repr(v) for v in results if v];attempt['observations_actual0']=True
  invoke(stage+'-monthly-build-core-guard',guard,current,stage);attempt['guard_actual0']=True
  np,na=proof(stage);steps.append({'stage':stage,'date':na['date'],'days':span,'save_sha256':np['after_sha256'],'status':np['status'],'boundaries':np['boundaries'],'base':np['rear_station_health'],'colonizer_work':np['actual_colonizer_work'],'population':np['actual_population'],'native_new_lost_military':np['native_new_lost_military'],'alive_military':len(np['alive_military_ship_ids'])});current=stage;attempt=None
  print(json.dumps(steps[-1]),flush=True)
  if np['status']!='PASS_NATIVE_TERRAVORE_MONTHLY_BUILD_CORE_COMPONENT' or np['monthly_build_calendar_ready'] is not True:stop='observed_native_boundary';break
except BaseException as err:
 h.write_json(run/(label+'-batch-result.json'),{'status':'STOPPED_ORIGINAL_FAILURE_RETAINED','validated_steps':steps,'last_valid_stage':current,'attempted_stage':attempt,'error_type':type(err).__name__,'error':str(err),'scope':'Actual native time at attempted stage remains real; no retry.'});raise
result={'status':'STOPPED_NATIVE_MONTHLY_BUILD_BOUNDARY' if stop=='observed_native_boundary' else 'PASS_BOUNDED_NATIVE_MONTHLY_BUILD_CORE_OBSERVATIONS','steps':steps,'last_stage':current,'stop':stop,'scope':'At most two scoped Mod core intervals, at most thirty days each, before Nov27 native timer, no full acceptance.'};h.write_json(run/(label+'-batch-result.json'),result);print(json.dumps(result),flush=True)
