"""Read-only native Terravore active-month checkpoints; never settles or edits saves."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,date,raw_days,raw_progress,raw_damage=sys.argv[1:]
days,progress,damage=map(int,(raw_days,raw_progress,raw_damage))
assert 1<=days<=360 and 0<=progress<48
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'))
bc,ac=b['countries']['0'],a['countries']['0'];core=a['planets']['7'];source=a['planets']['124']
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text(encoding='utf-8'))
state=json.loads((run/(after+'-state.json')).read_text(encoding='utf-8'))
with zipfile.ZipFile(run/(after+'.sav')) as z:raw=z.read('gamestate').decode('utf-8-sig')
pending=[q.scalars(v) for k,v,o in q.fields(raw) if k=='player_event' and o and q.scalars(v).get('country')==0]
sits={i:s for i,s in a['situations'].items() if s.get('type')=='situation_eep_devouring'}
gov=q.scalars(ac['government']);founder=str(ac['native']['founder_species_ref']);species=a['species'][founder]
start=json.loads((run/'terravore-second-native-devour-start.audit.json').read_text('utf-8'));startproof=json.loads((run/'terravore-second-native-devour-start-second-start-proof.json').read_text('utf-8'));ledger=start['countries']['0']['variables']
elapsed=lambda s:sum(x*y for x,y in zip(map(int,s.split('.')),[360,30,1]))
checks={'actual_date_and_days':a['date']==date and elapsed(a['date'])-elapsed(b['date'])==days,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_calendar_receipt':receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==date and receipt['days']==days,
 'no_new_error':state['new_error_bytes']==0 and (run/(after+'-error-after.log')).read_bytes()==(run/'terravore-second-native-devour-start-error-after.log').read_bytes(),
 'no_country0_pending':not pending,
 'initial_ledger_no_early_credit_manufacture':bc['variables']==ac['variables']==ledger,
 'no_early_EEP_notice':{k:v for k,v in ac['flags'].items() if k.startswith('eep_')}=={k:v for k,v in start['countries']['0']['flags'].items() if k.startswith('eep_')},
 'exact_original_task_and_progress':set(sits)=={'16777227'} and all(s['country']==0 and s['progress']==progress and s['approach']=='eep_devour_approach' and s['target']['type']=='planet' and s['target']['id']==124 for s in sits.values()),
 'no_duplicate_native_situation':not any(s.get('type')=='situation_terravore_consume_planet' for s in a['situations'].values()),
 'source_Q20_T48_seed_record_held':source['variables']=={'eep_q':20,'eep_months':48,'eep_old_damage':0,'eep_seed_existing':102,'eep_seed_need':-2},
 'source_still_owned_colony24':source['owner']==source['controller']==0 and source['colony']==24 and 24 in ac['owned_colonies'],
 'source_active_native_flags':all(k in source['flags'] for k in ['eep_active','eep_native','being_devoured','eep_owned_colony_event','colony_event']),
 'no_early_settlement_flags':not any(k in source['flags'] for k in ['eep_pending','eep_credit_done','eep_return_done','eep_destroy_done','eep_bites_done']),
 'source_native_modifier_once':source['modifiers'].count('modifier="being_devoured_modifier"')==1,
 'legal_original_government':all(gov[k]==q.scalars(bc['government'])[k] for k in ['type','authority','origin']) and gov['type']=='gov_devouring_swarm' and gov['authority']=='auth_hive_mind' and gov['origin']=='origin_heart_of_devouring',
 'legal_original_civics':[q.unquote(t) for t,_,_ in q.tokens(q.block(ac['government'],'civics'))]==['civic_hive_devouring_swarm','civic_hive_ascetic'],
 'original_lithoid_hive_founder':ac['native']['founder_species_ref']==bc['native']['founder_species_ref'] and species['class']=='LITHOID' and 'trait_lithoid' in species['traits'] and 'trait_hive_mind' in species['traits'],
 'paid_AP_and_traditions_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'core_owner_colony_and_unique_flag':core['owner']==core['controller']==0 and core['colony']==0 and sum('eep_core' in p['flags'] for p in a['planets'].values())==1,
 'core_size18_capacity6':core['planet_size']==18 and core['variables']['eep_capacity_value']==6,
 'core_capacity_once_permanent':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*6\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
 'court_once_permanent':core['modifiers'].count('modifier="eep_court"')==1 and 'days=-1' in core['modifiers'],
 'core_deposit_held':[(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'original_global_targets_held':b['event_targets']==a['event_targets'],
 'economic_stocks_nonnegative':all(D(str(v))>=0 for v in ac['effective_stockpile'].values())}
source_damage={str(i):a['deposits'].get(str(i)) for i in source['deposits'] if a['deposits'].get(str(i),{}).get('type')=='d_lithoid_devastation'}
checks['actual_source_native_damage_count']=len(source_damage)==damage

checks.update({
 'bound_original_second_start_pass':startproof['status']=='PASS_NATIVE_TERRAVORE_START_COMPONENT' and all(startproof['checks'].values()) and startproof['after_sha256']==start['save_sha256']==h.sha256(run/'terravore-second-native-devour-start.sav'),
 'original_first_shattered_source_held':a['planets']['90']==b['planets']['90'] and not any(g['planet']==15 and g['size']>0 for g in a['pop_groups'].values()),
 'only_original_mother_and_second_source_owned':bc['owned_colonies']==ac['owned_colonies']==[0,24],
 'mother_exact19_paid_districts_capacity24':{a['districts'][str(i)]['type']:a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts']}=={'district_hive':5,'district_mining':10,'district_generator':4} and a['colonies']['0']['districts']==b['colonies']['0']['districts'] and all(a['districts'][str(i)]==b['districts'][str(i)] for i in b['colonies']['0']['districts']) and 19<=core['planet_size']+core['variables']['eep_capacity_value']==24,
 'mother_paid_mining2000_generator800_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)]),
 'second_source_actual_positive_founder_population':a['colonies']['24']['actual_pop_sum']>0 and all(g['key']['species']==3321888769 for g in a['pop_groups'].values() if g['planet']==24 and g['size']>0)
})

net={k:str(sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))) for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']}
proof={'status':'PASS_NATIVE_TERRAVORE_ACTIVE_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_situations':sits,'actual_source_damage':source_damage,'source_physical_state':source,'population':{str(i):a['colonies'][str(i)]['actual_pop_sum'] for i in ac['owned_colonies']},'stockpile':ac['effective_stockpile'],'current_month_net':net,'newly_completed_technologies':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),'research_queues':ac['research_queues'],'pending':pending,'scope':'Second source124 active effective-month, native bite damage and no early EEP reward; original source90 held. Not exact multi-month random reward reconciliation, settlement, reload or full route acceptance.'}
out=run/(after+'-second-active-month-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original active-month FAIL retained; no automatic next segment'
