"""Only18 days from paid336work to native zone replacement; no storm/month boundary."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-society-construction-month-22840601';a=read_state(run,before);p=load(before+'-society-construction-month-v7-proof.json');x=load(before+'-society-construction-month-guard-v7-execution.json');sources=load('terravore-society-zone-priority-22831001-society-construction-first-month-review.json')['sources'];contact=q.block(q.block(a['roots']['first_contacts'],'contacts'),'63')
checks={
 'prior23PASS_actual0_source_exactSAV':len(p['checks'])==23 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'paid800_conversion336of360_front_original_three_lab_IDs':p['boundaries']==['paid_society_zone_completion_review'] and q.ids(q.block(a['queues']['0'],'items'))==[83886115,268435492,251658284,1191182345,117440553,1476395019,117440546] and q.scalars(a['items']['83886115'])=={'queue':0,'paying_country':0,'progress':336,'progress_needed':360} and q.scalars(q.block(a['items']['83886115'],'resources'))=={'minerals':800} and q.ids(q.block(q.block(a['roots']['zones'],'16777323'),'buildings'))==[16777251,83886120,16777323] and q.scalars(a['items']['268435492'])['progress']==22.4,
 'only18days_one_cached_tick_no_pending_storm33_contact80':a['audit']['date']=='2284.06.01' and p['project3_progress']==1213.59142 and not a['pending'] and q.scalars(contact)['leader']==4294967295 and q.scalars(contact)['days_left']==80 and not q.block(contact,'event') and any(k=='delayed_event' and q.scalars(v).get('event')=='cstorms.1815' and q.scalars(v).get('days')==33 for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj),
 'CN_same41_package_error627_native_sources_preserved':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(before+'-society-zone-completion-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2284.06.01','end_date':'2284.06.19','days':18,'maximum_days':18,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-society-zone-completion-review','sources':sources,'scope':'Normal paid zone completion only; one cached research tick, no new month/storm/contact outcome.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
