import json, logging, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-purifier-2287-adaptive-ecology-paid';stage='organic-purifier-2287-MOM-adopted'
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-option');assert '\u4f60\u786e\u8ba4\u8981\u9009\u62e9\u5fc3\u80dc\u4e8e\u7269\u5417\uff1f' in [x['text'] for x in f['rows']]
rows=[x for x in f['rows'] if x['text']=='\u662f' and x['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));assert h.win32gui.GetForegroundWindow()==hwnd
desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE;started=time.monotonic_ns()
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-actual-ack.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'desktop_point':list(desktop),'source_image_sha256':f['image_sha256'],'elapsed_ns':time.monotonic_ns()-started})
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0']
checks={'same_date':a['date']==b['date'],'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_variables_same':ca['variables']==cb['variables'],'no_new_errors':eb==(user/'logs/error.log').read_bytes()}
checks['expected_third_AP_only']=ca['ascension_perks']==cb['ascension_perks']+['ap_mind_over_matter']
checks['legal_government_same']=ca['government']==cb['government']
for k in ('completed_technologies','research_queues','traditions'):checks[k+'_same']=cb[k]==ca[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=b[k]==a[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Actual native legal third Mind over Matter AP only; psionic research and full ascension pending.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original response FAIL retained'
f=r.gpu_capture(stage+'-after-ui');print(json.dumps({'labels':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
