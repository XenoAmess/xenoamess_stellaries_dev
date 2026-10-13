"""Supplement one immutable failed month with exact native storm and shield changes."""
import hashlib
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state, omit

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = 'terravore-post-second-society-month-22880201'
after = 'terravore-post-second-society-month-22880301'
original_stage = after + '-post-second-society-month-guard-v4'
original_file = after + '-post-second-society-month-v4-proof.json'
original = json.loads((run / original_file).read_text('utf-8'))
execution = json.loads((run / (original_stage + '-execution.json')).read_text('utf-8'))
b, a = [read_state(run, stage) for stage in (before, after)]
star_path = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/star_classes/00_star_classes.txt')
action_path = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/on_actions/00_on_actions.txt')
event_path = Path('C:/SteamLibrary/steamapps/common/Stellaris/events/cosmic_storms_events_1.txt')
star_text = star_path.read_text('utf-8-sig')
action_text = action_path.read_text('utf-8-sig')
event_text = event_path.read_text('utf-8-sig')
event_match = re.search(r'system_event\s*=\s*\{\s*id\s*=\s*cstorms\.10\b', event_text)
event_slice = event_text[event_match.start():event_text.find('system_event = {', event_match.end())] if event_match else ''
old_ship, new_ship = [q.scalars(s['ships']['1']) for s in (b, a)]
old_mm, new_mm = [q.block(s['fleets']['1'], 'movement_manager') for s in (b, a)]
old_events, new_events = [q.block(s['country'], 'events') for s in (b, a)]
old_anomalies, new_anomalies = [q.ids(q.block(e, 'anomalies')) for e in (old_events, new_events)]
old_planet, new_planet = [q.block(q.block(s['roots']['planets'], 'planet'), '1070') for s in (b, a)]
old_flags, new_flags = [q.block(s['country'], 'flags') for s in (b, a)]

def flags(text):
    return {key: q.scalars(value) if obj else q.unquote(value)
            for key, value, obj in q.fields(text)}

old_flag_map, new_flag_map = flags(old_flags), flags(new_flags)
expected_flags = {
    key: dict(value, flag_days=value['flag_days'] - 30)
    if isinstance(value, dict) and 'flag_days' in value else value
    for key, value in old_flag_map.items()
    if not isinstance(value, dict) or 'flag_days' not in value or value['flag_days'] > 30
}
old_s96, new_s96 = [q.scalars(q.block(s['roots']['galactic_object'], '96')) for s in (b, a)]
target = {
    'all_other_native_tech_fields_and_project_shapes_held',
    'all75_original_ship_identity_native_main_regeneration',
    'native_flags_only_timer_change_contacts_held',
}
normal_life = True
for sid, old in b['ships'].items():
    now = a['ships'].get(sid, '')
    o, n = q.scalars(old), q.scalars(now)
    normal_life = normal_life and q.block(old, 'ship_design_implementation') == q.block(now, 'ship_design_implementation')
    normal_life = normal_life and q.block(old, 'name') == q.block(now, 'name')
    normal_life = normal_life and all(o.get(k) == n.get(k) for k in
        ('construction_date', 'killed', 'max_hitpoints', 'max_armor_hitpoints',
         'max_shield_hitpoints', 'hitpoints', 'armor_hitpoints'))
    if sid != '1':
        normal_life = normal_life and o.get('shield_hitpoints') == n.get('shield_hitpoints')

checks = {
    'original_v4_exact_three_fail_15_true_actual1_and_same_SAV':
        original['status'] == 'FAIL' and len(original['checks']) == 18
        and {key for key, value in original['checks'].items() if value is not True} == target
        and execution['returncode'] == 1
        and execution['helper_sha256'] == '29bc0ae0b292f63681813bfedac9682ba138db6b46d28a9446e21de52101f79d'
        and hashlib.sha256(Path(execution['command'][1]).read_bytes()).hexdigest() == execution['helper_sha256']
        and original['before_sha256'] == b['audit']['save_sha256'] == h.sha256(run / (before + '.sav'))
        and original['after_sha256'] == a['audit']['save_sha256'] == h.sha256(run / (after + '.sav')),
    'native_ship1_only_shield_recovers_in_nonpulsar16_all75_untouched':
        len(b['ships']) == len(a['ships']) == 75 and set(b['ships']) == set(a['ships'])
        and normal_life and old_ship.get('shield_hitpoints', 0) == 0
        and new_ship.get('shield_hitpoints') == 208
        and old_ship['max_shield_hitpoints'] == new_ship['max_shield_hitpoints'] == 320
        and old_ship['hitpoints'] == new_ship['hitpoints'] == 375
        and old_ship['armor_hitpoints'] == new_ship['armor_hitpoints'] == 125
        and old_ship['leader'] == new_ship['leader'] == 150994969
        and q.scalars(q.block(old_mm, 'coordinate')).get('origin') == 3
        and q.scalars(q.block(new_mm, 'coordinate')).get('origin') == 16
        and q.scalars(q.block(q.block(new_mm, 'last_ftl_jump'), 'from')).get('origin') == 3
        and q.scalars(q.block(new_mm, 'last_ftl_jump')).get('to') == 16
        and q.scalars(q.block(q.block(star_text, 'sc_binary_1'), 'modifier')).get('ship_shield_reduction') == 1.0
        and q.scalars(q.block(a['roots']['galactic_object'], '16')).get('star_class') == 'sc_f',
    'native_tech_unchanged_only_one_new_planet_anomaly1070':
        omit(q.block(b['country'], 'tech_status'), {'stored_techpoints', 'society_queue'})
        == omit(q.block(a['country'], 'tech_status'), {'stored_techpoints', 'society_queue'})
        and new_anomalies == old_anomalies + [1070]
        and omit(old_events, {'anomalies'}) == omit(new_events, {'anomalies'})
        and omit(old_planet, {'anomaly', 'flags'}) == omit(new_planet, {'anomaly', 'flags'})
        and 'anomaly' not in q.scalars(old_planet)
        and q.scalars(new_planet).get('anomaly') == 'STORMS_ANOM_POLYCHROMATIC'
        and not q.block(old_planet, 'flags')
        and list(q.scalars(q.block(new_planet, 'flags'))) == ['affected_by_gravity_storm'],
    'native_storm_left96_only_spawn_flag_and_timer_changes':
        old_s96.get('storm') == 50331648 and new_s96.get('storm') == 4294967295
        and old_flag_map.get('spawned_STORMS_ANOM_POLYCHROMATIC') is None
        and new_flag_map == dict(expected_flags, spawned_STORMS_ANOM_POLYCHROMATIC=63569736)
        and q.scalars(q.block(q.block(b['roots']['storms'], 'storms'), '50331648')).get('type') == 'gravity_storm'
        and q.scalars(q.block(q.block(a['roots']['storms'], 'storms'), '50331648')).get('type') == 'gravity_storm',
    'installed_vanilla_on_storm_left_system_cstorms10_sets_flag_and_anomaly':
        'on_storm_left_system' in action_text
        and bool(re.search(r'on_storm_left_system\s*=\s*\{[^}]*20\s*=\s*cstorms\.10', action_text, re.S))
        and 'set_country_flag = spawned_STORMS_ANOM_POLYCHROMATIC' in event_slice
        and 'category = STORMS_ANOM_POLYCHROMATIC' in event_slice,
}
passed = all(value is True for value in checks.values())
out = run / (after + '-post-second-society-month-v6-proof.json')
assert not out.exists()
supplement = dict(original)
supplement.update({
    'status': 'PASS_NATIVE_STORM_AND_SHIELD_SUPPLEMENT' if passed else 'FAIL',
    'checks': dict(original['checks'], **{key: passed for key in target},
                   **{'native_supplement_' + key: value for key, value in checks.items()}),
    'original_failed_proof': original_file,
    'original_failed_execution_stage': original_stage,
    'installed_vanilla_script_sha256': {str(p): h.sha256(p) for p in (star_path, action_path, event_path)},
    'scope': 'One exact Feb1-Mar1 shield recovery and native storm anomaly; no future exception.',
})
h.write_json(out, supplement)
print(json.dumps({'status': supplement['status'], 'checks': len(supplement['checks']),
                  'failed': [key for key, value in supplement['checks'].items() if value is not True],
                  'save_sha256': original['after_sha256']}), flush=True)
assert passed
