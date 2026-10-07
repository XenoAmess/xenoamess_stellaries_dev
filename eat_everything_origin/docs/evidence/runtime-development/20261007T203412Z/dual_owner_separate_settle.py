import json
import logging
from pathlib import Path
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
before = json.loads((run / 'rc7-dual-separate-first-month-stable-owner33-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, before['countries']))
assert before['planets']['196']['owner'] == 33
assert before['colonies']['19']['actual_pop_sum'] == 100
groups = [before['pop_groups'][str(identity)] for identity in before['colonies']['19']['pop_groups']]
assert all(group['key']['species'] == 44 and group['key']['category'] != 'purge' for group in groups)
h.press_scan_code(0x29, 'rc7-dual-separate-control-endpoint-console-open', 1)
h.type_text('effect event_target:eep_probe_foreign = { every_situation = { limit = { is_situation_type = situation_eep_devouring target = { planet = { is_same_value = event_target:eep_rc7_transfer_source } } } add_situation_progress = 47 situation_event = { id = eep.21 } } }', True, 'rc7-dual-separate-control-endpoint48-settle')
r.gpu_capture('rc7-dual-separate-control-endpoint-console-result')
h.press_scan_code(0x29, 'rc7-dual-separate-control-endpoint-console-close', 1)
after = r.native_save('rc7-dual-separate-new33-settled-old0-isolated-native', '2204.03.01', identities)
assert after['planets']['196']['planet_class'] == 'pc_shattered'
assert after['countries']['0']['variables'] == before['countries']['0']['variables']
assert all(after['countries']['33']['variables'][key] == value for key, value in [('eep_c', 20), ('eep_g', 20), ('eep_d', 7), ('eep_made', 300), ('eep_worlds', 1), ('eep_last_return', 100), ('eep_last_manufactured', 300)])
assert after['colonies']['10']['actual_pop_sum'] == before['colonies']['10']['actual_pop_sum'] + 400
assert after['colonies']['0']['actual_pop_sum'] == before['colonies']['0']['actual_pop_sum']
assert all(after['countries'][str(identity)]['stockpile'] == before['countries'][str(identity)]['stockpile'] for identity in (0, 33))
assert all(after['countries'][str(identity)] == before['countries'][str(identity)] for identity in identities if identity not in (0, 33))
assert sum(value['size'] for value in after['pop_groups'].values()) == sum(value['size'] for value in before['pop_groups'].values()) + 300
print(json.dumps({'phase': 'CONTROL endpoint48 actual settlement with two independent cores', 'save_sha256': after['save_sha256'], 'old0_core_population': after['colonies']['0']['actual_pop_sum'], 'new33_core_population': after['colonies']['10']['actual_pop_sum'], 'new33': after['countries']['33']['variables']}, ensure_ascii=False), flush=True)
