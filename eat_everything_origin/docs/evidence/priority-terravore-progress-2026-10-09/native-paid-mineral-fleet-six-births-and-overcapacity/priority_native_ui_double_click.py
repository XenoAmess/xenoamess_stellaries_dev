"""One normal native double click with documented held mouse inputs."""
import json,logging,sys,time
from datetime import datetime,timezone
stage,raw_x,raw_y=sys.argv[1:];x,y=int(raw_x),int(raw_y)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();hwnd=h.focus_pid(h.process_record(run)['pid']);rect=h.win32gui.GetClientRect(hwnd);assert 0<=x<rect[2] and 0<=y<rect[3]
point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(*point,duration=.1);time.sleep(.25)
for i in range(2):
 h.pyautogui.mouseDown();time.sleep(.15);h.pyautogui.mouseUp()
 if i==0:time.sleep(.1)
out=run/(stage+'.action.json');assert not out.exists();action={'action':'native-double-click','stage':stage,'client_point':[x,y],'hold_seconds':.15,'between_clicks_seconds':.1,'at_utc':datetime.now(timezone.utc).isoformat(),'foreground_after':h.win32gui.GetForegroundWindow(),'expected_hwnd':hwnd};assert action['foreground_after']==hwnd;h.write_json(out,action);print(json.dumps(action),flush=True)
