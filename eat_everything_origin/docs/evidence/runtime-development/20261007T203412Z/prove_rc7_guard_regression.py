import hashlib
import json
from pathlib import Path

run = Path(__file__).parent
checks = []
def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})
def load(name):
    state = json.loads((run / (name + '.audit.json')).read_text(encoding='utf-8'))
    check(name + ' actual bytes match audit', hashlib.sha256((run / (name + '.sav')).read_bytes()).hexdigest() == state['save_sha256'])
    return state
start = load('rc7-paired-tasks50-start')
end = load('rc7-paired-tasks50-year-complete')
half = load('rc7-seed50-native-precondition')
filled = load('rc7-seed50-formal-start-refilled-only50')
old = load('rc7-old-damage6-native-before-restart')
restarted = load('rc7-old-damage6-native-restarted-q14-t34')
for state, progress in ((start, 0), (end, 12)):
    tasks = [value for value in state['situations'].values() if value['type'] == 'situation_eep_devouring']
    check('50 tasks actual progress' + str(progress), len(tasks) == 50 and all(value['progress'] == progress for value in tasks))
    for value in tasks:
        source = state['planets'][str(value['target']['id'])]
        check('source' + str(value['target']['id']) + ' Q20T48 at' + str(progress), source['variables']['eep_q'] == 20 and source['variables']['eep_months'] == 48)
    check('no premature credit at' + str(progress), all(state['countries']['0']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)]))
check('actual one year', start['date'] == '2200.01.01' and end['date'] == '2201.01.01')
source = str(next(value['id'] for value in half['event_targets'] if value['name'] == 'eep_rc7_seed_case'))
colony = str(half['planets'][source]['colony'])
check('actual partial seed50 to100', half['colonies'][colony]['actual_pop_sum'] == 50 and filled['colonies'][colony]['actual_pop_sum'] == 100)
check('mother actual50 cost only', half['colonies']['0']['actual_pop_sum'] == 750 and filled['colonies']['0']['actual_pop_sum'] == 700)
check('same actual total5700', sum(value['size'] for value in half['pop_groups'].values()) == sum(value['size'] for value in filled['pop_groups'].values()) == 5700)
check('seed50 no stockpile or premature credit', half['countries']['0']['stockpile'] == filled['countries']['0']['stockpile'] and all(filled['countries']['0']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)]))
check('partial seed actualQ20T48', filled['planets'][source]['variables']['eep_q'] == 20 and filled['planets'][source]['variables']['eep_months'] == 48)
check('six actual old damaged deposits', len([value for value in old['deposits'].values() if value['type'] == 'd_lithoid_devastation' and value['deposit_holder']['id'] == 3]) == 6)
check('actual old damage q14 t34', restarted['planets']['3']['variables']['eep_q'] == 14 and restarted['planets']['3']['variables']['eep_months'] == 34)
check('old restart no stockpile/population creation', old['countries']['0']['stockpile'] == restarted['countries']['0']['stockpile'] and sum(value['size'] for value in old['pop_groups'].values()) == sum(value['size'] for value in restarted['pop_groups'].values()))
check('old restart no credit', all(restarted['countries']['0']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)]))
measurement = json.loads((run / 'rc7-paired-tasks50-measurement.json').read_text(encoding='utf-8'))
check('measurement binds exact original/endpoint', measurement['common_mod_zero_sha256'] == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5' and measurement['end_save_sha256'] == end['save_sha256'])
manifest = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
log = Path(manifest['userdir']) / 'logs/error.log'
raw = log.read_bytes()
snapshot = run / 'rc7-zero-query-guard-stage-error.log'
assert not snapshot.exists()
snapshot.write_bytes(raw)
check('complete error snapshot contains no unset EEP read', not any('Variable eep_' in line and 'is not set' in line for line in raw.decode('utf-8-sig').splitlines()))
report = {'status': 'PASS' if all(value['passed'] for value in checks) else 'FAIL', 'version': '0.2.0-rc.7',
          'scope': 'Zero old damage existing100 seed50-task year, actual50 refill, positive old damage6 restart and complete current-stage error log. Zero founder/new qualified owner and full Scorched Hive acceptance remain pending.',
          'checks_passed': sum(value['passed'] for value in checks), 'checks_total': len(checks), 'checks': checks,
          'mod_tree_sha256': manifest['copied_mod_tree_sha256'], 'measurement': measurement['samples'][-1],
          'error_snapshot_sha256': hashlib.sha256(raw).hexdigest(), 'error_snapshot_bytes': len(raw)}
destination = run / 'rc7-zero-query-guard-partial-proof.json'
assert not destination.exists()
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in report.items() if key != 'checks'}))
assert report['status'] == 'PASS', [value for value in checks if not value['passed']]
