"""Twelve native days for the last pair of six genuinely paid mineral ships."""
import json,logging,re,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-six-mineral-build-22800301';stage='terravore-last-paid-mineral-pair-birth-review'
pre=load(before+'-campaign-v8-proof.json');px=load(before+'-campaign-guard-v8-execution.json');a=load(before+'-construction-boundary-observation-v4.json')['after_state']
items={k:v for k,v,x in q.fields(q.block(q.block(a['raw_roots']['construction'],'item_mgr'),'items')) if x and q.scalars(v).get('paying_country')==0};ids=q.ids(q.block(q.block(q.block(q.block(a['raw_roots']['construction'],'queue_mgr'),'queues'),'3'),'items'))
checks={
 'prior24_PASS_actual0_source_original_SAV':len(pre['checks'])==24 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_future_MIA_boundary_not_crossed':pre['boundaries']==['original_native_MIA_return_review'] and a['audit']['date']=='2280.03.01' and q.scalars(a['owned_fleets_raw']['2'])['return_date']=='2280.03.16' and not any(re.search(r'\bfleet\s*=',q.block(q.block(v,'combat'),'in_combat_with')) for v in a['owned_fleets_raw'].values()),
 'last_two_original_paid_orders_work1463_of30':ids==[1392508939,83886114] and set(items)==set(map(str,ids)) and all(q.scalars(v)=={'queue':3,'paying_country':0,'progress':14.63,'progress_needed':30} and q.scalars(q.block(v,'resources'))=={'minerals':225} for v in items.values()) and pre['mineral_ship_count']==5,
 'CN_no_pending_error_exact_held':m['language']=='l_simp_chinese' and not a['pending_country0_raw'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':a['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'start_date':'2280.03.01','end_date':'2280.03.13','days':12,'maximum_days':12,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'remaining_paid_order_raw':items,'scope':'Last genuine paid pair birth only, ending before constructor return. No already completed birth, overcapacity economics or invasion claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
