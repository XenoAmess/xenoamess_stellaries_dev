import json
import logging
from pathlib import Path
import shutil
import sys
branch,start=sys.argv[1:]
assert branch in ('abandon','purge','star','bombard')
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run()
cp=run/Path(__file__).name
if not cp.exists():shutil.copyfile(Path(__file__),cp)
assert cp.read_bytes()==Path(__file__).read_bytes()
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));assert branch=='bombard'
def ledger(a):return {k:a['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']}
def groups(a):return {k:{f:v.get(f) for f in ['planet','size','key']} for k,v in a['pop_groups'].items()}
prefix='rc9-external-'+branch
pre={
 'zero_eep_reward':ledger(b)=={'eep_c':0,'eep_g':0,'eep_d':2,'eep_made':0,'eep_worlds':0},
 'source_zero_population':b['colonies'].get('24',{}).get('actual_pop_sum',0)==0,
 'only_original_mother_owned':b['countries']['0']['owned_colonies']==[0],
 'no_live_eep_task':not any(v.get('type')=='situation_eep_devouring' and v.get('killed')!='yes' for v in b['situations'].values()),
 'source_task_flags_cleared':not ({'eep_active','eep_pending'}&set(b['planets']['84']['flags'])),
 'no_first_notice':'eep_first_notice' not in b['countries']['0']['flags'],
 'no_reward_notice_pending':'eep_notice_pending' not in b['countries']['0']['flags'],
 'original_core_not_dead':'eep_core_dead' not in b['countries']['0']['flags'],
 'original_core_target1':next(v for v in b['event_targets'] if v['name']=='eep_core0')['id']==1,
 'original_actor0':next(v for v in b['event_targets'] if v['name']=='eep_core_actor1')['id']==0,
 'core_deposit_once':sum(b['deposits'][str(i)]['type']=='d_eep_core' for i in b['planets']['1']['deposits'])==1,
}
h.write_json(run/(prefix+'-completed-negative-preconditions.json'),{'status':'PASS_SCOPED' if all(pre.values()) else 'FAILED_PRECONDITION','checks':pre,'save_sha256':b['save_sha256'],'date':b['date'],'scope':'External loss and no devouring reward; native monthly economic changes retained.'})
assert all(pre.values())
error=user/'logs/error.log';eb=error.read_bytes();(run/(prefix+'-negative-replay-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,prefix+'-negative-replay-console-open',1)
for n in range(5):h.type_text('effect root = { country_event = { id = eep.2 } every_situation = { limit = { is_situation_type = situation_eep_devouring } situation_event = { id = eep.21 } } }',True,prefix+'-negative-five-replays-'+str(n))
r.gpu_capture(prefix+'-negative-replay-native-receipt')
h.press_scan_code(0x29,prefix+'-negative-replay-console-close',1)
a=r.native_save(prefix+'-five-negative-replays',b['date'],(0,16777244))
ea=error.read_bytes();(run/(prefix+'-negative-replay-error-after.log')).write_bytes(ea)
checks={
 'attacker_stock_same':a['countries']['16777244']['stockpile']==b['countries']['16777244']['stockpile'],
 'ledger_same':ledger(a)==ledger(b),
 'country0_stock_same':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'all_actual_population_groups_same':groups(a)==groups(b),
 'country0_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'country0_flags_same':a['countries']['0']['flags']==b['countries']['0']['flags'],
 'core_planet_same':a['planets']['1']==b['planets']['1'],
 'source_planet_same':a['planets']['84']==b['planets']['84'],
 'all_event_targets_same':a['event_targets']==b['event_targets'],
 'all_situations_same':a['situations']==b['situations'],
 'error_no_new_bytes':ea==eb,
}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_date':a['date'],'monthly_callbacks':5,'error_delta_bytes':len(ea)-len(eb),'scope':'This external destruction branch only; no claim that other routes or branches are complete.'}
h.write_json(run/(prefix+'-completed-negative-replay-proof.json'),proof)
print(json.dumps({'preconditions':pre,'proof':proof}),flush=True)
assert all(checks.values())
