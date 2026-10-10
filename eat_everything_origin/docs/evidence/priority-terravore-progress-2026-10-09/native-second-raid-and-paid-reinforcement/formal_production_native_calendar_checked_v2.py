"""One normal native calendar input with date, prior proof and stage checks before GUI."""
import json,logging,shutil,sys,time
from pathlib import Path
def validate_native_interval(start,end,days):
 def ordinal(value):
  year,month,day=map(int,value.split('.'));assert year>=1 and 1<=month<=12 and 1<=day<=30
  return year*360+(month-1)*30+day-1
 assert 1<=days<=360 and ordinal(end)-ordinal(start)==days,'Native30-day date mismatch; no GUI action allowed'
 return end
if __name__=='__main__':
 start,end,stage,raw_days,preproof_file,preexecution_stage=sys.argv[1:];days=int(raw_days)
 sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
 logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0' and m['language']=='l_simp_chinese'
 dest=run/Path(__file__).name
 if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
 else:shutil.copyfile(__file__,dest)
 b=json.loads((run/(start+'.audit.json')).read_text('utf-8'));validate_native_interval(b['date'],end,days)
 assert not list(run.glob(stage+'*')),'Stage already has artifacts; do not repeat calendar'
 pre=json.loads((run/preproof_file).read_text('utf-8'));execution=json.loads((run/(preexecution_stage+'-execution.json')).read_text('utf-8'))
 assert pre['status'].startswith('PASS') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and execution['returncode']==0
 assert h.sha256(run/(start+'.sav'))==b['save_sha256']
 eb=(user/'logs/error.log').read_bytes();assert eb==(run/(start+'-error-after.log')).read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
 h.press_scan_code(0x29,stage+'-console-open',1);h.type_text('fast_forward '+str(days),True,stage+'-native-days')
 for n in range(24):
  if n:time.sleep(10)
  f=r.gpu_capture(stage+'-calendar-poll-'+str(n));labels=[x['text'] for x in f['rows']]
  complete=end in labels and '\u6682\u505c' in labels and any(h.normalized(t).startswith('fastforwarded'+str(days)+'day') or h.normalized(t)=='fastforwarded'+str(days)+'d' for t in labels)
  print(json.dumps({'poll':n,'date_seen':end in labels,'receipt_complete':complete}),flush=True)
  if complete:
   h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','date':end,'start_date':b['date'],'days':days,'image_sha256':f['image_sha256'],'prior_proof_file':preproof_file,'prior_execution_stage':preexecution_stage,'actual_receipt_labels':[t for t in labels if 'fastforward' in h.normalized(t)]});break
 else:raise RuntimeError('Native calendar not confirmed; no repeated input')
 h.press_scan_code(0x29,stage+'-console-close',1);a=r.native_save(stage,end,(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
 v={'status':'OBSERVED_NATIVE_CALENDAR','date':a['date'],'save_sha256':a['save_sha256'],'population':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in a['countries']['0']['owned_colonies']),'new_error_bytes':len(ea)-len(eb),'scope':'Actual single native calendar, checked date/prior PASS before GUI, no grants. Independent state checks still required.'}
 h.write_json(run/(stage+'-state.json'),v);print(json.dumps(v),flush=True)
