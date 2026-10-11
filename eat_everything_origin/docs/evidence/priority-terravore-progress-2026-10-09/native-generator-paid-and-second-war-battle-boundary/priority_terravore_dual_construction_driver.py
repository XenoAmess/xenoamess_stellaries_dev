"""Bounded native paid dual-construction observation, no mission restoration claim."""
import json,logging,re,shutil,subprocess,sys
from pathlib import Path
from decimal import Decimal as D,ROUND_CEILING
start,label,target,raw_days=sys.argv[1:];requested=int(raw_days)
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
assert re.fullmatch(r'terravore-[a-z0-9-]{1,80}',label) and 1<=requested<=90
assert not list(run.glob(label+'*'))
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
load=lambda n:json.loads((run/n).read_text('utf-8'))
def ordinal(date):
 y,m,d=map(int,date.split('.'));assert 1<=m<=12 and 1<=d<=30
 return y*360+(m-1)*30+d-1
def date_after(date,days):
 x=ordinal(date)+days;y,rest=divmod(x,360);m,d=divmod(rest,30)
 return f'{y}.{m+1:02d}.{d+1:02d}'
initial=load(start+'.audit.json');validate_native_interval(initial['date'],target,requested)
assert meta['version']=='0.2.0' and meta['language']=='l_simp_chinese'
observer=Path('_runtime/heart-of-devouring/priority_terravore_war1_battle_observer_v50.py')
assert h.sha256(observer)=='2fa9fac6b7010d9756a65a13f5bb54ca0021159412b513e15dd99586193b5da9'
def ready(stage):
 p=load(stage+'-war1-battle-v50-proof.json');e=load(stage+'-battle-v50-execution.json');a=load(stage+'.audit.json')
 assert p['status'].startswith('PASS_') and len(p['checks'])==80 and all(v is True for v in p['checks'].values())
 assert e['returncode']==0 and e['helper_sha256']==h.sha256(observer)==h.sha256(run/observer.name)
 assert p['after_sha256']==a['save_sha256']==h.sha256(run/(stage+'.sav'))
 assert p['bounded_construction_calendar_ready'] is True and p['colony523_order_recovery_pending'] is True and p['short_idle_war_calendar_ready'] is False
 assert not p['actual_pending'] and not p['actual_active_owned_combat'] and len(p['actual_alive_military_ship_ids'])==27
 return p,a
record=Path('_runtime/heart-of-devouring/record_current_helper.py');calendar=Path('_runtime/heart-of-devouring/formal_production_native_calendar_checked_v2.py')
steps=[];current=start;total=0;stop='requested_interval_complete'
try:
 for index in range(1,4):
  p,a=ready(current);remaining=requested-total
  if remaining<=0:break
  shipyard_remaining=179-int(D(p['actual_rear_shipyard_progress']))
  generator_remaining=int(((D(240)-D(p['actual_generator7_progress']))/D('1.4')).to_integral_value(rounding=ROUND_CEILING))-1
  annual_remaining=ordinal('2272.01.30')-ordinal(a['date'])
  days=min(30,remaining,shipyard_remaining,generator_remaining,annual_remaining)
  if days<=0:stop='construction_or_annual_boundary';break
  stage=f'{label}-step{index}';end=date_after(a['date'],days)
  subprocess.run([sys.executable,'-X','utf8',str(record),stage+'-calendar',str(calendar),current,end,stage,str(days),current+'-war1-battle-v50-proof.json',current+'-battle-v50'],check=True,stdout=subprocess.DEVNULL)
  subprocess.run([sys.executable,'-X','utf8',str(record),stage+'-battle-v50',str(observer),current,stage],check=True,stdout=subprocess.DEVNULL)
  new,na=ready(stage);steps.append({'stage':stage,'date':na['date'],'days':days,'save_sha256':na['save_sha256'],'shipyard_progress':new['actual_rear_shipyard_progress'],'generator_progress':new['actual_generator7_progress']});current=stage;total+=days
 if total<requested and len(steps)==3:stop='three_step_limit'
except BaseException as error:
 h.write_json(run/(label+'-batch-result.json'),{'status':'STOPPED_ORIGINAL_FAILURE_RETAINED','steps':steps,'days':total,'last_valid_stage':current,'error_type':type(error).__name__,'error':str(error),'scope':'No repeated commands; failed attempted next stage retained separately.'})
 raise
result={'status':'PASS_BOUNDED_NATIVE_DUAL_CONSTRUCTION_BATCH','steps':steps,'days':total,'last_stage':current,'stop':stop,'scope':'Only original two construction orders before first completion, colony still parked and route unresolved. No full route acceptance.'}
h.write_json(run/(label+'-batch-result.json'),result);print(json.dumps(result),flush=True)
