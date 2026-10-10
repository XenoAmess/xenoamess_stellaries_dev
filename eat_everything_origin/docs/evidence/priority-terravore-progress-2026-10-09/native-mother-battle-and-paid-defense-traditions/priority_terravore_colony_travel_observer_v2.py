"""Reusable V2 native colony travel observer with retired item generation; never grants or writes saves."""
import sys,json,logging,shutil,zipfile,re
from pathlib import Path
from decimal import Decimal as D
before,after,prior_file,prior_exec=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
def fleets(cr):return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(cr,'fleets_manager'),'owned_fleets'))))
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bfl,afl=objs(br['fleet']),objs(ar['fleet']);bsh,ash=objs(br['ships']),objs(ar['ships']);owned=fleets(acr)
mil={i:q.ids(q.block(afl[str(i)],'ships')) for i in owned if q.scalars(afl[str(i)])['ship_class']=='shipclass_military'}
pre=json.loads((run/prior_file).read_text('utf-8'));ex=json.loads((run/(prior_exec+'-execution.json')).read_text('utf-8'));rc=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
paid_stage='terravore-colony1085-auto-survey-paid';paid=json.loads((run/(paid_stage+'-colony-auto-payment-proof.json')).read_text('utf-8'));pex=json.loads((run/(paid_stage+'-guard-execution.json')).read_text('utf-8'))
holders=lambda cr:re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(cr,'surveyed_deposit_holders'));bh,ah=holders(bcr),holders(acr);newholders=[v for v in ah if v not in bh]
pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0];combat=[i for i in owned if q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip()]
planets=objs(q.block(ar['planets'],'planet'));target=q.scalars(planets['1085']);ship=ash.get('33556279');ss=q.scalars(ship) if ship else {};cf=afl.get(str(ss.get('fleet')),'');order=q.block(q.block(cf,'current_order'),'colonize_planet_order')
colony_started=target.get('controller')==0 and 'colony' in target
known_habitable=[{'planet':int(i),**{k:v for k,v in q.scalars(planets[i]).items() if k in {'planet_class','planet_size','colony','owner','controller'}}} for ty,i in ah if ty=='0' and i in planets and q.scalars(planets[i]).get('planet_class') in {'pc_continental','pc_ocean','pc_tropical','pc_desert','pc_arid','pc_savannah','pc_alpine','pc_tundra','pc_arctic','pc_gaia','pc_nuked'}]
co=a['colonies']['0'];nets={k:sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','alloys','unity']}
item_fields=list(q.fields(q.block(q.block(ar['construction'],'item_mgr'),'items')))
retired_slot=[(k,v,o) for k,v,o in item_fields if int(k)%16777216==23]
completion_stage='terravore-colony1085-build-travel360'
completion=json.loads((run/(completion_stage+'-colony-travel-observation-proof.json')).read_text('utf-8'))
completion_exec=json.loads((run/(completion_stage+'-guard-execution.json')).read_text('utf-8'))
original_path=run/(after+'-colony-travel-observation-proof.json')
original_fail_bound=True
if original_path.exists():
 original=json.loads(original_path.read_text('utf-8'));original_exec=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
 original_fail_bound=(original['status']=='FAIL' and len(original['checks'])==15 and {k for k,v in original['checks'].items() if v is not True}=={'original_paid_item_completed_queue_and_expansion_empty'} and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'] and original_exec['returncode']==1 and original_exec['helper_sha256']=='6c657a6ab77c5c56f6986327e27422bde1ad93e7fcb8e1a50bd67617d12e368c' and h.sha256(run/Path(original_exec['command'][1]).name)==original_exec['helper_sha256'])
checks={
 'original_SHA_pair_prior_PASS_actual0':all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]) and pre['status'].startswith('PASS_') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and h.sha256(run/Path(ex['command'][1]).name)==ex['helper_sha256'],
 'unique_native_calendar_receipt_actual0':rc['status']=='CALENDAR_CONFIRMED' and rc['start_date']==b['date'] and rc['date']==a['date'] and 1<=rc['days']<=360 and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'original21_paid_order_proof_and_SHA_actual0':paid['status']=='PASS_TERRAVORE_COLONY1085_PAYMENT_AND_NATIVE_AUTO_SURVEY_COMPONENT' and len(paid['checks'])==21 and all(v is True for v in paid['checks'].values()) and paid['after_sha256']==h.sha256(run/(paid_stage+'.sav'))=='2c3b10843133a3b76276439bbeab20e10d4dbc757dde5645af4d4b37a3558fa5' and pex['returncode']==0 and pex['helper_sha256']=='8d6cfbcf326f1f1da28518922602ad053edfcb77cdaf7943f6b5a300a269ee55',
 'original_paid_item_retired_own_queue_and_expansion_empty':not any(k=='150994967' and o for k,v,o in item_fields) and len(retired_slot)==1 and int(retired_slot[0][0])>=150994967 and not q.ids(q.block(q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'3'),'items')) and not q.block(q.block(acr,'modules'),'standard_expansion_module').strip(),
 'real_original_colonizer_proven_or_native_colony_started':(bool(ship) and ss['construction_date']=='2266.03.17' and ss['hitpoints']==625 and q.scalars(q.block(ship,'colonization_data'))=={'species':73} and q.scalars(q.block(ship,'ship_design_implementation'))=={'design':150995039,'upgrade':4294967295,'growth_stage':0} and ss['fleet'] in owned and q.scalars(cf)['ship_class']=='shipclass_colonizer' and q.scalars(order).get('planet')==1085 and q.scalars(order).get('can_reach')=='yes') or (not ship and colony_started),
 'original8_military_ships_all_designs_full_health_held':mil=={788:[1816,1817],33555013:[33555519],33555034:[33556208,33556207,50332878,1807,1810]} and all(q.scalars(ash[str(i)])['hitpoints']==270 and q.block(bsh[str(i)],'ship_design_implementation')==q.block(ash[str(i)],'ship_design_implementation') and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] for ids in mil.values() for i in ids),
 'EEP_economy_flags_species_targets_capacity11_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and b['species']==a['species'] and b['event_targets']==a['event_targets'] and b['planets']['7']['modifiers']==a['planets']['7']['modifiers'] and ac['variables']['eep_d']==11 and ac['variables']['eep_psi']==1 and not a['situations'],
 'mother_still_unique_core_no_new_bombardment_or_damage':a['planets']['7']['owner']==0 and a['planets']['7']['bombardment_damage']==b['planets']['7']['bombardment_damage']==0 and a['planets']['7']['last_bombardment']==b['planets']['7']['last_bombardment']=='2261.07.03' and [k for k,v in planets.items() if 'eep_core' in q.scalars(q.block(v,'flags'))]==['7'],
 'all_mother_buildings_zones_districts_raw_held':all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','61']) and all(q.block(br['districts'],i)==q.block(ar['districts'],i) for i in ['1','2','3']) and all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for zid in ['0','2','61'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))),
 'all_original_workers_and200_fabricators_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('fabricator',200),('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2400),('technician_drone',1200)]),
 'positive_mother_housing_amenities_stability80':co['free_housing']>0 and co['free_amenities']>0 and co['stability']==80 and co['crime']==0,
 'known_surveys_monotonic_scientist_alive':set(bh)<=set(ah) and q.scalars(ash['1'])['hitpoints']==375 and q.scalars(ash['1'])['leader']==150994969 and q.scalars(afl['1'])['fleet_stance']=='evasive',
 'native_crisis_level1_menace90_held':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and ac['effective_stockpile']['menace']==90,
 'actual_endpoint_energy_minerals_alloys_positive':all(nets[k]>0 for k in ['energy','minerals','alloys']),
 'unfiltered2670_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks['first_actual_completion15_PASS_SHA_actual0_bound']=(completion['status']=='PASS_TERRAVORE_NATIVE_COLONY_TRAVEL_OBSERVATION_COMPONENT' and len(completion['checks'])==15 and all(v is True for v in completion['checks'].values()) and completion['after_sha256']==h.sha256(run/(completion_stage+'.sav'))=='c0678d32ce243a8f3f037515f20103e6778ac06716d0cd90f7d39e71d48fe31d' and completion_exec['returncode']==0 and completion_exec['helper_sha256']=='6c657a6ab77c5c56f6986327e27422bde1ad93e7fcb8e1a50bd67617d12e368c')
checks['original_single_FAIL_retained_and_bound_when_present']=original_fail_bound
checks={k:bool(v) for k,v in checks.items()};p={'status':'PASS_TERRAVORE_NATIVE_COLONY_TRAVEL_OBSERVATION_V2_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'actual_mother_population':co['actual_pop_sum'],'actual_housing_surplus':co['free_housing'],'actual_amenities_surplus':co['free_amenities'],'actual_colonizer':{'ship':33556279,'exists':bool(ship),'fleet':ss.get('fleet'),'construction_date':ss.get('construction_date'),'coordinate':q.scalars(q.block(q.block(cf,'movement_manager'),'coordinate')),'order':q.scalars(order)},'actual_target1085':target,'actual_original_order_slot':{'id':int(retired_slot[0][0]),'active_object':retired_slot[0][2]},'native_colony_started':colony_started,'known_habitable_planets':known_habitable,'actual_new_survey_holders':newholders,'actual_pending':pending,'actual_active_combat_fleets':combat,'actual_endpoint_nets':{k:str(v) for k,v in nets.items()},'calendar_ready':all(checks.values()) and not pending and not combat,'scope':'Only native paid colonyship/travel/colonization observation with unchanged Mod state and original military. Pending events block next calendar. Endpoint budget is not monthly ledger; no swallow, crisis upgrade,20-year or full-route acceptance.'}
out=run/(after+'-colony-travel-observation-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'pending':pending,'calendar_ready':p['calendar_ready']}),flush=True);assert all(checks.values()),'Original colony travel observation FAIL retained'
