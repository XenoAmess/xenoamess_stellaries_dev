"""Supplement the exact native May science-ship shield recovery in normal system26."""
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
before = 'terravore-post-second-society-month-22880501'
after = 'terravore-post-second-society-month-22880601'
old_stage = after + '-post-second-society-month-guard-v4'
old_file = after + '-post-second-society-month-v4-proof.json'
old = json.loads((run / old_file).read_text('utf-8'))
execution = json.loads((run / (old_stage + '-execution.json')).read_text('utf-8'))
b, a = [read_state(run, stage) for stage in (before, after)]
target = 'all75_original_ship_identity_native_main_regeneration'
old_ship, new_ship = [q.scalars(s['ships']['1']) for s in (b, a)]
old_mm, new_mm = [q.block(s['fleets']['1'], 'movement_manager') for s in (b, a)]
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
system26 = q.block(a['roots']['galactic_object'], '26')
system119 = q.block(a['roots']['galactic_object'], '119')
checks = {
    'original_v4_unique_fail17true_actual1_same_native_saves':
        old['status'] == 'FAIL' and len(old['checks']) == 18
        and {key for key, value in old['checks'].items() if value is not True} == {target}
        and execution['returncode'] == 1
        and execution['helper_sha256'] == '29bc0ae0b292f63681813bfedac9682ba138db6b46d28a9446e21de52101f79d'
        and hashlib.sha256(Path(execution['command'][1]).read_bytes()).hexdigest() == execution['helper_sha256']
        and old['before_sha256'] == b['audit']['save_sha256'] == h.sha256(run / (before + '.sav'))
        and old['after_sha256'] == a['audit']['save_sha256'] == h.sha256(run / (after + '.sav')),
    'all75_identity_life_only_ship1_shield304_to320_at_cap':
        all_ships and len(b['fleets']) == len(a['fleets']) == 35
        and all(q.ids(q.block(fleet, 'ships')) == q.ids(q.block(a['fleets'][fid], 'ships'))
                for fid, fleet in b['fleets'].items())
        and old_ship['shield_hitpoints'] == 304 and new_ship['shield_hitpoints'] == 320
        and new_ship['shield_hitpoints'] == new_ship['max_shield_hitpoints']
        and old_ship['max_shield_hitpoints'] == new_ship['max_shield_hitpoints'] == 320
        and old_ship['hitpoints'] == new_ship['hitpoints'] == 375
        and old_ship['armor_hitpoints'] == new_ship['armor_hitpoints'] == 125
        and old_ship['leader'] == new_ship['leader'] == 150994969
        and old_ship['last_damage'] == new_ship['last_damage'] == '2240.03.24'
        and old_ship['last_combat_activity'] == new_ship['last_combat_activity'] == '2240.03.24',
    'native_bypass26_to119_both_normal_no_combat':
        q.scalars(q.block(old_mm, 'coordinate')).get('origin') == 26
        and q.scalars(q.block(new_mm, 'coordinate')).get('origin') == 119
        and q.scalars(q.block(old_mm, 'last_ftl_jump')).get('to') == 26
        and q.scalars(q.block(new_mm, 'last_ftl_jump')).get('to') == 119
        and q.scalars(q.block(new_mm, 'last_ftl_jump')).get('bypass_from') == 18
        and q.scalars(q.block(new_mm, 'last_ftl_jump')).get('bypass_to') == 40
        and q.scalars(system26).get('star_class') == 'sc_m'
        and q.scalars(system26).get('storm') == 4294967295
        and not q.block(system26, 'timed_modifier')
        and q.scalars(system119).get('star_class') == 'sc_m_giant'
        and q.scalars(system119).get('storm') == 4294967295
        and not q.block(system119, 'timed_modifier')
        and not q.ids(q.block(q.block(b['fleets']['1'], 'combat'), 'in_combat_with'))
        and not q.ids(q.block(q.block(a['fleets']['1'], 'combat'), 'in_combat_with')),
}
passed = all(value is True for value in checks.values())
out = run / (after + '-post-second-society-month-v10-proof.json')
assert not out.exists()
supplement = dict(old)
supplement.update({
    'status': 'PASS_NATIVE_SHIELD_CAP_SUPPLEMENT' if passed else 'FAIL',
    'checks': dict(old['checks'], **{target: passed},
                   **{'shield_regen_' + key: value for key, value in checks.items()}),
    'original_failed_proof': old_file,
    'original_failed_execution_stage': old_stage,
    'scope': 'One exact May1-Jun1 ship1 shield reaches cap after native bypass from26 to119.',
})
h.write_json(out, supplement)
print(json.dumps({'status': supplement['status'], 'checks': len(supplement['checks']),
                  'failed': [key for key, value in supplement['checks'].items() if value is not True],
                  'save_sha256': old['after_sha256']}), flush=True)
assert passed
