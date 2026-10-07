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
shutil.copyfile(Path(__file__), run / 'dual_owner_transfer_separate_system.py')
prepared = json.loads((run / 'rc7-dual-separate-system-source-starbase-prepared.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, prepared['countries']))
source = str(next(value['id'] for value in prepared['event_targets'] if value['name'] == 'eep_rc7_transfer_source'))
colony = str(prepared['planets'][source]['colony'])
def command(text, stage):
    h.press_scan_code(0x29, stage + '-console-open', 1)
    h.type_text(text, True, stage + '-command')
    r.gpu_capture(stage + '-console-result')
    h.press_scan_code(0x29, stage + '-console-close', 1)
def tasks(state):
    return [value for value in state['situations'].values() if value['type'] == 'situation_eep_devouring' and value.get('killed') != 'yes' and str(value['target']['id']) == source]
command('effect event_target:eep_probe_original_country = { every_situation = { limit = { is_situation_type = situation_eep_devouring target = { planet = { is_same_value = event_target:eep_rc7_transfer_source } } } add_situation_progress = 13 } }', 'rc7-dual-separate-old-task-control13')
old = r.native_save('rc7-dual-separate-old-task13-native', '2204.02.02', identities)
assert len(tasks(old)) == 1 and tasks(old)[0]['country'] == 0 and tasks(old)[0]['progress'] == 13
command('effect event_target:eep_rc7_transfer_source = { solar_system = { starbase = { set_owner = event_target:eep_probe_foreign } } set_owner = event_target:eep_probe_foreign }', 'rc7-dual-separate-starbase-and-source-transfer33')
transferred = r.native_save('rc7-dual-separate-starbase-source-owner33-native', '2204.02.02', identities)
assert transferred['planets'][source]['owner'] == 33
assert transferred['planets']['8']['owner'] == 0 and transferred['planets']['2014']['owner'] == 33
command('effect event_target:eep_rc7_transfer_source = { eep_begin = yes }', 'rc7-dual-separate-old-active-new-start-refused')
refused = r.native_save('rc7-dual-separate-old13-new-start-refused-native', '2204.02.02', identities)
assert len(tasks(refused)) == 1 and tasks(refused)[0]['country'] == 0 and tasks(refused)[0]['progress'] == 13
assert refused['colonies'][colony]['actual_pop_sum'] == 100
assert refused['colonies']['10']['actual_pop_sum'] == transferred['colonies']['10']['actual_pop_sum']
h.press_scan_code(0x29, 'rc7-dual-separate-day1-console-open', 1)
h.type_text('fast_forward 1', True, 'rc7-dual-separate-day1-calendar')
for attempt in range(12):
    frame = r.gpu_capture('rc7-dual-separate-day1-confirm-' + str(attempt))
    texts = [row['text'] for row in frame['rows']]
    if '2204.02.03' in texts and any('fastforwarded1days' in h.normalized(label) for label in texts):
        break
    time.sleep(5)
else:
    raise RuntimeError('separate transfer day1 not complete')
h.press_scan_code(0x29, 'rc7-dual-separate-day1-console-close', 1)
cleaned = r.native_save('rc7-dual-separate-day1-old-task-cleaned-native', '2204.02.03', identities)
assert not tasks(cleaned)
assert cleaned['planets'][source]['owner'] == 33
assert cleaned['colonies'][colony]['actual_pop_sum'] == 100
assert 'eep_active' not in cleaned['planets'][source]['flags']
command('effect event_target:eep_rc7_transfer_source = { eep_begin = yes }', 'rc7-dual-separate-new33-zero-founder-formal-begin')
started = r.native_save('rc7-dual-separate-new33-real100-seed-task0-native', '2204.02.03', identities)
assert len(tasks(started)) == 1 and tasks(started)[0]['country'] == 33 and tasks(started)[0]['progress'] == 0
assert started['colonies'][colony]['actual_pop_sum'] == 200
assert started['colonies']['10']['actual_pop_sum'] == cleaned['colonies']['10']['actual_pop_sum'] - 100
assert started['planets'][source]['variables']['eep_q'] == 20 and started['planets'][source]['variables']['eep_months'] == 48
assert all(started['countries']['0']['variables'][key] == value for key, value in [('eep_c', 20), ('eep_g', 0), ('eep_d', 7), ('eep_made', 0)])
assert all(started['countries']['33']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)])
assert sum(value['size'] for value in started['pop_groups'].values()) == sum(value['size'] for value in cleaned['pop_groups'].values())
assert all(started['countries'][str(identity)]['stockpile'] == cleaned['countries'][str(identity)]['stockpile'] for identity in (0, 33))
print(json.dumps({'phase': 'separate-system old13 cleaned new33 begins0 with100', 'source': source, 'colony': colony,
                  'start_sha256': started['save_sha256'], 'new_mother_population': started['colonies']['10']['actual_pop_sum']}, ensure_ascii=False), flush=True)
