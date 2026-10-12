"""One bounded live UI clock pulse, actual date observed before original manual save."""
import json,logging,re,sys,time
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring/runs/20261009T044016Z'];sys.argv=['runtime']
import runtime as r
from priority_native_reviewed_error_baseline import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();before='terravore-overcap-full-month-22800501';stage='terravore-camera-live-pulse'
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
pre=load(before+'-campaign-v10-proof.json');ex=load(before+'-campaign-guard-v10-execution.json');ba=load(before+'.audit.json')
assert len(pre['checks'])==26 and all(v is True for v in pre['checks'].values()) and not pre['boundaries'] and pre['native_devour_calendar_ready'] and pre['maximum_days_to_native_bite_boundary']==30 and ex['returncode']==0 and ex['helper_sha256']==h.sha256(Path(ex['command'][1])) and pre['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ba['date']=='2280.05.01' and m['language']=='l_simp_chinese'
assert not list(run.glob(stage+'*'));eb=(user/'logs/error.log').read_bytes();assert reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),eb,run);(run/(stage+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x01,stage+'-close-search',1);h.press_scan_code(0x10,stage+'-focus-q',1);events=[]
def space():
 h.win32api.keybd_event(0,0x39,0x0008,0);events.append({'edge':'down','at':time.perf_counter()});time.sleep(.05);h.win32api.keybd_event(0,0x39,0x0008|h.win32con.KEYEVENTF_KEYUP,0);events.append({'edge':'up','at':time.perf_counter()})
space();time.sleep(1.25);space();assert events[-1]['at']-events[0]['at']<1.5
h.write_json(run/(stage+'-pulse.action.json'),{'events':events,'maximum_authorized_native_days':30,'source':'Normal Space pause controls, no fast_forward command or resource grant.'})
f=r.gpu_capture(stage+'-paused-date');labels=[v['text'] for v in f['rows']];dates=[v for v in labels if re.fullmatch(r'2280\.05\.[0-3][0-9]',v)];assert '\u6682\u505c' in labels and len(dates)==1
end=dates[0];days=int(end[-2:])-1;assert 0<=days<=30
h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','start_date':ba['date'],'date':end,'days':days,'evidence_type':'native_live_UI_pause_pulse_actual_OCR_date','image_sha256':f['image_sha256'],'business_preflight':True,'prior_proof_file':before+'-campaign-v10-proof.json','prior_execution_stage':before+'-campaign-guard-v10','live_pulse_events':events,'scope':'Actual live UI clock, not a predetermined fast_forward interval. Original resulting state requires independent checks.'})
a=r.native_save(stage,end,(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);assert reviewed_error_pair(eb,ea,run)
print(json.dumps({'status':'OBSERVED_NATIVE_LIVE_UI_PULSE','days':days,'date':end,'save_sha256':a['save_sha256']}),flush=True)
