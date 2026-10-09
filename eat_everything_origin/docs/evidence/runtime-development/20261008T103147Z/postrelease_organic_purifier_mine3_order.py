import json,logging,shutil,sys,zipfile
from decimal import Decimal
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
start='organic-mother-factory-ordered';stage='organic-mother-mine3-ordered'
b=json.loads((run/(start+'.research-v2.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-native-cost');labels=[v['text'] for v in f['rows']]
assert '\u5efa\u9020\u91c7\u77ff\u533a\u5212' in labels and '240300' in labels
h.click_point(464,439,stage+'-native-click');a=r.native_save(stage,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
bc,ac=b['countries']['0'],a['countries']['0']
def construction(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 c=q.block(t,'construction');queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');items=q.block(q.block(c,'item_mgr'),'items')
 return q.ids(q.block(queue,'items')),{k:v for k,v,o in q.fields(items) if o}
bid,bi=construction(start);aid,ai=construction(stage);item=ai.get(str(aid[-1]),'') if aid else '';sc=q.scalars(item)
changes={i:{k:[b['colonies'].get(i,{}).get(k),v] for k,v in c.items() if b['colonies'].get(i,{}).get(k)!=v} for i,c in a['colonies'].items() if c!=b['colonies'].get(i)}
checks={'same_actual_date':a['date']==b['date']=='2294.12.02',
 'actual_300_minerals_paid':Decimal(str(bc['effective_stockpile']['minerals']))-Decimal(str(ac['effective_stockpile']['minerals']))==300,
 'other_effective_stocks_same':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'actual_research_banks_same':bc['research_stockpile']==ac['research_stockpile'],
 'complete_tech_status_same':bc['tech_status']==ac['tech_status'],
 'one_existing_factory_then_one_new_mine':len(bid)==1 and len(aid)==2 and aid[:1]==bid and ai[str(bid[0])]==bi[str(bid[0])],
 'mother_country_and_district':sc.get('queue')==sc.get('paying_country')==0 and q.scalars(q.block(item,'buildable_district'))=={'district':'district_mining','planet':0},
 'progress0_needed240':sc.get('progress')==0 and sc.get('progress_needed')==240,
 'native_resources300':q.scalars(q.block(item,'resources'))=={'minerals':300},
 'only_expected_last_district_changed':changes=={'0':{'last_district_changed':['district_farming','district_mining']}},
 'no_new_errors':ea==eb}
for k in ('variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government'):checks[k+'_same']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','planets','districts','deposits','situations','species'):checks[k+'_same']=b[k]==a[k]
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,
 'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'auditor_sha256':a['audit_tool_sha256'],
 'native_queue_ids_before':bid,'native_queue_ids_after':aid,'new_native_item_raw':item,
 'strict_colonies_same':a['colonies']==b['colonies'],'colony_changes':changes,
 'raw_stock_changes':{k:[bc['stockpile'].get(k),v] for k,v in ac['stockpile'].items() if bc['stockpile'].get(k)!=v},
 'scope':'Real paid mine3 order after existing factory. No early completion; future construction and monthly budget pending.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original mine order failure retained; do not repeat order'
