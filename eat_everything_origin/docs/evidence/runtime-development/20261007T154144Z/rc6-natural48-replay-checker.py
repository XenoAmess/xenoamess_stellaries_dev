import copy
import json
from pathlib import Path

run = Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names = ['rc6-lith-true-ai-natural-month48-day2-settled',
         'rc6-lith-ai-natural-endpoint-after-five-replays']
a, b = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
checks = []


def check(name, actual, expected):
    checks.append({'check': name, 'status': 'PASS' if actual == expected else 'FAIL',
                   'actual': actual, 'expected': expected})


check('same_native_date', [a['date'], b['date']], ['2204.01.02'] * 2)
for field in ['colonies', 'pop_groups', 'pop_jobs', 'deposits', 'districts', 'species', 'event_targets']:
    check('full_' + field + '_preserved', b[field], a[field])
check('foreign_complete_audit_preserved', b['countries']['16777218'], a['countries']['16777218'])
ac, bc = [copy.deepcopy(x['countries']['0']) for x in (a, b)]
for key, old, new in [('eep_stage', 0, 1), ('eep_tasks', 1, 0)]:
    check('exact_known_notice_cache_' + key, [ac['variables'].pop(key), bc['variables'].pop(key)], [old, new])
check('exact_notice_pending_consumed', [ac['flags'].pop('eep_notice_pending'), 'eep_notice_pending' in bc['flags']], [62842584, False])
check('exact_first_notice_receipt', ['eep_first_notice' in ac['flags'], bc['flags'].pop('eep_first_notice')], [False, 62842584])
check('all_other_country_fields_preserved', bc, ac)
ap, bp = [copy.deepcopy(x['planets']) for x in (a, b)]
for key, old, new in [('eep_actual_pop', 5200, 6037), ('eep_free_districts', 9, 13)]:
    check('exact_core_display_export_' + key, [ap['8']['variables'].pop(key), bp['8']['variables'].pop(key)], [old, new])
check('exact_source_probe_export', [ap['3']['variables'].pop('eep_probe_real_progress'), bp['3']['variables'].pop('eep_probe_real_progress')], [47, 48])
check('all_other_physical_planet_fields_preserved', bp, ap)
at, bt = [copy.deepcopy(x['situations']) for x in (a, b)]
check('exact_killed_task_probe_export', [at['16777223']['variables'].pop('eep_probe_progress'), bt['16777223']['variables'].pop('eep_probe_progress')], [47, 48])
check('all_other_task_fields_preserved', bt, at)
result = {'status': 'PASS' if all(x['status'] == 'PASS' for x in checks) else 'FAIL',
          'checks': checks, 'version': '0.2.0-rc.6', 'language': 'l_simp_chinese',
          'saves': {n:x['save_sha256'] for n,x in zip(names,(a,b),strict=True)},
          'scope': 'Five same-day callback requests after natural48-month settlement. All economic fields preserved. Only exact first-notice/cache and fixture progress exports permitted; no broad variable filtering. Killed task remains killed; do not claim reward callback execution on a valid active task.'}
out = run / 'rc6-natural48-ai-five-replays-strict-proof.json'
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[x['check'] for x in checks if x['status']=='FAIL']}))
