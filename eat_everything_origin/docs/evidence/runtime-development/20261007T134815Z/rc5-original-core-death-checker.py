import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q
run = Path('_runtime/heart-of-devouring/runs/20261007T134815Z')
names = ['rc5-core-death-active-before-destruction',
         'rc5-core-permanently-destroyed-notice-pending',
         'rc5-core-death-notice-reloaded-before-ack',
         'rc5-core-death-real-next-day-aborted',
         'rc5-core-death-after-five-same-day-callbacks',
         'rc5-core-death-month-later-direct-restart-refused']
audits = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
alive, pending, reloaded, day, replay, month = audits
checks = []
def check(name, actual, expected):
    checks.append({'check': name, 'status': 'PASS' if actual == expected else 'FAIL',
                   'actual': actual, 'expected': expected})
check('actual_dates', [a['date'] for a in audits], ['2200.01.02'] * 3 + ['2200.01.03'] * 2 + ['2200.02.03'])
check('actual_active_task_before_destruction', [(t['target']['id'], t['progress']) for t in alive['situations'].values()], [(6, 0)])
check('actual_seed_before_destruction100', alive['colonies']['13']['actual_pop_sum'], 100)
check('actual_original_mother_destroyed', pending['planets']['1']['planet_class'], 'pc_shattered')
check('actual_old_mother_has_no_owner', 'owner' not in pending['planets']['1'], True)
check('actual_destruction_all_stocks_preserved', pending['countries']['0']['stockpile'], alive['countries']['0']['stockpile'])
check('actual_destruction_ledger_preserved', pending['countries']['0']['variables'], alive['countries']['0']['variables'])
check('actual_native_capital_survival_source_colony13', pending['countries']['0']['native']['capital'], 13)
for key in ['stockpile', 'variables', 'flags']:
    check('pending_notice_reload_' + key + '_preserved', reloaded['countries']['0'][key], pending['countries']['0'][key])
check('actual_pending_reload_source100', reloaded['colonies']['13']['actual_pop_sum'], 100)
check('actual_next_day_task_removed', day['situations'], {})
check('actual_next_day_source_seed_still100', day['colonies']['13']['actual_pop_sum'], 100)
for flag in ['eep_active', 'eep_pending', 'eep_native', 'eep_owned_colony_event', 'colony_event']:
    check('actual_next_day_source_flag_cleared_' + flag, flag in day['planets']['6']['flags'], False)
for key in ['countries', 'planets', 'colonies', 'pop_groups', 'pop_jobs', 'deposits',
            'districts', 'situations', 'species', 'event_targets']:
    check('same_day_five_state_callbacks_full_' + key + '_preserved', replay[key], day[key])
check('actual_month_later_restart_has_no_tasks', month['situations'], {})
for data, label in [(pending, 'pending'), (reloaded, 'reloaded'), (day, 'next_day'), (replay, 'replay'), (month, 'month_restart')]:
    check(label + '_only_original_core_target1', [t['id'] for t in data['event_targets'] if t['name'] == 'eep_core0'], [1])
    check(label + '_permanent_death_receipt', 'eep_core_dead' in data['countries']['0']['flags'], True)
    check(label + '_zero_economic_rewards', {k: data['countries']['0']['variables'][k] for k in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']},
          {'eep_c': 0, 'eep_g': 0, 'eep_d': 2, 'eep_made': 0, 'eep_worlds': 0})
check('actual_surviving_source_not_promoted_to_core', 'eep_core' in month['planets']['6']['flags'], False)
check('actual_surviving_source_no_eep_capacity_variable', 'eep_capacity_value' in month['planets']['6']['variables'], False)
check('actual_surviving_source_no_eep_capacity_modifier', 'eep_capacity' in month['planets']['6']['modifiers'], False)
check('actual_surviving_source_size20_preserved', month['planets']['6']['planet_size'], 20)
check('month_population_growth_is_native2', month['colonies']['13']['actual_pop_sum'] - day['colonies']['13']['actual_pop_sum'],
      sum(g.get('last_month_growth', 0) for g in month['pop_groups'].values() if g['planet'] == 13))
events = {}
for name in names:
    with zipfile.ZipFile(run / (name + '.sav')) as z:
        events[name] = [q.scalars(v).get('event') for k, v, obj in q.fields(z.read('gamestate').decode('utf-8-sig')) if obj and k == 'player_event']
check('actual_death_notice_pending_reload_one_each', [events[n].count('eep.42') for n in names[1:3]], [1, 1])
check('actual_no_repeat_death_notice_after_ack', [events[n].count('eep.42') for n in names[3:]], [0, 0, 0])
result = {'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
          'scope': 'Controlled permanent real mother destruction with an active real seeded task; native notice pending/reload/ack, actual next-day abort and source cleanup, strict same-day state replays, actual month and direct begin refusal, native population growth separately accounted. Completion replay loop is empty after actual task removal; no claim of invoking a destroyed situation. Original delayed seed intro acknowledged separately. Not full acceptance.',
          'version': '0.2.0-rc.5', 'language': 'l_simp_chinese', 'checks': checks,
          'saves': {n: a['save_sha256'] for n, a in zip(names, audits, strict=True)}}
dest = run / 'rc5-active-task-permanent-core-death-reload-month-restart-proof.json'
assert not dest.exists()
dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks),
                  'failed': [c['check'] for c in checks if c['status'] == 'FAIL']}))
