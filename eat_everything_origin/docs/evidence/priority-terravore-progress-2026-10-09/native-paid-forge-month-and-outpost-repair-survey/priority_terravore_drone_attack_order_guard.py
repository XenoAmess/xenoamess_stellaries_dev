"""Exact normal native attack-follow orders for the two existing paid fleets."""
import json,logging,shutil,sys,zipfile,re,itertools
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-postrepair-mining-halfyear';after='terravore-route-drone-attack-ordered'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after)
omit=lambda v,ks:[(k,x,o) for k,x,o in q.fields(v) if k not in ks]
objects=lambda v:{k:x for k,x,o in q.fields(v)}
pre=json.loads((run/(before+'-halfyear-observation-v2-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-v2-execution.json')).read_text('utf-8'))
old,new=[q.block(rt['fleet'],'33555034') for rt in [br,ar]];om,nm=[q.block(f,'movement_manager') for f in [old,new]];order=q.block(q.block(new,'current_order'),'follow_order');path=q.block(nm,'path');nodes=[v for k,v,o in q.fields(path) if k=='node' and o];origins=[q.scalars(q.block(v,'coordinate'))['origin'] for v in nodes];route=[k for k,g in itertools.groupby(origins)]
bs,ass=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]]
checks={
 'exact_same_date_original_SHA_pair':b['date']==a['date']=='2262.11.17' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'prior31_halted_outpost_observation_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_HALF_YEAR_CONSTRUCTION_AND_HALTED_OUTPOST_OBSERVATION_V2' and len(pre['checks'])==31 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pre['calendar_ready'] is False and ex['returncode']==0 and ex['helper_sha256']=='e5714145c5a8d5ef8d256e79d405f674447d91099b1fd5cafd13befc18e113be',
 'all_other_top_ordered_raw_held':[(k,v,o) for k,v,o in bf if k not in {'fleet','starbase_mgr','random_count','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'fleet','starbase_mgr','random_count','camera_focus'}],
 'only_main_fleet33555034_changed_other_fleets_raw_held':omit(br['fleet'],{'33555034'})==omit(ar['fleet'],{'33555034'}),
 'only_four_main_command_cache_fields_changed':omit(old,{'movement_manager','properties','order_id','current_order'})==omit(new,{'movement_manager','properties','order_id','current_order'}),
 'only_dirty_cloaking_strength_added':omit(q.block(old,'properties'),{'dirty_cloaking_strength'})==omit(q.block(new,'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(old,'properties')) and q.scalars(q.block(new,'properties'))['dirty_cloaking_strength']=='yes',
 'native_single_follow_attack33555206_order0_counter1':not q.block(old,'current_order').strip() and not q.block(new,'order').strip() and [(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('follow_order',True)] and q.scalars(order)=={'fleet':33555206,'attack_when_in_range':'yes','can_reach':'yes','order_id':0,'commissioner':4294967295} and q.scalars(q.block(order,'coordinate'))=={'x':0,'y':0,'origin':4294967295} and 'order_id' not in q.scalars(old) and q.scalars(new)['order_id']==1,
 'movement_only_target_path_orbit_changed_all_position_fields_held':omit(om,{'target','target_coordinate','path','orbit'})==omit(nm,{'target','target_coordinate','path','orbit'}) and q.scalars(q.block(q.block(om,'orbit'),'orbitable'))=={'starbase':0} and not q.block(nm,'orbit').strip(),
 'actual_target_enemy_and_coordinate':q.scalars(q.block(q.block(nm,'target'),'target'))=={'type':3,'id':33555206} and q.scalars(q.block(nm,'target_coordinate'))=={'x':58.96865,'y':-4.85465,'origin':70},
 'native_thirteen_nodes_seven_system_route_estimate':len(nodes)==13 and route==[0,103,151,188,139,171,70] and all(q.scalars(v)=={'ftl':'jump_hyperlane'} for v in nodes) and q.scalars(path)=={'date':'2264.01.20'} and q.scalars(q.block(nodes[-1],'coordinate'))=={'x':58.96865,'y':-4.85465,'origin':70},
 'all_route_hyperlane_edges_actual':all(y in map(int,re.findall(r'\bto=(\d+)',q.block(q.block(ar['galactic_object'],str(x)),'hyperlane'))) for x,y in zip(route,route[1:])),
 'same_fourteen_original_paid_ships_and_full_hp_no_combat':q.ids(q.block(old,'ships'))==q.ids(q.block(new,'ships')) and len(q.ids(q.block(new,'ships')))==14 and q.scalars(new)['hit_points']==3780 and not q.block(q.block(new,'combat'),'in_combat_with').strip(),
 'starbase_only_original_slot0_departure':q.scalars(q.block(bs,'orbitals'))=={'0':33555034,'1':4294967295,'2':4294967295} and q.scalars(q.block(ass,'orbitals'))=={'0':4294967295,'1':4294967295,'2':4294967295} and omit(bs,{'orbitals'})==omit(ass,{'orbitals'}) and omit(q.block(br['starbase_mgr'],'starbases'),{'0'})==omit(q.block(ar['starbase_mgr'],'starbases'),{'0'}) and omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'}),
 'exact_random_count_plus2':[v for k,v,o in bf if k=='random_count']==['106706594'] and [v for k,v,o in af if k=='random_count']==['106706596'],
 'only_camera_focus70_added':not any(k=='camera_focus' for k,v,o in bf) and [(v,o) for k,v,o in af if k=='camera_focus']==[('70',False)],
 'all_countries_real_economy_bank_research_EEP_raw_held':br['country']==ar['country'] and b['countries']==a['countries'],
 'all_actual_ships_leaders_and_construction_raw_held':all(br[k]==ar[k] for k in ['ships','leaders','construction']),
 'original_constructor_safely_halted171_raw_held':q.block(br['fleet'],'2')==q.block(ar['fleet'],'2') and q.scalars(q.block(q.block(q.block(ar['fleet'],'2'),'movement_manager'),'coordinate'))['origin']==171 and not q.block(q.block(ar['fleet'],'2'),'current_order').strip(),
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
 'normal_save_actual_exit0':json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0,
}
click=json.loads((run/'terravore-route-drone-attack-click.action.json').read_text('utf-8'));checks['single_normal_right_click_actual_exit0']=click['action']=='right-click' and click['client_point']==[417,385] and json.loads((run/'terravore-route-drone-attack-click-execution.json').read_text('utf-8'))['returncode']==0
checks['visible_enemy_six_ship_image_bound']=h.sha256(run/'terravore-route-drone-enemy-panel-visible.jpg')==json.loads((run/'terravore-route-drone-enemy-panel-visible.ocr.json').read_text('utf-8'))['image_sha256']
p={'status':'PASS_TERRAVORE_NATIVE_DRONE_ATTACK_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_target_fleet':33555206,'actual_attack_fleet':33555034,'native_route':route,'native_estimate':'2264.01.20','calendar_ready':all(checks.values()),'scope':'One normal fourteen-paid-ship attack-follow order; constructor halted safely and one original corvette remains home. Allows bounded native travel, not arrival, victory, outpost restoration, menace or full-route acceptance.'}
out=run/(after+'-drone-attack-order-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original drone attack order FAIL retained'
