import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
def policies(path):
 with zipfile.ZipFile(path) as z:t=z.read('gamestate').decode('utf-8-sig')
 raw=q.block(q.block(q.block(t,'country'),'0'),'active_policies');it=iter(q.tokens(raw));result={}
 for tok,start,end in it:
  assert tok=='{','Expected unnamed policy entry';depth=1;stop=None
  for val,before,after in it:
   if val=='{':depth+=1
   elif val=='}':
    depth-=1
    if not depth:stop=before;break
  assert stop is not None
  data=q.scalars(raw[end:stop]);key=data['policy'];assert key not in result;result[key]=data
 return raw,result
b=json.loads((run/'organic-foundry-limit-nextmonth.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture('organic-civilian-policy-confirmation-original');labels=[v['text'] for v in f['rows']]
assert any('\u7ecf\u6d4e\u653f\u7b56\u653f\u7b56\u6539\u4e3a\u6c11\u7528\u7ecf\u6d4e' in s for s in labels)
row=next(v for v in f['rows'] if v['text']=='\u662f' and v['score']>.8);x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));point=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*point);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/'organic-civilian-policy-confirm.action.json',{'action':'physical_click_then_escape','client_point':[x,y],'source_image_sha256':f['image_sha256'],'choice':'Native civilian economic policy; actual confirmation states 10-year policy lock.'})
a=r.native_save('organic-civilian-policy-selected',b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/'organic-civilian-policy-selected-error-after.log').write_bytes(ea)
br,bp=policies(run/'organic-foundry-limit-nextmonth.sav');ar,ap=policies(run/'organic-civilian-policy-selected.sav')
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'policy_key_sets_held':set(bp)==set(ap),'only_economic_policy_changed':{k:v for k,v in bp.items() if k!='economic_policy'}=={k:v for k,v in ap.items() if k!='economic_policy'},'native_balanced_to_civilian':bp['economic_policy']['selected']=='economic_policy_balanced' and ap['economic_policy']['selected']=='economic_policy_civilian'}
for k in ('stockpile','effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','native'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets'):checks[k+'_held']=a[k]==b[k]
h.write_json(run/'organic-civilian-policy-selected-proof.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'economic_policy_before':bp['economic_policy'],'economic_policy_after':ap['economic_policy'],'raw_policies_before':br,'raw_policies_after':ar,'scope':'Native policy choice and same-date state preservation only; next-month production still pending. Not a Mod reward or full acceptance.'})
print(json.dumps({'checks':checks,'policy_after':ap['economic_policy'],'sha':a['save_sha256']}),flush=True);assert all(checks.values()),'Original native policy failure retained'
