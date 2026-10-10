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
 'exact_pair_dates_SHA':before=='terravore-raid-repair-and-transit150' and after=='terravore-raid-recovered-month' and b['date']=='2262.04.17' and a['date']=='2262.05.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior35_repair_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_REPAIR_AND_TRANSIT_COMPONENT' and len(pre['checks'])==35 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='016b15f920cd714b43fdf9145bfbdbe096f399d066d10ed98e8c957694faa47b',
 'unique30_calendar_actual_exit0':receipt['days']==30 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'mother_construction_empty_both':not q.ids(q.block(queue(br,0),'items')) and not q.ids(q.block(queue(ar,0),'items')),
 'all_mother_buildings_raw_held':all(q.block(br['buildings'],i)==q.block(ar['buildings'],i) for i in mother_ids),
 'all_three_zones_raw_held':all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','61']),
 'repaired83_and_all_three_completed_nodes':q.ids(q.block(q.block(ar['zones'],'61'),'buildings'))==[83,16777258,86] and all(q.scalars(q.block(ar['buildings'],str(i)))=={'type':'building_hive_node','position':n} for n,i in enumerate([83,16777258,86])),
 'all_districts_hive5_mining10_generator6_held':b['districts']==a['districts'] and {a['districts'][str(i)]['type']:a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts']}=={'district_hive':5,'district_mining':10,'district_generator':6},
 'all_eight_native_jobs_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2000),('technician_drone',1200)]),
 'seven_real_owned_ships_no_new_no_loss':bm==am=={33555013:[33555519],33555034:[50333102,50332844,33554476,33555618,33556208,33556207]} and not new and len(ass)==len(set(ass))==7,
 'all_ship_native_designs_dates_health_held':all(q.scalars(q.block(bsh[str(i)],'ship_design_implementation'))==q.scalars(q.block(ash[str(i)],'ship_design_implementation'))=={'design':167772797,'upgrade':4294967295,'growth_stage':0} and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] and q.scalars(ash[str(i)])['fleet']==f and q.scalars(ash[str(i)])['hitpoints']==270 for f,ss in am.items() for i in ss),
 'ten_paid_orders_held_only_front_progress18_75_to56_25':bids==aids==[603979789,150994958,134217744,402653201,16777234,33554452,134217749,16777238,33554455,419430424] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and q.scalars(bi[str(i)])['progress']==(18.75 if n<2 else 0) and q.scalars(ai[str(i)])['progress']==(56.25 if n<2 else 0) for n,i in enumerate(aids)),
 'actual_naval_size35':q.scalars(q.block(ar['country'],'0'))['fleet_size']==35,
 'native_shipyard_two_slots_modules_buildings_held':q.scalars(queue(br,3))['simultaneous']==q.scalars(queue(ar,3))['simultaneous']==2 and all(q.block(q.block(q.block(br['starbase_mgr'],'starbases'),'0'),k)==q.block(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),k) for k in ['modules','buildings']),
 'all_owned_fleets_no_active_combat':all(not q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip() for i in owned(ar)),
 'station12500_shield4320_armor_recovers_last_combat_held':all(q.scalars(ash['0'])[k]==v for k,v in {'hitpoints':12500,'shield_hitpoints':4320,'last_damage':'2261.11.14','last_combat_activity':'2261.11.14'}.items()) and q.scalars(bsh['0'])['armor_hitpoints']<q.scalars(ash['0'])['armor_hitpoints']<=5125,
 'no_new_bombardment_native_damage_recovers':b['planets']['7']['last_bombardment']==core['last_bombardment']=='2261.07.03' and 0<=core['bombardment_damage']<b['planets']['7']['bombardment_damage'],
 'population10231_plus6_and_native_month_growth':b['colonies']['0']['actual_pop_sum']==10231 and a['colonies']['0']['actual_pop_sum']==10237 and q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':10231,'growth':6},
 'EEP_all_variables_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()),
 'unique_core_owned_capacity11_modifiers_held':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11 and b['planets']['7']['modifiers']==core['modifiers'],
 'only_mother_owned_no_active_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not a['situations'],
 'both_sources_unowned_shattered_no_actual_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'government_AP_traditions_held':omit(bc['government'],{'council_agenda_progress','council_agenda_cooldowns'})==omit(ac['government'],{'council_agenda_progress','council_agenda_cooldowns'}) and bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'native_events_level1_old_tech_held':q.block(q.block(br['country'],'0'),'events')==q.block(q.block(ar['country'],'0'),'events') and q.block(q.block(br['country'],'0'),'crisis_progression')==q.block(q.block(ar['country'],'0'),'crisis_progression') and q.scalars(q.block(q.block(ar['country'],'0'),'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_colonization_2':607.25288},
 'species_event_targets_full_psi_held':b['species']==a['species'] and b['event_targets']==a['event_targets'] and set(a['species'])=={'73'} and a['species']['73']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_psionic'] and all(q.scalars(q.block(q.block(ar['country'],'0'),'flags')).get(k)==v for k,v in [('breached_shroud',63314904),('psionic_traditions_unlocked',63314904),('eep_psi_notice',63315600)]),
 'actual273_survey_holders_all_held':holders(br)==holders(ar) and len(holders(ar))==273,
 'original_science_ship_and_scientist_alive_empty_orders':q.ids(q.block(afl['1'],'ships'))==[1] and q.scalars(ash['1'])['leader']==150994969 and q.scalars(ash['1'])['hitpoints']==375 and bool(q.block(ar['leaders'],'150994969').strip()) and not q.block(afl['1'],'current_order').strip() and not q.block(afl['1'],'order').strip(),
 'constructor_same_order_only_native_travel151':q.ids(q.block(afl['2'],'ships'))==[2] and q.block(bfl['2'],'current_order')==q.block(afl['2'],'current_order') and not q.block(afl['2'],'order').strip() and q.scalars(q.block(q.block(afl['2'],'movement_manager'),'coordinate'))=={'x':-12.53084,'y':192.6988,'origin':151},
 'all_primary_stocks_positive_energy_minerals_net_positive':all(ac['effective_stockpile'][k]>0 for k in nets) and nets['energy']>0 and nets['minerals']>0,
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
research_net={k:sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['physics_research','society_research','engineering_research']}
checks['society_project2_only_progress_changed']=omit(q.block(bc['tech_status'],'society_queue').strip()[1:-1],{'progress'})==omit(q.block(ac['tech_status'],'society_queue').strip()[1:-1],{'progress'}) and project(ac)['special_project']==2 and project(ac)['progress']==2318.83055
checks['society_bank_draw_exact_current_base_month']=draw>0 and abs(draw-research_net['society_research'])<D('0.00005') and all(ac['research_stockpile'][k]==bc['research_stockpile'][k]==0 for k in ['physics_research','engineering_research'])
checks['society_project_gain_exact_speed133_plus_bank_draw']=abs(gain-research_net['society_research']*D('1.33')-draw)<D('0.00005')
other_research={}
for field in ['physics','engineering']:
 x,y=[q.block(c['tech_status'],field+'_queue').strip()[1:-1] for c in [bc,ac]];g=D(str(q.scalars(y)['progress']))-D(str(q.scalars(x)['progress']));expected=research_net[field+'_research']*D('1.33');checks[field+'_queue_only_progress_speed133']=omit(x,{'progress'})==omit(y,{'progress'}) and abs(g-expected)<D('0.00005');other_research[field]={'gain':str(g),'expected':str(expected)}
p={'status':'PASS_TERRAVORE_RECOVERED_MONTH_BOUNDARY_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_owned_military_fleets':am,'remaining_paid_orders':aids,'society_gain':str(gain),'society_bank_draw':str(draw),'other_research':other_research,'actual_stocks':ac['effective_stockpile'],'current_month_nets':{k:str(v) for k,v in nets.items()},'calendar_ready':all(checks.values()),'scope':'One full post-raid month after original paid repair; no ship completion or loss, seven paid corvettes and ten pending orders, full jobs and research. Separate eight-resource ledger required. No outpost, menace or full-route claim.'}
out=run/(after+'-recovered-month-boundary-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original recovered month FAIL retained'
