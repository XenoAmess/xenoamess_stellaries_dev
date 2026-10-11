"""Documented pre-bite native situation waiting; native internal migration retained."""
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

before, after = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda name: json.loads((run / name).read_text('utf-8-sig'))
sha = h.sha256
obs = load(after + '-construction-boundary-observation.json')
oe = load(after + '-boundary-observation-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
bc, ac = ba['countries']['0'], aa['countries']['0']
cal = load(after + '-calendar-receipt.json')
ce = load(after + '-calendar-execution.json')
pre = load(cal['prior_proof_file'])
pe = load(cal['prior_execution_stage'] + '-execution.json')
anchor_stage = 'terravore-fourth-native-devour-started'
anchor = load(anchor_stage + '-native-devour-start-proof.json')
ae = load('terravore-fourth-native-devour-start-independent-guard-execution.json')
inv_name = 'terravore-fourth-native-devour-first-month-native-auto-migration-investigation.json'
inv = load(inv_name)

def ordinal(date):
    y, m, d = map(int, date.split('.'))
    return y * 360 + (m - 1) * 30 + d - 1

ob, oa = ordinal(ba['date']), ordinal(aa['date'])
days = oa - ob
months = sum(i % 30 == 0 for i in range(ob + 1, oa + 1))
total = lambda au: sum(au['colonies'][str(i)]['actual_pop_sum'] for i in au['countries']['0']['owned_colonies'])
growth = total(aa) - total(ba)
resources = ['energy', 'minerals', 'alloys', 'unity']
net = {k: sum((D(str(v.get(k, 0))) for v in ac['budget_categories']['current_month']['balance'].values()), D(0)) for k in resources}
stock_delta = {k: D(str(ac['effective_stockpile'].get(k, 0))) - D(str(bc['effective_stockpile'].get(k, 0))) for k in resources}

def own_structure(st):
    au = st['audit']
    districts = au['colonies']['0']['districts']
    zones = {i for d in districts for i in au['districts'][str(d)]['zones'] if i != 4294967295}
    buildings = {i for z in zones for i in q.ids(q.block(q.block(st['raw_roots']['zones'], str(z)), 'buildings'))}
    groups = {'districts': districts, 'zones': sorted(zones), 'buildings': sorted(buildings), 'deposit': au['planets']['7']['deposits']}
    return {root: {str(i): q.block(st['raw_roots'][root], str(i)) for i in ids} for root, ids in groups.items()}

def jobs_ok():
    bj, aj = [{i: job for i, job in au['pop_jobs'].items() if job['planet'] == 0} for au in [ba, aa]]
    return bj.keys() == aj.keys() and all(
        {k: v for k, v in job.items() if k not in {'workforce', 'bonus_workforce'}}
        == {k: v for k, v in aj[i].items() if k not in {'workforce', 'bonus_workforce'}}
        and all(aj[i][k] >= 0 or aj[i][k] == job[k] == -1 for k in ['workforce', 'bonus_workforce']) for i, job in bj.items())

def living(st):
    return {sid for raw in st['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
        for sid in q.ids(q.block(raw, 'ships')) if q.scalars(st['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0
        and q.scalars(st['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}

def eng_queue(tech):
    raw = q.block(tech, 'engineering_queue')
    tokens = list(q.tokens(raw))
    return q.scalars(raw[tokens[0][2]:tokens[-1][1]])

bs, ats = [au['situations'].get('50331660', {}) for au in [ba, aa]]
bt, at = bc['tech_status'], ac['tech_status']
be, eng = eng_queue(bt), eng_queue(at)
omit = lambda raw, keys: [(k, v, o) for k, v, o in q.fields(raw) if k not in keys]
p, bp = aa['planets']['523'], ba['planets']['523']
source_sit = q.block(q.block(a['raw_roots']['situations'], 'situations'), '50331660')
routine_delays = [(v, q.scalars(v)) for k, v, opened in q.fields(source_sit) if k == 'delayed_event' and opened]
known_delays = all(v.get('event') == 'eep.21' and v.get('days') == 1
    and q.scalars(q.block(raw, 'scope')).get('type') == 'situation'
    and q.scalars(q.block(raw, 'scope')).get('id') == 50331660
    and ats.get('progress', 32) < 32 for raw, v in routine_delays)
boundaries = []
if not known_delays:
    boundaries.append('unknown_situation_delayed_event')
country_event_module = q.block(q.block(a['country0_raw'], 'modules'), 'standard_event_module')
if any(k == 'delayed_event' and opened for k, v, opened in q.fields(country_event_module)):
    boundaries.append('unknown_country_delayed_event')
if a['pending_country0_raw']:
    boundaries.append('native_pending_event_requires_review')
if any(q.ids(q.block(q.block(raw, 'combat'), 'in_combat_with')) for raw in a['owned_fleets_raw'].values()):
    boundaries.append('native_owned_active_combat')
if any(q.scalars(q.block(raw, 'properties')).get('mia') == 'yes' for raw in a['owned_fleets_raw'].values()):
    boundaries.append('native_owned_MIA_requires_review')
new_messages = [v for v in a['messages_country0_raw'] if v not in b['messages_country0_raw']]
if any('eep_' in v or 'TERRAVORE_CONSUME' in v for v in new_messages):
    boundaries.append('new_Mod_or_native_consume_message')
if b['war1_battles_raw'] != a['war1_battles_raw']:
    boundaries.append('native_war_battle_history_changed')
if ac['effective_stockpile']['menace'] >= 1000:
    boundaries.append('native_Menace_level2_threshold')
if be.get('technology') != eng.get('technology'):
    boundaries.append('native_engineering_queue_changed')
manifest, tree = h.tree_manifest(h.MOD_ROOT)
checks = {
    'original_start14_PASS_actual0_source_SAV_and_births_bound': (
        len(anchor['checks']) == 14 and all(v is True for v in anchor['checks'].values())
        and ae['returncode'] == 0 and ae['helper_sha256'] == sha(run / 'priority_terravore_fourth_native_devour_start_guard.py')
        == '091aa3d3db0c131f96d4ca8f051e67b0d143055d5c4240cd8b46152a8c367411'
        and anchor['after_sha256'] == sha(run / (anchor_stage + '.sav'))
        == '53c2273f3686e57c8270446a5e2e3fca8b259cfb4e11c31a134660cca91dbec2'
        and pre['paid_births'] == anchor['paid_births']),
    'prior_component_PASS_actual0_source_and_original_SAV': (
        pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values())
        and pe['returncode'] == 0 and pe['helper_sha256'] == sha(Path(pe['command'][1]))
        and pe['helper_sha256'] in {ae['helper_sha256'], sha(Path(__file__))}
        and pre['after_sha256'] == ba['save_sha256']),
    'six_original_observations_alltrue_actual0_exact_source': (
        len(obs['checks']) == 6 and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0
        and oe['helper_sha256'] == sha(run / 'priority_terravore_construction_boundary_observation.py')
        == 'e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678'),
    'bounded_native_calendar_actual0_date_days_original_SAVs': (
        1 <= days <= 90 and '2276.02.01' <= ba['date'] < aa['date'] <= '2277.01.30'
        and cal['date'] == aa['date'] and cal['start_date'] == ba['date'] and cal['days'] == days
        and ce['returncode'] == 0 and ce['helper_sha256'] == sha(run / 'formal_production_native_calendar_checked_v2.py')
        == '66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc'
        and all(au['save_sha256'] == sha(run / (stage + '.sav')) for au, stage in [(ba, before), (aa, after)])
        and obs['before_sha256'] == ba['save_sha256'] and obs['after_sha256'] == aa['save_sha256']),
    'production41_tree_version020_simp_chinese_held': len(manifest) == 41 and meta['version'] == '0.2.0'
        and meta['language'] == 'l_simp_chinese' and tree == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
    'unfiltered_original_error2814_exact_bytes_SHA_held': (
        (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and sha(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'),
    'all_EEP_C49_D14_worlds3_PSI1_credit_held': bc['variables'] == ac['variables']
        and all(ac['variables'].get(k) == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_worlds': 3,
            'eep_psi': 1, 'eep_stage': 1, 'eep_fleet_stage': 0}.items()),
    'mother_structure27_levels_and_original_jobs_held': own_structure(b) == own_structure(a) and jobs_ok()
        and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts']) == 27,
    'mother_housing_amenities_crime_and_owner_held': aa['colonies']['0']['actual_pop_sum'] >= 10000
        and aa['colonies']['0']['free_housing'] > 0 and aa['colonies']['0']['free_amenities'] > 0
        and aa['colonies']['0']['crime'] == 0 and aa['planets']['7']['owner'] == aa['planets']['7']['controller'] == 0,
    'only_two_original_colonies_all_species73_empire_coarse_growth': (
        set(bc['owned_colonies']) == set(ac['owned_colonies']) == {0, 38} and 0 <= growth <= 10 * months
        and all(group['key']['species'] == 73 and group['planet'] in [0, 38] for au in [ba, aa] for group in au['pop_groups'].values())),
    'source_completed_colony38_size13_Q13_month32_no_native_damage': (
        all(p.get(k) == bp.get(k) == v for k, v in {'owner': 0, 'controller': 0, 'colony': 38,
            'planet_size': 13, 'planet_class': 'pc_tropical', 'colonize_date': '2276.02.01'}.items())
        and p['variables'] == bp['variables'] == anchor['after_state']['audit']['planets']['523']['variables']
        and p['deposits'] == bp['deposits'] and aa['colonies']['38']['actual_pop_sum'] >= 100
        and 'colonizing_species' not in aa['colonies']['38']),
    'active_native_flags_original360_and_modifier_held': (
        all(k in p['flags'] for k in ['eep_active', 'eep_native', 'eep_owned_colony_event', 'colony_event', 'being_devoured'])
        and p['flags']['recently_eaten_planet']['flag_date'] == bp['flags']['recently_eaten_planet']['flag_date']
        == anchor['after_state']['audit']['planets']['523']['flags']['recently_eaten_planet']['flag_date']
        and bp['flags']['recently_eaten_planet']['flag_days'] - p['flags']['recently_eaten_planet']['flag_days'] == days
        and p['flags']['recently_eaten_planet']['flag_days'] == 360 - (oa - ordinal('2276.02.01')) > 0
        and 'being_devoured_modifier' in p['modifiers']),
    'same_owned_situation_target_approach_progress_exact_month_ticks': (
        set(ba['situations']) == set(aa['situations']) == {'50331660'}
        and all(ats.get(k) == bs.get(k) == v for k, v in {'country': 0, 'type': 'situation_eep_devouring',
            'approach': 'eep_devour_approach', 'stage': 0}.items())
        and ats.get('target') == bs.get('target') == {'type': 'planet', 'id': 523, 'opener_id': 4294967295}
        and ats.get('progress') == bs.get('progress', 0) + months
        == oa // 30 - ordinal('2276.02.01') // 30 < 32),
    'routine_monthly_eep21_only_progress_below_completion_bound': known_delays,
    'native_migration_INV_original_two_UIs_sources_and_SAV_pair_bound': (
        sha(run / inv_name) == '81d4a76dba287f2e657aa6fb9fa96c924d314ee03fe38564424893fca338e9a2'
        and inv['before_sha256'] == anchor['after_sha256']
        and inv['after_sha256'] == sha(run / 'terravore-fourth-native-devour-first-month.sav')
        == '1684120e5962f61016b471acb1e36824310caf701e6c68d908fb7f97811ec7ad'
        and all(sha(Path(v['path'])) == v['sha256'] for v in inv['native_sources'])
        and all(sha(run / v['image']) == v['sha256'] for v in inv['ui_originals'].values())),
    'E_M_A_U_endpoint_net_positive_stock_nondecreasing': all(net[k] > 0 and stock_delta[k] >= 0 for k in resources),
    'true_P_S_banks_monotone_Eng0_starbase4_native_steady_queue': (
        all(ac['research_stockpile'][k] >= bc['research_stockpile'][k] for k in ['physics_research', 'society_research'])
        and ac['research_stockpile']['engineering_research'] == bc['research_stockpile']['engineering_research'] == 0
        and omit(bt, {'stored_techpoints', 'engineering_queue'}) == omit(at, {'stored_techpoints', 'engineering_queue'})
        and {k: v for k, v in be.items() if k != 'progress'} == {k: v for k, v in eng.items() if k != 'progress'}
        and eng.get('technology') == 'tech_starbase_4' and eng.get('progress', 0) >= be.get('progress', 0)),
    'all_owned_ship_identity_designs_and_original25_military_alive': (
        b['owned_ship_ids'] == a['owned_ship_ids'] and living(b) == living(a) and len(living(a)) == 25
        and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][sid], 'ship_design_implementation')
            for sid, raw in a['owned_ships_raw'].items())),
    'government_AP_traditions_crisis1_and_mod_flags_held': (
        all(bc[k] == ac[k] for k in ['government', 'ascension_perks', 'traditions', 'crisis'])
        and {k: v for k, v in bc['flags'].items() if k.startswith('eep_')}
        == {k: v for k, v in ac['flags'].items() if k.startswith('eep_')}),
}
passed = all(v is True for v in checks.values())
maximum = min(90, max(0, ordinal('2277.02.01') - oa - 1))
ready = passed and not boundaries and maximum > 0
proof = {'status': 'PASS_NATIVE_TERRAVORE_FOURTH_DEVOUR_WAIT_COMPONENT' if passed else 'FAIL',
    'checks': checks, 'date': aa['date'], 'days': days, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'paid_births': anchor['paid_births'], 'boundaries': boundaries, 'native_devour_calendar_ready': ready,
    'maximum_days_to_native_bite_boundary': maximum if ready else 0, 'situation_progress': ats.get('progress'),
    'mother_population': aa['colonies']['0']['actual_pop_sum'], 'source_population': aa['colonies']['38']['actual_pop_sum'],
    'empire_population': total(aa), 'coarse_empire_growth': growth, 'native_month_ticks': months,
    'mother_population_delta': aa['colonies']['0']['actual_pop_sum'] - ba['colonies']['0']['actual_pop_sum'],
    'source_population_delta': aa['colonies']['38']['actual_pop_sum'] - ba['colonies']['38']['actual_pop_sum'],
    'endpoint_net': {k: str(v) for k, v in net.items()}, 'stock_delta': {k: str(v) for k, v in stock_delta.items()},
    'routine_situation_delays_raw': [raw for raw, v in routine_delays], 'new_messages_raw': new_messages,
    'scope': 'Pre-bite native situation and Mod core; native internal migration and coarse empire growth. Not precise monthly ledger, consume reward, settlement, Queen C60 or full route acceptance.'}
out = run / (after + '-native-devour-wait-v2-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True],
    'date': proof['date'], 'progress': proof['situation_progress'], 'boundaries': boundaries, 'maximum_days': proof['maximum_days_to_native_bite_boundary']}), flush=True)
assert passed, 'Original waiting component failure retained; no calendar continuation'
