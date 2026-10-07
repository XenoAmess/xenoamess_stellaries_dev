import hashlib
import json
from pathlib import Path

run = Path(__file__).resolve().parent
names = ['rc6-native120-native08-initial', 'rc6-native120-source-seed-prepared',
         'rc6-native120-original-native-ui-start', 'rc6-native120-original-natural-monthone']
states = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
checks = []

def check(label, actual, expected):
    checks.append({'check': label, 'actual': actual, 'expected': expected,
                   'status': 'PASS' if actual == expected else 'FAIL'})

for i, (name, a) in enumerate(zip(names, states, strict=True)):
    check('original_save_hash_' + str(i), hashlib.sha256((run / (name + '.sav')).read_bytes()).hexdigest(), a['save_sha256'])
    check('actual_origin_default_' + str(i), 'origin="origin_default"' in a['countries']['0']['government'], True)
    check('actual_native_hive_' + str(i), 'authority="auth_hive_mind"' in a['countries']['0']['government'], True)
    check('actual_native_devouring_civic_' + str(i), '"civic_hive_devouring_swarm"' in a['countries']['0']['government'], True)
    sid = str(a['countries']['0']['native']['founder_species_ref'])
    check('actual_lithoid_class_' + str(i), a['species'][sid]['class'], 'LITHOID')
    check('actual_lithoid_trait_' + str(i), 'trait_lithoid' in a['species'][sid]['traits'], True)
    check('no_eep_economic_ledger_' + str(i), a['countries']['0']['variables'], {})
    check('no_eep_country_flags_except_probe_' + str(i),
          sorted(f for f in a['countries']['0']['flags'] if f.startswith('eep_') and not f.startswith('eep_probe_')), [])
    check('no_eep_core_target_' + str(i), [t for t in a['event_targets'] if t['name'].startswith('eep_core')], [])
    check('native_physical_mother_size_' + str(i), a['planets']['13']['planet_size'], 21)
    check('no_eep_physical_capacity_' + str(i), a['planets']['13']['variables'], {})
    check('no_royal_court_modifier_' + str(i), 'eep_court' in a['planets']['13']['modifiers'], False)
    check('no_royal_core_deposit_' + str(i), any(d['type'] == 'd_eep_core' for d in a['deposits'].values()), False)
    check('no_eep_situation_' + str(i), [s for s in a['situations'].values() if s['type'] == 'situation_eep_devouring'], [])

check('native_dates', [a['date'] for a in states], ['2200.01.01', '2200.01.01', '2200.01.02', '2200.02.01'])
check('native_initial_actual_population', states[0]['colonies']['0']['actual_pop_sum'], 5700)
check('actual_seed_transfer_mother', states[1]['colonies']['0']['actual_pop_sum'], 5600)
check('actual_seed_transfer_source', states[1]['colonies']['14']['actual_pop_sum'], 100)
check('seed_preparation_no_native_task', states[1]['situations'], {})
check('same_day_seed_country_stocks_unchanged', states[1]['countries']['0']['stockpile'], states[0]['countries']['0']['stockpile'])
for i in [2, 3]:
    a = states[i]
    tasks = list(a['situations'].values())
    check('exactly_one_native_task_' + str(i), len(tasks), 1)
    s = tasks[0]
    check('native_type_' + str(i), s['type'], 'situation_terravore_consume_planet')
    check('native_owner_' + str(i), s['country'], 0)
    check('native_target_' + str(i), [s['target']['type'], s['target']['id']], ['planet', 9])
    check('native_approach_' + str(i), s['approach'], 'approach_devour')
    check('native_progress_' + str(i), s['progress'], 0 if i == 2 else 8.5)
    check('native_size_variable_' + str(i), a['planets']['9']['variables']['num_districts_terravore'], 20)
    check('native_old_damage_variable_' + str(i), a['planets']['9']['variables']['num_lithoid_blockers'], 0)
    check('native_being_devoured_' + str(i), 'being_devoured' in a['planets']['9']['flags'], True)
    check('native_recently_eaten_' + str(i), 'recently_eaten_planet' in a['planets']['9']['flags'], True)
    check('no_eep_task_flags_' + str(i), [f for f in a['planets']['9']['flags'] if f.startswith('eep_') and not f.startswith('eep_probe_')], [])
    check('no_native_damage_first_month_' + str(i), sum(d['type'] == 'd_lithoid_devastation' and d['deposit_holder']['id'] == 9 for d in a['deposits'].values()), 0)

report = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'scope': 'Offline simplified-Chinese original non-EEP origin. Controlled real100 seed transfer; native decision UI routing and actual first natural month. Original task progress is8.5. Does not certify native endpoint, mathematical120-month prediction, true no-Mod baseline, or full Mod acceptance.',
          'language': 'l_simp_chinese', 'version': '0.2.0-rc.6',
          'saves': {n: a['save_sha256'] for n, a in zip(names, states, strict=True)}, 'checks': checks}
out = run / 'rc6-non-origin-native-ui-start-monthone-proof.json'
assert not out.exists()
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': report['status'], 'checks': len(checks), 'failed': [c for c in checks if c['status'] != 'PASS']}))
