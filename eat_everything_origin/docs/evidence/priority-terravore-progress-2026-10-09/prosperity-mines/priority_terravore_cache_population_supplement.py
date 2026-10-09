"""Strictly bound actual population hold and three observed cached fields."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-paid-economy-month';after='terravore-budget-cache-day2'
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'));p=json.loads((run/(after+'-budget-observation.json')).read_text('utf-8'))
allowed={'housing_usage','crime','power'}
checks={'original_only_cache_group_FAIL':p['status']=='FAIL' and [k for k,v in p['checks'].items() if not v]==['actual_population_groups_and_jobs_held'] and sum(p['checks'].values())==6,
 'original_SHA_pair_bound':h.sha256(run/(before+'.sav'))==b['save_sha256']==p['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==p['after_sha256'],
 'all_actual_jobs_raw_held':b['pop_jobs']==a['pop_jobs'],
 'all_other_group_raw_fields_held':set(a['pop_groups'])==set(b['pop_groups']) and all(({k:v for k,v in a['pop_groups'][i].items() if k not in allowed}=={k:v for k,v in c.items() if k not in allowed}) if i=='1' else a['pop_groups'][i]==c for i,c in b['pop_groups'].items()),
 'exact_three_observed_cache_changes':b['pop_groups']['1']['housing_usage']==2508 and a['pop_groups']['1']['housing_usage']==2514 and all(b['pop_groups']['1'][k]==25.08 and a['pop_groups']['1'][k]==25.14 for k in ['crime','power']),
 'cache_after_matches_existing_actual_size':a['pop_groups']['1']['size']==b['pop_groups']['1']['size']==a['pop_groups']['1']['housing_usage'] and all(a['pop_groups']['1'][k]==a['pop_groups']['1']['size']/100 for k in ['crime','power'])}
proof={'status':'PASS_SCOPED_POPULATION_CACHE_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'group_before_after':[b['pop_groups']['1'],a['pop_groups']['1']],'scope':'Actual population held, precisely three native group cache changes only. Original observation and monthly FAIL preserved.'}
out=run/(after+'-population-cache-supplement.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values())
