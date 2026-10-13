"""Bind the April science-ship shield change to a native pulsar transit."""
import hashlib
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = 'terravore-post-second-society-month-22880301'
after = 'terravore-post-second-society-month-22880401'
old_stage = after + '-post-second-society-month-guard-v4'
old_file = after + '-post-second-society-month-v4-proof.json'
old = json.loads((run / old_file).read_text('utf-8'))
execution = json.loads((run / (old_stage + '-execution.json')).read_text('utf-8'))
b, a = [read_state(run, stage) for stage in (before, after)]
star_file = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/star_classes/00_star_classes.txt')
star_raw = star_file.read_bytes()
binary = q.block(star_raw.decode('utf-8-sig'), 'sc_binary_1')
target = 'all75_original_ship_identity_native_main_regeneration'
old_mm, new_mm = [q.block(s['fleets']['1'], 'movement_manager') for s in (b, a)]
old_ship, new_ship = [q.scalars(s['ships']['1']) for s in (b, a)]
main = {str(i) for i in q.ids(q.block(b['fleets']['83886903'], 'ships'))}
supports = {str(i) for fid in ('917', '50332250') for i in q.ids(q.block(b['fleets'][fid], 'ships'))}
all_ships = len(b['ships']) == len(a['ships']) == 75 and set(b['ships']) == set(a['ships'])
for sid, previous in b['ships'].items():
    current = a['ships'].get(sid, '')
    p, c = q.scalars(previous), q.scalars(current)
    all_ships = all_ships and q.block(previous, 'ship_design_implementation') == q.block(current, 'ship_design_implementation')
    all_ships = all_ships and q.block(previous, 'name') == q.block(current, 'name')
    all_ships = all_ships and all(p.get(key) == c.get(key) for key in
        ('construction_date', 'killed', 'max_hitpoints', 'max_armor_hitpoints',
         'max_shield_hitpoints', 'hitpoints', 'armor_hitpoints'))
    if sid in main or sid in supports:
        all_ships = all_ships and c.get('shield_hitpoints', 0) == 0
    elif sid != '1':
        all_ships = all_ships and p.get('shield_hitpoints') == c.get('shield_hitpoints')

checks = {
    'original_unique_v4_fail_17_true_actual1_immutable_saves':
        old['status'] == 'FAIL' and len(old['checks']) == 18
        and {key for key, value in old['checks'].items() if value is not True} == {target}
        and execution['returncode'] == 1
        and execution['helper_sha256'] == '29bc0ae0b292f63681813bfedac9682ba138db6b46d28a9446e21de52101f79d'
        and hashlib.sha256(Path(execution['command'][1]).read_bytes()).hexdigest() == execution['helper_sha256']
        and old['before_sha256'] == b['audit']['save_sha256'] == h.sha256(run / (before + '.sav'))
        and old['after_sha256'] == a['audit']['save_sha256'] == h.sha256(run / (after + '.sav')),
    'all75_original_ship_identity_fleets_and_only_ship1_shield_delta':
        all_ships and len(b['fleets']) == len(a['fleets']) == 35
        and all(q.ids(q.block(fleet, 'ships')) == q.ids(q.block(a['fleets'][fid], 'ships'))
                for fid, fleet in b['fleets'].items())
        and old_ship['shield_hitpoints'] == 208 and new_ship['shield_hitpoints'] == 64
        and old_ship['max_shield_hitpoints'] == new_ship['max_shield_hitpoints'] == 320
        and old_ship['hitpoints'] == new_ship['hitpoints'] == 375
        and old_ship['armor_hitpoints'] == new_ship['armor_hitpoints'] == 125
        and old_ship['leader'] == new_ship['leader'] == 150994969,
    'native_path16_to_pulsar193_last_jump193_to_normal26':
        q.scalars(q.block(old_mm, 'coordinate')).get('origin') == 16
        and 'origin=193' in q.block(old_mm, 'path')
        and 'jump_bypass' in q.block(old_mm, 'path')
        and q.scalars(q.block(q.block(new_mm, 'last_ftl_jump'), 'from')).get('origin') == 193
        and q.scalars(q.block(new_mm, 'last_ftl_jump')).get('to') == 26
        and q.scalars(q.block(new_mm, 'coordinate')).get('origin') == 26
        and q.scalars(q.block(a['roots']['galactic_object'], '193')).get('star_class') == 'sc_binary_1'
        and q.scalars(q.block(a['roots']['galactic_object'], '26')).get('star_class') == 'sc_m'
        and q.scalars(q.block(binary, 'modifier')).get('ship_shield_reduction') == 1.0,
}
passed = all(value is True for value in checks.values())
out = run / (after + '-post-second-society-month-v7-proof.json')
assert not out.exists()
supplement = dict(old)
supplement.update({
    'status': 'PASS_NATIVE_PULSAR_TRANSIT_SUPPLEMENT' if passed else 'FAIL',
    'checks': dict(old['checks'], **{target: passed},
                   **{'pulsar_transit_' + key: value for key, value in checks.items()}),
    'original_failed_proof': old_file,
    'original_failed_execution_stage': old_stage,
    'installed_vanilla_star_classes_sha256': hashlib.sha256(star_raw).hexdigest(),
    'scope': 'One exact Mar1-Apr1 shield transit through pulsar system193; no future exception.',
})
h.write_json(out, supplement)
print(json.dumps({'status': supplement['status'], 'checks': len(supplement['checks']),
                  'failed': [key for key, value in supplement['checks'].items() if value is not True],
                  'save_sha256': old['after_sha256']}), flush=True)
assert passed
