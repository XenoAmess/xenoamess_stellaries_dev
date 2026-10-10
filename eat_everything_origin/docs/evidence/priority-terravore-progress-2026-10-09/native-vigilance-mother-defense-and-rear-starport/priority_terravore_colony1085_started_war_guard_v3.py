"""Exact native colony completion and available-design companion; no mutations."""
import json, logging, re, shutil, sys, zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0] = ['eat_everything_origin/tools']
sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, metadata = h.load_run()
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
before, after = 'terravore-colony1085-travel-year2', 'terravore-colony1085-travel-year3'
def load(name):
    return json.loads((run / name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        fs = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage + '.audit.json'), fs, {k: v for k, v, o in fs if o}
b, bf, br = read(before)
a, af, ar = read(after)
original = load(after + '-colony-travel-observation-v2-proof.json')
execution = load(after + '-guard-v2-execution.json')
old_sha = '3f56579e3482eecd4d5965707d2181e2d3efa773dde8228cc1c9002a076ba11f'
failed = 'original8_military_ships_all_designs_full_health_held'
objs = lambda text: {k: v for k, v, o in q.fields(text) if o}
bsh, ash, afl = objs(br['ships']), objs(ar['ships']), objs(ar['fleet'])
bcr, acr = [q.block(top['country'], '0') for top in [br, ar]]
owned = lambda cr: re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(cr, 'fleets_manager'), 'owned_fleets'))
mil = {int(i): q.ids(q.block(afl[i], 'ships')) for i in owned(acr)
       if q.scalars(afl[i]).get('ship_class') == 'shipclass_military'}
ids = [1816, 1817, 33555519, 33556208, 33556207, 50332878, 1807, 1810]
old_design_b, old_design_a = [q.block(top['ship_design'], '167772797') for top in [br, ar]]
new_design = q.block(ar['ship_design'], '385877628')
techs = lambda cr: {v.strip('"') for k, v, o in q.fields(q.block(cr, 'tech_status')) if k == 'technology'}
target_b, target_a = [q.scalars(q.block(q.block(top['planets'], 'planet'), '1085')) for top in [br, ar]]
co = a['colonies']['37']
checks = {
    'original17_exact_one_FAIL_actual1_SHA_bound': original['status'] == 'FAIL'
        and len(original['checks']) == 17
        and {k for k, v in original['checks'].items() if v is not True} == {failed}
        and original['checks'][failed] is False
        and execution['returncode'] == 1 and execution['helper_sha256'] == old_sha
        and h.sha256(run / Path(execution['command'][1]).name) == old_sha,
    'all_other_original16_checks_true': all(v is True for k, v in original['checks'].items() if k != failed),
    'exact_actual_SHA_pair_dates_bound': b['date'] == '2267.03.17' and a['date'] == '2268.03.17'
        and b['save_sha256'] == original['before_sha256'] == h.sha256(run / (before + '.sav'))
        == '8057345cf3fedb36f503e2528796ef25443f0d2255f6560be024aebfc68960da'
        and a['save_sha256'] == original['after_sha256'] == h.sha256(run / (after + '.sav'))
        == '6ba484e42f0b59d141967acb373bd393cc2b2091f314b72528e3ec56da4552d1',
    'exact_original8_ship_fleet_relationships_held': mil == {
        788: [1816, 1817], 33555013: [33555519], 33555034: [33556208, 33556207, 50332878, 1807, 1810]},
    'all8_actual_design_growth_dates_full_HP_held_no_upgrade_progress': all(
        q.scalars(ash[str(i)])['hitpoints'] == q.scalars(ash[str(i)])['max_hitpoints'] == 270
        and q.scalars(ash[str(i)])['upgrade_progress'] == 0
        and q.scalars(bsh[str(i)])['construction_date'] == q.scalars(ash[str(i)])['construction_date']
        and q.scalars(bsh[str(i)])['fleet'] == q.scalars(ash[str(i)])['fleet']
        and q.scalars(q.block(bsh[str(i)], 'ship_design_implementation'))
            == {'design': 167772797, 'upgrade': 4294967295, 'growth_stage': 0}
        and q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))
            == {'design': 167772797, 'upgrade': 385877628, 'growth_stage': 0}
        for i in ids),
    'original_actual_design_raw_held_new_design_only_FLAK2': bool(old_design_b)
        and old_design_b == old_design_a and old_design_a.count('FLAK_BATTERY_1') == 1
        and new_design == old_design_a.replace('FLAK_BATTERY_1', 'FLAK_BATTERY_2')
        and 385877628 in q.ids(q.block(q.block(acr, 'ship_design_collection'), 'ship_design')),
    'original_queued_flak2_completed_no_tech_loss': techs(bcr) <= techs(acr)
        and techs(acr) - techs(bcr) == {'tech_flak_batteries_2'}
        and 'technology="tech_flak_batteries_2"' in q.block(q.block(bcr, 'tech_status'), 'engineering_queue'),
    'original_paid_colonizer_consumed_native_target1085_colony37': '33556279' in bsh
        and '33556279' not in ash and '16777955' in owned(bcr) and '16777955' not in owned(acr)
        and 'colony' not in target_b and 'owner' not in target_b
        and target_a['owner'] == target_a['controller'] == 0 and target_a['colony'] == 37
        and target_a['planet_class'] == target_b['planet_class'] == 'pc_alpine'
        and target_a['planet_size'] == target_b['planet_size'] == 12
        and target_a['colonize_date'] == '2267.10.12'
        and co['colonizing_species'] == 73 and co['actual_pop_sum'] == 18
        and a['countries']['0']['owned_colonies'] == [0, 37]
        and all(a['pop_groups'][str(i)]['key']['species'] == 73 for i in co['pop_groups']),
    'no_pending_exact_remote_combat_observed': not original['actual_pending']
        and original['actual_active_combat_fleets'] == [477]
        and not [v for k, v, o in af if k == 'player_event' and o and q.scalars(v).get('country') == 0],
    'original_unfiltered2670_errors_exact_held':
        (run / (before + '-error-after.log')).read_bytes()
        == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and (run / (after + '-error-after.log')).stat().st_size == 2670,
}
failed_execution = load(after + '-established-guard-execution.json')
checks['original_private_KeyError_actual1_SHA_retained'] = (failed_execution['returncode'] == 1
    and failed_execution['helper_sha256'] == '403fc551d89e7051c5c6c8d1d7d119eaea8ec79c3b3a6ea0398f57af4bdbeda8'
    and h.sha256(run / Path(failed_execution['command'][1]).name) == failed_execution['helper_sha256']
    and (run / (after + '-established-guard-stdout.txt')).read_bytes() == b''
    and "KeyError: 'species'" in (run / (after + '-established-guard-stderr.txt')).read_text('utf-8'))
checks['native_colonization_growth_and_Chinese_UI_bound'] = (
    'GROWTH_CAT_COLONIZATION' in q.block(ar['pop_groups'], '335544348')
    and 'value=4' in q.block(q.block(ar['pop_groups'], '335544348'), 'last_month_growth_details')
    and any('\u6b63\u5728\u6b96\u6c11\u884c\u661f' in x['text']
        for x in load('terravore-colony1085-progress-hover-visible.ocr.json')['rows']))
v2 = load(after + '-colony1085-started-v2-proof.json')
v2execution = load(after + '-started-guard-v2-execution.json')
checks['original_V2_12_exact_combat_FAIL_actual1_SHA_bound'] = (v2['status'] == 'FAIL'
    and len(v2['checks']) == 12
    and {k for k,v in v2['checks'].items() if v is not True} == {'no_pending_no_active_owned_combat'}
    and v2execution['returncode'] == 1
    and v2execution['helper_sha256'] == 'a32dff727695f92316167ba077d953d3882efc98dd82ced1b41ee6d2d391c95d'
    and h.sha256(run / Path(v2execution['command'][1]).name) == v2execution['helper_sha256']
    and v2['before_sha256'] == b['save_sha256'] and v2['after_sha256'] == a['save_sha256'])
war = q.block(ar['war'],'1')
checks['native_war1_exact_participants_objectives_start_bound'] = (
    re.findall(r'\bcountry\s*=\s*(\d+)',q.block(war,'attackers')) == ['1']
    and re.findall(r'\bcountry\s*=\s*(\d+)',q.block(war,'defenders')) == ['0']
    and q.scalars(war)['start_date'] == '2265.12.30'
    and q.scalars(q.block(war,'attacker_war_goal'))['type'] == 'wg_end_threat_swarm'
    and q.scalars(q.block(war,'defender_war_goal'))['type'] == 'wg_absorption')
checks['exact_145_fleets477_825_mutual_combat_and_ownership'] = (
    '477' in owned(acr) and '825' in owned(q.block(ar['country'],'1'))
    and all(q.scalars(q.block(q.block(afl[str(i)],'movement_manager'),'coordinate'))['origin'] == 145 for i in [477,825])
    and re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(afl['477'],'combat'),'in_combat_with')) == ['825']
    and re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(afl['825'],'combat'),'in_combat_with')) == ['477']
    and all(q.scalars(q.block(afl[str(i)],'combat'))['start_date'] == '2268.03.12' for i in [477,825]))
checks['actual_base1415_H6250_shield513_armor2923_enemy16_ships'] = (
    q.ids(q.block(afl['477'],'ships')) == [1415]
    and q.scalars(ash['1415'])['hitpoints'] == q.scalars(ash['1415'])['max_hitpoints'] == 6250
    and q.scalars(ash['1415'])['shield_hitpoints'] == 513.59366
    and q.scalars(ash['1415'])['armor_hitpoints'] == 2923.30979
    and len(q.ids(q.block(afl['825'],'ships'))) == 16
    and all(str(i) in ash for i in q.ids(q.block(afl['825'],'ships')))
    and q.scalars(afl['825'])['military_power'] == 3288.90625)
passed = all(checks.values())
proof = {'status': 'PASS_TERRAVORE_NATIVE_COLONIZATION_AND_REMOTE_WAR_OBSERVATION_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'],
         'original_fail_proof': after + '-colony-travel-observation-v2-proof.json',
         'actual_target': target_a, 'actual_colony_population': co['actual_pop_sum'],
         'actual_mother_population': a['colonies']['0']['actual_pop_sum'],
         'available_upgrade_design': 385877628, 'actual_design_still': 167772797,
         'calendar_ready': False, 'normal_UI_defense_preparation_ready': passed,
         'actual_remote_combat': {'own_fleet':477,'enemy_fleet':825,'system':145,'war':1},
         'colony_UI_sha256': h.sha256(run / 'terravore-colony1085-progress-hover-visible.jpg'),
         'scope': 'Paid native colonization still incomplete, remote war1 combat active, annual calendar blocked; exact available upgrade pointer only. Original FAIL retained. No free actual upgrade, swallow, menace gain or route-completion claim.'}
out = run / (after + '-colonization-started-war-observation-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks),
                  'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Original colony completion companion FAIL retained'
