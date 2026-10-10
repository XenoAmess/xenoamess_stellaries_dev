"""Read-only native Terravore eligibility plus an already captured Chinese refusal."""
import json, logging, re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, m = h.load_run()
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
stage = 'terravore-native-painkillers-month'
a = json.loads((run / (stage + '.audit.json')).read_text('utf-8'))
c = a['countries']['0']
boundary = json.loads((run / (stage + '-meditate-year-proof.json')).read_text('utf-8'))
month = json.loads((run / (stage + '-meditate-month-proof.json')).read_text('utf-8'))
gov = q.scalars(c['government'])
game = h.GAME_EXE.parent
paths = {
    'AP': game / 'common/ascension_perks/00_ascension_perks.txt',
    'triggers': game / 'common/scripted_triggers/00_scripted_triggers.txt',
    'technology': game / 'common/technology/00_soc_tech.txt',
    'rules': game / 'common/game_rules/00_rules.txt',
    'main_CN': game / 'localisation/simp_chinese/main_2_l_simp_chinese.yml',
    'traditions_CN': game / 'localisation/simp_chinese/traditions_l_simp_chinese.yml',
    'technology_CN': game / 'localisation/simp_chinese/technology_l_simp_chinese.yml',
}
src = {k: p.read_text('utf-8-sig') for k, p in paths.items()}
trigger = q.block(src['triggers'], 'is_lithoid_devouring_swarm')
ap = q.block(src['AP'], 'ap_hive_worlds')
tech = q.block(src['technology'], 'tech_terrestrial_sculpting')
weights = [q.scalars(v) for k, v, o in q.fields(q.block(tech, 'weight_modifier')) if k == 'modifier' and o]
rule = q.block(src['rules'], 'can_terraform_planet')
denial = [v for k, v, o in q.fields(rule) if k == 'custom_tooltip' and o and q.scalars(v).get('fail_text') == 'requires_actor_not_devouring_swarm_lithoid']
frame = json.loads((run / 'terravore-native-terraform-native-requirement-ui.ocr.json').read_text('utf-8'))
hover = json.loads((run / 'terravore-native-terraform-actual-button-hover.action.json').read_text('utf-8'))
labels = [v['text'] for v in frame['rows']]
official = {}
for filename, key in [('traditions_CN', 'ap_hive_worlds'), ('technology_CN', 'tech_terrestrial_sculpting'), ('technology_CN', 'tech_climate_restoration'), ('main_CN', 'requires_actor_not_devouring_swarm_lithoid')]:
    rows = [(n, s) for n, s in enumerate(src[filename].splitlines(), 1) if re.match(r'^\s*' + re.escape(key) + r':', s)]
    assert len(rows) == 1
    official[key] = {'line': rows[0][0], 'raw': rows[0][1], 'file': str(paths[filename])}
checks = {
    'original_saved_SHA': h.sha256(run / (stage + '.sav')) == a['save_sha256'] == 'e6ddc10d9494d1763df4fdc9b03776e5be1542ab542451c2b8e31875d3352e93',
    'bound_actual40_boundary_and17_month_PASS': len(boundary['checks']) == 40 and len(month['checks']) == 17 and boundary['status'].startswith('PASS') and month['status'].startswith('PASS') and all(boundary['checks'].values()) and all(month['checks'].values()) and boundary['after_sha256'] == month['after_sha256'] == a['save_sha256'],
    'bound_actual_guard_and_ledger_exit0': all(json.loads((run / (stage + suffix + '-execution.json')).read_text('utf-8'))['returncode'] == 0 for suffix in ['-guard', '-ledger']),
    'actual_native_lithoid_hive_founder66': c['native']['founder_species_ref'] == 66 and a['species']['66']['class'] == 'LITHOID' and all(t in a['species']['66']['traits'] for t in ['trait_lithoid', 'trait_hive_mind']) and gov['authority'] == 'auth_hive_mind',
    'actual_valid_civic_and_non_wilderness_origin': gov['origin'] == 'origin_heart_of_devouring' and '"civic_hive_devouring_swarm"' in [v for v, _, _ in q.tokens(q.block(c['government'], 'civics'))],
    'native_predicate_exact_lithoid_swarm_non_wilderness': q.scalars(trigger) == {'is_lithoid_empire': 'yes', 'has_valid_civic': 'civic_hive_devouring_swarm'} and q.scalars(q.block(trigger, 'NOT')) == {'has_origin': 'origin_wilderness'},
    'native_hive_world_AP_forbids_terravore': q.scalars(q.block(ap, 'potential')).get('is_lithoid_devouring_swarm') == 'no',
    'native_terraform_rule_independently_forbids_terravore': len(denial) == 1 and q.scalars(denial[0]).get('exists') == 'root' and q.scalars(q.block(denial[0], 'root')) == {'is_lithoid_devouring_swarm': 'no'},
    'native_terrestrial_sculpting_draw_weight_zero': {'factor': 0, 'is_lithoid_devouring_swarm': 'yes'} in weights,
    'native_terraform_tech_and_AP_not_granted': 'tech_terrestrial_sculpting' not in c['completed_technologies'] and 'tech_climate_restoration' not in c['completed_technologies'] and 'ap_hive_worlds' not in c['ascension_perks'],
    'actual_fresh_GPU_image_SHA': frame['image_sha256'] == h.sha256(run / 'terravore-native-terraform-native-requirement-ui.jpg') == '40528b0daf155ff5c079cae5e785c8e78bd0417ca7c55a17672092b17bfb7f4a' and frame['capture'] == 'fresh Steam F12 GPU backbuffer',
    'actual_CN_date_resolution_and_run_pid': m['language'] == 'l_simp_chinese' and frame['resolution'] == [1024, 768] and frame['pid'] == 23712 and a['date'] == '2248.06.02' and a['date'] in labels,
    'actual_CN_specific_terravore_refusal': '我们是石质噬杀蜂群！我们以星球为食！' in labels,
    'native_localization_key_matches_refusal': '$civic_hive_devouring_swarm$' in official['requires_actor_not_devouring_swarm_lithoid']['raw'] and '我们以星球为食' in official['requires_actor_not_devouring_swarm_lithoid']['raw'],
    'actual_hover_only_no_terraform_purchase': hover['action'] == 'scroll' and hover['clicks'] == hover['wheel_delta'] == 0 and hover['point'] == [876, 205],
}
p = {'status': 'PASS_NATIVE_TERRAVORE_TERRAFORM_REFUSAL_COMPONENT' if all(checks.values()) else 'FAIL', 'checks': checks, 'after_sha256': a['save_sha256'], 'date': a['date'], 'official_localization': official, 'native_sources': [{'path': str(v), 'sha256': h.sha256(v)} for v in paths.values()], 'image_sha256': frame['image_sha256'], 'scope': 'Native Terravore exclusion and already captured Chinese refusal, bound to a stable month. No transformation or full-route claim; not a calendar gate.'}
out = run / 'terravore-native-terraform-refusal-proof.json'
assert not out.exists()
h.write_json(out, p)
print(json.dumps(p, ensure_ascii=False), flush=True)
assert all(checks.values()), 'Original native terraforming refusal check FAIL retained'
