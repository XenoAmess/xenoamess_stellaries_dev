"""Strict original same-day normal repair order; no arrival or repair claim."""
import sys,json,logging,shutil,zipfile,itertools
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-marauder15-acked';after='terravore-postdrone-repair-ordered'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after)
old,new=[q.block(rt['fleet'],'33555034') for rt in [br,ar]];om,nm=[q.block(f,'movement_manager') for f in [old,new]]
pre=json.loads((run/(before+'-empty-ack-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
order=q.block(q.block(new,'current_order'),'repair_fleet_order');orb=q.block(q.block(order,'sub_order'),'orbit_planet_order');move=q.block(q.block(orb,'sub_order'),'move_to_system_point_order')
nodes=[v for k,v,o in q.fields(q.block(nm,'path')) if k=='node' and o];origins=[q.scalars(q.block(v,'coordinate'))['origin'] for v in nodes];route=[k for k,g in itertools.groupby(origins)]
base=q.block(q.block(ar['starbase_mgr'],'starbases'),'0')
checks={
 'original_SHA_pair_same_date':a['date']==b['date']=='2263.11.17' and b['save_sha256']=='50e6f646caa876196ab70eeebfd6c1d04ff3a253cd4ed746c7a43bdca9072b6a' and a['save_sha256']=='3938fdb2e24435d7bf561eeb817ec500a5363a74ef61e7c4ddf7fd273c1fc5a1' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior13_ACK_PASS_actual0':pre['status']=='PASS_NATIVE_EMPTY_EFFECT_ACK_COMPONENT' and len(pre['checks'])==13 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='62d850f93d60a09265eec3b68171a595062c99e9ffdfc46dc7a7227cc5e850cb',
 'all_other_ordered_top_raw_held':[(k,v,o) for k,v,o in bf if k!='fleet']==[(k,v,o) for k,v,o in af if k!='fleet'],
 'only_original_main_fleet_three_command_fields_changed':omit(br['fleet'],{'33555034'})==omit(ar['fleet'],{'33555034'}) and omit(old,{'movement_manager','order_id','current_order'})==omit(new,{'movement_manager','order_id','current_order'}),
 'only_four_movement_fields_changed_actual_coordinate_held':omit(om,{'target','target_coordinate','path','time_since_last_path_update'})==omit(nm,{'target','target_coordinate','path','time_since_last_path_update'}) and q.scalars(om)['time_since_last_path_update']==1 and 'time_since_last_path_update' not in q.scalars(nm),
 'original_five_ships_health_design_and_country_raw_held':q.ids(q.block(new,'ships'))==[33556208,33556207,50332878,1807,1810] and q.scalars(new)['hit_points']==873.59918 and q.scalars(new)['military_power']==401.00781 and br['ships']==ar['ships'] and br['country']==ar['country'],
 'unique_native_repair_order_counter1_to2':q.scalars(old)['order_id']==1 and q.scalars(new)['order_id']==2 and [(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('repair_fleet_order',True)] and q.scalars(order)=={'exclude_allied':'no','home_base':'no','can_reach':'yes','order_id':1,'commissioner':4294967295} and not q.block(new,'order').strip(),
 'native_repair_targets_starbase0_planet0_reachable':q.scalars(q.block(orb,'orbitable'))=={'starbase':0} and q.scalars(q.block(orb,'star'))=={'planet':0} and q.scalars(orb)=={'merge_fleet':'none','can_reach':'yes','commissioner':4294967295} and q.scalars(move)=={'can_reach':'yes','commissioner':4294967295},
 'target0_existing_two_shipyards_held':q.scalars(base)['station']==0 and q.scalars(base)['level']=='starbase_level_starport' and q.scalars(q.block(base,'modules'))=={'0':'shipyard','1':'shipyard'} and q.scalars(q.block(base,'buildings'))=={'0':'crew_quarters'} and br['starbase_mgr']==ar['starbase_mgr'],
 'exact_native_destination_and_estimate':all(q.scalars(t)=={'x':19.61,'y':-19.61,'origin':0} for t in [q.block(nm,'target_coordinate'),q.block(q.block(nm,'target'),'coordinate'),q.block(move,'coordinate')]) and q.scalars(q.block(nm,'path'))=={'date':'2265.01.21'},
 'thirteen_nodes_exact_safe_route_native_hyperlanes':len(nodes)==13 and route==[70,171,139,188,151,103,0] and all('to='+str(y) in q.block(q.block(ar['galactic_object'],str(x)),'hyperlane') for x,y in zip(route,route[1:])) and all(q.scalars(v)=={'ftl':'jump_hyperlane'} for v in nodes),
 'normal_click_and_save_actual0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-postdrone-repair-click',after+'-save']) and json.loads((run/'terravore-postdrone-repair-click.action.json').read_text('utf-8'))['client_point']==[385,507],
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered2670_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
p={'status':'PASS_TERRAVORE_NATIVE_REPAIR_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_repair_destination':{'starbase':0,'planet':0,'system':0},'native_path':route,'native_estimate':'2265.01.21','calendar_ready':all(checks.values()),'scope':'Same-day original5-ship normal repair order only. Health held; no repair, arrival or route-complete claim.'}
out=run/(after+'-repair-order-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original repair order FAIL retained'
