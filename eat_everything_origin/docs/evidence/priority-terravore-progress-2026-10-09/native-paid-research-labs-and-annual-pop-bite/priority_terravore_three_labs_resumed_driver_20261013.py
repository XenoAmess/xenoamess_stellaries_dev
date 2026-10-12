"""At most six real native months; every actual nonzero/boundary stops."""
import json,os,subprocess,sys
from pathlib import Path
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z')
before='terravore-three-labs-normal-month-22811001';proof=before+'-three-labs-serial-month-v2-proof.json';execution=before+'-serial-labs-guard-v2'
env=os.environ.copy();env['PYTHONPATH']=str(Path('_runtime/heart-of-devouring').resolve())+os.pathsep+str(Path('eat_everything_origin/tools').resolve())
helpers={'priority_terravore_labs_native_calendar_v7_20261013.py':'659c34fe713d76de674b97d2f455278034efb51a125d291f32fa2a4cd9d4a3c1','priority_terravore_labs_native_observer_v7_20261013.py':'15ff4f3976e98cd18c0c37ed864582949c6564182ed092d36d2b426293faa46e','priority_terravore_three_labs_serial_guard_v2_20261013.py':'450e79e2aa8fbe26fc79a1a646bf4e542bd12a64f251a1346fe2da8cd084f952'}
import hashlib
assert all(hashlib.sha256((run/k).read_bytes()).hexdigest()==v for k,v in helpers.items())
def call(stage,helper,args):
 x=subprocess.run([sys.executable,str(run/'record_current_helper.py'),stage,str(run/helper),*args],capture_output=True,env=env)
 print(x.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(x.stderr.decode('utf-8',errors='replace'),end='',flush=True);assert x.returncode==0,'Actual failure retained; do not continue'
for _ in range(6):
 a=json.loads((run/(before+'.audit.json')).read_text('utf-8'));y,m,d=map(int,a['date'].split('.'));assert d==1;m+=1
 if m==13:y+=1;m=1
 end=f'{y:04}.{m:02}.01';after=f'terravore-three-labs-normal-month-{y:04}{m:02}01'
 call(after+'-calendar','priority_terravore_labs_native_calendar_v7_20261013.py',[before,end,after,'30',proof,execution])
 call(after+'-boundary-observation-v4','priority_terravore_labs_native_observer_v7_20261013.py',[before,after,end,'30'])
 call(after+'-serial-labs-guard-v2','priority_terravore_three_labs_serial_guard_v2_20261013.py',[before,after,proof,execution])
 proof=after+'-three-labs-serial-month-v2-proof.json';execution=after+'-serial-labs-guard-v2';before=after;p=json.loads((run/proof).read_text('utf-8'))
 print(json.dumps({'MONTH_COMPLETE':end,'project2':p['project2_progress'],'zone':p['front_lab_progress'],'boundaries':p['boundaries']}),flush=True)
 if not p['native_devour_calendar_ready']:break
