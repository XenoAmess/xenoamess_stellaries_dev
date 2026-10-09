import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
before='organic-temple-year1-marauder-resource-notice-ack';stage='organic-temple-year1-cleared'
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));supp=json.loads((run/'organic-temple-year1-volcano-tech-scope-supplement-v2-proof.json').read_text(encoding='utf-8'));assert supp['status']=='PASS_NATIVE_VOLCANO_EFFECT_PENDING_COST_VERIFICATION'
f=json.loads((run/'organic-temple-year1-society-options-costs.ocr.json').read_text(encoding='utf-8'));labels=[v['text'] for v in f['rows']];assert '\u5730\u58f3\u6df1\u90e8\u5de5\u7a0b' in labels and '1116/4464' in labels and '2309.05.02' in labels and '\u6682\u505c' in labels
assert h.sha256(Path(f['image']))==f['image_sha256'] and D(str(b['countries']['0']['research_progress_by_tech']['tech_volcano']))/D(4464)==D('.25')
eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x3e,stage+'-close-F4-read-only',1);h.press_scan_code(0x29,stage+'-console-open-read-only',1);receipt=r.gpu_capture(stage+'-original360-receipt');labels=[v['text'] for v in receipt['rows']];rows=[v for v in labels if h.normalized(v)=='fastforwarded360days'];ok='2309.05.02' in labels and '\u6682\u505c' in labels and bool(rows)
h.write_json(run/(stage+'-receipt-proof.json'),{'status':'PASS_OLD360_RECEIPT' if ok else 'FAIL','actual_date':'2309.05.02','old_full_receipt_labels':rows,'source_image_sha256':receipt['image_sha256'],'actual_source_save_sha256':b['save_sha256'],'scope':'Read existing completed360-day receipt; no command typed or calendar replay.'})
h.press_scan_code(0x29,stage+'-console-close-read-only',1)
if 'Debug View' in labels:h.click_point(538,347,stage+'-close-visible-debug-view')
assert ok,'Old receipt recovery failed; no date replay'
a=r.native_save(stage,'2309.05.02',(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
def raw(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    roots=list(q.fields(t));return t,{k:v for k,v,o in roots if o},[q.scalars(v) for k,v,o in roots if k=='player_event' and o and q.scalars(v).get('country')==0]
bt,br,bp=raw(before);at,ar,ap=raw(stage);bc,ac=b['countries']['0'],a['countries']['0'];checks={'same_date':a['date']==b['date'],'no_new_errors':ea==eb,'no_pending':not bp and not ap,'history_held':selected_history(bt)==selected_history(at),'native_country_flags_held':q.block(q.block(br['country'],'0'),'flags')==q.block(q.block(ar['country'],'0'),'flags'),'actual_native_volcano25percent':ac['research_progress_by_tech'].get('tech_volcano')==1116 and D(1116)/D(4464)==D('.25'),'old360_receipt_visible':ok}
for k in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies']:checks[('EEP_flags' if k=='flags' else k)+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species']:checks[k+'_held']=b[k]==a[k]
for k in ['construction','buildings','zones','leaders']:checks['raw_'+k+'_held']=br[k]==ar[k]
p={'status':'PASS_NATIVE_READONLY_INSPECTION_AND_RECEIPT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_volcano_partial':1116,'native_F4_total_cost':4464,'native_F4_image_sha256':f['image_sha256'],'scope':'Same-date read-only F4 research-cost and original calendar receipt verification; native stores and full EEP state held. No technology selection or replay.'};h.write_json(run/(stage+'-proof.json'),p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original inspection failure retained'
