"""Exact normal move of original constructor to surveyed star in visited system97."""
import itertools,json,logging,shutil,sys,zipfile,re
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);old,new=[q.block(rt['fleet'],'2') for rt in [br,ar]];bm,am=[q.block(f,'movement_manager') for f in [old,new]]
current=q.block(new,'current_order');order=q.block(current,'orbit_planet_order');sub=q.block(order,'sub_order');move=q.block(sub,'move_to_system_point_order');path=q.block(am,'path');nodes=[v for k,v,o in q.fields(path) if k=='node' and o];origins=[q.scalars(q.block(v,'coordinate'))['origin'] for v in nodes];route=[k for k,g in itertools.groupby(origins)]
pre=json.loads((run/(before+'-node83-repair-payment-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
checks={
 'exact_same_date_SHA_pair':before=='terravore-raid-node83-repair-paid' and after=='terravore-yodd-constructor-move-ordered' and b['date']==a['date']=='2261.11.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior26_repair_payment_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_NODE83_REPAIR_PAYMENT_COMPONENT' and len(pre['checks'])==26 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'all_other_top_ordered_raw_held':[row for row in bf if row[0] not in {'fleet','random_count','camera_focus'}]==[row for row in af if row[0] not in {'fleet','random_count','camera_focus'}],
 'only_fleet2_three_fields_changed':omit(br['fleet'],{'2'})==omit(ar['fleet'],{'2'}) and omit(old,{'order_id','current_order','movement_manager'})==omit(new,{'order_id','current_order','movement_manager'}),
 'original_constructor_ship2_counter9_to10':q.scalars(old)['ship_class']==q.scalars(new)['ship_class']=='shipclass_constructor' and q.ids(q.block(old,'ships'))==q.ids(q.block(new,'ships'))==[2] and q.scalars(old)['order_id']==9 and q.scalars(new)['order_id']==10,
 'only_native_orbit_planet_order_no_queue':[(k,o) for k,v,o in q.fields(current)]==[('orbit_planet_order',True)] and not q.block(old,'current_order').strip() and not q.block(new,'order').strip() and q.scalars(order)=={'merge_fleet':'none','can_reach':'yes','order_id':9,'commissioner':4294967295},
 'orbitable_star1078_and_only_sub_move':q.scalars(q.block(order,'orbitable'))==q.scalars(q.block(order,'star'))=={'planet':1078} and [(k,o) for k,v,o in q.fields(order) if o]==[('orbitable',True),('star',True),('sub_order',True)] and [(k,o) for k,v,o in q.fields(sub)]==[('move_to_system_point_order',True)],
 'sub_move_reachable_exact_target97':q.scalars(move)=={'can_reach':'yes','commissioner':4294967295} and [(k,o) for k,v,o in q.fields(move) if o]==[('coordinate',True)] and q.scalars(q.block(move,'coordinate'))=={'x':10.95,'y':10.95,'origin':97},
 'all_noncommand_movement_raw_held':omit(bm,{'target','target_coordinate','path','time_since_last_path_update'})==omit(am,{'target','target_coordinate','path','time_since_last_path_update'}) and q.scalars(bm)['time_since_last_path_update']==1 and 'time_since_last_path_update' not in q.scalars(am),
 'current_location75_held_and_native_target97':q.block(bm,'coordinate')==q.block(am,'coordinate') and q.scalars(q.block(am,'coordinate'))['origin']==75 and q.scalars(q.block(am,'target_coordinate'))==q.scalars(q.block(q.block(am,'target'),'coordinate'))=={'x':10.95,'y':10.95,'origin':97},
 'native13_system_path_estimate2264_04_09':route==[75,145,48,0,103,151,188,139,171,70,30,80,97] and len(nodes)==25 and all(q.scalars(v)=={'ftl':'jump_hyperlane'} for v in nodes) and q.scalars(path)=={'date':'2264.04.09'} and q.scalars(q.block(nodes[-1],'coordinate'))=={'x':10.95,'y':10.95,'origin':97},
 'path_each_actual_hyperlane_edge_exists':all(y in map(int,re.findall(r'\bto=(\d+)',q.block(q.block(ar['galactic_object'],str(x)),'hyperlane'))) for x,y in zip(route,route[1:])),
 'native_navigation_random_plus2_camera0_removed':[v for k,v,o in bf if k=='random_count']==['93316762'] and [v for k,v,o in af if k=='random_count']==['93316764'] and [v for k,v,o in bf if k=='camera_focus']==['0'] and not any(k=='camera_focus' for k,v,o in af),
 'all_country_economy_and_repair_ship_queues_raw_held':br['country']==ar['country'] and br['construction']==ar['construction'] and b['countries']==a['countries'],
 'all_ships_leaders_mother_pop_and_EEP_held':br['ships']==ar['ships'] and br['leaders']==ar['leaders'] and b['pop_groups']==a['pop_groups'] and b['pop_jobs']==a['pop_jobs'] and b['planets']==a['planets'],
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors_exact2670_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
 'save_actual_exit0':json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0,
}
click=json.loads((run/'terravore-yodd-constructor-move-click.action.json').read_text('utf-8'))
checks['normal_move_click_actual_exit0']=click['action']=='left-click' and click['client_point']==[600,413] and json.loads((run/'terravore-yodd-constructor-move-click-execution.json').read_text('utf-8'))['returncode']==0
checks['native_build_rejection_image_bound']=h.sha256(run/'terravore-yodd-outpost-rejection-visible.jpg')==json.loads((run/'terravore-yodd-outpost-rejection-visible.ocr.json').read_text('utf-8'))['image_sha256']
p={'status':'PASS_TERRAVORE_YODD_CONSTRUCTOR_MOVE_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_route':route,'native_estimated_arrival':'2264.04.09','calendar_ready':all(checks.values()),'scope':'Normal move order only after native refusal to build in incompletely surveyed system. No payment, arrival, outpost, colony, menace or full-route acceptance.'}
out=run/(after+'-constructor-move-order-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original move-order FAIL retained; do not replay order'
