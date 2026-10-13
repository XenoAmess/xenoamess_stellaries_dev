"""Supplement one immutable failed monthly guard for native pulsar shield suppression."""
import hashlib
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = 'terravore-first-post-hive-budget-22880101-v2'
after = 'terravore-post-second-society-month-22880201'
original_stage = after + '-post-second-society-month-guard-v4'
original_file = after + '-post-second-society-month-v4-proof.json'
original = json.loads((run / original_file).read_text('utf-8'))
execution = json.loads((run / (original_stage + '-execution.json')).read_text('utf-8'))
b, a = [read_state(run, stage) for stage in (before, after)]
game_file = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/star_classes/00_star_classes.txt')
game_raw = game_file.read_bytes()
class_data = q.block(game_raw.decode('utf-8-sig'), 'sc_binary_1')
target = 'all75_original_ship_identity_native_main_regeneration'

def identity_and_life(old, now):
    o, n = q.scalars(old), q.scalars(now)
    return (q.block(old, 'ship_design_implementation') == q.block(now, 'ship_design_implementation')
            and q.block(old, 'name') == q.block(now, 'name')
            and all(o.get(k) == n.get(k) for k in
                    ('construction_date', 'killed', 'max_hitpoints', 'max_armor_hitpoints',
                     'max_shield_hitpoints', 'hitpoints', 'armor_hitpoints')))

ship1_before, ship1_after = [q.scalars(s['ships']['1']) for s in (b, a)]
mm_before = q.block(b['fleets']['1'], 'movement_manager')
mm_after = q.block(a['fleets']['1'], 'movement_manager')
system3 = q.block(a['roots']['galactic_object'], '3')
planet206 = q.block(q.block(a['roots']['planets'], 'planet'), '206')
main = {str(i) for i in q.ids(q.block(b['fleets']['83886903'], 'ships'))}
support = {str(i) for fid in ('917', '50332250') for i in q.ids(q.block(b['fleets'][fid], 'ships'))}
normal_life = True
for sid, old in b['ships'].items():
    now = a['ships'].get(sid, '')
    o, n = q.scalars(old), q.scalars(now)
    normal_life = normal_life and identity_and_life(old, now)
    if sid in main:
        for key, cap in (('hitpoints', 'max_hitpoints'), ('armor_hitpoints', 'max_armor_hitpoints')):
            expected = min(D(str(o[cap])), D(str(o.get(key, 0))) + D(str(o[cap])) * D('.0025') * 30)
            normal_life = normal_life and abs(D(str(n.get(key, 0))) - expected) < D('.0001')
        normal_life = normal_life and n.get('shield_hitpoints', 0) == 0 and n.get('hitpoints', 0) > 0
    elif sid in support:
        normal_life = normal_life and n.get('shield_hitpoints', 0) == 0
    elif sid != '1':
        normal_life = normal_life and o.get('shield_hitpoints') == n.get('shield_hitpoints')

checks = {
    'immutable_original_v4_unique_fail_17_other_true_actual1':
        original['status'] == 'FAIL' and len(original['checks']) == 18
        and {key for key, value in original['checks'].items() if value is not True} == {target}
        and execution['returncode'] == 1
        and execution['helper_sha256'] == '29bc0ae0b292f63681813bfedac9682ba138db6b46d28a9446e21de52101f79d'
        and hashlib.sha256(Path(execution['command'][1]).read_bytes()).hexdigest() == execution['helper_sha256'],
    'same_original_native_saves_all75_members_and_life_except_shield1':
        original['before_sha256'] == b['audit']['save_sha256'] == h.sha256(run / (before + '.sav'))
        and original['after_sha256'] == a['audit']['save_sha256'] == h.sha256(run / (after + '.sav'))
        and len(b['ships']) == len(a['ships']) == 75 and set(b['ships']) == set(a['ships'])
        and normal_life
        and all(q.ids(q.block(fleet, 'ships')) == q.ids(q.block(a['fleets'][fid], 'ships'))
                for fid, fleet in b['fleets'].items()),
    'ship1_exact_native_shield320_to0_without_other_damage':
        ship1_before.get('shield_hitpoints') == 320 and 'shield_hitpoints' not in ship1_after
        and ship1_before['max_shield_hitpoints'] == ship1_after['max_shield_hitpoints'] == 320
        and ship1_before['hitpoints'] == ship1_after['hitpoints'] == 375
        and ship1_before['armor_hitpoints'] == ship1_after['armor_hitpoints'] == 125
        and ship1_before['leader'] == ship1_after['leader'] == 150994969
        and ship1_before['fleet'] == ship1_after['fleet'] == 1,
    'ship1_last_native_jump_168_to3_and_sc_binary1_pulsar':
        q.scalars(q.block(mm_before, 'coordinate')).get('origin') == 168
        and q.scalars(q.block(mm_before, 'last_ftl_jump')).get('to') == 168
        and q.scalars(q.block(mm_after, 'coordinate')).get('origin') == 3
        and q.scalars(q.block(q.block(mm_after, 'last_ftl_jump'), 'from')).get('origin') == 168
        and q.scalars(q.block(mm_after, 'last_ftl_jump')).get('to') == 3
        and q.scalars(mm_after).get('state') == 'move_wind_up'
        and q.scalars(system3).get('star_class') == 'sc_binary_1'
        and q.scalars(planet206).get('planet_class') == 'pc_pulsar',
    'installed_vanilla_sc_binary1_shield_reduction_exact100percent':
        q.scalars(q.block(class_data, 'modifier')).get('ship_shield_reduction') == 1.0
        and [q.scalars(value).get('key') for key, value, obj in q.fields(class_data)
             if key == 'planet' and obj] == ['pc_a_star', 'pc_pulsar'],
}
passed = all(value is True for value in checks.values())
out = run / (after + '-post-second-society-month-v5-proof.json')
assert not out.exists()
supplement = dict(original)
supplement.update({
    'status': 'PASS_NATIVE_PULSAR_SUPPLEMENT' if passed else 'FAIL',
    'checks': dict(original['checks'], **{target: passed}, **{'pulsar_supplement_' + k: v for k, v in checks.items()}),
    'original_failed_proof': original_file,
    'original_failed_execution_stage': original_stage,
    'installed_vanilla_star_classes_sha256': hashlib.sha256(game_raw).hexdigest(),
    'scope': 'One exact original Jan1-Feb1 science ship1 pulsar transit; no future shield exception.',
})
h.write_json(out, supplement)
print(json.dumps({'status': supplement['status'], 'checks': len(supplement['checks']),
                  'failed': [k for k, v in supplement['checks'].items() if v is not True],
                  'save_sha256': original['after_sha256']}), flush=True)
assert passed
