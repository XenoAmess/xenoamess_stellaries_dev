import hashlib,json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,stage,mode=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'))
def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:return z.read('gamestate').decode('utf-8-sig')
def pending(t):return {q.scalars(v)['id']:v for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0}
bt=raw(before);br={k:v for k,v,o in q.fields(bt) if o};bp=pending(bt)
event,option,label={'refuse':(433,3,'\u4f60\u4f11\u60f3\u4ece\u6211\u4eec\u8fd9\u91cc\u62ff\u5230\u4efb\u4f55\u4e1c\u897f\u3002'),'leader':(432,0,'\u8fd9\u9879\u65b0\u80fd\u529b\u5f88\u597d\u5730\u4e3a\u6211\u4eec\u6240\u7528\u3002'),'response':(None,None,'\u786e\u8ba4')}[mode]
if event is not None:assert event in bp
if mode=='refuse':assert 'marauder_1' in q.scalars(q.block(q.block(br.get('country',''),'12'),'flags')) and q.scalars(bp[event])['event']=='marauder.101'
if mode=='leader':
    targets=[q.scalars(v) for k,v,o in q.fields(q.block(q.block(bp[event],'scope'),'from')) if k=='saved_event_target' and o]
    assert [v for v in targets if v.get('name')=='psionic_leader']==[{'type':'leader','id':50331766,'opener_id':4294967295,'name':'psionic_leader'}]
    assert q.scalars(bp[event])['event']=='utopia.2606'
eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
f=r.gpu_capture(stage+'-actual-option')
if mode=='response':assert any('\u65e2\u7136\u4f60\u4eec\u4e0d\u80af\u4e3b\u52a8\u732e\u51fa\u8d21\u54c1' in v['text'] for v in f['rows'])
rows=[v for v in f['rows'] if v['text']==label and v['score']>=.8];assert len(rows)==1,'Actual native option missing or ambiguous; no choice made'
row=rows[0];pt=[round(sum(v[0] for v in row['box'])/4),round(sum(v[1] for v in row['box'])/4)]
hwnd=h.focus_pid(int(h.process_record(run)['pid']));desktop=h.win32gui.ClientToScreen(hwnd,tuple(pt));old=h.pyautogui.PAUSE
try:
    h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-choice.action.json'),{'action':'normal_native_choice_then_physical_escape','client_point':pt,'native_event_id':event,'actual_option':label,'source_image_sha256':f['image_sha256']})
a=r.native_save(stage,b['date'],(0,));at=raw(stage);ar={k:v for k,v,o in q.fields(at) if o};ap=pending(at);ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
bc,ac=b['countries']['0'],a['countries']['0'];bh,ah=selected_history(bt),selected_history(at)
checks={'same_actual_date':a['date']==b['date'],'no_new_errors':eb==ea,'pending_exact_removal':set(ap)==set(bp)-({event} if event else set()),'other_pending_raw_held':all(bp[k]==v for k,v in ap.items()),'selection_history_exact':ah==bh+([{'player_event':event,'human':1,'option':option}] if event else []),'complete_native_country_flags_held':q.block(q.block(br.get('country',''),'0'),'flags')==q.block(q.block(ar.get('country',''),'0'),'flags'),'native_marauder_flags_held':q.block(q.block(br.get('country',''),'12'),'flags')==q.block(q.block(ar.get('country',''),'12'),'flags')}
for k in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies']:checks[('EEP_flags' if k=='flags' else k)+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species']:checks[k+'_held']=b[k]==a[k]
for k in ['buildings','zones','construction']:checks['raw_'+k+'_held']=br.get(k,'')==ar.get(k,'')
bl,al={k:v for k,v,o in q.fields(br.get('leaders','')) if o},{k:v for k,v,o in q.fields(ar.get('leaders','')) if o}
if mode=='leader':
    target='50331766';trait='leader_trait_psionic';old_traits=[q.unquote(v) for k,v,o in q.fields(bl[target]) if k=='traits'];new_traits=[q.unquote(v) for k,v,o in q.fields(al[target]) if k=='traits']
    clean,n=re.subn(r'\n[ \t]*traits="leader_trait_psionic"','',al[target])
    checks.update(target_exact_one_psionic_trait=n==1 and trait not in old_traits and new_traits==old_traits+[trait],target_other_raw_fields_held=clean==bl[target],all_other_leaders_raw_held={k:v for k,v in bl.items() if k!=target}=={k:v for k,v in al.items() if k!=target})
else:checks['all_leaders_raw_held']=bl==al
p={'status':'PASS_NATIVE_CHOICE' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_pending_before':{k:q.scalars(v) for k,v in bp.items()},'native_pending_after':{k:q.scalars(v) for k,v in ap.items()},'selection_added':ah[len(bh):],'scope':'Same-date normal native event choice. Full EEP accounting, true stocks and native construction held. Existing raid retained; leader option is not full species ascension.'}
out=run/(stage+'-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native choice failure retained; no automatic replay'
