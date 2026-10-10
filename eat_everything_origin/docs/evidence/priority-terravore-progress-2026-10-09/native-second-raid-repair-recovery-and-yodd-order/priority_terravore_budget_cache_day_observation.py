"""Read-only next-day cache observation; preserves the failed original month."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-paid-economy-month';after='terravore-budget-cache-day2'
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'));orig=json.loads((run/(before+'-paid-economy-month-proof.json')).read_text('utf-8'))
checks={'actual_unique_one_day':b['date']=='2212.07.01' and a['date']=='2212.07.02' and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==1 and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'original_month_FAIL_retained':orig['status']=='FAIL' and [k for k,v in orig['checks'].items() if not v]==['all_eight_actual_budget_residuals_zero'],
 'all_actual_resources_and_true_banks_held':bc['effective_stockpile']==ac['effective_stockpile'],
 'actual_population_groups_and_jobs_held':b['pop_groups']==a['pop_groups'] and b['pop_jobs']==a['pop_jobs'],
 'full_EEP_and_original_districts_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and b['districts']==a['districts'],
 'error_original_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-postsettlement-month-error-after.log').read_bytes()}
p={'status':'PASS_SCOPED_NEXT_DAY_BUDGET_OBSERVATION' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'original_month_residuals':orig['actual_budget_residuals'],'budget_categories_before_after':[bc['budget_categories'],ac['budget_categories']],'scope':'One native day, no resource/population changes and actual budget observation only; does not turn the original monthly FAIL into PASS or prove a universal native cache rule.'}
out=run/(after+'-budget-observation.json');assert not out.exists();h.write_json(out,p);print(json.dumps({k:v for k,v in p.items() if k!='budget_categories_before_after'}),flush=True);assert all(checks.values())
