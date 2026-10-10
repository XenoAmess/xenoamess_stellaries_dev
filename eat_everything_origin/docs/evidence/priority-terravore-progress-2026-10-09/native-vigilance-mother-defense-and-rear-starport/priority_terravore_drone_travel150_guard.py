"""Read-only paid construction and travel observation; caravan pending blocks calendar."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-route-drone-attack-ordered';after='terravore-route-drone-travel150'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def owned(rt):return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))))
def military(rt):return {i:q.ids(q.block(q.block(rt['fleet'],str(i)),'ships')) for i in owned(rt) if q.scalars(q.block(rt['fleet'],str(i)))['ship_class']=='shipclass_military'}
def queue(rt,i):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),str(i))
def project(c):return q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])
def omit(v,ks):return [(k,x,o) for k,x,o in q.fields(v) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-drone-attack-order-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
bm,am=military(br),military(ar);bs=[s for ss in bm.values() for s in ss];ass=[s for ss in am.values() for s in ss];new=[s for s in ass if s not in bs]
gain=D(str(project(ac)['progress']))-D(str(project(bc)['progress']));draw=D(str(bc['research_stockpile']['society_research']))-D(str(ac['research_stockpile']['society_research']));residual=gain-draw*D('2.33')
bi=q.block(q.block(br['construction'],'item_mgr'),'items');ai=q.block(q.block(ar['construction'],'item_mgr'),'items')
mother=[str(i) for zid in ['0','2','61'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))]
main=q.block(ar['fleet'],'33555034');nets={k:sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys']}
pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={
 'exact_original_SHA_pair_and_dates':b['date']=='2262.11.17' and a['date']=='2263.04.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior23_attack_order_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_DRONE_ATTACK_ORDER_COMPONENT' and len(pre['checks'])==23 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='e580aca59165ce32e1a24e07a390717cc23fa915db4f2c9478026de2e70dc664',
 'unique150_calendar_actual_exit0':receipt['days']==150 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'seventeen_real_ships_no_original_loss_two_paid_new':len(bs)==15 and set(bs)<=set(ass) and len(ass)==len(set(ass))==17 and new==[1816,1817],
 'actual_three_fleet_memberships':am=={788:[1816,1817],33555013:bm[33555013],33555034:bm[33555034]},
 'all_real_design_full_health_original_dates_held':all(q.scalars(q.block(q.block(ar['ships'],str(s)),'ship_design_implementation'))=={'design':167772797,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(ar['ships'],str(s)))['hitpoints']==270 for s in ass) and all(q.scalars(q.block(br['ships'],str(s)))['construction_date']==q.scalars(q.block(ar['ships'],str(s)))['construction_date'] for s in bs),
 'two_new_native_dates2262_12_02':all(q.scalars(q.block(ar['ships'],str(s)))['construction_date']=='2262.12.02' for s in new),
 'final_two_paid_orders_completed_shipyard_empty':q.ids(q.block(queue(br,3),'items'))==[33554455,419430424] and not q.ids(q.block(queue(ar,3),'items')) and all(not q.block(ai,str(i)).strip() for i in [33554455,419430424]),
 'native_naval85_shipyard_modules_held':q.scalars(q.block(ar['country'],'0'))['fleet_size']==85 and q.scalars(queue(ar,3))['simultaneous']==2 and all(q.block(q.block(q.block(br['starbase_mgr'],'starbases'),'0'),k)==q.block(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),k) for k in ['modules','buildings']),
 'main14_same_follow_order_now139_not_arrival':q.block(q.block(br['fleet'],'33555034'),'current_order')==q.block(main,'current_order') and q.scalars(q.block(q.block(main,'movement_manager'),'coordinate'))=={'x':67.39654,'y':171.64324,'origin':139} and q.scalars(main)['hit_points']==3780,
 'all_owned_fleets_no_active_combat':all(not q.block(q.block(q.block(ar['fleet'],str(i)),'combat'),'in_combat_with').strip() for i in owned(ar)),
 'original_enemy_raw_held_not_defeated':q.block(br['fleet'],'33555206')==q.block(ar['fleet'],'33555206'),
 'constructor_safely_halted171_raw_held':q.block(br['fleet'],'2')==q.block(ar['fleet'],'2'),
 'original_science1_idle97_raw_held':q.block(br['fleet'],'1')==q.block(ar['fleet'],'1'),
 'same_second_paid_mine221_2_work':q.ids(q.block(queue(ar,0),'items'))==[771751943] and omit(q.block(bi,'771751943'),{'progress'})==omit(q.block(ai,'771751943'),{'progress'}) and q.scalars(q.block(ai,'771751943'))['progress']==221.2,
 'all_three_district_objects_raw_held':all(q.block(br['districts'],i)==q.block(ar['districts'],i) for i in ['1','2','3']),
 'all_actual_mother_buildings_zones_raw_held':all(q.block(br['buildings'],i)==q.block(ar['buildings'],i) for i in mother) and all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','61']),
 'native_expected_workers_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2200),('technician_drone',1200)]),
 'population10308_last_month10301_plus7':a['colonies']['0']['actual_pop_sum']==10308 and q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':10301,'growth':7},
 'native_damage_zero_without_new_bombardment':a['planets']['7']['bombardment_damage']==0 and a['planets']['7']['last_bombardment']==b['planets']['7']['last_bombardment']=='2261.07.03',
 'station_full_no_new_combat':all(q.scalars(q.block(ar['ships'],'0'))[k]==v for k,v in {'hitpoints':12500,'shield_hitpoints':4320,'armor_hitpoints':5125,'last_combat_activity':'2261.11.14'}.items()),
 'society2979_bank3701_gain_conserved':project(ac)=={'progress':2979.82063,'special_project':2,'date':'2258.11.02'} and ac['research_stockpile']['society_research']==3701.01087 and gain>0 and draw>0 and abs(residual)<D('0.00005'),
 'same_native_projects_and_level1_no_menace':q.block(q.block(br['country'],'0'),'events')==q.block(q.block(ar['country'],'0'),'events') and q.scalars(q.block(q.block(ar['country'],'0'),'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'},
 'EEP_variables_flags_unique_core_capacity11_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()) and sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and a['planets']['7']['variables']['eep_capacity_value']==11 and a['planets']['7']['modifiers']==b['planets']['7']['modifiers'],
 'same_species_full_psionic_and_event_targets':b['species']==a['species'] and b['event_targets']==a['event_targets'] and a['species']['73']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_psionic'] and all(q.scalars(q.block(q.block(ar['country'],'0'),'flags')).get(k)==v for k,v in [('breached_shroud',63314904),('psionic_traditions_unlocked',63314904),('eep_psi_notice',63315600)]),
 'only_mother_owned_no_EEP_task':ac['owned_colonies']==[0] and not a['situations'],
 'exact_original_caravan224_pending_observed':pending==[{'id':224,'event':'cara.2020','date':'2265.07.09','country':0}],
 'actual_energy_minerals_positive_alloys_negative_recorded':nets=={'energy':D('22.505'),'minerals':D('16.3585'),'unity':D('149.88550'),'alloys':D('-5.296')} and all(ac['effective_stockpile'][k]>0 for k in nets),
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks={k:bool(v) for k,v in checks.items()}
p={'status':'PASS_TERRAVORE_PAID_SHIP_COMPLETION_AND_TRAVEL150_OBSERVATION' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_military_fleets':am,'pending':pending,'society_gain':str(gain),'society_bank_draw':str(draw),'society_residual':str(residual),'calendar_ready':False,'scope':'Actual paid17 ships and travel to139 only. Original caravan pending blocks calendar; no arrival, cleared route, menace or full-route acceptance.'}
out=run/(after+'-travel150-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original travel observation FAIL retained'
