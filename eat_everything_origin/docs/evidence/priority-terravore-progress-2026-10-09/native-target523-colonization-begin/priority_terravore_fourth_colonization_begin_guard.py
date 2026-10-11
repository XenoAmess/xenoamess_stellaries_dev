"""Independent actual colony-begin component; original travel failure retained."""
import json
import logging
import sys
import zipfile

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda name: json.loads((run / name).read_text('utf-8'))
before = 'terravore-fourth-target523-colonization-ordered'
after = 'terravore-fourth-colonizer-native-travel-first90'
obs = load(after + '-construction-boundary-observation.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
bc, ac = ba['countries']['0'], aa['countries']['0']
failed = load(after + '-target523-travel-core-proof.json')
fe = load(after + '-travel-core-guard-execution.json')
order = load(before + '-target523-colonization-order-proof.json')
order_ex = load(before + '-order-guard-v2-execution.json')
inv_name = after + '-native-colonization-begin-investigation.json'
inv = load(inv_name)
with zipfile.ZipFile(run / (after + '.sav')) as archive:
    text = archive.read('gamestate').decode('utf-8-sig')
roots = {k: v for k, v, o in q.fields(text) if o}
colony = q.block(roots['colony'], '38')
target = a['planet_raw']['523']
ts = q.scalars(target)
new_jobs = {i: job for i, job in aa['pop_jobs'].items() if i not in ba['pop_jobs']}
mother_jobs = [{i: job for i, job in audit['pop_jobs'].items() if job['planet'] == 0} for audit in [ba, aa]]

def structure(st):
    audit = st['audit']
    districts = audit['colonies']['0']['districts']
    zones = {i for d in districts for i in audit['districts'][str(d)]['zones'] if i != 4294967295}
    buildings = {i for z in zones for i in q.ids(q.block(q.block(st['raw_roots']['zones'], str(z)), 'buildings'))}
    ids = {'districts': districts, 'zones': sorted(zones), 'buildings': sorted(buildings), 'deposit': audit['planets']['7']['deposits']}
    return {root: {str(i): q.block(st['raw_roots'][root], str(i)) for i in values} for root, values in ids.items()}

def none_entry(root, identity):
    return [(v, o) for k, v, o in q.fields(root) if k == identity] == [('none', False)]

mod_flags = lambda st: [(k, v, o) for k, v, o in q.fields(q.block(st['country0_raw'], 'flags')) if k.startswith('eep_')]
old_designs, new_designs = [q.block(st['country0_raw'], 'ship_design_collection') for st in [b, a]]
backup_raw = a['owned_ships_raw'].get('50333283', '')
backup = q.scalars(backup_raw)
failed_names = {'EEP_full_variables_flags_one_colony_species73_held', 'mother18_D14_paid27_structure_jobs_held', 'original_paid_births_species_design_health_identity_held', 'real_reachable_target523_before_arrival_no_colony_progress', 'owned_designs_held_no_unpaid_new_owned_ship'}
tree, tree_sha = h.tree_manifest(h.MOD_ROOT)
checks = {
    'original_travel19_exact5_FAIL_actual1_source_original_SAVs_retained': failed['status'] == 'FAIL' and len(failed['checks']) == 19 and {k for k, v in failed['checks'].items() if v is not True} == failed_names and fe['returncode'] == 1 and fe['helper_sha256'] == h.sha256(run / 'priority_terravore_fourth_colonizer_travel_core_guard.py') == 'f5f3ebf4e8fc327394edf3b10c12cdae95f3070b637df2de5b125746514bb2f7' and failed['before_sha256'] == ba['save_sha256'] and failed['after_sha256'] == aa['save_sha256'] and not failed['boundaries'],
    'original16_existing_paid_order_PASS_actual0_source': len(order['checks']) == 16 and all(v is True for v in order['checks'].values()) and order_ex['returncode'] == 0 and order_ex['helper_sha256'] == h.sha256(run / 'priority_terravore_fourth_colonization_order_guard_v2.py') == '413cafbe0f55610cc5e70f8d38d2429a8e1519d426674dd88b974e08719d506e' and order['after_sha256'] == ba['save_sha256'] and order['paid_births'] == failed['paid_births'],
    'original_SAV_pair_and_complete_colony_investigation_bound': ba['save_sha256'] == h.sha256(run / (before + '.sav')) == '7b01568d2ee040befbdcfb2bd17cbf394bd35798026829f08afff38081665887' and aa['save_sha256'] == h.sha256(run / (after + '.sav')) == 'b49e98ee96d7105be8ded1923fc22ba61cc2c220da90515b283112f152bd0476' and h.sha256(run / inv_name) == 'f631c55aa58f7904ef7e50618fc815d0c17f9462f0a8f1e60681c3af27af07dc' and inv['before_sha256'] == ba['save_sha256'] and inv['after_sha256'] == aa['save_sha256'] and colony == inv['colony38_raw'],
    'unique_native_target523_colony38_founding_date_zero_pop': ba['date'] == '2273.08.28' and aa['date'] == '2273.11.28' and bc['owned_colonies'] == [0] and ac['owned_colonies'] == [0, 38] and all(ts[k] == v for k, v in {'owner': 0, 'controller': 0, 'colony': 38, 'planet_size': 13, 'planet_class': 'pc_tropical', 'colonize_date': '2273.11.26'}.items()) and q.scalars(colony)['colonizing_species'] == 73 and q.scalars(q.block(colony, 'carrier')) == {'type': 'planet', 'reference': 523} and aa['colonies']['38']['actual_pop_sum'] == 0 and not inv['colony38_before_entry'],
    'only_original_paid_ship_fleet_consumed_no_new_owned_ship': none_entry(roots['ships'], '16779032') and none_entry(roots['fleet'], '863') and set(a['owned_ship_ids']) == set(b['owned_ship_ids']) - {16779032} and set(b['owned_fleets']) - set(a['owned_fleets']) == {863} and not set(a['owned_fleets']) - set(b['owned_fleets']),
    'all_original_designs_retained_and_backup_paid_ship_alive': old_designs == new_designs and all(q.block(b['raw_roots']['ship_design'], str(i)) == q.block(a['raw_roots']['ship_design'], str(i)) for i in q.ids(q.block(old_designs, 'ship_design'))) and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][sid], 'ship_design_implementation') for sid, raw in a['owned_ships_raw'].items()) and backup.get('fleet') == 33555294 and backup.get('construction_date') == '2273.06.28' and q.scalars(q.block(backup_raw, 'colonization_data')) == {'species': 73} and all(backup.get(k) == v for k, v in [('hitpoints', 625), ('armor_hitpoints', 125), ('shield_hitpoints', 320)]) and q.scalars(q.block(q.block(a['owned_fleets_raw'].get('33555294', ''), 'movement_manager'), 'coordinate')).get('origin') == 0,
    'EEP_variables_flags_C49_D14_worlds3_PSI1_no_repeat_return': bc['variables'] == ac['variables'] and mod_flags(b) == mod_flags(a) and all(ac['variables'][k] == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_worlds': 3, 'eep_psi': 1, 'eep_stage': 1, 'eep_fleet_stage': 0}.items()) and a['species_population_by_colony'] == {'0:73': 11229},
    'mother_only_structure_paid27_and_jobs_held': structure(b) == structure(a) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts']) == 27 and mother_jobs[0].keys() == mother_jobs[1].keys() and all({k: v for k, v in job.items() if k not in {'workforce', 'bonus_workforce'}} == {k: v for k, v in mother_jobs[1][i].items() if k not in {'workforce', 'bonus_workforce'}} for i, job in mother_jobs[0].items()) and aa['planets']['7']['planet_size'] == 18 and 'eep_core' in aa['planets']['7']['flags'] and not any(k == 'eep_core' for k, v, o in q.fields(q.block(target, 'flags'))),
    'exact_native_new38_three_zero_jobs_one_hive_district_capital': set(ba['pop_jobs']) <= set(aa['pop_jobs']) and len(new_jobs) == 3 and {(job['type'], job['max_workforce']) for job in new_jobs.values()} == {('logistics_drone', 200), ('patrol_drone', 100), ('coordinator', 200)} and all(job['planet'] == 38 and job['workforce'] == job['bonus_workforce'] == 0 for job in new_jobs.values()) and aa['colonies']['38']['districts'] == [71] and aa['districts']['71']['type'] == 'district_hive' and aa['districts']['71']['level'] == 1 and aa['districts']['71']['zones'] == [108, 4294967295, 4294967295] and q.scalars(q.block(a['raw_roots']['buildings'], '33554504'))['type'] == 'building_hive_capital',
    'known_native_pending_unchanged_no_new_Mod_boundary': a['pending_country0_raw'] == b['pending_country0_raw'] and not failed['boundaries'] and failed['actual_population'] == 11229 and ac['effective_stockpile']['menace'] == 885,
    'production41_Chinese_and_original_error_held': meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese' and len(tree) == 41 and tree_sha == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_TERRAVORE_TARGET523_COLONIZATION_BEGIN_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'], 'date': aa['date'],
         'paid_births': order['paid_births'], 'native_colonization_calendar_ready': passed,
         'maximum_days_to_colonization_boundary': 21 if passed else 0,
         'original_travel19_passed_checks': {k: v for k, v in failed['checks'].items() if v is True},
         'actual_colony': 38, 'actual_physical_planet': 523, 'actual_founding_date': ts['colonize_date'],
         'actual_mother_population': 11229, 'actual_colony_population': 0,
         'current_UI_completion_estimate': '2276.02.01',
         'current_UI_image_sha256': h.sha256(run / 'terravore-fourth-colony-begin-progress-tooltip-ui.jpg'),
         'current_UI_OCR_sha256': h.sha256(run / 'terravore-fourth-colony-begin-progress-tooltip-ui.ocr.json'),
         'scope': 'Actual legal native colony begin only. Prior travel19 remains FAIL. No colony completion, swallow, queen high milestone or full acceptance.'}
output = run / (after + '-target523-colonization-begin-proof.json')
assert not output.exists()
h.write_json(output, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True], 'colony': 38, 'founding_date': ts['colonize_date'], 'native_UI_completion_estimate': proof['current_UI_completion_estimate']}, ensure_ascii=True), flush=True)
assert passed
