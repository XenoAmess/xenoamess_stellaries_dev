"""Independent documented third settlement check; never issues game input."""
import json, logging, re, sys, zipfile
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

before, after = sys.argv[1:]
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run/n).read_text('utf-8'))
omit = lambda t, ks: [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
objects = lambda t: {k:v for k,v,o in q.fields(t) if o}
o = load(after+'-third-boundary-observation.json')
bs, az = o['before_state'], o['after_state']
b, a = bs['audit'], az['audit']
bc, ac = b['countries']['0'], a['countries']['0']
bcr, acr = bs['country0_raw'], az['country0_raw']
sp, ap = b['planets']['1085'], a['planets']['1085']
mb, ma = b['planets']['7'], a['planets']['7']
cb, ca = b['colonies']['0'], a['colonies']['0']
cal = load(after+'-calendar-receipt.json')
ce = load(after+'-calendar-execution.json')
oe = load(after+'-boundary-observation-execution.json')
pre = load('terravore-third-threshold29-third-threshold29-proof.json')
pe = load('terravore-third-threshold29-observer-execution.json')

def read_roots(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:
        return {k:v for k,v,obj in q.fields(z.read('gamestate').decode('utf-8-sig')) if obj}

br, ar = read_roots(before), read_roots(after)
barmy, aarmy = [objects(t['army']) for t in [br,ar]]
source_armies = [16777366,33554561,33554528,50331796]
owned_before, owned_after = [q.ids(q.block(t,'owned_armies')) for t in [bcr,acr]]
army_entries = {str(i): {'before': [(v,obj) for k,v,obj in q.fields(br['army']) if k==str(i)], 'after': [(v,obj) for k,v,obj in q.fields(ar['army']) if k==str(i)]} for i in owned_before}
army_inv = run/(after+'-source-defense-cleanup-investigation.json')
assert not army_inv.exists()
h.write_json(army_inv, {'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'owned_before':owned_before,'owned_after':owned_after,'entries':army_entries})

def queues(t):
    c=t['construction']
    return objects(q.block(q.block(c,'queue_mgr'),'queues')), objects(q.block(q.block(c,'item_mgr'),'items'))
bq, bi = queues(br)
aq, ai = queues(ar)
def queue(t,key):
    raw=q.block(t,key);ts=list(q.tokens(raw))
    if not ts:return {}
    assert ts[0][0]=='{' and ts[-1][0]=='}'
    return q.scalars(raw[ts[0][2]:ts[-1][1]])
bt, at = bc['tech_status'], ac['tech_status']
beng, aeng = [queue(t,'engineering_queue') for t in [bt,at]]
science = {k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bank_delta = {k:D(str(ac['research_stockpile'].get(k,0)))-D(str(bc['research_stockpile'].get(k,0))) for k in q.RESEARCH_RESOURCES}
stocks = set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
delta = {k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in stocks}
gross = {k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['income'].values()),D(0)) for k in ['minerals','alloys']}
reward_m = min(D(1000),max(D(100),gross['minerals']*5))
reward_a_raw = gross['alloys']*3
reward_a = reward_a_raw.quantize(D(1),rounding=ROUND_HALF_UP)
dep_types = [b['deposits'][str(i)]['type'] for i in sp['deposits']]
source_district_count = sum(b['districts'][str(i)]['level'] for i in b['colonies']['37']['districts'])
free_slots = sp['planet_size']-dep_types.count('d_lithoid_devastation')-dep_types.count('d_massive_glacier')-source_district_count
bites = (free_slots+1)//2
messages = [q.scalars(v) for v in o['new_native_bite_messages_raw']]
expected_messages = [dict(type='MESSAGE_TERRAVORE_CONSUME_WORLD',localization='MESSAGE_TERRAVORE_CONSUME_WORLD_'+kind+'_TEXT',receiver=0,target_planet=1085,end='2272.10.02',date='2272.07.02',notification=255+i,message_type='none') for i,kind in enumerate(['ALLOYS','MINERALS','ALLOYS'])]

def modifiers(p):
    return [q.scalars(v) for v in re.findall(r'\{([^{}]+)\}',p['modifiers'])]
def objectives(c):
    return [q.scalars(v) for k,v,obj in q.fields(q.block(c,'crisis_progression')) if k=='objective' and obj]
def source_flags_ok():
    done=['eep_bites_done','eep_population_done','eep_crisis_done','eep_destroy_done','eep_credit_done','eep_return_done']
    expected={k:63434424 for k in done}
    expected['superior_colonies_can_be_boosted']={'flag_date':63413520,'flag_days':2729}
    expected['recently_eaten_planet']={'flag_date':63434424,'flag_days':360}
    return ap['flags']==expected
timers=['entered_war_as_defender','recent_first_contact_process_started','recent_cara_3010','discovered_site','was_recently_targeted_by_voidworms']
def flags_ok():
    old,new=[q.block(c,'flags') for c in [bcr,acr]]
    return (omit(old,set(timers))==omit(new,set(timers+['eep_notice_pending']))
        and all(omit(q.block(old,k),{'flag_days'})==omit(q.block(new,k),{'flag_days'}) and q.scalars(q.block(old,k))['flag_days']-q.scalars(q.block(new,k))['flag_days']==1 and q.scalars(q.block(new,k))['flag_days']>0 for k in timers))
def modules_ok():
    old,new=[q.block(c,'modules') for c in [bcr,acr]]
    ev=[q.block(v,'standard_event_module') for v in [old,new]]
    de=[q.block(v,'delayed_event') for v in ev]
    return (omit(old,{'standard_event_module','standard_economy_module'})==omit(new,{'standard_event_module','standard_economy_module'})
        and omit(q.block(old,'standard_economy_module'),{'resources'})==omit(q.block(new,'standard_economy_module'),{'resources'})
        and omit(ev[0],{'delayed_event'})==omit(ev[1],{'delayed_event'})
        and omit(de[0],{'days'})==omit(de[1],{'days'}) and q.scalars(de[0])['event']==q.scalars(de[1])['event']=='paragon.999'
        and q.scalars(de[0])['days']-q.scalars(de[1])['days']==1)
def projects_ok():
    old,new=[q.block(c,'events') for c in [bcr,acr]]
    ps=[{q.scalars(v)['id']:v for k,v,obj in q.fields(t) if k=='special_project' and obj} for t in [old,new]]
    return (ps[0].keys()==ps[1].keys() and {4,5}<=ps[1].keys() and omit(old,{'special_project'})==omit(new,{'special_project'})
        and all(ps[0][i]==ps[1][i] if i not in [4,5] else omit(ps[0][i],{'days_left'})==omit(ps[1][i],{'days_left'}) and q.scalars(ps[0][i])['days_left']-q.scalars(ps[1][i])['days_left']==1 and q.scalars(ps[1][i])['debris']=={4:16777219,5:369098752}[i] for i in ps[0]))
def military(s):
    return {i for fid,raw in s['owned_fleets_raw'].items() if q.scalars(raw).get('ship_class')=='shipclass_military' for i in q.ids(q.block(raw,'ships'))}
bm, am = military(bs), military(az)
foundation=load('terravore-rear-clearing-first-born-calibration-war1-battle-v65-proof.json')
def ship_ok(i):
    old,new=[s['owned_ships_raw'][str(i)] for s in [bs,az]]
    os,ns=q.scalars(old),q.scalars(new)
    return (q.block(old,'ship_design_implementation')==q.block(new,'ship_design_implementation')
        and all(os.get(k)==ns.get(k) for k in ['fleet','construction_date','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints','last_combat_activity','last_damage','experience','upgrade_progress'])
        and all(0<=D(str(os[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
        and ns.get('killed')!='yes' and D(str(ns['hitpoints']))>0)
expected_vars=dict(bc['variables']);expected_vars.update(eep_c=49,eep_d=14,eep_last_capacity=3,eep_last_return=289,eep_previous_capacity=11,eep_worlds=3)
expected_flags=dict(bc['flags']);expected_flags['eep_notice_pending']=63434424
capacity_flags=dict(mb['flags']);capacity_flags.update({k:63434424 for k in ['uncapped_mining_districts','uncapped_farming_districts','uncapped_generator_districts']})
native_blocker=run/'native-blocker-clear-01_blocker_deposits.txt'
game_blocker=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/deposits/01_blocker_deposits.txt')
blockers=native_blocker.read_text('utf-8-sig')
native_obj=run/'native-war1-menace-00_crisis_objectives.txt'

checks={
 'fixed_single_original_July1_to_July2_pair':before=='terravore-third-threshold29' and after=='terravore-third-settlement-native' and b['date']=='2272.07.01' and a['date']=='2272.07.02' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='1c51e8c1e95e497273029fad8f3a30f2672e9d43e983ec252b4ff8b3f8601087' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='010da3f958056fac1b5de8c065c6bc6497fdc38763c7c353f7ecfd7175868352',
 'prior_threshold34_PASS_actual0_bound_source':pre['status']=='PASS_NATIVE_TERRAVORE_THIRD_THRESHOLD29_COMPONENT' and len(pre['checks'])==34 and all(v is True for v in pre['checks'].values()) and pre['third_settlement_day_ready'] is True and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_third_threshold29_observer.py')=='08bfc8bc12d3e9c84fd63dc48ad06ea860bd46cae4faa591aed5eed09bb72932' and pre['after_sha256']==b['save_sha256'],
 'native_calendar_actual0_source_and_one_day':cal['status']=='CALENDAR_CONFIRMED' and cal['days']==1 and cal['start_date']==b['date'] and cal['date']==a['date'] and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
 'full_boundary_observation6_actual0_SHA_bound':o['status']=='OBSERVED_NATIVE_TERRAVORE_THIRD_BOUNDARY' and len(o['checks'])==6 and all(v is True for v in o['checks'].values()) and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_third_boundary_observation.py')=='a11ed89e421e5fc177130377cb322dcf4d96fb9b7c900bca24af411f750ec801' and h.sha256(run/(after+'-third-boundary-observation.json'))=='13cc045a091e5804876d1b86b031e2df3a52295e6ea1928accb66e3d57b3c115',
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_zero_growth':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'native_blocker_primary_source_matches_game_minus1_each':h.sha256(native_blocker)==h.sha256(game_blocker) and all(q.scalars(q.block(q.block(blockers,k),'planet_modifier'))['planet_max_districts_add']==-1 for k in ['d_lithoid_devastation','d_massive_glacier']),
 'source_free_slots6_bites3_independent_from_deposits_and_district':dep_types.count('d_lithoid_devastation')==4 and dep_types.count('d_massive_glacier')==1 and source_district_count==1 and free_slots==6 and bites==3,
 'exact_three_native_A_M_A_messages_no_POP_branch':messages==expected_messages and len(messages)==bites,
 'only_these_three_new_country_messages':o['new_country0_messages_raw']==o['new_native_bite_messages_raw'] and all(v in az['messages_country0_raw'] for v in bs['messages_country0_raw']),
 'reward_formula_actual_gross283_75_and43_325':gross=={'minerals':D('283.75'),'alloys':D('43.325')} and reward_m==1000 and reward_a_raw==D('129.975') and reward_a==130,
 'true_native_M1000_A260_Menace750_stocks_only':delta['minerals']==reward_m and delta['alloys']==reward_a*2 and delta['menace']==750 and all(delta[k]==0 for k in stocks-set(q.RESEARCH_RESOURCES)-{'minerals','alloys','menace'}),
 'no_duplicate_resource_month_budget_held':bc['budget_categories']==ac['budget_categories'],
 'native_single_research_tick_P_S_bank':all(abs(bank_delta[k]-science[k]*D('1.33'))<=D('0.00005') for k in ['physics_research','society_research']) and bank_delta['engineering_research']==0,
 'same_mass_drivers3_progress_single_tick_other_tech_held':omit(bt,{'stored_techpoints','engineering_queue'})==omit(at,{'stored_techpoints','engineering_queue'}) and {k:v for k,v in beng.items() if k!='progress'}=={k:v for k,v in aeng.items() if k!='progress'} and aeng['technology']=='tech_mass_drivers_3' and abs(D(str(aeng['progress']))-D(str(beng['progress']))-science['engineering_research']*D('1.33'))<=D('0.00005'),
 'exact_return289_mother11123_total_population_conserved':cb['actual_pop_sum']==10834 and b['colonies']['37']['actual_pop_sum']==289 and ca['actual_pop_sum']==11123 and a['colonies']['37']['actual_pop_sum']==0 and ca['actual_pop_sum']==cb['actual_pop_sum']+b['colonies']['37']['actual_pop_sum'],
 'species73_only_migration_not_manufacture_or_other_species':bs['species_population_by_colony']=={'0:73':10834,'37:73':289} and az['species_population_by_colony']=={'0:73':11123} and b['species']==a['species'],
 'native_growth_records_held_no_second_growth_tick':all(q.block(bs['colony_raw'][k],'last_month_growth_data')==q.block(az['colony_raw'][k],'last_month_growth_data') for k in ['0','37']),
 'source_empty_pop_groups_and_removed_ownership':a['colonies']['37']['pop_groups']==[] and ac['owned_colonies']==[0] and bc['owned_colonies']==[0,37] and 'owner' not in ap and 'controller' not in ap,
 'housing_total14100_usage10827_cache_lag296_explicit':ca['total_housing']==14100 and ca['housing_usage']==cb['housing_usage']==10827 and ca['free_housing']==3273 and ca['actual_pop_sum']-ca['housing_usage']==296==7+289 and ca['employable_pops']==ca['num_sapient_pops']==11123 and ca['free_amenities']>0 and ca['crime']==0,
 'EEP_only_exact_C12_D3_world1_return289_delta':ac['variables']==expected_vars and ac['variables']['eep_d']==2+ac['variables']['eep_c']//4 and ac['variables']['eep_c']-bc['variables']['eep_c']==sp['variables']['eep_q']==12,
 'native_population_no_artificial_G_made_or_extra_entitlement':all(ac['variables'][k]==bc['variables'][k]==0 for k in ['eep_g','eep_made','eep_delta','eep_entitled','eep_last_manufactured']) and ac['variables']['eep_psi']==1,
 'Queen_only_pending_notice_stage1_no_high_or_fleet_stage':ac['flags']==expected_flags and ac['variables']['eep_stage']==1 and ac['variables']['eep_fleet_stage']==0 and ac['variables']['eep_c']==49<60,
 'unique_owned_core_physical7_size18_and_original_deposit1573':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and ma['owner']==ma['controller']==ma['colony']==0 and ma['planet_size']==mb['planet_size']==18 and ma['deposits']==mb['deposits'] and a['deposits']['1573']==b['deposits']['1573']=={'type':'d_eep_core','deposit_holder':{'type':0,'id':7}},
 'single_permanent_capacity14_and_court_same_no_stacking':modifiers(mb)==[{'modifier':'eep_court','days':-1},{'multiplier':11,'modifier':'eep_capacity','days':-1}] and modifiers(ma)==[{'modifier':'eep_court','days':-1},{'multiplier':14,'modifier':'eep_capacity','days':-1}] and ma['variables']==dict(mb['variables'],eep_capacity_value=14),
 'core_uncapped_flags_refreshed_original_core_flag_held':ma['flags']==capacity_flags and ma['bombardment_damage']==0,
 'paid_districts27_capacity32_no_free_district':all(a['districts'][str(i)]==b['districts'][str(i)] for i in [1,2,3]) and [(a['districts'][str(i)]['type'],a['districts'][str(i)]['level']) for i in [1,2,3]]==[('district_hive',5),('district_generator',7),('district_mining',15)] and sum(a['districts'][str(i)]['level'] for i in [1,2,3])==27<ma['planet_size']+ac['variables']['eep_d']==32,
 'mother_zones_and_all_buildings_held_no_free_construction':all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','104']) and br['buildings']==ar['buildings'],
 'all_mother_job_caps_held_technician1400':{i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in b['pop_jobs'].items() if j['planet']==0}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in a['pop_jobs'].items() if j['planet']==0} and len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['max_workforce']==j['workforce_limit']==1400])==1,
 'source_shattered_size12_modifiers_deposits_removed':ap['planet_class']=='pc_shattered' and ap['planet_size']==sp['planet_size']==12 and ap['modifiers']=='' and ap['deposits']==[],
 'source_devastation_exact_three_regular_bites_plus60':D(str(ap['bombardment_damage']))-D(str(sp['bombardment_damage']))==20*bites==60,
 'source_six_done_flags_cleanup_and_native_cooldown_reset':source_flags_ok() and ap['variables']==dict(sp['variables'],eep_return_amount=289),
 'original_situation_killed_no_live_EEP_or_native_duplicate':a['situations']['100663299']==dict(b['situations']['100663299'],killed='yes') and not any(v.get('type') in ['situation_eep_devouring','situation_terravore_consume_planet'] and v.get('killed')!='yes' for v in a['situations'].values()),
 'empty_source_planet_army_queues_only_owner_invalidated':all(q.ids(q.block(bq[k],'items'))==q.ids(q.block(aq[k],'items'))==[] and q.scalars(bq[k])['owner']==0 and q.scalars(aq[k])['owner']==4294967295 and omit(bq[k],{'owner'})==omit(aq[k],{'owner'}) for k in ['2105','2284']),
 'all_other_owned_queue_structures_held':{k:v for k,v in bq.items() if q.scalars(v).get('owner')==0 and k not in ['2105','2284']}=={k:v for k,v in aq.items() if q.scalars(v).get('owner')==0},
 'exact_four_source_defense_armies_removed_remaining12_held':owned_after==[i for i in owned_before if i not in source_armies] and len(owned_after)==12 and all(q.scalars(barmy[str(i)])['owner']==0 and q.scalars(barmy[str(i)])['colony']==37 and q.scalars(barmy[str(i)])['type']=='defense_army' and army_entries[str(i)]['after']==[('none',False)] for i in source_armies) and all(barmy[str(i)]==aarmy[str(i)] for i in owned_after),
 'nemesis_level1_original_ship135_plus_only_world750':q.scalars(q.block(bcr,'crisis_progression'))==q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and objectives(bcr)==[{'objective':'crisobj_destroy_enemy_ships','progress':135}] and objectives(acr)==objectives(bcr)+[{'objective':'crisobj_destroy_worlds','progress':750}],
 'true_Menace885_below1000_not_mineral_ship_unlock':bc['effective_stockpile']['menace']==135 and ac['effective_stockpile']['menace']==885<1000 and all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions']) and native_obj.exists(),
 'same_owned_fleets_all_ships_and_original28_military_naval140':bs['owned_fleets']==az['owned_fleets'] and bs['owned_ship_ids']==az['owned_ship_ids'] and bm==am==set(foundation['actual_alive_military_ship_ids']) and len(am)==28 and q.scalars(acr)['fleet_size']==140,
 'all28_military_same_identity_design_max_only_natural_repair':all(ship_ok(i) for i in am),
 'no_owned_combat_no_new_war1_battle':bs['war1_battles_raw']==az['war1_battles_raw'] and all(not q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in az['owned_fleets_raw'].values()),
 'original_lost_colonizer_still_none_target523_held':bs['original_ship16779140_entry']==az['original_ship16779140_entry']==[['none',False]] and bs['original_fleet16778062_entry']==az['original_fleet16778062_entry']==[['none',False]] and bs['planet_raw']['523']==az['planet_raw']['523'],
 'science_only_orientation_and_native_shield200_to208':omit(bs['owned_ships_raw']['1'],{'rotation','forward_x','forward_y','shield_hitpoints'})==omit(az['owned_ships_raw']['1'],{'rotation','forward_x','forward_y','shield_hitpoints'}) and q.scalars(bs['owned_ships_raw']['1'])['shield_hitpoints']==200 and q.scalars(az['owned_ships_raw']['1'])['shield_hitpoints']==208 and bs['owned_fleets_raw']['1']==az['owned_fleets_raw']['1'],
 'all_other_owned_civilian_stations_raw_held':all(bs['owned_ships_raw'][str(i)]==az['owned_ships_raw'][str(i)] for i in set(bs['owned_ship_ids'])-bm-{1}),
 'physics_paid_order_unfinished_exact264_6_plus1_4':q.ids(q.block(aq['0'],'items'))==[1258291211] and omit(bi['1258291211'],{'progress'})==omit(ai['1258291211'],{'progress'}) and q.scalars(bi['1258291211'])['progress']==263.2 and q.scalars(ai['1258291211'])['progress']==264.6<360,
 'rear_paid_colonizer_order_unborn_exact266_plus1_33':q.ids(q.block(aq['2287'],'items'))==[83886124] and omit(bi['83886124'],{'progress'})==omit(ai['83886124'],{'progress'}) and q.scalars(bi['83886124'])['progress']==264.67 and q.scalars(ai['83886124'])['progress']==266<360,
 'five_native_country_timers_only_minus1_with_notice':flags_ok(),
 'known_debris_only_minus1_no_new_special_project':projects_ok(),
 'native_paragon_timer_and_economy_mirror_only_modules':modules_ok(),
 'original_inactive264_only_pending_no_Queen_popup':bs['pending_country0_raw']==az['pending_country0_raw'] and len(az['pending_country0_raw'])==1 and q.scalars(az['pending_country0_raw'][0])=={'id':264,'event':'grand_archive.2800','date':'2273.12.20','country':0},
 'old_first_contact16777275_and_all_history_raw_held':bs['first_contact16777275_raw']==az['first_contact16777275_raw'] and br['open_player_event_selection_history']==ar['open_player_event_selection_history'],
}
passed=all(v is True for v in checks.values())
p={'status':'PASS_NATIVE_TERRAVORE_THIRD_SETTLEMENT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'actual_research_bank_delta':{k:str(v) for k,v in bank_delta.items()},'actual_source_free_slots':free_slots,'actual_regular_bites':bites,'actual_core_population':ca['actual_pop_sum'],'actual_core_capacity':14,'actual_total_district_capacity':32,'actual_alive_military_ship_ids':sorted(am),'source_defense_cleanup_evidence_sha256':h.sha256(army_inv),'housing_cache_refresh_pending':True,'housing_cache_lag':296,'queen_notice_month_refresh_pending':True,'calendar_ready':False,'third_settlement_accepted':passed,'scope':'Native third settlement only. Housing and monthly notice refresh still pending. No mineral fleet, fourth colony, physics completion, new colonizer birth or full Terravore route acceptance.'}
out=run/(after+'-third-settlement-proof.json')
assert not out.exists()
h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'population':p['actual_core_population'],'capacity':14,'stocks':p['actual_stock_deltas']}),flush=True)
assert passed,'Original settlement retained; do not replay calendar or random rewards'
