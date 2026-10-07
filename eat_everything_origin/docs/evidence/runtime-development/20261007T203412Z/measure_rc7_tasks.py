import json
import logging
from pathlib import Path
import sys
import time
from datetime import datetime, timezone
import psutil

count = int(sys.argv[1])
assert count in (0, 1, 10, 50)
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r

logging.disable(logging.INFO)
artifacts, userdir, manifest = r.harness.load_run()
zero = json.loads(Path('_runtime/heart-of-devouring/runs/20261007T193619Z/rc6-paired-mod-zero-frozen.audit.json').read_text(encoding='utf-8'))
stage = 'rc7-paired-tasks' + str(count)
loaded = r.native_load('eep-zero', stage + '-restore-exact-zero')
assert loaded['source_sha256'] == zero['save_sha256']
if count:
    command = ('effect while = { count = ' + str(count) + ' random_owned_colony = { '
               'limit = { has_planet_flag = perf_constructed eep_source_valid = yes } eep_begin = yes } }')
    r.harness.press_scan_code(0x29, stage + '-begin-console-open', 1)
    r.harness.type_text(command, True, stage + '-formal-begin-on-existing-seeds')
    r.gpu_capture(stage + '-begin-console-result')
    r.harness.press_scan_code(0x29, stage + '-begin-console-close', 1)
start = r.native_save(stage + '-start', '2200.01.01', (0,))
tasks = {key: value for key, value in start['situations'].items() if value['type'] == 'situation_eep_devouring'}
active = {key: value for key, value in start['planets'].items() if 'eep_active' in value['flags']}
assert len(tasks) == len(active) == count, (tasks, active)
assert all(value['progress'] == 0 for value in tasks.values())
assert all(value['variables']['eep_q'] == 20 and value['variables']['eep_months'] == 48 for value in active.values())
assert start['countries']['0']['stockpile'] == zero['countries']['0']['stockpile']
assert start['countries']['0']['native']['num_sapient_pops'] == 5700
assert sum(value['size'] for value in start['pop_groups'].values()) == 5700
assert len([value for value in start['planets'].values() if 'perf_constructed' in value['flags']]) == 50
print(json.dumps({'phase': 'start verified', 'count': count, 'sha': start['save_sha256'], 'active_source_ids': sorted(active)}, ensure_ascii=False), flush=True)
pid = int(r.harness.process_record(artifacts)['pid'])
process = psutil.Process(pid)
r.harness.press_scan_code(0x29, stage + '-measure-console-open', 1)
r.harness.type_text('fast_forward 360', False, stage + '-measure-command-typed')
started_utc = datetime.now(timezone.utc).isoformat()
cpu_start = process.cpu_times()
started = time.monotonic()
samples = []
receipt = artifacts / (stage + '-measurement.json')
r.harness.press_scan_code(0x1c, stage + '-measure-command-submit', 1)
completed = False
for attempt in range(30):
    if attempt:
        time.sleep(10)
    frame = r.gpu_capture(stage + '-completion-poll-' + str(attempt))
    elapsed = time.monotonic() - started
    cpu = process.cpu_times()
    texts = [row['text'] for row in frame['rows']]
    completed = ('2201.01.01' in texts and any('fastforwarded360days' in r.harness.normalized(label) for label in texts))
    samples.append({'elapsed_wall_seconds': elapsed, 'cpu_user_seconds': cpu.user - cpu_start.user,
                    'cpu_system_seconds': cpu.system - cpu_start.system, 'completion_frame': frame['image'],
                    'completion_frame_sha256': frame['image_sha256'], 'completed': completed})
    r.harness.write_json(receipt, {
        'status': 'MEASURED_AWAITING_NATIVE_SAVE' if completed else 'RUNNING', 'tasks_started': count,
        'start_date': start['date'], 'days_requested': 360, 'start_save_sha256': start['save_sha256'],
        'common_mod_zero_sha256': zero['save_sha256'], 'original_native_frozen_sha256': '962b7ab20132e76ec41bbe87120db2ece05f7252823634db017d94420512588f',
        'active_source_ids': sorted(active), 'pid': pid, 'started_at_utc': started_utc,
        'mod_tree_sha256': manifest['copied_mod_tree_sha256'],
        'sampling': 'before physical Enter through first fresh GPU/OCR completion confirmation; includes Enter and polling overhead, excludes native saving',
        'samples': samples,
    })
    print(json.dumps(samples[-1]), flush=True)
    if completed:
        break
assert completed, 'native fast_forward completion was not confirmed within bounded polling'
r.harness.press_scan_code(0x29, stage + '-measure-console-close', 1)
end = r.native_save(stage + '-year-complete', '2201.01.01', (0,))
end_tasks = {key: value for key, value in end['situations'].items() if value['type'] == 'situation_eep_devouring'}
assert len(end_tasks) == count, end_tasks
assert all(value['progress'] == 12 for value in end_tasks.values()), end_tasks
assert end['countries']['0']['variables']['eep_c'] == end['countries']['0']['variables']['eep_g'] == end['countries']['0']['variables']['eep_made'] == 0
report = json.loads(receipt.read_text(encoding='utf-8'))
report.update(version='0.2.0-rc.7', status='MEASURED_NATIVE_DATE_AND_TASKS_VERIFIED', end_date=end['date'],
              end_save_sha256=end['save_sha256'], tasks_at_endpoint=len(end_tasks),
              endpoint_progress=[value['progress'] for value in end_tasks.values()],
              start_save_bytes=(artifacts / (stage + '-start.sav')).stat().st_size,
              end_save_bytes=(artifacts / (stage + '-year-complete.sav')).stat().st_size,
              end_gamestate_bytes=end['gamestate_bytes'])
r.harness.write_json(receipt, report)
print(json.dumps({key: value for key, value in report.items() if key != 'samples'}, ensure_ascii=False), flush=True)
