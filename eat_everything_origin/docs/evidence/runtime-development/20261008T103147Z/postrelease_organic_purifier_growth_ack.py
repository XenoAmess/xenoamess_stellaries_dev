import json,logging,re,shutil,sys,time,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-purifier-growth-normal-pending';stage='organic-purifier-growth-acknowledged';b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
h.pyautogui.moveTo(*r.desktop_point(805,665));time.sleep(.5);f=r.gpu_capture(stage+'-clean-Queen-CG');labels=[x['text'] for x in f['rows']];assert '\u788e\u661f\u4e4b\u51a0' in labels
rows=[x for x in f['rows'] if x['text']=='\u8ba9\u4ed6\u4eec\u6210\u4e3a\u5730\u57fa\u3002' and x['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4);hwnd=h.focus_pid(h.process_record(run)['pid']);assert h.win32gui.GetForegroundWindow()==hwnd;desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE;started=time.monotonic_ns()
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-physical-option.action.json'),{'action':'actual_click_immediate_physical_ESC','client_point':[x,y],'source_image_sha256':f['image_sha256'],'elapsed_ns':time.monotonic_ns()-started})
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-final.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_ledger_same':ca['variables']==cb['variables'],'EEP_flags_same':ca['flags']==cb['flags'],'no_new_errors':eb==ea}
for k in ('completed_technologies','research_queues','traditions','ascension_perks','government'):checks[k+'_same']=ca[k]==cb[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets'):checks[k+'_same']=a[k]==b[k]
def native_events(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:text=z.read('gamestate').decode('utf-8-sig')
 pending=[q.scalars(v) for k,v,obj in q.fields(text) if k=='player_event' and obj]
 history=q.block(text,'open_player_event_selection_history');selections=re.findall(r'\{\s*player_event=(\d+)\s*human=(-?\d+)\s*option=(\d+)\s*\}',history)
 return pending,selections,history
bp,bh,braw=native_events(start);ap,ah,araw=native_events(stage);growth=[e for e in bp if e.get('event')=='eep.13' and e.get('country')==0];checks['actual_pending_growth_event_once']=len(growth)==1
gid=str(growth[0]['id']) if len(growth)==1 else '';checks['growth_pending_removed']=not any(str(e.get('id'))==gid for e in ap);checks['all_other_pending_same']=[e for e in bp if str(e.get('id'))!=gid]==ap;checks['exact_one_human_selection']=ah==bh+[(gid,'1','0')]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_growth_event':growth,'history_before':braw,'history_after':araw,'scope':'Actual Queen growth option at same paused date; no calendar/reward repeat, strict snapshot preservation.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original Queen ACK FAIL retained'
