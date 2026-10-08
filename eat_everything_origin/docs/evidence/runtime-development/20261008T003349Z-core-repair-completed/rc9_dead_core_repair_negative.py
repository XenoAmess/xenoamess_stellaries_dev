import hashlib
import json
import logging
from pathlib import Path
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,manifest=h.load_run()
copy=run/Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__),copy)
start=json.loads((run/'rc9-dead-core-original-reloaded.audit.json').read_text(encoding='utf-8'))
assert start['date']=='2200.01.06'
assert 'eep_core_dead' in start['countries']['0']['flags']
assert start['planets']['1']['planet_class']=='pc_shattered'
assert start['countries']['0']['owned_colonies']==[13]
old=start['planets']['1']['deposits']
removed=[i for i in old if start['deposits'][str(i)]['type']=='d_eep_core']
assert len(removed)==1
log=user/'logs/error.log'
before_log=log.read_bytes()
(run/'rc9-dead-repair-error-before.log').write_bytes(before_log)
h.press_scan_code(0x29,'rc9-dead-repair-console-open',1)
event='carrier_event = { id = eep.4 } '
monthly='country_event = { id = eep.2 } '
command='effect root = { event_target:eep_core@this = { remove_deposit = d_eep_core eep_repair_core_deposit = yes '+event*5+' } '+monthly*5+' }'
h.type_text(command,True,'rc9-dead-core-controlled-missing-and-five-replays')
r.gpu_capture('rc9-dead-core-repair-console-receipt')
h.press_scan_code(0x29,'rc9-dead-repair-console-close',1)
after=r.native_save('rc9-dead-core-missing-stays-dead','2200.01.06',(0,))
after_log=log.read_bytes()
(run/'rc9-dead-repair-error-after.log').write_bytes(after_log)
assert after_log.startswith(before_log)
delta=after_log[len(before_log):]
(run/'rc9-dead-repair-error-delta.log').write_bytes(delta)
b,a=start['countries']['0'],after['countries']['0']
checks={
 'dead_flag_preserved':a['flags']==b['flags'],
 'all_eep_variables_preserved':a['variables']==b['variables'],
 'all_country0_stock_preserved':a['stockpile']==b['stockpile'],
 'all_actual_groups_preserved':start['pop_groups']==after['pop_groups'],
 'all_eep_targets_preserved':start['event_targets']==after['event_targets'],
 'only_remaining_original_colony13':a['owned_colonies']==[13],
 'shattered_original_core':after['planets']['1']['planet_class']=='pc_shattered',
 'only_core_flavor_removed':after['planets']['1']['deposits']==[i for i in old if i not in removed],
 'no_core_deposit_restored':not any(after['deposits'][str(i)]['type']=='d_eep_core' for i in after['planets']['1']['deposits']),
 'no_court_created_on_any_audited_planet':not any('eep_court' in p['modifiers'] for p in after['planets'].values()),
 'no_native_error_delta':not delta,
}
result={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','scope':'Original native permanent death + controlled removal of surviving flavor deposit; five repair and monthly requests must not restore a core or choose backup. Not a natural terraform case.','date':after['date'],'before_save_sha256':start['save_sha256'],'after_save_sha256':after['save_sha256'],'controlled_removed_deposit_ids':removed,'checks':checks,'error_delta_bytes':len(delta),'error_after_sha256':hashlib.sha256(after_log).hexdigest()}
h.write_json(run/'rc9-permanent-core-death-repair-negative-proof.json',result)
print(json.dumps(result,ensure_ascii=True),flush=True)
assert all(checks.values())
