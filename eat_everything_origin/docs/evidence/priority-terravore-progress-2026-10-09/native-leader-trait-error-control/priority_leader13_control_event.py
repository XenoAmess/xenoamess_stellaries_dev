"""One explicit native fleet event in independent empty-mod diagnostic only."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(__file__,run/Path(__file__).name)
pre=json.loads((run/'leader13-control-loaded-proof.json').read_text('utf-8'));assert pre['status']=='PASS_LEADER13_CONTROL_LOAD_ONLY' and all(pre['checks'].values()) and h.sha256(run/'leader13-control-loaded.sav')==pre['after_sha256']
stage='leader13-control-event';b=json.loads((run/'leader13-control-loaded.audit.json').read_text('utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
command='event leader.13 565';h.press_scan_code(0x29,stage+'-console-open',1);h.type_text(command,True,stage+'-one-native-event');f=r.gpu_capture(stage+'-command-receipt');h.press_scan_code(0x29,stage+'-console-close',1)
a=r.native_save(stage,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
p={'status':'OBSERVED_CONTROLLED_NATIVE_LEADER_EVENT_ONLY','command':command,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_date':a['date'],'receipt_image_sha256':f['image_sha256'],'new_error_bytes':len(ea)-len(eb),'scope':'One explicit original-game fleet event with empty enabled_mods. No calendar, production mutation or natural acceptance claim.'};h.write_json(run/(stage+'-observation.json'),p);print(json.dumps(p),flush=True)
