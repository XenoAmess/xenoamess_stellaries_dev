import json,logging,shutil,sys,time
from decimal import Decimal
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
stage='organic-mine3-marauder-paid';b=json.loads((run/'organic-mine3-marauder-before.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-native-price');labels=[v['text'] for v in f['rows']];assert '\u8d44\u6e90\uff1a-250.00' in labels
rows=[v for v in f['rows'] if v['text']=='\u732e\u51fa\u8d21\u54c1\uff08\u80fd\u6e90\uff09' and v['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(v[0] for v in row['box'])/4);y=round(sum(v[1] for v in row['box'])/4)
assert b['countries']['0']['effective_stockpile']['energy']>=250 and b['date']=='2296.08.02'
hwnd=h.focus_pid(int(h.process_record(run)['pid']));assert h.win32gui.GetForegroundWindow()==hwnd;desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-payment.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'source_image_sha256':f['image_sha256'],'actual_displayed_energy_cost':250})
a=r.native_save(stage,b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'actual_energy_paid250':Decimal(str(bc['effective_stockpile']['energy']))-Decimal(str(ac['effective_stockpile']['energy']))==250,
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='energy'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='energy'},
 'native_research_banks_held':bc['research_stockpile']==ac['research_stockpile'],'complete_tech_status_held':bc['tech_status']==ac['tech_status'],'no_new_errors':ea==eb}
for k in ('variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'auditor_sha256':a['audit_tool_sha256'],
 'actual_energy_before':bc['effective_stockpile']['energy'],'actual_energy_after':ac['effective_stockpile']['energy'],
 'raw_mirror_changes':{k:[bc['stockpile'].get(k),v] for k,v in ac['stockpile'].items() if bc['stockpile'].get(k)!=v},
 'scope':'Real native marauder payment at existing calendar endpoint; no day replay or resource compensation.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original payment failure retained; do not repeat'
f=r.gpu_capture(stage+'-after-ui');print(json.dumps({'image':str(f['image']),'rows':[v['text'] for v in f['rows']]}),flush=True)
