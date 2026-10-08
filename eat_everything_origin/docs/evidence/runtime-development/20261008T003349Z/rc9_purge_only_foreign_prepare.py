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
b=json.loads((run/'rc9-external-purge-task-ready.audit.json').read_text(encoding='utf-8'))
assert b['colonies']['24']['actual_pop_sum']==100
h.press_scan_code(0x29,'rc9-external-purge-foreign100-console-open',1)
commands=[
 'effect root = { random_country = { limit = { is_country_type = default is_gestalt = no owner_main_species = { has_trait = trait_organic NOT = { has_trait = trait_hive_mind } } } owner_main_species = { save_global_event_target_as = eep_native_purge_species } } }',
 'effect root = { event_target:eep_native_purge_source = { create_pop_group = { species = event_target:eep_native_purge_species size = 100 } } }',
]
for n,cmd in enumerate(commands):h.type_text(cmd,True,'rc9-external-purge-controlled-foreign100-'+str(n))
r.gpu_capture('rc9-external-purge-foreign100-native-receipt')
h.press_scan_code(0x29,'rc9-external-purge-foreign100-console-close',1)
a=r.native_save('rc9-external-purge-foreign100-before-controls',b['date'],(0,))
sid=next(v['id'] for v in a['event_targets'] if v['name']=='eep_native_purge_species')
source_groups=[a['pop_groups'][str(i)] for i in a['colonies']['24']['pop_groups']]
checks={
 'source200':a['colonies']['24']['actual_pop_sum']==200,
 'actual_foreign100':sum(v['size'] for v in source_groups if v['key']['species']==sid)==100,
 'actual_founder100':sum(v['size'] for v in source_groups if v['key']['species']!=sid)==100,
 'mother7721':a['colonies']['0']['actual_pop_sum']==7721,
 'original_stockpiles_same':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'ledger_same':all(a['countries']['0']['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),
 'task_still0':a['situations']==b['situations'],
}
h.write_json(run/'rc9-external-purge-foreign100-precondition-proof.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':a['save_sha256'],'actual_species_id':sid,'scope':'Controlled actual ordinary non-hive organic species100 only; rights, native population control and natural purge still required.'})
print(json.dumps({'checks':checks,'save_sha256':a['save_sha256'],'species':sid}),flush=True)
assert all(checks.values())
