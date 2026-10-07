import json
import logging
from pathlib import Path
import shutil
import sys
import zipfile
sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / 'start_dual_owner_case_recovered.py')
original = json.loads(Path('_runtime/heart-of-devouring/runs/20261007T154144Z/rc6-mixed-generic-q20-current-start-no-native-flag.all-countries.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, original['countries']))
def command(text, stage):
    h.press_scan_code(0x29, stage + '-console-open', 1)
    h.type_text(text, True, stage + '-command')
    r.gpu_capture(stage + '-console-result')
    h.press_scan_code(0x29, stage + '-console-close', 1)
command('play 0', 'rc7-dual-recover-player-control-country0')
restored = r.native_save('rc7-dual-controller0-native-all37', '2204.01.02', identities)
import audit_save as q
with zipfile.ZipFile(run / 'rc7-dual-controller0-native-all37.sav') as archive:
    player_block = q.block(archive.read('gamestate').decode('utf-8-sig'), 'player')
assert 'country=0' in player_block and 'country=16777218' not in player_block
assert restored['event_targets'] == original['event_targets']
assert restored['countries']['0']['stockpile'] == original['countries']['0']['stockpile']
assert restored['colonies']['10']['actual_pop_sum'] == 6384
assert restored['countries']['33']['native']['founder_species_ref'] == 44
assert 'civic_fanatic_purifiers' in restored['countries']['33']['government']
command('effect every_situation = { limit = { is_situation_type = situation_eep_devouring target = { planet = { is_same_value = event_target:eep_probe_source } } } add_situation_progress = 13 }', 'rc7-dual-old-task-progress13-recovered-control')
before = r.native_save('rc7-dual-old-task-progress13-recovered-no-credit', '2204.01.02', identities)
assert len([value for value in before['situations'].values() if value['type'] == 'situation_eep_devouring' and value['progress'] == 13]) == 1
assert before['countries']['0']['variables']['eep_c'] == 20
command('effect event_target:eep_probe_foreign = { set_origin = origin_heart_of_devouring eep_initialize = yes }', 'rc7-dual-qualified33-controlled-origin-initialize')
initialized = r.native_save('rc7-dual-two-bound-cores-native-initialized', '2204.01.02', identities)
assert initialized['countries']['0'] == before['countries']['0']
assert initialized['countries']['33']['stockpile'] == before['countries']['33']['stockpile']
assert initialized['colonies']['10']['actual_pop_sum'] == 6384
assert initialized['planets']['2014']['planet_size'] == 30
assert all(initialized['countries']['33']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)])
targets = {value['name']: value for value in initialized['event_targets']}
assert targets['eep_core0']['id'] == 8 and targets['eep_core33']['id'] == 2014
assert targets['eep_core_actor8']['id'] == 0 and targets['eep_core_actor2014']['id'] == 33
command('event eep_probe.25', 'rc7-dual-transfer-existing-source13-to33')
transferred = r.native_save('rc7-dual-source13-new-owner-native-state', '2204.01.02', identities)
assert transferred['planets']['13']['owner'] == 33
assert transferred['countries']['0']['variables']['eep_c'] == 20 and transferred['countries']['0']['variables']['eep_g'] == 0 and transferred['countries']['0']['variables']['eep_d'] == 7
print(json.dumps({'phase': 'source transferred to qualified33', 'save_sha256': transferred['save_sha256'],
                  'source': transferred['planets']['13'], 'source_groups': [transferred['pop_groups'][str(identity)] for identity in transferred['colonies']['17']['pop_groups']],
                  'situations': transferred['situations'], 'new_mother_pop': transferred['colonies']['10']['actual_pop_sum']}, ensure_ascii=False), flush=True)
