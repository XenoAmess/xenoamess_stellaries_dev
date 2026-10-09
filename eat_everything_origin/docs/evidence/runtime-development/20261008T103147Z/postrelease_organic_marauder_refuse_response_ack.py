import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
stage='organic-third-marauder-refuse-response-ack';b=json.loads((run/'organic-third-marauder-expired-demand-refused.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-response');labels=[v['text'] for v in f['rows']];assert any('\u65e2\u7136\u4f60\u4eec\u4e0d\u80af\u4e3b\u52a8\u732e\u51fa\u8d21\u54c1' in v for v in labels)
rows=[v for v in f['rows'] if v['text']=='\u786e\u8ba4' and v['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(v[0] for v in row['box'])/4);y=round(sum(v[1] for v in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-click.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'source_image_sha256':f['image_sha256']})
a=r.native_save(stage,b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb}
for k in ('stockpile','effective_stockpile','research_stockpile','tech_status','variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_held']=b[k]==a[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Same-date native diplomatic response acknowledgement only. No calendar or reward replay.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original response failure retained'
