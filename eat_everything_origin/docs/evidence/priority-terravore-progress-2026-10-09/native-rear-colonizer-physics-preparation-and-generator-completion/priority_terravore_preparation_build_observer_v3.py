"""Scoped native construction observation after documented normal preparation."""
import json, logging, re, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r, audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
def load(name):return json.loads((run/name).read_text('utf-8'))
def read(stage):
 with zipfile.ZipFile(run/(stage+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(stage+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def objects(t):return {k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def owned(c):return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets'))))
def ordinal(s):
 y,m,d=map(int,s.split('.'));return y*360+(m-1)*30+d-1
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
receipt=load(after+'-calendar-receipt.json');days=receipt['days'];validate_native_interval(b['date'],a['date'],days)
pre=load(receipt['prior_proof_file']);ex=load(receipt['prior_execution_stage']+'-execution.json')
calendar_ex=load(after+'-calendar-execution.json')
foundation=load('terravore-rear-clearing-first-born-calibration-war1-battle-v65-proof.json')
foundation_ex=load('terravore-rear-clearing-first-born-calibration-battle-v65-execution.json')
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bfl,afl=[objects(t['fleet']) for t in [br,ar]];bsh,ash=[objects(t['ships']) for t in [br,ar]]
bo,ao=owned(bcr),owned(acr)
def fleetships(fleets,ids,military_only=False):
 return {i for fid in ids if not military_only or q.scalars(fleets[str(fid)]).get('ship_class')=='shipclass_military' for i in q.ids(q.block(fleets[str(fid)],'ships'))}
bm,am=fleetships(bfl,bo,True),fleetships(afl,ao,True)
def health_held_or_known_repair(i):
 old,new=bsh[str(i)],ash[str(i)];bs,ns=q.scalars(old),q.scalars(new)
 return (q.block(old,'ship_design_implementation')==q.block(new,'ship_design_implementation')
  and all(bs.get(k)==ns.get(k) for k in ['fleet','construction_date','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints','last_combat_activity','last_damage','experience','upgrade_progress'])
  and all(0<D(str(bs[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('hitpoints','max_hitpoints')])
  and all(0<=D(str(bs[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
  and bs.get('last_combat_activity','0.01.01')<='2271.12.01' and ns.get('killed')!='yes')
def construction(top):
 c=top['construction'];return objects(q.block(q.block(c,'queue_mgr'),'queues')),objects(q.block(q.block(c,'item_mgr'),'items'))
bqs,bi=construction(br);aqs,ai=construction(ar)
elapsed_b=ordinal(b['date'])-ordinal('2271.12.12');elapsed_a=ordinal(a['date'])-ordinal('2271.12.12')
gen_b=D(str(q.scalars(bi['788529161'])['progress']))
gen_a=D(240) if '788529161' not in ai else D(str(q.scalars(ai['788529161'])['progress']))
col_b,col_a=[D(str(q.scalars(items['83886124'])['progress'])) for items in [bi,ai]]
first=after=='terravore-preparation-first-work'
if first:
 rate=col_a;calibration_ok=before=='terravore-physics-zone-paid' and days==1 and elapsed_b==0 and elapsed_a==1 and col_b==0 and rate>0 and int(D(360)/rate) in [269,270,271]
else:
 cal=load('terravore-preparation-first-work-preparation-build-v2-proof.json');cex=load('terravore-preparation-first-work-build-observer-v2-execution.json')
 rate=D(cal['measured_colonizer_work_per_day']);calibration_ok=cal['status'].startswith('PASS_') and all(v is True for v in cal['checks'].values()) and cex['returncode']==0 and cex['helper_sha256']==h.sha256(run/'priority_terravore_preparation_build_observer_v2.py')=='7fd8e8d6db2f192df9b1ee70e9c205b42a3b914e7e3a799ac9b03e8f4e6fdc55' and cal['after_sha256']==h.sha256(run/'terravore-preparation-first-work.sav')
def original_order_held(i):return omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'})
pending=lambda fs:[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
pending_b,pending_a=pending(bf),pending(af)
contact_b,contact_a=[q.block(q.block(t['first_contacts'],'contacts'),'16777275') for t in [br,ar]]
source_b,source_a=b['planets']['1085'],a['planets']['1085'];mother_b,mother_a=b['planets']['7'],a['planets']['7']
source_flags=lambda v:{k:x for k,x in v['flags'].items() if k not in {'recently_eaten_planet','superior_colonies_can_be_boosted'}}
native_reports=lambda fs:[v for k,v,o in fs if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0]
legacy=load('terravore-preparation-first-work-preparation-build-proof.json')
legacy_ex=load('terravore-preparation-first-work-build-observer-execution.json')
def project_timers_held():
 old,new=[q.block(c,'events') for c in [bcr,acr]]
 bp,ap=[{q.scalars(v)['id']:v for k,v,o in q.fields(raw) if k=='special_project' and o} for raw in [old,new]]
 if bp.keys()!=ap.keys() or not {4,5}<=bp.keys() or omit(old,{'special_project'})!=omit(new,{'special_project'}):return False
 for i in bp:
  if i not in {4,5}:
   if bp[i]!=ap[i]:return False
  else:
   bs,ns=q.scalars(bp[i]),q.scalars(ap[i])
   if not (omit(bp[i],{'days_left'})==omit(ap[i],{'days_left'}) and bs['debris']==ns['debris']=={4:16777219,5:369098752}[i] and bs['days_left']-ns['days_left']==days and ns['days_left']>0):return False
 return True
checks={
 'generator_technician1200_to1400_and_housing600_actual':len([j for j in b['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['workforce']==j['max_workforce']==j['workforce_limit']==1200])==1 and len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['workforce']==j['max_workforce']==j['workforce_limit']==1400])==1 and b['colonies']['0']['total_housing']==13800 and a['colonies']['0']['total_housing']==14400 and a['colonies']['0']['free_housing']==a['colonies']['0']['total_housing']-a['colonies']['0']['housing_usage'] and a['colonies']['0']['housing_usage']==a['colonies']['0']['actual_pop_sum'],
 'original24_exact_two_timer_assumption_FAIL_actual1_bound':len(legacy['checks'])==24 and {k for k,v in legacy['checks'].items() if v is not True}=={'native_nemesis1_progression_events_government_AP_traditions_held','third_Q12_T29_seed103_need_minus3_no_early_payout'} and legacy_ex['returncode']==1 and legacy_ex['helper_sha256']==h.sha256(run/'priority_terravore_preparation_build_observer.py')=='c3196b23facc3785d42bd61073c03e710046e8ee204668ce3713f472361384c5' and legacy['after_sha256']==h.sha256(run/'terravore-preparation-first-work.sav')=='d92e3b4a4368e90ea986259f7bef60d5414af921b5f73b5dbf2966b418e2d906',
 'two_known_native_source_flags_exact_daily_countdown':all(source_b['flags'][k]['flag_date']==source_a['flags'][k]['flag_date'] and source_b['flags'][k]['flag_days']-source_a['flags'][k]['flag_days']==days and source_a['flags'][k]['flag_days']>0 for k in ['recently_eaten_planet','superior_colonies_can_be_boosted']),
 'native_source_devastation_nonnegative_recovery_no_annual_tick':0<=source_a['bombardment_damage']<=source_b['bombardment_damage'],
 'prior_PASS_actual0_original_SHA_and_source':pre['status'].startswith('PASS_') and bool(pre['checks']) and all(v is True for v in pre['checks'].values()) and ex['returncode']==0 and pre['after_sha256']==b['save_sha256'] and ex['helper_sha256']==h.sha256(run/Path(ex['command'][1]).name),
 'frozen106_foundation_actual0_same_original_tree':len(foundation['checks'])==106 and all(v is True for v in foundation['checks'].values()) and foundation_ex['returncode']==0 and foundation_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v65.py')=='e63467e1b2c8727301715616037ff8e9b32237673c357eb7b1f4378d65c52cf9' and foundation['after_sha256']==h.sha256(run/'terravore-rear-clearing-first-born-calibration.sav')=='acfad1a21cad0c3936bf4378f18bad9f1de0ef6a8e79cee1e7009d2b082385c3',
 'unique_native_calendar_actual0_exact_dates_source':calendar_ex['returncode']==0 and calendar_ex['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and receipt['date']==a['date'] and receipt['start_date']==b['date'] and receipt['status']=='CALENDAR_CONFIRMED',
 'original_two_SAV_SHA_and_bounded_precompletion_dates':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')) and 1<=days<=30 and elapsed_b==10 and elapsed_a==11 and days==1 and b['date']=='2271.12.22' and a['date']=='2271.12.23',
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'only_original_inactive264_pending_contact_history_held':pending_b==pending_a and len(pending_a)==1 and q.scalars(pending_a[0])=={'id':264,'event':'grand_archive.2800','date':'2273.12.20','country':0} and contact_b==contact_a and not q.block(contact_a,'event') and br['open_player_event_selection_history']==ar['open_player_event_selection_history'],
 'same_all_owned_fleets_and_ships_no_granted_birth_or_loss':bo==ao and fleetships(bfl,bo)==fleetships(afl,ao) and bm==am==set(foundation['actual_alive_military_ship_ids']) and len(am)==28 and q.scalars(acr)['fleet_size']==140,
 'all28_military_design_dates_max_held_only_known_native_repair':all(health_held_or_known_repair(i) for i in am),
 'owned_fleets_no_new_combat_or_war1_battle':not any(re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(afl[str(i)],'combat'),'in_combat_with')) for i in ao) and q.block(q.block(br['war'],'1'),'battles')==q.block(q.block(ar['war'],'1'),'battles') and native_reports(bf)==native_reports(af),
 'original_colonizer_ship_and_idle_fleet_still_retained':bsh['16779140']==ash['16779140'] and bfl['16778062']==afl['16778062'],
 'target523_uncolonized_same_raw_no_early_transfer':q.block(q.block(br['planets'],'planet'),'523')==q.block(q.block(ar['planets'],'planet'),'523'),
 'EEP_variables_flags_species_targets_unchanged':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'].get(k)==v for k,v in {'eep_c':37,'eep_d':11,'eep_g':0,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()) and b['species']==a['species'] and b['event_targets']==a['event_targets'],
 'native_nemesis1_progression_events_government_AP_traditions_held':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and project_timers_held() and all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions','owned_colonies']),
 'real_stock_banks_technology_held_no_day_tick_or_repeated_payment':bc['effective_stockpile']==ac['effective_stockpile'] and bc['tech_status']==ac['tech_status'] and ac['effective_stockpile']['menace']==135,
 'unique_owned_mother_capacity11_and_no_new_bombardment':mother_a['owner']==mother_a['controller']==0 and mother_a['colony']==0 and mother_a['variables']['eep_capacity_value']==11 and mother_b['modifiers']==mother_a['modifiers'] and mother_a['bombardment_damage']==0 and sum('eep_core' in p['flags'] for p in a['planets'].values())==1,
 'only_generator6_to7_other_districts_zones_and_all_compatible_buildings_held':all(b['districts'][i]==a['districts'][i] for i in ['1','3']) and {k:v for k,v in b['districts']['2'].items() if k!='level'}=={k:v for k,v in a['districts']['2'].items() if k!='level'} and b['districts']['2']['level']==6 and a['districts']['2']['level']==7 and all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','104']) and all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for zid in ['0','2','104'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))),
 'all_other_mother_job_types_and_caps_held_at_generator_complete':{i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in b['pop_jobs'].items() if j['planet']==0 and j['type']!='technician_drone'}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in a['pop_jobs'].items() if j['planet']==0 and j['type']!='technician_drone'},
 'third_Q12_T29_seed103_need_minus3_no_early_payout':source_b['variables']==source_a['variables']=={'eep_q':12,'eep_old_damage':0,'eep_months':29,'eep_seed_existing':103,'eep_seed_need':-3} and source_flags(source_b)==source_flags(source_a) and source_a['owner']==0 and source_a['colony']==37 and source_b['deposits']==source_a['deposits'] and source_b['modifiers']==source_a['modifiers'],
 'third22_of29_unique_mod_situation_no_native_duplicate':{i:v for i,v in b['situations'].items() if v.get('type')=='situation_eep_devouring'}=={i:v for i,v in a['situations'].items() if v.get('type')=='situation_eep_devouring'} and a['situations']['100663299']['progress']==22 and not any(v.get('type')=='situation_terravore_consume_planet' for v in a['situations'].values()),
 'seventh_generator_one_native_completion_none_retirement_queue_pop':q.ids(q.block(bqs['0'],'items'))==[788529161,1258291211] and q.ids(q.block(aqs['0'],'items'))==[1258291211] and gen_b==D('239.4') and gen_a==240 and [(v,o) for k,v,o in q.fields(q.block(q.block(ar['construction'],'item_mgr'),'items')) if k=='788529161']==[('none',False)] and not any(788529161 in q.ids(q.block(v,'items')) for v in aqs.values()),
 'physics_specialization_unstarted_original_paid_order_held':bi['1258291211']==ai['1258291211'] and q.scalars(ai['1258291211'])=={'queue':0,'paying_country':0,'progress':0,'progress_needed':360},
 'rear_colonizer_original_one_paid_order_and_measured_work':q.ids(q.block(bqs['2287'],'items'))==q.ids(q.block(aqs['2287'],'items'))==[83886124] and original_order_held(83886124) and calibration_ok and col_b==rate*elapsed_b and col_a==rate*elapsed_a and col_a<360,
 'all_other_player_queues_held_no_new_orders':{k:omit(v,{'items'}) for k,v in bqs.items() if q.scalars(v).get('owner')==0}=={k:omit(v,{'items'}) for k,v in aqs.items() if q.scalars(v).get('owner')==0} and {k:q.ids(q.block(v,'items')) for k,v in bqs.items() if q.scalars(v).get('owner')==0 and k!='0'}=={k:q.ids(q.block(v,'items')) for k,v in aqs.items() if q.scalars(v).get('owner')==0 and k!='0'},
}
passed=all(checks.values());p={'status':'PASS_NATIVE_TERRAVORE_PREPARATION_BUILD_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'days':days,'measured_colonizer_work_per_day':str(rate),'actual_colonizer_work':str(col_a),'actual_generator_work':str(gen_a),'actual_physics_zone_work':'0','actual_military_count':len(am),'preparation_build_calendar_ready':False,'maximum_precompletion_days':0,'actual_generator_completed':passed,'post_generator_build_calendar_ready':passed,'calendar_ready':False,'scope':'Exactly one native seventh-generator completion, technician1200 to1400/housing600, physics zone remains unstarted and colonizer14.63 pending. Frozen106 foundation retained; no six-ship completion, maintenance cycle, colony recovery, mineral fleet or whole-route acceptance.'}
out=run/(after+'-preparation-build-v3-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'colonizer_work':str(col_a),'generator_work':str(gen_a)}),flush=True)
assert passed,'Original scoped construction FAIL retained; no replay or calendar'
