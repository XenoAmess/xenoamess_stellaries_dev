import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names = ['rc6-lith-verified-true-ai-before-controlled-completion',
         'rc6-lith-true-ai-natural-month47-before-endpoint',
         'rc6-lith-true-ai-natural-precise-month48-day1',
         'rc6-lith-true-ai-natural-month48-day2-settled']
states = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
start, m47, day1, day2 = states
checks = []


def check(label, actual, expected):
    checks.append({'check': label, 'actual': actual, 'expected': expected,
                   'status': 'PASS' if actual == expected else 'FAIL'})


def progress(x):
    return next(s['progress'] for s in x['situations'].values()
                if s['type'] == 'situation_eep_devouring')


def damage(x):
    return sum(d['type'] == 'd_lithoid_devastation'
               and d['deposit_holder']['id'] == 3 for d in x['deposits'].values())


check('native_dates', [s['date'] for s in states],
      ['2200.01.03', '2203.12.30', '2204.01.01', '2204.01.02'])
check('actual_calendar_progress', [progress(s) for s in states], [0, 47, 48, 48])
for i, s in enumerate(states):
    with zipfile.ZipFile(run / (names[i] + '.sav')) as z:
        raw = z.read('gamestate').decode('utf-8-sig')
    check('actual_foreign_player_' + str(i), re.findall(r'country=(\d+)', q.block(raw, 'player')), ['16777218'])
    check('original_core_binding_' + str(i),
          next(t['id'] for t in s['event_targets'] if t['name'] == 'eep_core0'), 8)
    check('q20_t48_fixed_' + str(i),
          [s['planets']['3']['variables']['eep_q'], s['planets']['3']['variables']['eep_months']], [20, 48])
    check('core_original_size20_' + str(i), s['planets']['8']['planet_size'], 20)
    check('core_unique_royal_modifier_' + str(i), s['planets']['8']['modifiers'].count('modifier="eep_court"'), 1)
    v = s['countries']['0']['variables']
    check('ledger_' + str(i), [v[k] for k in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']],
          [20, 0, 7, 0, 1] if i == 3 else [0, 0, 2, 0, 0])
    check('physical_core_capacity_' + str(i), s['planets']['8']['variables']['eep_capacity_value'], 7 if i == 3 else 2)
    if i < 3:
        check('original_source_owned_' + str(i), [s['planets']['3']['owner'], s['planets']['3']['controller']], [0, 0])
        check('source_temporary_capital_' + str(i), s['countries']['0']['native']['capital'], 15)
        for f in ['eep_active', 'eep_native', 'eep_owned_colony_event', 'colony_event']:
            check('actual_current_start_flag_' + str(i) + '_' + f, f in s['planets']['3']['flags'], True)

check('no_damage_at_current_start', damage(start), 0)
check('native_six_damage_before_endpoint', [damage(m47), damage(day1)], [6, 6])
check('actual_native_cooldown_before_endpoint', 'recently_eaten_planet' in m47['planets']['3']['flags'], True)
check('actual_original_source_shattered', day2['planets']['3']['planet_class'], 'pc_shattered')
check('actual_original_source_unowned', 'owner' in day2['planets']['3'], False)
check('actual_original_source_deposits_cleared', day2['planets']['3']['deposits'], [])
for f in ['eep_active', 'eep_native', 'eep_owned_colony_event', 'colony_event', 'being_devoured', 'eep_pending']:
    check('actual_source_task_flag_cleared_' + f, f in day2['planets']['3']['flags'], False)
for f in ['eep_bites_done', 'eep_credit_done', 'eep_return_done', 'eep_population_done', 'eep_crisis_done', 'eep_destroy_done']:
    check('actual_source_receipt_' + f, f in day2['planets']['3']['flags'], True)
check('actual_final_return_all_source_population', day2['countries']['0']['variables']['eep_last_return'], day1['colonies']['15']['actual_pop_sum'])
extra = day2['colonies']['0']['actual_pop_sum'] - day1['colonies']['0']['actual_pop_sum'] - day1['colonies']['15']['actual_pop_sum']
check('actual_end_native_population_nonnegative', extra >= 0, True)
check('actual_end_native_population_is_default100_units', extra % 100, 0)
check('actual_no_generic_population', day2['countries']['0']['variables']['eep_last_manufactured'], 0)
check('actual_foreign_population_same_endpoint_day', day2['colonies']['2']['actual_pop_sum'], day1['colonies']['2']['actual_pop_sum'])
check('actual_foreign_stockpile_same_endpoint_day', day2['countries']['16777218']['stockpile'], day1['countries']['16777218']['stockpile'])
sa, sb = [x['countries']['0']['stockpile'] for x in (day1, day2)]
delta = {k: sb.get(k, 0) - sa.get(k, 0) for k in sorted(sa.keys() | sb.keys())}
check('only_original_native_end_resource_types', sorted(k for k, v in delta.items() if abs(v) > 0.00001), ['alloys', 'minerals'])
for k in ['alloys', 'minerals']:
    check('positive_native_end_' + k, delta[k] > 0, True)
log = Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T154144Z/logs/game.log').read_text(encoding='utf-8', errors='replace')
months = re.findall(r'\[([^\]]+)\] Log effect, file: events/eep_probe_events.txt line: 70\. EEP_MONTH source=EEP-UI-Q20 Q=20 T=48 progress=(\d+)', log)
series = [int(p) for _, p in months]
check('actual_native_log_contains_all47_months_in_order', any(series[i:i+47] == list(range(1, 48)) for i in range(len(series))), True)
check('initial_true_ai_marker_logged', 'EEP_RC6_TRUE_AI_AFTER_NATIVE_SLOT2' in log, True)
result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'version': '0.2.0-rc.6', 'language': 'l_simp_chinese', 'checks': checks,
          'scope': 'Real calendar on a controlled Q20 source after exact verified true-AI seed reload. Native47-month progress and real48-month next-day settlement, annual bites/cooldown, original-capital distinction, zero generic manufacturing and endpoint isolation. No resource/tech/AP/progress grant during calendar. Not natural newgame balance or non-origin120-month control. Initial incorrect two-day expected-date FAIL retained separately.',
          'saves': {n: s['save_sha256'] for n, s in zip(names, states, strict=True)},
          'endpoint_stock_deltas': delta, 'endpoint_native_new_pop_inference': extra,
          'native_month_logs': months}
out = run / 'rc6-true-ai-natural48-month-boundary-proof.json'
assert not out.exists()
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'failed': [c for c in checks if c['status'] == 'FAIL'],
                  'endpoint_stock_deltas': {k:v for k,v in delta.items() if v}, 'endpoint_native_new_pop': extra}))
