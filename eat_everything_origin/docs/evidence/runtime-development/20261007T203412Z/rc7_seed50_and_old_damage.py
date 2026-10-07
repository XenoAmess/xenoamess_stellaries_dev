import json
import logging
from pathlib import Path
import shutil
import sys

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / 'rc7_seed50_and_old_damage.py')
def command(text, stage):
    h.press_scan_code(0x29, stage + '-console-open', 1)
    h.type_text(text, True, stage + '-command')
    r.gpu_capture(stage + '-console-result')
    h.press_scan_code(0x29, stage + '-console-close', 1)
loaded = r.native_load('eep-zero', 'rc7-seed50-restore-common-zero')
assert loaded['source_sha256'] == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5'
command('effect random_owned_colony = { limit = { has_planet_flag = perf_constructed eep_source_valid = yes } planet = { save_global_event_target_as = eep_rc7_seed_case } random_owned_pop_group = { limit = { eep_founder_pop = yes pop_group_size = 100 } resettle_pop_group = { POP_GROUP = this PLANET = event_target:eep_core@root AMOUNT = 50 } } }', 'rc7-seed50-actual-half-return')
half = r.native_save('rc7-seed50-native-precondition', '2200.01.01', (0,))
source = str(next(value['id'] for value in half['event_targets'] if value['name'] == 'eep_rc7_seed_case'))
colony = str(half['planets'][source]['colony'])
assert half['colonies'][colony]['actual_pop_sum'] == 50, (source, half['colonies'][colony])
assert half['colonies']['0']['actual_pop_sum'] == 750
assert half['countries']['0']['native']['num_sapient_pops'] == 5700
command('effect event_target:eep_rc7_seed_case = { eep_begin = yes }', 'rc7-seed50-formal-begin')
filled = r.native_save('rc7-seed50-formal-start-refilled-only50', '2200.01.01', (0,))
assert filled['colonies'][colony]['actual_pop_sum'] == 100
assert filled['colonies']['0']['actual_pop_sum'] == 700
assert filled['countries']['0']['stockpile'] == half['countries']['0']['stockpile']
assert filled['countries']['0']['native']['num_sapient_pops'] == 5700
assert filled['planets'][source]['variables']['eep_q'] == 20
assert filled['planets'][source]['variables']['eep_months'] == 48
assert len([value for value in filled['situations'].values() if value['type'] == 'situation_eep_devouring' and value['progress'] == 0]) == 1
print(json.dumps({'case': 'actual50 seed replenished only50', 'source': source, 'before_sha256': half['save_sha256'], 'after_sha256': filled['save_sha256']}), flush=True)
old_original = json.loads(Path('_runtime/heart-of-devouring/runs/20261007T154144Z/rc6-native-old-damage-day1-before-restart.audit.json').read_text(encoding='utf-8'))
loaded = r.native_load('old-damage', 'rc7-old-damage-original-restored')
assert loaded['source_sha256'] == old_original['save_sha256']
before = r.native_save('rc7-old-damage6-native-before-restart', old_original['date'], (0,))
assert before['countries']['0']['stockpile'] == old_original['countries']['0']['stockpile']
assert len([value for value in before['deposits'].values() if value['type'] == 'd_lithoid_devastation' and value['deposit_holder']['id'] == 3]) == 6
command('event eep_probe.24', 'rc7-old-damage6-formal-restart')
after = r.native_save('rc7-old-damage6-native-restarted-q14-t34', before['date'], (0,))
assert after['planets']['3']['variables']['eep_q'] == 14
assert after['planets']['3']['variables']['eep_months'] == 34
assert after['countries']['0']['stockpile'] == before['countries']['0']['stockpile']
assert after['countries']['0']['native']['num_sapient_pops'] == before['countries']['0']['native']['num_sapient_pops']
assert after['countries']['0']['variables']['eep_c'] == after['countries']['0']['variables']['eep_g'] == after['countries']['0']['variables']['eep_made'] == 0
assert len([value for value in after['situations'].values() if value['type'] == 'situation_eep_devouring' and value['progress'] == 0]) == 1
h.write_json(run / 'rc7-seed50-and-positive-old-damage-mechanism-result.json', {
    'status': 'PASS', 'scope': 'Controlled actual50 seed refill and positive old-damage6 restart only; zero founder/new owner and Scorched Hive full acceptance remain pending.',
    'version': '0.2.0-rc.7', 'mod_tree_sha256': manifest['copied_mod_tree_sha256'],
    'seed50_source_id': source, 'seed50_before_sha256': half['save_sha256'], 'seed50_after_sha256': filled['save_sha256'],
    'old_damage_before_sha256': before['save_sha256'], 'old_damage_after_sha256': after['save_sha256'],
    'old_damage_q': 14, 'old_damage_months': 34})
print(json.dumps({'case': 'actual old damage6', 'q': 14, 'months': 34, 'sha256': after['save_sha256']}), flush=True)
