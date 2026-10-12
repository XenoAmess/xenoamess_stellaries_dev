"""Only12 days from completed society replacement to first native full budget; stop before storm."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-society-zone-completed-22840619';a=read_state(run,before);p=load(before+'-society-zone-completion-proof.json');x=load(before+'-society-zone-completed-guard-execution.json');sources=load('terravore-society-zone-priority-22831001-society-construction-first-month-review.json')['sources'];contact=q.block(q.block(a['roots']['first_contacts'],'contacts'),'63')
checks={
 'prior19PASS_actual0_source_exactSAV':len(p['checks'])==19 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'completed_society_three_labs_and_six_paid_hives':p['boundaries']==['post_conversion_month_budget_review','native_storm1815_due_review'] and q.ids(q.block(a['queues']['0'],'items'))==[268435492,251658284,1191182345,117440553,1476395019,117440546] and q.scalars(a['items']['268435492'])['progress']==22.4 and q.ids(q.block(q.block(a['roots']['zones'],'67108970'),'buildings'))==[16777251,83886120,16777323],
 'only12days_to_new_budget_no_pending_storm15_contact80':a['audit']['date']=='2284.06.19' and p['project3_progress']==1282.66121 and not a['pending'] and q.scalars(contact)['leader']==4294967295 and q.scalars(contact)['days_left']==80 and not q.block(contact,'event') and any(k=='delayed_event' and q.scalars(v).get('event')=='cstorms.1815' and q.scalars(v).get('days')==15 for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj),
 'CN_same41_package_error627_native_sources_preserved':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(before+'-society-first-budget-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2284.06.19','end_date':'2284.07.01','days':12,'maximum_days':12,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-society-first-budget-review','sources':sources,'scope':'First native new-month budget after completed replacement; zero research tick and no storm/contact outcome.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
