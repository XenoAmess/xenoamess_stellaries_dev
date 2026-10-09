import json, logging, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
start='organic-purifier-2284-event-paid';stage='organic-purifier-2284-response-ack'
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-actual-option');rows=[x for x in f['rows'] if x['text']=='\u786e\u8ba4' and x['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));assert h.win32gui.GetForegroundWindow()==hwnd
desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE;started=time.monotonic_ns()
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-actual-ack.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'desktop_point':list(desktop),'source_image_sha256':f['image_sha256'],'elapsed_ns':time.monotonic_ns()-started})
a=r.native_save(stage,b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0']
checks={'same_date':a['date']==b['date'],'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_variables_same':ca['variables']==cb['variables'],'no_new_errors':eb==(user/'logs/error.log').read_bytes()}
for k in ('completed_technologies','research_queues','traditions','ascension_perks'):checks[k+'_same']=cb[k]==ca[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_same']=b[k]==a[k]
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Native marauder response acknowledgement only.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original response FAIL retained'
h.press_scan_code(0x29,'organic-purifier-2284-original-receipt-open',1)
f=r.gpu_capture('organic-purifier-2284-original-receipt');labels=[x['text'] for x in f['rows']];receipt=[t for t in labels if h.normalized(t).startswith('fastforwarded360day')]
assert '2284.01.12' in labels and '\u6682\u505c' in labels and receipt,'Original receipt not confirmed; no new fast forward permitted'
stage='organic-purifier-unity-2284';h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED_AFTER_OCCLUSION','date':'2284.01.12','start_date':'2283.01.12','days':360,'image_sha256':f['image_sha256'],'actual_receipt_labels':receipt,'no_repeated_forward':True})
h.press_scan_code(0x29,stage+'-console-close',1);a=r.native_save(stage,'2284.01.12',(0,));c=a['countries']['0'];capital=c['native']['capital'];mothers=[p for p in a['planets'].values() if p.get('colony')==capital and p.get('owner')==0]
core_count=sum(a['deposits'].get(str(i),{}).get('type')=='d_eep_core' for p in mothers for i in p['deposits'])
checks={'actual_date':a['date']=='2284.01.12','legal_purifier_origin':'civic_fanatic_purifiers' in c['government'] and q.scalars(c['government']).get('origin')=='origin_heart_of_devouring','original_AP_only':c['ascension_perks']==['ap_one_vision','ap_consecrated_worlds'],'original_ledger':all(c['variables'].get(k)==v for k,v in {'eep_c':16,'eep_g':16,'eep_d':6,'eep_made':200,'eep_worlds':1,'eep_psi':0,'eep_fleet_stage':0}.items()),'one_actual_capital_core':len(mothers)==1 and core_count==1}
for k in ('food','consumer_goods','energy','minerals'):checks[k+'_not_exhausted']=c['stockpile'].get(k,0)>0
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);eb=(run/(stage+'-error-before.log')).read_bytes();delta=ea[len(eb):];checks['no_new_EEP_errors']=b'eep_' not in delta and b'eat_everything_origin' not in delta
population=sum(a['colonies'][str(i)]['actual_pop_sum'] for i in c['owned_colonies'])
h.write_json(run/(stage+'-state.json'),{'status':'OBSERVED_NATIVE_CALENDAR_RECOVERED','date':a['date'],'save_sha256':a['save_sha256'],'population':population,'new_error_bytes':len(delta)})
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'date':a['date'],'save_sha256':a['save_sha256'],'stockpile':c['stockpile'],'actual_total_population':population,'mother_population':a['colonies'][str(capital)]['actual_pop_sum'],'new_error_bytes':len(delta),'native_energy_tribute':250,'original_failed_driver_retained':True,'scope':'Recovered third natural resource year only; not strict reload, research balance invariance or full civic acceptance.'}
h.write_json(run/(stage+'-natural-resource-proof.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original year FAIL retained'
