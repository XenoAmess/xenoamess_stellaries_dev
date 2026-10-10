"""Independent full native foundry month: state boundary, eight stocks and actual jobs."""
import sys,json,logging,shutil,zipfile,re
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-forge-completion90';after='terravore-native-forge-full-month'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bfl,afl=objs(br['fleet']),objs(ar['fleet']);bsh,ash=objs(br['ships']),objs(ar['ships']);pre=json.loads((run/(before+'-forge-completion-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'));rc=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']}
residual={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-v for k,v in net.items()}
proj=lambda cr:{q.scalars(v)['id']:v for k,v,o in q.fields(q.block(cr,'events')) if k=='special_project' and o};bp,ap=proj(bcr),proj(acr)
growth=q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'));co=a['colonies']['0'];survivors=[33556208,33556207,50332878,1807,1810]
own=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(acr,'fleets_manager'),'owned_fleets'))));mil={i:q.ids(q.block(afl[str(i)],'ships')) for i in own if q.scalars(afl[str(i)])['ship_class']=='shipclass_military'}
cur=ac['budget_categories']['current_month'];checks={
 'original_SHA_pair_one_full_month':b['date']=='2264.02.17' and a['date']=='2264.03.17' and a['save_sha256']=='69ba768f0e26f86071194b7a171b80204b20551011c78079ede250786bfb7d17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior20_forge_completion_PASS_actual0':pre['status']=='PASS_TERRAVORE_NATIVE_PAID_FORGE_COMPLETION_COMPONENT' and len(pre['checks'])==20 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='b468d25585fa29c761fbc608a1fd00417e78d96ad383e7114eb1df88d4a62355',
 'unique30_calendar_actual0':rc['status']=='CALENDAR_CONFIRMED' and rc['days']==30 and rc['start_date']==b['date'] and rc['date']==a['date'] and json.loads((run/(after+'-calendar-execution.json')).read_text('utf-8'))['returncode']==0,
 'eight_independent_real_stock_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'last_month_exact_prior_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'actual_positive_energy_minerals_alloys_and_exact_nets':net=={'energy':D('36.265'),'minerals':D('16.9075'),'food':D(0),'consumer_goods':D(0),'alloys':D('10.832'),'unity':D('149.88550'),'trade':D('87.75428'),'influence':D('6.9753')},
 'actual_forge_income10_512_alloys_upkeep13_68_minerals':cur['income']['planet_metallurgists']=={'alloys':10.512} and cur['expenses']['planet_metallurgists']=={'minerals':13.68} and 'planet_metallurgists' not in bc['budget_categories']['current_month']['income'],
 'same_building_upkeep27_generator5_4_mining10_8':cur['expenses']['planet_buildings']=={'energy':27} and cur['expenses']['planet_districts_generator']=={'energy':5.4} and cur['expenses']['planet_districts_mining']=={'energy':10.8},
 'all_mother_buildings_districts_zones_raw_held':all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','61']) and all(q.block(br['districts'],i)==q.block(ar['districts'],i) for i in ['1','2','3']) and all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for zid in ['0','2','61'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))),
 'fabricator200_and_original_all_workers_full':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('fabricator',200),('coordinator',2000),('logistics_drone',500),('telepath_drone',200),('calculator_physicist',300),('calculator_biologist',300),('calculator_engineer',300),('mining_drone',2400),('technician_drone',1200)]),
 'population_only_native_growth7':growth=={'month_start_size':10370,'growth':7} and co['actual_pop_sum']==10377,
 'positive_native_housing_amenities_stability':co['total_housing']==12900 and co['free_housing']==2523 and co['free_amenities']==19913.9 and co['stability']==80 and co['crime']==0,
 'EEP_species_targets_fullpsi_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and b['species']==a['species'] and b['event_targets']==a['event_targets'] and b['planets']['7']['modifiers']==a['planets']['7']['modifiers'] and ac['owned_colonies']==[0] and not a['situations'],
 'actual_native_project1_2_events_objects_raw_held':set(bp)==set(ap)=={1,2,3} and bp[1]==ap[1] and bp[2]==ap[2] and q.scalars(ap[2])['special_project']=='CRISIS_SPECIAL_PROJECT_PSIONIC_1' and q.scalars(ap[2])['status']=='completed',
 'previous90_project1_2_independent_exact_supplement':all(q.scalars(v)['special_project'] in {'CLOUDS_PROJECT','CRISIS_SPECIAL_PROJECT_PSIONIC_1'} for i,v in bp.items() if i in {1,2}) and q.scalars(bp[2])['status']=='completed',
 'native_debris3_countdown30_only':q.scalars(bp[3])=={'id':3,'days_left':1709,'debris':318767104} and q.scalars(ap[3])=={'id':3,'days_left':1679,'debris':318767104},
 'native_crisis1_menace90_completion_flags_held':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and ac['effective_stockpile']['menace']==90 and all(q.scalars(q.block(acr,'flags')).get(k)==q.scalars(q.block(bcr,'flags')).get(k)==63355224 for k in ['crisis_special_project_1_complete','first_special_project_finished']),
 'true_society_bank_native_income_times_research_speed':D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))==D('34.79213') and ac['research_stockpile']['physics_research']==ac['research_stockpile']['engineering_research']==0,
 'original8_ships_no_new_combat_or_loss':mil=={788:[1816,1817],33555013:[33555519],33555034:survivors} and all(bfl[i]==afl[i] for i in ['788','33555013']) and all(not q.block(q.block(afl[str(i)],'combat'),'in_combat_with').strip() for i in own),
 'main_return_order_held_natural_hull_gain60_75_total':q.block(bfl['33555034'],'current_order')==q.block(afl['33555034'],'current_order') and q.scalars(afl['33555034'])['hit_points']==1116.59918 and q.scalars(q.block(q.block(afl['33555034'],'movement_manager'),'coordinate'))['origin']==188 and all(q.block(bsh[str(i)],'ship_design_implementation')==q.block(ash[str(i)],'ship_design_implementation') for i in survivors),
 'constructor_paid_order_held_alive_not_yet_built':q.block(bfl['2'],'current_order')==q.block(afl['2'],'current_order') and q.scalars(ash['2'])['hitpoints']==375 and q.ids(q.block(q.block(ar['galactic_object'],'97'),'starbases'))==[4294967295],
 'mother_bombardment_zero_last_date_held':a['planets']['7']['bombardment_damage']==b['planets']['7']['bombardment_damage']==0 and a['planets']['7']['last_bombardment']==b['planets']['7']['last_bombardment']=='2261.07.03',
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered2670_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
checks={k:bool(v) for k,v in checks.items()};p={'status':'PASS_TERRAVORE_NATIVE_FORGE_FULL_MONTH_LEDGER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_native_growth':growth,'actual_current_month_net':{k:str(v) for k,v in net.items()},'actual_budget_residuals':{k:str(v) for k,v in residual.items()},'actual_current_month_categories':cur,'actual_last_month_categories':ac['budget_categories']['last_month'],'calendar_ready':all(checks.values()),'scope':'One full actual foundry month, actual fabrication and eight stocks closed. Events-container project2 independently read; no completed fleet repair, outpost, level2 or full-route claim.'}
out=run/(after+'-forge-full-month-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original full foundry month FAIL retained'
