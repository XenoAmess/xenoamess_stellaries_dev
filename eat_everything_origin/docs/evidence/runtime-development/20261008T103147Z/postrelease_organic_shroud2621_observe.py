import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
def objects(raw):
 it=iter(q.tokens(raw));out=[]
 for tok,start,end in it:
  assert tok=='{';depth=1;stop=None
  for val,before,after in it:
   if val=='{':depth+=1
   elif val=='}':
    depth-=1
    if not depth:stop=before;break
  assert stop is not None;out.append(q.scalars(raw[end:stop]))
 return out
def metadata(name):
 with zipfile.ZipFile(run/(name+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 pending=[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
 history=objects(q.block(t,'open_player_event_selection_history'))
 mods=objects(q.block(q.block(q.block(q.block(t,'country'),'0'),'timed_modifier'),'items'))
 return pending,history,mods
before='organic-shroud-unravel-year-2301';stage='organic-shroud2621-observed';b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));bp,bh,bm=metadata(before);ev=next(v for v in bp if v['event']=='shroud.2621');assert ev['id']==397;eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-native-option');label='\u7ee7\u7eed\u89c2\u6d4b\u8fd9\u79cd\u73b0\u8c61\u3002';rows=[v for v in f['rows'] if v['text']==label and v['score']>.8];assert len(rows)==1;row=rows[0];point=(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4));hwnd=h.focus_pid(int(h.process_record(run)['pid']));desktop=h.win32gui.ClientToScreen(hwnd,point);old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-native-choice.action.json'),{'action':'physical_click_then_physical_escape','client_point':point,'source_image_sha256':f['image_sha256'],'actual_option':label,'native_expected_progress_gain':50})
a=r.native_save(stage,b['date'],(0,));ap,ah,am=metadata(stage);bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
added=[v for v in ah if v not in bh];removed=[v for v in bh if v not in ah];newmods=[v for v in am if v not in bm];oldmodsremoved=[v for v in bm if v not in am];bs,ass=b['situations']['33554438'],a['situations']['33554438']
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'native_progress_exact_plus_50':bs['progress']==214.75 and ass['progress']==264.75,'other_audited_situation_fields_held':{k:v for k,v in bs.items() if k!='progress'}=={k:v for k,v in ass.items() if k!='progress'},'pending397_removed_once':len(bp)-len(ap)==1 and {v['id'] for v in bp}-{v['id'] for v in ap}=={397},'actual_human_option0_once':added==[{'player_event':397,'human':1,'option':0}] and not removed,'only_native_ten_year_modifier_added':newmods==[{'modifier':'psionic_cluster_modifier','days':3600}] and not oldmodsremoved}
for k in ('effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','native'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','planets','districts','deposits','species','event_targets'):checks[k+'_held']=a[k]==b[k]
checks['each_colony_actual_population_held']={k:v['actual_pop_sum'] for k,v in b['colonies'].items()}=={k:v['actual_pop_sum'] for k,v in a['colonies'].items()}
stockdiff={k:[bc['stockpile'].get(k),ac['stockpile'].get(k)] for k in set(bc['stockpile'])|set(ac['stockpile']) if bc['stockpile'].get(k)!=ac['stockpile'].get(k)}
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_pending_event_before':ev,'added_choice_history':added,'native_modifiers_added':newmods,'raw_economy_mirror_differences':stockdiff,'colonies_raw_equal':b['colonies']==a['colonies'],'colony_differences':{k:{'before':b['colonies'].get(k),'after':a['colonies'].get(k)} for k in set(b['colonies'])|set(a['colonies']) if b['colonies'].get(k)!=a['colonies'].get(k)},'scope':'Actual native shroud.2621 option a: +50 progress and ten-year research/stability modifier; same-date preservation. Future-date pending-event metadata is not a trigger-date claim.'}
h.write_json(run/(stage+'-proof.json'),p);print(json.dumps({'checks':checks,'sha':a['save_sha256'],'stock_diff':stockdiff,'colony_raw_equal':p['colonies_raw_equal'],'new_modifier':newmods}),flush=True);assert all(checks.values()),'Original native event choice failure retained'
