import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['role']=='Post-release organic Fanatic Purifier natural continuation'
shutil.copyfile(Path(__file__),run/Path(__file__).name)
stage='organic-purifier-2287-adaptive-ecology-paid';b=json.loads((run/'organic-purifier-unity-2287.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
f=r.gpu_capture(stage+'-actual-confirm');labels=[x['text'] for x in f['rows']];assert '\u4f60\u786e\u5b9a\u8981\u91c7\u7eb3\u9002\u5e94\u6027\u751f\u6001\u5b66\u5417\uff1f' in labels and '\u82b1\u8d39\uff1a13172' in labels
rows=[x for x in f['rows'] if x['text']=='\u662f' and x['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));assert h.win32gui.GetForegroundWindow()==hwnd;desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE;started=time.monotonic_ns()
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-actual-payment.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'desktop_point':list(desktop),'source_image_sha256':f['image_sha256'],'elapsed_ns':time.monotonic_ns()-started,'actual_displayed_unity_cost':13172})
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];research={'physics_research','society_research','engineering_research'}
checks={'same_date':a['date']==b['date'],'actual_unity_payment_13172':abs(cb['stockpile']['unity']-ca['stockpile']['unity']-13172)<1e-5,'other_nonresearch_stock_same':{k:v for k,v in cb['stockpile'].items() if k not in research|{'unity'}}=={k:v for k,v in ca['stockpile'].items() if k not in research|{'unity'}},'research_pools_same':{k:cb['stockpile'].get(k) for k in research}=={k:ca['stockpile'].get(k) for k in research},'expected_traditions_only':ca['traditions']==cb['traditions']+['tr_adaptability_adaptive_ecology','tr_adaptability_finish'],'original_AP_only':cb['ascension_perks']==ca['ascension_perks']==['ap_one_vision','ap_consecrated_worlds'],'EEP_variables_same':cb['variables']==ca['variables'],'actual_pop_groups_same':b['pop_groups']==a['pop_groups'],'owned_colonies_same':cb['owned_colonies']==ca['owned_colonies'],'technology_same':cb['completed_technologies']==ca['completed_technologies'],'research_queues_same':cb['research_queues']==ca['research_queues'],'species_same':b['species']==a['species'],'no_free_districts_built':b['districts']==a['districts'],'deposits_same':b['deposits']==a['deposits'],'EEP_situations_same':{k:v for k,v in b['situations'].items() if str(v.get('type','')).startswith('eep_')}=={k:v for k,v in a['situations'].items() if str(v.get('type','')).startswith('eep_')}}
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);checks['no_new_errors']=eb==ea
differences={k:{'before':cb['stockpile'].get(k),'after':ca['stockpile'].get(k)} for k in cb['stockpile'].keys()|ca['stockpile'].keys() if cb['stockpile'].get(k)!=ca['stockpile'].get(k)}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'stock_differences':differences,'traditions_after':ca['traditions'],'scope':'Actual native paid last Adaptability tradition only; full Shroud ascension and civic acceptance pending.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True)
assert all(v for k,v in checks.items() if k!='research_pools_same'),'Original critical tradition payment FAIL retained'
f=r.gpu_capture(stage+'-after-ui');print(json.dumps({'labels':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
