import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-psionic-theory-month36';stage='organic-mother-factory-ordered';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-native-price');labels=[x['text'] for x in f['rows']];assert '\u6c11\u7528\u5de5\u4e1a\u4f53' in labels and '360400' in labels
h.click_point(812,453,stage+'-native-build-click');a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
def construction(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 c=q.block(t,'construction');queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');items=q.block(q.block(c,'item_mgr'),'items');return queue,{k:v for k,v,o in q.fields(items) if o}
bq,bi=construction(start);aq,ai=construction(stage);ids=q.ids(q.block(aq,'items'));item=ai.get(str(ids[0]),'') if len(ids)==1 else '';sc=q.scalars(item)
checks={'same_actual_date':a['date']==b['date'],'actual_400_minerals_paid':abs(cb['stockpile']['minerals']-ca['stockpile']['minerals']-400)<1e-5,'all_other_stock_same':{k:v for k,v in ca['stockpile'].items() if k!='minerals'}=={k:v for k,v in cb['stockpile'].items() if k!='minerals'},'empty_to_one_queue':q.ids(q.block(bq,'items'))==[] and len(ids)==1,'native_queue_mother_country':sc.get('queue')==sc.get('paying_country')==0,'native_resources400':q.scalars(q.block(item,'resources'))=={'minerals':400},'native_progress0_needed360':sc.get('progress')==0 and sc.get('progress_needed')==360,'EEP_ledger_same':ca['variables']==cb['variables'],'EEP_flags_same':ca['flags']==cb['flags'],'no_new_errors':ea==eb}
for k in ('completed_technologies','research_queues','traditions','ascension_perks','government'):checks[k+'_same']=ca[k]==cb[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=a[k]==b[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_item_raw':item,'all_stock_changes':{k:[cb['stockpile'].get(k),v] for k,v in ca['stockpile'].items() if cb['stockpile'].get(k)!=v},'scope':'Native paid civilian industry order; completion and monthly consumer-goods effect pending.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original native civilian factory order FAIL retained'
