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
old=load(before+'-second-society-first-budget-review.json');oldx=load(before+'-second-society-first-budget-review-execution.json')
failedstage='terravore-second-society-first-budget-22870201'
failedx=load(failedstage+'-calendar-execution.json')
ids=q.ids(q.block(a['queues']['0'],'items'))
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
checks={
 'prior19PASS_actual0_source_exactSAV':p['status']=='PASS_NATIVE_SECOND_PAID_SOCIETY_ZONE' and len(p['checks'])==19 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='5b5df4421763b65eddb3843f944a04f64cd79ab282003859658bbd16dd66522e' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'new_society119_original_labs_and_four_paid_hives':p['boundaries']==['post_second_society_conversion_month_budget_review'] and a['audit']['districts']['1']['zones']==[0,67108970,119] and q.scalars(q.block(a['roots']['zones'],'119'))=={'type':'zone_research_society'} and q.ids(q.block(q.block(a['roots']['zones'],'119'),'buildings'))==[33554447,50331690,16777354] and ids==[1191182345,117440553,1476395019,117440546] and q.scalars(a['items']['1191182345'])['progress']==2.8,
 'only13days_to_Feb1_no_day2_tick_pending_event_combat':a['audit']['date']=='2287.01.19' and p['project3_progress']==6218.77182 and not a['pending'] and not delays and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'CN41_same_production_and_live_error':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'original13day_review_and_preGUI_calendar_FAILURE_retained_no_SAV':old['status']=='PASS_REVIEWED_NATIVE_BOUNDARY' and len(old['checks'])==4 and all(v is True for v in old['checks'].values()) and old['days']==13 and old['end_date']=='2287.02.01' and oldx['returncode']==0 and oldx['helper_sha256']=='45fc890441002c9cf3d2a92943e18fdfde291ca43307a7380dde4d1be821f840' and failedx['returncode']==1 and failedx['helper_sha256']=='ffde2c9a4e2df229622ae0813071d45ef748c3a29d51da58d1fa9d588250ef2d' and b'Native30-day date mismatch; no GUI action allowed' in (run/(failedstage+'-calendar-stderr.txt')).read_bytes() and not (run/(failedstage+'.sav')).exists() and not (run/(failedstage+'-calendar-receipt.json')).exists(),
}
passed=all(v is True for v in checks.values());stage=before+'-second-society-first-budget-review-v2';out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2287.01.19','end_date':'2287.02.01','days':12,'maximum_days':12,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'scope':'Corrected 12-day native new-month budget; original 13-day preflight failure retained.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
