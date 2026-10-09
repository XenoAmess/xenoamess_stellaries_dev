import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-mother-temple-calendar360';stage='organic-MOM-agenda-launched';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-main-control');labels=[x['text'] for x in f['rows']];assert '\u70b9\u51fb\u542f\u52a8\u8bae\u7a0b' in labels
h.click_point(502,410,stage+'-actual-launch-click');f=r.gpu_capture(stage+'-after-click');print(json.dumps({'labels':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_ledger_same':ca['variables']==cb['variables'],'EEP_flags_same':ca['flags']==cb['flags'],'native_psionic_theory_not_completed':'tech_psionic_theory' not in ca['completed_technologies'],'no_new_errors':eb==ea}
for k in ('completed_technologies','traditions','ascension_perks'):checks[k+'_same']=ca[k]==cb[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=a[k]==b[k]
h.write_json(run/(stage+'-proof.json'),{'status':'OBSERVED_NATIVE_LAUNCH' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'research_queues_before':cb['research_queues'],'research_queues_after':ca['research_queues'],'government_before':cb['government'],'government_after':ca['government'],'all_stock_changes':{k:[cb['stockpile'].get(k),v] for k,v in ca['stockpile'].items() if cb['stockpile'].get(k)!=v},'scope':'Native matured agenda launch, exact technology-progress and cooldown proof pending readonly inspection.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original full native agenda launch FAIL retained'
