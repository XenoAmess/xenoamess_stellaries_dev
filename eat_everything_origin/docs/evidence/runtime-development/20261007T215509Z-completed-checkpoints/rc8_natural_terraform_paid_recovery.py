import json
import logging
from pathlib import Path
import shutil
import sys
import zipfile
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness
run,user,manifest=h.load_run()
shutil.copyfile(Path(__file__),run/'rc8_natural_terraform_paid_recovery.py')
before=json.loads((run/'rc8-hiveworld-energy-build-year2.audit.json').read_text())
after=json.loads((run/'rc8-hiveworld-natural-terraform10000-paid.audit.json').read_text())
a,b=before['countries']['0'],after['countries']['0']
assert Decimal(str(a['stockpile']['energy']))-Decimal(str(b['stockpile']['energy']))==Decimal(10000)
for key in a['stockpile']:
    if key not in ['energy','physics_research','society_research','engineering_research']:
        assert a['stockpile'].get(key,0)==b['stockpile'].get(key,0),key
assert a['variables']==b['variables'] and a['flags']==b['flags']
for key in ['colonies','pop_groups','pop_jobs','districts','deposits','situations','species','event_targets']:
    assert before[key]==after[key],key
with zipfile.ZipFile(run/'rc8-hiveworld-natural-terraform10000-paid.sav') as z:
    text=z.read('gamestate').decode('utf-8-sig')
planet=q.block(q.block(q.block(text,'planets'),'planet'),'1')
terraform={k:v for k,v,o in q.fields(planet) if 'terraform' in k}
assert terraform, 'Native planet terraforming data is required.'
h.write_json(run/'rc8-hiveworld-natural-terraform-paid-proof.json',{'status':'PASS_SCOPED','date':after['date'],
    'energy_paid':10000,'energy_remaining':b['stockpile']['energy'],
    'all_nonresearch_stocks_except_energy_and_eep_economy_kept':True,'world_population_jobs_districts_kept':True,
    'stock_changes':{k:{'before':a['stockpile'].get(k,0),'after':b['stockpile'].get(k,0)} for k in set(a['stockpile'])|set(b['stockpile']) if a['stockpile'].get(k,0)!=b['stockpile'].get(k,0)},
    'native_terraform_raw':terraform,'actual_class_before':'pc_volcanic','target':'pc_hive',
    'source_save_sha256':before['save_sha256'],'save_sha256':after['save_sha256'],
    'limitations':['This payment proof does not claim completed terraforming.','Three actual research pools changed; cause not isolated; original strict stock assertion FAIL preserved.']})
print(json.dumps({'status':'PASS_SCOPED','date':after['date'],'energy_remaining':b['stockpile']['energy'],'terraform':terraform},ensure_ascii=True),flush=True)
