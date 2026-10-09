import json,logging,shutil,subprocess,sys
from pathlib import Path
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
start='organic-mother-mine3-ordered';initial=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));base=initial['countries']['0'];rows=[]
assert base['research_stockpile'] is not None
for month in range(37,43):
 date='2295.'+str(month-36).zfill(2)+'.02';stage='organic-psionic-theory-month'+str(month)
 result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/formal_production_native_calendar.py',start,date,stage,'30'],capture_output=True,text=True,encoding='utf-8')
 (run/(stage+'-driver-output.txt')).write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
 if result.returncode:
  h.write_json(run/'organic-theory-endpoint-result.json',{'status':'FAILED_STAGE','stage':stage,'completed':rows,'returncode':result.returncode});print(result.stdout+result.stderr,flush=True);raise RuntimeError('Do not repeat calendar days')
 a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));c=a['countries']['0'];mother=a['planets']['7'];completed='tech_psionic_theory' in c['completed_technologies']
 eb=(run/(stage+'-error-before.log')).read_bytes();ea=(run/(stage+'-error-after.log')).read_bytes();new=ea[len(eb):] if ea.startswith(eb) else ea
 checks={'actual_date':a['date']==date,'EEP_ledger_same':c['variables']==base['variables'],'AP_same':c['ascension_perks']==base['ascension_perks'],
 'core_once':sum(a['deposits'].get(str(i),{}).get('type')=='d_eep_core' for i in mother['deposits'])==1,
 'source_shattered':a['planets']['1855'].get('planet_class')=='pc_shattered',
 'no_EEP_task':not any(v.get('type')=='situation_eep_devouring' and not v.get('killed') for v in a['situations'].values()),
 'schema2_native_bank_available':a['audit_schema_version']==2 and c['research_stockpile'] is not None,
 'primary_stocks_positive':all(c['effective_stockpile'].get(k,0)>0 for k in ('food','consumer_goods','minerals','energy','unity')),
 'theory_selected_or_native_complete':completed or 'tech_psionic_theory' in c['research_queues'].get('society_queue',''),
 'no_early_mine_completion':a['districts']['2']['level']==2,
 'no_early_artisan_jobs':any(v.get('type')=='artisan' and v.get('planet')==0 and v.get('max_workforce')==1400 for v in a['pop_jobs'].values()),
 'no_new_EEP_errors':b'eep.' not in new and b'eep_' not in new}
 budget=c['budget_categories']['current_month'];nets={k:sum(Decimal(str(v.get(k,0))) for v in budget['income'].values())-sum(Decimal(str(v.get(k,0))) for v in budget['expenses'].values()) for k in ('energy','minerals','food','consumer_goods','alloys','unity')}
 row={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','month':month,'date':date,'save_sha256':a['save_sha256'],'auditor_sha256':a['audit_tool_sha256'],'checks':checks,'theory_completed':completed,'society_queue':c['research_queues'].get('society_queue',''),'per_tech_progress':c['research_progress_by_tech'],'actual_research_bank':c['research_stockpile'],'raw_mirror':{k:c['stockpile'].get(k) for k in c['research_stockpile']},'effective_stockpile':c['effective_stockpile'],'budget_nets':{k:str(v) for k,v in nets.items()},'new_error_bytes':len(new)}
 h.write_json(run/(stage+'-proof.json'),row);rows.append(row);print(json.dumps(row),flush=True);h.write_json(run/'organic-theory-endpoint-result.json',{'status':'IN_PROGRESS' if all(checks.values()) else 'FAILED_GUARD','completed':rows});assert all(checks.values()),'Original endpoint guard FAIL retained';start=stage
 if completed:
  h.write_json(run/'organic-theory-endpoint-result.json',{'status':'NATIVE_TECH_COMPLETED','completed':rows,'scope':'Native theory only; full psionic tradition and Shroud endpoint pending.'});break
else:h.write_json(run/'organic-theory-endpoint-result.json',{'status':'NOT_COMPLETE_AT_MONTH42','completed':rows})
