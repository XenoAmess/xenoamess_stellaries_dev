"""Native held double click, measured below Windows double-click threshold."""
import ctypes,json,logging,sys,time
stage,x,y=sys.argv[1:];x,y=int(x),int(y)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();w=h.focus_pid(h.process_record(run)['pid']);rect=h.win32gui.GetClientRect(w);assert 0<=x<rect[2] and 0<=y<rect[3]
threshold=ctypes.windll.user32.GetDoubleClickTime();assert threshold>=250
out=run/(stage+'.action.json');assert not out.exists();point=h.win32gui.ClientToScreen(w,(x,y));h.win32api.SetCursorPos(point);time.sleep(.2);events=[]
for i in range(2):
 h.win32api.mouse_event(h.win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0);events.append({'edge':'down','at':time.perf_counter()});time.sleep(.08)
 h.win32api.mouse_event(h.win32con.MOUSEEVENTF_LEFTUP,0,0,0,0);events.append({'edge':'up','at':time.perf_counter()})
 if i==0:time.sleep(.08)
delta=events[2]['at']-events[0]['at'];assert delta*1000<threshold and all(events[i+1]['at']-events[i]['at']>=.07 for i in [0,2]);assert h.win32gui.GetForegroundWindow()==w
h.write_json(out,{'action':'native_held_double_click','client_point':[x,y],'screen_point':list(point),'events':events,'down_interval_ms':delta*1000,'windows_double_click_ms':threshold,'hwnd':w});print(json.dumps({'status':'native_double_input_sent','interval_ms':delta*1000,'threshold_ms':threshold}),flush=True)
