import json,logging,shutil,subprocess,sys
from pathlib import Path
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
start='organic-paid-industry-nextmonth';stage='organic-psionic-unity-2297';date='2297.09.02';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'))
result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/formal_production_native_calendar.py',start,date,stage,'360'],capture_output=True,text=True,encoding='utf-8');(run/(stage+'-driver-output.txt')).write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
if result.returncode:print(result.stdout+result.stderr,flush=True);raise RuntimeError('Preserve failed year, do not repeat days')
a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));bc,c=b['countries']['0'],a['countries']['0'];eb=(run/(stage+'-error-before.log')).read_bytes();ea=(run/(stage+'-error-after.log')).read_bytes();new=ea[len(eb):] if ea.startswith(eb) else ea
checks={'actual_date':a['date']==date,'EEP_ledger_held':bc['variables']==c['variables'],'AP_held':bc['ascension_perks']==c['ascension_perks'],'traditions_held':bc['traditions']==c['traditions'],'theory_held':'tech_psionic_theory' in c['completed_technologies'],
 'native_bank_available':c['research_stockpile'] is not None,'primary_stocks_positive':all(c['effective_stockpile'].get(k,0)>0 for k in ('energy','minerals','food','consumer_goods','unity')),
 'core_once':sum(a['deposits'].get(str(i),{}).get('type')=='d_eep_core' for i in a['planets']['7']['deposits'])==1,
 'no_active_EEP_task':not any(v.get('type')=='situation_eep_devouring' and not v.get('killed') for v in a['situations'].values()),
 'no_early_psi_notice':'eep_psi_notice' not in c['flags'],'no_new_EEP_errors':b'eep.' not in new and b'eep_' not in new}
budget=c['budget_categories']['current_month'];nets={k:sum(Decimal(str(v.get(k,0))) for v in budget['income'].values())-sum(Decimal(str(v.get(k,0))) for v in budget['expenses'].values()) for k in ('energy','minerals','food','consumer_goods','alloys','unity')}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'effective_stockpile':c['effective_stockpile'],'budget_nets':{k:str(v) for k,v in nets.items()},'new_error_bytes':len(new),'scope':'One actual native year of Unity accumulation, no tradition adopted yet.'};h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original year guard failure retained'
