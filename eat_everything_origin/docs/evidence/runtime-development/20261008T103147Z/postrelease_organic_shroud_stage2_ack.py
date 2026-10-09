import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='organic-shroud-stage2-pending';stage='organic-shroud-stage2-ack';b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:return z.read('gamestate').decode('utf-8-sig')
def pending(t):return [q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
def queue(t):
    c=q.block(t,'construction');sq=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');it=q.block(q.block(c,'item_mgr'),'items')
    return sq,{str(i):q.block(it,str(i)) for i in q.ids(q.block(sq,'items'))}
bt=raw(before);bp=pending(bt);assert len(bp)==1 and bp[0]['id']==424 and bp[0]['event']=='shroud.2760'
f=r.gpu_capture(stage+'-actual-option');label='\u90a3\u5c31\u5efa\u4e2a\u8fd9\u4ec0\u4e48\u201c\u7075\u80fd\u519b\u56e2\u201d\u5427\u3002'
rows=[v for v in f['rows'] if v['text']==label and v['score']>=.8];assert len(rows)==1
box=rows[0]['box'];x=round(sum(p[0] for p in box)/4);y=round(sum(p[1] for p in box)/4);desktop=r.desktop_point(x,y);old=h.pyautogui.PAUSE
try:
    h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-click.action.json'),{'action':'physical_click_then_physical_escape','actual_option':label,'client_point':[x,y],'source_image_sha256':f['image_sha256']})
a=r.native_save(stage,b['date'],(0,));ac,bc=a['countries']['0'],b['countries']['0'];at=raw(stage);ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':ea==eb,'actual_pending424_removed':not pending(at),'native_human_option0_once':selected_history(at)==selected_history(bt)+[{'player_event':424,'human':1,'option':0}],'native_mother_queue_held':queue(at)==queue(bt),'all_raw_buildings_held':q.block(at,'buildings')==q.block(bt,'buildings'),'all_raw_zones_held':q.block(at,'zones')==q.block(bt,'zones')}
for k in ('effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies'):checks[k+'_held']=ac[k]==bc[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_held']=a[k]==b[k]
p={'status':'PASS_NATIVE_STAGE2_NOTIFICATION_ACK' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'One real native shroud2760 tooltip-only ACK; no construction completion, psionic completion or civic acceptance.'}
h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original stage2 ACK failure retained; do not replay'
