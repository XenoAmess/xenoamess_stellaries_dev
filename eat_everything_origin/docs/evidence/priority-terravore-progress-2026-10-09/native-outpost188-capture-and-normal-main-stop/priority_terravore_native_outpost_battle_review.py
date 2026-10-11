"""Read-only exact known outpost combat review, limited to one specific interval."""
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
pre = load(stage + '-native-devour-wait-v7-proof.json')
pe = load(stage + '-native-devour-wait-guard-v7-execution.json')
suffix = '-construction-boundary-observation-v2.json' if (run / (stage + '-construction-boundary-observation-v2.json')).exists() else '-construction-boundary-observation.json'
obs = load(stage + suffix)
oe = load(stage + ('-boundary-observation-v2-execution.json' if 'v2.json' in suffix else '-boundary-observation-execution.json'))
audit = obs['after_state']['audit']
validate_native_interval(audit['date'], end, days)
with zipfile.ZipFile(run / (stage + '.sav')) as archive:
    roots = {k: v for k, v, opened in q.fields(archive.read('gamestate').decode('utf-8-sig')) if opened}
fleets = {k: v for k, v, opened in q.fields(roots['fleet']) if opened}
ships = {k: v for k, v, opened in q.fields(roots['ships']) if opened}
countries = {i: q.block(roots['country'], i) for i in ['0', '1']}
owned = {i: list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(v, 'fleets_manager'), 'owned_fleets')))) for i, v in countries.items()}
main, enemy = fleets['83886903'], fleets['33555300']
active = {i for i in owned['0'] if q.ids(q.block(q.block(fleets[str(i)], 'combat'), 'in_combat_with'))}
inv_name = 'terravore-fourth-devour-second-native-bite-date-native-population-bite-and-combat-investigation.json'
inv = load(inv_name)
anchor = inv['global_states']['terravore-fourth-devour-second-native-bite-date']
original = q.ids(q.block(anchor['fleets_raw']['83886903'], 'ships'))
military = {sid for i in owned['0'] if q.scalars(fleets[str(i)]).get('ship_class') == 'shipclass_military'
    for sid in q.ids(q.block(fleets[str(i)], 'ships'))
    if q.scalars(ships[str(sid)]).get('hitpoints', 0) > 0 and q.scalars(ships[str(sid)]).get('killed') != 'yes'}
checks = {
    'current23_PASS_actual0_V7_exact_source_and_SAV': len(pre['checks']) == 23 and all(v is True for v in pre['checks'].values())
        and pe['returncode'] == 0 and pe['helper_sha256'] == h.sha256(run / 'priority_terravore_fourth_native_devour_wait_guard_v7.py')
        == '37d12272fcac8675760799068fa9836163e0af61e7c94810fd3405bebc8eb327'
        and pre['after_sha256'] == audit['save_sha256'] == h.sha256(run / (stage + '.sav')),
    'current_six_original_observations_actual0_source_bound': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == h.sha256(Path(oe['command'][1]))
        and oe['helper_sha256'] in {'e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
            '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b'},
    'only_known_active_combat_boundary_no_ordinary_ready': pre['boundaries'] == ['native_owned_active_combat']
        and pre['native_devour_calendar_ready'] is False and active == {83886903},
    'native_interval1_to7_days_before_final_settlement': 1 <= days <= 7 and end <= '2278.09.30',
    'original_INV_source_and_second_bite_actual_SAV_bound': h.sha256(run / inv_name)
        == '0e3f4364f62bfbcbb3e4b4a742a0db612f2775d0975780c557be2784e1e45cd1'
        and inv['after_sha256'] == '9705ffcd1700af3093b518060aa93348d1544cace1a991cf6f1184f7c161dbd4',
    'main_original18_actual_designs_and_all25_alive': q.ids(q.block(main, 'ships')) == original
        and len(original) == 18 and len(military) == 25 and all(i in military for i in original)
        and all(q.block(ships[str(i)], 'ship_design_implementation')
            == q.block(anchor['ships_raw'][str(i)], 'ship_design_implementation') for i in original),
    'exact_native_main_vs_original_enemy_outpost188': q.ids(q.block(q.block(main, 'combat'), 'in_combat_with')) == [33555300]
        and q.scalars(q.block(q.block(main, 'movement_manager'), 'coordinate')).get('origin') == 188
        and q.scalars(q.block(q.block(enemy, 'movement_manager'), 'coordinate')).get('origin') == 188
        and q.scalars(enemy).get('ship_class') == 'shipclass_starbase'
        and q.ids(q.block(enemy, 'ships')) == [67110520],
    'original_enemy_station_still_owned1_not_disabled_or_deleted': 33555300 in owned['1'] and 33555300 not in owned['0']
        and q.scalars(ships['67110520']).get('fleet') == 33555300
        and q.scalars(ships['67110520']).get('hitpoints', 0) > 0
        and q.scalars(ships['67110520']).get('disabled') != 'yes',
    'source_and_mother_owner0_Q13_32month_active_situation': all(audit['planets'][i].get('owner')
        == audit['planets'][i].get('controller') == 0 for i in ['7', '523'])
        and audit['planets']['523']['variables']['eep_q'] == 13
        and audit['planets']['523']['variables']['eep_months'] == 32
        and audit['situations']['50331660']['progress'] < 32,
    'no_pending_or_new_error_and_same_production': not obs['after_state']['pending_country0_raw']
        and h.sha256(run / (stage + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and meta['language'] == 'l_simp_chinese' and meta['version'] == '0.2.0'
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL', 'checks': checks,
    'before_sha256': audit['save_sha256'], 'after_sha256': audit['save_sha256'], 'start_date': audit['date'],
    'end_date': end, 'days': days, 'maximum_days': days, 'allowed_boundaries': pre['boundaries'],
    'execution_stage': execution_stage, 'main_fleet_raw': main, 'enemy_fleet_raw': enemy,
    'enemy_ship_raw': ships['67110520'], 'scope': 'Only this exact known native combat interval. No victory, capture or full route acceptance claim.'}
out = run / (execution_stage + '-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Known battle review failed; no calendar allowed'
