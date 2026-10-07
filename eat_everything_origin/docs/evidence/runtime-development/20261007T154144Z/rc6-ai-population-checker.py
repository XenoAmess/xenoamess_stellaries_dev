import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names = ['rc6-lith-ai-trial2-real-day-before-controlled-completion',
         'rc6-lith-ai-trial2-controlled-native-completion-after']
a, b = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
checks = []

def check(name, actual, expected):
    checks.append({'check': name, 'actual': actual, 'expected': expected,
                   'status': 'PASS' if actual == expected else 'FAIL'})

def total(x):
    return sum(g['size'] for g in x['pop_groups'].values()
               if g['planet'] in x['countries']['0']['owned_colonies'])

player = []
for n in names:
    with zipfile.ZipFile(run / (n + '.sav')) as z:
        player.append(re.findall(r'country=(\d+)', q.block(z.read('gamestate').decode('utf-8-sig'), 'player')))
check('actual_player_foreign_both', player, [['16777218']] * 2)
log = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T154144Z/logs/game.log').read_text(encoding='utf-8')
check('native_original0_true_ai_before_trial2', 'EEP_RC6_TRIAL2_TRUE_AI_ORIGINAL0' in log, True)
check('actual_same_date', [a['date'], b['date']], ['2200.01.04'] * 2)
check('actual_capital_is_source_before', a['countries']['0']['native']['capital'], 15)
check('bound_core_is_original8_both', [next(t['id'] for t in x['event_targets'] if t['name'] == 'eep_core0') for x in (a, b)], [8, 8])
check('source_real100_before', a['colonies']['15']['actual_pop_sum'], 100)
check('core_real5200_before', a['colonies']['0']['actual_pop_sum'], 5200)
check('core_real5400_after', b['colonies']['0']['actual_pop_sum'], 5400)
check('native_new_population_exact100', total(b) - total(a), 100)
check('only100_left_for_final_eep_return', b['countries']['0']['variables']['eep_last_return'], 100)
check('native_ai_pop100_already_sent_to_bound_core',
      b['colonies']['0']['actual_pop_sum'] - a['colonies']['0']['actual_pop_sum']
      - b['countries']['0']['variables']['eep_last_return'], 100)
for key, value in [('eep_c', 20), ('eep_g', 0), ('eep_d', 7), ('eep_made', 0),
                   ('eep_last_manufactured', 0), ('eep_last_capacity', 5), ('eep_worlds', 1)]:
    check('actual_ledger_' + key, b['countries']['0']['variables'][key], value)
check('actual_source_shattered', b['planets']['3']['planet_class'], 'pc_shattered')
check('actual_source_no_owner', 'owner' in b['planets']['3'], False)
for flag in ['eep_active', 'eep_native', 'eep_owned_colony_event', 'colony_event', 'being_devoured']:
    check('actual_source_cleared_' + flag, flag in b['planets']['3']['flags'], False)
check('actual_bound_capacity7', b['planets']['8']['variables']['eep_capacity_value'], 7)
check('actual_bound_original_size20', b['planets']['8']['planet_size'], 20)
check('actual_royal_modifier_one', b['planets']['8']['modifiers'].count('modifier="eep_court"'), 1)
check('foreign_full_country_preserved', b['countries']['16777218'], a['countries']['16777218'])
foreign_colonies = a['countries']['16777218']['owned_colonies']
foreign_groups = {i: g for i, g in a['pop_groups'].items() if g['planet'] in foreign_colonies}
check('foreign_full_population_groups_preserved', {i: b['pop_groups'].get(i) for i in foreign_groups}, foreign_groups)
main = a['countries']['0']['native']['founder_species_ref']
check('actual_core_all_same_original_template',
      sorted({g['key']['species'] for g in b['pop_groups'].values() if g['planet'] == 0}), [main])
delta = {k: b['countries']['0']['stockpile'][k] - v for k, v in a['countries']['0']['stockpile'].items()}
check('only_native_minerals_alloys_stock_changes', sorted(k for k, v in delta.items() if v), ['alloys', 'minerals'])
check('native_minerals_positive', delta['minerals'] > 0, True)
check('native_alloys_positive', delta['alloys'] > 0, True)

result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'version': '0.2.0-rc.6', 'language': 'l_simp_chinese', 'checks': checks,
          'scope': 'Real original-country is_ai=yes after native player switch; current-start flags, source is temporary capital, controlled endpoint invokes unmodified native random lottery. Actual100 new native population plus100 final return reach bound core8, G/made0 and foreign full state isolated. Destination is inferred from exact real colony amounts and return ledger plus verified native branch code; not natural48-month timing or full acceptance.',
          'stock_deltas': delta, 'saves': {n: x['save_sha256'] for n, x in zip(names, (a, b), strict=True)}}
dest = run / 'rc6-real-ai-native-population-bound-core-proof.json'
assert not dest.exists()
dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'stock_deltas': {k:v for k,v in delta.items() if v},
                  'failed': [c['check'] for c in checks if c['status'] == 'FAIL']}))
