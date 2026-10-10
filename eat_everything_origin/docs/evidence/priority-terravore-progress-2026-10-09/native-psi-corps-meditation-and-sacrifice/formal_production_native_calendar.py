import json,logging,shutil,sys,time
from pathlib import Path
start,end,stage,raw_days=sys.argv[1:];days=int(raw_days);assert 1<=days<=360
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(Path(__file__),dest)
assert dest.read_bytes()==Path(__file__).read_bytes();b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stage+'-console-open',1);h.type_text('fast_forward '+str(days),True,stage+'-native-days')
for n in range(24):
 if n:time.sleep(10)
 f=r.gpu_capture(stage+'-calendar-poll-'+str(n));labels=[x['text'] for x in f['rows']];complete=end in labels and '\u6682\u505c' in labels and any(h.normalized(t).startswith('fastforwarded'+str(days)+'day') or h.normalized(t)=='fastforwarded'+str(days)+'d' for t in labels)
 print(json.dumps({'poll':n,'date_seen':end in labels,'receipt_complete':complete}),flush=True)
 if complete:
  h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','date':end,'start_date':b['date'],'days':days,'image_sha256':f['image_sha256'],'actual_receipt_labels':[t for t in labels if 'fastforward' in h.normalized(t)]});break
else:raise RuntimeError('Native calendar not confirmed')
h.press_scan_code(0x29,stage+'-console-close',1);a=r.native_save(stage,end,(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
v={'status':'OBSERVED_NATIVE_CALENDAR','date':a['date'],'save_sha256':a['save_sha256'],'variables_before':b['countries']['0']['variables'],'variables_after':a['countries']['0']['variables'],'population':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in a['countries']['0']['owned_colonies']),'new_error_bytes':len(ea)-len(eb),'scope':'Actual native calendar in final production-only process, no grants or test scripts.'};h.write_json(run/(stage+'-state.json'),v);print(json.dumps(v),flush=True)
