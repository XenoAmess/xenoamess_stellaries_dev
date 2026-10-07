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
shutil.copyfile(Path(__file__),run/Path(__file__).name)
before=json.loads((run/'rc8-hiveworld-market-funded-native.audit.json').read_text())
for n in range(2,7):
    h.click_point(250,438,f'rc8-natural-geothermal-{n}-paid-order')
frame=r.gpu_capture('rc8-natural-six-geothermal-paid-native-queue')
after=r.native_save('rc8-hiveworld-six-geothermal-paid-queued','2297.03.12',tuple(map(int,before['countries'])))
a,b=before['countries']['0'],after['countries']['0']
assert Decimal(str(a['stockpile']['minerals']))-Decimal(str(b['stockpile']['minerals']))==Decimal(1440)
for key in a['stockpile']:
    if key!='minerals':
        assert a['stockpile'].get(key,0)==b['stockpile'].get(key,0),key
assert a['variables']==b['variables'] and a['flags']==b['flags']
for key in ['colonies','pop_groups','pop_jobs','districts','deposits','situations','species','event_targets','planets']:
    assert before[key]==after[key],key
with zipfile.ZipFile(run/'rc8-hiveworld-six-geothermal-paid-queued.sav') as z:
    text=z.read('gamestate').decode('utf-8-sig')
roots=list(q.fields(text))
queue={key:value for key,value,obj in roots if obj and ('construction' in key or 'build' in key)}
h.write_json(run/'rc8-hiveworld-six-geothermal-native-queue-raw.json',queue)
h.write_json(run/'rc8-hiveworld-six-geothermal-queue-proof.json',{'status':'PASS_SCOPED','date':after['date'],
    'minerals_paid':1440,'orders':6,'expected_type':'district_geothermal','actual_built_before_completion':3,
    'energy_kept':b['stockpile']['energy'],'new_jobs_not_granted_before_completion':True,
    'save_sha256':after['save_sha256'],'image_sha256':frame['image_sha256']})
print(json.dumps({'status':'PASS_SCOPED','energy':b['stockpile']['energy'],'minerals':b['stockpile']['minerals'],'sha256':after['save_sha256']},ensure_ascii=True),flush=True)
