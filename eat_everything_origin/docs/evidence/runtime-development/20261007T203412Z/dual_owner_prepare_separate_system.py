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
shutil.copyfile(Path(__file__), run / 'dual_owner_prepare_separate_system.py')
previous = json.loads((run / 'rc7-dual-first-month-foreign-rights-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, previous['countries']))
def command(text, stage):
    h.press_scan_code(0x29, stage + '-console-open', 1)
    h.type_text(text, True, stage + '-command')
    r.gpu_capture(stage + '-console-result')
    h.press_scan_code(0x29, stage + '-console-close', 1)
h.press_scan_code(0x29, 'rc7-dual-reannex-day-console-open', 1)
h.type_text('fast_forward 1', True, 'rc7-dual-reannex-real-next-day')
for attempt in range(12):
    frame = r.gpu_capture('rc7-dual-reannex-next-day-confirm-' + str(attempt))
    texts = [row['text'] for row in frame['rows']]
    if '2204.02.02' in texts and any('fastforwarded1days' in h.normalized(label) for label in texts):
        break
    time.sleep(5)
else:
    raise RuntimeError('reannex next actual day did not complete')
h.press_scan_code(0x29, 'rc7-dual-reannex-day-console-close', 1)
cleaned = r.native_save('rc7-dual-native-reannex-invalid33-task-cleared', '2204.02.02', identities)
assert not [value for value in cleaned['situations'].values() if value['type'] == 'situation_eep_devouring' and value.get('killed') != 'yes' and value['target']['id'] == 13]
assert all(cleaned['countries']['33']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)])
command('effect event_target:eep_probe_original_country = { save_event_target_as = eep_probe_country eep_probe_galaxy_batch = { SIZE = 20 COUNT = 1 COMPLETE = no } } event_target:eep_probe_batch_source = { save_global_event_target_as = eep_rc7_transfer_source solar_system = { save_global_event_target_as = eep_rc7_transfer_system if = { limit = { NOT = { exists = starbase } } create_starbase = { size = starbase_outpost owner = event_target:eep_probe_original_country } } starbase = { save_global_event_target_as = eep_rc7_transfer_starbase } } }', 'rc7-dual-separate-system-real100-control-outpost')
prepared = r.native_save('rc7-dual-separate-system-source-starbase-prepared', '2204.02.02', identities)
targets = {value['name']: value for value in prepared['event_targets']}
source = str(targets['eep_rc7_transfer_source']['id'])
planet = prepared['planets'][source]
colony = str(planet['colony'])
assert source not in ('8', '13', '2014')
assert planet['owner'] == 0 and planet['planet_size'] == 20
assert prepared['colonies'][colony]['actual_pop_sum'] == 100
assert prepared['colonies']['0']['actual_pop_sum'] == cleaned['colonies']['0']['actual_pop_sum'] - 100
assert sum(value['size'] for value in prepared['pop_groups'].values()) == sum(value['size'] for value in cleaned['pop_groups'].values())
assert prepared['countries']['0']['stockpile'] == cleaned['countries']['0']['stockpile']
assert prepared['planets']['8']['owner'] == 0 and prepared['planets']['2014']['owner'] == 33
print(json.dumps({'phase': 'separate unowned system controlled source and outpost', 'source_id': source,
                  'source_colony': colony, 'targets': [value for value in targets.values() if value['name'].startswith('eep_rc7_transfer')],
                  'sha256': prepared['save_sha256']}, ensure_ascii=False), flush=True)
