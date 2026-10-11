"""Documented exact native dead-ship cleanup and reinforcement contact boundary."""
import json,logging,sys
from pathlib import Path
before,after=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8'));omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
obs_path=run/(after+'-construction-boundary-observation.json');obs=load(obs_path.name);oe=load(after+'-boundary-observation-execution.json');iv_path=run/(after+'-rear97-native-inventory.json');iv=load(iv_path.name);ie=load(after+'-rear97-native-inventory-execution.json')
b,a=obs['before_state'],obs['after_state'];ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0'];bcr,acr=b['country0_raw'],a['country0_raw'];eb,ea=iv[before],iv[after]
cal=load(after+'-calendar-receipt.json');ce=load(after+'-calendar-execution.json');pre=load(cal['prior_proof_file']);pe=load(cal['prior_execution_stage']+'-execution.json')
first=False;days=1;country_timers=['entered_war_as_defender','recent_first_contact_process_started','recent_cara_3010','discovered_site','was_recently_targeted_by_voidworms']
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

def mother_flag_ok():
 old,new=b['planet_raw']['7'],a['planet_raw']['7'];of,nf=q.block(old,'flags'),q.block(new,'flags');key='nomad_recent_combat'
 return omit(old,{'flags'})==omit(new,{'flags'}) and omit(of,{key})==omit(nf,{key}) and q.scalars(q.block(of,key))=={'flag_date':63436152,'flag_days':60} and q.scalars(q.block(nf,key))=={'flag_date':63436152,'flag_days':59}

reinforcement={'788','33555013','33555034','100664127'};combat_ships={'1807','1810','1816','1895','1896','33555519'};moving={'67110639','50333369'}
move_fields={'coordinate','target_coordinate','rotation','forward_x','forward_y','post_move_angle','speed'}
combat_fields=move_fields|{'section','formation_pos','targeting_module','targeting','disengagement_opportunities_used'}
def reinforcement_ships_ok():
 return all(omit(b['owned_ships_raw'][i],combat_fields if i in combat_ships else move_fields)==omit(a['owned_ships_raw'][i],combat_fields if i in combat_ships else move_fields) for i in combat_ships|moving)
def reinforcement_fleets_ok():
 return all(omit(b['owned_fleets_raw'][i],{'combat','fleet_stats','movement_manager','properties'})==omit(a['owned_fleets_raw'][i],{'combat','fleet_stats','movement_manager','properties'}) and q.block(b['owned_fleets_raw'][i],'current_order')==q.block(a['owned_fleets_raw'][i],'current_order') and q.ids(q.block(q.block(a['owned_fleets_raw'][i],'combat'),'in_combat_with'))==([] if i=='100664127' else [825]) and q.scalars(q.block(q.block(a['owned_fleets_raw'][i],'movement_manager'),'coordinate'))['origin']==97 for i in reinforcement)
def enemy_ok():
 if eb['enemy825_ship_ids']!=ea['enemy825_ship_ids'] or len(ea['enemy825_ship_ids'])!=12 or eb['enemy825_country1_owned'] is not True or ea['enemy825_country1_owned'] is not True:return False
 for i in eb['enemy825_ship_ids']:
  old,new=eb['enemy825_ships_raw'][str(i)],ea['enemy825_ships_raw'][str(i)];os,ns=q.scalars(old),q.scalars(new)
  if q.block(old,'ship_design_implementation')!=q.block(new,'ship_design_implementation'):return False
  for k in ['hitpoints','armor_hitpoints','shield_hitpoints']:
   if i==16779083 and k=='armor_hitpoints':
    if (os.get(k,0),ns.get(k,0))!=(625,273.0341):return False
   elif os.get(k,0)!=ns.get(k,0):return False
 return True
military={i for fid,f in a['owned_fleets_raw'].items() if q.scalars(f).get('ship_class')=='shipclass_military' for i in q.ids(q.block(f,'ships'))}
col=q.scalars(a['owned_ships_raw']['50333369']);cf=a['owned_fleets_raw']['33555278'];station=q.scalars(a['owned_ships_raw']['67109591'])
owned_queues=lambda st:{k:v for k,v,o in q.fields(q.block(q.block(st['raw_roots']['construction'],'queue_mgr'),'queues')) if o and q.scalars(v).get('owner')==0}
checks={
 'actual6_observation_source_SHA':len(obs['checks'])==6 and all(v is True for v in obs['checks'].values()) and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_construction_boundary_observation.py')=='e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
 'actual4_inventory_source_SHA':len(iv['checks'])==4 and all(v is True for v in iv['checks'].values()) and ie['returncode']==0 and ie['helper_sha256']==h.sha256(run/'priority_terravore_rear97_native_inventory_v2.py')=='ad06a4fe55b739820553f71774d60774cd1b936ad5f40dfc0177be270e888f14' and h.sha256(iv_path)=='6937d886945cb68eab21199f44ba154a8358af28c7977310bbea75f2ed9407a3',
 'prior36_all_PASS_actual0_source_and_ready':pre['status']=='PASS_NATIVE_TERRAVORE_REAR97_FIRST_CORVETTE_LOSS_CIVILIAN_EVASION_COMPONENT' and len(pre['checks'])==36 and all(v is True for v in pre['checks'].values()) and pre['rear_loss_cleanup_single_day_ready'] is True and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_rear97_first_loss_evasion_guard_v2.py')=='d8afe1952bc336559f137a0d0fd86c6023b0337364cbe24e81ae80609bf53ac3',
 'single_native_day_actual0_source_dates':ba['date']=='2272.09.14' and aa['date']=='2272.09.15' and cal['days']==1 and cal['status']=='CALENDAR_CONFIRMED' and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
 'original_SAV_SHA_pair':all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav'))==x['save_sha256'] for st,name,x in [(b,before,eb),(a,after,ea)]) and pre['after_sha256']==obs['before_sha256'],
 'production41_tree_Chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'original_unfiltered_error_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'exact_known_dead_ship_and_fleet_removed_no_new_entities':set(b['owned_ship_ids'])-set(a['owned_ship_ids'])=={117441817} and not set(a['owned_ship_ids'])-set(b['owned_ship_ids']) and set(b['owned_fleets'])-set(a['owned_fleets'])=={16778073} and not set(a['owned_fleets'])-set(b['owned_fleets']),
 '27_positive_HP_alive_military_naval140_old_cache':len(military)==27 and all(q.scalars(a['owned_ships_raw'][str(i)]).get('killed')!='yes' and q.scalars(a['owned_ships_raw'][str(i)])['hitpoints']>0 for i in military) and q.scalars(acr)['fleet_size']==140,
 'all_owned_remaining_designs_held':all(q.block(v,'ship_design_implementation')==q.block(b['owned_ships_raw'][i],'ship_design_implementation') for i,v in a['owned_ships_raw'].items()),
 'six_reinforcements_native_combat_seventh_moving_only':reinforcement_ships_ok() and reinforcement_fleets_ok(),
 'colonizer_full_HP_same_order_evade37_still97':(col['hitpoints'],col['armor_hitpoints'],col['shield_hitpoints'])==(625,125,320) and q.block(b['owned_fleets_raw']['33555278'],'current_order')==q.block(cf,'current_order') and q.scalars(q.block(q.block(q.block(q.block(cf,'current_order'),'evade_hostiles_order'),'sub_order'),'move_to_system_point_order'))=={'can_reach':'yes','commissioner':4294967295} and q.scalars(q.block(q.block(cf,'movement_manager'),'coordinate'))=={'x':26.09618,'y':-13.12609,'origin':97} and q.ids(q.block(q.block(cf,'combat'),'in_combat_with'))==[825],
 'rear_station_fullHP_exact_native_repair_damage_base_owner_held':station['hitpoints']==18300 and station['armor_hitpoints']==4999.34353 and station['shield_hitpoints']==3596.20377 and station['fleet']==804 and 804 in a['owned_fleets'] and eb['rear153_raw']==ea['rear153_raw'],
 'enemy12_identity_design_and_only_one_exact_armor_damage':enemy_ok(),
 'all_other_ships_held_only1916_original_repair':all(v==b['owned_ships_raw'][i] for i,v in a['owned_ships_raw'].items() if i not in combat_ships|moving|{'1916','67109591'}) and omit(b['owned_ships_raw']['1916'],{'armor_hitpoints'})==omit(a['owned_ships_raw']['1916'],{'armor_hitpoints'}) and q.scalars(a['owned_ships_raw']['1916'])['armor_hitpoints']-q.scalars(b['owned_ships_raw']['1916'])['armor_hitpoints']==0.625,
 'all_other_fleets_held':all(v==b['owned_fleets_raw'][i] for i,v in a['owned_fleets_raw'].items() if i not in reinforcement|{'804','33555278'}),
 'messages_pending_and_war_held_no_new_rewards':b['messages_country0_raw']==a['messages_country0_raw'] and b['pending_country0_raw']==a['pending_country0_raw'] and b['war1_battles_raw']==a['war1_battles_raw'],
 'mother_only60_to59_native_flag_and_EEP_colony_population_housing_held':mother_flag_ok() and bc['variables']==ac['variables'] and b['colony_raw']==a['colony_raw'] and aa['colonies']['0']['actual_pop_sum']==11137 and aa['colonies']['0']['total_housing']==14100,
 'source_original_two_timers_only':source_timers_ok(),
 'all_core_districts_zones_buildings_deposits_designs_history_held':all(b['raw_roots'][k]==a['raw_roots'][k] for k in ['districts','zones','buildings','deposit','ship_design','open_player_event_selection_history']),
 'true_stocks_banks_budget_technology_and_Menace885_held':all(bc[k]==ac[k] for k in ['effective_stockpile','research_stockpile','budget_categories','tech_status']) and ac['effective_stockpile']['menace']==885,
 'jobs_and_species_population_held':b['species_population_by_colony']==a['species_population_by_colony'] and {i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in ba['pop_jobs'].items()}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in aa['pop_jobs'].items()},
 'all12_owned_queues_still_empty':owned_queues(b)==owned_queues(a) and len(owned_queues(a))==12 and all(not q.ids(q.block(v,'items')) for v in owned_queues(a).values()),
 'target523_and_original_dead_colonizer_entries_held':b['planet_raw']['523']==a['planet_raw']['523'] and b['original_ship16779140_entry']==a['original_ship16779140_entry'] and b['original_fleet16778062_entry']==a['original_fleet16778062_entry'],
 'armies_government_traditions_AP_and_true_crisis_held':q.ids(q.block(bcr,'owned_armies'))==q.ids(q.block(acr,'owned_armies')) and len(q.ids(q.block(acr,'owned_armies')))==12 and all(bc[k]==ac[k] for k in ['government','traditions','ascension_perks']) and q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression'),
 'known_country_and_modules_project_timers_only':timers_ok() and modules_ok() and projects_ok(),
 'country_other_fields_and_fleet_manager_other_fields_held':omit(bcr,{'events','flags','sensor_range_fleets','modules','fleets_manager'})==omit(acr,{'events','flags','sensor_range_fleets','modules','fleets_manager'}) and omit(q.block(bcr,'fleets_manager'),{'owned_fleets'})==omit(q.block(acr,'fleets_manager'),{'owned_fleets'}),
 'complete_exact_delta_investigation_SHA_pair':h.sha256(run/(after+'-exact-delta-investigation-v2.json'))=='e26eaf5759cfbb17b255ece893ed4fa602789b65812fe935cb53f57cff018770',
}
passed=all(v is True for v in checks.values());proof={'status':'PASS_NATIVE_TERRAVORE_REAR97_DEAD_CORVETTE_CLEANUP_REINFORCEMENT_CONTACT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'alive_military_ship_ids':sorted(military),'native_evade_target_system':37,'rear_battle_single_day_ready':passed,'maximum_days_to_battle_observation':1,'normal_colonization_route_ready':False,'scope':'Known native dead ship cleanup and first reinforcement contact only; colonizer still97/combat825, no transit/full acceptance.'}
out=run/(after+'-cleanup-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date']}),flush=True);assert passed
