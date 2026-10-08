"""Bounded production settlement, actual population conservation is decisive."""
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
b=json.loads((run/'rc9-return-production-original100-restored.audit.json').read_text(encoding='utf-8'))
pre=b
current=json.loads((run/'rc9-return-production-controlled-terminal39.audit.json').read_text(encoding='utf-8'))
assert len(current['situations'])==1 and next(iter(current['situations'].values()))['progress']==39
error=user/'logs/error.log';eb=error.read_bytes();(run/'rc9-return-production-callback-error-before.log').write_bytes(eb)
h.press_scan_code(0x29,'rc9-return-production-callback-console-open',1)
h.type_text('effect root = { every_situation = { limit = { is_situation_type = situation_eep_devouring } situation_event = { id = eep.21 } } }',True,'rc9-return-production-real-completion-check-eep21')
r.gpu_capture('rc9-return-production-callback-console-receipt')
h.press_scan_code(0x29,'rc9-return-production-callback-console-close',1)
a=r.native_save('rc9-return-production-terminal39-callback',b['date'],(0,))
ea=error.read_bytes();(run/'rc9-return-production-callback-error-after.log').write_bytes(ea)
assert ea.startswith(eb);(run/'rc9-return-production-callback-error-delta.log').write_bytes(ea[len(eb):])
c=a['countries']['0'];v=c['variables']
checks={'actual_mother8021':a['colonies']['0']['actual_pop_sum']==8021,'actual_owned_total8021':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in c['owned_colonies'])==8021,'source_zero':a['colonies']['24']['actual_pop_sum']==0,'source_shattered':a['planets']['84']['planet_class']=='pc_shattered','one_world_ledger':{k:v.get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']}=={'eep_c':16,'eep_g':16,'eep_d':6,'eep_made':200,'eep_worlds':1},'recorded_return100':v.get('eep_last_return')==100,'original_stockpiles_same':c['stockpile']==pre['countries']['0']['stockpile'],'no_task':not a['situations'],'no_new_error_bytes':ea==eb}
result={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':pre['save_sha256'],'after_sha256':a['save_sha256'],'actual_mother':a['colonies']['0']['actual_pop_sum'],'expected_mother':8021,'error_delta_bytes':len(ea)-len(eb),'scope':'Controlled same-day terminal39 of a real formal100 seed task; directly checks actual total population, not natural-calendar completion.'}
h.write_json(run/'rc9-return-production-callback-conservation-proof.json',result)
print(json.dumps(result),flush=True)
assert all(checks.values())
