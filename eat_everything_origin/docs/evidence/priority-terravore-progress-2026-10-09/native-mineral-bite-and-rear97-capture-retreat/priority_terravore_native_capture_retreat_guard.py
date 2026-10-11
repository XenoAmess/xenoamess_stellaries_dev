"""Read-only exact native rear capture and single same-day science retreat."""
import json
import logging
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
stage = 'terravore-fourth-devour-pre-second-bite-year-wait-03'
after = 'terravore-rear97-science-native-emergency-retreated'
obs = load(stage + '-construction-boundary-observation.json')
strict = load(stage + '-native-devour-wait-v3-proof.json')
se = load(stage + '-native-devour-wait-guard-v3-execution.json')
oe = load(stage + '-boundary-observation-execution.json')
de = load('terravore-fourth-devour-pre-second-bite-year-wait-driver-execution.json')
save_ex = load(after + '-save-execution.json')
failure = 'all_owned_ship_identity_designs_and_original25_military_alive'


def read(label):
    with zipfile.ZipFile(run / (label + '.sav')) as archive:
        fs = list(q.fields(archive.read('gamestate').decode('utf-8-sig')))
    roots = {k: v for k, v, obj in fs if obj}
    countries = {i: q.block(roots['country'], i) for i in ['0', '1']}
    fleets = {k: v for k, v, obj in q.fields(roots['fleet']) if obj}
    ships = {k: v for k, v, obj in q.fields(roots['ships']) if obj}
    owned = {i: list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)',
        q.block(q.block(c, 'fleets_manager'), 'owned_fleets')))) for i, c in countries.items()}
    ids = sorted({sid for fid in owned['0'] for sid in q.ids(q.block(fleets[str(fid)], 'ships'))})
    messages = [v for k, v, obj in fs if k == 'message' and obj and q.scalars(v).get('receiver') == 0]
    return {'audit': load(label + '.audit.json'), 'countries_raw': countries, 'owned_fleets': owned,
        'owned_ship_ids': ids, 'owned_fleets_raw': {str(i): fleets[str(i)] for i in owned['0']},
        'owned_ships_raw': {str(i): ships[str(i)] for i in ids},
        'watched_fleets_raw': {i: fleets[i] for i in ['166', '804', '825']},
        'watched_ships_raw': {i: ships[i] for i in ['1049', '67109591']},
        'leader74_raw': q.block(roots['leaders'], '74'),
        'starbases_raw': {i: q.block(q.block(roots['starbase_mgr'], 'starbases'), i) for i in ['153', '158']},
        'wars_raw': roots['war'], 'messages_country0_raw': messages,
        'pending_country0_raw': [v for k, v, obj in fs if k == 'player_event' and obj and q.scalars(v).get('country') == 0]}


b, a = read(stage), read(after)
old = obs['before_state']
ba, aa = b['audit'], a['audit']
station = q.scalars(b['watched_ships_raw']['67109591'])
sf = q.scalars(a['watched_fleets_raw']['166'])
ship = q.scalars(a['watched_ships_raw']['1049'])
reports = [v for v in b['messages_country0_raw'] if q.scalars(v).get('notification') == 273]
military = lambda st: {sid for raw in st['owned_fleets_raw'].values()
    if q.scalars(raw).get('ship_class') == 'shipclass_military' for sid in q.ids(q.block(raw, 'ships'))
    if q.scalars(st['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
    and q.scalars(st['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}
pins = {
    'priority_terravore_fourth_native_devour_wait_guard_v3.py': 'ff8e46d30640ff1e49ad0fa3bb6297d4cf1073ee12e6535e379b0e2dd3342813',
    'priority_terravore_native_devour_bounded_driver_v2.py': 'be8f0b23d31fb2b60c7b803d6036f8de99fbd18eff903f8818c1c2787b6c221e',
    'priority_terravore_construction_boundary_observation.py': 'e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
    'priority_native_save.py': '19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e',
    'priority_native_ui_input_v3.py': '801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f',
}
checks = {
    'immutable_original_component20_exact_one_failure_actual1_driver_stopped':
        len(strict['checks']) == 20 and [k for k, v in strict['checks'].items() if v is not True] == [failure]
        and se['returncode'] == de['returncode'] == 1
        and se['helper_sha256'] == pins['priority_terravore_fourth_native_devour_wait_guard_v3.py']
        and de['helper_sha256'] == pins['priority_terravore_native_devour_bounded_driver_v2.py'],
    'six_original_observations_actual0_and_source_pins': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == pins['priority_terravore_construction_boundary_observation.py']
        and all(h.sha256(run / k) == v for k, v in pins.items()),
    'actual_same_day_normal_save_source_and_exact_original_SHA_pair':
        ba['date'] == aa['date'] == '2277.11.01' and save_ex['returncode'] == 0
        and save_ex['helper_sha256'] == pins['priority_native_save.py']
        and ba['save_sha256'] == strict['after_sha256'] == h.sha256(run / (stage + '.sav'))
        == '9edb91cc3addd6b26698a1c58cfd7a1802f6b24e860ef382a980f75e00284e81'
        and aa['save_sha256'] == h.sha256(run / (after + '.sav'))
        == 'a291c0d0d9dfc4c7b38877440d3347f08316993e9b3c20b2c067f862fd07fd26',
    'only_station_removed_from_owned_not_deleted_original_disabled_ship':
        set(old['owned_ship_ids']) - set(b['owned_ship_ids']) == {67109591}
        and not set(b['owned_ship_ids']) - set(old['owned_ship_ids'])
        and station.get('fleet') == 804 and station.get('hitpoints') == 1 and station.get('disabled') == 'yes'
        and b['watched_ships_raw']['67109591'] == a['watched_ships_raw']['67109591']
        and 804 not in b['owned_fleets']['0'] and 804 in b['owned_fleets']['1']
        and b['starbases_raw'] == a['starbases_raw'],
    'original_native273_we_disabled_report_zero_station_losses':
        len(reports) == 1 and q.scalars(reports[0]).get('type') == 'COMBAT_STATS'
        and q.scalars(reports[0]).get('date') == '2277.10.22'
        and q.scalars(q.block(reports[0], 'combat_stats')).get('reason') == 'we_disabled'
        and '67109591' in b['watched_fleets_raw']['804'],
    'original25_military_alive_and_all_current_owned_actual_designs_held':
        len(military(a)) == 25 and military(old) == military(b) == military(a)
        and b['owned_ship_ids'] == a['owned_ship_ids']
        and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][i], 'ship_design_implementation')
            for i, raw in a['owned_ships_raw'].items()),
    'same_day_country_core_resources_true_banks_variables_gov_unchanged': ba['countries']['0'] == aa['countries']['0'],
    'same_day_actual_owned_pop_source_mother_situation_structure_jobs_unchanged':
        all(ba[k] == aa[k] for k in ['planets', 'colonies', 'situations', 'districts', 'deposits', 'pop_groups', 'pop_jobs', 'species']),
    'one_actual_normal_emergency_click_source_actual0':
        load('terravore-rear97-science-request-native-emergency-ftl-execution.json')['returncode'] == 0
        and load('terravore-rear97-science-request-native-emergency-ftl.action.json')['client_point'] == [210, 389],
    'original_science166_1049_and_leader74_alive_native_MIA_scheduled_return':
        q.ids(q.block(a['watched_fleets_raw']['166'], 'ships')) == [1049]
        and q.scalars(q.block(a['watched_fleets_raw']['166'], 'properties')).get('mia') == 'yes'
        and sf.get('mia_type') == 'mia_emergency_ftl' and sf.get('return_date') == '2278.01.06'
        and not q.ids(q.block(q.block(a['watched_fleets_raw']['166'], 'combat'), 'enemies'))
        and ship.get('fleet') == 166 and ship.get('leader') == 74
        and all(ship.get(k) == v for k, v in {'hitpoints': 375, 'shield_hitpoints': 320, 'armor_hitpoints': 125}.items())
        and a['leader74_raw'] == b['leader74_raw'],
    'same_day_wars_no_new_Mod_message_pending_or_error': b['wars_raw'] == a['wars_raw']
        and b['pending_country0_raw'] == a['pending_country0_raw'] == []
        and not any('eep_' in raw or 'TERRAVORE_CONSUME' in raw for raw in a['messages_country0_raw'] if raw not in b['messages_country0_raw'])
        and (run / (stage + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
    'production41_version020_simp_chinese_tree_held': meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese'
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_CAPTURE_AND_SCIENCE_RETREAT_COMPONENT' if passed else 'FAIL',
    'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'date': aa['date'], 'before_state': b, 'after_state': a,
    'original_strict_checks_retained_not_reexecuted': strict['checks'],
    'paid_births': strict['paid_births'], 'boundaries': ['native_science_MIA_return_2278.01.06', 'enemy825_in_rear97'],
    'scope': 'Exact native capture and same-day normal retreat; 19 original Mod core checks retained and same-day state independently compared. No claim of return, full route, reload or precise ledger.'}
out = run / (after + '-native-capture-retreat-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}, ensure_ascii=False), flush=True)
assert passed, 'Original independent capture/retreat failure retained; no calendar continuation'
