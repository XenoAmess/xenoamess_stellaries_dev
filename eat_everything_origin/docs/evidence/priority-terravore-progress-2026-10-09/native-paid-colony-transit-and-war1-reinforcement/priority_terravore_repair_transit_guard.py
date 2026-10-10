"""Read-only post-raid repair, paid ships, survey and transit boundary."""
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
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def owned(rt):return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))))
def military(rt,fs):return {i:q.ids(q.block(fs[str(i)],'ships')) for i in owned(rt) if q.scalars(fs[str(i)])['ship_class']=='shipclass_military'}
def queue(rt,i):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),str(i))
def items(rt):return obj(q.block(q.block(rt['construction'],'item_mgr'),'items'))
def project(c):return q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])
def holders(rt):return re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(q.block(rt['country'],'0'),'surveyed_deposit_holders'))
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bfl,afl=obj(br['fleet']),obj(ar['fleet']);bsh,ash=obj(br['ships']),obj(ar['ships'])
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'));validate_native_interval(b['date'],a['date'],receipt['days'])
pre=json.loads((run/receipt['prior_proof_file']).read_text('utf-8'));ex=json.loads((run/(receipt['prior_execution_stage']+'-execution.json')).read_text('utf-8'))
bm,am=military(br,bfl),military(ar,afl);bs=[s for ss in bm.values() for s in ss];ass=[s for ss in am.values() for s in ss];new=[i for i in ass if i not in bs]
bids,aids=[q.ids(q.block(queue(rt,3),'items')) for rt in [br,ar]];bi,ai=items(br),items(ar);core=a['planets']['7'];nets={k:sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys','trade']}
mother_ids=[str(i) for zid in ['0','2','61'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))]
gain=D(str(project(ac)['progress']))-D(str(project(bc)['progress']));draw=D(str(bc['research_stockpile']['society_research']))-D(str(ac['research_stockpile']['society_research']));residual=gain-draw*D('2.33')
checks={
 'exact_original_SHA_pair_dates':before=='terravore-yodd-constructor-move-ordered' and after=='terravore-raid-repair-and-transit150' and b['date']=='2261.11.17' and a['date']=='2262.04.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior20_move_order_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_YODD_CONSTRUCTOR_MOVE_ORDER_COMPONENT' and len(pre['checks'])==20 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'unique150_calendar_confirmed_actual_exit0':receipt['days']==150 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'native_repair83_same_type_position_only_ruin_removed':q.scalars(q.block(br['buildings'],'83'))=={'type':'building_hive_node','ruined':'yes','position':0} and q.scalars(q.block(ar['buildings'],'83'))=={'type':'building_hive_node','position':0} and omit(q.block(br['buildings'],'83'),{'ruined'})==list(q.fields(q.block(ar['buildings'],'83'))),
 'paid_repair620757018_completed_exact_none_queue0_empty':q.ids(q.block(queue(br,0),'items'))==[620757018] and not q.ids(q.block(queue(ar,0),'items')) and q.scalars(q.block(q.block(ar['construction'],'item_mgr'),'items')).get('620757018')=='none' and q.scalars(q.block(bi['620757018'],'resources'))=={'minerals':160},
 'all_other_mother_buildings_raw_held':all(q.block(br['buildings'],i)==q.block(ar['buildings'],i) for i in mother_ids if i!='83'),
 'all_three_zones_memberships_raw_held':all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','61']) and q.ids(q.block(q.block(ar['zones'],'61'),'buildings'))==[83,16777258,86],
 'all_districts_held_hive5_mining10_generator6':b['districts']==a['districts'] and all({v['districts'][str(i)]['type']:v['districts'][str(i)]['level'] for i in v['colonies']['0']['districts']}=={'district_hive':5,'district_mining':10,'district_generator':6} for v in [b,a]),
 'all_full_native_workers_after_repair':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2000),('technician_drone',1200)]),
 'only_six_paid_completions_original_survivor_held':bm=={33555013:[33555519]} and am=={33555013:[33555519],33555034:[50333102,50332844,33554476,33555618,33556208,33556207]} and len(new)==6 and set(bs)<=set(ass) and len(ass)==len(set(ass))==7,
 'actual_all_seven_designs_and_health':all(q.scalars(q.block(ash[str(i)],'ship_design_implementation'))=={'design':167772797,'upgrade':4294967295,'growth_stage':0} and q.scalars(ash[str(i)])['hitpoints']==q.scalars(ash[str(i)])['max_hitpoints']==270 for i in ass),
 'six_native_construction_dates_match_paid_pair_batches':[q.scalars(ash[str(i)])['construction_date'] for i in new]==['2261.12.26']*2+['2262.02.14']*2+['2262.04.02']*2 and q.scalars(ash['33555519'])['construction_date']=='2261.11.08',
 'ten_original_paid_orders_exact_suffix_and_other_fields_held':len(bids)==16 and aids==bids[6:]==[603979789,150994958,134217744,402653201,16777234,33554452,134217749,16777238,33554455,419430424] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) for i in aids),
 'remaining_two_slots_progress18_75_then_zero':all(q.scalars(ai[str(i)])['progress']==(18.75 if n<2 else 0) for n,i in enumerate(aids)) and q.scalars(queue(br,3))['simultaneous']==q.scalars(queue(ar,3))['simultaneous']==2,
 'actual_naval_size35':q.scalars(q.block(ar['country'],'0'))['fleet_size']==35,
 'native_shipyard_modules_and_building_held':all(q.block(q.block(q.block(br['starbase_mgr'],'starbases'),'0'),k)==q.block(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),k) for k in ['modules','buildings']),
 'all_owned_fleets_no_active_combat':all(not q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip() for i in owned(ar)),
 'station_full_hull_shield_native_armor_recovered':q.ids(q.block(afl['0'],'ships'))==[0] and 0 in owned(ar) and all(q.scalars(ash['0'])[k]==v for k,v in {'hitpoints':12500,'shield_hitpoints':4320,'armor_hitpoints':3233.875,'last_damage':'2261.11.14','last_combat_activity':'2261.11.14'}.items()),
 'no_new_bombardment_native_damage_recovered':b['planets']['7']['last_bombardment']==core['last_bombardment']=='2261.07.03' and b['planets']['7']['bombardment_damage']==10.08963 and core['bombardment_damage']==7.01613,
 'actual_population10231_last_month10225_plus6':b['colonies']['0']['actual_pop_sum']==10201 and a['colonies']['0']['actual_pop_sum']==10231 and q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':10225,'growth':6},
 'EEP_ledger_flags_capacity_and_unique_core_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()) and sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11 and b['planets']['7']['modifiers']==core['modifiers'],
 'only_mother_owned_no_active_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not a['situations'],
 'both_old_sources_unowned_shattered_no_actual_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'government_AP_traditions_held':omit(bc['government'],{'council_agenda_progress','council_agenda_cooldowns'})==omit(ac['government'],{'council_agenda_progress','council_agenda_cooldowns'}) and bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'society_project2_actual_progress_bank_conserved':project(bc)=={'progress':1967.16037,'special_project':2,'date':'2258.11.02'} and project(ac)=={'progress':2259.78388,'special_project':2,'date':'2258.11.02'} and ac['research_stockpile']['society_research']==4010.03954 and draw>0 and abs(residual)<D('0.00005'),
 'native_events_level1_old_tech_held':q.block(q.block(br['country'],'0'),'events')==q.block(q.block(ar['country'],'0'),'events') and q.scalars(q.block(q.block(ar['country'],'0'),'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_colonization_2':607.25288},
 'species_event_targets_held_full_psi_breach':b['species']==a['species'] and b['event_targets']==a['event_targets'] and set(a['species'])=={'73'} and a['species']['73']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_psionic'] and all(q.scalars(q.block(q.block(ar['country'],'0'),'flags')).get(k)==v for k,v in [('breached_shroud',63314904),('psionic_traditions_unlocked',63314904),('eep_psi_notice',63315600)]),
 'actual_holders273_old_all_retained_exact_three_added':len(holders(br))==270 and len(holders(ar))==273 and set(holders(br))<=set(holders(ar)) and set(holders(ar))-set(holders(br))=={('0','1080'),('0','1082'),('0','2072')},
 'all_ten97_objects_actually_surveyed':all(('0',str(i)) in holders(ar) for i in [1078,1079,1080,1081,1082,1083,1084,1085,1086,2072]),
 'original_science_ship_and_scientist_alive_orders_empty':q.ids(q.block(afl['1'],'ships'))==[1] and q.scalars(ash['1'])['leader']==150994969 and q.scalars(ash['1'])['hitpoints']==375 and q.block(ar['leaders'],'150994969').strip() and not q.block(afl['1'],'current_order').strip() and not q.block(afl['1'],'order').strip(),
 'constructor2_original_move_order_raw_held_native_transit151':q.ids(q.block(afl['2'],'ships'))==[2] and q.block(bfl['2'],'current_order')==q.block(afl['2'],'current_order') and not q.block(afl['2'],'order').strip() and q.scalars(q.block(q.block(afl['2'],'movement_manager'),'coordinate'))=={'x':-5.37569,'y':-190.8992,'origin':151} and q.scalars(afl['2'])['order_id']==10,
 'real_stocks_energy_minerals_unity_alloys_trade_positive':all(ac['effective_stockpile'][k]>0 for k in nets),
 'actual_energy_minerals_net_positive_building_upkeep27':nets['energy']>0 and nets['minerals']>0 and ac['budget_categories']['current_month']['expenses']['planet_buildings']['energy']==27,
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors_exact2670_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks={k:bool(v) for k,v in checks.items()}
p={'status':'PASS_TERRAVORE_NATIVE_REPAIR_AND_TRANSIT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_new_paid_ship_ids':new,'actual_owned_military_fleets':am,'remaining_paid_orders':aids,'actual_society_gain':str(gain),'actual_society_bank_draw':str(draw),'actual_society_residual':str(residual),'actual_stockpile':ac['effective_stockpile'],'current_month_nets':{k:str(v) for k,v in nets.items()},'calendar_ready':all(checks.values()),'scope':'Original paid node83 repair complete, six additional paid ships, all ten97 objects surveyed, constructor still in transit151. No recovered full stable month, arrival, outpost, menace or full-route acceptance.'}
out=run/(after+'-repair-transit-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original repair/transit FAIL retained'
