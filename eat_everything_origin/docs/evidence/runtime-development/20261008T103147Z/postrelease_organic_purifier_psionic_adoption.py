import json,logging,shutil,sys
from decimal import Decimal,ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
stage='organic-psionic-tradition-adopted';b=json.loads((run/'organic-psionic-unity-2297.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
f=r.gpu_capture(stage+'-native-confirm');labels=[v['text'] for v in f['rows']]
assert '\u4f60\u786e\u5b9a\u8981\u91c7\u7eb3\u7075\u80fd\u4f20\u7edf\u5417\uff1f' in labels and '\u82b1\u8d39\uff1a15537' in labels
rows=[v for v in f['rows'] if v['text']=='\u662f' and v['score']>=.8];assert len(rows)==1
row=rows[0];x=round(sum(v[0] for v in row['box'])/4);y=round(sum(v[1] for v in row['box'])/4)
hwnd=h.focus_pid(int(h.process_record(run)['pid']));desktop=h.win32gui.ClientToScreen(hwnd,(x,y));old=h.pyautogui.PAUSE
try:
 h.pyautogui.PAUSE=0;h.pyautogui.click(*desktop);h.win32api.keybd_event(0,0x01,0x0008,0);h.win32api.keybd_event(0,0x01,0x0008|h.win32con.KEYEVENTF_KEYUP,0)
finally:h.pyautogui.PAUSE=old
h.write_json(run/(stage+'-payment.action.json'),{'action':'physical_click_then_physical_escape','client_point':[x,y],'source_image_sha256':f['image_sha256'],'actual_displayed_unity_cost':15537})
a=r.native_save(stage,b['date'],(0,));bc,ac=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
paid=Decimal(str(bc['effective_stockpile']['unity']))-Decimal(str(ac['effective_stockpile']['unity']));new_situations={k:v for k,v in a['situations'].items() if k not in b['situations'] and v.get('type')=='situation_breach_shroud'}
checks={'same_actual_date':a['date']==b['date']=='2297.09.02','actual_positive_affordable_payment':0<paid<=Decimal(str(bc['effective_stockpile']['unity'])),
 'actual_payment_ceil_matches15537':paid.to_integral_value(rounding=ROUND_CEILING)==15537,
 'all_other_effective_stock_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='unity'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='unity'},
 'native_research_banks_held':bc['research_stockpile']==ac['research_stockpile'],'complete_tech_status_held':bc['tech_status']==ac['tech_status'],
 'only_psionic_adopt_added':ac['traditions']==bc['traditions']+['tr_psionics_shroud_adopt'],
 'one_native_breach_progress0':len(new_situations)==1 and next(iter(new_situations.values()))['progress']==0,
 'all_colony_actual_population_held':{k:v['actual_pop_sum'] for k,v in b['colonies'].items()}=={k:v['actual_pop_sum'] for k,v in a['colonies'].items()},
 'no_early_EEP_psi':'eep_psi_notice' not in ac['flags'] and ac['variables']['eep_psi']==0,
 'no_new_errors':ea==eb}
for k in ('variables','flags','completed_technologies','research_queues','research_progress_by_tech','ascension_perks','government','owned_colonies'):checks[k+'_held']=bc[k]==ac[k]
for k in ('districts','deposits'):checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_PAYMENT_SCOPE' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'auditor_sha256':a['audit_tool_sha256'],'actual_unity_paid':str(paid),
 'new_native_situations':new_situations,'founder_refs':[bc['native'].get('founder_species_ref'),ac['native'].get('founder_species_ref')],
 'species_before':b['species'],'species_after':a['species'],'raw_pop_groups_same':b['pop_groups']==a['pop_groups'],'raw_jobs_same':b['pop_jobs']==a['pop_jobs'],
 'raw_stock_changes':{k:[bc['stockpile'].get(k),v] for k,v in ac['stockpile'].items() if bc['stockpile'].get(k)!=v},
 'template_relation_verification_pending':True,'scope':'Actual paid native adoption and zero-progress breach only. Template/foreign preservation and notification ACK separately pending; no full psionic completion.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original adoption failure retained; do not repay'
f=r.gpu_capture(stage+'-after-native-ui');print(json.dumps({'image':str(f['image']),'rows':[v['text'] for v in f['rows']]}),flush=True)
