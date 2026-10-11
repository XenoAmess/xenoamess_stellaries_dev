"""Documented Mod core during ordinary native colonization; endpoint economy only."""
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
load = lambda name: json.loads((run / name).read_text('utf-8'))
omit = lambda raw, keys: [(k, v, o) for k, v, o in q.fields(raw) if k not in keys]
obs = load(after + '-construction-boundary-observation.json')
oe = load(after + '-boundary-observation-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
bc, ac = ba['countries']['0'], aa['countries']['0']
cb, ca = ba['colonies']['0'], aa['colonies']['0']
cal = load(after + '-calendar-receipt.json')
ce = load(after + '-calendar-execution.json')
pre = load(cal['prior_proof_file'])
pe = load(cal['prior_execution_stage'] + '-execution.json')
anchor_stage = 'terravore-fourth-target523-colonization-ordered'
anchor = load(anchor_stage + '-target523-colonization-order-proof.json')
anchor_ex = load(anchor_stage + '-order-guard-v2-execution.json')

def ordinal(date):
    y, m, d = map(int, date.split('.'))
    return y * 360 + (m - 1) * 30 + d - 1

ob, oa = ordinal(ba['date']), ordinal(aa['date'])
days = oa - ob
months = sum(i % 30 == 0 for i in range(ob + 1, oa + 1))
growth = ca['actual_pop_sum'] - cb['actual_pop_sum']
resources = ['energy', 'minerals', 'alloys', 'unity']
net = {k: sum((D(str(v.get(k, 0))) for v in ac['budget_categories']['current_month']['balance'].values()), D(0)) for k in resources}
stock_delta = {k: D(str(ac['effective_stockpile'].get(k, 0))) - D(str(bc['effective_stockpile'].get(k, 0))) for k in set(bc['effective_stockpile']) | set(ac['effective_stockpile'])}

def own_structure(st):
    au = st['audit']
    districts = au['colonies']['0']['districts']
    zones = {i for d in districts for i in au['districts'][str(d)]['zones'] if i != 4294967295}
    buildings = {i for z in zones for i in q.ids(q.block(q.block(st['raw_roots']['zones'], str(z)), 'buildings'))}
    ids = {'districts': districts, 'zones': sorted(zones), 'buildings': sorted(buildings), 'deposit': au['planets']['7']['deposits']}
    return {root: {str(i): q.block(st['raw_roots'][root], str(i)) for i in entries} for root, entries in ids.items()}

def jobs_ok():
    bj, aj = [{i:job for i,job in audit['pop_jobs'].items() if job['planet']==0} for audit in [ba,aa]]
    return bj.keys() == aj.keys() and all(
        {k: v for k, v in job.items() if k not in {'workforce', 'bonus_workforce'}} == {k: v for k, v in aj[i].items() if k not in {'workforce', 'bonus_workforce'}}
        and all(aj[i][k] >= 0 or aj[i][k] == job[k] == -1 for k in ['workforce', 'bonus_workforce']) for i, job in bj.items())

def living_military(st):
    return {sid for raw in st['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
            for sid in q.ids(q.block(raw, 'ships')) if q.scalars(st['owned_ships_raw'][str(sid)]).get('hitpoints', 0) > 0 and q.scalars(st['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}

def birth_ship_ok(identity, idle_system=None):
    sid, fid = str(identity['ship_id']), str(identity['fleet_id'])
    raw = a['owned_ships_raw'].get(sid, '')
    fleet = a['owned_fleets_raw'].get(fid, '')
    ss = q.scalars(raw)
    return (ss.get('fleet') == int(fid) and q.ids(q.block(fleet, 'ships')) == [int(sid)]
            and q.scalars(q.block(raw, 'colonization_data')) == {'species': 73}
            and q.scalars(q.block(raw, 'ship_design_implementation')) == {'design': 150995039, 'upgrade': 4294967295, 'growth_stage': 0}
            and ss.get('construction_date') == identity['birth_date']
            and all(ss.get(k) == value for k, value in [('hitpoints', 625), ('armor_hitpoints', 125), ('shield_hitpoints', 320)])
            and q.scalars(q.block(fleet, 'properties')).get('mia') != 'yes'
            and not q.ids(q.block(q.block(fleet, 'combat'), 'in_combat_with'))
            and (idle_system is None or (q.scalars(q.block(q.block(fleet, 'movement_manager'), 'coordinate')).get('origin') == idle_system and not q.block(fleet, 'current_order'))))

def engineering_queue(tech):
    raw = q.block(tech, 'engineering_queue')
    tokens = list(q.tokens(raw))
    return q.scalars(raw[tokens[0][2]:tokens[-1][1]])

bt, at = bc['tech_status'], ac['tech_status']
beng, aeng = engineering_queue(bt), engineering_queue(at)
fleet = a['owned_fleets_raw'].get('863', '')
order = q.block(q.block(fleet, 'current_order'), 'colonize_planet_order')
movement = q.block(fleet, 'movement_manager')
path = q.block(movement, 'path')
arrival = q.scalars(path).get('date')
path_origins = [q.scalars(q.block(v, 'coordinate')).get('origin') for k, v, o in q.fields(path) if k == 'node' and o]
station = q.scalars(a['owned_ships_raw'].get('67109591', ''))
home_ids = {sid for fid in ['83886903', '33555259', '67109603'] for sid in q.ids(q.block(b['owned_fleets_raw'].get(fid, ''), 'ships'))}
old_designs, new_designs = [q.block(st['country0_raw'], 'ship_design_collection') for st in [b, a]]
old_messages = {q.scalars(v).get('notification') for v in b['messages_country0_raw']}
new_messages = [v for v in a['messages_country0_raw'] if q.scalars(v).get('notification') not in old_messages]
new_mod_messages = [v for v in new_messages if 'eep_' in v or 'TERRAVORE_CONSUME' in v]
active_combat = [fid for fid, raw in a['owned_fleets_raw'].items() if q.ids(q.block(q.block(raw, 'combat'), 'in_combat_with'))]
boundaries = []
if b['pending_country0_raw'] != a['pending_country0_raw']:
    boundaries.append('native_pending_event_changed')
if new_mod_messages:
    boundaries.append('new_Mod_or_consume_message')
if active_combat:
    boundaries.append('native_owned_active_combat')
if ac['effective_stockpile']['menace'] >= 1000:
    boundaries.append('native_Menace_level2_threshold')
known_sources = {'6e79b4a2d9c7e9b92d87d2c132bd99a9f5ec387318697aa38535930d29f0143c', 'fc1206b6672760a582f36ac16c8b864d43f22055f3c7bd60a495246fa8b77e72', h.sha256(Path(__file__))}
mod_flags = lambda raw: [(k, v, o) for k, v, o in q.fields(q.block(raw, 'flags')) if k.startswith('eep_')]
checks = {
    'original_order16_PASS_actual0_source_SHA_held': len(anchor['checks']) == 16 and all(v is True for v in anchor['checks'].values()) and anchor_ex['returncode'] == 0 and anchor_ex['helper_sha256'] == h.sha256(run / 'priority_terravore_fourth_colonization_order_guard_v2.py') == '413cafbe0f55610cc5e70f8d38d2429a8e1519d426674dd88b974e08719d506e' and anchor['after_sha256'] == h.sha256(run / (anchor_stage + '.sav')) == '7b01568d2ee040befbdcfb2bd17cbf394bd35798026829f08afff38081665887',
    'prior_actual_PASS_exit0_original_source_SHA': pre['status'].startswith('PASS_') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pe['returncode'] == 0 and pe['helper_sha256'] in known_sources and pe['helper_sha256'] == h.sha256(run / Path(pe['command'][1]).name) and pre['after_sha256'] == ba['save_sha256'],
    'complete_original_observation6_actual0_source': len(obs['checks']) == 6 and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0 and oe['helper_sha256'] == h.sha256(run / 'priority_terravore_construction_boundary_observation.py') == 'e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
    'bounded_native_calendar_actual0_source_original_dates': cal['status'] == 'CALENDAR_CONFIRMED' and cal['days'] == days and 1 <= days <= 90 and months <= 3 and ce['returncode'] == 0 and ce['helper_sha256'] == h.sha256(run / 'formal_production_native_calendar_checked_v2.py') == '66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
    'original_SAV_SHA_pair': all(st['audit']['save_sha256'] == h.sha256(run / (stage + '.sav')) for st, stage in [(b, before), (a, after)]),
    'production41_original_tree_simp_chinese': meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41 and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
    'unfiltered_original2814_error_held': (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes() == (run / (after + '-error-after.log')).read_bytes() and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
    'EEP_full_variables_flags_two_colonies_species73_held': bc['variables'] == ac['variables'] and mod_flags(b['country0_raw']) == mod_flags(a['country0_raw']) and all(ac['variables'][k] == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_worlds': 3, 'eep_psi': 1, 'eep_stage': 1, 'eep_fleet_stage': 0}.items()) and bc['owned_colonies'] == ac['owned_colonies'] == [0,38] and all(group['key']['species']==73 for group in aa['pop_groups'].values()) and ba['species']['73'] == aa['species']['73'],
    'mother18_D14_paid27_structure_jobs_held': all(ba['planets']['7'][k] == aa['planets']['7'][k] for k in ['owner', 'controller', 'colony', 'planet_size', 'modifiers', 'deposits']) and aa['planets']['7']['planet_size'] == 18 and own_structure(b) == own_structure(a) and sum(aa['districts'][str(i)]['level'] for i in ca['districts']) == 27 and jobs_ok(),
    'coarse_population_growth_bound_positive_housing_amenities': 0 <= growth <= 10 * months and ca['total_housing'] == 14100 and ca['free_housing'] == 14100 - ca['housing_usage'] > 0 and 0 <= ca['actual_pop_sum'] - ca['housing_usage'] <= 10 and ca['actual_pop_sum'] == ca['employable_pops'] == ca['num_sapient_pops'] and ca['free_amenities'] > 0 and ca['crime'] == 0,
    'endpoint_economy_positive_and_true_resources_nondecreasing': all(net[k] > 0 and stock_delta[k] >= 0 for k in resources),
    'true_P_S_bank_nondecreasing_original_Eng_queue': all(ac['research_stockpile'][k] >= bc['research_stockpile'][k] for k in ['physics_research', 'society_research']) and bc['research_stockpile']['engineering_research'] == ac['research_stockpile']['engineering_research'] == 0 and omit(bt, {'stored_techpoints', 'engineering_queue'}) == omit(at, {'stored_techpoints', 'engineering_queue'}) and {k: v for k, v in beng.items() if k != 'progress'} == {k: v for k, v in aeng.items() if k != 'progress'} and aeng['technology'] == 'tech_mass_drivers_3' and aeng['progress'] >= beng['progress'],
    'original_paid_births_species_design_health_identity_held': pre['paid_births'] == anchor['paid_births'] and birth_ship_ok(pre['paid_births']['100663340'], 0),
    'actual_target523_owned_colony38_native_founding': all(q.scalars(a['planet_raw']['523']).get(k)==v for k,v in {'owner':0,'controller':0,'colony':38,'planet_size':13,'colonize_date':'2273.11.26'}.items()) and '16779032' not in a['owned_ships_raw'] and '863' not in a['owned_fleets_raw'],
    'no_unpaid_new_owned_ship_original_ship_designs_held': set(b['owned_ship_ids']) == set(a['owned_ship_ids']) and all(q.block(raw, 'ship_design_implementation') == q.block(b['owned_ships_raw'][sid], 'ship_design_implementation') for sid, raw in a['owned_ships_raw'].items() if sid!='1931'),
    'all25_military_alive_home20_held': living_military(b) == living_military(a) and len(living_military(a)) == 25 and len(home_ids) == 20 and home_ids <= living_military(a),
    'rear_base_owned_station804_health_above6000': station.get('fleet') == 804 and q.ids(q.block(a['owned_fleets_raw'].get('804', ''), 'ships')) == [67109591] and station.get('hitpoints', 0) > 6000,
    'original_second_colonizer_species_identity_alive': q.scalars(q.block(a['owned_ships_raw'].get('50333369',''), 'colonization_data')) == {'species':73} and q.scalars(a['owned_ships_raw'].get('50333369','')).get('fleet')==33555278 and q.scalars(a['owned_ships_raw'].get('50333369','')).get('hitpoints',0)>0,
    'government_AP_traditions_crisis1_held': all(bc[k] == ac[k] for k in ['government', 'ascension_perks', 'traditions']) and q.block(b['country0_raw'], 'crisis_progression') == q.block(a['country0_raw'], 'crisis_progression') and ac['effective_stockpile']['menace'] >= bc['effective_stockpile']['menace'],
}
passed = all(v is True for v in checks.values())
max_days = 90
pending = [q.scalars(raw) for raw in a['pending_country0_raw']]
future_dates = [v['date'] for v in pending if isinstance(v.get('date'), str) and ordinal(v['date']) > oa]
if future_dates:
    max_days = min(max_days, min(ordinal(v) - oa - 1 for v in future_dates))
event_module = q.block(q.block(a['country0_raw'], 'modules'), 'standard_event_module')
delays = [q.scalars(raw)['days'] for k, raw, o in q.fields(event_module) if k == 'delayed_event' and o and 'days' in q.scalars(raw)]
if delays:
    max_days = min(max_days, max(0, min(delays) - 1))
# Native phase boundaries are recorded without relabeling them as Mod failures.
for fid, raw in a['owned_fleets_raw'].items():
    ss=q.scalars(raw)
    if q.scalars(q.block(raw,'properties')).get('mia')=='yes' and isinstance(ss.get('return_date'),str):
        delta=ordinal(ss['return_date'])-oa
        max_days=min(max_days,max(0,delta-1))
    if q.scalars(q.block(b['owned_fleets_raw'].get(fid,''),'properties')).get('mia') != q.scalars(q.block(raw,'properties')).get('mia'):
        boundaries.append('native_MIA_phase_changed_'+fid)
if aeng.get('technology') != beng.get('technology'):
    boundaries.append('native_engineering_queue_changed')
with __import__('zipfile').ZipFile(run/(after+'.sav')) as archive:
    roots={k:v for k,v,o in q.fields(archive.read('gamestate').decode('utf-8-sig')) if o}
base=q.block(q.block(roots['starbase_mgr'],'starbases'),'158')
if q.scalars(q.block(roots['colony'],'38')).get('colonizing_species') != 73:
    boundaries.append('native_colony38_colonizing_species_phase_changed')
if q.scalars(base).get('level')!='starbase_level_outpost':
    boundaries.append('native_paid_front158_upgrade_phase_changed')
if any(isinstance(v.get('date'),str) and ordinal(v['date'])<=oa for v in pending):
    boundaries.append('native_pending_date_reached_requires_UI_review')
max_days=min(max_days,max(0,ordinal('2276.02.01')-oa-1))
ready = passed and not boundaries and max_days > 0
proof = {'status': 'PASS_NATIVE_TERRAVORE_TARGET523_COLONIZATION_WAIT_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'], 'date': aa['date'], 'days': days,
         'native_colonization_calendar_ready': ready, 'maximum_days_to_colonization_boundary': max_days if ready else 0,
         'paid_births': pre['paid_births'], 'boundaries': boundaries, 'actual_arrival_estimate': arrival,
         'actual_population': ca['actual_pop_sum'], 'coarse_growth_delta': growth, 'native_month_ticks': months,
         'endpoint_net': {k: str(v) for k, v in net.items()}, 'actual_stock_delta': {k: str(v) for k, v in stock_delta.items()},
         'actual_colonizer_coordinate': q.scalars(q.block(movement, 'coordinate')), 'path_remaining_origins': path_origins,
         'actual_pending': pending, 'native_delayed_days': delays, 'new_country0_messages_raw': new_messages,
         'active_combat_fleets': active_combat,
         'native_colony_population': aa['colonies']['38']['actual_pop_sum'], 'front158_raw': base, 'scope': 'Mod core during actual native colonization only; endpoint/coarse growth, not exact monthly ledgers, completed colony, swallow or full acceptance.'}
output = run / (after + '-target523-colonization-wait-proof.json')
assert not output.exists()
h.write_json(output, proof)
print(json.dumps({k: proof[k] for k in ['status', 'date', 'actual_population', 'actual_arrival_estimate', 'boundaries', 'maximum_days_to_colonization_boundary']} | {'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}, ensure_ascii=True), flush=True)
assert passed
