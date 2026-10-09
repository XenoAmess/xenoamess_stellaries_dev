import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='organic-mine4-completed';stage='organic-mine4-native-crime-ack';b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
def raw(stem):
 with zipfile.ZipFile(run/(stem+'.sav')) as z:return z.read('gamestate').decode('utf-8-sig')
def pending(t):return [q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
def history(t):return [q.scalars(v) for k,v,o in q.fields(q.block(q.block(t,'open_player_event_selection_history'),'selected')) if o]
bt=raw(before);bp=pending(bt);assert len(bp)==1 and bp[0]['id']==420 and bp[0]['event']=='crime.40'
f=r.gpu_capture(stage+'-actual-option');rows=[v for v in f['rows'] if v['text']=='\u771f\u662f\u4ee4\u4eba\u5fcd\u65e0\u53ef\u5fcd\u3002' and v['score']>=.8];assert len(rows)==1
box=rows[0]['box'];x=round(sum(p[0] for p in box)/4);y=round(sum(p[1] for p in box)/4);hwnd=h.focus_pid(int(h.process_record(run)['pid']));desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-click.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'source_image_sha256':f['image_sha256']})
a=r.native_save(stage,b['date'],(0,));ac,bc=a['countries']['0'],b['countries']['0'];at=raw(stage);ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'actual_pending420_removed':not pending(at),'actual_human_option0_once':history(at)==history(bt)+[{'player_event':420,'human':1,'option':0}]}
for k in ('effective_stockpile','research_stockpile','tech_status','variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government','owned_colonies'):checks[k+'_held']=ac[k]==bc[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_held']=a[k]==b[k]
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_history_before':history(bt),'actual_history_after':history(at),'scope':'Normal same-date native crime40 option ACK; existing criminal effects remain. No calendar/payment/reward replay or full route acceptance.'};h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original crime ACK failure retained'
