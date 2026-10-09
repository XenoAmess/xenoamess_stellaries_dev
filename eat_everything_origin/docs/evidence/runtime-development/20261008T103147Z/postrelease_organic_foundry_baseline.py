import json, logging, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools'); sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness; run,user,m=h.load_run()
shutil.copyfile(__file__,run/Path(__file__).name)
b=json.loads((run/'organic-psionic-adoption-nextmonth.audit.json').read_text(encoding='utf-8'))
a=r.native_save('organic-foundry-priority-restored-baseline',b['date'],(0,))
checks={'same_date':a['date']==b['date']}
for k in ('stockpile','effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','native'):
 checks[k+'_held']=a['countries']['0'][k]==b['countries']['0'][k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):
 checks[k+'_held']=a[k]==b[k]
h.write_json(run/'organic-foundry-priority-restored-baseline-proof.json',{'status':'OBSERVATION','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Two native foundry priority tile clicks, intended to restore original priority; record every native cache or priority difference before workforce adjustment.'})
print(json.dumps({'baseline_checks':checks,'sha':a['save_sha256']}),flush=True)
hwnd=h.focus_pid(int(h.process_record(run)['pid']))
h.pyautogui.moveTo(*h.win32gui.ClientToScreen(hwnd,(577,481)))
for i in range(6):
 h.win32api.mouse_event(h.win32con.MOUSEEVENTF_WHEEL,0,0,-120,0); time.sleep(.12)
h.write_json(run/'organic-foundry-details-scroll.action.json',{'action':'native_mouse_wheel','client_point':[577,481],'steps':6,'delta_each':-120})
f=r.gpu_capture('organic-foundry-details-scroll')
print(json.dumps({'image':str(f['image']),'rows':[v['text'] for v in f['rows']]}),flush=True)
