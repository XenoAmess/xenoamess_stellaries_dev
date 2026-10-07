import hashlib
import json
from pathlib import Path

run = Path(__file__).parent
prefix = 'conflict-eep-first'
before, start, end = [json.loads((run / (prefix + '-' + suffix + '.audit.json')).read_text(encoding='utf-8')) for suffix in ('restored', 'native-ui-start', 'native-first-month')]
original = json.loads((run / (prefix + '-route-proof.json')).read_text(encoding='utf-8'))
assert original['status'] == 'FAIL'
assert [value['check'] for value in original['checks'] if not value['passed']] == ['same actual source selected']
checks = [value for value in original['checks'] if value['check'] != 'same actual source selected']
tasks = [value for value in start['situations'].values() if value['type'] == 'situation_terravore_consume_planet']
assert len(tasks) == 1
source = str(tasks[0]['target']['id'])
def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})
check('actual selected source1731 from native target', source == '1731')
check('native source name matches photographed Spring', before['planets'][source]['name'] == 'HUMAN1_PLANET_Spring')
check('same real original carrier Q20 and actual100', before['planets'][source]['planet_size'] == 20 and before['planets'][source]['colony'] == 15 and before['colonies']['15']['actual_pop_sum'] == 100)
for suffix, state in [('restored', before), ('native-ui-start', start), ('native-first-month', end)]:
    check(suffix + ' native bytes bind audit', hashlib.sha256((run / (prefix + '-' + suffix + '.sav')).read_bytes()).hexdigest() == state['save_sha256'])
report = {key: value for key, value in original.items() if key not in ('status', 'checks', 'checks_passed', 'checks_total')}
report.update(status='PASS' if all(value['passed'] for value in checks) else 'FAIL',
              correction='Original hardcoded source1115 assertion was wrong; native UI Spring actually targeted1731. Original FAIL retained. All15 unrelated checks retained plus independent native-target/name/asset/hash checks.',
              checks=checks, checks_passed=sum(value['passed'] for value in checks), checks_total=len(checks))
destination = run / (prefix + '-actual-source-route-proof.json')
assert not destination.exists()
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in report.items() if key != 'checks'}))
assert report['status'] == 'PASS'
