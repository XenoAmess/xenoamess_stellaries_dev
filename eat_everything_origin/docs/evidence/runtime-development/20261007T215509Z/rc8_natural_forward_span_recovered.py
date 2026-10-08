import json
import logging
from pathlib import Path
import shutil
import sys
import time
import zipfile
from datetime import datetime,timezone
start_name=sys.argv[1]
end_date=sys.argv[2]
stage=sys.argv[3]
days=int(sys.argv[4]) if len(sys.argv)>4 else 360
assert 1<=days<=1800
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness
run,user,manifest=h.load_run()
copy=run/'rc8_natural_forward_span_recovered.py'
if not copy.exists(): shutil.copyfile(Path(__file__),copy)
start=json.loads((run/(start_name+'.audit.json')).read_text())
h.press_scan_code(0x29,stage+'-console-open',1)
h.type_text('fast_forward '+str(days),True,stage+'-native-calendar-span')
began=time.monotonic()
for n in range(90):
    if n: time.sleep(15)
    frame=r.gpu_capture(stage+'-native-year-poll-'+str(n))
    labels=[row['text'] for row in frame['rows']]
    receipt_texts={'fastforwarded'+str(days)+'days','fastforwarded'+str(days)+'d'}
    complete=(end_date in labels and '暂停' in labels and any(h.normalized(t) in receipt_texts for t in labels))
    h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED' if complete else 'RUNNING',
        'start_date':start['date'],'expected_date':end_date,'days':days,'elapsed_wall_seconds':time.monotonic()-began,
        'frame_sha256':frame['image_sha256'],'confirmed_at_utc':datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'poll':n,'seconds':round(time.monotonic()-began,2),'dates':[t for t in labels if t.startswith(('229','230','231'))], 'complete':complete}),flush=True)
    if complete: break
else: raise RuntimeError('Natural year date/completion was not confirmed; no further dependent input sent.')
h.press_scan_code(0x29,stage+'-console-close',1)
after=r.native_save(stage,end_date,(0,))
c=after['countries']['0']
assert {k:c['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']}=={k:start['countries']['0']['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']}
assert c['stockpile']['energy']>0
mother=after['colonies']['0']
districts={after['districts'][str(i)]['type']:after['districts'][str(i)]['level'] for i in mother['districts']}
with zipfile.ZipFile(run/(stage+'.sav')) as z:
    text=z.read('gamestate').decode('utf-8-sig')
planet=q.block(q.block(q.block(text,'planets'),'planet'),'1')
terraform={k:v for k,v,o in q.fields(planet) if 'terraform' in k}
h.write_json(run/(stage+'-native-terraform-checkpoint.json'),{'date':after['date'],
    'actual_class':after['planets']['1']['planet_class'],'terraform':terraform,
    'save_sha256':after['save_sha256'],'eep_ledger':{k:c['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']},
    'country_scope':'Focus country0 and automatically present EEP owners; not all native foreign countries.'})
print(json.dumps({'date':after['date'],'energy':c['stockpile']['energy'],'minerals':c['stockpile']['minerals'],
    'population':mother['actual_pop_sum'],'districts':districts,'terraform':terraform,'sha256':after['save_sha256']},ensure_ascii=True),flush=True)
