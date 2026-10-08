import json
import logging
from pathlib import Path
import shutil
import sys
import time
from datetime import datetime, timezone

start_name, end_date, stage, raw_days = sys.argv[1:]
days = int(raw_days)
assert 1 <= days <= 1800
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
copy = run / Path(__file__).name
if not copy.exists():
    shutil.copyfile(Path(__file__), copy)
assert copy.read_bytes() == Path(__file__).read_bytes()
start = json.loads((run / (start_name + '.audit.json')).read_text(encoding='utf-8'))
h.press_scan_code(0x29, stage + '-console-open', 1)
h.type_text('fast_forward ' + str(days), True, stage + '-actual-calendar-command')
for n in range(45):
    if n:
        time.sleep(10)
    frame = r.gpu_capture(stage + '-calendar-poll-' + str(n))
    labels = [row['text'] for row in frame['rows']]
    receipts = {'fastforwarded'+str(days)+'days','fastforwarded'+str(days)+'d'}
    complete = end_date in labels and '暂停' in labels and any(h.normalized(t) in receipts for t in labels)
    print(json.dumps({'poll':n,'complete':complete,'date':end_date if end_date in labels else None}),flush=True)
    if complete:
        h.write_json(run / (stage + '-calendar-receipt.json'), {
            'status':'CALENDAR_CONFIRMED','start_date':start['date'],'date':end_date,'days':days,
            'frame_sha256':frame['image_sha256'],'confirmed_at_utc':datetime.now(timezone.utc).isoformat()})
        break
else:
    raise RuntimeError('Correct date, paused state and actual day receipt not confirmed.')
h.press_scan_code(0x29, stage + '-console-close', 1)
after = r.native_save(stage,end_date,(0,))
c = after['countries']['0']
ledger = {k:c['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']}
h.write_json(run / (stage + '-actual-purge-transition.json'), {'date':after['date'],'save_sha256':after['save_sha256'],'previous_ledger':{k:start['countries']['0']['variables'][k] for k in ledger},'actual_ledger':ledger,'source':after['planets'].get('84'),'source_colony':after['colonies'].get('24'),'situations':after['situations'],'scope':'Actual calendar observation. Legal final settlement may change ledger; not an automatic acceptance PASS.'})
mother = after['planets']['1']
deposits = [after['deposits'][str(i)]['type'] for i in mother['deposits']]
print(json.dumps({'date':after['date'],'save_sha256':after['save_sha256'],
                  'mother_class':mother['planet_class'],'deposits':deposits,
                  'population':after['colonies']['0']['actual_pop_sum'],'ledger':ledger,
                  'all_stockpile_same':c['stockpile'] == start['countries']['0']['stockpile']},ensure_ascii=True),flush=True)
