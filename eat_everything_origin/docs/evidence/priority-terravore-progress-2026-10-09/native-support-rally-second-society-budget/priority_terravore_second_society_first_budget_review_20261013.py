"""Read-only preflight for the first native month ledger after the second society zone."""
import json, logging, sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools'); sys.argv=['runtime']
import runtime as r, audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-second-society-completed-22870119';a=read_state(run,before)
p=load(before+'-second-society-zone-completion-proof.json');x=load(before+'-second-society-zone-completion-guard-execution.json')
ids=q.ids(q.block(a['queues']['0'],'items'))
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
checks={
 'prior19PASS_actual0_source_exactSAV':p['status']=='PASS_NATIVE_SECOND_PAID_SOCIETY_ZONE' and len(p['checks'])==19 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='5b5df4421763b65eddb3843f944a04f64cd79ab282003859658bbd16dd66522e' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'new_society119_original_labs_and_four_paid_hives':p['boundaries']==['post_second_society_conversion_month_budget_review'] and a['audit']['districts']['1']['zones']==[0,67108970,119] and q.scalars(q.block(a['roots']['zones'],'119'))=={'type':'zone_research_society'} and q.ids(q.block(q.block(a['roots']['zones'],'119'),'buildings'))==[33554447,50331690,16777354] and ids==[1191182345,117440553,1476395019,117440546] and q.scalars(a['items']['1191182345'])['progress']==2.8,
 'only13days_to_Feb1_no_day2_tick_pending_event_combat':a['audit']['date']=='2287.01.19' and p['project3_progress']==6218.77182 and not a['pending'] and not delays and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'CN41_same_production_and_live_error':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());stage=before+'-second-society-first-budget-review';out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2287.01.19','end_date':'2287.02.01','days':13,'maximum_days':13,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'scope':'One native new-month budget for two society zones, no day2 research tick or manual payment.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
