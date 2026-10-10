"""Read-only annual native campaign observations and initial-ledger guards."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,date=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'))
a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'))
state=json.loads((run/(after+'-state.json')).read_text(encoding='utf-8'))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text(encoding='utf-8'))
bc,ac=b['countries']['0'],a['countries']['0'];core=a['planets']['7']
with zipfile.ZipFile(run/(after+'.sav')) as z:text=z.read('gamestate').decode('utf-8-sig')
fields=list(q.fields(text));roots={k:v for k,v,o in fields if o}
pending=[q.scalars(v) for k,v,o in fields if k=='player_event' and o and q.scalars(v).get('country')==0]
gov=q.scalars(ac['government']);founder=str(ac['native']['founder_species_ref']);species=a['species'][founder]
forbidden={'ap_engineered_evolution','ap_the_flesh_is_weak','ap_synthetic_evolution','ap_synthetic_age','ap_organo_machine_interfacing','ap_organo_machine_interfacing_assimilator'}
expected={'eep_c':0,'eep_g':0,'eep_d':2,'eep_made':0,'eep_worlds':0,'eep_stage':0,
          'eep_last_capacity':0,'eep_last_return':0,'eep_last_manufactured':0,'eep_fleet_stage':0}
checks={'expected_native_year_date':a['date']==date,
        'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
        'actual_native360_receipt':receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==date and receipt['days']==360,
        'no_new_errors':state['new_error_bytes']==0,'no_country0_pending':not pending,
        'initial_EEP_ledger_held':bc['variables']==ac['variables']==expected,
        'original_EEP_flags_held':bc['flags']==ac['flags'],
        'same_legal_government_authority_origin':all(gov[k]==q.scalars(bc['government'])[k] for k in ['type','authority','origin']) and gov['type']=='gov_devouring_swarm' and gov['authority']=='auth_hive_mind' and gov['origin']=='origin_heart_of_devouring',
        'same_legal_civic_tokens':[q.unquote(t) for t,_,_ in q.tokens(q.block(ac['government'],'civics'))]==['civic_hive_devouring_swarm','civic_hive_ascetic'],
        'original_lithoid_hive_founder':ac['native']['founder_species_ref']==bc['native']['founder_species_ref'] and species['class']=='LITHOID' and 'trait_lithoid' in species['traits'] and 'trait_hive_mind' in species['traits'],
        'no_incompatible_AP':not forbidden.intersection(ac['ascension_perks']),
        'unique_original_core_owned':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and 'eep_core' in core['flags'] and core['owner']==core['controller']==0 and core['colony']==0,
        'original_size_and_extra2':core['planet_size']==18 and core['variables']['eep_capacity_value']==2,
        'one_original_core_deposit':[(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
        'one_permanent_capacity2':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*2\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
        'one_permanent_court':core['modifiers'].count('modifier="eep_court"')==1 and bool(re.search(r'modifier\s*=\s*"eep_court"\s+days\s*=\s*-1',core['modifiers'])),
        'bound_original_event_target':len([v for v in a['event_targets'] if v['name']=='eep_core0' and v['type']=='planet' and v['id']==7])==1,
        'no_EEP_source_task_yet':not any(v.get('type')=='situation_eep_devouring' for v in a['situations'].values()),
        'actual_resources_nonnegative':all(D(str(v))>=0 for v in ac['effective_stockpile'].values()),
        'native_true_research_available':ac['research_stockpile'] is not None}
period=ac['budget_categories']['current_month'];resources=('energy','minerals','food','consumer_goods','alloys','unity','trade','influence')
net={k:str(sum((D(str(v.get(k,0))) for v in period['balance'].values()),D(0))) for k in resources}
population={str(i):a['colonies'][str(i)]['actual_pop_sum'] for i in ac['owned_colonies']}
proof={'status':'PASS_NATIVE_TERRAVORE_ANNUAL_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,
       'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_current_month_net':net,
       'actual_stockpile':ac['effective_stockpile'],'actual_owned_population':population,
       'actual_traditions':ac['traditions'],'actual_AP':ac['ascension_perks'],
       'completed_technology_count':len(ac['completed_technologies']),
       'newly_completed_technologies':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),
       'actual_research_queues':ac['research_queues'],
       'deposits_removed':{k:v for k,v in b['deposits'].items() if k not in a['deposits']},
       'deposits_added':{k:v for k,v in a['deposits'].items() if k not in b['deposits']},
       'source_colony_candidates':[i for i in ac['owned_colonies'] if i!=0],
       'scope':'Actual native annual initial-ledger guard, not multi-month budget reconciliation, pure population growth, natural swallowing or full-route acceptance.'}
out=run/(after+'-annual-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original annual component failure retained; no automatic next year'
