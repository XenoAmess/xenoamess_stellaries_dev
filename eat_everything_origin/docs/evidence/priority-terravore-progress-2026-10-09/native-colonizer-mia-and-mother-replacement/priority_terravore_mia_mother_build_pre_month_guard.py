"""Bounded native rear combat observation with explicit non-PASS boundary stops."""
import json,logging,sys
from pathlib import Path
before,after=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8'));omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
obs=load(after+'-construction-boundary-observation.json');oe=load(after+'-boundary-observation-execution.json');iv=load(after+'-rear97-native-inventory-v4.json');ie=load(after+'-rear97-native-inventory-v4-execution.json')
b,a=obs['before_state'],obs['after_state'];ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0'];bcr,acr=b['country0_raw'],a['country0_raw'];eb,ea=iv[before],iv[after]
cal=load(after+'-calendar-receipt.json');ce=load(after+'-calendar-execution.json');pre=load(cal['prior_proof_file']);pe=load(cal['prior_execution_stage']+'-execution.json');days=cal['days'];first=False
country_timers=['entered_war_as_defender','recent_first_contact_process_started','recent_cara_3010','discovered_site','was_recently_targeted_by_voidworms']
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
        and all(old['flags'][k]['flag_date']==new['flags'][k]['flag_date'] and old['flags'][k]['flag_days']-new['flags'][k]['flag_days']==days for k in timers))

def mother_flag_ok():
 old,new=b['planet_raw']['7'],a['planet_raw']['7'];of,nf=q.block(old,'flags'),q.block(new,'flags');key='nomad_recent_combat';os,ns=q.scalars(q.block(of,key)),q.scalars(q.block(nf,key))
 return omit(old,{'flags'})==omit(new,{'flags'}) and omit(of,{key})==omit(nf,{key}) and os['flag_date']==ns['flag_date']==63436152 and os['flag_days']-ns['flag_days']==days and ns['flag_days']>0

def colony_only_amenities_cache_ok():
 if b['colony_raw'].keys()!=a['colony_raw'].keys():return False
 for i,old in b['colony_raw'].items():
  new=a['colony_raw'][i]
  if i!='0':
   if old!=new:return False
  else:
   x,y=q.scalars(old),q.scalars(new)
   if omit(old,{'amenities','free_amenities'})!=omit(new,{'amenities','free_amenities'}):return False
   if abs((y['amenities']-x['amenities'])-(y['free_amenities']-x['free_amenities']))>0.001 or not 0<=y['free_amenities']<=y['amenities']:return False
 return ba['pop_jobs']==aa['pop_jobs']

def own_design_registry_ok():
 old,new=q.block(bcr,'ship_design_collection'),q.block(acr,'ship_design_collection')
 return old==new and all(q.block(b['raw_roots']['ship_design'],str(i))==q.block(a['raw_roots']['ship_design'],str(i)) for i in q.ids(q.block(old,'ship_design')))

def military(st):
 return {i for fid,f in st['owned_fleets_raw'].items() if q.scalars(f).get('ship_class')=='shipclass_military' for i in q.ids(q.block(f,'ships'))}
def alive(st):
 return {i for i in military(st) if q.scalars(st['owned_ships_raw'][str(i)]).get('killed')!='yes' and q.scalars(st['owned_ships_raw'][str(i)]).get('hitpoints',0)>0}
def original_designs_ok():
 return not set(a['owned_ship_ids'])-set(b['owned_ship_ids']) and all(q.block(v,'ship_design_implementation')==q.block(b['owned_ships_raw'][i],'ship_design_implementation') for i,v in a['owned_ships_raw'].items()) and all(q.block(v,'ship_design_implementation')==q.block(eb['enemy825_ships_raw'][i],'ship_design_implementation') for i,v in ea['enemy825_ships_raw'].items() if v and eb['enemy825_ships_raw'].get(i))
def health_valid(raw):
 v=q.scalars(raw)
 return v.get('killed')=='yes' or all(-0.001<=v.get(key,0)<=v.get(maxkey,0)+0.001 for key,maxkey in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
rear={1807,1810,1816,1895,1896,33555519,67110639};bm,am=military(b),military(a);known_dead={i for i in bm if i not in alive(b)};new_lost=alive(b)-alive(a)
colraw=a['owned_ships_raw'].get('50333369','');col=q.scalars(colraw);cf=a['owned_fleets_raw'].get('33555278','');cfpos=q.scalars(q.block(q.block(cf,'movement_manager'),'coordinate'));colhealth={k:col.get(k,0) for k in ['hitpoints','armor_hitpoints','shield_hitpoints']}
station=q.scalars(a['owned_ships_raw'].get('67109591',''));new_messages=[v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
enemy_lost=set(eb['enemy825_ship_ids'])-set(ea['enemy825_ship_ids']);enemy_killed={int(i) for i,raw in ea['enemy825_ships_raw'].items() if raw and (q.scalars(raw).get('killed')=='yes' or q.scalars(raw).get('hitpoints',0)<=0)}
old_order=q.block(b['owned_fleets_raw']['33555278'],'current_order');new_order=q.block(cf,'current_order')
boundaries=[]
if new_lost:boundaries.append('new_owned_military_loss')
if enemy_lost or enemy_killed:boundaries.append('enemy825_loss_or_killed_entity')
if new_messages:boundaries.append('new_country0_message')
if b['pending_country0_raw']!=a['pending_country0_raw']:boundaries.append('pending_changed')
if b['war1_battles_raw']!=a['war1_battles_raw']:boundaries.append('war_battle_history_changed')
if colhealth['hitpoints']!=625 or colhealth['armor_hitpoints']!=125:boundaries.append('colonizer_hull_or_armor_damage')
if q.scalars(q.block(cf,'properties')).get('mia')!='yes':boundaries.append('colonizer_MIA_ended')
if old_order!=new_order:boundaries.append('colonizer_evade_order_changed')
if station.get('hitpoints',0)<6000:boundaries.append('rear_base_HP_below6000')
if set(ea['enemy825_ship_ids'])-set(eb['enemy825_ship_ids']):boundaries.append('enemy_fleet_reinforced')
if not q.ids(q.block(q.block(a['owned_fleets_raw'].get('804',''),'combat'),'in_combat_with')):boundaries.append('rear_base_no_longer_in_combat')
owned_queues=lambda st:{k:v for k,v,o in q.fields(q.block(q.block(st['raw_roots']['construction'],'queue_mgr'),'queues')) if o and q.scalars(v).get('owner')==0}
prior_source=run/Path(pe['command'][1]).name
prior_ok=pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(prior_source) and pre['after_sha256']==obs['before_sha256']
prior_known=pe['helper_sha256'] in {'d8afe1952bc336559f137a0d0fd86c6023b0337364cbe24e81ae80609bf53ac3','84ab88455f270281cb33afee35658085984f0311f0431cfebea5c442faf87148','73358a47fc6afcede8653d7e231942c48914ac87913c87d863fa7e710ac52bc1','d23166b05da6ea19baa562a0809b989546174d33835e853c63e27bc6e35ba56a',h.sha256(Path(__file__))}
checks={
 'actual_complete_observation6_source_and_original_tree':len(obs['checks'])==6 and all(v is True for v in obs['checks'].values()) and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_construction_boundary_observation.py')=='e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
 'actual_native_inventory4_source':len(iv['checks'])==4 and all(v is True for v in iv['checks'].values()) and ie['returncode']==0 and ie['helper_sha256']==h.sha256(run/'priority_terravore_rear97_native_inventory_v4.py')=='e6e8ca9f31893549b6990f5ae2db24df49b212da6fdf864b91b585c86a6d4b20',
 'original_PASS_prior_actual0_source_and_SHA':prior_ok and prior_known,
 'actual_checked_native_calendar_source_and_1_to3_days_before_month_end':cal['status']=='CALENDAR_CONFIRMED' and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and 1<=days<=3 and ba['date']=='2272.09.27' and aa['date']=='2272.09.30',
 'original_SAV_SHA_pair':all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav'))==x['save_sha256'] for st,name,x in [(b,before,eb),(a,after,ea)]),
 'production41_same_tree_Chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered_original2814_error_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'no_free_new_ship_and_all_retained_original_designs':original_designs_ok(),
 'mother20_military_untouched_except1916_native_repair':len(alive(b)-rear)==20 and all(b['owned_ships_raw'][str(i)]==a['owned_ships_raw'].get(str(i)) for i in alive(b)-rear-{1916}) and omit(b['owned_ships_raw']['1916'],{'armor_hitpoints'})==omit(a['owned_ships_raw']['1916'],{'armor_hitpoints'}) and 0<=q.scalars(a['owned_ships_raw']['1916'])['armor_hitpoints']-q.scalars(b['owned_ships_raw']['1916'])['armor_hitpoints']<=days*0.625+0.001,
 'survivors_native_HP_armor_shield_within_original_design_caps':all(health_valid(v) for i,v in a['owned_ships_raw'].items() if int(i) in am or i in {'50333369','67109591'}) and all(health_valid(v) for v in ea['enemy825_ships_raw'].values() if v),
 'colonizer_original_fleet_species_and_design_held':col.get('fleet')==33555278 and q.ids(q.block(cf,'ships'))==[50333369] and q.scalars(q.block(colraw,'colonization_data'))=={'species':73},
 'rear_base153_owner_chain_held':eb['rear153_raw']==ea['rear153_raw'] and station.get('fleet')==804 and 804 in a['owned_fleets'] and q.ids(q.block(a['owned_fleets_raw']['804'],'ships'))==[67109591],
 'EEP_colony_population_housing_and_mother_only_known_timer':bc['variables']==ac['variables'] and colony_only_amenities_cache_ok() and aa['colonies']['0']['actual_pop_sum']==11137 and aa['colonies']['0']['total_housing']==14100 and mother_flag_ok(),
 'source_only_original_two_timer_decrements':source_timers_ok(),
 'mother_districts_zones_buildings_deposits_design_registry_held':all(b['raw_roots'][k]==a['raw_roots'][k] for k in ['districts','zones','buildings','deposit']) and own_design_registry_ok(),
 'true_stocks_banks_budget_tech_Menace885_held':all(bc[k]==ac[k] for k in ['effective_stockpile','research_stockpile','budget_categories','tech_status']) and ac['effective_stockpile']['menace']==885,
 'jobs_species_population_held':b['species_population_by_colony']==a['species_population_by_colony'] and {i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in ba['pop_jobs'].items()}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in aa['pop_jobs'].items()},
 'original_mother_queue3_order_work3_99_other11_owned_queues_empty':len(owned_queues(a))==12 and {k:v for k,v in owned_queues(b).items() if k!='3'}=={k:v for k,v in owned_queues(a).items() if k!='3'} and all(not q.ids(q.block(v,'items')) for k,v in owned_queues(a).items() if k!='3') and q.ids(q.block(owned_queues(b)['3'],'items'))==q.ids(q.block(owned_queues(a)['3'],'items'))==[100663340] and q.scalars(q.block(q.block(q.block(a['raw_roots']['construction'],'item_mgr'),'items'),'100663340'))=={'queue':3,'paying_country':0,'progress':3.99,'progress_needed':360} and omit(q.block(q.block(q.block(b['raw_roots']['construction'],'item_mgr'),'items'),'100663340'),{'progress'})==omit(q.block(q.block(q.block(a['raw_roots']['construction'],'item_mgr'),'items'),'100663340'),{'progress'}),
 'original_colonizer_MIA_type_return_no_live_combat':q.scalars(cf)['mia_type']=='mia_emergency_ftl' and q.scalars(cf)['return_date']=='2275.08.02' and q.scalars(q.block(cf,'properties'))['mia']=='yes' and not q.ids(q.block(q.block(cf,'combat'),'in_combat_with')),
 'target523_original_dead_colonizer_held':b['planet_raw']['523']==a['planet_raw']['523'] and b['original_ship16779140_entry']==a['original_ship16779140_entry'] and b['original_fleet16778062_entry']==a['original_fleet16778062_entry'],
 'armies_government_traditions_AP_true_crisis_held':q.ids(q.block(bcr,'owned_armies'))==q.ids(q.block(acr,'owned_armies')) and len(q.ids(q.block(acr,'owned_armies')))==12 and all(bc[k]==ac[k] for k in ['government','traditions','ascension_perks']) and q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression'),
 'known_country_modules_and_project_timers':timers_ok() and modules_ok() and projects_ok(),
 'original_missing_zero_cap_exception_actual1_source_investigation_retained':load('terravore-rear97-loss-cleanup-day-stable-rear-battle-observer-execution.json')['returncode']==1 and load('terravore-rear97-loss-cleanup-day-stable-rear-battle-observer-execution.json')['helper_sha256']==h.sha256(run/'priority_terravore_rear97_stable_battle_observer.py')=='fe6ca2d224246ef938d607050af6133493ee1a817f1dc9f41c4546bb60f01e62' and not (run/'terravore-rear97-loss-cleanup-day-stable-rear-battle-proof.json').exists() and h.sha256(run/'terravore-rear97-loss-cleanup-day-enemy-zero-health-cap-investigation.json')=='6f4a4935757324afa14b3c88cb2b9b9693ed0fe4116bca5fa02fa1db1fee6d71',
 'original24_exact3_failures_actual1_driver1_complete_investigation_retained':len(load('terravore-rear97-short-battle-batch1-step1-stable-rear-battle-v2-proof.json')['checks'])==24 and [k for k,v in load('terravore-rear97-short-battle-batch1-step1-stable-rear-battle-v2-proof.json')['checks'].items() if v is not True]==['EEP_colony_population_housing_and_mother_only_known_timer','mother_districts_zones_buildings_deposits_design_registry_held','country_other_fields_and_fleet_manager_other_fields_held'] and load('terravore-rear97-short-battle-batch1-step1-stable-rear-battle-observer-v2-execution.json')['returncode']==1 and load('terravore-rear97-short-battle-batch1-driver-execution.json')['returncode']==1 and h.sha256(run/'terravore-rear97-short-battle-batch1-step1-three-core-failures-investigation.json')=='92e8894a051ccea6afb513d48843c78187a4f829ce566335904266b14c7e4039',
 'naval_native_cache140_or_refreshed135':q.scalars(acr)['fleet_size'] in {140,135} and q.scalars(acr)['used_naval_capacity'] in {140,135} and q.scalars(acr)['military_power']>=0,
 'country_other_fields_and_fleet_manager_other_fields_held':omit(bcr,{'events','flags','sensor_range_fleets','modules','fleets_manager','fleet_size','used_naval_capacity','military_power'})==omit(acr,{'events','flags','sensor_range_fleets','modules','fleets_manager','fleet_size','used_naval_capacity','military_power'}) and omit(q.block(bcr,'fleets_manager'),{'owned_fleets'})==omit(q.block(acr,'fleets_manager'),{'owned_fleets'}),
}
passed=all(v is True for v in checks.values());ready=passed and not boundaries and len(alive(a))==27
status='PASS_NATIVE_TERRAVORE_MIA_MOTHER_BUILD_PRE_MONTH_COMPONENT' if ready else ('OBSERVED_NATIVE_TERRAVORE_REAR97_BOUNDARY' if passed else 'FAIL')
proof={'status':status,'checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'days':days,'boundaries':boundaries,'new_lost_owned_military':sorted(new_lost),'enemy_removed':sorted(enemy_lost),'enemy_killed':sorted(enemy_killed),'new_country0_messages_raw':new_messages,'alive_military_ship_ids':sorted(alive(a)),'registered_military_ship_ids':sorted(am),'known_dead_cleaned':sorted(known_dead-am),'rear_station_health':{k:station.get(k,0) for k in ['hitpoints','armor_hitpoints','shield_hitpoints']},'new_colonizer_health':colhealth,'new_colonizer_position':cfpos,'new_colonizer_order_raw':new_order,'rear_battle_calendar_ready':False,'native_month_boundary_ready':ready,'maximum_days_to_month_boundary':1,'maximum_days_to_battle_observation':(3 if station.get('hitpoints',0)>=12000 and station.get('armor_hitpoints',0)>=2000 and colhealth['shield_hitpoints']==320 else 1) if ready else 0,'normal_colonization_route_ready':False,'scope':'Stable Mod core under bounded native combat; OBSERVED boundary explicitly not a calendar PASS or full acceptance.'}
out=run/(after+'-mia-build-pre-month-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':status,'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'boundaries':boundaries,'base':proof['rear_station_health'],'colonizer_position':cfpos}),flush=True);assert passed
