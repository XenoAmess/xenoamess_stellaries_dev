import collections
import copy
import hashlib
import json
from pathlib import Path
import sys
import zipfile
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q
run = Path('_runtime/heart-of-devouring/runs/20261007T203412Z')
names = ['rc7-dual33-report-before-native', 'rc7-dual33-report-pending-native', 'rc7-dual33-report-reloaded-native', 'rc7-dual33-report-reloaded-acked-native', 'rc7-dual33-no-report-reloaded-native-control']
before, pending, restored, acked, control = states = [json.loads((run / (name + '.audit.json')).read_text(encoding='utf-8')) for name in names]
checks = []
def check(name, actual, expected):
    def small(value):
        data = json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')
        return value if len(data) < 1000 else {'canonical_json_sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
    checks.append({'check': name, 'status': 'PASS' if actual == expected else 'FAIL', 'actual': small(actual), 'expected': small(expected)})
display = {'eep_tasks': 0, 'eep_c_remainder': 0, 'eep_core_state': 0, 'eep_g_remainder': 2, 'eep_waiting': 0, 'eep_crisis': 0, 'eep_chunks': 18, 'eep_psi': 0}
mother_display = {'eep_actual_pop': 6594, 'eep_free_districts': 24}
def stripped(state):
    result = copy.deepcopy(state)
    for key in display:
        result['countries']['33']['variables'].pop(key, None)
    for key in mother_display:
        result['planets']['2014']['variables'].pop(key, None)
    return result
for label, left, right in [('native_direct_report', before, pending), ('native_report_ACK', restored, acked), ('report_vs_no_report_reload', control, restored)]:
    a, b = stripped(left), stripped(right)
    for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
        check(label + ':exact_full_' + key, b[key], a[key])
    check(label + ':all37_real_stocks', {key: right['countries'][key]['stockpile'] for key in right['countries']}, {key: left['countries'][key]['stockpile'] for key in left['countries']})
for label, state in [('pending', pending), ('reloaded', restored), ('acked', acked)]:
    check(label + ':exact_eight_report_fields', {key: state['countries']['33']['variables'].get(key) for key in display}, display)
    check(label + ':exact_two_core_fields', {key: state['planets']['2014']['variables'].get(key) for key in mother_display}, mother_display)
    check(label + ':only_own_true_population', [state['colonies']['0']['actual_pop_sum'], state['colonies']['10']['actual_pop_sum']], [5838, 6594])
    check(label + ':source_shattered', state['planets']['196']['planet_class'], 'pc_shattered')
    check(label + ':both_ledgers', {owner: {key: state['countries'][owner]['variables'][key] for key in ['eep_c', 'eep_g', 'eep_d', 'eep_made']} for owner in ['0', '33']}, {'0': {'eep_c': 20, 'eep_g': 0, 'eep_d': 7, 'eep_made': 0}, '33': {'eep_c': 20, 'eep_g': 20, 'eep_d': 7, 'eep_made': 300}})
def mass(state):
    amounts = collections.Counter()
    for value in state['pop_groups'].values():
        amounts[(value['planet'], value['key']['species'])] += value['size']
    return sorted((str(key), value) for key, value in amounts.items())
check('reload_every_colony_species_actual_population', mass(restored), mass(pending))
check('reload_all37_stocks', {key: restored['countries'][key]['stockpile'] for key in restored['countries']}, {key: pending['countries'][key]['stockpile'] for key in pending['countries']})
check('reload_full_actual_global_total', sum(value['size'] for value in restored['pop_groups'].values()), 38730)
raws = []
for name in [names[2], names[4]]:
    with zipfile.ZipFile(run / (name + '.sav')) as archive:
        gamestate = archive.read('gamestate').decode('utf-8-sig')
    raws.append({key: value for key, value, object_value in q.fields(q.block(gamestate, 'country')) if object_value and key != '33'})
check('reload_control_all36_other_raw_country_blocks', raws[0], raws[1])
for name, state in zip(names, states, strict=True):
    check(name + ':exact_original_native_bytes', hashlib.sha256((run / (name + '.sav')).read_bytes()).hexdigest(), state['save_sha256'])
result = {'status': 'PASS' if all(value['status'] == 'PASS' for value in checks) else 'FAIL', 'version': '0.2.0-rc.7', 'language': 'l_simp_chinese', 'scope': 'Country33 direct bound-mother report, pending original-byte reload, same-day acknowledgment, exact no-report original-byte reload control. All37 stocks and actual population kept. All native reload promotions, derived caches and budgets exactly reproduced by no-report control; no blanket exclusion. Only eight enumerated report fields and two actual mother snapshot fields differ. Original full-object reload guard FAIL and all224 delta paths retained. Other owner report/replay and full Scorched Hive acceptance remain pending.', 'saves': {name: state['save_sha256'] for name, state in zip(names, states, strict=True)}, 'checks': checks}
destination = run / 'rc7-dual33-native-report-reload-control-proof.json'
assert not destination.exists()
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'failed': [value['check'] for value in checks if value['status'] == 'FAIL']}))
