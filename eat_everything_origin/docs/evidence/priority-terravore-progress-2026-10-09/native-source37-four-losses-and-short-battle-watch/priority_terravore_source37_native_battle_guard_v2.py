"""Exact original native four-ship loss and three emergency MIA; no game actions."""
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
obs = load(after + '-construction-boundary-observation-v2.json')
oe = load(after + '-boundary-observation-v2-execution.json')
strict_name = after + '-native-devour-wait-v8-proof.json'
strict = load(strict_name)
se = load(after + '-native-devour-wait-guard-v8-execution.json')
cal = load(after + '-calendar-receipt.json')
ce = load(after + '-calendar-execution.json')
pre = load(cal['prior_proof_file'])
pe = load(cal['prior_execution_stage'] + '-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
lost = {1807, 1895, 1896, 67110639}
mia = {'2': ('2280.03.16', 2), '33555013': ('2280.01.03', 33555519),
    '33555278': ('2281.06.27', 50333369)}
typed_enemies = lambda raw: set(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(raw, 'combat'), 'in_combat_with'))))

def living(st):
    return {sid for raw in st['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
        for sid in q.ids(q.block(raw, 'ships')) if q.scalars(st['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
        and q.scalars(st['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}

def global_read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        text = z.read('gamestate').decode('utf-8-sig')
    roots = {k: v for k, v, op in q.fields(text) if op}
    return {'country_raw': {i: q.block(roots['country'], i) for i in ['0', '1']},
        'ships_lost_entries': {str(i): [(v, op) for k, v, op in q.fields(roots['ships']) if k == str(i)] for i in lost},
        'enemy825_raw': q.block(roots['fleet'], '825'),
        'dead_fleets_entries': {str(i): [(v, op) for k, v, op in q.fields(roots['fleet']) if k == str(i)] for i in [788, 33555034, 100664127]},
        'wars_raw': roots['war'], 'armies_raw': roots.get('army', roots.get('armies', '')),
        'system37_raw': q.block(roots['galactic_object'], '37'),
        'base158_raw': q.block(q.block(roots['starbase_mgr'], 'starbases'), '158')}

bg, ag = global_read(before), global_read(after)
new_messages = [v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
message = new_messages[0] if len(new_messages) == 1 else ''
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

reports = {q.scalars(v).get('fleet'): v for v in objects(q.block(stats, 'fleets'))}
bw, aw = [q.block(st['wars_raw'], '1') for st in [bg, ag]]
omit = lambda raw, keys: [(k, v, op) for k, v, op in q.fields(raw) if k not in keys]
active = {i for i, raw in a['owned_fleets_raw'].items() if typed_enemies(raw)}
checks = {
    'original_V8_24_exact_three_FAIL_actual1_source_and_original_SAV_pair': len(strict['checks']) == 24
        and [k for k, v in strict['checks'].items() if v is not True] == [
            'all_owned_ship_identity_designs_and_original25_military_alive',
            'native_war1_original_participants_goals_and_forcedpeace_date_held',
            'original_outpost_capture11_and_normal_stop9_actual0_fixed_sources_SAVs_assets_bound']
        and strict['status'] == 'FAIL' and se['returncode'] == 1
        and se['helper_sha256'] == h.sha256(run / 'priority_terravore_fourth_native_devour_wait_guard_v8.py')
        == 'ca50c10766845fedea8594ed264c02f0d393dac4580a3360132217d2a6cf0d69'
        and strict['before_sha256'] == ba['save_sha256'] == h.sha256(run / (before + '.sav'))
        == '1dac57e441620825cc9829689bd12edae7eaefe9c7f109e6fea4db76c2bc825d'
        and strict['after_sha256'] == aa['save_sha256'] == h.sha256(run / (after + '.sav'))
        == '42b50583432e04a42fcf734d0f2928492fbfb10d4a6a147973c342f5bf1aea7e',
    'six_observations_actual0_original_source': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == h.sha256(Path(oe['command'][1]))
        == '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b',
    'calendarV3_actual0_and_prior_stop9_actual0_fixed_source': ce['returncode'] == 0
        and ce['helper_sha256'] == h.sha256(Path(ce['command'][1]))
        == 'c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589'
        and cal.get('business_preflight') is True and pe['returncode'] == 0
        and pe['helper_sha256'] == h.sha256(Path(pe['command'][1]))
        == 'd633642788d3e0caf8272917be922817b42b20fa26f7dbed7a5725470af05a93'
        and len(pre['checks']) == 9 and all(v is True for v in pre['checks'].values())
        and pre['after_sha256'] == ba['save_sha256'],
    'only_four_original_military_ships_removed_global_entries_none_no_added':
        set(b['owned_ship_ids']) - set(a['owned_ship_ids']) == lost
        and set(a['owned_ship_ids']) - set(b['owned_ship_ids']) == set()
        and all(v == [('none', False)] for v in ag['ships_lost_entries'].values())
        and ag['dead_fleets_entries'] == {'788': [], '33555034': [('none', False)], '100664127': [('none', False)]},
    'unique_native277_we_escaped_four_exact_reported_corvette_losses':
        all(q.scalars(message).get(k) == v for k, v in {'type': 'COMBAT_STATS', 'receiver': 0,
            'notification': 277, 'date': '2278.04.14'}.items())
        and q.scalars(stats).get('reason') == 'we_escaped' and q.scalars(stats).get('date') == '2278.04.06'
        and set(reports) == {33555034, 100664127, 788, 33555013}
        and all(q.ids(q.block(reports[fid], 'ship_size_count_lost')) == [n]
            for fid, n in {33555034: 1, 100664127: 1, 788: 2, 33555013: 0}.items()),
    'remaining_original21_alive_actual_designs_held_no_replacement': living(a) == living(b) - lost
        and len(living(b)) == 25 and len(living(a)) == 21
        and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in a['owned_ships_raw'].items()),
    'only_three_original_fleets_native_emergency_MIA_exact_return_dates':
        {i for i, raw in a['owned_fleets_raw'].items() if q.scalars(q.block(raw, 'properties')).get('mia') == 'yes'} == set(mia)
        and all(q.scalars(a['owned_fleets_raw'][fid]).get('return_date') == date
            and q.scalars(a['owned_fleets_raw'][fid]).get('mia_type') == 'mia_emergency_ftl'
            and q.ids(q.block(a['owned_fleets_raw'][fid], 'ships')) == [sid]
            and q.scalars(a['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0 for fid, (date, sid) in mia.items()),
    'only_science166_base849_active_vs_original_enemy825_typed_fleet_not_debris': active == {'166', '849'}
        and all(typed_enemies(a['owned_fleets_raw'][i]) == {825} for i in active)
        and typed_enemies(ag['enemy825_raw']) == {166, 849}
        and q.scalars(q.block(q.block(ag['enemy825_raw'], 'movement_manager'), 'coordinate')).get('origin') == 37,
    'original_science_leader_and_source_starport_alive_controlled_no_pending':
        q.scalars(a['owned_ships_raw']['1049']).get('leader') == 74
        and q.scalars(a['owned_ships_raw']['1049']).get('hitpoints') == 375
        and q.scalars(a['owned_ships_raw']['1931']).get('hitpoints', 0) > 0
        and q.scalars(a['owned_ships_raw']['1931']).get('disabled') != 'yes'
        and q.scalars(ag['base158_raw']).get('station') == 1931 and not a['pending_country0_raw']
        and aa['planets']['7']['owner'] == aa['planets']['7']['controller']
        == aa['planets']['523']['owner'] == aa['planets']['523']['controller'] == 0,
    'war1_only_known_forcepeace_two_fields_and_native_fatigue_battles_changed':
        omit(bw, {'battles', 'attacker_war_exhaustion', 'defender_war_exhaustion'})
        == omit(aw, {'battles', 'attacker_war_exhaustion', 'defender_war_exhaustion', 'defender_force_peace', 'defender_force_peace_date'})
        and q.scalars(aw).get('defender_force_peace') == 'yes'
        and q.scalars(aw).get('defender_force_peace_date') == '2280.04.15',
    'native_devour27_C49_D14_worlds3_and_original_error_unfiltered_held': strict['situation_progress'] == 27
        and strict['mother_population'] == 11397 and strict['source_population'] == 389
        and (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
v1 = load(after + '-native-source37-battle-proof.json')
v1e = load(after + '-native-source37-battle-guard-execution.json')
checks['V1_original_one_FAIL_actual1_source_original_pair_retained'] = (
    len(v1['checks']) == 11 and [k for k, v in v1['checks'].items() if v is not True]
    == ['only_four_original_military_ships_removed_global_entries_none_no_added']
    and v1e['returncode'] == 1 and v1e['helper_sha256']
    == h.sha256(run / 'priority_terravore_source37_native_battle_guard.py')
    == 'ca99b7757b78c15dc77cef50a5022c0bcd7b14085030d113a46f11b374f18a05'
    and v1['before_sha256'] == ba['save_sha256'] and v1['after_sha256'] == aa['save_sha256'])
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_SOURCE37_BATTLE_COMPONENT' if passed else 'FAIL', 'checks': checks,
    'date': aa['date'], 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'before_global_state': bg, 'after_global_state': ag,
    'before_state': b, 'after_state': a, 'lost_ship_ids': sorted(lost), 'military_ids': sorted(living(a)),
    'known_MIA': mia, 'native_report277_raw': message, 'strict_original_proof_file': strict_name,
    'strict_original_proof_sha256': h.sha256(run / strict_name), 'strict_original_checks': strict['checks'],
    'paid_births': strict['paid_births'], 'boundaries': strict['boundaries'],
    'native_devour_calendar_ready': False, 'maximum_days_to_native_bite_boundary': 0,
    'scope': 'Exact native four-ship deaths and three original MIA; 21 original Mod core checks retained. Active source battle requires separate exact short interval review. No full-route claim.'}
out = run / (after + '-native-source37-battle-v2-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Battle component failure retained; no continuation'
