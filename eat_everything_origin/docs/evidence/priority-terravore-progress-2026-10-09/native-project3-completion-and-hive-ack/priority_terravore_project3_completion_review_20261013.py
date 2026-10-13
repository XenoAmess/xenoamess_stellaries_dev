"""Review exactly one native day before psionic crisis project 3 completes."""
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
before = 'terravore-post-second-society-month-22880901'
end = '2288.09.02'
prior_file = before + '-post-second-society-month-v4-proof.json'
prior_stage = before + '-post-second-society-month-guard-v4'
s = read_state(run, before)
a = s['audit']
c = a['countries']['0']
prior = json.loads((run / prior_file).read_text('utf-8'))
execution = json.loads((run / (prior_stage + '-execution.json')).read_text('utf-8'))
special_path = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/special_projects/00_projects_nemesis.txt')
event_path = Path('C:/SteamLibrary/steamapps/common/Stellaris/events/nemesis_crisis_events.txt')
special = special_path.read_text('utf-8-sig')
event = event_path.read_text('utf-8-sig')
native_project = next((value for key, value, obj in q.fields(special)
                       if key == 'special_project' and obj
                       and q.scalars(value).get('key') == 'CRISIS_SPECIAL_PROJECT_PSIONIC_3'), '')
native_event = next((value for key, value, obj in q.fields(event)
                     if key == 'country_event' and obj
                     and q.scalars(value).get('id') == 'crisis.4130'), '')
project = next((value for key, value, obj in q.fields(q.block(s['country'], 'events'))
                if key == 'special_project' and obj and q.scalars(value).get('id') == 9), '')
raw_queue = c['research_queues']['society_queue']
tokens = list(q.tokens(raw_queue))
queue = q.scalars(raw_queue[tokens[0][2]:tokens[-1][1]])
income = sum((D(str(group.get('society_research', 0)))
              for group in c['budget_categories']['current_month']['income'].values()), D(0))
progress = D(str(queue['progress']))
bank = D(str(c['research_stockpile']['society_research']))
expected_tick = income * D('1.35') + min(income, bank)
front_ids = q.ids(q.block(s['queues']['0'], 'items'))
head = q.scalars(s['items'][str(front_ids[0])])
delays = [value for key, value, obj in q.fields(
    q.block(q.block(s['country'], 'modules'), 'standard_event_module'))
    if key == 'delayed_event' and obj]
checks = {
    'prior_month_18PASS_actual0_same_original_SAV':
        prior['status'].startswith('PASS') and len(prior['checks']) == 18
        and all(value is True for value in prior['checks'].values())
        and execution['returncode'] == 0
        and execution['helper_sha256'] == h.sha256(Path(execution['command'][1]))
        and prior['after_sha256'] == a['save_sha256'] == h.sha256(run / (before + '.sav')),
    'single_native_day_Sep1_to_Sep2_original_project9_in_progress':
        a['date'] == '2288.09.01' and end == '2288.09.02'
        and q.scalars(project).get('special_project') == 'CRISIS_SPECIAL_PROJECT_PSIONIC_3'
        and q.scalars(project).get('status') == 'in_progress'
        and queue['special_project'] == 9,
    'genuine_society_tick_crosses12000_bank_and_hive_under480':
        q.scalars(native_project).get('cost') == 12000
        and progress == D('11814.65809') and income == D('132.8122')
        and bank == D('5783.999') and progress < 12000 < progress + expected_tick
        and front_ids == [117440553, 1476395019, 117440546]
        and head['progress'] == 337.4 and D(str(head['progress'])) + D('1.4') < 480,
    'installed_vanilla_project_success_sets_flag_and_calls_crisis4130_hive_option':
        'set_country_flag = crisis_special_project_3_complete' in q.block(native_project, 'on_success')
        and 'country_event = { id = crisis.4130 }' in q.block(native_project, 'on_success')
        and 'name = crisis.4130.hive.a' in native_event
        and 'is_hive_empire = yes' in native_event,
    'crisis3_queen2_no_complete_flag_or_pending_before_day2':
        [q.unquote(value) for key, value, obj in q.fields(q.block(s['country'], 'crisis_progression'))
         if key == 'level' and not obj] == ['crisis_level_1', 'crisis_level_2', 'crisis_level_3']
        and c['variables']['eep_stage'] == 2 and c['variables']['eep_crisis'] == 3
        and c['effective_stockpile']['menace'] == 3065
        and 'crisis_special_project_3_complete' not in q.scalars(q.block(s['country'], 'flags'))
        and not s['pending'],
    'normal_paid_mother_75ships35fleets15armies_no_combat_delays':
        a['districts']['1']['level'] == 8
        and [a['pop_jobs'][str(i)]['workforce'] for i in (23, 24, 25)] == [360, 2280, 360]
        and len(s['ships']) == 75 and len(s['fleets']) == 35
        and len(q.ids(q.block(s['country'], 'owned_armies'))) == 15
        and not delays
        and all(not q.ids(q.block(q.block(fleet, 'combat'), 'in_combat_with'))
                for fleet in s['fleets'].values()),
    'simplified_CN_same_production41_and_unfiltered_error':
        meta['language'] == 'l_simp_chinese' and meta['version'] == '0.2.0'
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
        and (user / 'logs/error.log').read_bytes() == (run / (before + '-error-after.log')).read_bytes(),
}
passed = all(value is True for value in checks.values())
stage = before + '-project3-completion-review'
out = run / (stage + '.json')
assert not out.exists()
h.write_json(out, {
    'status': 'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL',
    'checks': checks, 'before_sha256': a['save_sha256'], 'after_sha256': a['save_sha256'],
    'start_date': a['date'], 'end_date': end, 'days': 1, 'maximum_days': 1,
    'allowed_boundaries': prior['boundaries'], 'execution_stage': stage,
    'expected_project_tick_if_budget_unchanged': str(expected_tick),
    'installed_vanilla_source_sha256': {str(path): h.sha256(path)
                                        for path in (special_path, event_path)},
    'scope': 'Only one native day to first project3 completion and crisis.4130 observation.',
})
print(json.dumps({'status': 'PASS' if passed else 'FAIL', 'checks': len(checks),
                  'failed': [key for key, value in checks.items() if value is not True],
                  'date': a['date'], 'end': end, 'progress': str(progress),
                  'expected_tick': str(expected_tick)}), flush=True)
assert passed
