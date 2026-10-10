"""Native paid foundry actual completion with exact original fleet/survey components."""
import sys,json,logging,shutil,zipfile,re
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-postdrone-outpost-paid';after='terravore-native-forge-completion90'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bfl,afl=objs(br['fleet']),objs(ar['fleet']);bsh,ash=objs(br['ships']),objs(ar['ships']);bb,ab=objs(br['buildings']),objs(ar['buildings']);bz,az=objs(br['zones']),objs(ar['zones'])
pre=json.loads((run/(before+'-new-outpost-payment-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'));rc=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
survivors=[33556208,33556207,50332878,1807,1810];own=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(acr,'fleets_manager'),'owned_fleets'))));mil={i:q.ids(q.block(afl[str(i)],'ships')) for i in own if q.scalars(afl[str(i)])['ship_class']=='shipclass_military'}
holders=lambda cr:re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(cr,'surveyed_deposit_holders'))
bh,ah=holders(bcr),holders(acr);newholders=[i for i in ah if i not in bh];co=a['colonies']['0'];nets={k:sum(D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys']}
checks={
 'original_SHA_pair_actual_dates':b['date']=='2263.11.17' and a['date']=='2264.02.17' and a['save_sha256']=='cbb0c6cf70e9d49d56b1aa8dc9e6e0c007ad2a405166bd631eeb81d6b9a1f5a2' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior17_new_outpost_payment_PASS_actual0':pre['status']=='PASS_TERRAVORE_POSTDRONE_NEW_OUTPOST_PAYMENT_COMPONENT' and len(pre['checks'])==17 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='795f811d8389aa17d5b0bc189c53d32191de308fcca695af8a2f85ad97cb90cc',
 'unique90_calendar_actual0':rc['status']=='CALENDAR_CONFIRMED' and rc['days']==90 and rc['start_date']==b['date'] and rc['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'original_paid_order_completed_and_mother_queue_empty':q.scalars(q.block(q.block(ar['construction'],'item_mgr'),'items')).get('83886102')=='none' and not q.block(q.block(ar['construction'],'queues'),'0').strip(),
 'original_warren_removed_new120_foundry_same_slot':q.scalars(ar['buildings']).get('2')=='none' and q.scalars(ab['120'])=={'type':'building_foundry_1','position':2} and q.ids(q.block(az['0'],'buildings'))==[33554466,1,120,33554454,46,48],
 'all_other_original_buildings_zones_and_districts_held':all(bz[i]==az[i] for i in ['2','61']) and all(bb[str(i)]==ab[str(i)] for i in [33554466,1,33554454,46,48,16777251,83886120,16777323,83,16777258,86]) and all(q.block(br['districts'],i)==q.block(ar['districts'],i) for i in ['1','2','3']),
 'actual200_fabricator_and_original_workers_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('fabricator',200),('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2400),('technician_drone',1200)]),
 'native1500_housing_loss_surplus2530_stability80':b['colonies']['0']['total_housing']==14400 and co['total_housing']==12900 and co['housing_usage']==10370 and co['free_housing']==2530 and co['stability']==80 and co['crime']==0,
 'native_amenities_actual_positive_surplus':co['amenities']==24588.9 and co['amenities_usage']==4708.6 and co['free_amenities']==19880.3,
 'population10370_natural_last_month6':co['actual_pop_sum']==10370 and q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':10364,'growth':6},
 'EEP_species_targets_capacity_fullpsi_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and b['species']==a['species'] and b['event_targets']==a['event_targets'] and a['planets']['7']['modifiers']==b['planets']['7']['modifiers'] and ac['owned_colonies']==[0] and not a['situations'],
 'mother_no_new_bombardment_or_damage':a['planets']['7']['bombardment_damage']==b['planets']['7']['bombardment_damage']==0 and a['planets']['7']['last_bombardment']==b['planets']['7']['last_bombardment']=='2261.07.03',
 'actual8_original_military_ships_no_active_combat':mil=={788:[1816,1817],33555013:[33555519],33555034:survivors} and all(bfl[i]==afl[i] for i in ['788','33555013']) and q.scalars(acr)['fleet_size']==40 and all(not q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip() for i in own),
 'main_native_hull_regeneration_only_still_returning139':q.scalars(afl['33555034'])['hit_points']==1055.84918 and [q.scalars(ash[str(i)])['hitpoints'] for i in survivors]==[270,176.28034,171.24532,270,168.32356] and all(q.block(bsh[str(i)],'ship_design_implementation')==q.block(ash[str(i)],'ship_design_implementation') and q.scalars(bsh[str(i)])['construction_date']==q.scalars(ash[str(i)])['construction_date'] for i in survivors) and q.block(bfl['33555034'],'current_order')==q.block(afl['33555034'],'current_order') and q.scalars(q.block(q.block(afl['33555034'],'movement_manager'),'coordinate'))['origin']==139,
 'paid_outpost_order_held_constructor_alive80':q.block(bfl['2'],'current_order')==q.block(afl['2'],'current_order') and q.ids(q.block(afl['2'],'ships'))==[2] and q.scalars(ash['2'])['hitpoints']==375 and q.scalars(q.block(q.block(afl['2'],'movement_manager'),'coordinate'))['origin']==80 and q.ids(q.block(q.block(ar['galactic_object'],'97'),'starbases'))==[4294967295],
 'exact3_additional_known_surveys_current914':len(bh)==278 and len(ah)==281 and set(bh)<=set(ah) and newholders==[('0','913'),('0','916'),('0','917')] and q.scalars(q.block(q.block(afl['1'],'current_order'),'survey_planet_order'))['progress']==4.6 and q.scalars(q.block(q.block(q.block(afl['1'],'current_order'),'survey_planet_order'),'deposit_holder'))=={'type':0,'id':914} and q.scalars(ash['1'])['hitpoints']==375,
 'native_menace90_level1_project_state_held':ac['effective_stockpile']['menace']==90 and q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.block(bcr,'special_project')==q.block(acr,'special_project'),
 'actual_cached_budget_recorded_not_forge_output_claim':nets=={'energy':D('36.265'),'minerals':D('30.6415'),'unity':D('149.8855'),'alloys':D('0.32')},
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered2670_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks={k:bool(v) for k,v in checks.items()};p={'status':'PASS_TERRAVORE_NATIVE_PAID_FORGE_COMPLETION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_foundry':120,'actual_fabricators':200,'actual_housing_surplus':2530,'current_month_cached_nets':{k:str(v) for k,v in nets.items()},'calendar_ready':all(checks.values()),'scope':'Actual paid foundry completion, original8 ships and native task continuation. Full post-completion month ledger still pending; no outpost, repair-base arrival, level2 or route-complete claim.'}
out=run/(after+'-forge-completion-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original forge completion FAIL retained'
