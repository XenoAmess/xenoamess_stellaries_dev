import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-MOM-agenda-launched';stage='organic-psionic-theory-selected';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-native-option');labels=[x['text'] for x in f['rows']];assert '\u7075\u80fd\u7406\u8bba' in labels and '1929/7716' in labels
h.click_point(425,433,stage+'-actual-native-select');f=r.gpu_capture(stage+'-after-select-ui');print(json.dumps({'labels':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_ledger_same':ca['variables']==cb['variables'],'EEP_flags_same':ca['flags']==cb['flags'],'only_society_queue_added':{k:v for k,v in ca['research_queues'].items() if k!='society_queue'}==cb['research_queues'] and 'tech_psionic_theory' in ca['research_queues'].get('society_queue',''),'no_psionic_theory_completed_early':'tech_psionic_theory' not in ca['completed_technologies'],'no_new_errors':ea==eb}
for k in ('completed_technologies','traditions','ascension_perks','government'):checks[k+'_same']=ca[k]==cb[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=a[k]==b[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'research_queues_after':ca['research_queues'],'scope':'Native theory selection only, actual completion pending.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original full native research selection FAIL retained'
