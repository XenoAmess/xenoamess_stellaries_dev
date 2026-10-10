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
        and all(a['pop_groups'][str(i)]['species'] == 73 for i in co['pop_groups']),
    'no_pending_no_active_owned_combat': not original['actual_pending']
        and not original['actual_active_combat_fleets']
        and not [v for k, v, o in af if k == 'player_event' and o and q.scalars(v).get('country') == 0],
    'original_unfiltered2670_errors_exact_held':
        (run / (before + '-error-after.log')).read_bytes()
        == (run / (after + '-error-before.log')).read_bytes()
        == (run / (after + '-error-after.log')).read_bytes()
        and (run / (after + '-error-after.log')).stat().st_size == 2670,
}
passed = all(checks.values())
proof = {'status': 'PASS_TERRAVORE_NATIVE_COLONY1085_ESTABLISHED_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'],
         'original_fail_proof': after + '-colony-travel-observation-v2-proof.json',
         'actual_target': target_a, 'actual_colony_population': co['actual_pop_sum'],
         'actual_mother_population': a['colonies']['0']['actual_pop_sum'],
         'available_upgrade_design': 385877628, 'actual_design_still': 167772797,
         'calendar_ready': passed,
         'scope': 'Paid native colony founded, actual original military unchanged; exact available upgrade pointer only. Original FAIL retained. No free actual upgrade, swallow, menace gain or route-completion claim.'}
out = run / (after + '-colony1085-established-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks),
                  'failed': [k for k, v in checks.items() if v is not True]}), flush=True)
assert passed, 'Original colony completion companion FAIL retained'
