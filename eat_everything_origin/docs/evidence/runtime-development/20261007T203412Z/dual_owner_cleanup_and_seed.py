import json
import logging
from pathlib import Path
import shutil
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / 'dual_owner_cleanup_and_seed.py')
previous = json.loads((run / 'rc7-dual-source13-new-owner-native-state.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, previous['countries']))
def command(text, stage):
    h.press_scan_code(0x29, stage + '-console-open', 1)
    h.type_text(text, True, stage + '-command')
    r.gpu_capture(stage + '-console-result')
    h.press_scan_code(0x29, stage + '-console-close', 1)
def tasks(state):
    return [value for value in state['situations'].values() if value['type'] == 'situation_eep_devouring' and value.get('killed') != 'yes' and value['target']['id'] == 13]
command('effect event_target:eep_probe_source = { eep_begin = yes }', 'rc7-dual-new-owner-still-active-begin-refused')
refused = r.native_save('rc7-dual-new-owner-old-task13-begin-refused', '2204.01.02', identities)
assert len(tasks(refused)) == 1 and tasks(refused)[0]['country'] == 0 and tasks(refused)[0]['progress'] == 13
assert refused['colonies']['17']['actual_pop_sum'] == 100 and refused['colonies']['10']['actual_pop_sum'] == 6384
assert all(refused['countries'][str(identity)]['stockpile'] == previous['countries'][str(identity)]['stockpile'] for identity in (0, 33))
h.press_scan_code(0x29, 'rc7-dual-actual-day1-console-open', 1)
h.type_text('fast_forward 1', True, 'rc7-dual-natural-day1-submit')
for attempt in range(10):
    frame = r.gpu_capture('rc7-dual-natural-day1-confirm-' + str(attempt))
    texts = [row['text'] for row in frame['rows']]
    if '2204.01.03' in texts and any('fastforwarded1days' in h.normalized(label) for label in texts):
        break
    time.sleep(5)
else:
    raise RuntimeError('actual day1 did not complete')
h.press_scan_code(0x29, 'rc7-dual-actual-day1-console-close', 1)
cleaned = r.native_save('rc7-dual-real-day1-old-task-cleaned', '2204.01.03', identities)
assert not tasks(cleaned), tasks(cleaned)
assert 'eep_active' not in cleaned['planets']['13']['flags']
assert cleaned['planets']['13']['owner'] == 33 and cleaned['colonies']['17']['actual_pop_sum'] == 100
assert all(cleaned['countries']['0']['variables'][key] == value for key, value in [('eep_c', 20), ('eep_g', 0), ('eep_d', 7), ('eep_made', 0)])
assert all(cleaned['countries']['33']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)])
assert all(cleaned['pop_groups'][str(identity)]['key']['species'] == 48 for identity in cleaned['colonies']['17']['pop_groups'])
command('effect event_target:eep_probe_source = { eep_begin = yes }', 'rc7-dual-new-owner-zero-founder-formal-begin')
started = r.native_save('rc7-dual-new-owner44-actual100-seed-task0', '2204.01.03', identities)
assert len(tasks(started)) == 1 and tasks(started)[0]['country'] == 33 and tasks(started)[0]['progress'] == 0
assert started['colonies']['10']['actual_pop_sum'] == cleaned['colonies']['10']['actual_pop_sum'] - 100
assert started['colonies']['17']['actual_pop_sum'] == 200
groups = [started['pop_groups'][str(identity)] for identity in started['colonies']['17']['pop_groups']]
assert sum(value['size'] for value in groups if value['key']['species'] == 44) == 100
assert sum(value['size'] for value in groups if value['key']['species'] == 48) == 100
assert started['planets']['13']['variables']['eep_q'] == 20 and started['planets']['13']['variables']['eep_months'] == 48
assert next(value['id'] for value in started['event_targets'] if value['name'] == 'eep_task_actor13') == 33
assert all(started['countries'][str(identity)]['stockpile'] == cleaned['countries'][str(identity)]['stockpile'] for identity in (0, 33))
assert started['countries']['0']['variables'] == cleaned['countries']['0']['variables']
assert started['countries']['33']['variables'] == cleaned['countries']['33']['variables']
assert sum(value['size'] for value in started['pop_groups'].values()) == sum(value['size'] for value in cleaned['pop_groups'].values())
h.write_json(run / 'rc7-dual-source-owner-old13-new0-seed-result.json', {
    'status': 'PASS', 'scope': 'Controlled owner transfer/new task and actual zero-founder100 seed from new owner; settlement, twin reports and full Scorched Hive acceptance pending.',
    'old_progress': 13, 'new_progress': 0, 'new_owner': 33, 'source_id': 13, 'old_founder': 48, 'new_founder': 44,
    'refused_sha256': refused['save_sha256'], 'cleaned_sha256': cleaned['save_sha256'], 'started_sha256': started['save_sha256'],
    'mod_tree_sha256': manifest['copied_mod_tree_sha256']})
print(json.dumps({'phase': 'old13 cleared, new33 begins0 with actual100', 'sha256': started['save_sha256'], 'groups': groups, 'new_mother_population': started['colonies']['10']['actual_pop_sum']}, ensure_ascii=False), flush=True)
