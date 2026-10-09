import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,stage,mode=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
spec={'shroud_unity':('shroud.2305',410,1,'\u4e0d\u8981\u6253\u6270\u8fd9\u4e2a\u5723\u5730\u3002'),'marauder_withdraw':('marauder.111',408,0,'\u8d76\u5feb\u6eda\uff01')};event,eid,option,label=spec[mode]
def objects(raw):
 it=iter(q.tokens(raw));out=[]
 for tok,start,end in it:
  assert tok=='{';depth=1;stop=None
  for val,bef,aft in it:
   if val=='{':depth+=1
   elif val=='}':
    depth-=1
    if not depth:stop=bef;break
  assert stop is not None;out.append(q.scalars(raw[end:stop]))
 return out
def metadata(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 pending=[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
 history=objects(q.block(q.block(t,'open_player_event_selection_history'),'selected'))
 module=q.block(q.block(q.block(q.block(t,'country'),'0'),'modules'),'standard_shroud_module');assert module
 return pending,history,module
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));bp,bh,bsm=metadata(before);assert any(v['id']==eid and v['event']==event for v in bp);assert not (run/(stage+'.sav')).exists();eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-option');rows=[v for v in f['rows'] if v['text']==label and v['score']>.8];assert len(rows)==1;row=rows[0];point=(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4));hwnd=h.focus_pid(h.process_record(run)['pid']);desktop=h.win32gui.ClientToScreen(hwnd,point);old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-actual-choice.action.json'),{'action':'physical_click_then_physical_escape','actual_option':label,'client_point':point,'source_image_sha256':f['image_sha256']})
a=r.native_save(stage,b['date'],(0,));ap,ah,asm=metadata(stage);bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
delta={k:str(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))) for k in set(bc['effective_stockpile'])|set(ac['effective_stockpile']) if bc['effective_stockpile'].get(k)!=ac['effective_stockpile'].get(k)}
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'only_expected_pending_removed':len(bp)-len(ap)==1 and {v['id'] for v in bp}-{v['id'] for v in ap}=={eid},'expected_human_history_once':[v for v in ah if v not in bh]==[{'player_event':eid,'human':1,'option':option}] and not [v for v in bh if v not in ah]}
if mode=='shroud_unity':checks['only_native_unity_reward_matching_tooltip']=set(delta)=={'unity'} and abs(D(delta['unity'])-D('2781.0'))<=D('.05')
else:checks['all_effective_stocks_held']=not delta;checks['raw_native_shroud_module_held']=bsm==asm
for k in ('research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','native'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','planets','districts','deposits','species','situations'):checks[k+'_held']=a[k]==b[k]
checks['all_colony_population_held']={k:v['actual_pop_sum'] for k,v in a['colonies'].items()}=={k:v['actual_pop_sum'] for k,v in b['colonies'].items()}
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_effective_stock_delta':delta,'native_shroud_module_before':bsm,'native_shroud_module_after':asm,'pending_before':bp,'pending_after':ap,'colonies_raw_equal':a['colonies']==b['colonies'],'raw_economy_mirror_delta':{k:[bc['stockpile'].get(k),ac['stockpile'].get(k)] for k in set(bc['stockpile'])|set(ac['stockpile']) if bc['stockpile'].get(k)!=ac['stockpile'].get(k)},'scope':'Actual existing native event selection, with same-date payment/effect preservation; no replay or console grant.'};h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native event choice failure retained'
