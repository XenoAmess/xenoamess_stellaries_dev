"""Bounded native rear combat observation with explicit non-PASS boundary stops."""
import json,logging,sys
from decimal import Decimal as D
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
prior_known=pe['helper_sha256'] in {'d8afe1952bc336559f137a0d0fd86c6023b0337364cbe24e81ae80609bf53ac3','84ab88455f270281cb33afee35658085984f0311f0431cfebea5c442faf87148','73358a47fc6afcede8653d7e231942c48914ac87913c87d863fa7e710ac52bc1','d23166b05da6ea19baa562a0809b989546174d33835e853c63e27bc6e35ba56a','005dbcecc139e3df338eaa8666dc31e8b357fbc915d194716b7e25d518598e64',h.sha256(Path(__file__))}

def ordinal(x):
 y,m,d=map(int,x.split('.'));return y*360+(m-1)*30+d-1
ob,oa=ordinal(ba['date']),ordinal(aa['date']);mt=sum(i%30==0 for i in range(ob+1,oa+1));rt=sum(i%30==1 for i in range(ob+1,oa+1))
keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence'];stocks=set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in keys}
delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in stocks}
science={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bank_delta={k:D(str(ac['research_stockpile'].get(k,0)))-D(str(bc['research_stockpile'].get(k,0))) for k in q.RESEARCH_RESOURCES}
def research_queue(t,key):
 raw=q.block(t,key);ts=list(q.tokens(raw))
 if not ts:return {}
 assert ts[0][0]=='{' and ts[-1][0]=='}'
 return q.scalars(raw[ts[0][2]:ts[-1][1]])
bt,at=bc['tech_status'],ac['tech_status'];beng,aeng=[research_queue(t,'engineering_queue') for t in [bt,at]]
cb,ca=ba['colonies']['0'],aa['colonies']['0'];new_growth=ca['actual_pop_sum']-cb['actual_pop_sum'];gr=q.block(a['colony_raw']['0'],'last_month_growth_data');growth=q.scalars(q.block(gr,'growth_and_size'));growth_details=[(k,q.unquote(v),o) for k,v,o in q.fields(q.block(gr,'current_month_growth_details'))]
def population_ok():
 return new_growth==0 if not mt else (new_growth>=0 and growth=={'month_start_size':cb['actual_pop_sum'],'growth':new_growth} and growth_details==[('key','GROWTH_CAT_GROWTH',False),('value',new_growth,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)])
def jobs_ok():
 return ba['pop_jobs'].keys()==aa['pop_jobs'].keys() and all({k:v for k,v in j.items() if k not in {'workforce','bonus_workforce'}}=={k:v for k,v in aa['pop_jobs'][i].items() if k not in {'workforce','bonus_workforce'}} and (aa['pop_jobs'][i]['workforce']>=0 or aa['pop_jobs'][i]['workforce']==j['workforce']==-1) and (aa['pop_jobs'][i]['bonus_workforce']>=0 or aa['pop_jobs'][i]['bonus_workforce']==j['bonus_workforce']==-1) for i,j in ba['pop_jobs'].items())
def item(st):return q.block(q.block(q.block(st['raw_roots']['construction'],'item_mgr'),'items'),'100663340')

checks={
 'original30_exact_two_private_QA_failures_actual1_full_INV_held':len(load('terravore-mother-colonizer3-first-month-mia-build-first-month-proof.json')['checks'])==30 and [k for k,v in load('terravore-mother-colonizer3-first-month-mia-build-first-month-proof.json')['checks'].items() if v is not True]==['mother_districts_zones_buildings_deposits_design_registry_held','jobs_original_structure_and_species73_only'] and load('terravore-mother-colonizer3-first-month-mia-build-guard-execution.json')['returncode']==1 and load('terravore-mother-colonizer3-first-month-mia-build-guard-execution.json')['helper_sha256']==h.sha256(run/'priority_terravore_mia_mother_first_month_guard.py')=='bbaa787ea601cff234a4f72543bca0951ab89d9bf3ae636b503bca00be6dd72a' and h.sha256(run/'terravore-mother-colonizer3-first-month-two-failures-investigation.json')=='44a6c5cf60ba53a321733c9f0e7f326be9f1fa06e3c4d702d9f565a6af80a410',

 'actual_complete_observation6_source_and_original_tree':len(obs['checks'])==6 and all(v is True for v in obs['checks'].values()) and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_construction_boundary_observation.py')=='e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
 'actual_native_inventory4_source':len(iv['checks'])==4 and all(v is True for v in iv['checks'].values()) and ie['returncode']==0 and ie['helper_sha256']==h.sha256(run/'priority_terravore_rear97_native_inventory_v4.py')=='e6e8ca9f31893549b6990f5ae2db24df49b212da6fdf864b91b585c86a6d4b20',
 'original_PASS_prior_actual0_source_and_SHA':prior_ok and prior_known,
 'actual_checked_native_calendar_first_month_and_research_boundary':cal['status']=='CALENDAR_CONFIRMED' and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and days==oa-ob==1 and ordinal('2272.09.30')<=ob<oa<=ordinal('2272.10.02') and 0<=mt<=1 and 0<=rt<=1,
 'original_SAV_SHA_pair':all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav'))==x['save_sha256'] for st,name,x in [(b,before,eb),(a,after,ea)]),
 'production41_same_tree_Chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered_original2814_error_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'no_free_new_ship_and_all_retained_original_designs':original_designs_ok(),
 'mother20_military_untouched_except1916_native_repair':len(alive(b)-rear)==20 and all(b['owned_ships_raw'][str(i)]==a['owned_ships_raw'].get(str(i)) for i in alive(b)-rear-{1916}) and omit(b['owned_ships_raw']['1916'],{'armor_hitpoints'})==omit(a['owned_ships_raw']['1916'],{'armor_hitpoints'}) and 0<=q.scalars(a['owned_ships_raw']['1916'])['armor_hitpoints']-q.scalars(b['owned_ships_raw']['1916'])['armor_hitpoints']<=days*0.625+0.001,
 'survivors_native_HP_armor_shield_within_original_design_caps':all(health_valid(v) for i,v in a['owned_ships_raw'].items() if int(i) in am or i in {'50333369','67109591'}) and all(health_valid(v) for v in ea['enemy825_ships_raw'].values() if v),
 'colonizer_original_fleet_species_and_design_held':col.get('fleet')==33555278 and q.ids(q.block(cf,'ships'))==[50333369] and q.scalars(q.block(colraw,'colonization_data'))=={'species':73},
 'rear_base153_owner_chain_held':eb['rear153_raw']==ea['rear153_raw'] and station.get('fleet')==804 and 804 in a['owned_fleets'] and q.ids(q.block(a['owned_fleets_raw']['804'],'ships'))==[67109591],
 'EEP_variables_core_and_mother_timer_held':bc['variables']==ac['variables'] and mother_flag_ok() and all(ac['variables'][k]==v for k,v in {'eep_c':49,'eep_d':14,'eep_worlds':3,'eep_psi':1,'eep_stage':1,'eep_fleet_stage':0}.items()),
 'source_only_original_two_timer_decrements':source_timers_ok(),
 'mother_districts_zones_buildings_deposits_design_registry_held':all(b['raw_roots'][k]==a['raw_roots'][k] for k in ['districts','zones','buildings']) and ba['planets']['7']['deposits']==aa['planets']['7']['deposits'] and all(q.block(b['raw_roots']['deposit'],str(i))==q.block(a['raw_roots']['deposit'],str(i)) for i in aa['planets']['7']['deposits']) and own_design_registry_ok(),
 'true_resource_budget_bridge_caps_no_repeat_rewards':all(abs(delta.get(k,D(0))-net[k]*mt)<=D('0.00005') for k in keys if k not in {'trade','influence'}) and all(delta[k]==0 for k in stocks-set(keys)-set(q.RESEARCH_RESOURCES)) and all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap for k,cap in [('trade',50000),('influence',1000)]) and ac['effective_stockpile']['menace']==885,
 'jobs_original_structure_and_species73_only':jobs_ok() and bc['owned_colonies']==ac['owned_colonies']==[0] and a['species_population_by_colony']=={'0:73':ca['actual_pop_sum']} and ba['species']==aa['species'],
 'original_paid_queue3_order_1_33_work_daily_other11_empty':len(owned_queues(a))==12 and owned_queues(b)==owned_queues(a) and all(not q.ids(q.block(v,'items')) for k,v in owned_queues(a).items() if k!='3') and q.ids(q.block(owned_queues(a)['3'],'items'))==[100663340] and omit(item(b),{'progress'})==omit(item(a),{'progress'}) and D(str(q.scalars(item(a))['progress']))==D(str(q.scalars(item(b))['progress']))+D('1.33')*days<D(360),
 'original_colonizer_MIA_type_return_no_live_combat':q.scalars(cf)['mia_type']=='mia_emergency_ftl' and q.scalars(cf)['return_date']=='2275.08.02' and q.scalars(q.block(cf,'properties'))['mia']=='yes' and not q.ids(q.block(q.block(cf,'combat'),'in_combat_with')),
 'target523_original_dead_colonizer_held':b['planet_raw']['523']==a['planet_raw']['523'] and b['original_ship16779140_entry']==a['original_ship16779140_entry'] and b['original_fleet16778062_entry']==a['original_fleet16778062_entry'],
 'armies_government_traditions_AP_true_crisis_held':q.ids(q.block(bcr,'owned_armies'))==q.ids(q.block(acr,'owned_armies')) and len(q.ids(q.block(acr,'owned_armies')))==12 and all(bc[k]==ac[k] for k in ['government','traditions','ascension_perks']) and q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression'),
 'known_country_modules_and_project_timers':timers_ok() and modules_ok() and projects_ok(),
 'naval_native_cache140_or_refreshed135':q.scalars(acr)['fleet_size'] in {140,135} and q.scalars(acr)['used_naval_capacity'] in {140,135} and q.scalars(acr)['military_power']>=0,
 'country_core_fields_and_fleet_manager_held':omit(bcr,{'last_date_at_war','budget','ai','relations_manager','events','flags','sensor_range_fleets','modules','fleets_manager','fleet_size','used_naval_capacity','military_power'})==omit(acr,{'last_date_at_war','budget','ai','relations_manager','events','flags','sensor_range_fleets','modules','fleets_manager','fleet_size','used_naval_capacity','military_power'}) and omit(q.block(bcr,'fleets_manager'),{'owned_fleets'})==omit(q.block(acr,'fleets_manager'),{'owned_fleets'}),
 'budget_month_roll_or_same_budget':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'] if mt else bc['budget_categories']==ac['budget_categories'],
 'positive_actual_core_monthly_economy':all(net[k]>0 for k in ['energy','minerals','alloys','unity']),
 'research_true_P_S_bank_native_tick_and_Eng_bank0':all(abs(bank_delta[k]-science[k]*D('1.33')*rt)<=D('0.00005') for k in ['physics_research','society_research']) and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0,
 'engineering_only_original_mass_drivers3_native_progress':omit(bt,{'stored_techpoints','engineering_queue'})==omit(at,{'stored_techpoints','engineering_queue'}) and {k:v for k,v in beng.items() if k!='progress'}=={k:v for k,v in aeng.items() if k!='progress'} and beng['technology']==aeng['technology']=='tech_mass_drivers_3' and abs(D(str(aeng['progress']))-D(str(beng['progress']))-science['engineering_research']*D('1.33')*rt)<=D('0.00005'),
 'population_native_month_classification_no_repeat_return':population_ok(),
 'housing_native_growth_cache_bounded_and_source_colony_held':ca['total_housing']==14100 and ca['free_housing']==14100-ca['housing_usage'] and 0<=ca['actual_pop_sum']-ca['housing_usage']<=max(new_growth,cb['actual_pop_sum']-cb['housing_usage']) and ca['housing_usage']>=cb['housing_usage'] and ca['actual_pop_sum']==ca['employable_pops']==ca['num_sapient_pops'] and ca['free_amenities']>0 and ca['crime']==0 and b['colony_raw']['37']==a['colony_raw']['37'],
}
passed=all(v is True for v in checks.values());ready=passed and not boundaries and len(alive(a))==27
status='PASS_NATIVE_TERRAVORE_MIA_MOTHER_FIRST_MONTH_COMPONENT' if ready else ('OBSERVED_NATIVE_TERRAVORE_REAR97_BOUNDARY' if passed else 'FAIL')
proof={'status':status,'checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'days':days,'boundaries':boundaries,'new_lost_owned_military':sorted(new_lost),'enemy_removed':sorted(enemy_lost),'enemy_killed':sorted(enemy_killed),'new_country0_messages_raw':new_messages,'alive_military_ship_ids':sorted(alive(a)),'registered_military_ship_ids':sorted(am),'known_dead_cleaned':sorted(known_dead-am),'rear_station_health':{k:station.get(k,0) for k in ['hitpoints','armor_hitpoints','shield_hitpoints']},'new_colonizer_health':colhealth,'new_colonizer_position':cfpos,'new_colonizer_order_raw':new_order,'rear_battle_calendar_ready':False,'native_research_day_ready':ready and aa['date']=='2272.10.01','maximum_days_to_research_boundary':1 if ready and aa['date']=='2272.10.01' else 0,'actual_net':{k:str(v) for k,v in net.items()},'actual_stock_delta':{k:str(v) for k,v in delta.items()},'actual_science_income':{k:str(v) for k,v in science.items()},'actual_research_bank_delta':{k:str(v) for k,v in bank_delta.items()},'actual_population':ca['actual_pop_sum'],'native_new_growth':new_growth,'native_growth_record':growth,'housing_cache_lag':ca['actual_pop_sum']-ca['housing_usage'],'actual_colonizer_work':q.scalars(item(a))['progress'],'maximum_days_to_battle_observation':(3 if station.get('hitpoints',0)>=12000 and station.get('armor_hitpoints',0)>=2000 and colhealth['shield_hitpoints']==320 else 1) if ready else 0,'normal_colonization_route_ready':False,'scope':'Stable Mod core under bounded native combat; OBSERVED boundary explicitly not a calendar PASS or full acceptance.'}
out=run/(after+'-mia-build-first-month-v2-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':status,'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'boundaries':boundaries,'base':proof['rear_station_health'],'colonizer_position':cfpos}),flush=True);assert passed
