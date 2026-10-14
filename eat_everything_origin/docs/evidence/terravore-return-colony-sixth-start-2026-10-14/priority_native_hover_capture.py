"""Normal client hover and a fresh native GPU frame; no click or calendar."""
import json,logging,sys,time
stage,x,y=sys.argv[1:];x,y=int(x),int(y)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
assert m['language']=='l_simp_chinese'
hwnd=h.focus_pid(h.process_record(run)['pid']);rect=h.win32gui.GetClientRect(hwnd)
assert 0<=x<rect[2] and 0<=y<rect[3]
point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.moveTo(*point,duration=.15);time.sleep(.9)
assert h.win32gui.GetForegroundWindow()==hwnd
out=run/(stage+'-hover.action.json');assert not out.exists()
h.write_json(out,{'action':'native_hover_only','client_point':[x,y],'desktop_point':list(point),'hwnd':hwnd,'dwell_seconds':.9})
frame=r.gpu_capture(stage)
print(json.dumps({k:frame[k] for k in ['stage','image_sha256','capture','resolution']}),flush=True)
