import collections
import hashlib
import json
from pathlib import Path
import sys
import zipfile
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q
run = Path('_runtime/heart-of-devouring/runs/20261007T203412Z')
names = [
    'rc7-dual-separate-system-source-starbase-prepared',
    'rc7-dual-separate-old-task13-native',
    'rc7-dual-separate-starbase-source-owner33-native',
    'rc7-dual-separate-old13-new-start-refused-native',
    'rc7-dual-separate-day1-old-task-cleaned-native',
    'rc7-dual-separate-new33-real100-seed-task0-native',
    'rc7-dual-separate-first-month-stable-owner33-native',
    'rc7-dual-separate-new33-settled-old0-isolated-native',
]
states = [json.loads((run / (name + '.audit.json')).read_text(encoding='utf-8')) for name in names]
checks = []
def compact(value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')
    return value if len(data) < 1000 else {'canonical_json_sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
def check(name, actual, expected):
    checks.append({'check': name, 'status': 'PASS' if actual == expected else 'FAIL', 'actual': compact(actual), 'expected': compact(expected)})
def ledger(state, owner):
    return {key: state['countries'][str(owner)]['variables'][key] for key in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']}
def active(state):
    return [value for value in state['situations'].values() if value['type'] == 'situation_eep_devouring' and value.get('killed') != 'yes' and value['target']['id'] == 196]
def source_species(state):
    counter = collections.Counter()
    for value in state['pop_groups'].values():
        if value['planet'] == 19:
            counter[str(value['key']['species'])] += value['size']
    return dict(counter)
for index, (name, state) in enumerate(zip(names, states, strict=True)):
    check(name + ':exact_native_bytes', hashlib.sha256((run / (name + '.sav')).read_bytes()).hexdigest(), state['save_sha256'])
    targets = {target['name']: target['id'] for target in state['event_targets']}
    for key, expected in [('eep_core0', 8), ('eep_core33', 2014), ('eep_core_actor8', 0), ('eep_core_actor2014', 33), ('eep_rc7_transfer_source', 196), ('eep_rc7_transfer_system', 154), ('eep_rc7_transfer_starbase', 22)]:
        check(name + ':binding:' + key, targets.get(key), expected)
    check(name + ':mother_owners', [state['planets'][key]['owner'] for key in ['8', '2014']], [0, 33])
    check(name + ':old_ledger', ledger(state, 0), {'eep_c': 20, 'eep_g': 0, 'eep_d': 7, 'eep_made': 0, 'eep_worlds': 1})
    expected = {'eep_c': 20, 'eep_g': 20, 'eep_d': 7, 'eep_made': 300, 'eep_worlds': 1} if index == 7 else {'eep_c': 0, 'eep_g': 0, 'eep_d': 2, 'eep_made': 0, 'eep_worlds': 0}
    check(name + ':new_ledger', ledger(state, 33), expected)
    if index < 7:
        check(name + ':source_actual_owner_controller', [state['planets']['196']['owner'], state['planets']['196']['controller']], [0, 0] if index < 2 else [33, 33])
        check(name + ':frozen_Q_T', [state['planets']['196']['variables'][key] for key in ['eep_q', 'eep_months']], [20, 48])
    expected_tasks = [] if index in [4, 7] else [(0 if index < 4 else 33, 0 if index in [0, 5] else 1 if index == 6 else 13)]
    check(name + ':actual_active_task_owner_progress', [(task['country'], task['progress']) for task in active(state)], expected_tasks)
for label, left, right in [('controlled13', 0, 1), ('transfer', 1, 2), ('old_active_refusal', 2, 3), ('formal_seed', 4, 5), ('new_settlement', 6, 7)]:
    before, after = states[left], states[right]
    check(label + ':both_all_stocks', {key: after['countries'][key]['stockpile'] for key in ['0', '33']}, {key: before['countries'][key]['stockpile'] for key in ['0', '33']})
    foreign = [key for key in before['countries'] if key not in ['0', '33']]
    check(label + ':all35_other_countries', {key: after['countries'][key] for key in foreign}, {key: before['countries'][key] for key in foreign})
    check(label + ':old_mother_actual_population', after['colonies']['0']['actual_pop_sum'], before['colonies']['0']['actual_pop_sum'])
check('new_seed_actual_species', source_species(states[5]), {'48': 100, '44': 100})
check('seed_only100_from_new_core', states[5]['colonies']['10']['actual_pop_sum'], states[4]['colonies']['10']['actual_pop_sum'] - 100)
check('seed_global_actual_total_unchanged', sum(value['size'] for value in states[5]['pop_groups'].values()), sum(value['size'] for value in states[4]['pop_groups'].values()))
check('month_actual_date', [states[5]['date'], states[6]['date']], ['2204.02.03', '2204.03.01'])
check('month_only_actual_new_founder', source_species(states[6]), {'44': 100})
check('source_physically_shattered', states[7]['planets']['196']['planet_class'], 'pc_shattered')
check('new_core_actual_return100_and_create300', states[7]['colonies']['10']['actual_pop_sum'], states[6]['colonies']['10']['actual_pop_sum'] + 400)
check('manufacture_global_only300', sum(value['size'] for value in states[7]['pop_groups'].values()), sum(value['size'] for value in states[6]['pop_groups'].values()) + 300)
check('old_country_all_variables_isolated', states[7]['countries']['0']['variables'], states[6]['countries']['0']['variables'])
check('actual_new_capacity7', states[7]['planets']['2014']['variables']['eep_capacity_value'], 7)
check('actual_old_capacity7', states[7]['planets']['8']['variables']['eep_capacity_value'], 7)
raws = []
for name in [names[6], names[7]]:
    with zipfile.ZipFile(run / (name + '.sav')) as archive:
        gamestate = archive.read('gamestate').decode('utf-8-sig')
    raws.append({key: value for key, value, is_object in q.fields(q.block(gamestate, 'country')) if is_object and key not in ['0', '33']})
check('settlement_all35_foreign_raw_country_blocks', raws[1], raws[0])
result = {'status': 'PASS' if all(value['status'] == 'PASS' for value in checks) else 'FAIL', 'version': '0.2.0-rc.7', 'language': 'l_simp_chinese', 'scope': 'Controlled qualified second-owner33 and independent cores8/2014. Independent unowned system154/source196/outpost22 transfer, old13 rejection, actual day cleanup, new zero-founder real100 migration, actual28-day stable first month, CONTROL endpoint48 and real production settlement. No free seed/population/stocks. Controlled outpost/source and progress are not natural economy or complete Purifier acceptance. Earlier same-system native reannexation remains retained. Final purge waiting and Queen report/reload are separate pending proofs.', 'saves': {name: state['save_sha256'] for name, state in zip(names, states, strict=True)}, 'checks': checks}
destination = run / 'rc7-dual-owner-separate-system-settlement-proof.json'
assert not destination.exists()
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'failed': [value['check'] for value in checks if value['status'] == 'FAIL']}))
