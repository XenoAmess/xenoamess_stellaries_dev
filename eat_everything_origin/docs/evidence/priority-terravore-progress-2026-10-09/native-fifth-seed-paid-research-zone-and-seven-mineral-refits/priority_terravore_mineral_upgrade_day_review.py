"""Read-only actual partial mineral upgrades permitting one following native day."""
import json,logging,sys
from pathlib import Path
stage,prior_file,prior_execution,end=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
a=read_state(run,stage);au=a['audit'];pre=load(prior_file);px=load(prior_execution+'-execution.json');minerals={16777746,50333149,50333147,33554923,1960,1961,1962}
order=q.block(q.block(a['fleets']['50332250'],'current_order'),'upgrade_design_at_orbitable_fleet_order');assert order,'No partial upgrade order remains; review the actual completion separately'
raw=q.block(order,'status');rows=[];depth=0;start=None
for token,begin,finish in q.tokens(raw):
 if token=='{':
  if depth==0:start=finish
  depth+=1
 elif token=='}':
  depth-=1;assert depth>=0
  if depth==0:rows.append(raw[start:begin])
 else:assert depth>0
assert depth==0
done=[];active=[];details=[]
for v in rows:
 s=q.scalars(v);ship=s['ship'];impl=q.scalars(q.block(a['ships'][str(ship)],'ship_design_implementation'));iid=str(s['build_queue_item'])
 if s['status']=='upgrade_done':
  valid=impl=={'design':218105405,'upgrade':4294967295,'growth_stage':0} and iid not in a['items'];done.append(ship)
 else:
  it=a['items'].get(iid,'');build=q.block(it,'buildable_ship_upgrade');isv=q.scalars(it)
  valid=s['status']=='upgrade_upgrading' and impl=={'design':184550902,'upgrade':218105405,'growth_stage':0} and isv.get('queue')==3 and isv.get('paying_country')==0 and 0<=isv.get('progress',-1)<isv.get('progress_needed',0)==.0666 and not q.block(it,'resources') and q.scalars(build)=={'ship_design':218105405,'ship':ship} and q.scalars(q.block(build,'orbitable'))=={'starbase':0};active.append(iid)
 details.append({'ship':ship,'original_status_raw':v,'item_raw':a['items'].get(iid),'valid':valid and ship in minerals and s['value']==.0666 and q.scalars(q.block(v,'upgrade_implementation'))=={'design':218105405}})
original=load('terravore-seven-minerals-refit-order-mineral-refit-order-v3-proof.json')['ships_before']
checks={
 'original16_PASS_actual0_exact_held_business_source':len(pre['checks'])==16 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1]))=='6de6e133a70c28cfd88820cfcd530dc5fa7a485b24d6eed854277cc7f2a2210d',
 'same_original_SAV_and_exact_upgrade_boundary':pre['after_sha256']==au['save_sha256']==h.sha256(run/(stage+'.sav')) and pre['boundaries']==['unreviewed_native_upgrade_boundary'] and not pre['native_devour_calendar_ready'],
 'exact_next_one_day_same_November_no_month_tick':au['date'][:8]==end[:8]=='2280.11.' and int(end[-2:])-int(au['date'][-2:])==1 and 3<=int(au['date'][-2:])<int(end[-2:])<=30,
 'seven_original_ships_statuses_full_identity_birth_health_no_new_hulls':set(q.ids(q.block(a['fleets']['50332250'],'ships')))==minerals and len(rows)==len(details)==7 and {v['ship'] for v in details}==minerals and all(v['valid'] for v in details) and all(all(q.scalars(a['ships'][str(i)]).get(k)==q.scalars(original[str(i)]).get(k) for k in ['construction_date','hitpoints','max_hitpoints','armor_hitpoints','max_armor_hitpoints','shield_hitpoints','max_shield_hitpoints']) and q.block(a['ships'][str(i)],'name')==q.block(original[str(i)],'name') for i in minerals),
 'partial_native_zero_cost_upgrade_queue_bijective_remaining_only':0<len(done)<7 and 0<len(active)<7 and set(active)==set(map(str,q.ids(q.block(a['queues']['3'],'items')))) and q.scalars(a['queues']['3'])=={'owner':0,'simultaneous':2,'type':'ships'} and q.scalars(q.block(a['queues']['3'],'location'))=={'type':0,'id':0} and q.scalars(q.block(order,'orbitable'))=={'starbase':0} and q.scalars(order)['queue']==3,
 'actual_at_base0_no_combat_pending_or_unreviewed_messages':q.scalars(q.block(q.block(q.block(a['fleets']['50332250'],'movement_manager'),'orbit'),'orbitable'))=={'starbase':0} and not a['pending'] and not pre['new_messages'] and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'production_CN_original_error_and_state_module_source_held':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(stage+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850' and pre['state_module_sha256']==h.sha256(run/'priority_terravore_native_state.py')==h.sha256(Path(__file__).with_name('priority_terravore_native_state.py')),
}
passed=all(v is True for v in checks.values());out=run/(stage+'-upgrade-day-review-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':au['save_sha256'],'after_sha256':au['save_sha256'],'start_date':au['date'],'end_date':end,'days':1,'maximum_days':1,'allowed_boundaries':pre['boundaries'],'execution_stage':stage+'-upgrade-day-review','partial_statuses':details,'done_ships':done,'remaining_items':active,'scope':'Only one next native day observation of actual zero cost partial upgrades. No all seven completion or maintenance month accepted.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'done':len(done),'remaining':len(active)}),flush=True);assert passed
