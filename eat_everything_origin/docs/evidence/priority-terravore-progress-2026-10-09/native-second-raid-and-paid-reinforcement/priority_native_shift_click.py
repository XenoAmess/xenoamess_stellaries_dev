"""One normal physical Shift + client left click, guaranteed modifier release."""
import json,logging,shutil,sys,time
from datetime import datetime,timezone
from pathlib import Path
stage,rx,ry=sys.argv[1:];x,y=int(rx),int(ry);sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
out=run/(stage+'.action.json');assert not out.exists();pid=h.process_record(run)['pid'];hwnd=h.focus_pid(pid);rect=h.win32gui.GetClientRect(hwnd);assert 0<=x<rect[2] and 0<=y<rect[3];point=h.win32gui.ClientToScreen(hwnd,(x,y))
h.pyautogui.moveTo(*point,duration=.1);time.sleep(.25);h.win32api.keybd_event(0,0x2a,0x0008,0)
try:
 time.sleep(.1);h.pyautogui.mouseDown(button='left');time.sleep(.15)
finally:
 h.pyautogui.mouseUp(button='left');h.win32api.keybd_event(0,0x2a,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
p={'action':'normal_physical_shift_left_click','stage':stage,'pid':pid,'modifier_scan':42,'modifier_released':True,'client_point':[x,y],'at_utc':datetime.now(timezone.utc).isoformat(),'foreground_after':h.win32gui.GetForegroundWindow(),'expected_hwnd':hwnd};assert p['foreground_after']==hwnd;h.write_json(out,p);print(json.dumps(p),flush=True)
