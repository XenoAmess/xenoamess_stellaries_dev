"""Documented same-day native four-fleet attack order validation; no GUI."""
import json,logging,sys
from pathlib import Path
before,after=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8'));omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
obs_path=run/(after+'-same-day-order-observation.json');obs=load(obs_path.name);oe=load(after+'-same-day-order-observation-execution.json');b,a=obs['before_state'],obs['after_state'];ba,aa=b['audit'],a['audit']
pre=load(before+'-birth-v2-proof.json');pe=load(before+'-observer-v2-execution.json');se=load(after+'-native-save-execution.json')
inv_path=run/(after+'-source-orbitals-and-random-investigation.json');iv=load(inv_path.name);ib,ia=iv[before],iv[after]
selected=['788','33555013','33555034','100664127'];military=lambda st:{j for fid,f in st['owned_fleets_raw'].items() if q.scalars(f).get('ship_class')=='shipclass_military' for j in q.ids(q.block(f,'ships'))}

def native_orders_ok():
    target=q.scalars(q.block(q.block(a['enemy825_raw'],'movement_manager'),'coordinate'))
    for fid in selected:
        old,new=b['owned_fleets_raw'][fid],a['owned_fleets_raw'][fid];os,ns=q.scalars(old),q.scalars(new);order=q.block(new,'current_order');follow=q.block(order,'follow_order');bm,am=q.block(old,'movement_manager'),q.block(new,'movement_manager');path=q.block(am,'path');node=q.block(path,'node')
        if not (not q.block(old,'current_order') and [(k,o) for k,v,o in q.fields(order)]==[('follow_order',True)]
            and q.scalars(follow)=={'fleet':825,'attack_when_in_range':'yes','can_reach':'yes','order_id':os['order_id'],'commissioner':4294967295}
            and q.scalars(q.block(follow,'coordinate'))=={'x':0,'y':0,'origin':4294967295} and ns['order_id']==os['order_id']+1
            and omit(old,{'current_order','auto_movement','order_id','movement_manager'})==omit(new,{'current_order','auto_movement','order_id','movement_manager'})
            and q.scalars(q.block(old,'auto_movement'))=={'type':'auto_move_planet','auto_move_target':1085,'clear_on_new_orders':'yes','has_arrived':'yes'} and not q.block(new,'auto_movement')
            and omit(bm,{'target','target_coordinate','path','orbit','time_since_last_path_update'})==omit(am,{'target','target_coordinate','path','orbit','time_since_last_path_update'})
            and q.scalars(q.block(q.block(am,'target'),'target'))=={'type':3,'id':825} and q.scalars(q.block(am,'target_coordinate'))==target
            and q.scalars(q.block(node,'coordinate'))==target and q.scalars(node)=={'ftl':'jump_hyperlane'} and q.scalars(path)=={'date':'2272.10.05' if fid=='788' else '2272.10.06'}
            and q.scalars(q.block(q.block(bm,'orbit'),'orbitable'))=={'planet':1085} and not list(q.fields(q.block(am,'orbit')))
            and q.scalars(q.block(am,'coordinate'))['origin']==97 and not q.ids(q.block(q.block(new,'combat'),'in_combat_with'))):return False
    return True

def source_orbitals_ok():
    old,new=b['planet_raw']['1085'],a['planet_raw']['1085']
    return (old==ib['source1085_raw'] and new==ia['source1085_raw'] and omit(old,{'planet_orbitals'})==omit(new,{'planet_orbitals'})
        and q.scalars(q.block(old,'planet_orbitals'))=={'0':788,'1':33555013,'2':33555034,'3':100664127,'4':166}
        and q.scalars(q.block(new,'planet_orbitals'))=={'0':4294967295,'1':4294967295,'2':4294967295,'3':4294967295,'4':166})

def input_actions_ok():
    for name in ['fourth','third','first','second']:
        stage='terravore-rear97-reinforcement-order-'+name;e=load(stage+'-execution.json');action=load(stage+'.action.json')
        if not(e['returncode']==0 and e['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and action['action']=='right-click' and action['client_point']==[756,444] and action['foreground_after']==action['expected_hwnd']):return False
    return True

checks={
 'same_day_observation6_all_true_actual0_source_original_SHA':obs['status']=='OBSERVED_NATIVE_TERRAVORE_REAR97_SAME_DAY_ORDER' and len(obs['checks'])==6 and all(v is True for v in obs['checks'].values()) and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_rear97_same_day_order_observation.py')=='b04f53f8ae56c0210113eb0ddfa6ed73ef669e60f13c06c89b5dd06a10736f28' and h.sha256(obs_path)=='237f55a1a730115ba157b9f811ca4fa595759a0dbbdaf91a3e80c39a3c0df6b1',
 'prior_birth46_all_PASS_actual0_source':pre['status']=='PASS_NATIVE_TERRAVORE_REAR_COLONIZER_BIRTH_IN_COMBAT_COMPONENT' and len(pre['checks'])==46 and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_rear_colonizer_birth_observer_v2.py')=='ed9b38a96bc838d3340d82d8c272dd883dba7a9595f1f27b67818384c21516fa',
 'fixed_original_SAV_pair_same_native_date':before=='terravore-rear-colonizer-born' and after=='terravore-rear97-idle-reinforcement-ordered' and ba['date']==aa['date']=='2272.09.13' and obs['before_sha256']==pre['after_sha256']==ib['save_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and obs['after_sha256']==ia['save_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'normal_save_actual0_source':se['returncode']==0 and se['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e',
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'four_normal_right_clicks_actual0_source_correct_target_UI':input_actions_ok(),
 'exactly_four_owned_fleets_changed':{i for i in b['owned_fleets_raw'] if b['owned_fleets_raw'][i]!=a['owned_fleets_raw'].get(i)}==set(selected),
 'all_owned_fleet_and_ship_identity_collections_held':b['owned_fleets']==a['owned_fleets'] and b['owned_ship_ids']==a['owned_ship_ids'],
 'all_owned_ship_raw_design_health_position_held':b['owned_ships_raw']==a['owned_ships_raw'],
 'all28_military_same_no_naval_change':military(b)==military(a) and len(military(a))==28 and q.scalars(b['country0_raw'])['fleet_size']==q.scalars(a['country0_raw'])['fleet_size']==140,
 'four_native_unique_follow825_attack_orders_original_counter_paths_no_teleport':native_orders_ok(),
 'full_country0_raw_and_audit_resources_research_EEP_qualifications_held':b['country0_raw']==a['country0_raw'] and ba['countries']['0']==aa['countries']['0'],
 'mother_and_target523_full_raw_held':all(b['planet_raw'][i]==a['planet_raw'][i] for i in ['7','523']),
 'source_only_four_old_orbitals_released':source_orbitals_ok(),
 'independent_all_other_planets_and_wrapper_held':h.sha256(inv_path)=='010c0735e6791ba8d743b0ce19f175850def053a1ca0337859ce493df39e67fd' and ib['all_other_planets_fields_sha256']==ia['all_other_planets_fields_sha256']=='048df03de3c130724a6e57362c4320c769347be822d5ab4b8bde1169119afa6c' and ib['planets_wrapper_other_fields']==ia['planets_wrapper_other_fields'],
 'colony_population_jobs_full_held':b['colony_raw']==a['colony_raw'] and b['species_population_by_colony']==a['species_population_by_colony'] and ba['pop_jobs']==aa['pop_jobs'],
 'all_buildings_zones_districts_deposits_construction_situations_design_history_raw_held':b['raw_roots']==a['raw_roots'],
 'enemy825_base153_and_war1_raw_held':b['enemy825_raw']==a['enemy825_raw'] and b['rear153_raw']==a['rear153_raw'] and b['war1_battles_raw']==a['war1_battles_raw'],
 'pending_and_country_messages_held':b['pending_country0_raw']==a['pending_country0_raw'] and b['messages_country0_raw']==a['messages_country0_raw'],
 'ordered_top300_all_other_fields_exact_SHA_held':len(b['top_fields_content_sha256'])==len(a['top_fields_content_sha256'])==300 and [(v[0],v[1]) for v in b['top_fields_content_sha256']]==[(v[0],v[1]) for v in a['top_fields_content_sha256']] and [u[0] for u,v in zip(b['top_fields_content_sha256'],a['top_fields_content_sha256']) if u!=v]==['planets','fleet','random_count'],
 'only_native_four_orders_random_count_plus8':ib['random_count']==244764823 and ia['random_count']==244764831,
}
passed=all(v is True for v in checks.values());proof={'status':'PASS_NATIVE_TERRAVORE_REAR97_REINFORCEMENT_ORDER_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'ordered_fleets':list(map(int,selected)),'target_enemy_fleet':825,'rear_battle_single_day_ready':passed,'maximum_days_to_next_battle_observation':1,'normal_colonization_route_ready':False,'scope':'Four native same-day attack orders only; not arrival, battle victory, safe colony transit or full-route acceptance.'}
out=run/(after+'-order-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date']}),flush=True);assert passed
