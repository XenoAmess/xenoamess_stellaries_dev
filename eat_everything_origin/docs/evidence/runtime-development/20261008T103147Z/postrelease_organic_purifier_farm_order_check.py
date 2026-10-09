import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-purifier-2287-MOM-agenda-selected';stage='organic-purifier-2287-farm-ordered'
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(stage+'.audit.json')).read_text(encoding='utf-8'));cb,ca=b['countries']['0'],a['countries']['0']
def queues(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:text=z.read('gamestate').decode('utf-8-sig')
 construction=q.block(text,'construction');queue=q.block(q.block(q.block(construction,'queue_mgr'),'queues'),'0');items=q.block(q.block(construction,'item_mgr'),'items')
 return queue,{k:v for k,v,obj in q.fields(items) if obj}
bqueue,bitems=queues(start);aqueue,aitems=queues(stage);ids=q.ids(q.block(aqueue,'items'));item=aitems.get(str(ids[0]),'') if len(ids)==1 else '';native=q.scalars(item) if item else {}
checks={'same_date':b['date']==a['date'],'actual_mineral_payment_300':abs(cb['stockpile']['minerals']-ca['stockpile']['minerals']-300)<1e-5,'all_other_stock_same':{k:v for k,v in cb['stockpile'].items() if k!='minerals'}=={k:v for k,v in ca['stockpile'].items() if k!='minerals'},'EEP_variables_same':cb['variables']==ca['variables'],'native_empty_to_one_order':q.ids(q.block(bqueue,'items'))==[] and len(ids)==1,'native_item_on_mother':native.get('queue')==0 and native.get('paying_country')==0 and q.scalars(q.block(item,'buildable_district'))=={'district':'district_farming','planet':0},'native_recorded_cost':q.scalars(q.block(item,'resources'))=={'minerals':300},'native_progress_zero_needed_240':native.get('progress')==0 and native.get('progress_needed')==240,'farm_not_completed_early':b['districts']['3']['level']==a['districts']['3']['level']==3}
for k in ('completed_technologies','research_queues','traditions','ascension_perks','government'):checks[k+'_same']=cb[k]==ca[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=b[k]==a[k]
eb=(run/'organic-purifier-unity-2287-error-after.log').read_bytes();ea=(user/'logs/error.log').read_bytes();checks['no_new_errors_since_2287']=eb==ea;(run/(stage+'-error-final.log')).write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_queue_before':bqueue,'native_queue_after':aqueue,'native_item':item,'item_ids':ids,'scope':'Actual paid natural mother farm order only; workforce, completion and food recovery pending.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps({k:v for k,v in proof.items() if k not in ('native_queue_before','native_queue_after','native_item')}),flush=True);assert all(checks.values()),'Original farm order FAIL retained'
