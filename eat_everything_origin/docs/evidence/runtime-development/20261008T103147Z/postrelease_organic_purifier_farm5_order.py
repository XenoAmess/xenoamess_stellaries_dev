import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-growth-ack-nextmonth';stage='organic-mother-farm5-ordered';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-cost');labels=[x['text'] for x in f['rows']];assert '\u5efa\u9020\u519c\u4e1a\u533a\u5212' in labels and '240300' in labels
h.click_point(674,439,stage+'-native-build-click');a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
def native_queue(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 c=q.block(t,'construction');queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');items=q.block(q.block(c,'item_mgr'),'items');return queue,{k:v for k,v,obj in q.fields(items) if obj}
bq,bi=native_queue(start);aq,ai=native_queue(stage);ids=q.ids(q.block(aq,'items'));item=ai.get(str(ids[0]),'') if len(ids)==1 else '';sc=q.scalars(item) if item else {}
checks={'same_actual_date':a['date']==b['date'],'actual_minerals_300_paid':abs(cb['stockpile']['minerals']-ca['stockpile']['minerals']-300)<1e-5,'all_other_stock_same':{k:v for k,v in ca['stockpile'].items() if k!='minerals'}=={k:v for k,v in cb['stockpile'].items() if k!='minerals'},'EEP_ledger_same':ca['variables']==cb['variables'],'farm_level4_not_early_complete':a['districts']['3']['level']==b['districts']['3']['level']==4,'empty_to_one_queue':q.ids(q.block(bq,'items'))==[] and len(ids)==1,'native_order_mother':sc.get('queue')==sc.get('paying_country')==0 and q.scalars(q.block(item,'buildable_district'))=={'district':'district_farming','planet':0},'native_cost_300':q.scalars(q.block(item,'resources'))=={'minerals':300},'native_progress_zero_240_days':sc.get('progress')==0 and sc.get('progress_needed')==240,'no_new_errors':ea==eb}
for k in ('completed_technologies','research_queues','traditions','ascension_perks','government'):checks[k+'_same']=ca[k]==cb[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=a[k]==b[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'queue_item_ids':ids,'native_order_raw':item,'scope':'Native paid level5 farm order in capacity actually earned from natural Q11 devour; completion and sustained budget pending.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original paid farm5 order FAIL retained'
