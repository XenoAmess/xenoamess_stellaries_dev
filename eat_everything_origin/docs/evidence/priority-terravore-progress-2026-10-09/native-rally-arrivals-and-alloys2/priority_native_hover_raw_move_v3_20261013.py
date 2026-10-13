"""Native one-pixel movement to refresh hover; no click or calendar."""
import json,logging,sys,time
stage,x,y=sys.argv[1:];x,y=int(x),int(y)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
assert m['language']=='l_simp_chinese'
hwnd=h.focus_pid(h.process_record(run)['pid']);rect=h.win32gui.GetClientRect(hwnd)
assert 1<=x<rect[2] and 0<=y<rect[3]
point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(point[0]-8,point[1],duration=.15)
h.win32api.mouse_event(1,16,0,0,0);time.sleep(1.2)
actual=h.win32gui.GetCursorPos()
out=run/(stage+'-hover.action.json');assert not out.exists()
h.write_json(out,{'action':'native_hover_only','client_point':[x,y],'desktop_point':list(point),'actual_cursor':list(actual),'hwnd':hwnd,'native_mouse_move':[16,0],'clicks':0,'dwell_seconds':1.2})
assert abs(actual[0]-point[0])<=16 and actual[1]==point[1] and h.win32gui.GetForegroundWindow()==hwnd
frame=r.gpu_capture(stage)
print(json.dumps({k:frame[k] for k in ['stage','image_sha256','capture','resolution']}),flush=True)
