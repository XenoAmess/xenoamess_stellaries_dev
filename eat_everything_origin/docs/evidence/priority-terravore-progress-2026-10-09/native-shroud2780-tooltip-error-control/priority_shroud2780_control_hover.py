"""Only native existing2780 option hover in empty-mod control; no selection."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
pre=json.loads((run/'shroud2780-control-loaded-supplement.json').read_text('utf-8'));assert pre['status']=='PASS_NATIVE2780_CONTROL_LOAD_SUPPLEMENT' and all(pre['checks'].values()) and json.loads((run/'shroud2780-control-load-supplement-execution.json').read_text('utf-8'))['returncode']==0
stage='shroud2780-control-hover';assert not list(run.glob(stage+'*'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
r.gpu_scroll(0,510,597,stage+'-option-hover',1);f=r.gpu_capture(stage+'-option-tooltip-ui');assert any(x['text']=='\u5927\u89c9\u9192' for x in f['rows'])
a=r.native_save(stage,'2254.11.02',(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
p={'status':'OBSERVED_NATIVE2780_TOOLTIP_ONLY','before_sha256':pre['after_sha256'],'after_sha256':a['save_sha256'],'image_sha256':f['image_sha256'],'new_error_bytes':len(ea)-len(eb),'scope':'Only existing native2780 option hovered once and native same-date save. No event/effect/selection/calendar. Independent full-body attribution required.'};h.write_json(run/(stage+'-observation.json'),p);print(json.dumps(p),flush=True)
