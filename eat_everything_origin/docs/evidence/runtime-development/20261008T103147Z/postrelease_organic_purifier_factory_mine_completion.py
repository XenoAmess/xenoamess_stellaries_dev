import json,logging,shutil,subprocess,sys,zipfile
from decimal import Decimal
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
start='organic-psionic-theory-month40';initial=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));base=initial['countries']['0'];rows=[]
def native(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 c=q.block(t,'construction');queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0')
 return {'zone0':q.ids(q.block(q.block(q.block(t,'zones'),'0'),'buildings')),
         'buildings':{k:q.scalars(v) for k,v,o in q.fields(q.block(t,'buildings')) if o},
         'queue':q.ids(q.block(queue,'items'))}
original=native(start)
for phase,date,days in (('factory','2295.12.02',240),('mine3','2296.08.02',240),('nextmonth','2296.09.02',30)):
 stage='organic-paid-'+phase+'-completed' if phase!='nextmonth' else 'organic-paid-industry-nextmonth'
 b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'))
 result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/formal_production_native_calendar.py',start,date,stage,str(days)],capture_output=True,text=True,encoding='utf-8');(run/(stage+'-driver-output.txt')).write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
 if result.returncode:
  h.write_json(run/'organic-paid-industry-completion-result.json',{'status':'FAILED_STAGE','stage':stage,'completed':rows,'returncode':result.returncode});print(result.stdout+result.stderr,flush=True);raise RuntimeError('Do not repeat calendar')
 a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));c=a['countries']['0'];state=native(stage);new_buildings=[i for i in state['zone0'] if i not in original['zone0']]
 def job(kind):return next(v for v in a['pop_jobs'].values() if v.get('planet')==0 and v.get('type')==kind)
 eb=(run/(stage+'-error-before.log')).read_bytes();ea=(run/(stage+'-error-after.log')).read_bytes();new=ea[len(eb):] if ea.startswith(eb) else ea
 checks={'actual_date':a['date']==date,'EEP_ledger_same':c['variables']==base['variables'],'AP_same':c['ascension_perks']==base['ascension_perks'],'traditions_same':c['traditions']==base['traditions'],
 'theory_kept':'tech_psionic_theory' in c['completed_technologies'],'core_once':sum(a['deposits'].get(str(i),{}).get('type')=='d_eep_core' for i in a['planets']['7']['deposits'])==1,
 'original_five_buildings_held':len(original['zone0'])==5 and set(original['zone0'])<=set(state['zone0']) and all(state['buildings'][str(i)]['type']==original['buildings'][str(i)]['type'] for i in original['zone0']),
 'one_actual_new_factory':len(new_buildings)==1 and len(state['zone0'])==6 and state['buildings'][str(new_buildings[0])]['type']=='building_factory_1',
 'artisan1600_filled':job('artisan')['workforce']==job('artisan')['max_workforce']==1600,
 'mine_correct_phase':a['districts']['2']['level']==(2 if phase=='factory' else 3),
 'miner_correct_phase_filled':job('miner')['workforce']==job('miner')['max_workforce']==(400 if phase=='factory' else 600),
 'queue_correct_phase':state['queue']==([150994983] if phase=='factory' else []),
 'native_research_bank_available':c['research_stockpile'] is not None,
 'primary_stocks_positive':all(c['effective_stockpile'].get(k,0)>0 for k in ('food','consumer_goods','minerals','energy','unity')),
 'no_new_EEP_errors':b'eep.' not in new and b'eep_' not in new}
 budget=c['budget_categories']['current_month'];nets={k:sum(Decimal(str(v.get(k,0))) for v in budget['income'].values())-sum(Decimal(str(v.get(k,0))) for v in budget['expenses'].values()) for k in ('energy','minerals','food','consumer_goods','alloys','unity')}
 row={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','phase':phase,'date':date,'save_sha256':a['save_sha256'],'checks':checks,'new_buildings':new_buildings,'queue':state['queue'],'artisan':job('artisan'),'miner':job('miner'),'effective_stockpile':c['effective_stockpile'],'actual_research_bank':c['research_stockpile'],'budget_nets':{k:str(v) for k,v in nets.items()},'new_error_bytes':len(new)}
 if phase=='nextmonth':
  previous=b['countries']['0']['effective_stockpile'];row['six_stock_budget_residuals']={k:str(Decimal(str(c['effective_stockpile'][k]))-Decimal(str(previous[k]))-v) for k,v in nets.items()};checks['six_stock_budget_residuals_zero']=all(Decimal(v)==0 for v in row['six_stock_budget_residuals'].values());row['status']='PASS_SCOPED' if all(checks.values()) else 'FAIL'
 h.write_json(run/(stage+'-proof.json'),row);rows.append(row);print(json.dumps(row),flush=True);h.write_json(run/'organic-paid-industry-completion-result.json',{'status':'IN_PROGRESS' if all(checks.values()) else 'FAILED_GUARD','completed':rows});assert all(checks.values()),'Original paid construction failure retained';start=stage
h.write_json(run/'organic-paid-industry-completion-result.json',{'status':'PASS_SCOPED','completed':rows,'scope':'Actual paid factory and mine3 completion, employment and next-month economy only; full civic acceptance pending.'})
