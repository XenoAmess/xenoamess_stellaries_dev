"""One documented normal Ctrl+left client click; no game commands/calendar."""
import ctypes,json,logging,sys,time
from datetime import datetime,timezone
stage,rx,ry=sys.argv[1:];x,y=int(rx),int(ry)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();out=run/(stage+'.action.json');assert not out.exists()
pid=h.process_record(run)['pid'];hwnd=h.focus_pid(pid);assert h.win32gui.GetForegroundWindow()==hwnd
rect=h.win32gui.GetClientRect(hwnd);assert 0<=x<rect[2] and 0<=y<rect[3]
point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(*point,duration=.1);time.sleep(.25)
h.pyautogui.keyDown('ctrl')
try:
    h.pyautogui.mouseDown(button='left')
    try:time.sleep(.15)
    finally:h.pyautogui.mouseUp(button='left')
finally:h.pyautogui.keyUp('ctrl')
time.sleep(.15)
released=(ctypes.windll.user32.GetAsyncKeyState(0x11)&0x8000)==0
foreground=h.win32gui.GetForegroundWindow();action={'action':'ctrl-left-click','stage':stage,'client_point':[x,y],'desktop_point':list(point),'pid':pid,'expected_hwnd':hwnd,'foreground_after':foreground,'ctrl_released':released,'at_utc':datetime.now(timezone.utc).isoformat()}
h.write_json(out,action);print(json.dumps(action),flush=True);assert released and foreground==hwnd
