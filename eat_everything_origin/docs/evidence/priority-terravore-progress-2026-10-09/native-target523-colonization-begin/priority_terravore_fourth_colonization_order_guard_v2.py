"""Documented native command of the existing paid ship, without a new payment."""
import itertools
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
before = 'terravore-rear-colonizer4-native-birth'
after = 'terravore-fourth-target523-colonization-ordered'
omit = lambda raw, keys: [(k, v, o) for k, v, o in q.fields(raw) if k not in keys]

def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as archive:
        text = archive.read('gamestate').decode('utf-8-sig')
    roots = {k: v for k, v, o in q.fields(text) if o}
    audit = load(stage + '.audit.json')
    assert h.sha256(run / (stage + '.sav')) == audit['save_sha256']
    return text, roots, audit

bt, br, ba = read(before)
at, ar, aa = read(after)
pre = load(before + '-paid-colonizer-lifecycle-v3-proof.json')
pe = load(before + '-lifecycle-core-guard-v3-execution.json')
se = load(after + '-native-save-execution.json')
bc, ac = [audit['countries']['0'] for audit in [ba, aa]]
old, new = [q.block(roots['fleet'], '863') for roots in [br, ar]]
bm, am = [q.block(fleet, 'movement_manager') for fleet in [old, new]]
order = q.block(q.block(new, 'current_order'), 'colonize_planet_order')
path = q.block(am, 'path')
origins = [q.scalars(q.block(v, 'coordinate'))['origin'] for k, v, o in q.fields(path) if k == 'node' and o]
route = [key for key, group in itertools.groupby(origins)]
old_bases, new_bases = [q.block(roots['starbase_mgr'], 'starbases') for roots in [br, ar]]
old_base, new_base = [q.block(bases, '153') for bases in [old_bases, new_bases]]
ship = q.block(ar['ships'], '16779032')
ss = q.scalars(ship)
target = q.block(q.block(ar['planets'], 'planet'), '523')
ts = q.scalars(target)
actions = [
    ('terravore-fourth-target-select-rear-paid-colonizer', 'left-click', [900, 542]),
    ('terravore-fourth-target-colonizer-context', 'right-click', [578, 470]),
    ('terravore-fourth-target-order-colonize-existing-ship', 'left-click', [620, 500]),
    ('terravore-fourth-target-confirm-existing-ship-colonization', 'left-click', [804, 603]),
    ('terravore-fourth-target-confirm-default-colony-name', 'left-click', [592, 420]),
]
def actions_ok():
    for stage, mode, point in actions:
        action = load(stage + '.action.json')
        execution = load(stage + '-input-execution.json')
        if not (action['action'] == mode and action['client_point'] == point
                and execution['returncode'] == 0 and execution['helper_sha256'] == h.sha256(run / 'priority_native_ui_input_v3.py') == '801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f'):
            return False
    return True

checks = {
    'prior_birth26_PASS_actual0_original_source_SHA': pre['status'] == 'PASS_NATIVE_TERRAVORE_PAID_COLONIZER_LIFECYCLE_CORE_COMPONENT' and len(pre['checks']) == 26 and all(v is True for v in pre['checks'].values()) and pe['returncode'] == 0 and pe['helper_sha256'] == h.sha256(run / 'priority_terravore_paid_colonizers_lifecycle_core_guard_v3.py') == '98c2c63a0c409f3bb8670f102d8bcfd3ee0fce8eb24561506dd3222e0165a43a' and pre['after_sha256'] == ba['save_sha256'] == '456b1c2f10ab0e71fb8c258d6ed4dd262f79f79ec4e897b16a86cc7ff8859c39',
    'same_day_original_save_actual0_source_SHA': ba['date'] == aa['date'] == '2273.08.28' and aa['save_sha256'] == '7b01568d2ee040befbdcfb2bd17cbf394bd35798026829f08afff38081665887' and se['returncode'] == 0 and se['helper_sha256'] == h.sha256(run / 'priority_native_save.py') == '19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e',
    'complete_actual_diff_investigation_bound': h.sha256(run / (after + '-same-day-full-order-investigation.json')) == '274aa962bcb9ccac441e48d94f2de9d798d262ea6fdb008da9f3ae7470bef80b',
    'production41_original_tree_simp_chinese': meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41 and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
    'five_normal_existing_ship_UI_actions_actual0_source': actions_ok(),
    'all_countries_and_true_resources_research_raw_held': br['country'] == ar['country'] and bc['effective_stockpile'] == ac['effective_stockpile'] and bc['research_stockpile'] == ac['research_stockpile'],
    'only_original_fleet863_three_command_fields': omit(br['fleet'], {'863'}) == omit(ar['fleet'], {'863'}) and omit(old, {'current_order', 'order_id', 'movement_manager'}) == omit(new, {'current_order', 'order_id', 'movement_manager'}) and q.ids(q.block(old, 'ships')) == q.ids(q.block(new, 'ships')) == [16779032] and not q.block(old, 'current_order') and not q.block(new, 'order') and q.scalars(old).get('order_id', 0) == 0 and q.scalars(new)['order_id'] == 1,
    'all_original_ship_entities_raw_held_and_paid_identity': br['ships'] == ar['ships'] and pre['paid_births']['50331690']['ship_id'] == 16779032 and pre['paid_births']['50331690']['fleet_id'] == ss['fleet'] == 863 and q.scalars(q.block(ship, 'colonization_data')) == {'species': 73} and q.scalars(q.block(ship, 'ship_design_implementation')) == {'design': 150995039, 'upgrade': 4294967295, 'growth_stage': 0} and ss['construction_date'] == '2273.08.28' and all(ss[k] == value for k, value in [('hitpoints', 625), ('armor_hitpoints', 125), ('shield_hitpoints', 320)]),
    'exact_single_reachable_colonize523_native_default_name': [(k, o) for k, v, o in q.fields(q.block(new, 'current_order'))] == [('colonize_planet_order', True)] and q.scalars(order) == {'planet': 523, 'progress': 0, 'can_reach': 'yes', 'order_id': 0, 'commissioner': 4294967295} and q.scalars(q.block(order, 'name')) == {'key': 'NEW_COLONY_NAME_1'} and 'key="Yomon"' in q.block(order, 'name'),
    'native_path97_to37_actual_ETA_and_no_teleport': route == [97, 37] and q.scalars(path)['date'] == '2274.01.29' and q.block(bm, 'coordinate') == q.block(am, 'coordinate') and q.scalars(q.block(am, 'coordinate')).get('origin') == 97 and q.scalars(q.block(am, 'target_coordinate')) == {'x': -47.2722, 'y': 110.9877, 'origin': 37} and omit(bm, {'target', 'target_coordinate', 'path', 'orbit'}) == omit(am, {'target', 'target_coordinate', 'path', 'orbit'}),
    'original_base153_only_exact_departure_orbital_registration': omit(br['starbase_mgr'], {'starbases'}) == omit(ar['starbase_mgr'], {'starbases'}) and omit(old_bases, {'153'}) == omit(new_bases, {'153'}) and omit(old_base, {'orbitals'}) == omit(new_base, {'orbitals'}) and q.scalars(q.block(old_base, 'orbitals')) == {'0': 863} and q.scalars(q.block(new_base, 'orbitals')) == {'0': 4294967295},
    'all_planets_raw_held_target523_tropical13_uncolonized': br['planets'] == ar['planets'] and ts['planet_class'] == 'pc_tropical' and ts['planet_size'] == 13 and 'owner' not in ts and 'colony' not in ts and q.scalars(q.block(target, 'coordinate'))['origin'] == 37,
    'other_all_top_ordered_state_held_no_new_build_payment_or_pending': omit(bt, {'random_count', 'fleet', 'starbase_mgr', 'camera_focus'}) == omit(at, {'random_count', 'fleet', 'starbase_mgr', 'camera_focus'}),
    'exact_native_path_random_plus4_and_camera97_to37': q.scalars(bt)['random_count'] == 258374446 and q.scalars(at)['random_count'] == 258374450 and q.scalars(bt)['camera_focus'] == 97 and q.scalars(at)['camera_focus'] == 37,
    'mother11209_EEP_C49_D14_worlds3_PSI1_Menace885_held': all(bc['variables'][k] == ac['variables'][k] == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_worlds': 3, 'eep_psi': 1}.items()) and ba['colonies']['0']['actual_pop_sum'] == aa['colonies']['0']['actual_pop_sum'] == 11209 and ac['effective_stockpile']['menace'] == 885,
    'unfiltered_original2814_error_no_increment': (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes() == (run / (after + '-error-after.log')).read_bytes() and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_TERRAVORE_TARGET523_COLONIZATION_ORDER_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
         'date': aa['date'], 'paid_births': pre['paid_births'], 'actual_native_route': route,
         'actual_native_arrival_estimate': q.scalars(path)['date'], 'native_colony_travel_calendar_ready': passed,
         'maximum_days_to_travel_boundary': 90 if passed else 0,
         'scope': 'Same-day command of one existing paid colony ship only. Travel limit90 is before arrival and the known future pending date; not arrival, completed colony, swallow or full acceptance.'}
output = run / (after + '-target523-colonization-order-proof.json')
assert not output.exists()
h.write_json(output, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True], 'route': route, 'ETA': proof['actual_native_arrival_estimate']}, ensure_ascii=True), flush=True)
assert passed
