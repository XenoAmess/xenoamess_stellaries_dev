"""One ordinary foreground double click for native camera/navigation UI."""
import json,logging,shutil,sys,time
from datetime import datetime,timezone
from pathlib import Path
stage,x,y=sys.argv[1:];x=int(x);y=int(y)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
out=run/(stage+'.action.json');assert not out.exists();pid=h.process_record(run)['pid'];hwnd=h.focus_pid(pid);rect=h.win32gui.GetClientRect(hwnd);assert 0<=x<rect[2] and 0<=y<rect[3]
h.pyautogui.moveTo(*h.win32gui.ClientToScreen(hwnd,(x,y)),duration=.1);time.sleep(.25);h.pyautogui.doubleClick(interval=.1,button='left');assert h.win32gui.GetForegroundWindow()==hwnd
v={'action':'ordinary_double_left_click','stage':stage,'pid':pid,'client_point':[x,y],'interval_seconds':.1,'at_utc':datetime.now(timezone.utc).isoformat(),'scope':'Native camera/navigation activation only. No calendar or grants.'};h.write_json(out,v);print(json.dumps(v),flush=True)
