import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
stage='organic-mine3-marauder-ack';b=json.loads((run/'organic-mine3-marauder-paid.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-response');labels=[v['text'] for v in f['rows']];assert any('\u4f60\u4eec\u7684\u4eba\u6c11\u5b89\u5168\u4e86' in v for v in labels)
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
h.press_scan_code(0x29,stage+'-existing-console-open',1);f=r.gpu_capture(stage+'-existing-240day-receipt');labels=[v['text'] for v in f['rows']]
checks={'actual_date':b['date']=='2296.08.02' and b['date'] in labels,'actual_paused':'\u6682\u505c' in labels,'existing_complete240day_receipt':any(h.normalized(v).startswith('fastforwarded240day') for v in labels)}
h.write_json(run/'organic-mine3-existing-calendar-receipt-recovery.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'image_sha256':f['image_sha256'],'original_failed_stage':'organic-paid-mine3-completed','original_start_date':'2295.12.02','actual_end_date':a['date'],'days_already_executed':240,'no_days_repeated':True,'end_save_sha256':a['save_sha256'],'visible_receipt_labels':[v for v in labels if 'fastforward' in h.normalized(v)]});print(json.dumps({'receipt_checks':checks}),flush=True);assert all(checks.values()),'Existing receipt recovery failed, never repeat days'
h.press_scan_code(0x29,stage+'-existing-console-close',1)
