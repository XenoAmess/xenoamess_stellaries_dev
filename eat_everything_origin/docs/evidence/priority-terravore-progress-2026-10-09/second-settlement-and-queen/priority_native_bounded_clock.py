"""Observe a bounded ordinary native clock; restore pause/ticks before saving."""
import json, logging, re, shutil, sys, time, zipfile
from pathlib import Path

before, stage, raw_seconds = sys.argv[1:]
seconds = float(raw_seconds)
assert 0 < seconds <= 10
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
assert manifest['version'] == '0.2.0' and manifest['language'] == 'l_simp_chinese'
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
assert not (run / (stage + '.sav')).exists()
b = json.loads((run / (before + '.audit.json')).read_text(encoding='utf-8'))
assert h.sha256(run / (before + '.sav')) == b['save_sha256']
with zipfile.ZipFile(run / (before + '.sav')) as z:
    text = z.read('gamestate').decode('utf-8-sig')
pending = [q.scalars(v) for k, v, obj in q.fields(text)
           if k == 'player_event' and obj and q.scalars(v).get('country') == 0]
assert not pending, 'Review original pending choices before running a clock'

def date_in(frame):
    dates = [v['text'] for v in frame['rows']
             if min(p[1] for p in v['box']) < 25
             and min(p[0] for p in v['box']) > 880
             and re.fullmatch(r'\d{4}\.\d{2}\.\d{2}', v['text'])]
    assert len(dates) == 1, dates
    return dates[0]

def day_number(date):
    y, m, d = map(int, date.split('.'))
    return y * 360 + (m - 1) * 30 + d - 1

frame = r.gpu_capture(stage + '-before')
assert date_in(frame) == b['date'] and '\u6682\u505c' in [x['text'] for x in frame['rows']]
eb = (user / 'logs/error.log').read_bytes()
(run / (stage + '-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29, stage + '-console-open', 1)
h.type_text('ticks_per_turn 10', True, stage + '-ticks10')
started = time.monotonic()
try:
    h.type_text('game_paused false', True, stage + '-run')
    time.sleep(seconds)
finally:
    h.type_text('game_paused true', True, stage + '-pause')
    h.type_text('ticks_per_turn 1', True, stage + '-ticks1')
elapsed = time.monotonic() - started
frame = r.gpu_capture(stage + '-paused-console')
labels = [v['text'] for v in frame['rows']]
assert '\u6682\u505c' in labels, 'Do not save an unconfirmed running state'
date = date_in(frame)
h.press_scan_code(0x29, stage + '-console-close', 1)
# Leave the original debug overlay visible if F12 opened it; native_save handles ESC.
a = r.native_save(stage, date, (0,))
ea = (user / 'logs/error.log').read_bytes()
(run / (stage + '-error-after.log')).write_bytes(ea)
days = day_number(a['date']) - day_number(b['date'])
proof = {
    'status': 'OBSERVED_BOUNDED_NATIVE_CLOCK' if 1 <= days <= 360 else 'FAIL_CLOCK_BOUND',
    'before_date': b['date'], 'after_date': a['date'], 'actual_days': days,
    'requested_running_seconds': seconds, 'command_span_seconds': elapsed,
    'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'],
    'restored_commands': ['game_paused true', 'ticks_per_turn 1'],
    'actual_receipt_labels': labels, 'source_UI_sha256': frame['image_sha256'],
    'new_error_bytes': len(ea) - len(eb), 'error_prefix_held': ea.startswith(eb),
    'scope': 'Ordinary native clock with ticks10 then pause/ticks1 restoration. No exact-day boundary or route/economy acceptance.'
}
h.write_json(run / (stage + '-clock-observation.json'), proof)
print(json.dumps(proof), flush=True)
assert 1 <= days <= 360, 'Original bound failure retained; no automatic continuation'
