"""Bounded sequential native observation; never retries or repairs failures."""
import json, re, shutil, subprocess, sys
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
before, proof_name, execution_stage, prefix, limit, steps = sys.argv[1:]
steps = int(steps)
assert 1 <= steps <= 3 and re.fullmatch(r'[a-z0-9-]{1,42}', prefix)
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r
h = r.harness
run, user, metadata = h.load_run()
assert metadata['version'] == '0.2.0' and metadata['language'] == 'l_simp_chinese'
dest = run / Path(__file__).name
assert not dest.exists() or dest.read_bytes() == Path(__file__).read_bytes()
if not dest.exists(): shutil.copyfile(__file__, dest)
root = Path('_runtime/heart-of-devouring')
sources = {
    'record_current_helper.py':'7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3',
    'formal_production_native_calendar_checked_v2.py':'66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
    'priority_terravore_war1_battle_observer_v9.py':'a39f884b439203a964353ed00c8111f732aa1fcd34ab7b71f9bd0be3d52a0717',
}
def load(name): return json.loads((run / name).read_text('utf-8'))
def ordinal(date):
    y,m,d = map(int,date.split('.'))
    assert 1 <= m <= 12 and 1 <= d <= 30
    return y*360+(m-1)*30+d-1
def date_after(date,days):
    n=ordinal(date)+days
    return f'{n//360:04d}.{n%360//30+1:02d}.{n%30+1:02d}'
def validate(stage,pname,ename):
    p=load(pname);e=load(ename+'-execution.json')
    assert p['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT'
    assert p['checks'] and all(v is True for v in p['checks'].values())
    assert p['short_combat_calendar_ready'] is True and p['actual_pending']==[]
    assert p['after_sha256']==h.sha256(run/(stage+'.sav'))
    assert e['returncode']==0 and e['command'][-1]==stage
    assert e['helper_sha256']==sources['priority_terravore_war1_battle_observer_v9.py']
    assert h.sha256(run/'priority_terravore_war1_battle_observer_v9.py')==e['helper_sha256']
    assert e['wrapper_sha256']==sources['record_current_helper.py']
    assert all(h.sha256(root/name)==sha for name,sha in sources.items())
    return p
def invoke(stage,helper,args):
    assert not (run/(stage+'-execution.json')).exists()
    result=subprocess.run([sys.executable,str(root/'record_current_helper.py'),stage,str(root/helper),*args],check=False)
    assert result.returncode==0
    receipt=load(stage+'-execution.json')
    assert receipt['returncode']==0 and receipt['helper_sha256']==sources[helper]
    assert receipt['wrapper_sha256']==sources['record_current_helper.py']

assert not (run/(prefix+'-batch-result.json')).exists()
if prefix=='terravore-war1-bounded2':
    old=load('terravore-war1-bounded1-driver-execution.json')
    oldcal=load('terravore-war1-bounded1-step1-calendar-execution.json')
    assert old['returncode']==oldcal['returncode']==1
    assert old['helper_sha256']==h.sha256(run/'priority_terravore_bounded_defense_driver.py')=='900cf5a65a8f4c66f3a670491a17038accbc171bbb7d6478c9b5f4955d989b3e'
    assert oldcal['helper_sha256']==sources['formal_production_native_calendar_checked_v2.py']
    assert 'Stage already has artifacts; do not repeat calendar' in (run/'terravore-war1-bounded1-step1-calendar-stderr.txt').read_text('utf-8')
    assert (run/'terravore-war1-bounded1-step1-calendar-stdout.txt').read_bytes()==b''
    assert not any((run/('terravore-war1-bounded1-step1'+suffix)).exists() for suffix in ['.sav','-calendar-receipt.json','-error-before.log'])
    assert before=='terravore-war1-defense-three-days17'
initial=validate(before,proof_name,execution_stage)
assert 0 < ordinal(limit)-ordinal(initial['date']) <= 9
total=0;results=[];stop='step_limit'
for index in range(1,steps+1):
    previous=validate(before,proof_name,execution_stage)
    remaining=ordinal(limit)-ordinal(previous['date'])
    if remaining<=0: stop='date_limit';break
    hp=D(str(previous['actual_base0_ship_state']['hitpoints']))
    assert hp>0 and previous['actual_base0_ship_state']['original_owner']==0
    front=[D(str(v)) for v in previous['front_order_progress']]
    assert front and all(0<=v<60 for v in front)
    until_birth=min(int(((D(60)-v)/D('1.58')).to_integral_value(rounding=ROUND_CEILING)) for v in front)
    days=min(3,6 if hp>1000 else 3 if hp>500 else 1,remaining,9-total,until_birth)
    assert days>0
    stage=f'{prefix}-step{index}'
    next_date=date_after(previous['date'],days)
    plan=run/(prefix+'-dispatch-plan-step'+str(index)+'.json')
    assert not plan.exists() and not (run/(stage+'.sav')).exists()
    h.write_json(plan,{'before':before,'date':next_date,'days':days,'prior_proof':proof_name,'prior_execution':execution_stage,'base_hp':str(hp),'days_until_birth':until_birth,'scope':'Unique bounded native calendar, independently checked before any next dispatch.'})
    invoke(stage+'-calendar','formal_production_native_calendar_checked_v2.py',[before,next_date,stage,str(days),proof_name,execution_stage])
    invoke(stage+'-battle-v9','priority_terravore_war1_battle_observer_v9.py',[before,stage])
    proof_name=stage+'-war1-battle-v9-proof.json';execution_stage=stage+'-battle-v9'
    current=validate(stage,proof_name,execution_stage)
    total+=days
    results.append({'stage':stage,'date':next_date,'days':days,'base_hp':current['actual_base0_ship_state']['hitpoints'],'new_paid':current['actual_new_paid_ships'],'new_lost':current['actual_lost_military_requires_separate_combat_evidence'],'checks':len(current['checks'])})
    before=stage
    print(json.dumps({'checkpoint':results[-1]},ensure_ascii=True),flush=True)
    if current['actual_new_paid_ships']: stop='new_paid_birth';break
    if current['actual_lost_military_requires_separate_combat_evidence']: stop='new_loss';break
    if D(current['actual_menace_delta'])!=0: stop='menace_changed';break
    if current['actual_base0_ship_state']['hitpoints']<=200: stop='base_at_or_below200';break
    if D(str(current['actual_base0_ship_state']['hitpoints']))<hp: stop='base_hull_declined';break
    if current['actual_base0_ship_state']['hitpoints']<=500:
        engaged=[current['actual_fleet_details'][fid] for fid in current['actual_owned_military'] if current['actual_active_owned_combat'].get(fid)]
        if not engaged: stop='no_engaged_military_reinforcement';break
        full=all(ship.get('hitpoints',0)==ship['max_hitpoints'] and ship.get('armor_hitpoints',0)==ship.get('max_armor_hitpoints',0) and ship.get('shield_hitpoints',0)==ship.get('max_shield_hitpoints',0) for fleet in engaged for ship in fleet['ship_states'].values())
        if not full: stop='engaged_reinforcement_damaged';break
    if current['actual_active_owned_combat'].get('0')!=[825]: stop='base_combat_changed';break
    if total>=9: stop='nine_day_limit';break
summary={'status':'COMPLETED_BOUNDED_OBSERVATIONS','stop':stop,'steps':results,'last_stage':before,'last_proof':proof_name,'last_execution':execution_stage,'days':total,'scope':'No full-route acceptance or victory claim; original individual checks and actual exits remain authoritative.'}
h.write_json(run/(prefix+'-batch-result.json'),summary)
print(json.dumps(summary,ensure_ascii=True),flush=True)
