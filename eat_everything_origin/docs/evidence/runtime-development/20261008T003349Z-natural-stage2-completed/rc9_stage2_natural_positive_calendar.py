import json
import logging
from pathlib import Path
import shutil
import sys
import time
import zipfile
from datetime import datetime, timezone

start_name, end_date, stage, raw_days = sys.argv[1:]
days = int(raw_days)
assert 1 <= days <= 360
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
copy = run / Path(__file__).name
if not copy.exists():
    shutil.copyfile(Path(__file__), copy)
assert copy.read_bytes() == Path(__file__).read_bytes()
assert not (run / (stage + '.sav')).exists()
before = json.loads((run / (start_name + '.audit.json')).read_text(encoding='utf-8'))
eb = (user / 'logs/error.log').read_bytes()
(run / (stage + '-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29, stage + '-console-open', 1)
h.type_text('fast_forward ' + str(days), True, stage + '-actual-calendar-command')
for n in range(24):
    if n:
        time.sleep(10)
    frame = r.gpu_capture(stage + '-calendar-poll-' + str(n))
    labels = [row['text'] for row in frame['rows']]
    receipts = {'fastforwarded' + str(days) + 'days', 'fastforwarded' + str(days) + 'd'}
    complete = end_date in labels and '\u6682\u505c' in labels and any(h.normalized(t) in receipts for t in labels)
    print(json.dumps({'poll': n, 'complete': complete, 'date': end_date if end_date in labels else None}), flush=True)
    if complete:
        h.write_json(run / (stage + '-calendar-receipt.json'), {
            'status': 'CALENDAR_CONFIRMED', 'start_date': before['date'], 'date': end_date, 'days': days,
            'frame_sha256': frame['image_sha256'], 'confirmed_at_utc': datetime.now(timezone.utc).isoformat()})
        break
else:
    raise RuntimeError('Correct date, paused state and actual day receipt not confirmed.')
h.press_scan_code(0x29, stage + '-console-close', 1)
after = r.native_save(stage, end_date, (0, 16777219))
with zipfile.ZipFile(run / (stage + '.sav')) as archive:
    raw = archive.read('gamestate').decode('utf-8-sig')
tables = {k: v for k, v, isblock in q.fields(raw) if isblock}
country = q.block(tables['country'], '0')
source = q.scalars(q.block(q.block(tables['planets'], 'planet'), '660'))
cp = q.block(country, 'crisis_progression')
objectives = [q.scalars(v) for k, v, isblock in q.fields(cp) if k == 'objective' and isblock]
ea = (user / 'logs/error.log').read_bytes()
(run / (stage + '-error-after.log')).write_bytes(ea)
result = {
    'status': 'OBSERVED_NATIVE_CALENDAR', 'save_sha256': after['save_sha256'], 'date': after['date'],
    'source_world': source, 'source_population': after['colonies'].get(str(source.get('colony')), {}).get('actual_pop_sum', 0),
    'root_variables_before': before['countries']['0']['variables'], 'root_variables_after': after['countries']['0']['variables'],
    'root_flags_after': after['countries']['0']['flags'], 'crisis_raw': cp, 'objectives': objectives,
    'menace_sum': sum(x.get('progress', 0) for x in objectives),
    'root_stock_before': before['countries']['0']['stockpile'], 'root_stock_after': after['countries']['0']['stockpile'],
    'new_error_bytes': len(ea) - len(eb),
    'scope': 'Real native days only; no EEP settlement/event calls, resource/population grants, crisis stage or menace writes.'
}
h.write_json(run / (stage + '-state.json'), result)
print(json.dumps({k: v for k, v in result.items() if not k.startswith('root_stock_') and k != 'crisis_raw'}), flush=True)
