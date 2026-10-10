"""Read-only native paid building order audit, never issues UI actions."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,building,zone,price=sys.argv[1:];zone=int(zone);price=int(price);assert price>0
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 roots={k:v for k,v,o in q.fields(t) if o};c=roots['construction']
 queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0')
 items={k:v for k,v,o in q.fields(q.block(q.block(c,'item_mgr'),'items')) if o}
 return a,roots,queue,items
b,br,bq,bi=read(before);a,ar,aq,ai=read(after);bc,ac=b['countries']['0'],a['countries']['0']
old=q.ids(q.block(bq,'items'));new=q.ids(q.block(aq,'items'));added=[i for i in new if i not in old]
item=ai.get(str(added[0]),'') if len(added)==1 else '';sc=q.scalars(item)
checks={'same_actual_date':a['date']==b['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_expected_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==price,
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'only_one_appended_mother_order':len(added)==1 and new==old+added,
 'old_mother_orders_raw_held':all(ai.get(str(i))==bi[str(i)] for i in old),
 'native_paid_country_queue':sc.get('queue')==sc.get('paying_country')==0,
 'native_resources_expected_price':q.scalars(q.block(item,'resources'))=={'minerals':price},
 'native_progress0_360':sc.get('progress')==0 and sc.get('progress_needed')==360,
 'native_building_mother_zone':q.scalars(q.block(item,'buildable_planet_building'))=={'building':building,'planet':0,'zone':zone},
 'actual_error_original_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','planets','districts','deposits','species','situations','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['mother_last_building_changed_exact']=a['colonies']['0'].get('last_building_changed')==building
checks['all_colonies_except_exact_mother_building_record_held']=set(a['colonies'])==set(b['colonies']) and all(({k:v for k,v in a['colonies'][i].items() if k!='last_building_changed'}=={k:v for k,v in c.items() if k!='last_building_changed'}) if i=='0' else a['colonies'][i]==c for i,c in b['colonies'].items())
checks['all_zones_and_buildings_raw_held']=br['zones']==ar['zones'] and br['buildings']==ar['buildings']
proof={'status':'PASS_NATIVE_PAID_BUILDING_ORDER' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'expected_actual_price':price,'native_item_raw':item,'mineral_before_after':[bc['effective_stockpile']['minerals'],ac['effective_stockpile']['minerals']],'scope':'Actual one paid order only; completion, jobs and monthly maintenance require later evidence.'}
out=run/(after+'-paid-v4-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original order failure retained; do not repeat purchase'
