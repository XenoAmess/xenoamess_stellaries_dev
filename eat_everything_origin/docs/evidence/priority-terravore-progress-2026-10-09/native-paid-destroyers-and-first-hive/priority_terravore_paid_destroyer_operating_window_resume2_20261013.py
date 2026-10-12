"""Sequential bounded driver; stop immediately on any child nonzero, never repeat an input."""
import json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
root=Path('D:/workspace/xenoamess_stellaries_dev');helpers=root/'_runtime/heart-of-devouring';run=helpers/'runs/20261009T044016Z'
wrapper=helpers/'record_current_helper.py';component=run/'priority_terravore_paid_destroyer_operating_month_20261013.py'
before='terravore-native-tunnel303-ack-22841201';prior=before+'-empty-native-ack-proof.json';execution=before+'-empty-native-ack-guard'
receipt=run/'terravore-paid-destroyer-operating-window-resume2-receipt.json';assert not receipt.exists()
steps=[]
def save(status):
 receipt.write_text(json.dumps({'status':status,'at_utc':datetime.now(timezone.utc).isoformat(),'last_original_stage':before,'last_business_proof':prior,'last_business_execution':execution,'steps':steps,'scope':'At most8 native months, no operation after May1 or any child nonzero.'},indent=2),encoding='utf-8')
def call(stage,helper,*args):
 assert not (run/(stage+'-execution.json')).exists(),stage
 command=[sys.executable,str(wrapper),stage,str(helper),*map(str,args)]
 result=subprocess.run(command,cwd=root,check=False)
 record=json.loads((run/(stage+'-execution.json')).read_text('utf-8-sig'))
 steps.append({'stage':stage,'returncode':record['returncode'],'wrapper_returncode':result.returncode,'helper_sha256':record['helper_sha256']})
 if result.returncode!=0 or record['returncode']!=0:
  save('STOP_NONZERO');sys.exit(1)
for index in range(5):
 audit=json.loads((run/(before+'.audit.json')).read_text('utf-8-sig'));year,month,d=map(int,audit['date'].split('.'));assert d==1
 month+=1
 if month==13:year+=1;month=1
 end=f'{year:04d}.{month:02d}.01';assert end<='2285.05.01'
 after='terravore-paid-destroyer-operating-'+end.replace('.','')
 call(before+'-operating-month-review',component,'review',before,end,prior,execution)
 call(after+'-calendar',run/'priority_terravore_labs_native_calendar_v7_20261013.py',before,end,after,30,prior,execution,before+'-operating-month-review.json')
 call(after+'-boundary-observation-v4',run/'priority_terravore_labs_native_observer_v8_20261013.py',before,after,end,30)
 call(after+'-operating-month-guard',component,'guard',before,after,prior,execution)
 before=after;prior=after+'-operating-month-proof.json';execution=after+'-operating-month-guard'
 proof=json.loads((run/prior).read_text('utf-8-sig'));assert proof['status'].startswith('PASS') and all(v is True for v in proof['checks'].values())
 save('RUNNING')
 print(json.dumps({'month_completed':index+1,'date':end,'new_paid_hulls':len(proof['new_ship_ids']),'orders_left':len(proof['remaining_paid_orders']),'project3':proof['project3_progress'],'hive_work':proof['hive_work']}),flush=True)
save('PASS_WINDOW_AT_DOCUMENTED_BOUNDARY')
