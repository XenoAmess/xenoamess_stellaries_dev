import json
from pathlib import Path

run=Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names=['rc6-native-mid47-cancel-original-reloaded','rc6-native-mid47-aborted-old-damage-preserved',
       'rc6-native-old-damage-day1-before-restart','rc6-native-old-damage14-new34month-task-started',
       'rc6-native-restarted-q14-controlled-completion']
xs=[json.loads((run/(n+'.audit.json')).read_text(encoding='utf-8')) for n in names]
before,aborted,day,start,done=xs
checks=[]


def check(name,actual,expected):
    checks.append({'check':name,'actual':actual,'expected':expected,'status':'PASS' if actual==expected else 'FAIL'})


def damage(x):
    return sum(d['type']=='d_lithoid_devastation' and d['deposit_holder']['id']==3 for d in x['deposits'].values())


check('native_exact_dates',[x['date'] for x in xs],['2203.12.30','2203.12.30','2204.01.01','2204.01.01','2204.01.01'])
check('actual_cancel_was_mid47',next(s['progress'] for s in before['situations'].values() if s['type']=='situation_eep_devouring'),47)
for field in ['countries','colonies','pop_groups','pop_jobs','deposits','districts','species','event_targets']:
    check('same_day_abort_full_'+field,aborted[field],before[field])
    check('same_day_restart_full_'+field,start[field],day[field])
for label,x in [('before',before),('aborted',aborted),('next_real_day',day),('restart',start)]:
    check('actual_old_six_damage_'+label,damage(x),6)
    check('actual_original_size20_'+label,x['planets']['3']['planet_size'],20)
    v=x['countries']['0']['variables']
    check('no_reward_before_completion_'+label,[v[k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']],[0,0,2,0,0])
    check('original_core_bound_'+label,next(t['id'] for t in x['event_targets'] if t['name']=='eep_core0'),8)
for f in ['eep_active','eep_native','eep_owned_colony_event','colony_event','being_devoured']:
    check('actual_abort_cleared_'+f,f in aborted['planets']['3']['flags'],False)
    check('actual_current_restart_flag_'+f,f in start['planets']['3']['flags'],True)
check('abort_preserved_native_cooldown',aborted['planets']['3']['flags']['recently_eaten_planet'],before['planets']['3']['flags']['recently_eaten_planet'])
check('no_active_old_task_after_real_day',day['situations'],{})
v=start['planets']['3']['variables']
check('actual_restart_q14_old6_t34',[v[k] for k in ['eep_q','eep_old_damage','eep_months']],[14,6,34])
check('actual_new_task_zero_progress',[(s['type'],s['progress'],s.get('killed')) for s in start['situations'].values()],[('situation_eep_devouring',0,None)])
v=done['countries']['0']['variables']
check('controlled_remaining_only_final_ledger',[v[k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds','eep_last_capacity','eep_last_manufactured']],[14,0,5,0,1,3,0])
check('controlled_done_source_shattered',done['planets']['3']['planet_class'],'pc_shattered')
check('controlled_done_physical_capacity5',done['planets']['8']['variables']['eep_capacity_value'],5)
check('controlled_done_source_unowned','owner' in done['planets']['3'],False)
check('controlled_done_foreign_complete_country_same',done['countries']['16777218'],start['countries']['16777218'])
check('controlled_done_return_all_previous_source',v['eep_last_return'],start['colonies']['15']['actual_pop_sum'])
popdelta=done['colonies']['0']['actual_pop_sum']-start['colonies']['0']['actual_pop_sum']-start['colonies']['15']['actual_pop_sum']
check('controlled_done_extra_only_nonnegative_native100_units',popdelta>=0 and popdelta%100==0,True)
result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','version':'0.2.0-rc.6','language':'l_simp_chinese','checks':checks,
        'saves':{n:x['save_sha256'] for n,x in zip(names,xs,strict=True)},'extra_native_population':popdelta,
        'scope':'Real47-month natural-source cancellation preserves all audited country/population/job/district/species/deposit/target data and six actual native damage. Native next day clears old task; current restart derives Q14/T34 and grants no reward. Controlled endpoint credits only14 and D5, native population only. Not a natural34-month completion; known original material-reward research-pool behavior documented separately.'}
out=run/'rc6-natural-mid47-cancel-old-damage-restart-q14-proof.json'
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c['check'] for c in checks if c['status']=='FAIL'],'extra_native_population':popdelta}))
