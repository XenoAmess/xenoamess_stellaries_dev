"""Normal native capital tooltip followed by same-day save, empty-mod diagnosis."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
pre=json.loads((run/'coordinator-control-loaded-proof.json').read_text('utf-8'));ex=json.loads((run/'coordinator-control-load-execution.json').read_text('utf-8'));assert all(pre['checks'].values()) and pre['status']=='PASS_COORDINATOR_CONTROL_LOAD_ONLY' and ex['returncode']==0
stage='coordinator-control-hover';assert not list(run.glob(stage+'*'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
r.gpu_click(904,233,stage+'-normal-mother-open');r.gpu_scroll(0,151,335,stage+'-upgrade-hover',1);f=r.gpu_capture(stage+'-native-quote')
a=r.native_save(stage,'2238.10.02',(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
p={'status':'OBSERVED_NATIVE_TOOLTIP_ONLY','before_sha256':pre['after_sha256'],'after_sha256':a['save_sha256'],'image_sha256':f['image_sha256'],'new_error_bytes':len(ea)-len(eb),'scope':'Normal mother UI and capital upgrade hover followed by native same-day save. No paid click, effect or calendar. Independent attribution required.'};h.write_json(run/(stage+'-observation.json'),p);print(json.dumps(p),flush=True)
