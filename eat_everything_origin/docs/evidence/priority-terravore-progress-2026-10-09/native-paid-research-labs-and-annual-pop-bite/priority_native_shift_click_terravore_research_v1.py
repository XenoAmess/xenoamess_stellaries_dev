"""One focused native Shift+left-click; always releases Shift and mouse."""
import json,logging,sys,time
stage,x,y=sys.argv[1:];x,y=int(x),int(y)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();hwnd=h.focus_pid(h.process_record(run)['pid']);rect=h.win32gui.GetClientRect(hwnd)
assert m['language']=='l_simp_chinese' and 0<=x<rect[2] and 0<=y<rect[3]
out=run/(stage+'-shift-click.action.json');assert not out.exists();point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(*point,duration=.15);time.sleep(.3)
h.pyautogui.keyDown('shift')
try:
 h.pyautogui.mouseDown(button='left');time.sleep(.15)
finally:
 h.pyautogui.mouseUp(button='left');h.pyautogui.keyUp('shift')
time.sleep(.5);assert h.win32gui.GetForegroundWindow()==hwnd
v={'action':'native_shift_left_click','stage':stage,'client_point':[x,y],'hwnd':hwnd,'shift_released':True};h.write_json(out,v);print(json.dumps(v),flush=True)
