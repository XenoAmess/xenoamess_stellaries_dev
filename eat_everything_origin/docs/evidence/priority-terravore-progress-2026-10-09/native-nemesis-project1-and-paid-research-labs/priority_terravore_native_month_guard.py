"""Read-only actual native month budgeting for the legal Terravore start."""
import json,logging,shutil,sys,zipfile
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
bc,ac=b['countries']['0'],a['countries']['0'];core=a['planets']['7']
resources=('energy','minerals','food','consumer_goods','alloys','unity','trade','influence')
period=ac['budget_categories']['current_month']
net={k:sum((D(str(v.get(k,0))) for v in period['balance'].values()),D(0)) for k in resources}
residuals={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-net[k] for k in resources}
with zipfile.ZipFile(run/(after+'.sav')) as z:text=z.read('gamestate').decode('utf-8-sig')
pending=[q.scalars(v) for k,v,o in q.fields(text) if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={'actual_expected_date':a['date']==date,'original_SHA_pair_bound':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
        'no_new_errors':state['new_error_bytes']==0,'no_country0_pending':not pending,
        'EEP_ledger_held':bc['variables']==ac['variables'],'EEP_flags_held':bc['flags']==ac['flags'],
        'AP_and_traditions_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
        'true_research_available':ac['research_stockpile'] is not None,
        'all_eight_budget_residuals_zero':all(v==0 for v in residuals.values()),
        'same_single_owned_colony':bc['owned_colonies']==ac['owned_colonies']==[0],
        'native_founder_templates_held':bc['native']['founder_species_ref']==ac['native']['founder_species_ref'] and b['species']==a['species'],
        'unique_bound_core_and_original_size':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and 'eep_core' in core['flags'] and core['owner']==core['controller']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==2,
        'core_deposit_held':[(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
        'core_court_capacity_modifiers_held':b['planets']['7']['modifiers']==core['modifiers'],
        'bound_event_targets_held':b['event_targets']==a['event_targets'],
        'no_EEP_source_task':not any(v.get('type')=='situation_eep_devouring' for v in a['situations'].values()),
        'actual_colony_population_consistent':a['colonies']['0']['actual_pop_sum']==sum(a['pop_groups'][str(i)]['size'] for i in a['colonies']['0']['pop_groups']),
        'all_actual_resources_nonnegative':all(D(str(v))>=0 for v in ac['effective_stockpile'].values()),
        'actual_lithoid_mineral_food_upkeep':period['expenses'].get('planet_pops_traits',{}).get('minerals',0)>0 and period['expenses'].get('planet_pops_traits',{}).get('food',0)==0}
proof={'status':'PASS_NATIVE_TERRAVORE_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,
       'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
       'current_month_net':{k:str(v) for k,v in net.items()},'budget_residuals':{k:str(v) for k,v in residuals.items()},
       'population_before':b['colonies']['0']['actual_pop_sum'],'population_after':a['colonies']['0']['actual_pop_sum'],
       'actual_pop_traits_upkeep':period['expenses'].get('planet_pops_traits',{}),
       'negative_primary_net_observed':[k for k,v in net.items() if v<0],
       'scope':'Actual one-month budget and initial native lithoid/core guards. Zero food/consumer-goods stock permitted; not permanent economic closure or full-route acceptance.'}
out=run/(after+'-budget-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original native month failure retained'
