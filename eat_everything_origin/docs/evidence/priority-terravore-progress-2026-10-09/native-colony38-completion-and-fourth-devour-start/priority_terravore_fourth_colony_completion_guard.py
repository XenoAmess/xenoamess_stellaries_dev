"""Exact documented native colony38 completion; original waiting failure retained."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path(__file__).parent
before, after = sys.argv[1:]
assert before == 'terravore-colonization-near-completion-wait-02'
assert after == 'terravore-colony38-native-completion-date'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda name: json.loads((run / name).read_text('utf-8-sig'))
old = load(after + '-target523-colonization-wait-v6-proof.json')
oe = load(after + '-colonization-wait-guard-v6-execution.json')
obs = load(after + '-construction-boundary-observation.json')
be = load(after + '-boundary-observation-execution.json')
b, a = obs['before_state'], obs['after_state']
failed = 'actual_target523_owned_colony38_native_founding'
expected_before = 'cd6ed6cf0a39d2b79be1b475543f2904db989282060b5ddacacef6934a44df68'
expected_after = 'ed8e4bee8bf6924ea713b0ac5338c2528e913d74822f72735b7fe88f1bec92d0'
checks = {k: v for k, v in old['checks'].items() if k != failed}
checks['original25_exact_one_phase_FAIL_actual1_source_and_SAVs_bound'] = (
    len(old['checks']) == 25 and {k for k, v in old['checks'].items() if v is not True} == {failed}
    and old['status'] == 'FAIL' and oe['returncode'] == 1
    and oe['helper_sha256'] == sha(run / 'priority_terravore_fourth_colonization_wait_guard_v6.py')
    == '012b72c3d3981840c21bcea0f3b1ea6d9cbabf3686a1c84d53fa4961ca2bf650'
    and old['before_sha256'] == sha(run / (before + '.sav')) == expected_before
    and old['after_sha256'] == sha(run / (after + '.sav')) == expected_after
    and old['boundaries'] == ['native_colony38_colonizing_species_phase_changed'])
checks['original_observation6_alltrue_actual0_source_and_SAVs_bound'] = (
    len(obs['checks']) == 6 and all(v is True for v in obs['checks'].values())
    and be['returncode'] == 0
    and be['helper_sha256'] == sha(run / 'priority_terravore_construction_boundary_observation.py')
    == 'e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678'
    and obs['before_sha256'] == expected_before and obs['after_sha256'] == expected_after
    and b['audit']['date'] == '2276.01.30' and a['audit']['date'] == '2276.02.01')

def native_colony(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as archive:
        roots = {k: v for k, v, opened in q.fields(archive.read('gamestate').decode('utf-8-sig')) if opened}
    return q.block(roots['colony'], '38')

cb, ca = native_colony(before), native_colony(after)
pb, pa = [q.scalars(st['planet_raw']['523']) for st in [b, a]]
checks['exact_native_completion_date_owned_size13_original_colony38'] = (
    all(pb.get(k) == pa.get(k) == v for k, v in {'owner': 0, 'controller': 0, 'colony': 38,
        'planet_size': 13, 'planet_class': 'pc_tropical', 'original_owner': 0}.items())
    and pb['colonize_date'] == '2273.11.26' and pa['colonize_date'] == '2276.02.01'
    and pa.get('save_on_death') == 1)
checks['original_colonizing_species73_retired_and_102_real_founder_pop'] = (
    q.scalars(cb).get('colonizing_species') == 73 and 'colonizing_species' not in q.scalars(ca)
    and b['species_population_by_colony']['38:73'] == 98
    and a['species_population_by_colony']['38:73'] == a['audit']['colonies']['38']['actual_pop_sum'] == 102
    and {k for k in a['species_population_by_colony'] if k.startswith('38:')} == {'38:73'})
messages = obs['new_country0_messages_raw']
checks['one_native_finish_colonize_notification268_correct_date_and_names'] = (
    len(messages) == 1 and all(q.scalars(messages[0]).get(k) == v for k, v in {
        'type': 'TYPE_FINISH_COLONIZE_PLANET', 'localization': 'MESSAGE_ORDER_FINISH_COLONIZE_PLANET',
        'receiver': 0, 'notification': 268, 'date': '2276.02.01'}.items())
    and '亚蒙-I' in messages[0] and 'key="COLONY"' in messages[0] and 'key="SYSTEM"' in messages[0])
checks['original_colonizer_consumption_not_reversed_no_pending_or_active_combat'] = (
    '16779032' not in a['owned_ships_raw'] and '863' not in a['owned_fleets_raw']
    and not a['pending_country0_raw'] and not old['active_combat_fleets'])
ui = load('terravore-colony38-native-completion2276-ui.ocr.json')
ui_text = '\n'.join(row['text'] for row in ui['rows'])
checks['reviewed_fresh_simp_chinese_completion_UI_exact_image_and_OCR_date'] = (
    ui['image_sha256'] == sha(run / 'terravore-colony38-native-completion2276-ui.jpg')
    == '68af7ecaf838e3a8e95764c4a34c9f8b67c7ba04d00914889c4a77458d0c2db8'
    and '2276.02.01' in ui_text and '决议' in ui_text and '正在殖民行星' not in ui_text)
checks['reviewed_native_decision_panel_original_image_held'] = (
    sha(run / 'terravore-colony38-native-decisions2276-ui.jpg')
    == 'a336c3e7a19d74e4a1c27a77506726114920ff7aff97713f8a58fb78bd83a3ba')
passed = all(v is True for v in checks.values())
proof = {'status': 'PASS_NATIVE_TERRAVORE_COLONY38_COMPLETION_COMPONENT' if passed else 'FAIL',
    'checks': checks, 'before_sha256': expected_before, 'after_sha256': expected_after,
    'date': a['audit']['date'], 'paid_births': old['paid_births'],
    'actual_population': old['actual_population'], 'native_colony_population': 102,
    'completed_colony38_raw': ca, 'prior_colonizing_colony38_raw': cb,
    'native_finish_message_raw': messages,
    'scope': 'Exact native completed colony and original Mod core only. Not devouring start, settlement, Queen C60 or full route acceptance.'}
out = run / (after + '-colony38-completion-proof.json')
assert not out.exists()
out.write_text(json.dumps(proof, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({'status': proof['status'], 'checks': len(checks),
    'failed': [k for k, v in checks.items() if v is not True], 'date': proof['date']}), flush=True)
assert passed, 'Original completion component failure retained; no calendar or devour continuation'
