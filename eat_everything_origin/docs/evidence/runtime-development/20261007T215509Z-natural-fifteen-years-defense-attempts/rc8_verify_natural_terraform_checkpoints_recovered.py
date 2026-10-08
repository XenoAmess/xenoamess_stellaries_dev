"""Read completed native checkpoints; never send input or modify a save."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
source_copy = run / 'rc8_verify_natural_terraform_checkpoints_recovered.py'
if not source_copy.exists():
    shutil.copyfile(Path(__file__), source_copy)
assert source_copy.read_bytes() == Path(__file__).read_bytes()
stages = sys.argv[1:]
assert stages and len(set(stages)) == len(stages)
checks = []
rows = []
expected_ledger = dict(zip(['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds'], [57, 57, 16, 900, 3]))


def check(label, actual, expected):
    checks.append({'check': label, 'actual': actual, 'expected': expected, 'passed': actual == expected})


def day_number(date):
    year, month, day = map(int, date.split('.'))
    return year * 360 + (month - 1) * 30 + day - 1


def anonymous_blocks(text):
    iterator = iter(q.tokens(text))
    for token, before, after in iterator:
        if token != '{':
            raise ValueError('Native modifier list contains an unexpected scalar')
        start = after
        depth = 1
        for nested, left, right in iterator:
            depth += (nested == '{') - (nested == '}')
            if depth == 0:
                yield text[start:left]
                break
        else:
            raise ValueError('Native modifier list contains an unclosed object')


for stage in stages:
    path = run / (stage + '.sav')
    a = json.loads(path.with_suffix('.audit.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    check(stage + ': original native bytes match audit', digest, a['save_sha256'])
    c = a['countries']['0']
    p = a['planets']['1']
    mother = a['colonies']['0']
    check(stage + ': physical mother / colony', p.get('colony'), 0)
    check(stage + ': mother owner', p.get('owner'), 0)
    check(stage + ': mother controller', p.get('controller'), 0)
    check(stage + ': exact EEP ledger', {k: c['variables'].get(k) for k in expected_ledger}, expected_ledger)
    check(stage + ': physical core flag', 'eep_core' in p['flags'], True)
    check(stage + ': original mother reference',
          [{'type': t.get('type'), 'id': t.get('id')} for t in a['event_targets'] if t['name'] == 'eep_core0'],
          [{'type': 'planet', 'id': 1}])
    check(stage + ': original actor reference',
          [{'type': t.get('type'), 'id': t.get('id')} for t in a['event_targets'] if t['name'] == 'eep_core_actor1'],
          [{'type': 'country', 'id': 0}])
    deposits = [a['deposits'][str(i)]['type'] for i in p['deposits']]
    check(stage + ': exactly one EEP core deposit', deposits.count('d_eep_core'), 1)
    mods = [q.scalars(v) for v in anonymous_blocks(q.block(p['modifiers'], 'items'))]
    check(stage + ': one capacity16 modifier',
          [m for m in mods if m.get('modifier') == 'eep_capacity'],
          [{'multiplier': 16, 'modifier': 'eep_capacity', 'days': -1}])
    check(stage + ': one permanent court modifier',
          [m for m in mods if m.get('modifier') == 'eep_court'],
          [{'modifier': 'eep_court', 'days': -1}])
    check(stage + ': positive energy stock', c['stockpile'].get('energy', 0) > 0, True)
    with zipfile.ZipFile(path) as archive:
        native = archive.read('gamestate').decode('utf-8-sig')
    planet = q.block(q.block(q.block(native, 'planets'), 'planet'), '1')
    terraform = q.block(planet, 'terraform_process')
    t = q.scalars(terraform)
    days = day_number(a['date']) - day_number('2299.03.12')
    if terraform:
        check(stage + ': actual unfinished class', p['planet_class'], 'pc_volcanic')
        check(stage + ': target Hive World', t.get('planet_class'), 'pc_hive')
        check(stage + ': actual progress equals natural days', t.get('progress'), days)
        check(stage + ': unchanged actual total', t.get('total'), 7200)
        check(stage + ': native payer', t.get('who'), 0)
        check(stage + ': original payment', q.scalars(q.block(terraform, 'paid')), {'energy': 10000})
    else:
        check(stage + ': completed class', p['planet_class'], 'pc_hive')
        check(stage + ': twenty actual years reached', days >= 7200, True)
    balance = c['budget_categories']['last_month']['balance']
    net = {resource: round(sum(cat.get(resource, 0) for cat in balance.values()), 5)
           for resource in ['energy', 'minerals', 'food', 'alloys', 'unity', 'trade']}
    districts = {a['districts'][str(i)]['type']: a['districts'][str(i)]['level'] for i in mother['districts']}
    rows.append({'stage': stage, 'date': a['date'], 'save_sha256': digest,
                 'actual_class': p['planet_class'], 'natural_days_since_paid': days,
                 'terraform_process': t, 'terraform_paid': q.scalars(q.block(terraform, 'paid')),
                 'eep_ledger': {k: c['variables'].get(k) for k in expected_ledger},
                 'population': mother['actual_pop_sum'], 'stockpile': c['stockpile'],
                 'last_month_net': net, 'built_districts': districts, 'deposit_types': deposits,
                 'mother_jobs': {str(i): a['pop_jobs'][str(i)] for i in mother['pop_jobs']}})

failed = [item for item in checks if not item['passed']]
last = rows[-1]
report = {'status': 'FAIL' if failed else 'PASS_SCOPED',
          'scope': 'Read-only completed native Scorched Hive checkpoints; not complete EAT acceptance.',
          'country_scope': 'Current Focus country0; no same-day foreign-country isolation claim.',
          'full_terraform_completion': last['actual_class'] == 'pc_hive' and not last['terraform_process'],
          'engine_capacity_ui_acceptance': 'NOT_EVALUATED_BY_THIS_READ_ONLY_CHECK',
          'check_count': len(checks), 'failed_count': len(failed), 'checks': checks, 'checkpoints': rows}
output = run / ('rc8-natural-terraform-checkpoints-' + str(len(stages)) + '-' + last['date'].replace('.', '-') + '-proof.json')
assert not output.exists(), 'Proof filenames must be unique; preserve earlier proofs.'
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': report['status'], 'checks': len(checks), 'failed': len(failed),
                  'full_terraform_completion': report['full_terraform_completion'],
                  'last_date': last['date'], 'last_month_net': last['last_month_net'],
                  'proof': str(output), 'failures': failed}, ensure_ascii=True))
if failed:
    raise SystemExit(1)
