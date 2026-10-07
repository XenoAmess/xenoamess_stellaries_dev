import copy
import hashlib
import json
from pathlib import Path
import sys
import zipfile
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q
run = Path('_runtime/heart-of-devouring/runs/20261007T203412Z')
names = ['rc7-dual0-report-before-native', 'rc7-dual0-report-pending-native', 'rc7-dual0-report-acked-native', 'rc7-dual33-before-five-replays-native', 'rc7-dual-both-after-five-replays-native', 'rc7-dual33-first-notice-acked-native', 'rc7-dual-both-after-ack-five-again-native']
states = [json.loads((run / (name + '.audit.json')).read_text(encoding='utf-8')) for name in names]
checks = []
raws = []
events = []
def check(name, actual, expected):
    def small(value):
        data = json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')
        return value if len(data) < 1000 else {'canonical_json_sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    checks.append({'check': name, 'status': 'PASS' if actual == expected else 'FAIL', 'actual': small(actual), 'expected': small(expected)})
for name, state in zip(names, states, strict=True):
    raw = (run / (name + '.sav')).read_bytes()
    check(name + ':exact_native_bytes', hashlib.sha256(raw).hexdigest(), state['save_sha256'])
    with zipfile.ZipFile(run / (name + '.sav')) as archive:
        gamestate = archive.read('gamestate').decode('utf-8-sig')
    roots = list(q.fields(gamestate))
    raws.append({key: value for key, value, obj in q.fields(q.block(gamestate, 'country')) if obj})
    events.append([q.scalars(value).get('event') for key, value, obj in roots if obj and key == 'player_event'])
    check(name + ':two_distinct_cores', {value['name']: value['id'] for value in state['event_targets'] if value['name'] in ['eep_core0', 'eep_core33']}, {'eep_core0': 8, 'eep_core33': 2014})
    check(name + ':two_real_populations', [state['colonies']['0']['actual_pop_sum'], state['colonies']['10']['actual_pop_sum']], [5838, 6594])
    check(name + ':both_ledger_economics', {owner: {key: state['countries'][owner]['variables'][key] for key in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']} for owner in ['0', '33']}, {'0': {'eep_c': 20, 'eep_g': 0, 'eep_d': 7, 'eep_made': 0, 'eep_worlds': 1}, '33': {'eep_c': 20, 'eep_g': 20, 'eep_d': 7, 'eep_made': 300, 'eep_worlds': 1}})
for label, left, right in [('old0_report', 0, 1), ('old0_ACK', 1, 2), ('player33_switch', 2, 3), ('both_first_five', 3, 4), ('new33_notice_ACK', 4, 5), ('both_second_five', 5, 6)]:
    before, after = states[left], states[right]
    for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets']:
        check(label + ':full_' + key, after[key], before[key])
    check(label + ':all37_stocks', {owner: value['stockpile'] for owner, value in after['countries'].items()}, {owner: value['stockpile'] for owner, value in before['countries'].items()})
    if label != 'both_first_five':
        check(label + ':all37_countries', after['countries'], before['countries'])
        check(label + ':all37_raw_country_blocks', raws[right], raws[left])
    if label not in ['old0_report', 'both_first_five']:
        check(label + ':all_physical_planets', after['planets'], before['planets'])
check('old0_report_exact_fresh_actual_snapshot', {key: states[1]['planets']['8']['variables'][key] for key in ['eep_actual_pop', 'eep_free_districts']}, {'eep_actual_pop': 5838, 'eep_free_districts': 12})
a, b = [copy.deepcopy(state['planets']) for state in states[:2]]
for key in ['eep_actual_pop', 'eep_free_districts']:
    a['8']['variables'].pop(key)
    b['8']['variables'].pop(key)
check('old0_report_all_other_physical_fields', b, a)
check('first_five_all36_other_countries', {key: states[4]['countries'][key] for key in states[4]['countries'] if key != '33'}, {key: states[3]['countries'][key] for key in states[3]['countries'] if key != '33'})
check('first_five_all36_other_raw_blocks', {key: raws[4][key] for key in raws[4] if key != '33'}, {key: raws[3][key] for key in raws[3] if key != '33'})
a, b = [copy.deepcopy(state['countries']['33']) for state in states[3:5]]
display = {'eep_tasks': 0, 'eep_c_remainder': 0, 'eep_core_state': 0, 'eep_g_remainder': 2, 'eep_waiting': 0, 'eep_crisis': 0, 'eep_chunks': 18, 'eep_psi': 0}
for key, value in display.items():
    check('first_five_exact_new_display:' + key, [a['variables'].pop(key, None), b['variables'].pop(key, None)], [None, value])
check('first_five_only_stage_receipt', [a['variables'].pop('eep_stage'), b['variables'].pop('eep_stage')], [0, 1])
check('first_five_notice_consumed', [a['flags'].pop('eep_notice_pending'), 'eep_notice_pending' in b['flags']], [62844000, False])
check('first_five_one_new_notice_receipt', ['eep_first_notice' in a['flags'], b['flags'].pop('eep_first_notice')], [False, 62844000])
check('first_five_all_other_new33_country_fields', b, a)
a, b = [copy.deepcopy(state['planets']) for state in states[3:5]]
for key, value in [('eep_actual_pop', 6594), ('eep_free_districts', 24)]:
    check('first_five_exact_core_snapshot:' + key, [a['2014']['variables'].pop(key, None), b['2014']['variables'].pop(key, None)], [None, value])
check('first_five_all_other_physical_fields', b, a)
check('old_report_one_window_then_ACK', [events[1].count('eep.100'), events[2].count('eep.100')], [1, 0])
check('new_notice_zero_one_ACK_zero_repeat_zero', [events[index].count('eep.11') for index in [3, 4, 5, 6]], [0, 1, 0, 0])
result = {'status': 'PASS' if all(value['status'] == 'PASS' for value in checks) else 'FAIL', 'version': '0.2.0-rc.7', 'language': 'l_simp_chinese', 'scope': 'Two independent real bound-mother GUI reports and qualified second owner33 notice. Old0 report C20/G0/made0/pop5838, new33 C20/G20/made300/pop6594; new33 pending report load separately proven by exact no-report control. Five monthly calls to each owner, one real player33 first notice, same-day ACK, five calls each again. All37 stocks/population/jobs/districts/tasks and all other raw country blocks strictly conserved, only exact new33 display/message receipts recorded. Controlled owner case, not complete Purifier route or full Scorched Hive acceptance.', 'saves': {name: state['save_sha256'] for name, state in zip(names, states, strict=True)}, 'events': {name: value for name, value in zip(names, events, strict=True)}, 'checks': checks}
out = run / 'rc7-dual-core-reports-notice-ten-callbacks-proof.json'
assert not out.exists()
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'failed': [value['check'] for value in checks if value['status'] == 'FAIL']}))
