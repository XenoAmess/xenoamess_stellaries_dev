import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q

run = Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names = ['rc6-lith-true-ai-natural-precise-month48-day1',
         'rc6-lith-true-ai-natural-month48-day2-settled',
         'rc6-ai-calendar-control-dayone-reloaded-before-abort',
         'rc6-ai-calendar-control-dayone-native-aborted',
         'rc6-ai-calendar-control-daytwo-no-settlement',
         'rc6-original-colony190-control-reloaded-before-bite',
         'rc6-original-colony190-one-bite-same-day-control']
xs = [json.loads((run / (n + '.audit.json')).read_text(encoding='utf-8')) for n in names]
initial, settled, reload, aborted, no_settlement, native_before, native_after = xs
checks = []


def check(name, actual, expected):
    checks.append({'check': name, 'actual': actual, 'expected': expected,
                   'status': 'PASS' if actual == expected else 'FAIL'})


def resources(x):
    return x['countries']['0']['stockpile']


def damage(x):
    return sum(d['type'] == 'd_lithoid_devastation' and d['deposit_holder']['id'] == 3 for d in x['deposits'].values())


for n, x in zip(names, xs, strict=True):
    with zipfile.ZipFile(run / (n + '.sav')) as z:
        player = re.findall(r'country=(\d+)', q.block(z.read('gamestate').decode('utf-8-sig'), 'player'))
    check('actual_foreign_player_' + n, player, ['16777218'])
check('actual_control_dates', [x['date'] for x in xs],
      ['2204.01.01', '2204.01.02', '2204.01.01', '2204.01.01', '2204.01.02', '2204.01.01', '2204.01.01'])
for label, x in [('reloaded', reload), ('aborted', aborted), ('no_settlement', no_settlement), ('native_before', native_before)]:
    check('all_original_stockpile_preserved_' + label, resources(x), resources(initial))
    check('actual_colony_pop_preserved_' + label,
          {k:v['actual_pop_sum'] for k,v in x['colonies'].items()},
          {k:v['actual_pop_sum'] for k,v in initial['colonies'].items()})
    v = x['countries']['0']['variables']
    check('no_eep_ledger_reward_' + label, [v[k] for k in ['eep_c', 'eep_g', 'eep_d', 'eep_made', 'eep_worlds']], [0,0,2,0,0])
    check('old_native_six_damage_preserved_' + label, damage(x), 6)
check('calendar_control_research_queues_equal_settlement', no_settlement['countries']['0']['research_queues'], settled['countries']['0']['research_queues'])
check('calendar_control_completed_tech_equal_settlement', no_settlement['countries']['0']['completed_technologies'], settled['countries']['0']['completed_technologies'])
check('original_event_same_day_queues_preserved', native_after['countries']['0']['research_queues'], native_before['countries']['0']['research_queues'])
check('original_event_same_day_completed_tech_preserved', native_after['countries']['0']['completed_technologies'], native_before['countries']['0']['completed_technologies'])
check('original_event_actual_damage_six_to_eight', [damage(native_before), damage(native_after)], [6,8])
check('original_event_actual_source_not_destroyed', [native_after['planets']['3']['planet_class'],native_after['planets']['3']['owner']], ['pc_continental',0])
check('original_event_actual_original_capital_source', native_after['countries']['0']['native']['capital'],15)
check('original_event_actual_unchanged_core_binding', next(t['id'] for t in native_after['event_targets'] if t['name']=='eep_core0'),8)
v = native_after['countries']['0']['variables']
check('original_event_no_eep_credit_or_manufacture', [v[k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']], [0,0,2,0,0])
check('original_event_no_source_eep_receipts', any(f in native_after['planets']['3']['flags'] for f in ['eep_credit_done','eep_return_done','eep_population_done','eep_destroy_done']),False)
check('original_event_original_random_alloy100', resources(native_after)['alloys']-resources(native_before)['alloys'],100)
check('original_event_foreign_full_country_preserved', native_after['countries']['16777218'],native_before['countries']['16777218'])
check('original_event_actual_colony_pop_preserved',
      {k:v['actual_pop_sum'] for k,v in native_after['colonies'].items()},
      {k:v['actual_pop_sum'] for k,v in native_before['colonies'].items()})
for key in ['physics_research','society_research','engineering_research']:
    check('original_event_exact_science_zero_' + key, resources(native_after).get(key,0),0)
    check('original_event_same_science_loss_as_settlement_' + key,
          resources(native_after).get(key,0)-resources(native_before).get(key,0),
          resources(settled).get(key,0)-resources(initial).get(key,0))
sa,sb=resources(initial),resources(settled)
delta={k:sb.get(k,0)-sa.get(k,0) for k in sorted(sa.keys()|sb.keys())}
check('settlement_all_other_original_resources_preserved',
      {k:v for k,v in delta.items() if k not in ['minerals','alloys','physics_research','society_research','engineering_research']},
      {k:0 for k in delta if k not in ['minerals','alloys','physics_research','society_research','engineering_research']})
original=json.loads((run/'rc6-true-ai-natural48-month-boundary-proof.json').read_text(encoding='utf-8'))
check('original_boundary_only_failed_resource_assumption', [c['check'] for c in original['checks'] if c['status']=='FAIL'], ['only_original_native_end_resource_types'])
check('all_other_original_boundary_checks_pass', sum(c['status']=='PASS' for c in original['checks']),76)
game=Path('C:/SteamLibrary/steamapps/common/Stellaris')
source={str(p.relative_to(game)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [game/'events/colony_events_1.txt',game/'common/scripted_effects/00_scripted_effects.txt']}
result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','checks':checks,
        'version':'0.2.0-rc.6','language':'l_simp_chinese','saves':{n:x['save_sha256'] for n,x in zip(names,xs,strict=True)},
        'native_sources':source,'original_boundary_report_status':original['status'],
        'scope':'Natural48-month boundary76 checks plus independent exact-byte calendar/no-settlement and unmodified native colony.190/consume_world actual material-lottery control. Research stock loss reproduced in original native event same day with queues unchanged; not normal research progress. Preserve original77-check FAIL. This closes the native-payout attribution, does not promise unaffected research stock for vanilla lottery or claim full Mod acceptance.',
        'known_native_behavior':'Native material reward transaction in this month-boundary state clears three research pools; original unmodified event reproduces the exact amounts. EEP preserves this original payout behavior.'}
out=run/'rc6-natural48-native-science-payout-isolation-proof.json'
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c['check'] for c in checks if c['status']=='FAIL']}))
