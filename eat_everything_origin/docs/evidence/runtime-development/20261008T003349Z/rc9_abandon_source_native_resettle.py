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
h.press_scan_code(0x29,'rc9-external-abandon-resettle-console-open',1)
h.type_text('effect root = { event_target:eep_native_purge_source = { every_owned_pop_group = { limit = { eep_founder_pop = yes } resettle_pop_group = { POP_GROUP = this PLANET = event_target:eep_seed69_mother PERCENTAGE = 1 } } } }',True,'rc9-external-abandon-native-resettle-all100')
r.gpu_capture('rc9-external-abandon-native-resettle-receipt')
h.press_scan_code(0x29,'rc9-external-abandon-resettle-console-close',1)
a=r.native_save('rc9-external-abandon-after-last-founder-resettled',b['date'],(0,))
c=a['countries']['0']
checks={'only_mother_owned':c['owned_colonies']==[0],'source_actual_zero':a['colonies'].get('24',{}).get('actual_pop_sum',0)==0,'mother_received100':a['colonies']['0']['actual_pop_sum']==7821,'all_stockpiles_same':c['stockpile']==b['countries']['0']['stockpile'],'zero_eep_reward':all(c['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),'source_not_mod_shattered':a['planets']['84']['planet_class']=='pc_volcanic','no_first_notice':'eep_first_notice' not in c['flags'],'bound_mother_kept':next(v for v in a['event_targets'] if v['name']=='eep_core0')['id']==1}
h.write_json(run/'rc9-external-abandon-resettle-proof.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Native last-founder resettlement caused colony abandonment. Next real day/month callback still required.'})
print(json.dumps({'checks':checks,'save_sha256':a['save_sha256'],'source':a['planets']['84'],'tasks':a['situations']}),flush=True)
assert all(checks.values())
