import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
stage='organic-temple-storm-year1-pending-recovery';original='organic-temple-storm-year1';receipt=json.loads((run/(original+'-calendar-execution.json')).read_text(encoding='utf-8'));assert receipt['status']=='FAILED_CALENDAR_HELPER'
f=r.gpu_capture(stage+'-actual-occluded-endpoint');labels=[v['text'] for v in f['rows']];assert '2309.05.02' in labels and '\u6682\u505c' in labels
h.press_scan_code(0x29,stage+'-console-close',1)
if 'Debug View' in labels:h.click_point(538,347,stage+'-close-visible-debug-view')
shutil.copyfile(run/(original+'-error-before.log'),run/(stage+'-error-before.log'))
a=r.native_save(stage,'2309.05.02',(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots=list(q.fields(t));pending=[{'native':q.scalars(v),'raw_scope':q.block(v,'scope')} for k,v,o in roots if k=='player_event' and o and q.scalars(v).get('country')==0]
p={'status':'OBSERVED_RECOVERED_DATE_PENDING_REVIEW','date':a['date'],'save_sha256':a['save_sha256'],'native_pending':pending,'new_error_bytes':len(ea)-len((run/(original+'-error-before.log')).read_bytes()),'error_raw_held':ea==(run/(original+'-error-before.log')).read_bytes(),'original_calendar_returncode':receipt['returncode'],'scope':'Normal native save after stopping only occluded receipt polling; no calendar/resource/trait grant or event choice.'};h.write_json(run/(stage+'-observation.json'),p);print(json.dumps(p),flush=True)
