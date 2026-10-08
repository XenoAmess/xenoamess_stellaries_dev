"""Controlled boundary setup; never claims a natural 39-month progression."""
import json
import logging
from pathlib import Path
import shutil
import sys

start = sys.argv[1]
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
copy = run / Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__), copy)
a = json.loads((run / (start + '.audit.json')).read_text(encoding='utf-8'))
assert a['date'] == '2223.12.02'
c = a['countries']['0']
assert a['colonies']['24']['actual_pop_sum'] == 69
assert set(c['owned_colonies']) == {0,24}
assert c['variables']['eep_c'] == c['variables']['eep_g'] == 0
assert not any(s.get('type') == 'situation_eep_devouring' for s in a['situations'].values())
frame = r.gpu_capture('rc9-focus-recovered-wait-setup-before')
labels = [v['text'] for v in frame['rows']]
assert '2223.12.02' in labels and '暂停' in labels
h.press_scan_code(0x29, 'rc9-focus-recovered-wait-setup-console-open', 1)
commands = [
    'effect root = { every_owned_planet = { limit = { is_capital = no } planet = { save_global_event_target_as = eep_native_purge_source set_name = "EEP-PURGE-16" eep_begin = yes } } }',
    'effect root = { random_country = { limit = { is_country_type = default is_gestalt = no owner_main_species = { has_trait = trait_organic NOT = { has_trait = trait_hive_mind } } } owner_main_species = { save_global_event_target_as = eep_native_purge_species } } }',
    'effect root = { event_target:eep_native_purge_source = { create_pop_group = { species = event_target:eep_native_purge_species size = 1200 } } }',
    'effect root = { every_situation = { limit = { is_situation_type = situation_eep_devouring } add_situation_progress = 38 } }',
]
for n, command in enumerate(commands):
    h.type_text(command, True, 'rc9-focus-recovered-wait-controlled-precondition-' + str(n))
receipt = r.gpu_capture('rc9-focus-recovered-wait-setup-console-receipt')
h.press_scan_code(0x29, 'rc9-focus-recovered-wait-setup-console-close', 1)
after = r.native_save('rc9-focus-valid-wait-purge-month38', '2223.12.02', (0,))
checks = {'one_task':sum(s.get('type') == 'situation_eep_devouring' for s in after['situations'].values()) == 1, 'source_seed100_plus_foreign1200':after['colonies']['24']['actual_pop_sum'] == 1300, 'mother_minus31':after['colonies']['0']['actual_pop_sum'] == 7721, 'q16_t39':after['planets']['84']['variables'].get('eep_q') == 16 and after['planets']['84']['variables'].get('eep_months') == 39, 'active': 'eep_active' in after['planets']['84']['flags'], 'no_preaward':all(after['countries']['0']['variables'][k] == c['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds'])}
h.write_json(run / 'rc9-focus-valid-wait-setup-preconditions.json', {'status':'CONTROLLED_VALID_TASK_SETUP' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':after['save_sha256']})
assert all(checks.values()), 'Valid task setup was not achieved.'
h.write_json(run / 'rc9-focus-recovered-wait-purge-setup-kind.json', {
    'status':'CONTROLLED_SETUP_SAVED', 'date':after['date'],'save_sha256':after['save_sha256'],
    'source_physical_id':84,'source_colony_id':24,'original_founder_population':69,
    'expected_formal_seed_topup_from_mother':31,'controlled_foreign_population_created':1200,
    'controlled_situation_progress_added':38,
    'scope':'Only setup. Must read real species rights, seed transfer and progress, then actual month39, waiting reload and natural purge settlement.'})
print(json.dumps({'date':after['date'],'save_sha256':after['save_sha256'],
                  'source':after['colonies'].get('24'),'situations':after['situations']},ensure_ascii=True),flush=True)
