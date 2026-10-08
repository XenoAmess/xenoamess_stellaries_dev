import copy
import json
from pathlib import Path
import shutil
import sys
import zipfile
from decimal import Decimal
sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
shutil.copyfile(Path(__file__),run/'rc8_prove_geothermal_queue_recovered.py')
a=json.loads((run/'rc8-hiveworld-market-funded-native.audit.json').read_text())
b=json.loads((run/'rc8-hiveworld-six-geothermal-paid-queued.audit.json').read_text())
with zipfile.ZipFile(run/'rc8-hiveworld-six-geothermal-paid-queued.sav') as z:
    text=z.read('gamestate').decode('utf-8-sig')
construction=q.block(text,'construction')
queues=q.block(q.block(construction,'queue_mgr'),'queues')
queue0=q.block(queues,'0')
items={k:v for k,v,obj in q.fields(q.block(q.block(construction,'item_mgr'),'items')) if obj}
ids=q.ids(q.block(queue0,'items'))
checks=[]
def check(name,actual,expected):
    checks.append({'check':name,'status':'PASS' if actual==expected else 'FAIL','actual':actual,'expected':expected})
check('queue_actual_six_orders',len(ids),6)
check('queue_owner',q.scalars(queue0)['owner'],0)
check('queue_physical_location',q.scalars(q.block(queue0,'location')),{'type':2,'id':1})
for i in ids:
    item=items[str(i)]
    scalar=q.scalars(item)
    for k,v in {'queue':0,'paying_country':0,'progress':0,'progress_needed':240}.items():
        check(str(i)+':'+k,scalar[k],v)
    check(str(i)+':minerals_cost',q.scalars(q.block(item,'resources')),{'minerals':240})
    check(str(i)+':type_and_actual_colony',q.scalars(q.block(item,'buildable_district')),{'district':'district_geothermal','planet':0})
check('paid_six_actual_costs',str(Decimal(str(a['countries']['0']['stockpile']['minerals']))-Decimal(str(b['countries']['0']['stockpile']['minerals']))),'1440.00000')
c,d=copy.deepcopy(a['colonies']),copy.deepcopy(b['colonies'])
check('only_last_order_type_change',[c['0'].pop('last_district_changed'),d['0'].pop('last_district_changed')],['district_polytechnic','district_geothermal'])
check('all_other_colony_fields',d==c,True)
for key in ['pop_groups','pop_jobs','districts','deposits','situations','species','event_targets','planets']:
    check('all_'+key,b[key]==a[key],True)
for key in ['variables','flags']:
    check('eep_'+key,b['countries']['0'][key],a['countries']['0'][key])
for key,value in a['countries']['0']['stockpile'].items():
    if key!='minerals': check('stock:'+key,b['countries']['0']['stockpile'].get(key,0),value)
result={'status':'PASS_SCOPED' if all(c['status']=='PASS' for c in checks) else 'FAIL','scope':'Six normal native paid district orders, no pre-completion jobs or EEP award.',
        'date':b['date'],'save_sha256':b['save_sha256'],'native_queue_ids':ids,'checks':checks,
        'original_failure_retained':'rc8_natural_geothermal_queue.py strict all colonies assertion; exact sole changed field documented.'}
out=run/'rc8-hiveworld-six-geothermal-paid-queue-recovered-proof.json'
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failures':[c for c in checks if c['status']!='PASS']},ensure_ascii=True))
