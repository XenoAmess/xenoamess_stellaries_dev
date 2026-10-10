"""Bounded native combat observation with all owned military fleets; no injected state."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def obj(t):return {k:v for k,v,o in q.fields(t) if o}
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));rt={k:v for k,v,o in fs if o};return a,fs,rt,obj(rt['fleet']),obj(rt['ships'])
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
def military(rt,fs):return {i:q.ids(q.block(fs[str(i)],'ships')) for i in owned(rt) if q.scalars(fs[str(i)])['ship_class']=='shipclass_military'}
def queue(rt):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),'3')
def items(rt):return obj(q.block(q.block(rt['construction'],'item_mgr'),'items'))
def progress(c):return q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])
b,bf,br,bfl,bsh=read(before);a,af,ar,afl,ash=read(after);bc,ac=b['countries']['0'],a['countries']['0']
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'));days=receipt['days'];validate_native_interval(b['date'],a['date'],days)
pre=json.loads((run/receipt['prior_proof_file']).read_text('utf-8'));ex=json.loads((run/(receipt['prior_execution_stage']+'-execution.json')).read_text('utf-8'))
bm,am=military(br,bfl),military(ar,afl);bs=[s for ss in bm.values() for s in ss];ass=[s for ss in am.values() for s in ss];new=[i for i in ass if i not in bs];lost=[i for i in bs if i not in ass]
bids,aids=[q.ids(q.block(queue(rt),'items')) for rt in [br,ar]];bi,ai=items(br),items(ar);removed=len(bids)-len(aids)
sb,sa=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]];core=a['planets']['7'];nets={k:sum(v.get(k,0) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys','trade']}
checks={
 'bound_actual_prior_PASS_execution_zero':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_bounded_native_days_receipt_execution_zero':days==30 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'paid_orders_contiguous_completion_other_fields_held':removed>=0 and aids==bids[removed:] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and 0<=q.scalars(ai[str(i)])['progress']<60 for i in aids),
 'actual_new_ships_equal_paid_completed_orders':len(new)==removed,
 'actual_all_owned_military_ship_relations_and_design':len(ass)==len(set(ass)) and all(q.scalars(ash[str(i)])['fleet']==fid and q.scalars(q.block(ash[str(i)],'ship_design_implementation'))['design']==(167772797 if i in new else 67110548) and 0<q.scalars(ash[str(i)])['hitpoints']<=q.scalars(ash[str(i)])['max_hitpoints'] for fid,ss in am.items() for i in ss),
 'old_surviving_real_design_and_construction_dates_held':all(q.scalars(q.block(bsh[str(i)],'ship_design_implementation'))['design']==q.scalars(q.block(ash[str(i)],'ship_design_implementation'))['design'] and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] for i in set(bs)&set(ass)),
 'total_naval_size_matches_all_actual_owned_corvettes':q.scalars(q.block(ar['country'],'0'))['fleet_size']==5*len(ass),
 'actual_native_shipyard_modules_and_crews_held':q.scalars(q.block(sb,'modules'))==q.scalars(q.block(sa,'modules'))=={'0':'shipyard','1':'shipyard'} and q.block(sb,'buildings')==q.block(sa,'buildings') and all(q.scalars(sb)[k]==q.scalars(sa)[k] for k in ['level','type','build_queue','shipyard_build_queue','station']),
 'EEP_ledger_and_country_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'unique_core_owned_capacity11_original_modifiers':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11 and b['planets']['7']['modifiers']==core['modifiers'],
 'both_sources_unowned_shattered_no_actual_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned_no_active_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'government_core_and_AP_traditions_held':omit(bc['government'],{'council_agenda_progress','council_agenda_cooldowns'})==omit(ac['government'],{'council_agenda_progress','council_agenda_cooldowns'}) and bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'actual_society_project2_progress_and_bank_conserved':progress(bc)['special_project']==progress(ac)['special_project']==2 and 0<progress(bc)['progress']<progress(ac)['progress']<3000 and abs((D(str(progress(ac)['progress']))-D(str(progress(bc)['progress'])))-(D(str(bc['research_stockpile']['society_research']))-D(str(ac['research_stockpile']['society_research'])))*D('2.33'))<D('0.00005'),
 'native_project_events_level1_and_old_tech_held':q.block(q.block(br['country'],'0'),'events')==q.block(q.block(ar['country'],'0'),'events') and q.scalars(q.block(q.block(ar['country'],'0'),'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_colonization_2':607.25288} and ac['research_stockpile']['society_research']>0,
 'all_primary_actual_stocks_positive':all(ac['effective_stockpile'][k]>0 for k in nets),
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['species','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['exact_month3_input_date_and_prior42_precondition']=before=='terravore-raid-defense-month2' and after=='terravore-raid-defense-month3' and b['date']=='2261.09.02' and a['date']=='2261.10.02' and len(pre['checks'])==42
checks['first_two_paid_orders_completed_next_two_work15']=len(bids)==20 and len(aids)==18 and aids==bids[2:] and all(q.scalars(bi[str(i)])['progress']==0 and q.scalars(ai[str(i)])['progress']==(15 if n<2 else 0) for n,i in enumerate(aids)) and q.scalars(queue(br))['simultaneous']==q.scalars(queue(ar))['simultaneous']==2
expected_lost=set()
checks['no_new_losses_four_old_two_new_survivors']=not lost and set(new)=={33555993,33555628} and set(bm)=={16777797} and set(am)=={16777797,777} and am[16777797]==bm[16777797]==[16778303,1568,16778649,33555886] and am[777]==[33555993,33555628]
combat=lambda f:set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(f,'combat'),'in_combat_with'))))
checks['each_lost_ship_previously_fighting_same_enemy']=all(combat(bfl[str(q.scalars(bsh[str(i)])['fleet'])])=={18} for i in lost)
checks['active_reciprocal_main_station_and_enemy_combat']=combat(afl['18'])=={16777797,0,777} and combat(afl['16777797'])==combat(afl['0'])==combat(afl['777'])=={18}
checks['destroyed_fleet602_and_ship1570_exact_none']=q.scalars(br['fleet']).get('602')==q.scalars(br['ships']).get('1570')=='none' and not any(k=='602' for k,v,o in q.fields(ar['fleet'])) and not any(k=='1570' for k,v,o in q.fields(ar['ships']))
def anonymous(t):
 out=[];depth=0
 for token,start,end in q.tokens(t):
  if token=='{':
   if depth==0:beg=end
   depth+=1
  elif token=='}':
   depth-=1
   if depth==0:out.append(t[beg:start])
 assert depth==0
 return out
stats=q.block(q.block(afl['18'],'fleet_stats'),'combat_stats')
enemy_counts={q.scalars(v)['fleet']:(q.ids(q.block(v,'ship_size_count')),q.ids(q.block(v,'ship_size_count_lost'))) for v in anonymous(q.block(stats,'enemy'))}
checks['native_enemy_cumulative_loss_counts_exact']=q.scalars(stats)['date']=='2261.07.03' and enemy_counts=={16777797:([18],[14]),602:([1],[1]),0:([1],[0]),777:([2],[0])}
own_stats=q.block(q.block(afl['16777797'],'fleet_stats'),'combat_stats');own=q.block(own_stats,'fleet')
checks['native_main_stats_independently_four_of18_alive']=q.scalars(own_stats)['date']=='2261.07.03' and q.scalars(own)['fleet']==16777797 and q.ids(q.block(own,'ship_size_count'))==[18] and q.ids(q.block(own,'ship_size_count_lost'))==[14]
checks['enemy44_real_hitpoints2153_not_fleet_cache']=q.ids(q.block(afl['18'],'ships'))==[44] and q.scalars(ash['44'])['fleet']==18 and q.scalars(ash['44'])['hitpoints']==2153.25964<q.scalars(bsh['44'])['hitpoints']==6139.94232 and q.scalars(ash['44'])['max_hitpoints']==12000 and q.scalars(ash['44'])['construction_date']==q.scalars(bsh['44'])['construction_date']=='2140.01.01'
checks['actual_station0_survives_hull9020_armor_damaged']=q.ids(q.block(afl['0'],'ships'))==[0] and q.scalars(ash['0'])['fleet']==0 and q.scalars(ash['0'])['hitpoints']==9020.51972 and q.scalars(ash['0'])['max_hitpoints']==12500 and q.scalars(ash['0'])['shield_hitpoints']==4320 and q.scalars(ash['0'])['armor_hitpoints']==2.5625
checks['mother_bombardment_did_not_resume']=b['planets']['7']['last_bombardment']==core['last_bombardment']=='2261.07.03' and b['planets']['7']['bombardment_damage']==11.60589 and core['bombardment_damage']==11.01168
ng=q.block(q.block(ar['colony'],'0'),'last_month_growth_data')
checks['native_growth6_no_bombardment_death_category']=q.scalars(q.block(ng,'growth_and_size'))=={'month_start_size':10189,'growth':6} and b['colonies']['0']['actual_pop_sum']==10189 and a['colonies']['0']['actual_pop_sum']==10195 and list(q.fields(q.block(ng,'current_month_growth_details')))==[('key','"GROWTH_CAT_GROWTH"',False),('value','6',False),('key','"GROWTH_CAT_PROMOTION"',False),('value','0',False)]
checks['hive5_mining10_generator6_both_states']=all({v['districts'][str(i)]['type']:v['districts'][str(i)]['level'] for i in v['colonies']['0']['districts']}=={'district_hive':5,'district_mining':10,'district_generator':6} for v in [b,a])
mother_ids=[str(i) for zid in ['0','2','61'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))]
checks['all_actual_mother_buildings_raw_held_only_old83_ruined']=all(q.block(br['buildings'],i)==q.block(ar['buildings'],i) for i in mother_ids) and q.scalars(q.block(ar['buildings'],'83'))=={'type':'building_hive_node','ruined':'yes','position':0}
checks['coordinator1800_all_research300_logistics500_telepath200_full']=all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',1800),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2000),('technician_drone',1200)])
checks['full_psionic_breach_species73_EEP_psi1_held']=bc['variables']['eep_psi']==ac['variables']['eep_psi']==1 and all(q.scalars(q.block(q.block(rt['country'],'0'),'flags')).get(k)==v for rt in [br,ar] for k,v in [('breached_shroud',63314904),('psionic_traditions_unlocked',63314904),('eep_psi_notice',63315600)]) and set(a['species'])=={'73'} and a['species']['73']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_psionic'] and not a['situations']
holders=lambda rt:set(re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(q.block(rt['country'],'0'),'surveyed_deposit_holders')))
checks['object1084_actually_surveyed_holders269']=holders(br)<=holders(ar) and holders(ar)-holders(br)=={('0','1084')} and len(holders(ar))==269
science=afl['1'];survey=q.block(q.block(science,'current_order'),'survey_planet_order')
checks['original_science1_scientist_alive_survey1085']=q.ids(q.block(science,'ships'))==[1] and q.scalars(ash['1'])['leader']==150994969 and q.scalars(ash['1'])['hitpoints']>0 and q.scalars(q.block(q.block(science,'movement_manager'),'coordinate'))['origin']==97 and q.scalars(q.block(survey,'deposit_holder'))=={'type':0,'id':1085} and q.scalars(survey)=={'progress':9.2,'can_reach':'yes','order_id':43,'commissioner':4294967295}
queued=[v for k,v,o in q.fields(q.block(science,'order')) if k=='survey_planet_order' and o]
checks['three_remaining_survey_orders_raw_held']=len(queued)==3 and [q.scalars(q.block(v,'deposit_holder'))['id'] for v in queued]==[1080,1082,2072] and queued==[v for k,v,o in q.fields(q.block(bfl['1'],'order')) if k=='survey_planet_order' and o][1:]
checks['actual_society_project1909_15775_and_bank4160_52287']=progress(ac)['progress']==1909.15775 and ac['research_stockpile']['society_research']==4160.52287
checks['energy_minerals_positive_and_unfiltered_errors2670']=nets['energy']>0 and nets['minerals']>0 and len((run/(after+'-error-after.log')).read_bytes())==2670
checks['two_new_ships_exact_paid_design_and_native_build_date']=len(new)==2 and all(q.scalars(q.block(ash[str(i)],'ship_design_implementation'))=={'design':167772797,'upgrade':4294967295,'growth_stage':0} and q.scalars(ash[str(i)])['construction_date']=='2261.09.20' for i in new)
original=json.loads((run/(after+'-raid-month3-proof.json')).read_text('utf-8'))
checks['original43_exact_two_failures_preserved']=original['status']=='FAIL' and len(original['checks'])==43 and {k for k,v in original['checks'].items() if v is False}=={'destroyed_fleet602_and_ship1570_exact_none','mother_bombardment_did_not_resume'} and all(v is True for k,v in original['checks'].items() if k not in {'destroyed_fleet602_and_ship1570_exact_none','mother_bombardment_did_not_resume'}) and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'] and h.sha256(run/'priority_terravore_raid_month3_guard.py')=='7039305a8e447f4b4fd25a7c0db43b3fabeb82e7dccdc1ee6db55c16ceb46d36' and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==1
p={'status':'PASS_TERRAVORE_SECOND_RAID_MONTH3_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'days':days,'actual_owned_military_fleets':am,'actual_new_paid_ship_ids':new,'actual_lost_ship_ids':lost,'remaining_paid_orders':aids,'front_order_progress':[q.scalars(ai[str(i)])['progress'] for i in aids[:2]],'enemy_native_loss_counts':enemy_counts,'actual_enemy44':q.scalars(ash['44']),'actual_station0':q.scalars(ash['0']),'actual_stocks':ac['effective_stockpile'],'current_month_nets':nets,'calendar_ready':all(checks.values()),'scope':'Third 30-day native combat month: no new losses, four old and two newly paid corvettes survive;18 paid orders incomplete. No victory, final stable economy, menace or full-route acceptance.'}
out=run/(after+'-raid-month3-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original combat month2 FAIL retained'
