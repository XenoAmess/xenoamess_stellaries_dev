import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path(__file__).parent
native = run.parent / '20261007T184149Z'
checks = []

def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})

def load(folder, name):
    path = folder / (name + '.sav')
    with zipfile.ZipFile(path) as archive:
        raw = archive.read('gamestate').decode('utf-8-sig')
    identities = [int(key) for key, value, obj in q.fields(q.block(raw, 'country')) if obj]
    result = q.audit(path, identities)
    destination = run / (name + '.all-countries.audit.json')
    assert not destination.exists()
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result

frozen = load(native, 'vanilla-shared-world-frozen50-unstarted')
zero = load(run, 'rc6-paired-mod-zero-frozen')
sources = {key: value for key, value in frozen['planets'].items() if 'perf_constructed' in value['flags']}
check('true native frozen exact hash', frozen['save_sha256'] == '962b7ab20132e76ec41bbe87120db2ece05f7252823634db017d94420512588f')
check('mod zero exact hash', zero['save_sha256'] == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5')
check('same actual42 countries', len(frozen['countries']) == len(zero['countries']) == 42 and frozen['countries'].keys() == zero['countries'].keys())
check('same original stocks', frozen['countries']['0']['stockpile'] == zero['countries']['0']['stockpile'])
check('50 actual existing sources', len(sources) == 50)
baseline = json.loads((native / 'vanilla-shared-world-native-year-retry-measurement.json').read_text(encoding='utf-8'))
sample = baseline['samples'][-1]
rows = [{'mode': 'true_no_mod', 'tasks': 0, 'wall_seconds': sample['elapsed_wall_seconds'],
         'user_cpu_seconds': sample['cpu_user_seconds'], 'system_cpu_seconds': sample['cpu_system_seconds'],
         'start_save_bytes': (native / 'vanilla-shared-world-frozen-restored-retry.sav').stat().st_size,
         'end_save_bytes': (native / 'vanilla-shared-world-native-year-retry-complete.sav').stat().st_size}]
for count in (0, 1, 10, 50):
    prefix = 'rc6-paired-tasks' + str(count)
    receipt = json.loads((run / (prefix + '-measurement.json')).read_text(encoding='utf-8'))
    restored = json.loads((run / (prefix + '-restore-exact-zero.load.json')).read_text(encoding='utf-8'))
    start = load(run, prefix + '-start')
    end = load(run, prefix + '-year-complete')
    check(prefix + ' exact common source restored', restored['source_sha256'] == zero['save_sha256'])
    check(prefix + ' receipt binds native saves', receipt['start_save_sha256'] == start['save_sha256'] and receipt['end_save_sha256'] == end['save_sha256'])
    check(prefix + ' date360 verified', receipt['status'] == 'MEASURED_NATIVE_DATE_AND_TASKS_VERIFIED' and start['date'] == '2200.01.01' and end['date'] == '2201.01.01')
    check(prefix + ' same country cohort', start['countries'].keys() == end['countries'].keys() == frozen['countries'].keys())
    check(prefix + ' same actual start stocks and total5700', start['countries']['0']['stockpile'] == frozen['countries']['0']['stockpile'] and start['countries']['0']['native']['num_sapient_pops'] == 5700)
    check(prefix + ' mother700 size20', start['colonies']['0']['actual_pop_sum'] == 700 and start['planets']['3']['planet_size'] == 20)
    active = {key: value for key, value in start['planets'].items() if 'eep_active' in value['flags']}
    check(prefix + ' exact actual task sources', len(active) == count and sorted(active) == receipt['active_source_ids'])
    for key, original in sources.items():
        value = start['planets'][key]
        check(prefix + ' source' + key + ' same real asset and100 seed',
              all(value[field] == original[field] for field in ('planet_size', 'planet_class', 'owner', 'colony'))
              and start['colonies'][str(value['colony'])]['actual_pop_sum'] == 100)
    for state, progress in ((start, 0), (end, 12)):
        tasks = [value for value in state['situations'].values() if value['type'] == 'situation_eep_devouring']
        check(prefix + ' exact count/progress' + str(progress), len(tasks) == count and all(value['progress'] == progress for value in tasks))
        check(prefix + ' no premature economy at progress' + str(progress), all(state['countries']['0']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_made', 0), ('eep_d', 2)]))
        for key in active:
            value = state['planets'][key]
            check(prefix + ' source' + key + ' fixedQ20T48 at' + str(progress), value['variables']['eep_q'] == 20 and value['variables']['eep_months'] == 48)
    sample = receipt['samples'][-1]
    check(prefix + ' actual completed positive wall/CPU', sample['completed'] is True and sample['elapsed_wall_seconds'] > 0 and sample['cpu_user_seconds'] > 0)
    rows.append({'mode': 'mod', 'tasks': count, 'wall_seconds': sample['elapsed_wall_seconds'],
                 'user_cpu_seconds': sample['cpu_user_seconds'], 'system_cpu_seconds': sample['cpu_system_seconds'],
                 'start_save_bytes': receipt['start_save_bytes'], 'end_save_bytes': receipt['end_save_bytes'],
                 'end_gamestate_bytes': receipt['end_gamestate_bytes'], 'active_source_ids': sorted(active)})
report = {'status': 'PASS' if all(row['passed'] for row in checks) else 'FAIL',
          'scope': 'Same frozen actual42-country/50-source world, true no-Mod and mod0/1/10/50, one actual360-day sample each. Decision conflict and overall Scorched Hive acceptance remain pending.',
          'checks_passed': sum(row['passed'] for row in checks), 'checks_total': len(checks), 'checks': checks,
          'measurements': rows,
          'limitations': ['Single sample per branch; no statistical performance claim.',
                          'Wall sampling includes physical Enter/GPU/OCR polling, excludes native saving.',
                          'Controlled50 colony construction/actual population transfer; not natural economy evidence.',
                          'Actual native deficits, calendar growth, and random outcomes retained.',
                          'One/ten source selections differ after native reload; identical50 source assets, not nested subsets or fixed RNG.',
                          'Native derived cache empire_size recalculation is recorded separately.',
                          'No conclusion of zero script cost from comparable coarse wall measurements.']}
destination = run / 'rc6-shared-world-performance-proof.json'
assert not destination.exists()
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in report.items() if key != 'checks'}), flush=True)
assert report['status'] == 'PASS', [row for row in checks if not row['passed']]
