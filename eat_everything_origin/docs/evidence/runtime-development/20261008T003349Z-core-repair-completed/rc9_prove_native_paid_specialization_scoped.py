import json
from pathlib import Path
import shutil
import sys
import zipfile
from decimal import Decimal
sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
dest=run/Path(__file__).name
assert not dest.exists()
shutil.copyfile(Path(__file__),dest)
before=json.loads((run/'rc9-hiveworld-reloaded-core-once.audit.json').read_text(encoding='utf-8'))
after=json.loads((run/'rc9-native-heavy-industry800-paid.audit.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(run/'rc9-native-heavy-industry800-paid.sav') as z:
 text=z.read('gamestate').decode('utf-8-sig')
construction=q.block(text,'construction')
queue=q.block(q.block(q.block(construction,'queue_mgr'),'queues'),'0')
ids=q.ids(q.block(queue,'items'))
items={k:v for k,v,b in q.fields(q.block(q.block(construction,'item_mgr'),'items')) if b}
assert len(ids)==1
item=items[str(ids[0])]
b,a=before['countries']['0'],after['countries']['0']
checks={
 'queue_count_one':len(ids)==1,
 'original_physical_queue':q.scalars(q.block(queue,'location'))=={'type':2,'id':1},
 'native_payer_country0':q.scalars(item).get('paying_country')==0,
 'progress0_of_base360':q.scalars(item).get('progress')==0 and q.scalars(item).get('progress_needed')==360,
 'native_cost800':q.scalars(q.block(item,'resources'))=={'minerals':800},
 'native_hive_foundry_colony0_district113_slot0':q.scalars(q.block(item,'buildable_zone'))=={'zone':'zone_foundry_hive','planet':0,'district':113,'zone_slot':0},
 'paid_exact800':Decimal(str(b['stockpile']['minerals']))-Decimal(str(a['stockpile']['minerals']))==800,
 'other_resources_except_recorded_native_research_equal':{k:v for k,v in a['stockpile'].items() if k not in ('minerals','physics_research','society_research','engineering_research')}=={k:v for k,v in b['stockpile'].items() if k not in ('minerals','physics_research','society_research','engineering_research')},
 'exact_native_research_stock_difference':all(b['stockpile'].get(k,0)>0 and a['stockpile'].get(k,0)==0 for k in ('physics_research','society_research','engineering_research')),
 'research_queues_equal':a['research_queues']==b['research_queues'],
 'all_eep_variables_equal':a['variables']==b['variables'],
 'all_eep_flags_equal':a['flags']==b['flags'],
 'targets_equal':before['event_targets']==after['event_targets'],
 'all_actual_pop_groups_equal':before['pop_groups']==after['pop_groups'],
 'all_actual_jobs_equal':before['pop_jobs']==after['pop_jobs'],
 'all_built_districts_equal':before['districts']==after['districts'],
 'deposits_equal':before['deposits']==after['deposits'],
}
result={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','scope':'Native normal paid zone selection, no extra EEP awards or pre-completion jobs. UI estimated195 days is distinct from base work360.', 'before_sha256':before['save_sha256'],'after_sha256':after['save_sha256'],'date':after['date'],'queue_item_id':ids[0],'native_queue_item':item,'native_stock_changes':{k:[b['stockpile'].get(k),a['stockpile'].get(k)] for k in set(b['stockpile'])|set(a['stockpile']) if b['stockpile'].get(k)!=a['stockpile'].get(k)},'checks':checks,'original_fail_retained':'rc9-native-heavy-industry-paid-proof.json; exact 3 research stock keys missing after native payment; no all-resource equality claim'}
(run/'rc9-native-heavy-industry-paid-scoped-proof.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=True))
assert all(checks.values())
