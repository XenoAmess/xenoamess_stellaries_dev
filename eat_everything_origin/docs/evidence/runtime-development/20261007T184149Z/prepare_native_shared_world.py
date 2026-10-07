import json
import logging
import sys

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--vanilla']
import runtime as r

logging.disable(logging.INFO)
initial = json.loads((r.harness.load_run()[0] / 'vanilla-shared-world-native-initial.audit.json').read_text(encoding='utf-8'))
assert initial['date'] == '2200.01.01'
assert initial['countries']['0']['native']['num_sapient_pops'] == 5700
assert 'origin="origin_default"' in initial['countries']['0']['government']
assert initial['countries']['0']['variables'] == {}
assert initial['countries']['0']['flags'] == {}
assert initial['event_targets'] == []
command = (
    'effect save_global_event_target_as = perf_country '
    'capital_scope = { planet = { save_global_event_target_as = perf_mother } } '
    'while = { count = 50 random_galaxy_planet = { '
    'limit = { has_owner = no is_star = no is_colony = no is_artificial = no '
    'NOT = { is_planet_class = pc_gas_giant } solar_system = { has_owner = no } } '
    'change_pc = pc_continental set_planet_size = 20 clear_deposits = yes '
    'create_colony = { owner = event_target:perf_country species = event_target:perf_country } '
    'save_global_event_target_as = perf_source set_planet_flag = perf_constructed '
    'event_target:perf_mother = { random_owned_pop_group = { '
    'limit = { pop_group_size >= 100 is_same_species = owner.owner_main_species } '
    'resettle_pop_group = { POP_GROUP = this PLANET = event_target:perf_source AMOUNT = 100 } } } } } '
    'event_target:perf_source = { set_name = "Native-UI-Q20" }'
)
assert 'eep' not in command.lower()
r.harness.press_scan_code(0x29, 'vanilla-shared-world-native-prepare-open', 1)
r.harness.type_text(command, True, 'vanilla-shared-world-native-prepare50')
frame = r.gpu_capture('vanilla-shared-world-native-prepare50-console-result')
print(json.dumps({'image': frame['image'], 'rows': [x['text'] for x in frame['rows']]}, ensure_ascii=False), flush=True)
r.harness.press_scan_code(0x29, 'vanilla-shared-world-native-prepare-close', 1)
result = r.native_save('vanilla-shared-world-frozen50-unstarted', '2200.01.01', (0,))
sources = {key: value for key, value in result['planets'].items() if 'perf_constructed' in value['flags']}
mother = result['planets']['3']
mother_pop = sum(result['pop_groups'][str(key)]['size'] for key in result['colonies'][str(mother['colony'])]['pop_groups'])
source_pops = {key: sum(result['pop_groups'][str(group)]['size'] for group in result['colonies'][str(value['colony'])]['pop_groups']) for key, value in sources.items()}
assert len(sources) == 50, len(sources)
assert set(source_pops.values()) == {100}, source_pops
assert mother_pop == 700, mother_pop
assert result['countries']['0']['native']['num_sapient_pops'] == 5700
assert result['countries']['0']['stockpile'] == initial['countries']['0']['stockpile']
assert result['countries']['0']['variables'] == {}
assert result['countries']['0']['flags'] == {}
assert result['event_targets'] == []
assert result['situations'] == {}
assert all(value['planet_size'] == 20 and value['planet_class'] == 'pc_continental' for value in sources.values())
print(json.dumps({'date': result['date'], 'sha': result['save_sha256'], 'mother': 3, 'mother_size': mother['planet_size'], 'mother_pop': mother_pop, 'sources': source_pops, 'status': 'NATIVE_SHARED_WORLD_PRECONDITIONS_PASS'}, ensure_ascii=False))
