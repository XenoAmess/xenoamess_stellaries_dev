import json,logging,shutil,sys
from decimal import Decimal as D,ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='organic-psicorps-tradition-paid';stage='organic-psicorps-tradition-confirmed';b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
f=r.gpu_capture(stage+'-real-affordable-node');labels=[v['text'] for v in f['rows']];assert '\u4f60\u786e\u5b9a\u8981\u91c7\u7eb3\u7075\u80fd\u519b\u56e2\u5417\uff1f' in labels and '\u82b1\u8d39\uff1a16696' in labels;assert b['countries']['0']['effective_stockpile']['unity']>=16696
hwnd=h.focus_pid(h.process_record(run)['pid']);desk=h.win32gui.ClientToScreen(hwnd,(630,416));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desk);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-payment.action.json'),{'action':'physical_click_then_physical_escape','client_point':[630,416],'actual_UI_cost':16696,'source_image_sha256':f['image_sha256']})
a=r.native_save(stage,b['date'],(0,));ac,bc=a['countries']['0'],b['countries']['0'];paid=D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'same_actual_date':a['date']==b['date']=='2305.05.02','actual_positive_affordable_Unity_paid':0<paid<=D(str(bc['effective_stockpile']['unity'])),'actual_payment_ceil16696':paid.to_integral_value(rounding=ROUND_CEILING)==16696,'all_other_actual_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='unity'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='unity'},'one_actual_PsiCorps_tradition_added':ac['traditions']==bc['traditions']+['tr_psionics_shroud_psi_corps'],'no_new_errors':ea==eb,'no_early_full_psionic_notice':ac['variables']['eep_psi']==0 and 'eep_psi_notice' not in ac['flags']}
for k in ('research_stockpile','tech_status','variables','flags','ascension_perks','government','owned_colonies'):checks[k+'_held']=ac[k]==bc[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_held']=a[k]==b[k]
p={'status':'PASS_PAYMENT_SCOPE' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_Unity_paid':str(paid),'actual_Unity_after':ac['effective_stockpile']['unity'],'actual_traditions_after':ac['traditions'],'raw_economy_mirror_difference':{k:[bc['stockpile'].get(k),ac['stockpile'].get(k)] for k in set(bc['stockpile'])|set(ac['stockpile']) if bc['stockpile'].get(k)!=ac['stockpile'].get(k)},'scope':'One real paid native PsiCorps tradition, no building completion, all tree or EEP psionic completion claim.'};h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original tradition payment guard failure retained; do not repay'
