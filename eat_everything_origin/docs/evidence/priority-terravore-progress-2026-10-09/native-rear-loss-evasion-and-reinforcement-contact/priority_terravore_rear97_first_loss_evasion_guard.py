"""Documented exact first rear corvette death and newborn colonizer evasion boundary."""
import json,logging,math,sys
from pathlib import Path
before,after=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8'));omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
obs_path=run/(after+'-construction-boundary-observation.json');obs=load(obs_path.name);oe=load(after+'-boundary-observation-execution.json');inv_path=run/(after+'-rear97-native-inventory.json');inv=load(inv_path.name);ie=load(after+'-rear97-native-inventory-execution.json')
b,a=obs['before_state'],obs['after_state'];ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0'];bcr,acr=b['country0_raw'],a['country0_raw'];eb,ea=inv[before],inv[after]
cal=load(after+'-calendar-receipt.json');ce=load(after+'-calendar-execution.json');pre=load(cal['prior_proof_file']);pe=load(cal['prior_execution_stage']+'-execution.json')
first=False;days=1;country_timers=['entered_war_as_defender','recent_first_contact_process_started','recent_cara_3010','discovered_site','was_recently_targeted_by_voidworms']
reinforcement=['788','33555013','33555034','100664127'];moving_ships=['1807','1810','1816','1895','1896','33555519','67110639','50333369']
movement_fields={'coordinate','target_coordinate','rotation','forward_x','forward_y','post_move_angle','speed'}
military=lambda st:{i for fid,f in st['owned_fleets_raw'].items() if q.scalars(f).get('ship_class')=='shipclass_military' for i in q.ids(q.block(f,'ships'))}

def entries(raw):
    out=[];depth=0;start=0
    for token,lo,hi in q.tokens(raw):
        if token=='{':
            if depth==0:start=hi
            depth+=1
        elif token=='}':
            depth-=1
            if depth==0:out.append(raw[start:lo])
    return out

def timers_ok():
    old,new=[q.block(c,'flags') for c in [bcr,acr]]
    return (omit(old,set(country_timers+(['eep_notice_pending'] if first else [])))==omit(new,set(country_timers))
        and all(omit(q.block(old,k),{'flag_days'})==omit(q.block(new,k),{'flag_days'}) and q.scalars(q.block(old,k))['flag_days']-q.scalars(q.block(new,k))['flag_days']==days and q.scalars(q.block(new,k))['flag_days']>0 for k in country_timers))

def modules_ok():
    old,new=[q.block(c,'modules') for c in [bcr,acr]]
    ev=[q.block(v,'standard_event_module') for v in [old,new]];de=[q.block(v,'delayed_event') for v in ev]
    return (omit(old,{'standard_event_module','standard_economy_module'})==omit(new,{'standard_event_module','standard_economy_module'})
        and omit(q.block(old,'standard_economy_module'),{'resources'})==omit(q.block(new,'standard_economy_module'),{'resources'})
        and omit(ev[0],{'delayed_event'})==omit(ev[1],{'delayed_event'}) and omit(de[0],{'days'})==omit(de[1],{'days'})
        and q.scalars(de[0])['event']==q.scalars(de[1])['event']=='paragon.999' and q.scalars(de[0])['days']-q.scalars(de[1])['days']==days)

def projects_ok():
    old,new=[q.block(c,'events') for c in [bcr,acr]]
    ps=[{q.scalars(v)['id']:v for k,v,o in q.fields(t) if k=='special_project' and o} for t in [old,new]]
    return (ps[0].keys()==ps[1].keys() and {4,5}<=ps[1].keys()
        and omit(old,{'special_project','situations'})==omit(new,{'special_project','situations'})
        and not q.ids(q.block(new,'situations'))
        and all(ps[0][i]==ps[1][i] if i not in [4,5] else omit(ps[0][i],{'days_left'})==omit(ps[1][i],{'days_left'}) and q.scalars(ps[0][i])['days_left']-q.scalars(ps[1][i])['days_left']==days and q.scalars(ps[1][i])['days_left']>0 for i in ps[0]))


def source_timers_ok():
    old,new=ba['planets']['1085'],aa['planets']['1085'];timers={'recently_eaten_planet','superior_colonies_can_be_boosted'}
    return (omit(b['planet_raw']['1085'],{'flags'})==omit(a['planet_raw']['1085'],{'flags'})
        and {k:v for k,v in old['flags'].items() if k not in timers}=={k:v for k,v in new['flags'].items() if k not in timers}
        and all(old['flags'][k]['flag_date']==new['flags'][k]['flag_date'] and old['flags'][k]['flag_days']-new['flags'][k]['flag_days']==1 for k in timers))

def seven_reinforcement_and_colonizer_movement_ok():
    return all(omit(b['owned_ships_raw'][i],movement_fields)==omit(a['owned_ships_raw'][i],movement_fields)
        and q.scalars(q.block(a['owned_ships_raw'][i],'coordinate'))['origin']==97 for i in moving_ships)

def four_follow_orders_ok():
    for i in reinforcement:
        old,new=b['owned_fleets_raw'][i],a['owned_fleets_raw'][i];bm,am=q.block(old,'movement_manager'),q.block(new,'movement_manager');x,y=q.scalars(q.block(bm,'coordinate')),q.scalars(q.block(am,'coordinate'))
        if not(q.block(old,'current_order')==q.block(new,'current_order') and q.scalars(q.block(q.block(new,'current_order'),'follow_order'))['fleet']==825
            and q.scalars(old)['order_id']==q.scalars(new)['order_id'] and q.ids(q.block(old,'ships'))==q.ids(q.block(new,'ships')) and x['origin']==y['origin']==97
            and 0<math.hypot(y['x']-x['x'],y['y']-x['y'])<=20 and not q.ids(q.block(q.block(new,'combat'),'in_combat_with'))):return False
    return True

def new_colonizer_evade_ok():
    raw=a['owned_ships_raw']['50333369'];s=q.scalars(raw);f=a['owned_fleets_raw']['33555278'];order=q.block(q.block(f,'current_order'),'evade_hostiles_order');sub=q.block(q.block(order,'sub_order'),'move_to_system_point_order')
    return (s['hitpoints']==s['max_hitpoints']==625 and s['armor_hitpoints']==s['max_armor_hitpoints']==125 and s['shield_hitpoints']==s['max_shield_hitpoints']==320
        and s['fleet']==33555278 and q.ids(q.block(f,'ships'))==[50333369] and q.scalars(q.block(raw,'colonization_data'))=={'species':73}
        and q.scalars(order)=={'can_reach':'yes','order_id':0,'commissioner':4294967295} and q.scalars(sub)=={'can_reach':'yes','commissioner':4294967295}
        and q.scalars(q.block(sub,'coordinate'))=={'x':0,'y':0,'origin':37} and q.scalars(f)['fleet_stance']=='evasive'
        and q.scalars(q.block(q.block(f,'movement_manager'),'coordinate'))=={'x':21.16778,'y':-18.52189,'origin':97}
        and q.ids(q.block(q.block(f,'combat'),'in_combat_with'))==[825] and q.scalars(q.block(ea['rear153_raw'],'orbitals'))=={'0':4294967295})

new_messages=[v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
evade=[v for v in new_messages if q.scalars(v).get('type')=='FLEET_EVADE_HOSTILE_MESSAGE_TYPE'];reports=[v for v in new_messages if q.scalars(v).get('type')=='COMBAT_STATS']
def death_report_ok():
    if len(reports)!=1:return False
    report=q.block(reports[0],'combat_stats');own=entries(q.block(report,'fleets'));enemy=entries(q.block(report,'enemy'))
    return (len(own)==len(enemy)==1 and q.scalars(report)['reason']=='we_destroyed' and q.scalars(own[0])['fleet']==16778073 and q.scalars(own[0])['country']==0
        and q.ids(q.block(own[0],'ship_size_count'))==q.ids(q.block(own[0],'ship_size_count_lost'))==[1]
        and q.scalars(enemy[0])['fleet']==825 and q.scalars(enemy[0])['country']==1 and sum(q.ids(q.block(enemy[0],'ship_size_count')))==12 and sum(q.ids(q.block(enemy[0],'ship_size_count_lost')))==0)

def war_record_ok():
    old,new=entries(b['war1_battles_raw']),entries(a['war1_battles_raw'])
    return (len(old)==10 and len(new)==11 and new[:10]==old and q.scalars(new[-1])=={'system':97,'colony':4294967295,'attacker_war_exhaustion':0,'defender_war_exhaustion':0.0238,'attacker_victory':'yes','date':'2272.09.14','attacker_losses':0,'defender_losses':1,'type':'ships'} and q.ids(q.block(new[-1],'attackers'))==[0] and q.ids(q.block(new[-1],'defenders'))==[1])

def enemy_health_ok():
    for i in eb['enemy825_ship_ids']:
        old,new=eb['enemy825_ships_raw'][str(i)],ea['enemy825_ships_raw'][str(i)];os,ns=q.scalars(old),q.scalars(new)
        if q.block(old,'ship_design_implementation')!=q.block(new,'ship_design_implementation'):return False
        for key in ['hitpoints','armor_hitpoints','shield_hitpoints']:
            if i==67109342 and key in ['hitpoints','armor_hitpoints']:
                if (os.get(key,0),ns.get(key,0))!=({'hitpoints':(870,862.53195),'armor_hitpoints':(65.69158,0)}[key]):return False
            elif os.get(key,0)!=ns.get(key,0):return False
    return eb['enemy825_ship_ids']==ea['enemy825_ship_ids'] and len(ea['enemy825_ship_ids'])==12 and eb['enemy825_country1_owned'] is ea['enemy825_country1_owned'] is True

owned_queues=lambda st:{k:v for k,v,o in q.fields(q.block(q.block(st['raw_roots']['construction'],'queue_mgr'),'queues')) if o and q.scalars(v).get('owner')==0}
registered=military(a);alive={i for i in registered if q.scalars(a['owned_ships_raw'][str(i)]).get('killed')!='yes' and q.scalars(a['owned_ships_raw'][str(i)]).get('hitpoints',0)>0}
dead=q.scalars(a['owned_ships_raw']['117441817']);station=q.scalars(a['owned_ships_raw']['67109591'])
checks={
 'current_full_observation6_true_actual0_source_SHA':obs['status']=='OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY' and len(obs['checks'])==6 and all(v is True for v in obs['checks'].values()) and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_construction_boundary_observation.py')=='e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678' and h.sha256(obs_path)=='83e7b3fd2f501fe3d8428c5eb6616b34931faa7dfabf9d842fe9721029bcf3f2',
 'current_enemy_inventory4_true_actual0_source_SHA':inv['status']=='OBSERVED_NATIVE_TERRAVORE_REAR97_INVENTORY' and len(inv['checks'])==4 and all(v is True for v in inv['checks'].values()) and ie['returncode']==0 and ie['helper_sha256']==h.sha256(run/'priority_terravore_rear97_native_inventory_v2.py')=='ad06a4fe55b739820553f71774d60774cd1b936ad5f40dfc0177be270e888f14' and h.sha256(inv_path)=='456b78dd5800da12a59500987b7794c6c8ce437e347c180082bf7dc56ea5238a',
 'prior22_all_PASS_actual0_source_and_single_day_ready':pre['status']=='PASS_NATIVE_TERRAVORE_REAR97_REINFORCEMENT_ORDER_COMPONENT' and len(pre['checks'])==22 and all(v is True for v in pre['checks'].values()) and pre['rear_battle_single_day_ready'] is True and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_rear97_reinforcement_order_guard.py')=='c9e9f200544c855645d0a0fab30f03ae642fb48f0e2efce03b03d9993d81b049',
 'single_checked_native_calendar_actual0_fixed_dates_and_source':ba['date']=='2272.09.13' and aa['date']=='2272.09.14' and cal['days']==1 and cal['status']=='CALENDAR_CONFIRMED' and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
 'original_SAV_SHA_pair':all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav'))==iv['save_sha256'] for st,name,iv in [(b,before,eb),(a,after,ea)]) and pre['after_sha256']==obs['before_sha256'],
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'all_registered_owned_identity_sets_held_before_native_cleanup':b['owned_fleets']==a['owned_fleets'] and b['owned_ship_ids']==a['owned_ship_ids'] and military(b)==registered and len(registered)==28,
 'exactly_one_killed117_negative_HP_only27_alive_registered28_naval_cache140':alive==registered-{117441817} and len(alive)==27 and dead['killed']=='yes' and dead['hitpoints']==-156.2756 and dead['fleet']==16778073 and q.scalars(a['owned_fleets_raw']['16778073'])['hit_points']==-156.27557 and q.scalars(acr)['fleet_size']==140,
 'dead_ship_original_design_and_date_held':q.block(b['owned_ships_raw']['117441817'],'ship_design_implementation')==q.block(a['owned_ships_raw']['117441817'],'ship_design_implementation') and dead['last_combat_activity']==dead['last_damage']=='2272.09.14' and dead['construction_date']=='2271.12.11',
 'unique_country0_destroyed_report_fleet16778073_loss1_enemy825_loss0':death_report_ok(),
 'war1_old10_prefix_single_actual_direction_inconsistent_raw_preserved':war_record_ok(),
 'new_messages_exactly_evade258_and_destroyed259_no_other_country_event':len(new_messages)==2 and len(evade)==len(reports)==1 and q.scalars(evade[0])['target_fleet']==33555278 and q.scalars(evade[0])['notification']==258 and q.scalars(reports[0])['notification']==259 and all(q.scalars(v)['date']=='2272.09.14' for v in new_messages),
 'new_colonizer_full_health_native_evade37_departed_base_not_safe_route':new_colonizer_evade_ok(),
 'seven_reinforcement_and_colonizer_only_normal_ship_movement':seven_reinforcement_and_colonizer_movement_ok(),
 'four_follow825_orders_held_bounded_native_position_change_not_arrived':four_follow_orders_ok(),
 'all_other_owned_ships_raw_held_except1916_natural_armor_repair':all(old==a['owned_ships_raw'][i] for i,old in b['owned_ships_raw'].items() if i not in set(moving_ships)|{'117441817','67109591','1916'}) and omit(b['owned_ships_raw']['1916'],{'armor_hitpoints'})==omit(a['owned_ships_raw']['1916'],{'armor_hitpoints'}) and q.scalars(a['owned_ships_raw']['1916'])['armor_hitpoints']-q.scalars(b['owned_ships_raw']['1916'])['armor_hitpoints']==0.625,
 'all_other_owned_fleets_raw_held_only_fixed7_fleets_changed':{i for i,old in b['owned_fleets_raw'].items() if old!=a['owned_fleets_raw'][i]}==set(reinforcement)|{'804','16778073','33555278'},
 'rear_station_original_design_owner_full_HP_exact_native_damage':station['fleet']==804 and 804 in a['owned_fleets'] and station['hitpoints']==station['max_hitpoints']==18300 and station['armor_hitpoints']==4996.78103 and station['shield_hitpoints']==3889.51447 and q.block(b['owned_ships_raw']['67109591'],'ship_design_implementation')==q.block(a['owned_ships_raw']['67109591'],'ship_design_implementation'),
 'native_base153_only_departed_new_colonizer_orbital_held_owner_chain':omit(eb['rear153_raw'],{'orbitals'})==omit(ea['rear153_raw'],{'orbitals'}) and q.scalars(ea['rear153_raw'])['station']==67109591 and q.scalars(q.block(eb['rear153_raw'],'orbitals'))=={'0':33555278} and q.scalars(q.block(ea['rear153_raw'],'orbitals'))=={'0':4294967295},
 'enemy12_same_designs_exact_single_ship_damage_no_entity_loss':enemy_health_ok(),
 'true_stocks_and_research_banks_held_no_rewards_or_refunds':bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'] and ac['effective_stockpile']['menace']==885,
 'native_budget_and_technology_held_no_month_or_research_tick':bc['budget_categories']==ac['budget_categories'] and bc['tech_status']==ac['tech_status'],
 'EEP_variables_flags_core_population_and_housing_held':bc['variables']==ac['variables'] and b['planet_raw']['7']==a['planet_raw']['7'] and b['colony_raw']==a['colony_raw'] and aa['colonies']['0']['actual_pop_sum']==11137 and aa['colonies']['0']['total_housing']==14100,
 'source_only_original_two_timer_days_decremented':source_timers_ok(),
 'all_mother_districts_zones_buildings_deposits_and_design_history_held':all(b['raw_roots'][k]==a['raw_roots'][k] for k in ['districts','zones','buildings','deposit','ship_design','open_player_event_selection_history']),
 'all_job_caps_and_species_population_held':b['species_population_by_colony']==a['species_population_by_colony'] and {i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in ba['pop_jobs'].items()}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in aa['pop_jobs'].items()},
 'all12_owned_construction_queues_held_empty_no_new_orders':owned_queues(b)==owned_queues(a) and len(owned_queues(a))==12 and all(not q.ids(q.block(v,'items')) for v in owned_queues(a).values()),
 'target523_and_original_dead_colonizer_entries_held':b['planet_raw']['523']==a['planet_raw']['523'] and b['original_ship16779140_entry']==a['original_ship16779140_entry'] and b['original_fleet16778062_entry']==a['original_fleet16778062_entry'],
 'owned_defense_armies_and_government_traditions_AP_held':q.ids(q.block(bcr,'owned_armies'))==q.ids(q.block(acr,'owned_armies')) and len(q.ids(q.block(acr,'owned_armies')))==12 and all(bc[k]==ac[k] for k in ['government','traditions','ascension_perks']),
 'pending264_held_no_new_Queen_notice_or_live_EEP':b['pending_country0_raw']==a['pending_country0_raw'] and len(a['pending_country0_raw'])==1 and not any(v.get('type') in ['situation_eep_devouring','situation_terravore_consume_planet'] for v in aa['situations'].values()),
 'same_native_nemesis1_objectives_no_added_Menace':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression'),
 'original_five_country_timers_exact_one_day':timers_ok(),
 'only_native_paragon999_timer_and_economy_modules':modules_ok(),
 'only_known_debris_timers_no_new_owned_projects':projects_ok(),
}
passed=all(v is True for v in checks.values());proof={'status':'PASS_NATIVE_TERRAVORE_REAR97_FIRST_CORVETTE_LOSS_CIVILIAN_EVASION_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'alive_military_ship_ids':sorted(alive),'registered_military_ship_ids':sorted(registered),'actual_killed_ship':117441817,'new_colonizer_ship':50333369,'new_colonizer_full_health':True,'native_evade_target_system':37,'rear_loss_cleanup_single_day_ready':passed,'maximum_days_to_cleanup_observation':1,'normal_colonization_route_ready':False,'scope':'Observed native loss and automatic civilian evasion only; registered dead ship not alive, direction-inconsistent war record not victory, no safe transit or full acceptance.'}
out=run/(after+'-loss-evasion-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'alive_military':len(alive),'registered_military':len(registered),'colonizer_full_health':True}),flush=True);assert passed
