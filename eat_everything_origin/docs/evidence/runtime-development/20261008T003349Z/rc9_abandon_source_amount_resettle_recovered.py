import json
import logging
from pathlib import Path
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run()
shutil.copyfile(Path(__file__),run/Path(__file__).name)
b=json.loads((run/'rc9-external-abandon-task-ready.audit.json').read_text(encoding='utf-8'))
assert b['colonies']['24']['actual_pop_sum']==100
receipt=r.native_load('return-task100','rc9-external-abandon-amount-original100-load')
assert receipt['source_sha256']==b['save_sha256']
error=user/'logs/error.log';eb=error.read_bytes();(run/'rc9-external-abandon-amount-error-before.log').write_bytes(eb)
h.press_scan_code(0x29,'rc9-external-abandon-amount-console-open',1)
cmd='effect root = { event_target:eep_native_purge_source = { every_owned_pop_group = { limit = { eep_founder_pop = yes pop_group_size > 0 } export_trigger_value_to_variable = { trigger = pop_group_size variable = eep_abandon_move } event_target:eep_native_purge_source = { set_variable = { which = eep_abandon_amount value = prev.eep_abandon_move } } resettle_pop_group = { POP_GROUP = this PLANET = event_target:eep_seed69_mother AMOUNT = event_target:eep_native_purge_source.eep_abandon_amount } } } }'
h.type_text(cmd,True,'rc9-external-abandon-native-amount-resettle-all100')
r.gpu_capture('rc9-external-abandon-native-amount-resettle-receipt')
h.press_scan_code(0x29,'rc9-external-abandon-amount-console-close',1)
a=r.native_save('rc9-external-abandon-after-amount-all-resettled',b['date'],(0,))
ea=error.read_bytes();(run/'rc9-external-abandon-amount-error-after.log').write_bytes(ea)
c=a['countries']['0']
checks={
 'source_actual_zero':a['colonies'].get('24',{}).get('actual_pop_sum',0)==0,
 'mother_received100':a['colonies']['0']['actual_pop_sum']==7821,
 'owned_population_conserved':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in c['owned_colonies'])==7821,
 'all_stockpiles_same':c['stockpile']==b['countries']['0']['stockpile'],
 'zero_eep_reward':all(c['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),
 'source_not_mod_shattered':a['planets']['84']['planet_class']=='pc_volcanic',
 'no_first_notice':'eep_first_notice' not in c['flags'],
 'bound_mother_kept':next(v for v in a['event_targets'] if v['name']=='eep_core0')['id']==1,
 'no_new_error_bytes':ea==eb,
}
h.write_json(run/'rc9-external-abandon-amount-resettle-proof.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'observed_owned_colonies':c['owned_colonies'],'error_delta_bytes':len(ea)-len(eb),'scope':'Controlled native explicit source-size AMOUNT100 total resettlement. Next real day/month must verify native abandonment and task cleanup; no direct destruction.'})
print(json.dumps({'checks':checks,'save_sha256':a['save_sha256'],'owned_colonies':c['owned_colonies'],'source_population':a['colonies'].get('24',{}).get('actual_pop_sum',0),'mother_population':a['colonies']['0']['actual_pop_sum']}),flush=True)
assert all(checks.values())
