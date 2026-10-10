"""Normal client-coordinate double-click navigation; no console or state edits."""
import json,logging,shutil,sys,time
from pathlib import Path
from datetime import datetime,timezone
stage,x,y=sys.argv[1:];x,y=int(x),int(y)
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
out=run/(stage+'.action.json');assert not out.exists();pid=h.process_record(run)['pid'];hwnd=h.focus_pid(pid)
rect=h.win32gui.GetClientRect(hwnd);assert 0<=x<rect[2] and 0<=y<rect[3]
point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(*point,duration=.1);time.sleep(.25);clicks=[]
for n in range(2):
 h.pyautogui.mouseDown(button='left')
 try:time.sleep(.12)
 finally:h.pyautogui.mouseUp(button='left')
 clicks.append({'index':n,'at_utc':datetime.now(timezone.utc).isoformat()})
 if n==0:time.sleep(.08)
assert h.win32gui.GetForegroundWindow()==hwnd
action={'action':'double-click','stage':stage,'pid':pid,'client_point':[x,y],'desktop_point':list(point),'client_rect':list(rect),'clicks':clicks,'hold_seconds':.12,'interval_seconds':.08,'expected_hwnd':hwnd,'foreground_after':h.win32gui.GetForegroundWindow()}
h.write_json(out,action);print(json.dumps(action),flush=True)
