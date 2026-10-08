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
b=json.loads((run/'rc9-external-purge-native-paid-growth-control.audit.json').read_text(encoding='utf-8'))
assert 'planet_population_control_gestalt' in b['planets']['84']['modifiers']
sid=next(v['id'] for v in b['event_targets'] if v['name']=='eep_native_purge_species')
source_groups=[b['pop_groups'][str(i)] for i in b['colonies']['24']['pop_groups']]
actual_founder_sizes=sorted(v['size'] for v in source_groups if v['key']['species']!=sid)
assert sum(actual_founder_sizes)==100
assert len(actual_founder_sizes)==len(set(actual_founder_sizes))
error=user/'logs/error.log';eb=error.read_bytes();(run/'rc9-external-purge-founder-move-error-before.log').write_bytes(eb)
h.press_scan_code(0x29,'rc9-external-purge-founder-move-console-open',1)
for size in actual_founder_sizes:
 cmd='effect root = { event_target:eep_native_purge_source = { random_owned_pop_group = { limit = { eep_founder_pop = yes pop_group_size = '+str(size)+' } resettle_pop_group = { POP_GROUP = this PLANET = event_target:eep_seed69_mother AMOUNT = '+str(size)+' } } } }'
 h.type_text(cmd,True,'rc9-external-purge-native-founder-resettle'+str(size))
 r.gpu_capture('rc9-external-purge-founder-move-receipt-'+str(size))
h.press_scan_code(0x29,'rc9-external-purge-founder-move-console-close',1)
a=r.native_save('rc9-external-purge-only-foreign100-ready',b['date'],(0,))
ea=error.read_bytes();(run/'rc9-external-purge-founder-move-error-after.log').write_bytes(ea)
source_groups=[a['pop_groups'][str(i)] for i in a['colonies']['24']['pop_groups']]
checks={
 'only_actual_foreign100':a['colonies']['24']['actual_pop_sum']==100 and all(v['key']['species']==sid for v in source_groups),
 'mother_received100':a['colonies']['0']['actual_pop_sum']==7821,
 'controlled_total_population_conserved':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in a['countries']['0']['owned_colonies'])==7921,
 'growth_control_still_present':'planet_population_control_gestalt' in a['planets']['84']['modifiers'],
 'all_stockpiles_same':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'zero_eep_reward':all(a['countries']['0']['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),
 'task_still0':a['situations']==b['situations'],
 'no_new_error_bytes':ea==eb,
}
h.write_json(run/'rc9-external-purge-only-foreign100-preconditions.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':a['save_sha256'],'actual_species_id':sid,'error_delta_bytes':len(ea)-len(eb),'scope':'Controlled independent constant-size native founder resettlements based on actual post-decision groups after actual paid growth control; foreign decline remains native.'})
print(json.dumps({'checks':checks,'save_sha256':a['save_sha256'],'source_groups':source_groups}),flush=True)
assert all(checks.values())
