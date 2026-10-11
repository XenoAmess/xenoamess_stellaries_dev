"""Pure business boundary validation, no runtime or GUI imports."""
import importlib.util
import json
from pathlib import Path

run = Path('_runtime/heart-of-devouring/runs/20261009T044016Z')
spec = importlib.util.spec_from_file_location('native_calendar_v3', run / 'formal_production_native_calendar_checked_v3.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
ordinary = load('terravore-rear97-science-native-actual-return-native-devour-wait-v6-proof.json')
boundary = load('terravore-fourth-devour-pre-second-bite-post-return-02-native-devour-wait-v6-proof.json')
cap = load('terravore-fourth-devour-native-front-watch-04-native-devour-wait-v4-proof.json')
review = {'status': 'PASS_REVIEWED_NATIVE_BOUNDARY', 'checks': {'test_exact_review': True},
    'before_sha256': boundary['after_sha256'], 'start_date': '2278.01.30', 'end_date': '2278.02.01',
    'days': 1, 'allowed_boundaries': boundary['boundaries'], 'maximum_days': 1}
checks = {}
def case(name, expected, pre, start, end, days, rev=None):
    try:
        m.validate_business_interval(pre, start, end, days, rev)
        allowed = True
    except AssertionError:
        allowed = False
    checks[name] = allowed is expected
case('ordinary15_allowed', True, ordinary, '2278.01.07', '2278.01.22', 15)
case('over_business_max_rejected', False, ordinary, '2278.01.07', '2278.01.23', 16)
case('original_PASS22_actual0_active_combat_rejected', False, boundary, '2278.01.30', '2278.02.01', 1)
case('cap_unready_without_review_rejected', False, cap, '2278.01.01', '2278.01.02', 1)
for key, value in [('before_sha256', 'wrong'), ('end_date', '2278.02.02'), ('allowed_boundaries', []), ('checks', {'bad': False})]:
    case('mismatch_' + key + '_rejected', False, boundary, '2278.01.30', '2278.02.01', 1, {**review, key: value})
case('exact_review_pure_function_allowed', True, boundary, '2278.01.30', '2278.02.01', 1, review)
p = run / 'native-calendar-v3-business-preflight-check-proof.json'
assert not p.exists()
p.write_text(json.dumps({'status': 'PASS_PURE_BUSINESS_PREFLIGHT' if all(checks.values()) else 'FAIL',
    'checks': checks, 'scope': 'Pure validator branches only. No runtime import, game input or calendar replay.'}, indent=2), encoding='utf-8')
print(json.dumps({'checks': len(checks), 'failed': [k for k,v in checks.items() if v is not True]}), flush=True)
assert all(checks.values())
