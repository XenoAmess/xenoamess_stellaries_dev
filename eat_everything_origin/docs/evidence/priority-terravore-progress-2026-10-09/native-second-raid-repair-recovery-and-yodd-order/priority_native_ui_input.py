"""Single normal Unicode text input or client-coordinate right click; no calendar."""
import ctypes,json,logging,shutil,sys,time
from ctypes import wintypes as W
from datetime import datetime,timezone
from pathlib import Path
mode,stage,*args=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
out=run/(stage+'.action.json');assert not out.exists();hwnd=h.focus_pid(h.process_record(run)['pid'])
action={'action':mode,'stage':stage,'pid':h.process_record(run)['pid'],'at_utc':datetime.now(timezone.utc).isoformat()}
if mode=='unicode':
 text=''.join(chr(int(c,16)) for c in args);assert text and all(0<ord(c)<65536 for c in text)
 P=ctypes.c_size_t
 class K(ctypes.Structure):_fields_=[('wVk',W.WORD),('wScan',W.WORD),('dwFlags',W.DWORD),('time',W.DWORD),('dwExtraInfo',P)]
 class M(ctypes.Structure):_fields_=[('dx',W.LONG),('dy',W.LONG),('mouseData',W.DWORD),('dwFlags',W.DWORD),('time',W.DWORD),('dwExtraInfo',P)]
 class U(ctypes.Union):_fields_=[('ki',K),('mi',M)]
 class I(ctypes.Structure):_anonymous_=['u'];_fields_=[('type',W.DWORD),('u',U)]
 assert ctypes.sizeof(I)==(40 if ctypes.sizeof(P)==8 else 28)
 send=ctypes.WinDLL('user32',use_last_error=True).SendInput;send.argtypes=[W.UINT,ctypes.POINTER(I),ctypes.c_int];send.restype=W.UINT
 counts=[]
 for ch in text:
  keys=(I*2)();keys[0].type=keys[1].type=1;keys[0].ki=K(0,ord(ch),4,0,0);keys[1].ki=K(0,ord(ch),6,0,0)
  count=send(2,keys,ctypes.sizeof(I));counts.append(count);assert count==2,f'SendInput failed: {ctypes.get_last_error()}'
  time.sleep(.06)
 action.update(text=text,codepoints=args,sent_counts=counts)
elif mode=='right-click':
 x,y=map(int,args);rect=h.win32gui.GetClientRect(hwnd);assert 0<=x<rect[2] and 0<=y<rect[3]
 point=h.win32gui.ClientToScreen(hwnd,(x,y));h.pyautogui.click(*point,button='right');action.update(client_point=[x,y],desktop_point=list(point))
else:raise ValueError('Unknown input mode')
action['foreground_after']=h.win32gui.GetForegroundWindow();action['expected_hwnd']=hwnd;assert action['foreground_after']==hwnd
h.write_json(out,action);print(json.dumps(action,ensure_ascii=False),flush=True)
