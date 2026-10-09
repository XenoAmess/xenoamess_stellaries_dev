import json, logging, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'eat_everything_origin/tools'); sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO); h=r.harness; run,user,m=h.load_run()
assert m['role']=='Post-release organic Fanatic Purifier natural continuation'
shutil.copyfile(Path(__file__),run/Path(__file__).name)
stage='organic-purifier-2284-event-paid'
b=json.loads((run/'organic-purifier-2284-event-before.audit.json').read_text(encoding='utf-8'))
eb=(user/'logs/error.log').read_bytes(); (run/(stage+'-error-before.log')).write_bytes(eb)
f=r.gpu_capture(stage+'-actual-option')
rows=[x for x in f['rows'] if x['text']=='\u732e\u51fa\u8d21\u54c1\uff08\u80fd\u6e90\uff09' and x['score']>=.8]
assert len(rows)==1 and b['date']=='2284.01.12' and b['countries']['0']['stockpile']['energy']>=250
row=rows[0]; x=round(sum(p[0] for p in row['box'])/4); y=round(sum(p[1] for p in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid'])); assert h.win32gui.GetForegroundWindow()==hwnd
desktop=h.win32gui.ClientToScreen(hwnd,(x,y)); old=h.pyautogui.PAUSE; started=time.monotonic_ns()
try:
 h.pyautogui.PAUSE=0; h.pyautogui.click(*desktop)
 h.win32api.keybd_event(0,0x01,0x0008,0); h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally: h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-click-and-native-menu.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'desktop_point':list(desktop),'foreground_hwnd':hwnd,'source_image_sha256':f['image_sha256'],'elapsed_ns':time.monotonic_ns()-started})
a=r.native_save(stage,b['date'],(0,)); cb,ca=b['countries']['0'],a['countries']['0']
checks={'same_date':b['date']==a['date'],'energy_paid_250':abs(cb['stockpile']['energy']-ca['stockpile']['energy']-250)<1e-5,'other_stock_same':{k:v for k,v in cb['stockpile'].items() if k!='energy'}=={k:v for k,v in ca['stockpile'].items() if k!='energy'},'EEP_variables_same':cb['variables']==ca['variables']}
for k in ('completed_technologies','research_queues','traditions','ascension_perks'): checks[k+'_same']=cb[k]==ca[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'): checks[k+'_same']=b[k]==a[k]
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);checks['no_new_errors']=eb==ea
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'energy_before':cb['stockpile']['energy'],'energy_after':ca['stockpile']['energy'],'scope':'Actual native marauder tribute payment only; no calendar replay or compensation.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original payment FAIL retained'
f=r.gpu_capture(stage+'-after-ui');print(json.dumps({'labels':[x['text'] for x in f['rows']]}),flush=True)
