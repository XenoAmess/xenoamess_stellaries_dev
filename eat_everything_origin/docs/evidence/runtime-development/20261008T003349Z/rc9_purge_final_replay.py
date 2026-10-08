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
run,user,m=h.load_run()
shutil.copyfile(Path(__file__),run/Path(__file__).name)
stem='rc9-focus-native-purge-finished-notice-pending'
b=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
def ledger(a):return {k:a['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']}
def groups(a):return {k:{f:v.get(f) for f in ['planet','size','key']} for k,v in a['pop_groups'].items()}
pre={
 'actual_shattered_source':b['planets']['84']['planet_class']=='pc_shattered',
 'source_tombstone_zero_population':b['colonies']['24']['actual_pop_sum']==0,
 'only_bound_mother_owned':b['countries']['0']['owned_colonies']==[0],
 'no_tasks':not b['situations'],
 'ledger_exact':ledger(b)=={'eep_c':16,'eep_g':16,'eep_d':6,'eep_made':200,'eep_worlds':1},
 'manufactured200':b['countries']['0']['variables']['eep_last_manufactured']==200,
 'actual_return228_recorded_twice':b['countries']['0']['variables']['eep_last_return']==b['planets']['84']['variables']['eep_return_amount']==228,
 'no_foreign_on_mother':all(b['pop_groups'][str(i)]['key']['species']!=39 for i in b['colonies']['0']['pop_groups']),
 'five_settlement_receipts':{'eep_credit_done','eep_return_done','eep_population_done','eep_crisis_done','eep_destroy_done'}<=set(b['planets']['84']['flags']),
 'no_source_active_pending':not ({'eep_active','eep_pending'}&set(b['planets']['84']['flags'])),
 'first_notice_recorded':'eep_first_notice' in b['countries']['0']['flags'],
}
h.write_json(run/'rc9-focus-native-purge-final-proof.json',{'status':'PASS_SCOPED' if all(pre.values()) else 'FAIL','checks':pre,'save_sha256':b['save_sha256'],'actual_date':b['date'],'mother_population':b['colonies']['0']['actual_pop_sum'],'scope':'Actual post-waiting purge_normal settlement after 360 native days. Controlled progress38 preparation; not a second natural39-month proof. Return amount is authoritative saved settlement receipt, not independently captured immediately-before-return population.'})
assert all(pre.values())
error=user/'logs/error.log'
eb=error.read_bytes();(run/'rc9-focus-purge-final-replay-error-before.log').write_bytes(eb)
h.press_scan_code(0x29,'rc9-focus-purge-final-replay-console-open',1)
for n in range(5):
 h.type_text('effect root = { country_event = { id = eep.2 } every_situation = { limit = { is_situation_type = situation_eep_devouring } situation_event = { id = eep.21 } } }',True,'rc9-focus-purge-final-five-replays-'+str(n))
r.gpu_capture('rc9-focus-purge-final-replay-console-receipt')
h.press_scan_code(0x29,'rc9-focus-purge-final-replay-console-close',1)
a=r.native_save('rc9-focus-native-purge-final-five-replays',b['date'],(0,))
ea=error.read_bytes();(run/'rc9-focus-purge-final-replay-error-after.log').write_bytes(ea)
checks={
 'ledger_once':ledger(a)==ledger(b),
 'all_stockpiles_same':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'all_actual_population_groups_same':groups(a)==groups(b),
 'all_country0_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'same_source_planet':a['planets']['84']==b['planets']['84'],
 'same_targets':a['event_targets']==b['event_targets'],
 'same_country0_flags':a['countries']['0']['flags']==b['countries']['0']['flags'],
 'no_new_task':a['situations']==b['situations']=={},
 'no_new_error_bytes':ea==eb,
}
h.write_json(run/'rc9-focus-native-purge-final-replay-proof.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'monthly_callbacks':5,'error_delta_bytes':len(ea)-len(eb),'scope':'Completed settlement economic/population idempotence; no natural stage2 milestone claim.'})
print(json.dumps({'final_checks':pre,'replay_checks':checks,'after_sha256':a['save_sha256']}),flush=True)
assert all(checks.values())
