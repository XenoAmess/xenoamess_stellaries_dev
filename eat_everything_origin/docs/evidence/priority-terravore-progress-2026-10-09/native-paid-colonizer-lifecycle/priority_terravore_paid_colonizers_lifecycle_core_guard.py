"""Documented paid native colonizer lifecycle and scoped Mod core; no unpaid births."""
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

before, after = sys.argv[1:]
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r
import audit_save as q

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf8'))
omit = lambda raw, keys: [(k, v, z) for k, v, z in q.fields(raw) if k not in keys]
obs = load(after + '-construction-boundary-observation.json')
oe = load(after + '-boundary-observation-execution.json')
iv = load(after + '-rear97-native-inventory-v4.json')
ie = load(after + '-rear97-native-inventory-v4-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
bc, ac = ba['countries']['0'], aa['countries']['0']
bcr, acr = b['country0_raw'], a['country0_raw']
eb, ea = iv[before], iv[after]
cal = load(after + '-calendar-receipt.json')
ce = load(after + '-calendar-execution.json')
pre = load(cal['prior_proof_file'])
pe = load(cal['prior_execution_stage'] + '-execution.json')
calibration = after == 'terravore-mother-colonizer3-first-research-day'

def ordinal(s):
    y, m, d = map(int, s.split('.'))
    return y * 360 + (m - 1) * 30 + d - 1

ob, oa = ordinal(ba['date']), ordinal(aa['date'])
days = oa - ob
mt = sum(i % 30 == 0 for i in range(ob + 1, oa + 1))
rt = sum(i % 30 == 1 for i in range(ob + 1, oa + 1))
keys = ['energy', 'minerals', 'food', 'consumer_goods', 'alloys', 'unity', 'trade', 'influence']
net = {k: sum((D(str(v.get(k, 0))) for v in ac['budget_categories']['current_month']['balance'].values()), D(0)) for k in keys}
stocks = set(bc['effective_stockpile']) | set(ac['effective_stockpile'])
delta = {k: D(str(ac['effective_stockpile'].get(k, 0))) - D(str(bc['effective_stockpile'].get(k, 0))) for k in stocks}
science = {k: sum((D(str(v.get(k, 0))) for v in ac['budget_categories']['current_month']['income'].values()), D(0)) for k in q.RESEARCH_RESOURCES}
bank_delta = {k: D(str(ac['research_stockpile'].get(k, 0))) - D(str(bc['research_stockpile'].get(k, 0))) for k in q.RESEARCH_RESOURCES}

def research_queue(t, key):
    raw = q.block(t, key)
    ts = list(q.tokens(raw))
    if not ts:
        return {}
    assert ts[0][0] == '{' and ts[-1][0] == '}'
    return q.scalars(raw[ts[0][2]:ts[-1][1]])

bt, at = bc['tech_status'], ac['tech_status']
beng, aeng = [research_queue(t, 'engineering_queue') for t in [bt, at]]
cb, ca = ba['colonies']['0'], aa['colonies']['0']
mb, ma = ba['planets']['7'], aa['planets']['7']
new_growth = ca['actual_pop_sum'] - cb['actual_pop_sum']
gr = q.block(a['colony_raw']['0'], 'last_month_growth_data')
growth = q.scalars(q.block(gr, 'growth_and_size'))
growth_details = [(k, q.unquote(v), z) for k, v, z in q.fields(q.block(gr, 'current_month_growth_details'))]

def population_ok():
    if not mt:
        return new_growth == 0
    return (new_growth >= 0 and growth == {'month_start_size': cb['actual_pop_sum'], 'growth': new_growth}
            and growth_details == [('key', 'GROWTH_CAT_GROWTH', False), ('value', new_growth, False), ('key', 'GROWTH_CAT_PROMOTION', False), ('value', 0, False)])

def jobs_ok():
    bj, aj = ba['pop_jobs'], aa['pop_jobs']
    return bj.keys() == aj.keys() and all(
        {k: v for k, v in j.items() if k not in {'workforce', 'bonus_workforce'}} == {k: v for k, v in aj[i].items() if k not in {'workforce', 'bonus_workforce'}}
        and all(aj[i][k] >= 0 or aj[i][k] == j[k] == -1 for k in ['workforce', 'bonus_workforce']) for i, j in bj.items())

def own_structure(st):
    au = st['audit']
    districts = au['colonies']['0']['districts']
    zones = {i for d in districts for i in au['districts'][str(d)]['zones'] if i != 4294967295}
    buildings = {i for z in zones for i in q.ids(q.block(q.block(st['raw_roots']['zones'], str(z)), 'buildings'))}
    ids = {'districts': districts, 'zones': sorted(zones), 'buildings': sorted(buildings), 'deposit': au['planets']['7']['deposits']}
    return {root: {str(i): q.block(st['raw_roots'][root], str(i)) for i in entries} for root, entries in ids.items()}

def owned_queues(st):
    return {k: v for k, v, z in q.fields(q.block(q.block(st['raw_roots']['construction'], 'queue_mgr'), 'queues')) if z and q.scalars(v).get('owner') == 0}

def item(st, order='100663340'):
    return q.block(q.block(q.block(st['raw_roots']['construction'], 'item_mgr'), 'items'), order)

def military(st):
    return {i for f in st['owned_fleets_raw'].values() if q.scalars(f).get('ship_class') == 'shipclass_military' for i in q.ids(q.block(f, 'ships'))}

def alive(st):
    return {i for i in military(st) if q.scalars(st['owned_ships_raw'][str(i)]).get('killed') != 'yes' and q.scalars(st['owned_ships_raw'][str(i)]).get('hitpoints', 0) > 0}

def health_valid(raw):
    v = q.scalars(raw)
    return v.get('killed') == 'yes' or all(-0.001 <= v.get(k, 0) <= v.get(cap, 0) + 0.001 for k, cap in [('hitpoints', 'max_hitpoints'), ('armor_hitpoints', 'max_armor_hitpoints'), ('shield_hitpoints', 'max_shield_hitpoints')])

home = {i for fid in ['83886903', '33555259', '67109603'] for i in q.ids(q.block(b['owned_fleets_raw'].get(fid, ''), 'ships'))}
station = q.scalars(a['owned_ships_raw'].get('67109591', ''))
cf = a['owned_fleets_raw'].get('33555278', '')
colraw = a['owned_ships_raw'].get('50333369', '')
col = q.scalars(colraw)
old_designs, new_designs = [q.block(c, 'ship_design_collection') for c in [bcr, acr]]
old_notifications = {q.scalars(v).get('notification') for v in b['messages_country0_raw']}
new_messages = [v for v in a['messages_country0_raw'] if q.scalars(v).get('notification') not in old_notifications]
new_mod_messages = [v for v in new_messages if 'eep_' in v or 'TERRAVORE_CONSUME' in v]
boundaries = []
if b['pending_country0_raw'] != a['pending_country0_raw']:
    boundaries.append('new_or_changed_pending_event')
if new_mod_messages:
    boundaries.append('new_Mod_or_native_consumption_message')
if ac['effective_stockpile']['menace'] >= 1000:
    boundaries.append('native_crisis_level2_Menace_threshold')

known_prior = {'8679416504ec89347ed3e6f870679afd7854a4deb2461e87d7f310179caccd10', h.sha256(Path(__file__))}
prior_source = run / Path(pe['command'][1]).name
reviewed = load('terravore-mother-colonizer3-first-research-day-mia-build-first-research-v3-proof.json')
reviewed_ex = load('terravore-mother-colonizer3-first-research-day-mia-build-guard-v3-execution.json')

# Immutable order identities backed by the original paid receipts.
orders = {'100663340': ('3', 0, 0), '50331690': ('2287', 153, 97)}
paid_births = dict(pre.get('paid_births', {}))
new_births = {}
remaining_work = {}
lifecycle_reasons = []

def ship_identity_ok(st, identity):
    sid, fid = str(identity['ship_id']), str(identity['fleet_id'])
    raw = st['owned_ships_raw'].get(sid, '')
    fleet = st['owned_fleets_raw'].get(fid, '')
    sc = q.scalars(raw)
    return (int(sid) in st['owned_ship_ids'] and int(fid) in st['owned_fleets']
            and sc.get('fleet') == int(fid) and sc.get('hitpoints', 0) > 0 and sc.get('killed') != 'yes'
            and q.ids(q.block(fleet, 'ships')) == [int(sid)]
            and q.scalars(q.block(raw, 'ship_design_implementation')) == {'design': 150995039, 'upgrade': 4294967295, 'growth_stage': 0}
            and q.scalars(q.block(raw, 'colonization_data')) == {'species': 73}
            and q.scalars(fleet).get('ship_class') == 'shipclass_colonizer'
            and q.scalars(q.block(fleet, 'properties')).get('mia') != 'yes'
            and q.scalars(q.block(raw, 'coordinate')).get('origin') == identity['system_id']
            and q.scalars(q.block(q.block(fleet, 'movement_manager'), 'coordinate')).get('origin') == identity['system_id']
            and not q.block(fleet, 'current_order') and not q.ids(q.block(q.block(fleet, 'combat'), 'in_combat_with')))

def lifecycle_ok():
    bq, aq = owned_queues(b), owned_queues(a)
    if len(bq) != 12 or bq.keys() != aq.keys():
        lifecycle_reasons.append('owned_queue_registry_changed'); return False
    bentries = {k: (v, z) for k, v, z in q.fields(q.block(q.block(b['raw_roots']['construction'], 'item_mgr'), 'items'))}
    aentries = {k: (v, z) for k, v, z in q.fields(q.block(q.block(a['raw_roots']['construction'], 'item_mgr'), 'items'))}
    added = set(a['owned_ship_ids']) - set(b['owned_ship_ids'])
    assigned = set()
    for oid, (queue, base, system) in orders.items():
        if omit(bq[queue], {'items'}) != omit(aq[queue], {'items'}):
            lifecycle_reasons.append('queue_metadata_changed_' + oid); return False
        if oid in paid_births:
            identity = paid_births[oid]
            if (identity['base_id'] != base or identity['system_id'] != system
                    or not ship_identity_ok(b, identity) or not ship_identity_ok(a, identity)
                    or q.ids(q.block(bq[queue], 'items')) or q.ids(q.block(aq[queue], 'items'))
                    or bentries.get(oid) != ('none', False) or aentries.get(oid) != ('none', False)):
                lifecycle_reasons.append('retained_paid_birth_identity_changed_' + oid); return False
            continue
        bi = item(b, oid); bv = q.scalars(bi)
        if (q.ids(q.block(bq[queue], 'items')) != [int(oid)] or bv.get('progress_needed') != 360
                or q.scalars(q.block(bi, 'resources')) != {'minerals': 375, 'alloys': 150}
                or q.scalars(q.block(q.block(bi, 'buildable_colony_ship'), 'orbitable')) != {'starbase': base}
                or q.scalars(q.block(q.block(bi, 'buildable_colony_ship'), 'colonization_data')) != {'species': 73}):
            lifecycle_reasons.append('original_paid_order_invalid_' + oid); return False
        expected = D(str(bv['progress'])) + D('1.33') * days
        if expected < 360:
            ai = item(a, oid)
            if (q.ids(q.block(aq[queue], 'items')) != [int(oid)] or omit(bi, {'progress'}) != omit(ai, {'progress'})
                    or D(str(q.scalars(ai).get('progress', -1))) != expected):
                lifecycle_reasons.append('unfinished_paid_order_invalid_' + oid); return False
            remaining_work[oid] = str(expected)
            continue
        if not (days == 1 and D(str(bv['progress'])) == D('359.1') and not q.ids(q.block(aq[queue], 'items'))
                and aentries.get(oid) == ('none', False)):
            lifecycle_reasons.append('birth_not_unique_precompletion_day_' + oid); return False
        candidates = []
        for sid in sorted(added - assigned):
            raw = a['owned_ships_raw'][str(sid)]; sc = q.scalars(raw)
            fid = sc.get('fleet'); fleet = a['owned_fleets_raw'].get(str(fid), '')
            identity = {'ship_id': sid, 'fleet_id': fid, 'base_id': base, 'system_id': system, 'birth_date': aa['date']}
            if (fid not in b['owned_fleets'] and ship_identity_ok(a, identity)
                    and list(q.fields(q.block(raw, 'ship_design_implementation'))) == list(q.fields(q.block(q.block(bi, 'buildable_colony_ship'), 'ship_design_implementation')))
                    and all(sc.get(k) == sc.get(cap) == value for k, cap, value in [('hitpoints','max_hitpoints',625),('armor_hitpoints','max_armor_hitpoints',125),('shield_hitpoints','max_shield_hitpoints',320)])
                    and sc.get('construction_date') == aa['date']
                    and q.scalars(fleet).get('fleet_stance') == 'evasive'
                    and q.scalars(q.block(q.block(q.block(fleet, 'movement_manager'), 'orbit'), 'orbitable')) == {'starbase': base}):
                candidates.append(identity)
        if len(candidates) != 1:
            lifecycle_reasons.append('paid_birth_count_or_identity_invalid_' + oid); return False
        identity = candidates[0]; assigned.add(identity['ship_id']); paid_births[oid] = identity; new_births[oid] = identity
    if added != assigned:
        lifecycle_reasons.append('unpaid_new_owned_ship'); return False
    allowed_queues = {v[0] for v in orders.values()}
    if any(bq[k] != aq[k] or q.ids(q.block(aq[k], 'items')) for k in bq if k not in allowed_queues):
        lifecycle_reasons.append('other_owned_queue_changed'); return False
    return True

lifecycle_valid = lifecycle_ok()

checks = {
    'original_rear19_payment_PASS_actual0_source_original_SHA': load('terravore-rear-colonizer4-paid-rear-colonizer4-payment-v2-proof.json')['status']=='PASS_TERRAVORE_NATIVE_REAR_COLONIZER4_PAYMENT_COMPONENT' and len(load('terravore-rear-colonizer4-paid-rear-colonizer4-payment-v2-proof.json')['checks'])==19 and all(v is True for v in load('terravore-rear-colonizer4-paid-rear-colonizer4-payment-v2-proof.json')['checks'].values()) and load('terravore-rear-colonizer4-paid-payment-guard-v2-execution.json')['returncode']==0 and load('terravore-rear-colonizer4-paid-payment-guard-v2-execution.json')['helper_sha256']==h.sha256(run/'priority_terravore_rear_colonizer4_payment_guard_v2.py')=='c518ac30d9953b3c1652faf104fe6e406aab0bb2d86d6790c2d74e24bed9f2e7' and load('terravore-rear-colonizer4-paid-rear-colonizer4-payment-v2-proof.json')['after_sha256']==h.sha256(run/'terravore-rear-colonizer4-paid.sav')=='317ba823fd8420e760d7d9d3f4bc8ebc028d30e545ad97b5fbd73ffac51de086',

    'actual_complete_observation6_source': len(obs['checks']) == 6 and all(v is True for v in obs['checks'].values()) and oe['returncode'] == 0 and oe['helper_sha256'] == h.sha256(run / 'priority_terravore_construction_boundary_observation.py') == 'e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678',
    'actual_native_inventory4_source': len(iv['checks']) == 4 and all(v is True for v in iv['checks'].values()) and ie['returncode'] == 0 and ie['helper_sha256'] == h.sha256(run / 'priority_terravore_rear97_native_inventory_v4.py') == 'e6e8ca9f31893549b6990f5ae2db24df49b212da6fdf864b91b585c86a6d4b20',
    'prior_PASS_actual0_original_source_SHA': pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values()) and pe['returncode'] == 0 and pe['helper_sha256'] == h.sha256(prior_source) and pe['helper_sha256'] in known_prior and pre['after_sha256'] == obs['before_sha256'],
    'original_first_research34_reviewed_actual0_held': reviewed['status'] == 'PASS_NATIVE_TERRAVORE_REVIEWED_FIRST_RESEARCH_COMPONENT' and len(reviewed['checks']) == 34 and all(v is True for v in reviewed['checks'].values()) and reviewed_ex['returncode'] == 0 and reviewed_ex['helper_sha256'] == h.sha256(run / 'priority_terravore_mia_mother_first_research_guard_v3.py') == '5ae6411742bf5b314b0ffe181105feebc8b5698a2353c3e87e3e47eb4dbca9a7' and (not calibration or reviewed['after_sha256'] == obs['after_sha256']),
    'checked_native_calendar_actual0_source_and_bounded_month': cal['status'] == 'CALENDAR_CONFIRMED' and ce['returncode'] == 0 and ce['helper_sha256'] == h.sha256(run / 'formal_production_native_calendar_checked_v2.py') == '66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and cal['days'] == days and 1 <= days <= 30 and 0 <= mt <= 1 and 0 <= rt <= 1 and ordinal('2272.10.01') <= ob < oa < ordinal('2273.09.01'),
    'original_SAV_SHA_pair': all(st['audit']['save_sha256'] == h.sha256(run / (name + '.sav')) == inv['save_sha256'] for st, name, inv in [(b, before, eb), (a, after, ea)]),
    'production41_same_tree_Chinese': meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41 and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
    'unfiltered_original_error_held': (run / (before + '-error-after.log')).read_bytes() == (run / (after + '-error-before.log')).read_bytes() == (run / (after + '-error-after.log')).read_bytes() and h.sha256(run / (after + '-error-after.log')) == 'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
    'EEP_core_variables_and_one_colony_species73_only': bc['variables'] == ac['variables'] and all(ac['variables'][k] == v for k, v in {'eep_c': 49, 'eep_d': 14, 'eep_worlds': 3, 'eep_psi': 1, 'eep_stage': 1, 'eep_fleet_stage': 0}.items()) and bc['owned_colonies'] == ac['owned_colonies'] == [0] and a['species_population_by_colony'] == {'0:73': ca['actual_pop_sum']} and ba['species'].get('73') == aa['species'].get('73'),
    'mother18_plus_D14_capacity32_and_paid_27_original_structure': all(mb[k] == ma[k] for k in ['owner', 'controller', 'colony', 'planet_size', 'modifiers', 'deposits']) and ma['owner'] == ma['controller'] == ma['colony'] == 0 and ma['planet_size'] == 18 and 'eep_core' in ma['flags'] and own_structure(b) == own_structure(a) and sum(aa['districts'][str(i)]['level'] for i in ca['districts']) == 27 and jobs_ok(),
    'budget_true_resources_only_native_month_net': all(abs(delta.get(k, D(0)) - net[k] * mt) <= D('0.00005') for k in keys if k not in {'trade', 'influence'}) and all(delta[k] == 0 for k in stocks - set(keys) - set(q.RESEARCH_RESOURCES) - {'menace'}) and all(bc['effective_stockpile'][k] == ac['effective_stockpile'][k] == cap for k, cap in [('trade', 50000), ('influence', 1000)]),
    'native_budget_roll_or_held_between_months': ac['budget_categories']['last_month'] == bc['budget_categories']['current_month'] if mt else bc['budget_categories'] == ac['budget_categories'],
    'positive_native_mother_economy': all(net[k] > 0 for k in ['energy', 'minerals', 'alloys', 'unity']),
    'true_P_S_bank_only_native_research_tick_Eng_bank0': all(abs(bank_delta[k] - science[k] * D('1.33') * rt) <= D('0.00005') for k in ['physics_research', 'society_research']) and bc['research_stockpile']['engineering_research'] == ac['research_stockpile']['engineering_research'] == 0,
    'only_original_mass_drivers3_native_progress': omit(bt, {'stored_techpoints', 'engineering_queue'}) == omit(at, {'stored_techpoints', 'engineering_queue'}) and {k: v for k, v in beng.items() if k != 'progress'} == {k: v for k, v in aeng.items() if k != 'progress'} and beng['technology'] == aeng['technology'] == 'tech_mass_drivers_3' and abs(D(str(aeng['progress'])) - D(str(beng['progress'])) - science['engineering_research'] * D('1.33') * rt) <= D('0.00005'),
    'native_population_growth_no_repeat_mod_return': population_ok(),
    'housing_native_cache_and_no_uninhabitable_colonists': ca['total_housing'] == 14100 and ca['free_housing'] == 14100 - ca['housing_usage'] and 0 <= ca['actual_pop_sum'] - ca['housing_usage'] <= max(new_growth, cb['actual_pop_sum'] - cb['housing_usage']) and ca['housing_usage'] >= cb['housing_usage'] and ca['actual_pop_sum'] == ca['employable_pops'] == ca['num_sapient_pops'] and ca['free_amenities'] > 0 and ca['crime'] == 0 and b['colony_raw']['37'] == a['colony_raw']['37'],
    'two_original_paid_orders_native_lifecycle_no_unpaid_birth': lifecycle_valid,
    'original_own_design_registry_and_retained_ship_designs': old_designs == new_designs and all(q.block(b['raw_roots']['ship_design'], str(i)) == q.block(a['raw_roots']['ship_design'], str(i)) for i in q.ids(q.block(old_designs, 'ship_design'))) and all(q.block(v, 'ship_design_implementation') == q.block(b['owned_ships_raw'][i], 'ship_design_implementation') for i, v in a['owned_ships_raw'].items() if i in b['owned_ships_raw']),
    'mother20_alive_designs_health_and_home_fleets_held': len(home) == 20 and home <= alive(a) and all(q.ids(q.block(b['owned_fleets_raw'][fid], 'ships')) == q.ids(q.block(a['owned_fleets_raw'].get(fid, ''), 'ships')) for fid in ['83886903', '33555259', '67109603']) and all(all(q.scalars(a['owned_ships_raw'][str(i)]).get(k, 0) >= q.scalars(b['owned_ships_raw'][str(i)]).get(k, 0) for k in ['hitpoints', 'armor_hitpoints', 'shield_hitpoints']) for i in home),
    'retained_owned_native_ship_health_within_design_caps': all(health_valid(v) for v in a['owned_ships_raw'].values()),
    'rear_base153_still_owned_original_station': eb['rear153_raw'] == ea['rear153_raw'] and station.get('fleet') == 804 and q.ids(q.block(a['owned_fleets_raw'].get('804', ''), 'ships')) == [67109591] and station.get('hitpoints', 0) > 6000,
    'original_MIA_colonizer_identity_species_return_no_revival': col.get('fleet') == 33555278 and q.ids(q.block(cf, 'ships')) == [50333369] and q.scalars(q.block(colraw, 'colonization_data')) == {'species': 73} and q.scalars(cf).get('mia_type') == 'mia_emergency_ftl' and q.scalars(cf).get('return_date') == '2275.08.02' and q.scalars(q.block(cf, 'properties')).get('mia') == 'yes' and b['planet_raw']['523'] == a['planet_raw']['523'] and 16779140 not in a['owned_ship_ids'] and 16778062 not in a['owned_fleets'],
    'original_government_AP_traditions_armies_crisis1_held': all(bc[k] == ac[k] for k in ['government', 'traditions', 'ascension_perks']) and q.ids(q.block(bcr, 'owned_armies')) == q.ids(q.block(acr, 'owned_armies')) and len(q.ids(q.block(acr, 'owned_armies'))) == 12 and q.block(bcr, 'crisis_progression') == q.block(acr, 'crisis_progression') and ac['effective_stockpile']['menace'] >= bc['effective_stockpile']['menace'],
}
passed = all(v is True for v in checks.values())
work = D(str(q.scalars(item(a)).get('progress', 360)))
rear_work = D(str(q.scalars(item(a,'50331690')).get('progress',360)))
max_days = min([30] + [max(0, int((D(360) - D(v) - D('0.00001')) // D('1.33'))) for v in remaining_work.values()]) if remaining_work else 0
delayed_days = [q.scalars(v)['days'] for k, v, z in q.fields(q.block(q.block(acr, 'modules'), 'standard_event_module')) if k == 'delayed_event' and z and 'days' in q.scalars(v)]
if delayed_days:
    max_days = min(max_days, max(0, min(delayed_days) - 1))
ready = passed and not boundaries and max_days > 0
proof = {
    'status': 'PASS_NATIVE_TERRAVORE_PAID_COLONIZER_LIFECYCLE_CORE_COMPONENT' if passed and not boundaries else ('OBSERVED_NATIVE_TERRAVORE_MONTHLY_BUILD_BOUNDARY' if passed else 'FAIL'),
    'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'], 'date': aa['date'], 'days': days,
    'boundaries': boundaries, 'monthly_build_calendar_ready': ready, 'maximum_days_to_monthly_build_boundary': max_days if ready else 0,
    'actual_net': {k: str(v) for k, v in net.items()}, 'actual_stock_delta': {k: str(v) for k, v in delta.items()}, 'actual_research_bank_delta': {k: str(v) for k, v in bank_delta.items()},
    'actual_population': ca['actual_pop_sum'], 'native_growth': new_growth, 'native_growth_record': growth, 'housing_cache_lag': ca['actual_pop_sum'] - ca['housing_usage'],
    'actual_colonizer_work': str(work), 'actual_rear_colonizer_work': str(rear_work), 'paid_births': paid_births, 'new_paid_births': new_births, 'remaining_order_work': remaining_work, 'lifecycle_reasons': lifecycle_reasons, 'native_delayed_event_days': delayed_days,
    'alive_military_ship_ids': sorted(alive(a)), 'native_new_lost_military': sorted(alive(b) - alive(a)),
    'enemy825_ids_before': eb['enemy825_ship_ids'], 'enemy825_ids_after': ea['enemy825_ship_ids'], 'native_war_history_changed': b['war1_battles_raw'] != a['war1_battles_raw'],
    'new_country0_messages_raw': new_messages, 'rear_station_health': {k: station.get(k, 0) for k in ['hitpoints', 'armor_hitpoints', 'shield_hitpoints']},
    'scope': 'Mod core and original paid colonizer lifecycle only; native combat facts retained; no colony, fourth consumption or full acceptance claim.'}
out = run / (after + '-paid-colonizer-lifecycle-core-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({k: proof[k] for k in ['status', 'date', 'actual_population', 'actual_colonizer_work', 'actual_rear_colonizer_work', 'maximum_days_to_monthly_build_boundary', 'boundaries', 'native_new_lost_military', 'rear_station_health', 'new_paid_births', 'lifecycle_reasons']} | {'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True]}, ensure_ascii=True), flush=True)
assert passed
