import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
stage='organic-storm-original320-receipt-recovery';b=json.loads((run/'organic-storm-native-leader-awakened.audit.json').read_text(encoding='utf-8'));p=json.loads((run/'organic-storm-native-leader-trait-supplement-proof.json').read_text(encoding='utf-8'));assert p['status']=='PASS_NATIVE_LEADER_TRAIT_SUPPLEMENT' and p['after_sha256']==b['save_sha256'] and b['date']=='2308.04.22'
h.press_scan_code(0x29,stage+'-console-open',1);f=r.gpu_capture(stage+'-actual-original-receipt');labels=[v['text'] for v in f['rows']];receipts=[v for v in labels if h.normalized(v)=='fastforwarded320days']
checks={'actual_paused_date_visible':'2308.04.22' in labels and '\u6682\u505c' in labels,'old_full320_receipt_visible':len(receipts)>=1}
h.press_scan_code(0x29,stage+'-console-close',1)
if 'Debug View' in labels:h.click_point(538,347,stage+'-close-visible-debug-view')
out=run/(stage+'-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_ORIGINAL_RECEIPT_RECOVERY' if all(checks.values()) else 'FAIL','checks':checks,'original_calendar_stage':'organic-storm-mine5-lastday','actual_recovered_save_sha256':b['save_sha256'],'source_image_sha256':f['image_sha256'],'original_full_receipt_labels':receipts,'scope':'Read already-executed320-day receipt after normal pending choices; no command typed, no calendar replay.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original receipt recovery failure retained; no date replay'
