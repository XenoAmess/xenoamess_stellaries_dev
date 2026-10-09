import json,logging,shutil,subprocess,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
original=json.loads((run/'organic-purifier-2287-real-devour-begin.audit.json').read_text(encoding='utf-8'));base=original['countries']['0'];start='organic-purifier-2287-real-devour-begin';rows=[]
for month,date,days in ((12,'2288.10.12',360),(24,'2289.10.12',360),(26,'2289.12.12',60)):
 stage='organic-purifier-real-devour-month'+str(month)
 result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/formal_production_native_calendar.py',start,date,stage,str(days)],capture_output=True,text=True,encoding='utf-8')
 (run/(stage+'-driver-output.txt')).write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
 if result.returncode:
  h.write_json(run/'organic-purifier-real-devour-calendar-result.json',{'status':'FAILED_STAGE','stage':stage,'completed':rows,'returncode':result.returncode});print(result.stdout+result.stderr,flush=True);raise RuntimeError(stage+' calendar stopped; do not repeat days')
 a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));c=a['countries']['0'];p=a['planets'].get('1855',{});s=[v for v in a['situations'].values() if v.get('type')=='situation_eep_devouring'];mother=a['planets']['7'];core=[i for i in mother['deposits'] if a['deposits'].get(str(i),{}).get('type')=='d_eep_core']
 eb=(run/(stage+'-error-before.log')).read_bytes();ea=(run/(stage+'-error-after.log')).read_bytes();new=ea[len(eb):] if ea.startswith(eb) else ea
 checks={'date':a['date']==date,'source_owned':p.get('owner')==p.get('controller')==0,'source_active':'eep_active' in p.get('flags',{}),'Q11_T27':p.get('variables',{}).get('eep_q')==11 and p.get('variables',{}).get('eep_months')==27,'native_progress':len(s)==1 and s[0].get('progress')==month,'no_early_rewards':c['variables']==base['variables'],'three_legal_AP_same':c['ascension_perks']==base['ascension_perks'],'core_once':len(core)==1,'primary_stocks_positive':all(c['stockpile'].get(k,0)>0 for k in ('food','consumer_goods','energy','minerals','unity')),'no_new_EEP_errors':b'eep_' not in new and b'eep.' not in new}
 row={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','month':month,'date':date,'save_sha256':a['save_sha256'],'checks':checks,'stockpile':c['stockpile'],'source_population':a['colonies']['42']['actual_pop_sum'],'mother_population':a['colonies']['0']['actual_pop_sum'],'new_error_bytes':len(new)}
 h.write_json(run/(stage+'-proof.json'),row);rows.append(row);print(json.dumps(row),flush=True)
 h.write_json(run/'organic-purifier-real-devour-calendar-result.json',{'status':'IN_PROGRESS' if all(checks.values()) else 'FAILED_GUARD','completed':rows});assert all(checks.values()),stage+' guard failed, original evidence retained';start=stage
h.write_json(run/'organic-purifier-real-devour-calendar-result.json',{'status':'COMPLETED_PRETERMINAL_SCOPE','completed':rows,'scope':'Only actual 12/24/26 months, final month and Queen notification pending.'})
