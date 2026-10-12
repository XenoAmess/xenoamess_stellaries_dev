"""Read-only exact last day before native month32; no settlement assumptions."""
import json
import logging
import re
import sys
from pathlib import Path

stage, execution_stage = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from formal_production_native_calendar_checked_v3 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
pre_name = stage + '-native-devour-wait-v10-proof.json'
pre, pe = load(pre_name), load(stage + '-native-devour-wait-guard-v10-execution.json')
obs = load(stage + '-construction-boundary-observation-v2.json')
oe = load(stage + '-boundary-observation-v2-execution.json')
cal, ce = load(stage + '-calendar-receipt.json'), load(stage + '-calendar-execution.json')
a = obs['after_state']
audit = a['audit']
c = audit['countries']['0']
p, core = audit['planets']['523'], audit['planets']['7']
sit = audit['situations']['50331660']
source_name = 'terravore-fourth-devour-post-capture-wait-01-native-source37-battle-v2-proof.json'
source = load(source_name)
source_ex = load('terravore-fourth-devour-post-capture-wait-01-native-source37-battle-guard-v2-execution.json')
defense_name = 'terravore-source37-native-battle-step12-native-defense-end-proof.json'
defense = load(defense_name)
typed = lambda raw: set(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(raw, 'combat'), 'in_combat_with'))))
military = {sid for raw in a['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
    for sid in q.ids(q.block(raw, 'ships')) if q.scalars(a['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
    and q.scalars(a['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}
validate_native_interval(audit['date'], '2278.10.01', 1)
checks = {
    'latest26_PASS_actual0_fixed_V10_source_and_exact_last_SAV': len(pre['checks']) == 26
        and all(v is True for v in pre['checks'].values()) and pre['status'].startswith('PASS_')
        and pe['returncode'] == 0 and pe['helper_sha256'] == h.sha256(Path(pe['command'][1]))
        == 'fc5f352c71faa985e792ff296eca1e2c9528fd3f2ee0d2daad4707d911913f6d'
        and pre['after_sha256'] == audit['save_sha256'] == h.sha256(run / (stage + '.sav'))
        == 'f47a4b8364163511683dce72a2728dc0eea2c09631cc6e07569e201431f6c55c',
    'six_original_observations_actual0_fixed_source': len(obs['checks']) == 6
        and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == h.sha256(Path(oe['command'][1]))
        == '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b',
    'previous_calendarV3_actual0_native_last_date_and_cap_not_ordinary_ready':
        ce['returncode'] == 0 and ce['helper_sha256'] == h.sha256(Path(ce['command'][1]))
        == 'c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589'
        and cal.get('business_preflight') is True and cal['date'] == audit['date'] == '2278.09.30'
        and cal['start_date'] == '2278.09.18' and cal['days'] == 12
        and pre['boundaries'] == [] and pre['native_devour_calendar_ready'] is False
        and pre['maximum_days_to_native_bite_boundary'] == 0,
    'active_original_situation31_Q13_month32_exact_target_and_approach':
        set(audit['situations']) == {'50331660'} and sit['progress'] == 31 and sit['country'] == 0
        and sit['type'] == 'situation_eep_devouring' and sit['approach'] == 'eep_devour_approach'
        and sit['target'] == {'type': 'planet', 'id': 523, 'opener_id': 4294967295}
        and p['variables']['eep_q'] == 13 and p['variables']['eep_months'] == 32 and p['planet_size'] == 13,
    'original_EEP_C49_D14_G0_made0_worlds3_PSI1_stage1_fleet0_Menace885':
        all(c['variables'].get(k) == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_g': 0,
            'eep_made': 0, 'eep_worlds': 3, 'eep_psi': 1, 'eep_stage': 1, 'eep_fleet_stage': 0, 'eep_crisis': 1}.items())
        and c['effective_stockpile']['menace'] == 885,
    'source_owned_completed_colony38_all_founder73_native_active_no_pending':
        set(c['owned_colonies']) == {0, 38} and p['colony'] == 38
        and p['colonize_date'] == '2276.02.01' and 'colonizing_species' not in audit['colonies']['38']
        and audit['colonies']['38']['actual_pop_sum'] == pre['source_population'] == 390
        and all(g['key']['species'] == 73 for g in audit['pop_groups'].values())
        and all(k in p['flags'] for k in ['eep_active', 'eep_native', 'being_devoured'])
        and 'eep_pending' not in p['flags'] and p['flags']['recently_eaten_planet']['flag_days'] > 1,
    'source_mother_owner_controller0_mother10K_housing_amenities_crime_good':
        p['owner'] == p['controller'] == core['owner'] == core['controller'] == 0
        and audit['colonies']['0']['actual_pop_sum'] >= 10000
        and audit['colonies']['0']['free_housing'] > 0 and audit['colonies']['0']['free_amenities'] > 0
        and audit['colonies']['0']['crime'] == 0,
    'original_source12_actual0_only_three_known_MIA_no_combat_or_pending':
        h.sha256(run / source_name) == 'c8f6f43d08e3a737079fece93f8b30e66035374aba66d997d071ea51e1f88a31'
        and len(source['checks']) == 12 and all(v is True for v in source['checks'].values())
        and source_ex['returncode'] == 0 and source_ex['helper_sha256'] == h.sha256(Path(source_ex['command'][1]))
        == 'fa51dd4f8fcec3d01c24d9ada472f9973b7cd5a53541703a98eb634781d15bec'
        and not a['pending_country0_raw'] and not any(typed(raw) for raw in a['owned_fleets_raw'].values())
        and {i for i, raw in a['owned_fleets_raw'].items() if q.scalars(q.block(raw, 'properties')).get('mia') == 'yes'}
        == set(source['known_MIA']) and all(q.scalars(a['owned_fleets_raw'][i]).get('return_date') == date
            and q.ids(q.block(a['owned_fleets_raw'][i], 'ships')) == [sid]
            for i, (date, sid) in source['known_MIA'].items()),
    'defense_end_fixed_proof_all_owned_actual_designs_and21_military_held':
        h.sha256(run / defense_name) == '75f617c46016304166f82e912895bb97fef9388448fbdcd201f390c90d722768'
        and a['owned_ship_ids'] == defense['after_state']['owned_ship_ids']
        and len(military) == 21 and military == set(source['military_ids'])
        and all(q.block(raw, 'ship_design_implementation')
            == q.block(defense['after_state']['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in a['owned_ships_raw'].items()),
    'original_unfiltered_error_SHA_production41_020_simp_chinese_held':
        h.sha256(run / (stage + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese'
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
v1_name = 'terravore-fourth-devour-final-boundary-review-proof.json'
v1 = load(v1_name)
v1e = load('terravore-fourth-devour-final-boundary-review-execution.json')
checks['V1_original_fixed_POP_assumption_one_FAIL_actual1_source_and_proof_retained'] = (
    h.sha256(run / v1_name) == 'bc99d1ed9a34f94fd9149d8ee0b4f56d3c16b402766a06282d8d2661630fa996'
    and len(v1['checks']) == 10 and [k for k, v in v1['checks'].items() if v is not True]
    == ['source_owned_completed_colony38_all_founder73_native_active_no_pending']
    and v1e['returncode'] == 1 and v1e['helper_sha256']
    == h.sha256(run / 'priority_terravore_fourth_final_boundary_review.py')
    == 'e0e23986de6f25f2f206c9a588b8902bef23ff4e00c8169cd41cbcb6c0787131'
    and v1['after_sha256'] == audit['save_sha256'])
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL', 'checks': checks,
    'before_sha256': audit['save_sha256'], 'after_sha256': audit['save_sha256'],
    'start_date': '2278.09.30', 'end_date': '2278.10.01', 'days': 1, 'maximum_days': 1,
    'allowed_boundaries': [], 'execution_stage': execution_stage,
    'source_proof_file': pre_name, 'source_proof_sha256': h.sha256(run / pre_name),
    'scope': 'Only last native day before month32; permits observation, not settlement or Queen acceptance.'}
out = run / (execution_stage + '-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Final boundary review failure retained; no continuation'
