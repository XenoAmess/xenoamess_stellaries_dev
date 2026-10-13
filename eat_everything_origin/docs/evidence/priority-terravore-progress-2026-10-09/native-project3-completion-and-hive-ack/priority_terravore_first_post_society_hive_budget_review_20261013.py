"""Read-only preflight of the two native days to the first post-hive ledger."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-first-post-conversion-hive-completed-22871230';s=read_state(run,before);a=s['audit'];c=a['countries']['0']
p=load(before+'-first-post-society-hive-completion-proof.json');x=load(before+'-first-post-society-hive-completion-guard-execution.json')
ids=q.ids(q.block(s['queues']['0'],'items'))
raw=c['research_queues']['society_queue'];ts=list(q.tokens(raw));project=q.scalars(raw[ts[0][2]:ts[-1][1]])
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(s['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
checks={
 'prior18PASS_actual0_source_exactSAV':p['status']=='PASS_NATIVE_FIRST_HIVE_AFTER_TWO_SOCIETY_ZONES' and len(p['checks'])==18 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='9fe6fd06eb2ca5b00c5da6161ad0a5e52cbe6346f5e8930f1dd610d5efa81716' and p['after_sha256']==a['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_two_native_days_to_Jan1_three_original_paid_hives':a['date']=='2287.12.30' and p['boundaries']==['first_hive_new_month_budget_review'] and ids==[117440553,1476395019,117440546] and all(q.scalars(s['items'][str(i)])['progress']==0 and q.scalars(q.block(s['items'][str(i)],'resources'))=={'minerals':400} for i in ids),
 'hive8_two_society_zones_S2280_E360_project3_pending':a['districts']['1']=={'type':'district_hive','level':8,'zones':[0,67108970,119]} and [a['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2280,360] and project['special_project']==9 and project['progress']==9317.78873,
 'no_pending_delayed_event_combat_or_ship_order':not s['pending'] and not delays and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in s['fleets'].values()) and not q.ids(q.block(s['queues'].get('3',''),'items')),
 'CN41_same_production_and_live_error':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());stage=before+'-first-hive-budget-review';out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['save_sha256'],'after_sha256':a['save_sha256'],'start_date':'2287.12.30','end_date':'2288.01.01','days':2,'maximum_days':2,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'scope':'First new-month ledger after hive8; no Jan2 research tick.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
