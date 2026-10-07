import hashlib
import json
import re
from pathlib import Path

run = Path(__file__).resolve().parent
names = ['rc6-native120-original-native-ui-start', 'rc6-native120-original-natural-monthone',
         'rc6-native120-original-natural-month117-last-day',
         'rc6-native120-original-natural-month118-dayone-pending',
         'rc6-native120-original-month118-same-day-ack',
         'rc6-native120-original-month118-next-day-cleanup',
         'rc6-native120-original-natural-month119-no-eep-reward',
         'rc6-native120-original-natural-month120-no-eep-reward']
states = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
checks = []

def check(label, actual, expected):
    def evidence(v):
        data = json.dumps(v, sort_keys=True, ensure_ascii=False).encode('utf-8')
        return v if len(data) <= 1400 else {'complete_canonical_json_sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'full_inputs': 'original audit JSON and native SAV retained'}
    checks.append({'check': label, 'actual': evidence(actual), 'expected': evidence(expected),
                   'status': 'PASS' if actual == expected else 'FAIL'})

dates = ['2200.01.02', '2200.02.01', '2209.10.30', '2209.11.01', '2209.11.01',
         '2209.11.02', '2209.12.01', '2210.01.01']
check('actual_native_dates', [a['date'] for a in states], dates)
for i, (n, a) in enumerate(zip(names, states, strict=True)):
    check('actual_original_save_bytes_' + str(i), hashlib.sha256((run / (n + '.sav')).read_bytes()).hexdigest(), a['save_sha256'])
    check('actual_original_origin_' + str(i), 'origin="origin_default"' in a['countries']['0']['government'], True)
    check('actual_original_ledger_empty_' + str(i), a['countries']['0']['variables'], {})
    check('no_eep_royal_country_flags_' + str(i), [f for f in a['countries']['0']['flags'] if f.startswith('eep_') and not f.startswith('eep_probe_')], [])
    check('native_core_size21_' + str(i), a['planets']['13']['planet_size'], 21)
    check('no_eep_core_capacity_' + str(i), a['planets']['13']['variables'], {})
    check('no_eep_royal_modifier_' + str(i), 'eep_court' in a['planets']['13']['modifiers'], False)
    check('no_eep_royal_deposit_' + str(i), any(d['type'] == 'd_eep_core' for d in a['deposits'].values()), False)
    check('no_eep_core_binding_' + str(i), [t for t in a['event_targets'] if t['name'].startswith('eep_core')], [])
    check('no_eep_situation_' + str(i), [s for s in a['situations'].values() if s['type'] == 'situation_eep_devouring'], [])
    check('source_original_num_districts20_' + str(i), a['planets']['9']['variables']['num_districts_terravore'], 20)
    check('no_eep_source_variables_' + str(i), [v for v in a['planets']['9']['variables'] if v.startswith('eep_')], [])
    check('no_eep_source_receipts_' + str(i), [f for f in a['planets']['9']['flags'] if f.startswith('eep_') and not f.startswith('eep_probe_')], [])
    sid = str(a['countries']['0']['native']['founder_species_ref'])
    check('actual_native_lithoid_' + str(i), a['species'][sid]['class'], 'LITHOID')
    if i < 5:
        tasks = list(a['situations'].values())
        check('one_native_task_' + str(i), len(tasks), 1)
        s = tasks[0]
        check('actual_native_task_type_' + str(i), s['type'], 'situation_terravore_consume_planet')
        check('actual_native_task_source_' + str(i), [s['country'], s['target']['type'], s['target']['id']], [0, 'planet', 9])
        check('actual_native_progress_' + str(i), s['progress'], [0, 8.5, 994.5, 1000, 1000][i])
        if i:
            check('actual_native_last_month_step_' + str(i), s['last_month_progress'], 8.5)
    else:
        check('actual_native_task_cleaned_' + str(i), a['situations'], {})
        check('actual_native_being_devoured_cleaned_' + str(i), 'being_devoured' in a['planets']['9']['flags'], False)
    if i >= 3:
        check('actual_source_shattered_' + str(i), a['planets']['9']['planet_class'], 'pc_shattered')
        check('actual_source_no_owner_' + str(i), 'owner' in a['planets']['9'], False)
        check('actual_source_deposits_empty_' + str(i), a['planets']['9']['deposits'], [])
        check('actual_source_colony_population_zero_' + str(i), a['colonies']['14']['actual_pop_sum'], 0)

check('117_native_months_exact8point5', states[2]['situations']['7']['progress'], 117 * 8.5)
check('117_boundary_still_owned', [states[2]['planets']['9']['owner'], states[2]['planets']['9']['controller']], [0, 0])
check('117_boundary_original18_damage', sum(d['type'] == 'd_lithoid_devastation' and d['deposit_holder']['id'] == 9 for d in states[2]['deposits'].values()), 18)
check('117_boundary_actual_source_population', states[2]['colonies']['14']['actual_pop_sum'], 336)
check('118_boundary_actual_mother_population', states[3]['colonies']['0']['actual_pop_sum'], 6497)
metadata = {'save', 'save_sha256', 'gamestate_sha256', 'gamestate_bytes'}
check('same_day_original_event_ack_all_audit_game_fields',
      {k: v for k, v in states[4].items() if k not in metadata},
      {k: v for k, v in states[3].items() if k not in metadata})
check('same_day_real_next_day_mother_population', states[5]['colonies']['0']['actual_pop_sum'], states[4]['colonies']['0']['actual_pop_sum'])
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
check('actual_language', manifest['language'], 'l_simp_chinese')
check('actual_fixture_fingerprint', manifest['copied_mod_tree_sha256'], '769fec7a3641fedc655db3f84d8a32b73b623bd61bbca6e74e71e261cbc8b6dd')
fixture = Path(manifest['copied_mod'])
for kind, name in [('script_values', 'terravore_progress'), ('situations', 'situation_terravore_consume_planet')]:
    definitions = [p.relative_to(fixture).as_posix() for p in (fixture / 'common' / kind).glob('*.txt')
                   if re.search(r'(?m)^\s*' + re.escape(name) + r'\s*=', p.read_text(encoding='utf-8-sig'))]
    check('no_fixture_original_definition_override_' + name, definitions, [])
game = Path('C:/SteamLibrary/steamapps/common/Stellaris')
source_hashes = {p: hashlib.sha256((game / p).read_bytes()).hexdigest() for p in
                 ['common/script_values/00_script_values.txt', 'common/situations/02_strategic_situations.txt', 'events/colony_events_1.txt']}
report = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'scope': 'Offline simplified-Chinese non-EEP original origin with rc6 fixture loaded. Controlled genuine100 seed transfer, natural original task progress8.5 over117 months, completion118 and original UI ack/next-day cleanup/persistence to nominal119 and120. No EEP reward, capacity, royal modifier, queen state or task. Exact full-audit same-day original event acknowledgement. Not true no-Mod baseline or full Mod acceptance; original120 prediction differs from native observed118 and needs independent no-Mod control.',
          'version': '0.2.0-rc.6', 'language': 'l_simp_chinese', 'full_mod_acceptance': 'NOT_COMPLETE',
          'true_no_mod_agreement': 'PENDING', 'nominal_month_prediction': 120, 'observed_effective_completion_months': 118,
          'saves': {n: a['save_sha256'] for n, a in zip(names, states, strict=True)},
          'primary_game_source_sha256': source_hashes, 'checks': checks}
out = run / 'rc6-non-origin-native-natural118-nominal120-proof.json'
assert not out.exists()
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': report['status'], 'checks': len(checks), 'failed': [c for c in checks if c['status'] != 'PASS']}))
