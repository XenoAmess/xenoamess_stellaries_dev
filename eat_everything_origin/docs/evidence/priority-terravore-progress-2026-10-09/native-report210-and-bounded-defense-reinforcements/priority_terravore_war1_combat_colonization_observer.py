"""Bounded native war1 construction/colonization observation, no state mutations."""
import json, logging, re, shutil, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r, audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, metadata = h.load_run()
assert metadata['version'] == '0.2.0' and metadata['language'] == 'l_simp_chinese'
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
def load(name):
    return json.loads((run / name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        fields = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage + '.audit.json'), fields, {k: v for k, v, o in fields if o}
def objects(text):
    return {k: v for k, v, o in q.fields(text) if o}
def omit(text, keys):
    return [(k, v, o) for k, v, o in q.fields(text) if k not in keys]
def owned(country):
    return list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(country, 'fleets_manager'), 'owned_fleets'))))
def combat(fleet):
    return list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(fleet, 'combat'), 'in_combat_with'))))
b, bf, br = read(before)
a, af, ar = read(after)
bc, ac = b['countries']['0'], a['countries']['0']
bcr, acr = [q.block(top['country'], '0') for top in [br, ar]]
bfl, afl = objects(br['fleet']), objects(ar['fleet'])
bsh, ash = objects(br['ships']), objects(ar['ships'])
bo, ao = owned(bcr), owned(acr)
enemy_owned = owned(q.block(ar['country'], '1'))
military = lambda fleets, own: {i: q.ids(q.block(fleets[str(i)], 'ships')) for i in own
                               if q.scalars(fleets[str(i)]).get('ship_class') == 'shipclass_military'}
bm, am = military(bfl, bo), military(afl, ao)
old_ships = [i for ids in bm.values() for i in ids]
current_ships = [i for ids in am.values() for i in ids]
added_ships = [i for i in current_ships if i not in old_ships]
lost_ships = [i for i in old_ships if i not in current_ships]
original8 = {1816, 1817, 33555519, 33556208, 33556207, 50332878, 1807, 1810}
paid_ships = [i for i in current_ships if i not in original8]
receipt = load(after + '-calendar-receipt.json')
days = receipt['days']
validate_native_interval(b['date'], a['date'], days)
pre = load(receipt['prior_proof_file'])
execution = load(receipt['prior_execution_stage'] + '-execution.json')
paid_stage = 'terravore-war1-reinforce-paid'
paid = load(paid_stage + '-war1-reinforcement-payment-proof.json')
paid_execution = load(paid_stage + '-guard-execution.json')
queue = lambda top: q.block(q.block(q.block(top['construction'], 'queue_mgr'), 'queues'), '3')
bq, aq = queue(br), queue(ar)
bids, aids = [q.ids(q.block(v, 'items')) for v in [bq, aq]]
items = lambda top: objects(q.block(q.block(top['construction'], 'item_mgr'), 'items'))
bi, ai = items(br), items(ar)
completed = len(bids) - len(aids)
base_b, base_a = [q.block(q.block(top['starbase_mgr'], 'starbases'), '0') for top in [br, ar]]
pending = [q.scalars(v) for k, v, o in af if k == 'player_event' and o and q.scalars(v).get('country') == 0]
active = {i: combat(afl[str(i)]) for i in ao if combat(afl[str(i)])}
target = a['planets']['1085']
mother = a['planets']['7']
colony = a['colonies']['37']
nets = {k: sum(D(str(v.get(k, 0))) for v in ac['budget_categories']['current_month']['balance'].values())
        for k in ['energy', 'minerals', 'alloys', 'unity', 'trade']}
project2 = lambda country: [v for k, v, o in q.fields(q.block(country, 'events'))
                          if k == 'special_project' and o and q.scalars(v).get('id') == 2]
war = q.block(ar['war'], '1')
checks = {
    'prior_all_PASS_actual0_original_helper_bound': pre['status'].startswith('PASS_')
        and bool(pre['checks']) and all(v is True for v in pre['checks'].values())
        and pre['after_sha256'] == b['save_sha256'] and execution['returncode'] == 0
        and h.sha256(run / Path(execution['command'][1]).name) == execution['helper_sha256'],
    'actual_SHA_pair_unique_native_calendar1_to30_actual0':
        all(h.sha256(run / (st + '.sav')) == au['save_sha256'] for st, au in [(before, b), (after, a)])
        and 1 <= days <= 30 and receipt['status'] == 'CALENDAR_CONFIRMED'
        and receipt['start_date'] == b['date'] and receipt['date'] == a['date']
        and load(after + '-calendar-execution.json')['returncode'] == 0,
    'fixed_original45_paid30_orders_SHA_actual0_bound':
        paid['status'] == 'PASS_TERRAVORE_WAR1_REINFORCEMENT_PAYMENT_COMPONENT'
        and len(paid['checks']) == 45 and all(v is True for v in paid['checks'].values())
        and paid['after_sha256'] == h.sha256(run / (paid_stage + '.sav'))
        == 'b4344cd46f423531c3a23607248276c9b963cfa66be6d6572fb0ad08637ca36c'
        and paid_execution['returncode'] == 0
        and paid_execution['helper_sha256'] == 'ffe533def5fd2da48252413df05b336729a7935fc59428929a1a576943cd51e1',
    'paid_orders_contiguous_completion_and_original_nonprogress_raw_held':
        completed >= 0 and aids == bids[completed:]
        and aids == paid['native_queue_ids'][len(paid_ships):]
        and all(omit(bi[str(i)], {'progress'}) == omit(ai[str(i)], {'progress'})
                and 0 <= q.scalars(ai[str(i)])['progress'] < 60 for i in aids),
    'actual_paid_ship_count_and_order_conservation_no_unknown_loss':
        len(added_ships) == completed and not lost_ships and len(paid_ships) + len(aids) == 30
        and original8 <= set(current_ships),
    'all_military_relations_unique_positive_actual_hull':
        len(current_ships) == len(set(current_ships))
        and all(q.scalars(ash[str(i)])['fleet'] == fid
                and 0 < q.scalars(ash[str(i)])['hitpoints'] <= q.scalars(ash[str(i)])['max_hitpoints']
                for fid, ids in am.items() for i in ids),
    'original8_actual_design_dates_full_HP270_held': all(
        q.scalars(ash[str(i)])['hitpoints'] == q.scalars(ash[str(i)])['max_hitpoints'] == 270
        and q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))['design'] == 167772797
        and q.scalars(bsh[str(i)])['construction_date'] == q.scalars(ash[str(i)])['construction_date']
        for i in original8),
    'paid_built_ships_actual_design_dates_and_no_actual_free_upgrade': all(
        q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))['design'] == 385877628
        and q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))['growth_stage'] == 0
        and q.scalars(ash[str(i)])['upgrade_progress'] == 0
        and '2268.03.17' <= q.scalars(ash[str(i)])['construction_date'] <= a['date'] for i in paid_ships)
        and all(b['date'] <= q.scalars(ash[str(i)])['construction_date'] <= a['date'] for i in added_ships)
        and all(q.scalars(bsh[str(i)])['construction_date'] == q.scalars(ash[str(i)])['construction_date']
                for i in set(old_ships) & set(paid_ships)),
    'actual_naval_size5_per_owned_corvette': q.scalars(acr)['fleet_size'] == 5 * len(current_ships),
    'original_two_shipyards_base0_queue3_nonitem_fields_held':
        omit(bq, {'items'}) == omit(aq, {'items'})
        and q.scalars(q.block(base_b, 'modules')) == q.scalars(q.block(base_a, 'modules'))
        == {'0': 'shipyard', '1': 'shipyard'}
        and all(q.scalars(base_b)[k] == q.scalars(base_a)[k]
                for k in ['level', 'type', 'build_queue', 'shipyard_build_queue', 'station'])
        and q.block(base_b, 'buildings') == q.block(base_a, 'buildings'),
    'EEP_ledger_flags_species_targets_and_no_active_task_held':
        bc['variables'] == ac['variables'] and bc['flags'] == ac['flags']
        and all(ac['variables'][k] == v for k, v in {'eep_c': 37, 'eep_g': 0, 'eep_d': 11, 'eep_made': 0, 'eep_worlds': 2, 'eep_psi': 1}.items())
        and b['species'] == a['species'] and b['event_targets'] == a['event_targets'] and not a['situations'],
    'unique_mother_owned_core_capacity11_no_new_bombardment':
        mother['owner'] == mother['controller'] == 0 and mother['colony'] == 0
        and mother['planet_size'] == 18 and mother['variables']['eep_capacity_value'] == 11
        and sum('eep_core' in v['flags'] for v in a['planets'].values()) == 1
        and mother['modifiers'] == b['planets']['7']['modifiers']
        and mother['bombardment_damage'] == 0 and mother['last_bombardment'] == '2261.07.03',
    'all_mother_zones_buildings_districts_raw_held':
        all(q.block(br['zones'], i) == q.block(ar['zones'], i) for i in ['0', '2', '61'])
        and all(q.block(br['districts'], i) == q.block(ar['districts'], i) for i in ['1', '2', '3'])
        and all(q.block(br['buildings'], str(i)) == q.block(ar['buildings'], str(i))
                for zid in ['0', '2', '61'] for i in q.ids(q.block(q.block(ar['zones'], zid), 'buildings'))),
    'original_full_mother_jobs_housing_amenities_stability80_held':
        all(len([j for j in a['pop_jobs'].values() if j['planet'] == 0 and j['type'] == kind
                 and j['workforce'] == j['max_workforce'] == n]) == 1
            for kind, n in [('fabricator', 200), ('coordinator', 2000), ('logistics_drone', 500),
                            ('telepath_drone', 200), ('calculator_physicist', 300), ('calculator_biologist', 300),
                            ('calculator_engineer', 300), ('mining_drone', 2400), ('technician_drone', 1200)])
        and a['colonies']['0']['free_housing'] > 0 and a['colonies']['0']['free_amenities'] > 0
        and a['colonies']['0']['stability'] == 80 and a['colonies']['0']['crime'] == 0,
    'same_native_colony37_1085_owned_species73_still_colonizing':
        bc['owned_colonies'] == ac['owned_colonies'] == [0, 37]
        and target['owner'] == target['controller'] == 0 and target['colony'] == 37
        and target['planet_size'] == 12 and target['planet_class'] == 'pc_alpine'
        and target['bombardment_damage'] == 0 and target['last_bombardment'] == '0.01.01'
        and colony.get('colonizing_species') == 73
        and colony['actual_pop_sum'] >= b['colonies']['37']['actual_pop_sum']
        and all(a['pop_groups'][str(i)]['key']['species'] == 73 for i in colony['pop_groups']),
    'native_finished_PSIONIC1_full_breach_level1_menace90_held':
        len(project2(bcr)) == len(project2(acr)) == 1 and project2(bcr) == project2(acr)
        and q.scalars(project2(acr)[0]).get('status') == 'completed'
        and q.block(bcr, 'crisis_progression') == q.block(acr, 'crisis_progression')
        and ac['effective_stockpile']['menace'] == 90
        and all(q.scalars(q.block(acr, 'flags')).get(k) == value for k, value in [
            ('breached_shroud', 63314904), ('psionic_traditions_unlocked', 63314904),
            ('crisis_special_project_1_complete', 63355224)]),
    'actual_war1_participants_objectives_start_held': q.scalars(war)['start_date'] == '2265.12.30'
        and re.findall(r'\bcountry\s*=\s*(\d+)', q.block(war, 'attackers')) == ['1']
        and re.findall(r'\bcountry\s*=\s*(\d+)', q.block(war, 'defenders')) == ['0']
        and q.scalars(q.block(war, 'attacker_war_goal'))['type'] == 'wg_end_threat_swarm'
        and q.scalars(q.block(war, 'defender_war_goal'))['type'] == 'wg_absorption',
    'current_owned_combat_only_actual_war1_enemy_fleets':
        all(i in enemy_owned for enemies in active.values() for i in enemies),
    'all_actual_primary_stocks_positive_report_actual_nets':
        all(ac['effective_stockpile'][k] > 0 for k in ['energy', 'minerals', 'alloys', 'unity']),
    'unfiltered_error2670_exact_held': (run / (before + '-error-after.log')).read_bytes()
        == (run / (after + '-error-before.log')).read_bytes() == (run / (after + '-error-after.log')).read_bytes()
        and (run / (after + '-error-after.log')).stat().st_size == 2670,
}
if before == paid_stage:
    checks['first_month_exact_477_captured_disabled_no_original_military_loss'] = (
        a['date'] == '2268.04.17' and days == 30
        and 477 in bo and 477 not in ao and 477 in enemy_owned
        and q.ids(q.block(afl['477'], 'ships')) == [1415]
        and q.scalars(ash['1415'])['original_owner'] == 0
        and q.scalars(ash['1415'])['disabled'] == 'yes' and q.scalars(ash['1415'])['hitpoints'] == 1
        and q.scalars(ash['1415'])['last_damage'] == q.scalars(ash['1415'])['last_combat_activity'] == '2268.03.22'
        and q.scalars(ash['1415'])['construction_date'] == q.scalars(bsh['1415'])['construction_date'] == '2223.11.21'
        and q.block(ash['1415'], 'ship_design_implementation') == q.block(bsh['1415'], 'ship_design_implementation')
        and combat(bfl['477']) == [825] and combat(bfl['825']) == [477]
        and q.scalars(q.block(bfl['477'], 'combat'))['start_date'] == '2268.03.12'
        and q.ids(q.block(afl['825'], 'ships')) == q.ids(q.block(bfl['825'], 'ships'))
        and len(aids) == 30 and not added_ships and not lost_ships
        and [q.scalars(ai[str(i)])['progress'] for i in aids] == [37.5, 37.5] + [0] * 28)
passed = all(checks.values())
details = {i: {'owned_by_player': i in ao, 'owned_by_country1': i in enemy_owned,
               'position': q.scalars(q.block(q.block(afl[str(i)], 'movement_manager'), 'coordinate')),
               'ships': q.ids(q.block(afl[str(i)], 'ships')), 'combat_with': combat(afl[str(i)]),
               'ship_states': {sid: q.scalars(ash[str(sid)]) for sid in q.ids(q.block(afl[str(i)], 'ships'))}}
           for i in set(ao) | {477, 825} if str(i) in afl and (i in am or i in {477, 825})}
proof = {'status': 'PASS_TERRAVORE_NATIVE_WAR1_COMBAT_COLONIZATION_OBSERVATION_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'], 'date': a['date'],
         'days': days, 'actual_owned_military': am, 'actual_new_paid_ships': added_ships,
         'actual_lost_military_requires_separate_combat_evidence': lost_ships, 'remaining_paid_orders': aids,
         'front_order_progress': [q.scalars(ai[str(i)])['progress'] for i in aids[:2]],
         'actual_fleet_details': details, 'actual_active_owned_combat': active, 'actual_pending': pending,
         'actual_mother_population': a['colonies']['0']['actual_pop_sum'], 'actual_colonization_population': colony['actual_pop_sum'],
         'actual_endpoint_nets': {k: str(v) for k, v in nets.items()}, 'actual_stockpiles': ac['effective_stockpile'],
         'actual_war1': q.scalars(war), 'calendar_ready': False, 'short_combat_calendar_ready': passed and not pending,
         'scope': 'Only bounded native war1/paid reinforcement/ongoing colonization observation. Remote capture is retained, no annual safety, victory, completed colonization, monthly ledger or full-route claim.'}
out = run / (after + '-war1-combat-colonization-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True],
                  'pending': pending, 'new_paid_ships': added_ships, 'remaining_orders': len(aids),
                  'short_combat_calendar_ready': proof['short_combat_calendar_ready']}), flush=True)
assert passed, 'Original war1 observation FAIL retained; no repeated calendar'
