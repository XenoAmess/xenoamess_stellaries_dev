"""One normal native paid capital upgrade in empty-mod diagnostic world."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
pre=json.loads((run/'coordinator-control-loaded-proof.json').read_text('utf-8'));ho=json.loads((run/'coordinator-control-hover-observation.json').read_text('utf-8'));ex=json.loads((run/'coordinator-control-hover-observe-execution.json').read_text('utf-8'));assert all(pre['checks'].values()) and pre['status']=='PASS_COORDINATOR_CONTROL_LOAD_ONLY' and ex['returncode']==0 and ho['before_sha256']==ho['after_sha256']==pre['after_sha256'] and ho['new_error_bytes']==0
stage='coordinator-control-paid';assert not list(run.glob(stage+'*'));eb=(user/'logs/error.log').read_bytes();assert eb==(run/'coordinator-control-hover-error-after.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
r.gpu_click(904,233,stage+'-normal-mother-open');r.gpu_scroll(0,151,335,stage+'-upgrade-hover',1);f=r.gpu_capture(stage+'-native-quote');assert any(h.normalized(v['text'])=='343480' for v in f['rows']),'No exact current native343/480 quote; no purchase'
r.gpu_click(151,335,stage+'-normal-upgrade-click-once');a=r.native_save(stage,'2238.10.02',(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
p={'status':'OBSERVED_NATIVE_PAID_CAPITAL_CONTROL','before_sha256':ho['after_sha256'],'after_sha256':a['save_sha256'],'image_sha256':f['image_sha256'],'new_error_bytes':len(ea)-len(eb),'scope':'One normal480-mineral native upgrade click then same-day save, empty-mod diagnosis. No grants/calendar. Independent attribution required.'};h.write_json(run/(stage+'-observation.json'),p);print(json.dumps(p),flush=True)
