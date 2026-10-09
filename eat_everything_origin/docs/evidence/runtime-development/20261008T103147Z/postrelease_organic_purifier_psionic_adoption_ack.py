import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
stage='organic-psionic-adoption-ack';b=json.loads((run/'organic-psionic-tradition-adopted.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
h.pyautogui.moveTo(700,670);f=r.gpu_capture(stage+'-actual-native-option');label='\u4e5f\u8bb8\u77a5\u89c1\u4e86\u7b49\u5f85\u7740\u6211\u4eec\u7684\u672a\u6765\u3002'
rows=[v for v in f['rows'] if v['text']==label and v['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(v[0] for v in row['box'])/4);y=round(sum(v[1] for v in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-native-click.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'source_image_sha256':f['image_sha256'],'actual_option':label})
a=r.native_save(stage,b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb}
for k in ('stockpile','effective_stockpile','research_stockpile','tech_status','variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government','native'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets'):checks[k+'_held']=b[k]==a[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Native latent-psionic adoption event acknowledgement only; no extra payment, population or EEP award.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original native adoption ACK failure retained'
f=r.gpu_capture(stage+'-after-native-ui');print(json.dumps({'image':str(f['image']),'rows':[v['text'] for v in f['rows']]}),flush=True)
