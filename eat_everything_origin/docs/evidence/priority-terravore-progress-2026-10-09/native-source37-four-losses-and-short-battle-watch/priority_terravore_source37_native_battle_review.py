"""Exact short native source37 battle review, retaining known deaths and MIA."""
import json
import logging
import re
import sys
import zipfile
from pathlib import Path

stage, end, raw_days, execution_stage = sys.argv[1:]
days = int(raw_days)
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from formal_production_native_calendar_checked_v3 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
first = stage == 'terravore-fourth-devour-post-capture-wait-01'
name = stage + ('-native-source37-battle-v2-proof.json' if first else '-native-devour-wait-v9-proof.json')
ex_name = stage + ('-native-source37-battle-guard-v2' if first else '-native-devour-wait-guard-v9')
pre, pe = load(name), load(ex_name + '-execution.json')
obs = load(stage + '-construction-boundary-observation-v2.json')
oe = load(stage + '-boundary-observation-v2-execution.json')
a = obs['after_state']
audit = a['audit']
validate_native_interval(audit['date'], end, days)
anchor_name = 'terravore-fourth-devour-post-capture-wait-01-native-source37-battle-v2-proof.json'
anchor = load(anchor_name)
ae = load('terravore-fourth-devour-post-capture-wait-01-native-source37-battle-guard-v2-execution.json')
with zipfile.ZipFile(run / (stage + '.sav')) as z:
    roots = {k: v for k, v, op in q.fields(z.read('gamestate').decode('utf-8-sig')) if op}
enemy = q.block(roots['fleet'], '825')
typed = lambda raw: set(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(raw, 'combat'), 'in_combat_with'))))
active = {i for i, raw in a['owned_fleets_raw'].items() if typed(raw)}
military = {sid for raw in a['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
    for sid in q.ids(q.block(raw, 'ships')) if q.scalars(a['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
    and q.scalars(a['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}
known_mia = anchor['known_MIA']
expected_source = 'fa51dd4f8fcec3d01c24d9ada472f9973b7cd5a53541703a98eb634781d15bec' if first else 'c590fc6fdb32728faf83629a842ea158bfd967bb12cc9b3e533d1e556f1fe5b7'
checks = {
    'original_source_battle12_actual0_fixed_proof_source_and_SAV': h.sha256(run / anchor_name)
        == 'c8f6f43d08e3a737079fece93f8b30e66035374aba66d997d071ea51e1f88a31'
        and len(anchor['checks']) == 12 and all(v is True for v in anchor['checks'].values())
        and ae['returncode'] == 0 and ae['helper_sha256'] == h.sha256(Path(ae['command'][1]))
        == 'fa51dd4f8fcec3d01c24d9ada472f9973b7cd5a53541703a98eb634781d15bec'
        and anchor['after_sha256'] == h.sha256(run / 'terravore-fourth-devour-post-capture-wait-01.sav'),
    'latest_component_alltrue_actual0_correct_source_current_SAV': pre['status'].startswith('PASS_')
        and len(pre['checks']) == (12 if first else 25) and all(v is True for v in pre['checks'].values())
        and pe['returncode'] == 0 and pe['helper_sha256'] == h.sha256(Path(pe['command'][1])) == expected_source
        and pre['after_sha256'] == audit['save_sha256'] == h.sha256(run / (stage + '.sav')),
    'six_observations_alltrue_actual0_fixed_source': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == h.sha256(Path(oe['command'][1]))
        == '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b',
    'only_exact_known_boundary_no_unknown_new_history': pre['native_devour_calendar_ready'] is False
        and pre['boundaries'] == (['native_owned_active_combat', 'native_owned_MIA_requires_review', 'native_war_battle_history_changed']
            if first else ['native_owned_active_combat']),
    'exact_short1_to7_native_days_before_final_boundary': 1 <= days <= 7 and end <= '2278.09.30'
        and (not first or days == 1 and end == '2278.06.01'),
    'only_original_science166_and_starport849_vs_native825_at37': active == {'166', '849'}
        and all(typed(a['owned_fleets_raw'][i]) == {825} for i in active) and typed(enemy) == {166, 849}
        and q.scalars(q.block(q.block(enemy, 'movement_manager'), 'coordinate')).get('origin') == 37,
    'science1049_leader74_and_original_station1931_alive_no_disabled_or_pending':
        q.scalars(a['owned_ships_raw']['1049']).get('leader') == 74
        and q.scalars(a['owned_ships_raw']['1049']).get('hitpoints', 0) > 0
        and q.scalars(a['owned_ships_raw']['1931']).get('hitpoints', 0) > 0
        and q.scalars(a['owned_ships_raw']['1931']).get('disabled') != 'yes' and not a['pending_country0_raw'],
    'remaining21_military_original_ids_and_all_owned_actual_designs_held': len(military) == 21
        and military == set(anchor['military_ids'])
        and a['owned_ship_ids'] == anchor['after_state']['owned_ship_ids']
        and all(q.block(raw, 'ship_design_implementation')
            == q.block(anchor['after_state']['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in a['owned_ships_raw'].items()),
    'only_three_exact_original_MIA_dates_ship_identity_positive_HP':
        {i for i, raw in a['owned_fleets_raw'].items() if q.scalars(q.block(raw, 'properties')).get('mia') == 'yes'} == set(known_mia)
        and all(q.scalars(a['owned_fleets_raw'][i]).get('return_date') == date
            and q.ids(q.block(a['owned_fleets_raw'][i], 'ships')) == [sid]
            and q.scalars(a['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
            for i, (date, sid) in known_mia.items()),
    'source_and_mother_controlled_Q13_month32_incomplete_no_error_change':
        audit['planets']['523']['owner'] == audit['planets']['523']['controller']
        == audit['planets']['7']['owner'] == audit['planets']['7']['controller'] == 0
        and audit['planets']['523']['variables']['eep_q'] == 13
        and audit['planets']['523']['variables']['eep_months'] == 32
        and audit['situations']['50331660']['progress'] < 32
        and h.sha256(run / (stage + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL', 'checks': checks,
    'before_sha256': audit['save_sha256'], 'after_sha256': audit['save_sha256'],
    'start_date': audit['date'], 'end_date': end, 'days': days, 'maximum_days': days,
    'allowed_boundaries': pre['boundaries'], 'execution_stage': execution_stage,
    'source_proof_file': name, 'source_proof_sha256': h.sha256(run / name), 'enemy825_raw': enemy,
    'scope': 'Only current native source37 combat and original known losses/MIA; exact bounded interval, no ordinary calendar readiness.'}
out = run / (execution_stage + '-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Review failure retained; no calendar continuation'
