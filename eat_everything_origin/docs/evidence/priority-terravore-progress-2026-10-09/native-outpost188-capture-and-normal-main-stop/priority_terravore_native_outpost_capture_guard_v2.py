"""Read-only exact four original enemy stations transferred in native battle188."""
import json
import logging
import re
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
sha = h.sha256
strict_name = after + '-native-devour-wait-v7-proof.json'
strict = load(strict_name)
se = load(after + '-native-devour-wait-guard-v7-execution.json')
obs = load(after + '-construction-boundary-observation-v2.json')
oe = load(after + '-boundary-observation-v2-execution.json')
cal = load(after + '-calendar-receipt.json')
ce = load(after + '-calendar-execution.json')
review = load(cal['review_file'])
rexe = load(review['execution_stage'] + '-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
expected = {50332983: (16778103, 'shipclass_mining_station'),
    50333076: (16778097, 'shipclass_mining_station'),
    50333335: (875, 'shipclass_research_station'),
    67110520: (33555300, 'shipclass_starbase')}

def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        text = z.read('gamestate').decode('utf-8-sig')
    roots = {k: v for k, v, opened in q.fields(text) if opened}
    ships = {k: v for k, v, opened in q.fields(roots['ships']) if opened}
    fleets = {k: v for k, v, opened in q.fields(roots['fleet']) if opened}
    countries = {i: q.block(roots['country'], i) for i in ['0', '1']}
    owned = {i: list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)',
        q.block(q.block(v, 'fleets_manager'), 'owned_fleets')))) for i, v in countries.items()}
    return {'save_sha256': sha(run / (stage + '.sav')), 'countries_raw': countries,
        'owned_fleets': owned, 'asset_ships_raw': {str(i): ships[str(i)] for i in expected},
        'asset_fleets_raw': {str(fid): fleets[str(fid)] for fid, cls in expected.values()},
        'system188_raw': q.block(roots['galactic_object'], '188'),
        'base160_raw': q.block(q.block(roots['starbase_mgr'], 'starbases'), '160'),
        'wars_raw': roots['war']}

bg, ag = read(before), read(after)

def living(st):
    return {sid for raw in st['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
        for sid in q.ids(q.block(raw, 'ships')) if q.scalars(st['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
        and q.scalars(st['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}

new_messages = [v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
messages = [v for v in new_messages if q.scalars(v).get('notification') == 276]
message = messages[0] if len(messages) == 1 else ''
stats = q.block(message, 'combat_stats')
def objects(raw):
    depth = 0
    begin = 0
    for token, start, end in q.tokens(raw):
        if token == '{':
            if depth == 0:
                begin = end
            depth += 1
        elif token == '}':
            depth -= 1
            if depth == 0:
                yield raw[begin:start]
    assert depth == 0

own_report = list(objects(q.block(stats, 'fleets')))
enemy_report = list(objects(q.block(stats, 'enemy')))
main_ids = q.ids(q.block(a['owned_fleets_raw']['83886903'], 'ships'))
transfers_ok = all(
    fid in bg['owned_fleets']['1'] and fid not in bg['owned_fleets']['0']
    and fid in ag['owned_fleets']['0'] and fid not in ag['owned_fleets']['1']
    and all(q.scalars(st['asset_ships_raw'][str(sid)]).get('fleet') == fid
        and q.ids(q.block(st['asset_fleets_raw'][str(fid)], 'ships')) == [sid]
        and q.scalars(st['asset_fleets_raw'][str(fid)]).get('ship_class') == cls
        and q.scalars(q.block(st['asset_ships_raw'][str(sid)], 'coordinate')).get('origin') == 188
        for st in [bg, ag])
    and q.block(bg['asset_ships_raw'][str(sid)], 'ship_design_implementation')
        == q.block(ag['asset_ships_raw'][str(sid)], 'ship_design_implementation')
    and q.scalars(bg['asset_ships_raw'][str(sid)]).get('construction_date')
        == q.scalars(ag['asset_ships_raw'][str(sid)]).get('construction_date')
        < ba['date'] for sid, (fid, cls) in expected.items())
checks = {
    'exact_original_V7_one_FAIL_actual1_source_SAV_retained': len(strict['checks']) == 23
        and [k for k, v in strict['checks'].items() if v is not True]
        == ['all_owned_ship_identity_designs_and_original25_military_alive']
        and strict['status'] == 'FAIL' and se['returncode'] == 1
        and se['helper_sha256'] == sha(run / 'priority_terravore_fourth_native_devour_wait_guard_v7.py')
        == '37d12272fcac8675760799068fa9836163e0af61e7c94810fd3405bebc8eb327'
        and strict['before_sha256'] == bg['save_sha256'] == ba['save_sha256']
        == '134df22353d41ebfa742ba8e1834287601756146bfbbf266f3227555225cfce9'
        and strict['after_sha256'] == ag['save_sha256'] == aa['save_sha256']
        == 'c96af5aa83534d977dec8dc0ed235d33bccb528ac3b1c55acd8d85409670ca29',
    'six_observations_actual0_current_original_source': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == sha(run / 'priority_terravore_construction_boundary_observation_v2.py')
        == '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b',
    'review10_actual0_calendarV3_actual0_exact_SAV_interval': len(review['checks']) == 10
        and all(v is True for v in review['checks'].values()) and rexe['returncode'] == 0
        and rexe['helper_sha256'] == sha(Path(rexe['command'][1]))
        == 'd7959d08a7932aac6fe5c22218ce2a8edb24d40285b6a970ff32f09538460892'
        and ce['returncode'] == 0 and ce['helper_sha256'] == sha(Path(ce['command'][1]))
        == 'c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589'
        and cal.get('business_preflight') is True and cal['review_sha256'] == sha(run / cal['review_file'])
        and review['after_sha256'] == bg['save_sha256'] and cal['days'] == 7
        and review['start_date'] == ba['date'] == '2278.02.23'
        and review['end_date'] == aa['date'] == '2278.02.30',
    'only_four_original_enemy_stations_transferred_no_owned_removed': transfers_ok
        and set(a['owned_ship_ids']) - set(b['owned_ship_ids']) == set(expected)
        and set(b['owned_ship_ids']) - set(a['owned_ship_ids']) == set(),
    'all_original_owned_designs_held_and25_military_alive': living(b) == living(a) and len(living(a)) == 25
        and all(q.block(raw, 'ship_design_implementation') == q.block(a['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in b['owned_ships_raw'].items())
        and len(main_ids) == 18 and main_ids == q.ids(q.block(b['owned_fleets_raw']['83886903'], 'ships')),
    'unique_native_COMBAT_STATS276_main18_lost0_enemy_outpost1_lost0': new_messages == messages
        and all(q.scalars(message).get(k) == v for k, v in {'type': 'COMBAT_STATS', 'receiver': 0,
            'date': '2278.02.29', 'notification': 276}.items())
        and q.scalars(q.block(message, 'coordinate')).get('origin') == 188
        and q.scalars(stats).get('reason') == 'no_more_enemies'
        and q.scalars(stats).get('date') == '2278.01.30'
        and len(own_report) == len(enemy_report) == 1
        and q.scalars(own_report[0]).get('fleet') == 83886903
        and q.ids(q.block(own_report[0], 'ship_size_count')) == [18]
        and q.ids(q.block(own_report[0], 'ship_size_count_lost')) == [0]
        and q.scalars(enemy_report[0]).get('fleet') == 33555300
        and q.ids(q.block(enemy_report[0], 'ship_size_count')) == [1]
        and q.ids(q.block(enemy_report[0], 'ship_size_count_lost')) == [0],
    'captured_original_outpost_disabled_native_repair_base160': q.scalars(ag['asset_ships_raw']['67110520']).get('disabled') == 'yes'
        and q.scalars(ag['asset_ships_raw']['67110520']).get('is_being_repaired') == 'yes'
        and q.scalars(ag['asset_ships_raw']['67110520']).get('hitpoints', 0) > 0
        and q.scalars(ag['base160_raw']).get('station') == 67110520
        and q.scalars(ag['base160_raw']).get('level') == 'starbase_level_outpost',
    'no_unknown_business_boundary_active_combat_MIA_pending': strict['boundaries'] == []
        and not a['pending_country0_raw'] and all(
            not q.ids(q.block(q.block(raw, 'combat'), 'in_combat_with'))
            and q.scalars(q.block(raw, 'properties')).get('mia') != 'yes'
            for raw in a['owned_fleets_raw'].values()),
    'source_mother_core_and_native_progress24_no_free_grant': ba['countries']['0']['variables'] == aa['countries']['0']['variables']
        and strict['situation_progress'] == 24 and strict['mother_population'] == 11378
        and strict['source_population'] == 388 and strict['empire_population'] == 11766
        and all(float(v) == 0 for v in strict['stock_delta'].values())
        and aa['planets']['523']['owner'] == aa['planets']['7']['owner'] == 0,
    'original_error_bytes_no_append_and_production41_020_chinese_held':
        (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and sha(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese'
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
v1_ex = load(after + '-native-outpost-capture-guard-execution.json')
checks['V1_original_parse_exception_actual1_source_preserved'] = (
    v1_ex['returncode'] == 1 and v1_ex['helper_sha256']
    == sha(run / 'priority_terravore_native_outpost_capture_guard.py')
    == '5b0f230d5b658c0c75f6f56c0cabe9ac3860378bd6477ba08c3e82537f740b4c'
    and 'unexpected delimiter at field boundary' in (run / (after + '-native-outpost-capture-guard-stderr.txt')).read_text()
    and not (run / (after + '-native-outpost-capture-proof.json')).exists())
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_OUTPOST188_CAPTURE_COMPONENT' if passed else 'FAIL',
    'checks': checks, 'date': aa['date'], 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'strict_original_proof_file': strict_name, 'strict_original_proof_sha256': sha(run / strict_name),
    'strict_original_checks_retained': strict['checks'], 'before_global_state': bg, 'after_global_state': ag,
    'new_messages_raw': new_messages, 'transferred_assets': list(expected), 'original_military_ids': sorted(living(a)),
    'paid_births': strict['paid_births'], 'boundaries': [], 'native_devour_calendar_ready': passed,
    'maximum_days_to_native_bite_boundary': 90 if passed else 0,
    'scope': 'Exact native station transfer after original battle; independent component, original strict FAIL retained. No full-route acceptance.'}
out = run / (after + '-native-outpost-capture-v2-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Original capture failure retained; no continuation'
