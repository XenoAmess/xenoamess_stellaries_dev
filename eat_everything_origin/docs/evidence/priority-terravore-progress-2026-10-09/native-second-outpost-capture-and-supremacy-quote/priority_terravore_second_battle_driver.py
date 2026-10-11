"""At most three independent one-day checks of the known native outpost battle."""
import json,logging,re,shutil,subprocess,sys
from pathlib import Path
from decimal import Decimal as D
start,label,raw_steps=sys.argv[1:];limit=int(raw_steps)
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
assert meta['version']=='0.2.0' and meta['language']=='l_simp_chinese'
assert re.fullmatch(r'terravore-[a-z0-9-]{1,80}',label) and 1<=limit<=3
assert not list(run.glob(label+'*'))
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
load=lambda n:json.loads((run/n).read_text('utf-8'))
observer=Path('_runtime/heart-of-devouring/priority_terravore_war1_battle_observer_v52.py')
assert h.sha256(observer)=='aa9bdddfcf53d31f16ae24eebdb5d4f1300c778356f087d3e1a66edb8a3b411e'
record=Path('_runtime/heart-of-devouring/record_current_helper.py');calendar=Path('_runtime/heart-of-devouring/formal_production_native_calendar_checked_v2.py')
def ready(stage):
 p=load(stage+'-war1-battle-v52-proof.json');e=load(stage+'-battle-v52-execution.json');a=load(stage+'.audit.json')
 assert p['status'].startswith('PASS_') and len(p['checks'])==83 and all(v is True for v in p['checks'].values())
 assert e['returncode']==0 and e['helper_sha256']==h.sha256(observer)==h.sha256(run/observer.name)
 assert p['after_sha256']==a['save_sha256']==h.sha256(run/(stage+'.sav'))
 assert p['known_outpost_battle_calendar_ready'] is True and p['actual_active_owned_combat']=={'198':[825]}
 assert p['bounded_construction_calendar_ready'] is False and p['colony523_order_recovery_pending'] is True and p['short_idle_war_calendar_ready'] is False
 assert not p['actual_pending'] and not p['actual_pending_destroyed_ship_ids'] and len(p['actual_alive_military_ship_ids'])==27
 return p,a
def one_day(date):
 y,m,d=map(int,date.split('.'));assert 1<=m<=12 and 1<=d<=30
 n=y*360+(m-1)*30+d;y,n=divmod(n,360);m,d=divmod(n,30)
 return f'{y}.{m+1:02d}.{d+1:02d}'
steps=[];current=start;attempt=None;stop='step_limit'
try:
 for index in range(1,limit+1):
  p,a=ready(current)
  if D(str(p['actual_outpost1090_state']['hitpoints']))<=4500:stop='outpost_hull_at_or_below4500';break
  if D(p['actual_rear_shipyard_progress'])>=179 or D(p['actual_generator7_progress'])+D('1.4')>=240 or a['date']>='2272.01.30':stop='construction_or_annual_boundary';break
  stage=f'{label}-step{index}';end=one_day(a['date']);attempt={'stage':stage,'from':a['date'],'to':end,'calendar_actual0':False,'observer_actual0':False}
  subprocess.run([sys.executable,'-X','utf8',str(record),stage+'-calendar',str(calendar),current,end,stage,'1',current+'-war1-battle-v52-proof.json',current+'-battle-v52'],check=True,stdout=subprocess.DEVNULL)
  attempt['calendar_actual0']=True
  subprocess.run([sys.executable,'-X','utf8',str(record),stage+'-battle-v52',str(observer),current,stage],check=True,stdout=subprocess.DEVNULL)
  attempt['observer_actual0']=True
  np,na=ready(stage);steps.append({'stage':stage,'date':na['date'],'save_sha256':np['after_sha256'],'outpost_hp':np['actual_outpost1090_state']['hitpoints'],'shipyard_progress':np['actual_rear_shipyard_progress'],'generator_progress':np['actual_generator7_progress']});current=stage;attempt=None
except BaseException as err:
 h.write_json(run/(label+'-batch-result.json'),{'status':'STOPPED_ORIGINAL_FAILURE_RETAINED','validated_steps':steps,'last_valid_stage':current,'attempted_stage':attempt,'error_type':type(err).__name__,'error':str(err),'scope':'One-day observations only; attempted native time remains real even when validation fails. No retries.'})
 raise
result={'status':'PASS_BOUNDED_KNOWN_NATIVE_OUTPOST_BATTLE','validated_steps':steps,'last_stage':current,'stop':stop,'scope':'At most three independent one-day checks; no victory, route recovery or full acceptance.'}
h.write_json(run/(label+'-batch-result.json'),result);print(json.dumps(result),flush=True)
