import json,logging,re,shutil,subprocess,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
start='organic-shroud-thread87-corrected';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));baseline=b;result_path=run/'organic-third-latent-devour-final-approach-result.json';assert not result_path.exists()
result={'status':'RUNNING','stages':[],'scope':'Actual latent-family Q13/T32 preterminal calendar only; native events stop further stages. No population, tech, resources, traditions or progress grants.'};h.write_json(result_path,result)
def pending(stage):
 with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return [q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
resources=('energy','minerals','food','consumer_goods','alloys','unity')
assert not pending(start)
for month,date,days,expected_threads in ((23,'2302.12.02',30,90),(27,'2303.04.02',120,102),(31,'2303.08.02',120,114)):
 stage='organic-third-latent-devour-month'+str(month)
 driver=subprocess.run([sys.executable,'_runtime/heart-of-devouring/formal_production_native_calendar.py',start,date,stage,str(days)],capture_output=True,text=True,encoding='utf-8')
 (run/(stage+'-driver-output.txt')).write_text(driver.stdout+driver.stderr,encoding='utf-8')
 if driver.returncode:
  result.update(status='FAILED_STAGE',failed_stage=stage,original_driver_returncode=driver.returncode);h.write_json(result_path,result);print(json.dumps(result),flush=True);raise RuntimeError('Actual calendar failure retained; do not repeat days')
 a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));bc,ac=baseline['countries']['0'],a['countries']['0'];source=a['planets']['1679'];eep=[v for v in a['situations'].values() if v.get('type')=='situation_eep_devouring' and v.get('killed')!='yes'];shroud=a['situations']['33554438'];events=pending(stage)
 eb=(run/(stage+'-error-before.log')).read_bytes();ea=(run/(stage+'-error-after.log')).read_bytes();new=ea[len(eb):] if ea.startswith(eb) else ea
 cv=dict(bc['variables'])
 source_col=a['colonies']['38'];core=[i for i in a['planets']['7']['deposits'] if a['deposits'].get(str(i),{}).get('type')=='d_eep_core']
 checks={'actual_date':a['date']==date,'source_owner_controller_held':source['owner']==source['controller']==0,'Q13_T32_held':source['variables'].get('eep_q')==13 and source['variables'].get('eep_months')==32,'source_active': 'eep_active' in source['flags'],'one_native_EEP_progress_exact':len(eep)==1 and eep[0]['progress']==month and eep[0]['target']['id']==1679,'all_original_EEP_variables_held_no_early_credit':ac['variables']==cv,'EEP_country_flags_held':ac['flags']==bc['flags'],'AP_traditions_held':ac['ascension_perks']==bc['ascension_perks'] and ac['traditions']==bc['traditions'],'owned_colonies_held':ac['owned_colonies']==bc['owned_colonies'],'latent_family_definitions_held':all(a['species'][k]==baseline['species'][k] for k in ('102','103')),'actual_source_all_latent_family':all(a['pop_groups'][str(i)]['key']['species'] in (102,103) for i in source_col['pop_groups']),'mother_unique_core_owned':len(core)==1 and sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and a['planets']['7']['owner']==a['planets']['7']['controller']==0,'primary_stocks_positive':all(ac['effective_stockpile'][k]>0 for k in resources),'true_research_bank_available':ac['research_stockpile'] is not None,'threads_exact_actual_budget':ac['effective_stockpile']['astral_threads']==expected_threads,'threads_reserve_at_least_80':ac['effective_stockpile']['astral_threads']>=80,'shroud_same_stage_approach':shroud['stage']==0 and shroud['approach']=='approach_situation_breach_shroud_nothing','no_early_psionic_completion':ac['variables']['eep_psi']==0,'no_new_EEP_errors':not re.search(rb'eep[._]',new,re.I)}
 nets={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
 proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'month':month,'date':a['date'],'before_sha256':b['save_sha256'],'recovery_baseline_sha256':baseline['save_sha256'],'after_sha256':a['save_sha256'],'source_population':source_col['actual_pop_sum'],'mother_population':a['colonies']['0']['actual_pop_sum'],'actual_stocks':ac['effective_stockpile'],'actual_primary_net':{k:str(v) for k,v in nets.items()},'negative_primary_net':[k for k,v in nets.items() if v<0],'shroud':shroud,'source_variables':source['variables'],'pending_native_events':events,'new_error_bytes':len(new),'scope':'Natural population growth continues; full original EEP report variables are held and actual situation progress is checked separately. Food deficit recorded against positive reserve; terminal settlement still pending.'}
 h.write_json(run/(stage+'-task-guard-proof.json'),proof);result['stages'].append({'stage':stage,'proof':proof});h.write_json(result_path,result);print(json.dumps(proof),flush=True)
 if not all(checks.values()):result.update(status='FAILED_GUARDS',failed_stage=stage);h.write_json(result_path,result);raise RuntimeError('Original guard failure retained')
 if month==23:
  budget=subprocess.run([sys.executable,'_runtime/heart-of-devouring/postrelease_organic_monthly_budget_proof.py',start,stage,date,'3.75','0'],capture_output=True,text=True,encoding='utf-8');(run/(stage+'-budget-driver-output.txt')).write_text(budget.stdout+budget.stderr,encoding='utf-8')
  if budget.returncode:result.update(status='FAILED_NATIVE_MONTH_BUDGET',current_stage=stage);h.write_json(result_path,result);raise RuntimeError('Original one-month budget failure retained; no replay')
 b=a;start=stage
 if events:result.update(status='STOP_PENDING_NATIVE_EVENT',current_stage=start);h.write_json(result_path,result);break
else:result.update(status='STOP_BEFORE_LAST_SETTLEMENT_MONTH',current_stage=start);h.write_json(result_path,result)
