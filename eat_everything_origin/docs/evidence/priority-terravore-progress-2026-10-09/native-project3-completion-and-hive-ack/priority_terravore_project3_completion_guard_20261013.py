"""Prove native project3 completion and the still-pending crisis.4130 boundary."""
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state, omit

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = 'terravore-post-second-society-month-22880901'
after = 'terravore-project3-completion-22880902'
load = lambda name: json.loads((run / name).read_text('utf-8-sig'))
b, a = [read_state(run, stage) for stage in (before, after)]
ba, aa = b['audit'], a['audit']
bc, ac = [s['countries']['0'] for s in (ba, aa)]
prior = load(before + '-post-second-society-month-v4-proof.json')
review = load(before + '-project3-completion-review.json')
calendar = load(after + '-calendar-receipt.json')
observe = load(after + '-construction-boundary-observation-v4.json')
executions = [load(stage + '-execution.json') for stage in
    (before + '-post-second-society-month-guard-v4',
     before + '-project3-completion-review', after + '-calendar', after + '-boundary-observation-v4')]

def events(state):
    return [(q.scalars(value).get('id'), value) for key, value, obj in
            q.fields(q.block(state['country'], 'events'))
            if key == 'special_project' and obj]

def flags(state):
    return {key: q.scalars(value) if obj else q.unquote(value) for key, value, obj
            in q.fields(q.block(state['country'], 'flags'))}

before_projects, after_projects = events(b), events(a)
old_project = dict(before_projects)[9]
new_project = dict(after_projects)[9]
other_projects = [(pid, raw) for pid, raw in before_projects if pid != 9]
other_after = [(pid, raw) for pid, raw in after_projects if pid != 9]
old_flags, new_flags = flags(b), flags(a)
expected_flags = {key: dict(value, flag_days=value['flag_days'] - 1)
                  if isinstance(value, dict) and 'flag_days' in value else value
                  for key, value in old_flags.items()}
income = lambda country, resource: sum(
    (D(str(group.get(resource, 0))) for group in
     country['budget_categories']['current_month']['income'].values()), D(0))
cash = ('energy', 'minerals', 'food', 'alloys', 'unity', 'rare_crystals', 'influence', 'trade', 'menace')
head = q.scalars(a['items']['117440553'])
ids = q.ids(q.block(a['queues']['0'], 'items'))
news = [q.scalars(raw) for raw in observe['new_country0_messages_raw']]
pending = [q.scalars(raw) for raw in a['pending']]
ship_identity = len(b['ships']) == len(a['ships']) == 75 and set(b['ships']) == set(a['ships'])
for sid, old in b['ships'].items():
    new = a['ships'].get(sid, '')
    o, n = q.scalars(old), q.scalars(new)
    ship_identity = ship_identity and q.block(old, 'ship_design_implementation') == q.block(new, 'ship_design_implementation')
    ship_identity = ship_identity and q.block(old, 'name') == q.block(new, 'name')
    ship_identity = ship_identity and all(o.get(k) == n.get(k) for k in
        ('construction_date', 'killed', 'max_hitpoints', 'max_armor_hitpoints',
         'max_shield_hitpoints', 'hitpoints', 'armor_hitpoints', 'shield_hitpoints', 'leader'))

checks = {
    'prior18PASS_review7PASS_calendar_observe6PASS_actual0_original_SAVs':
        prior['status'].startswith('PASS') and len(prior['checks']) == 18
        and review['status'] == 'PASS_REVIEWED_NATIVE_BOUNDARY' and len(review['checks']) == 7
        and calendar['status'] == 'CALENDAR_CONFIRMED' and calendar['days'] == 1
        and observe['status'] == 'OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY'
        and len(observe['checks']) == 6
        and all(all(value is True for value in proof['checks'].values())
                for proof in (prior, review, observe))
        and all(x['returncode'] == 0 and x['helper_sha256'] == h.sha256(Path(x['command'][1]))
                for x in executions)
        and prior['after_sha256'] == review['after_sha256'] == ba['save_sha256'] == h.sha256(run / (before + '.sav'))
        and observe['after_sha256'] == aa['save_sha256'] == h.sha256(run / (after + '.sav')),
    'one_native_day_exact_project9_completed_only_society_queue_removed':
        ba['date'] == '2288.09.01' and aa['date'] == '2288.09.02'
        and q.scalars(old_project).get('status') == 'in_progress'
        and q.scalars(new_project).get('status') == 'completed'
        and q.scalars(new_project).get('special_project') == 'CRISIS_SPECIAL_PROJECT_PSIONIC_3'
        and omit(old_project, {'status'}) == omit(new_project, {'status'})
        and other_projects == other_after
        and 'society_queue' in bc['research_queues']
        and 'society_queue' not in ac['research_queues']
        and omit(q.block(b['country'], 'tech_status'), {'stored_techpoints', 'society_queue'})
            == omit(q.block(a['country'], 'tech_status'), {'stored_techpoints', 'society_queue'})
        and omit(q.block(b['country'], 'events'), {'special_project'})
            == omit(q.block(a['country'], 'events'), {'special_project'}),
    'one_true_research_tick_society_draw_physics_engineering_bank_exact':
        D(str(bc['research_stockpile']['society_research'])) - D(str(ac['research_stockpile']['society_research']))
            == income(bc, 'society_research') == D('132.8122')
        and all(abs(D(str(ac['research_stockpile'][resource]))
                    - D(str(bc['research_stockpile'][resource]))
                    - income(bc, resource) * D('1.35')) < D('.00005')
                for resource in ('physics_research', 'engineering_research')),
    'project3_complete_flag_only_new_two_country_timers_minus1':
        new_flags == dict(expected_flags, crisis_special_project_3_complete=63574104)
        and bc['variables'] == ac['variables']
        and q.block(b['country'], 'crisis_progression') == q.block(a['country'], 'crisis_progression')
        and ac['variables']['eep_crisis'] == 3 and ac['variables']['eep_stage'] == 2
        and ac['effective_stockpile']['menace'] == 3065,
    'only_crisis4130_pending_ID305_and_one_formal_CN_event_message':
        not b['pending'] and pending == [{'id': 305, 'event': 'crisis.4130',
                                          'date': '2290.12.02', 'country': 0}]
        and len(news) == 1 and news[0].get('type') == 'EVENT_MESSAGE_TYPE'
        and news[0].get('event') == 305 and news[0].get('receiver') == 0
        and news[0].get('date') == '2288.09.02' and '异界注能' in news[0].get('text', ''),
    'mother_paid_hive_one_day_plus1point4_all_jobs_and_assets_held':
        ids == q.ids(q.block(b['queues']['0'], 'items')) == [117440553, 1476395019, 117440546]
        and D(str(head['progress'])) - D(str(q.scalars(b['items']['117440553'])['progress'])) == D('1.4')
        and all(a['items'][str(i)] == b['items'][str(i)] for i in ids[1:])
        and ba['colonies']['0']['actual_pop_sum'] == aa['colonies']['0']['actual_pop_sum'] == 13069
        and ba['districts']['1'] == aa['districts']['1']
        and all(ba['pop_jobs'][str(i)] == aa['pop_jobs'][str(i)] for i in (23, 24, 25))
        and len(a['fleets']) == len(b['fleets']) == 35 and set(a['fleets']) == set(b['fleets'])
        and all(q.ids(q.block(fleet, 'ships')) == q.ids(q.block(a['fleets'][fid], 'ships'))
                for fid, fleet in b['fleets'].items())
        and ship_identity
        and q.ids(q.block(b['country'], 'owned_armies')) == q.ids(q.block(a['country'], 'owned_armies')),
    'cash_war_truce_error_and_production_unchanged':
        all(bc['effective_stockpile'][key] == ac['effective_stockpile'][key] for key in cash)
        and b['roots']['war'] == a['roots']['war'] and b['roots']['truce'] == a['roots']['truce']
        and (run / (before + '-error-after.log')).read_bytes()
            == (run / (after + '-error-after.log')).read_bytes()
        and meta['language'] == 'l_simp_chinese'
        and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed = all(value is True for value in checks.values())
out = run / (after + '-project3-completion-proof.json')
assert not out.exists()
h.write_json(out, {
    'status': 'PASS_NATIVE_PROJECT3_COMPLETED_EVENT_PENDING' if passed else 'FAIL',
    'checks': checks, 'before_sha256': ba['save_sha256'], 'after_sha256': aa['save_sha256'],
    'date': aa['date'], 'project_id': 9, 'pending_event_id': 305,
    'boundaries': ['crisis4130_hive_option_ack_review'],
    'native_devour_calendar_ready': False, 'maximum_days_to_native_bite_boundary': 0,
    'scope': 'Project3 research complete with crisis.4130 pending; crisis level4 and Queen stage3 unaccepted.',
})
print(json.dumps({'status': 'PASS' if passed else 'FAIL', 'checks': len(checks),
                  'failed': [key for key, value in checks.items() if value is not True],
                  'date': aa['date'], 'project': q.scalars(new_project).get('status'),
                  'pending': pending}), flush=True)
assert passed
