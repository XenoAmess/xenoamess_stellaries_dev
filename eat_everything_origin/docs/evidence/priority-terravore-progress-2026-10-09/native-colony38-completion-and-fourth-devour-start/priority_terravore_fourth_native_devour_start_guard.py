"""Documented same-day native decision start; no calendar or save mutation."""
import json
import logging
import re
import sys
import zipfile
from pathlib import Path

before, after = sys.argv[1:]
assert before == 'terravore-colony38-native-completion-date'
assert after == 'terravore-fourth-native-devour-started'
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda name: json.loads((run / name).read_text('utf-8-sig'))
sha = h.sha256

def read(stage):
    audit = load(stage + '.audit.json')
    with zipfile.ZipFile(run / (stage + '.sav')) as archive:
        fs = list(q.fields(archive.read('gamestate').decode('utf-8-sig')))
    roots = {k: v for k, v, opened in fs if opened}
    country = q.block(roots['country'], '0')
    fleets = {k: v for k, v, opened in q.fields(roots['fleet']) if opened}
    ships = {k: v for k, v, opened in q.fields(roots['ships']) if opened}
    owned = sorted(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(country, 'fleets_manager'), 'owned_fleets'))))
    ship_ids = sorted({i for fid in owned for i in q.ids(q.block(fleets[str(fid)], 'ships'))})
    return {'audit': audit, 'country0_raw': country,
        'planet523_raw': q.block(q.block(roots['planets'], 'planet'), '523'),
        'planet7_raw': q.block(q.block(roots['planets'], 'planet'), '7'),
        'colony38_raw': q.block(roots['colony'], '38'), 'colony0_raw': q.block(roots['colony'], '0'),
        'situations_raw': roots['situations'], 'owned_fleet_ids': owned, 'owned_ship_ids': ship_ids,
        'owned_fleets_raw': {str(i): fleets[str(i)] for i in owned},
        'owned_ships_raw': {str(i): ships[str(i)] for i in ship_ids},
        'messages_raw': [v for k, v, opened in fs if k == 'message' and opened and q.scalars(v).get('receiver') == 0],
        'pending_raw': [v for k, v, opened in fs if k == 'player_event' and opened and q.scalars(v).get('country') == 0]}

b, a = read(before), read(after)
ba, aa = b['audit'], a['audit']
bc, ac = ba['countries']['0'], aa['countries']['0']
pre = load(before + '-colony38-completion-proof.json')
pe = load('terravore-colony38-native-completion-independent-guard-execution.json')
se = load('terravore-fourth-native-devour-start-save-execution.json')
save = load(after + '-observation.json')
p = aa['planets']['523']
sit = {k: v for k, v in aa['situations'].items() if v.get('type') == 'situation_eep_devouring'}
old_sit = {k: v for k, v in ba['situations'].items() if v.get('type') == 'situation_eep_devouring'}
manifest, tree = h.tree_manifest(h.MOD_ROOT)
flags = p['flags']
core_jobs = lambda audit: {k: v for k, v in audit['pop_jobs'].items() if v.get('planet') == 0}
living = lambda state: {sid for fid, raw in state['owned_fleets_raw'].items()
    if q.scalars(raw).get('ship_class') == 'shipclass_military'
    for sid in q.ids(q.block(raw, 'ships'))
    if q.scalars(state['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0}
checks = {
    'original_completed_colony32_PASS_actual0_exact_source_and_SAV': (
        len(pre['checks']) == 32 and all(v is True for v in pre['checks'].values())
        and pe['returncode'] == 0 and pe['helper_sha256'] == sha(run / 'priority_terravore_fourth_colony_completion_guard.py')
        == '879e33c3c82ae67249d62d9588df71e4712eeca044932b9f7858b7f7d1b29d22'
        and pre['after_sha256'] == sha(run / (before + '.sav'))
        == 'ed8e4bee8bf6924ea713b0ac5338c2528e913d74822f72735b7fe88f1bec92d0'),
    'actual_native_save0_exact_source_dependency_bindings_date_and_SAVs': (
        se['returncode'] == 0 and se['helper_sha256'] == sha(run / 'priority_native_save.py')
        == '19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e'
        and all(sha(Path(row['path'])) == row['sha256'] for row in save['dependency_bindings'])
        and ba['date'] == aa['date'] == save['date'] == '2276.02.01'
        and ba['save_sha256'] == sha(run / (before + '.sav'))
        and aa['save_sha256'] == save['save_sha256'] == sha(run / (after + '.sav'))
        == '53c2273f3686e57c8270446a5e2e3fca8b259cfb4e11c31a134660cca91dbec2'),
    'production41_tree_simp_chinese_version020': meta['language'] == 'l_simp_chinese'
        and meta['version'] == '0.2.0' and len(manifest) == 41
        and tree == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
    'all_unfiltered_error2814_original_SHA_held': (
        (run / (before + '-error-after.log')).read_bytes()
        == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and sha(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and save['new_error_bytes'] == 0 and save['error_prefix_held']),
    'same_day_C49_D14_worlds3_all_EEP_credit_held': bc['variables'] == ac['variables']
        and all(ac['variables'].get(k) == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_worlds': 3, 'eep_psi': 1, 'eep_stage': 1}.items()),
    'core_structure27_jobs_and_11399_pop_exact_held_no_seed_move': (
        ba['colonies']['0'] == aa['colonies']['0'] and ba['planets']['7'] == aa['planets']['7']
        and core_jobs(ba) == core_jobs(aa) and ba['colonies']['0']['actual_pop_sum'] == 11399
        and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts']) == 27
        and all(ba['districts'][str(i)] == aa['districts'][str(i)] for i in aa['colonies']['0']['districts'])),
    'same102_founder_source_pop_no_resettlement_or_new_population': (
        ba['pop_groups'] == aa['pop_groups'] and ba['colonies']['38']['actual_pop_sum']
        == aa['colonies']['38']['actual_pop_sum'] == 102
        and all(group['key']['species'] == 73 for group in aa['pop_groups'].values())),
    'true_research_bank_and_all_effective_stocks_exact_same_day_no_grants': (
        bc['research_stockpile'] == ac['research_stockpile'] and bc['effective_stockpile'] == ac['effective_stockpile']),
    'government_AP_traditions_crisis_original_colonies_held': all(bc[k] == ac[k]
        for k in ['government', 'ascension_perks', 'traditions', 'crisis', 'owned_colonies']),
    'physical523_completed_colony38_size13_original_owner_and_no_prior_damage': (
        all(p.get(k) == v for k, v in {'owner': 0, 'controller': 0, 'colony': 38, 'planet_size': 13,
            'planet_class': 'pc_tropical', 'colonize_date': '2276.02.01'}.items())
        and 'colonizing_species' not in aa['colonies']['38']
        and all(p['variables'].get(k) == v for k, v in {'eep_q': 13, 'eep_months': 32,
            'eep_old_damage': 0, 'eep_seed_existing': 102, 'eep_seed_need': -2}.items())),
    'native_active_flags360_and_modifier_no_immediate_bite_deposit': (
        all(k in flags for k in ['eep_active', 'eep_native', 'eep_owned_colony_event', 'colony_event', 'being_devoured'])
        and flags.get('recently_eaten_planet', {}).get('flag_days') == 360
        and 'being_devoured_modifier' in p['modifiers'] and 'days=-1' in p['modifiers']
        and ba['planets']['523']['deposits'] == p['deposits']),
    'exact_one_new_owned_situation50331660_target523_progress0': (
        not old_sit and set(sit) == {'50331660'} and sit['50331660'].get('country') == 0
        and sit['50331660'].get('target', {}).get('type') == 'planet'
        and sit['50331660'].get('target', {}).get('id') == 523
        and sit['50331660'].get('progress') == 0 and sit['50331660'].get('approach') == 'eep_devour_approach'),
    'all_original_owned_ship_fleet_identity_designs_and_25_military_held': (
        b['owned_ship_ids'] == a['owned_ship_ids'] and b['owned_fleet_ids'] == a['owned_fleet_ids']
        and living(b) == living(a) and len(living(a)) == 25
        and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in a['owned_ships_raw'].items())),
    'no_new_pending_message_or_active_owned_combat': not a['pending_raw'] and b['messages_raw'] == a['messages_raw']
        and not any(q.ids(q.block(q.block(raw, 'combat'), 'in_combat_with')) for raw in a['owned_fleets_raw'].values()),
}
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_TERRAVORE_FOURTH_DEVOUR_START_COMPONENT' if passed else 'FAIL',
    'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'], 'date': aa['date'],
    'paid_births': pre['paid_births'], 'situation_id': 50331660, 'source_planet': 523, 'source_colony': 38,
    'source_q': 13, 'months_required': 32, 'before_state': b, 'after_state': a,
    'scope': 'Actual same-day native decision start only. No completion, C60 Queen, Menace tier or full route acceptance.'}
out = run / (after + '-native-devour-start-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks),
    'failed': [k for k, v in checks.items() if v is not True], 'date': proof['date']}), flush=True)
assert passed, 'Original native start failure retained; no calendar continuation'
