"""Exact native defense report278 closes current source37 combat boundary."""
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
pre_name = after + '-native-devour-wait-v9-proof.json'
pre = load(pre_name)
pe = load(after + '-native-devour-wait-guard-v9-execution.json')
obs = load(after + '-construction-boundary-observation-v2.json')
oe = load(after + '-boundary-observation-v2-execution.json')
cal = load(after + '-calendar-receipt.json')
ce = load(after + '-calendar-execution.json')
review = load(cal['review_file'])
rexe = load(review['execution_stage'] + '-execution.json')
anchor_name = 'terravore-fourth-devour-post-capture-wait-01-native-source37-battle-v2-proof.json'
anchor = load(anchor_name)
ae = load('terravore-fourth-devour-post-capture-wait-01-native-source37-battle-guard-v2-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
with zipfile.ZipFile(run / (after + '.sav')) as z:
    roots = {k: v for k, v, op in q.fields(z.read('gamestate').decode('utf-8-sig')) if op}
enemy = q.block(roots['fleet'], '825')
typed = lambda raw: set(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(raw, 'combat'), 'in_combat_with'))))

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

new_messages = [v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
message = new_messages[0] if len(new_messages) == 1 else ''
stats = q.block(message, 'combat_stats')
own_report = list(objects(q.block(stats, 'fleets')))
enemy_report = list(objects(q.block(stats, 'enemy')))
bw, aw = [q.block(pre['wars_raw'][stage], '1') for stage in [before, after]]
bb, ab = [list(objects(q.block(w, 'battles'))) for w in [bw, aw]]
new_battle = ab[-1] if len(ab) == len(bb) + 1 else ''
military = {sid for raw in a['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
    for sid in q.ids(q.block(raw, 'ships')) if q.scalars(a['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
    and q.scalars(a['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}
omit = lambda raw, keys: [(k, v, op) for k, v, op in q.fields(raw) if k not in keys]
checks = {
    'current_V9_25_PASS_actual0_fixed_source_original_SAV_pair_and_only_history_boundary':
        len(pre['checks']) == 25 and all(v is True for v in pre['checks'].values())
        and pre['status'].startswith('PASS_') and pe['returncode'] == 0
        and pe['helper_sha256'] == h.sha256(Path(pe['command'][1]))
        == 'c590fc6fdb32728faf83629a842ea158bfd967bb12cc9b3e533d1e556f1fe5b7'
        and pre['before_sha256'] == ba['save_sha256'] == h.sha256(run / (before + '.sav'))
        == '3b068598166f41e5a78fb9d389e9c096e22b56f8b598fa07e70bfa1cbb244751'
        and pre['after_sha256'] == aa['save_sha256'] == h.sha256(run / (after + '.sav'))
        == 'e77525cc744d43ad831235b940db716c63131e4bab8f2e44f55e6b4771f85b3f'
        and pre['boundaries'] == ['native_war_battle_history_changed'],
    'six_original_observations_actual0_fixed_source': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == h.sha256(Path(oe['command'][1]))
        == '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b',
    'calendarV3_review10_actual0_exact_original_sources_SHA_interval': ce['returncode'] == 0
        and ce['helper_sha256'] == h.sha256(Path(ce['command'][1]))
        == 'c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589'
        and cal.get('business_preflight') is True and rexe['returncode'] == 0
        and rexe['helper_sha256'] == h.sha256(Path(rexe['command'][1]))
        == '57ac88e594f5db982ebd4a572ff90e75d0b5fd6055d7136e04f6247d7ff160ea'
        and len(review['checks']) == 10 and all(v is True for v in review['checks'].values())
        and review['after_sha256'] == ba['save_sha256'] and cal['review_sha256'] == h.sha256(run / cal['review_file'])
        and review['start_date'] == ba['date'] == '2278.08.11'
        and review['end_date'] == aa['date'] == '2278.08.18' and cal['days'] == 7,
    'original_source37_four_deaths_three_MIA12_actual0_fixed_proof_source': h.sha256(run / anchor_name)
        == 'c8f6f43d08e3a737079fece93f8b30e66035374aba66d997d071ea51e1f88a31'
        and len(anchor['checks']) == 12 and all(v is True for v in anchor['checks'].values())
        and ae['returncode'] == 0 and ae['helper_sha256'] == h.sha256(Path(ae['command'][1]))
        == 'fa51dd4f8fcec3d01c24d9ada472f9973b7cd5a53541703a98eb634781d15bec',
    'owned_identity_and_actual_designs_held_original21_military_alive': b['owned_ship_ids'] == a['owned_ship_ids']
        and len(military) == 21 and military == set(anchor['military_ids'])
        and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in a['owned_ships_raw'].items()),
    'only_known_three_MIA_held_no_active_typed_combat_or_pending': not a['pending_country0_raw']
        and not any(typed(raw) for raw in a['owned_fleets_raw'].values()) and not typed(enemy)
        and {i for i, raw in a['owned_fleets_raw'].items() if q.scalars(q.block(raw, 'properties')).get('mia') == 'yes'}
        == set(anchor['known_MIA']) and all(q.scalars(a['owned_fleets_raw'][i]).get('return_date') == date
            and q.ids(q.block(a['owned_fleets_raw'][i], 'ships')) == [sid]
            for i, (date, sid) in anchor['known_MIA'].items()),
    'unique_report278_native_no_more_enemies_own_station_lost0_enemy_arrays_raw':
        all(q.scalars(message).get(k) == v for k, v in {'type': 'COMBAT_STATS', 'receiver': 0,
            'notification': 278, 'date': '2278.08.11'}.items())
        and q.scalars(stats).get('reason') == 'no_more_enemies' and q.scalars(stats).get('date') == '2278.03.30'
        and len(own_report) == len(enemy_report) == 1
        and q.scalars(own_report[0]).get('fleet') == 849
        and q.ids(q.block(own_report[0], 'ship_size_count')) == [1]
        and q.ids(q.block(own_report[0], 'ship_size_count_lost')) == [0]
        and q.scalars(enemy_report[0]).get('fleet') == 825
        and q.ids(q.block(enemy_report[0], 'ship_size_count')) == [1, 9, 4, 1]
        and q.ids(q.block(enemy_report[0], 'ship_size_count_lost')) == [0, 8, 1, 1],
    'war1_exact_single_new_native_defense_battle_other_fields_except_fatigue_held':
        len(ab) == len(bb) + 1 and ab[:-1] == bb
        and omit(bw, {'battles', 'attacker_war_exhaustion', 'defender_war_exhaustion'})
        == omit(aw, {'battles', 'attacker_war_exhaustion', 'defender_war_exhaustion'})
        and q.ids(q.block(new_battle, 'attackers')) == [1] and q.ids(q.block(new_battle, 'defenders')) == [0]
        and all(q.scalars(new_battle).get(k) == v for k, v in {'system': 37, 'date': '2278.08.11',
            'attacker_victory': 'no', 'attacker_losses': 11, 'defender_losses': 0, 'type': 'ships'}.items()),
    'source_mother_controlled_native_progress30_and_all_EEP_held':
        aa['planets']['523']['owner'] == aa['planets']['523']['controller']
        == aa['planets']['7']['owner'] == aa['planets']['7']['controller'] == 0
        and pre['situation_progress'] == 30 and pre['mother_population'] == 11416
        and pre['source_population'] == 389 and pre['empire_population'] == 11805
        and ba['countries']['0']['variables'] == aa['countries']['0']['variables'],
    'original_station1931_and_science1049_leader74_positive_not_disabled':
        q.scalars(a['owned_ships_raw']['1931']).get('hitpoints', 0) > 0
        and q.scalars(a['owned_ships_raw']['1931']).get('disabled') != 'yes'
        and q.scalars(a['owned_ships_raw']['1049']).get('hitpoints') == 375
        and q.scalars(a['owned_ships_raw']['1049']).get('leader') == 74,
    'original_error_exact_bytes_production41_020_simp_chinese_held':
        (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese'
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_SOURCE37_DEFENSE_END_COMPONENT' if passed else 'FAIL', 'checks': checks,
    'date': aa['date'], 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'original_core_proof_file': pre_name, 'original_core_proof_sha256': h.sha256(run / pre_name),
    'native_report278_raw': message, 'native_new_war_battle_raw': new_battle,
    'before_war1_raw': bw, 'after_war1_raw': aw, 'enemy825_raw': enemy,
    'country1_raw': q.block(roots['country'], '1'), 'after_state': a,
    'paid_births': pre['paid_births'], 'boundaries': [], 'native_devour_calendar_ready': passed,
    'maximum_days_to_native_bite_boundary': 30 if passed else 0,
    'scope': 'Exact native defense end only; report arrays and war loss fields retained separately. Original four deaths remain. No final settlement, Queen or full-route claim.'}
out = run / (after + '-native-defense-end-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Defense end component failure retained; no continuation'
