"""Documented bounded native construction/economy checks before September completion."""
import json, logging, re, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path[:0] = ['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r, audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run/n).read_text('utf-8'))
omit = lambda t,ks: [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
objects = lambda t: {k:v for k,v,o in q.fields(t) if o}

def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:
        fields=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'), fields, {k:v for k,v,o in fields if o}
def ordinal(s):
    y,m,d=map(int,s.split('.'));return y*360+(m-1)*30+d-1
def owned(c):
    return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets'))))
def fleetships(fleets,ids,military=False):
    return {i for fid in ids if not military or q.scalars(fleets[str(fid)]).get('ship_class')=='shipclass_military' for i in q.ids(q.block(fleets[str(fid)],'ships'))}
def construction(t):
    c=t['construction']
    return objects(q.block(q.block(c,'queue_mgr'),'queues')),objects(q.block(q.block(c,'item_mgr'),'items'))
def research_queue(t,key):
    raw=q.block(t,key);ts=list(q.tokens(raw))
    if not ts:return {}
    assert ts[0][0]=='{' and ts[-1][0]=='}'
    return q.scalars(raw[ts[0][2]:ts[-1][1]])
b,bf,br=read(before);a,af,ar=read(after)
bc,ac=b['countries']['0'],a['countries']['0']
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bfl,afl=[objects(t['fleet']) for t in [br,ar]]
bsh,ash=[objects(t['ships']) for t in [br,ar]]
bo,ao=owned(bcr),owned(acr)
bm,am=fleetships(bfl,bo,True),fleetships(afl,ao,True)
ob,oa=ordinal(b['date']),ordinal(a['date']);days=oa-ob
validate_native_interval(b['date'],a['date'],days)
mt=sum(i%30==0 for i in range(ob+1,oa+1))
rt=sum(i%30==1 for i in range(ob+1,oa+1))
first=before=='terravore-third-settlement-native'
original='terravore-third-post-settlement-month'
cal=load(after+'-calendar-receipt.json') if not first else None
ce=load(after+'-calendar-execution.json') if not first else None
pre=load(cal['prior_proof_file']) if cal else load('terravore-third-settlement-native-third-settlement-proof.json')
pe=load(cal['prior_execution_stage']+'-execution.json') if cal else load('terravore-third-settlement-native-observer-fullpath-execution.json')
observation=load(after+'-post-settlement-observation.json') if first else None
oe=load(after+'-observation-execution.json') if first else None

def chain_ok():
    if first:
        return (after==original+'-recovered' and days==29 and pre['status']=='PASS_NATIVE_TERRAVORE_THIRD_SETTLEMENT_COMPONENT' and len(pre['checks'])==51
            and pe['helper_sha256']=='97bcc09b4f2474b1c75d7863988d03eea67718ef0e9c193b8d46b0ecf462587f'
            and observation['status']=='OBSERVED_NATIVE_TERRAVORE_POST_SETTLEMENT_RECOVERED_MONTH' and len(observation['checks'])==9 and all(v is True for v in observation['checks'].values())
            and oe['returncode']==0 and oe['helper_sha256']==h.sha256(run/'priority_terravore_post_settlement_observation.py')=='f2b44c3c5860cc4bf4cc4ddd5fa638bf3433bf10cc8342ae03275afffeb5204a'
            and h.sha256(run/(after+'-post-settlement-observation.json'))=='cd8fc8a7257ffcc967ac2830222a8683a6a2138193aa5faac8a25039bbbbd61f'
            and observation['before_sha256']==b['save_sha256'] and observation['after_sha256']==a['save_sha256']=='83a64119a810bc39fb650a3ee0a50128db060a503efd0bbdb047856a2f574240')
    return (pre['status']=='PASS_NATIVE_TERRAVORE_POST_SETTLEMENT_BUILD_COMPONENT' and pre['post_settlement_build_calendar_ready'] is True
        and pe['helper_sha256']==h.sha256(Path(__file__)) and cal['status']=='CALENDAR_CONFIRMED' and cal['days']==days and cal['start_date']==b['date'] and cal['date']==a['date']
        and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc')

cb,ca=b['colonies']['0'],a['colonies']['0']
mb,ma=b['planets']['7'],a['planets']['7']
sp,sa=b['planets']['1085'],a['planets']['1085']
growth_raw=q.block(q.block(ar['colony'],'0'),'last_month_growth_data')
growth=q.scalars(q.block(growth_raw,'growth_and_size'))
growth_details=[(k,q.unquote(v),o) for k,v,o in q.fields(q.block(growth_raw,'current_month_growth_details'))]
new_growth=ca['actual_pop_sum']-cb['actual_pop_sum']
def population_ok():
    if first:
        return (new_growth==7 and cb['actual_pop_sum']==11123 and ca['actual_pop_sum']==11130
            and growth=={'month_start_size':10834,'growth':296}
            and growth_details==[('key','GROWTH_CAT_GROWTH',False),('value',7,False),('key','GROWTH_CAT_OTHER',False),('value',289,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)]
            and growth['month_start_size']+growth['growth']==ca['actual_pop_sum'])
    if not mt:return new_growth==0
    return (growth=={'month_start_size':cb['actual_pop_sum'],'growth':new_growth} and new_growth==7
        and growth_details==[('key','GROWTH_CAT_GROWTH',False),('value',7,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)])
keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in keys}
stocks=set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in stocks}
residual={k:delta.get(k,D(0))-net[k]*mt for k in keys}
bt,at=bc['tech_status'],ac['tech_status']
beng,aeng=[research_queue(t,'engineering_queue') for t in [bt,at]]
science={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bank_delta={k:D(str(ac['research_stockpile'].get(k,0)))-D(str(bc['research_stockpile'].get(k,0))) for k in q.RESEARCH_RESOURCES}
bqs,bi=construction(br);aqs,ai=construction(ar)
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
pending=lambda fs:[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
messages=lambda fs:[v for k,v,o in fs if k=='message' and o and q.scalars(v).get('receiver')==0]
foundation=load('terravore-rear-clearing-first-born-calibration-war1-battle-v65-proof.json')
expected_vars=dict(bc['variables'],eep_crisis=1) if first else bc['variables']
expected_flags={k:v for k,v in bc['flags'].items() if k!='eep_notice_pending'} if first else bc['flags']
expected_mvars=dict(mb['variables'],eep_actual_pop=11123,eep_free_districts=3) if first else mb['variables']
def military_ok():
    for i in bm:
        old,new=bsh[str(i)],ash[str(i)];os,ns=q.scalars(old),q.scalars(new)
        if i!=1916:
            if old!=new:return False
        elif not (omit(old,{'hitpoints','armor_hitpoints'})==omit(new,{'hitpoints','armor_hitpoints'})
            and all(0<D(str(os[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')])):return False
    return True
def fleets_ok():
    return all(bfl[str(i)]==afl[str(i)] if i!=83886903 else omit(bfl[str(i)],{'diplomacy_weight','hit_points','military_power'})==omit(afl[str(i)],{'diplomacy_weight','hit_points','military_power'}) for i in bo)
blocker_file=run/'native-blocker-clear-01_blocker_deposits.txt'
blockers=blocker_file.read_text('utf-8-sig')
planet_deps=[a['deposits'][str(i)]['type'] for i in ma['deposits']]
blocked=sum(q.scalars(q.block(q.block(blockers,t),'planet_modifier')).get('planet_max_districts_add',0) for t in planet_deps)

checks={
 'original_interval_chain_or_precise_failed_OCR_recovery':chain_ok(),
 'prior_all_PASS_actual0_original_SHA_and_source':all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(Path(pe['command'][1])) and pre['after_sha256']==b['save_sha256'],
 'bounded_1_to30_days_zero_or_one_month_and_research_tick':1<=days<=30 and 0<=mt<=1 and 0<=rt<=1 and ordinal('2272.07.02')<=ob<oa<=ordinal('2272.09.10'),
 'original_SAV_SHA_pair':all(x['save_sha256']==h.sha256(run/(st+'.sav')) for st,x in [(before,b),(after,a)]),
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'true_resources_only_native_month_net_no_repeat_rewards':all(abs(residual[k])<=D('0.00005') for k in keys if k not in ['trade','influence']) and all(delta[k]==0 for k in stocks-set(keys)-set(q.RESEARCH_RESOURCES)) and all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap for k,cap in [('trade',50000),('influence',1000)]),
 'native_budget_month_roll_or_held_between_months':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'] if mt else bc['budget_categories']==ac['budget_categories'],
 'positive_native_energy_minerals_alloys_unity_net':all(net[k]>0 for k in ['energy','minerals','alloys','unity']),
 'research_true_P_S_banks_only_native_tick_Eng_bank0':all(abs(bank_delta[k]-science[k]*D('1.33')*rt)<=D('0.00005') for k in ['physics_research','society_research']) and bank_delta['engineering_research']==0,
 'only_original_mass_drivers3_progress_no_new_completed_tech':omit(bt,{'stored_techpoints','engineering_queue'})==omit(at,{'stored_techpoints','engineering_queue'}) and {k:v for k,v in beng.items() if k!='progress'}=={k:v for k,v in aeng.items() if k!='progress'} and beng['technology']==aeng['technology']=='tech_mass_drivers_3' and abs(D(str(aeng['progress']))-D(str(beng['progress']))-science['engineering_research']*D('1.33')*rt)<=D('0.00005'),
 'population_only_growth7_with_historic_migration289_once':population_ok(),
 'one_owned_colony_only_species73_source_empty':bc['owned_colonies']==ac['owned_colonies']==[0] and b['species']==a['species'] and sum(g['size'] for g in a['pop_groups'].values() if g['planet']==0 and g['key']['species']==73)==ca['actual_pop_sum'] and not any(g['planet']==37 and g['size']>0 for g in a['pop_groups'].values()),
 'housing_return_cache_refreshed_only_current_month_growth_lag':ca['total_housing']==14100 and ca['free_housing']==14100-ca['housing_usage'] and 0<=ca['actual_pop_sum']-ca['housing_usage']<=7 and ca['housing_usage']>=cb['housing_usage'] and (not mt or ca['housing_usage']==cb['actual_pop_sum']) and ca['actual_pop_sum']==ca['employable_pops']==ca['num_sapient_pops'] and ca['free_amenities']>0 and ca['crime']==0,
 'aligned_month_end_or_final_prebuild_housing_fully_refreshed':not (a['date'].endswith('.30') or a['date']=='2272.09.10') or ca['housing_usage']==ca['actual_pop_sum'],
 'report_only_expected_snapshot_C49_D14_worlds3_held':ac['variables']==expected_vars and all(ac['variables'][k]==v for k,v in {'eep_c':49,'eep_d':14,'eep_worlds':3,'eep_psi':1,'eep_g':0,'eep_made':0,'eep_delta':0,'eep_stage':1,'eep_fleet_stage':0}.items()),
 'monthly_pending_notice_cleared_no_new_Queen_flags':ac['flags']==expected_flags and 'eep_notice_pending' not in ac['flags'],
 'unique_owned_core18_capacity14_original_deposit_and_modifier':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and ma['owner']==ma['controller']==ma['colony']==0 and ma['planet_size']==18 and ma['modifiers']==mb['modifiers'] and ma['deposits']==mb['deposits'] and ma['flags']==mb['flags'] and ma['variables']==expected_mvars and a['deposits']['1573']==b['deposits']['1573'],
 'report_free3_independent_two_native_capacity_blockers':blocked==-2 and all(planet_deps.count(t)==1 and q.scalars(q.block(q.block(blockers,t),'planet_modifier'))['planet_max_districts_add']==-1 for t in ['d_failing_infrastructure','d_ruined_district']) and ma['variables']['eep_free_districts']==18+14-27+blocked==3,
 'paid_districts7_15_5_and_all_mother_zones_buildings_held':all(b['districts'][str(i)]==a['districts'][str(i)] for i in [1,2,3]) and all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','104']) and all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for zid in ['0','2','104'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))),
 'mother_all_job_caps_held_technician1400':{i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in b['pop_jobs'].items() if j['planet']==0}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in a['pop_jobs'].items() if j['planet']==0} and len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['max_workforce']==j['workforce_limit']==1400])==1,
 'source_shattered_unowned_cleaned_no_new_progress':sa['planet_class']=='pc_shattered' and 'owner' not in sa and 'controller' not in sa and sa['deposits']==[] and sa['modifiers']=='' and sa['variables']==sp['variables'] and sa['bombardment_damage']==sp['bombardment_damage'],
 'source_done_flags_held_only_two_cooldowns_minus_days':{k:v for k,v in sa['flags'].items() if k not in ['recently_eaten_planet','superior_colonies_can_be_boosted']}=={k:v for k,v in sp['flags'].items() if k not in ['recently_eaten_planet','superior_colonies_can_be_boosted']} and all(sp['flags'][k]['flag_date']==sa['flags'][k]['flag_date'] and sp['flags'][k]['flag_days']-sa['flags'][k]['flag_days']==days and sa['flags'][k]['flag_days']>0 for k in ['recently_eaten_planet','superior_colonies_can_be_boosted']),
 'dead_situation_removed_no_live_EEP_or_native_duplicate':not any(v.get('type') in ['situation_eep_devouring','situation_terravore_consume_planet'] for v in a['situations'].values()),
 'same_nemesis1_objectives_and_true_Menace885':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and ac['effective_stockpile']['menace']==885,
 'only_original_inactive264_pending_no_new_country_messages':pending(bf)==pending(af) and len(pending(af))==1 and q.scalars(pending(af)[0])=={'id':264,'event':'grand_archive.2800','date':'2273.12.20','country':0} and all(v in messages(bf) for v in messages(af)),
 'all_owned_ships_fleets_and_original28_military_naval140':bo==ao and fleetships(bfl,bo)==fleetships(afl,ao) and bm==am==set(foundation['actual_alive_military_ship_ids']) and len(am)==28 and q.scalars(acr)['fleet_size']==140,
 'all_military_raw_held_except_original1916_monotonic_repair':military_ok(),
 'all_fleets_raw_held_only1916_fleet_health_power_cache':fleets_ok(),
 'science_only_orientation_and_bounded_native_shield_regen':omit(bsh['1'],{'rotation','forward_x','forward_y','shield_hitpoints'})==omit(ash['1'],{'rotation','forward_x','forward_y','shield_hitpoints'}) and D(str(q.scalars(ash['1'])['shield_hitpoints']))==min(D(320),D(str(q.scalars(bsh['1'])['shield_hitpoints']))+8*days),
 'all_other_civilian_stations_raw_held_no_new_ship':all(bsh[str(i)]==ash[str(i)] for i in fleetships(bfl,bo)-bm-{1}),
 'no_owned_combat_or_war1_new_battle':q.block(q.block(br['war'],'1'),'battles')==q.block(q.block(ar['war'],'1'),'battles') and all(not q.ids(q.block(q.block(afl[str(i)],'combat'),'in_combat_with')) for i in ao),
 'original_colonizer_death_and_target523_held':[(v,o) for k,v,o in q.fields(br['ships']) if k=='16779140']==[(v,o) for k,v,o in q.fields(ar['ships']) if k=='16779140']==[('none',False)] and [(v,o) for k,v,o in q.fields(ar['fleet']) if k=='16778062']==[('none',False)] and q.block(q.block(br['planets'],'planet'),'523')==q.block(q.block(ar['planets'],'planet'),'523'),
 'same12_owned_defense_armies_no_free_transports':q.ids(q.block(bcr,'owned_armies'))==q.ids(q.block(acr,'owned_armies')) and len(q.ids(q.block(acr,'owned_armies')))==12,
 'original_physics_order_exact_absolute_work_below360':q.ids(q.block(aqs['0'],'items'))==[1258291211] and omit(bi['1258291211'],{'progress'})==omit(ai['1258291211'],{'progress'}) and all(D(str(q.scalars(items['1258291211'])['progress']))==D('1.4')*(ord_value-ordinal('2271.12.23'))<360 for items,ord_value in [(bi,ob),(ai,oa)]),
 'original_rear_colonizer_order_absolute_work_below360':q.ids(q.block(aqs['2287'],'items'))==[83886124] and omit(bi['83886124'],{'progress'})==omit(ai['83886124'],{'progress'}) and all(D(str(q.scalars(items['83886124'])['progress']))==D('1.33')*(ord_value-ordinal('2271.12.12'))<360 for items,ord_value in [(bi,ob),(ai,oa)]),
 'all_owned_queue_structures_held_no_new_orders':{k:v for k,v in bqs.items() if q.scalars(v).get('owner')==0}=={k:v for k,v in aqs.items() if q.scalars(v).get('owner')==0},
 'five_country_native_timers_exact_days_only_notice_removed':timers_ok(),
 'only_native_paragon999_timer_and_economy_mirror_modules':modules_ok(),
 'only_known_debris_timers_and_removed_dead_situation':projects_ok(),
 'government_traditions_AP_and_manual_history_held':all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions']) and br['open_player_event_selection_history']==ar['open_player_event_selection_history'],
}
passed=all(v is True for v in checks.values())
remaining=ordinal('2272.09.10')-oa
p={'status':'PASS_NATIVE_TERRAVORE_POST_SETTLEMENT_BUILD_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'days':days,'actual_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'research_bank_delta':{k:str(v) for k,v in bank_delta.items()},'native_new_growth':new_growth,'native_month_record':growth,'housing_cache_lag':ca['actual_pop_sum']-ca['housing_usage'],'housing_cache_refresh_pending':ca['actual_pop_sum']!=ca['housing_usage'],'returned_population_cache_refreshed':True,'actual_core_population':ca['actual_pop_sum'],'actual_physics_zone_work':q.scalars(ai['1258291211'])['progress'],'actual_colonizer_work':q.scalars(ai['83886124'])['progress'],'actual_alive_military_ship_ids':sorted(am),'post_settlement_build_calendar_ready':passed and remaining>0,'maximum_days_to_build_boundary':remaining,'scope':'Bounded native post-settlement economy/science/population and paid unfinished construction. Original OCR failure retained. No original colonizer recovery, new colonizer birth, physics completion, mineral fleet or full route acceptance.'}
out=run/(after+'-post-settlement-build-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':a['date'],'net':p['actual_net'],'population':p['actual_core_population'],'housing_lag':p['housing_cache_lag'],'physics_work':p['actual_physics_zone_work'],'colonizer_work':p['actual_colonizer_work']}),flush=True)
assert passed,'Original failure retained; no calendar replay'
