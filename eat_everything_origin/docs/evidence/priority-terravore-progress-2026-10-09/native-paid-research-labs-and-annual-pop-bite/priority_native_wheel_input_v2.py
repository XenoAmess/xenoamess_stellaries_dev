"""Focused native wheel input only; no calendar, console, or resource action."""
import json,logging,sys,time
stage,x,y,amount=sys.argv[1:];x,y,amount=int(x),int(y),int(amount)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
hwnd=h.focus_pid(h.process_record(run)['pid']);rect=h.win32gui.GetClientRect(hwnd)
assert m['language']=='l_simp_chinese' and 0<=x<rect[2] and 0<=y<rect[3] and 1<=abs(amount)<=30
out=run/(stage+'-wheel.action.json');assert not out.exists()
point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(*point,duration=.15);time.sleep(.25);h.scroll(amount,x,y,stage+'-win32',6);time.sleep(.5)
assert h.win32gui.GetForegroundWindow()==hwnd
v={'action':'native_mouse_wheel','stage':stage,'client_point':[x,y],'wheel_amount':amount,'hwnd':hwnd};h.write_json(out,v);print(json.dumps(v),flush=True)
