"""Align the existing window client to desktop origin without resizing or changing game state."""
import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
out=run/'terravore-raid-window-aligned.json';assert not out.exists()
pid=h.process_record(run)['pid'];hwnd=h.focus_pid(pid)
def state():return {'window':list(h.win32gui.GetWindowRect(hwnd)),'client':list(h.win32gui.GetClientRect(hwnd)),'origin':list(h.win32gui.ClientToScreen(hwnd,(0,0))),'desktop':list(h.pyautogui.size()),'style':h.win32gui.GetWindowLong(hwnd,h.win32con.GWL_STYLE)}
b=state();assert b['client']==[0,0,1024,768] and b['desktop']==[1024,768]
h.win32gui.SetWindowPos(hwnd,0,b['window'][0]-b['origin'][0],b['window'][1]-b['origin'][1],0,0,h.win32con.SWP_NOSIZE|h.win32con.SWP_NOZORDER|h.win32con.SWP_NOACTIVATE)
time.sleep(.5);a=state()
checks={'client_size_held':a['client']==b['client'],'desktop_size_held':a['desktop']==b['desktop'],'window_size_held':a['window'][2]-a['window'][0]==b['window'][2]-b['window'][0] and a['window'][3]-a['window'][1]==b['window'][3]-b['window'][1],'window_style_held':a['style']==b['style'],'client_origin_zero':a['origin']==[0,0],'entire_client_in_desktop':a['origin'][0]>=0 and a['origin'][1]>=0 and a['origin'][0]+a['client'][2]<=a['desktop'][0] and a['origin'][1]+a['client'][3]<=a['desktop'][1],'same_foreground_window':h.win32gui.GetForegroundWindow()==hwnd}
p={'status':'PASS_NATIVE_WINDOW_ALIGNMENT' if all(checks.values()) else 'FAIL','checks':checks,'pid':pid,'hwnd':hwnd,'before':b,'after':a,'scope':'OS window position only; no save/economic/calendar acceptance.'};h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Window alignment failed; do not click invisible UI'
