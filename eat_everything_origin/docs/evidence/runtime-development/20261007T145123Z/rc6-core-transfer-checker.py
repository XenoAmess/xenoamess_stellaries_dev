import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T145123Z')
stages = [
    ('rc6-own-old-save-before-court-migration', 0, 0, 0),
    ('rc6-own-court-migrated-real-day', 0, 0.1, 1),
    ('rc6-foreign-native-transfer-same-day', 1, 0, 0),
    ('rc6-foreign-native-transfer-real-next-day', 1, 0, 0),
    ('rc6-foreign-reloaded-fresh-export', 1, 0, 0),
    ('rc6-own-native-return-same-day', 0, 0.1, 1),
    ('rc6-own-native-return-real-next-day', 0, 0.1, 1),
    ('rc6-own-after-five-monthly-sync-callbacks', 0, 0.1, 1),
    ('rc6-own-return-reloaded-fresh-export', 0, 0.1, 1),
]
audits = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n, *_ in stages]
checks = []

def check(name, actual, expected):
    checks.append({'check': name, 'status': 'PASS' if actual == expected else 'FAIL',
                   'actual': actual, 'expected': expected})

def masses(a):
    c = collections.Counter()
    for g in a['pop_groups'].values():
        c[(g['planet'], g['key']['species'])] += g['size']
    return sorted((str(k), v) for k, v in c.items())

base = audits[0]
ledger = ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds', 'eep_stage', 'eep_fleet_stage']
for (name, owner, jobs, count), a in zip(stages, audits, strict=True):
    p = a['planets']['1']
    # Native timed modifier items contain anonymous blocks.
    import re
    court_count = len(re.findall(r'modifier="eep_court"', p['modifiers']))
    check(name + ':actual_owner', p['owner'], owner)
    check(name + ':physical_jobs_modifier', p['variables']['eep_probe_jobs_mult'], jobs)
    check(name + ':exact_court_count', court_count, count)
    check(name + ':physical_capacity_value', p['variables']['eep_capacity_value'], 2)
    check(name + ':capacity_count', len(re.findall(r'modifier="eep_capacity"', p['modifiers'])), 1)
    check(name + ':capacity_multiplier2', bool(re.search(r'multiplier=2\s+modifier="eep_capacity"', p['modifiers'])), True)
    check(name + ':original_size', p['planet_size'], base['planets']['1']['planet_size'])
    check(name + ':original_deposits', p['deposits'], base['planets']['1']['deposits'])
    check(name + ':all_original_stocks', a['countries']['0']['stockpile'], base['countries']['0']['stockpile'])
    check(name + ':all_foreign_stocks', a['countries']['1']['stockpile'], base['countries']['1']['stockpile'])
    check(name + ':eep_ledger', {k: a['countries']['0']['variables'].get(k) for k in ledger},
          {k: base['countries']['0']['variables'].get(k) for k in ledger})
    check(name + ':actual_population_by_colony_species', masses(a), masses(base))
    check(name + ':no_new_devour_task', a['situations'], base['situations'])
    targets = {t['name']: t['id'] for t in a['event_targets']}
    check(name + ':bound_original_planet', targets.get('eep_core0'), 1)
    check(name + ':bound_original_actor', targets.get('eep_core_actor1'), 0)

check('same_day_repeated_monthly_state', audits[7]['countries']['0']['variables'], audits[6]['countries']['0']['variables'])
check('same_day_repeated_all_popgroups', audits[7]['pop_groups'], audits[6]['pop_groups'])
check('same_day_repeated_all_jobs', audits[7]['pop_jobs'], audits[6]['pop_jobs'])
check('same_day_repeated_all_districts', audits[7]['districts'], audits[6]['districts'])
check('same_day_repeated_all_colonies', audits[7]['colonies'], audits[6]['colonies'])
result = {
    'status': 'PASS' if all(c['status'] == 'PASS' for c in checks) else 'FAIL',
    'version': '0.2.0-rc.6', 'language': 'l_simp_chinese',
    'scope': 'Native controlled mother transfer and retake, no manual court sync at transfer; old-save migration, actual next days, exact original-byte reload and five same-day monthly callbacks. Native ownership changes can alter jobs/rights; exact stocks, population by colony/species, EEP ledger, binding and physical capacity compared. Not natural war or full Mod acceptance.',
    'checks': checks,
    'saves': {n: a['save_sha256'] for (n, *_), a in zip(stages, audits, strict=True)},
}
dest = run / 'rc6-native-court-transfer-retake-reload-proof.json'
assert not dest.exists()
dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'failed': [c['check'] for c in checks if c['status'] == 'FAIL']}))
