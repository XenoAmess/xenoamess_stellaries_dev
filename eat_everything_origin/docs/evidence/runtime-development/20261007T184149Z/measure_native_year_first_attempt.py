import json
import logging
import sys
import time
from datetime import datetime, timezone
import psutil

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--vanilla']
import runtime as r

logging.disable(logging.INFO)
artifacts, userdir, manifest = r.harness.load_run()
baseline = json.loads((artifacts / 'vanilla-shared-world-frozen50-unstarted.audit.json').read_text(encoding='utf-8'))
assert baseline['date'] == '2200.01.01'
assert baseline['situations'] == {}
assert json.loads((userdir / 'dlc_load.json').read_text(encoding='utf-8-sig'))['enabled_mods'] == []
pid = int(r.harness.process_record(artifacts)['pid'])
process = psutil.Process(pid)
stage = 'vanilla-shared-world-native-year'
r.harness.press_scan_code(0x29, stage + '-console-open', 1)
r.harness.type_text('fast_forward 360', False, stage + '-command-typed')
started_utc = datetime.now(timezone.utc).isoformat()
cpu_start = process.cpu_times()
started = time.monotonic()
samples = []
receipt = artifacts / (stage + '-measurement.json')
r.harness.press_scan_code(0x1c, stage + '-command-submit', 1)
completed = False
for attempt in range(30):
    if attempt:
        time.sleep(10)
    frame = r.gpu_capture(stage + '-completion-poll-' + str(attempt))
    elapsed = time.monotonic() - started
    cpu = process.cpu_times()
    texts = [row['text'] for row in frame['rows']]
    completed = any('FastForwarded' in r.harness.normalized(label).replace(' ', '') for label in texts)
    samples.append({'elapsed_wall_seconds': elapsed,
                    'cpu_user_seconds': cpu.user - cpu_start.user,
                    'cpu_system_seconds': cpu.system - cpu_start.system,
                    'completion_frame': frame['image'],
                    'completion_frame_sha256': frame['image_sha256'],
                    'completed': completed})
    r.harness.write_json(receipt, {
        'status': 'MEASURED_AWAITING_NATIVE_SAVE' if completed else 'RUNNING',
        'start_date': baseline['date'], 'days_requested': 360,
        'baseline_save_sha256': baseline['save_sha256'], 'enabled_mods': [],
        'pid': pid, 'started_at_utc': started_utc,
        'sampling': 'before physical Enter through first fresh GPU/OCR completion confirmation; includes Enter and polling overhead, excludes native saving',
        'samples': samples,
    })
    print(json.dumps(samples[-1]), flush=True)
    if completed:
        break
if not completed:
    raise RuntimeError('native fast_forward completion was not confirmed within bounded polling')
r.harness.press_scan_code(0x29, stage + '-console-close', 1)
result = r.native_save('vanilla-shared-world-native-year-complete', '2201.01.01', (0,))
report = json.loads(receipt.read_text(encoding='utf-8'))
report.update(status='MEASURED_NATIVE_DATE_VERIFIED', end_date=result['date'],
              end_save_sha256=result['save_sha256'],
              start_save_bytes=(artifacts / 'vanilla-shared-world-frozen50-unstarted.sav').stat().st_size,
              end_save_bytes=(artifacts / 'vanilla-shared-world-native-year-complete.sav').stat().st_size,
              end_gamestate_bytes=result['gamestate_bytes'])
r.harness.write_json(receipt, report)
print(json.dumps({key: value for key, value in report.items() if key != 'samples'}), flush=True)
