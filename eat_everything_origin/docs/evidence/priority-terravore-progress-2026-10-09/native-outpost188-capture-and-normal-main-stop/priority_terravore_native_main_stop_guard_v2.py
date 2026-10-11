"""Exact same-day normal GUI stop after independently verified outpost capture."""
import json
import logging
import sys
import zipfile
from pathlib import Path

before, after = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
cap = load(before + '-native-outpost-capture-v2-proof.json')
cape = load(before + '-native-outpost-capture-guard-v2-execution.json')
obs = load(before + '-construction-boundary-observation-v2.json')
ba = obs['after_state']['audit']
aa = load(after + '.audit.json')
save = load(after + '-observation.json')
se = load(after + '-native-save-execution.json')
gui_stage = 'terravore-outpost188-main-native-stop-ordered'
gui = load(gui_stage + '-execution.json')
action = load(gui_stage + '.action.json')

def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        text = z.read('gamestate').decode('utf-8-sig')
    fields = list(q.fields(text))
    roots = {k: v for k, v, opened in fields if opened}
    return fields, {k: v for k, v, opened in q.fields(roots['fleet']) if opened}

bf, b = read(before)
af, a = read(after)
omit = lambda raw, keys: [(k, v, o) for k, v, o in q.fields(raw) if k not in keys]
bm, am = [q.block(st['83886903'], 'movement_manager') for st in [b, a]]
checks = {
    'capture11_PASS_actual0_exact_source_and_SAV': len(cap['checks']) == 11
        and all(v is True for v in cap['checks'].values()) and cap['status'].startswith('PASS_')
        and cape['returncode'] == 0 and cape['helper_sha256'] == h.sha256(Path(cape['command'][1]))
        == '3e75588b16c42cfcc3469311885bd7fd136bb0dd980df32b2b13960bc91e5598'
        and cap['after_sha256'] == ba['save_sha256'] == h.sha256(run / (before + '.sav'))
        == 'c96af5aa83534d977dec8dc0ed235d33bccb528ac3b1c55acd8d85409670ca29',
    'unique_normal_GUI_stop_exact_control_actual0_source_tooltip': gui['returncode'] == 0
        and gui['helper_sha256'] == h.sha256(Path(gui['command'][1]))
        == '801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f'
        and action['action'] == 'left-click' and action['client_point'] == [69, 64]
        and h.sha256(run / 'terravore-outpost188-main-stop-tooltip-ui.jpg')
        == 'b87ca53998c2363b6c5abf9a07b0cee7202d59605e0815872237fb8887c08e3c',
    'same_day_native_save_actual0_source_original_dependencies': se['returncode'] == 0
        and se['helper_sha256'] == h.sha256(Path(se['command'][1]))
        == '19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e'
        and save['status'] == 'OBSERVED_NATIVE_SAVE' and save['new_error_bytes'] == 0
        and all(h.sha256(Path(v['path'])) == v['sha256'] for v in save['dependency_bindings'])
        and ba['date'] == aa['date'] == save['date'] == '2278.02.30'
        and save['save_sha256'] == aa['save_sha256'] == h.sha256(run / (after + '.sav'))
        == '1dac57e441620825cc9829689bd12edae7eaefe9c7f109e6fea4db76c2bc825d',
    'entire_native_world_except_fleet_root_identical_including_duplicate_fields':
        [(k, v, op) for k, v, op in bf if k != 'fleet']
        == [(k, v, op) for k, v, op in af if k != 'fleet'],
    'all_fleets_original_ids_other_fleets_exact_raw_only_main_movement_changed': b.keys() == a.keys()
        and all(v == a[k] for k, v in b.items() if k != '83886903')
        and omit(b['83886903'], {'movement_manager', 'current_order'}) == omit(a['83886903'], {'movement_manager', 'current_order'})
        and [(k, op) for k, v, op in q.fields(q.block(b['83886903'], 'current_order'))] == [('move_to_system_point_order', True)]
        and q.scalars(q.block(q.block(q.block(b['83886903'], 'current_order'), 'move_to_system_point_order'), 'coordinate')).get('origin') == 37
        and not any(k == 'current_order' for k, v, op in q.fields(a['83886903'])),
    'main_native_move_idle_no_path_nodes_invalid_target_current_coordinate188':
        q.scalars(bm).get('state') == 'move_system' and q.scalars(am).get('state') == 'move_idle'
        and q.scalars(q.block(am, 'coordinate')) == q.scalars(q.block(bm, 'coordinate'))
        and q.scalars(q.block(am, 'coordinate')).get('origin') == 188
        and q.scalars(q.block(q.block(am, 'target'), 'coordinate')).get('origin') == 4294967295
        and not any(k == 'node' for k, v, op in q.fields(q.block(am, 'path'))),
    'audit_all_economy_population_EEP_structure_technology_and_owned_identity_exact':
        {k: v for k, v in ba.items() if k not in {'save', 'save_sha256', 'gamestate_sha256', 'gamestate_bytes'}}
        == {k: v for k, v in aa.items() if k not in {'save', 'save_sha256', 'gamestate_sha256', 'gamestate_bytes'}},
    'original_error_unfiltered_exact_bytes_and_SHA':
        (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
v1 = load(after + '-native-main-stop-proof.json')
v1e = load(after + '-independent-guard-execution.json')
checks['V1_original_one_FAIL_actual1_source_retained'] = (
    len(v1['checks']) == 8 and [k for k, v in v1['checks'].items() if v is not True]
    == ['all_fleets_original_ids_other_fleets_exact_raw_only_main_movement_changed']
    and v1e['returncode'] == 1 and v1e['helper_sha256'] == h.sha256(run / 'priority_terravore_native_main_stop_guard.py')
    == '1e5c52febfc07604dc72c0c37ac2c181b1e3b4887c9e8adb7dccd3ca267ae29d'
    and v1['before_sha256'] == ba['save_sha256'] and v1['after_sha256'] == aa['save_sha256'])
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_MAINFLEET_STOP_COMPONENT' if passed else 'FAIL', 'checks': checks,
    'date': aa['date'], 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'before_main_raw': b['83886903'], 'after_main_raw': a['83886903'],
    'capture_proof_file': before + '-native-outpost-capture-v2-proof.json',
    'capture_proof_sha256': h.sha256(run / (before + '-native-outpost-capture-v2-proof.json')),
    'paid_births': cap['paid_births'], 'boundaries': [], 'native_devour_calendar_ready': passed,
    'maximum_days_to_native_bite_boundary': 90 if passed else 0,
    'scope': 'Same-day normal stop only; all other world fields identical, no full-route claim.'}
out = run / (after + '-native-main-stop-v2-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Stop component failure retained; no calendar continuation'
