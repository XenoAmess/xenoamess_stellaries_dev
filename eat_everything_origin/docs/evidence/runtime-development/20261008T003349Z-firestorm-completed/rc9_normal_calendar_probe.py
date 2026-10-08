import json,logging,re,shutil,sys,time
from pathlib import Path
start,stage,seconds=sys.argv[1:];seconds=float(seconds);assert 0<seconds<=30
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();copy=run/Path(__file__).name
if not copy.exists():shutil.copyfile(Path(__file__),copy)
assert copy.read_bytes()==Path(__file__).read_bytes()
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'))
def current_date(frame):
 rows=[x for x in frame['rows'] if min(p[1] for p in x['box'])<25 and min(p[0] for p in x['box'])>880 and re.fullmatch(r'\d{4}\.\d{2}\.\d{2}',x['text'])]
 assert len(rows)==1
 return rows[0]['text']
before=r.gpu_capture(stage+'-before-normal-clock')
assert current_date(before)==b['date']
assert any(x['text']=='\u6682\u505c' for x in before['rows'])
h.press_scan_code(0x39,stage+'-native-unpause',1)
time.sleep(seconds)
h.press_scan_code(0x39,stage+'-native-pause',1)
after=r.gpu_capture(stage+'-after-normal-clock')
if not any(x['text']=='\u6682\u505c' for x in after['rows']):
 h.press_scan_code(0x39,stage+'-native-pause-confirmed-running',1)
 after=r.gpu_capture(stage+'-confirmed-paused-clock')
assert any(x['text']=='\u6682\u505c' for x in after['rows'])
date=current_date(after)
a=r.native_save(stage,date,(0,))
checks={'actual_date_advanced':a['date']>b['date'],'zero_eep_award_kept':all(a['countries']['0']['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds'])}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'before_date':b['date'],'after_date':a['date'],'seconds_requested':seconds,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Native unpause/pause observed calendar advance only; actual combat/bombardment requires separate native-state analysis.'}
h.write_json(run/(stage+'-normal-calendar-proof.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values())
