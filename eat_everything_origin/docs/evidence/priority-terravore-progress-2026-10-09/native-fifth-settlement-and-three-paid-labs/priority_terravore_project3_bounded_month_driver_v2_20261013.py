"""At most six normal native months; preserve child records and stop at every boundary."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
before,proof,execution,raw_count=sys.argv[1:];count=int(raw_count);assert 1<=count<=6
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z')
helpers={'priority_terravore_labs_native_calendar_v7_20261013.py': '659c34fe713d76de674b97d2f455278034efb51a125d291f32fa2a4cd9d4a3c1', 'priority_terravore_labs_native_observer_v8_20261013.py': 'b2a7d6de08f1897cdd05654ea02e02abeb30889eab95e29f0e3976bd6820f98a', 'priority_terravore_remaining_labs_month_guard_v8_20261013.py': '80425cfde5a71b52c8a099b81a7a95541d6b6122e971beff5b2e3e7f29025729'}
assert all(hashlib.sha256((run/k).read_bytes()).hexdigest()==v for k,v in helpers.items())
env=os.environ.copy();env['PYTHONPATH']=str(run.resolve())+os.pathsep+str(Path('_runtime/heart-of-devouring').resolve())+os.pathsep+str(Path('eat_everything_origin/tools').resolve())
def call(stage,helper,args):
 result=subprocess.run([sys.executable,str(run/'record_current_helper.py'),stage,str(run/helper),*args],capture_output=True,env=env)
 print(json.dumps({'stage':stage,'actual':result.returncode}),flush=True)
 assert result.returncode==0,'Child original streams retained; no continuation'
 receipt=json.loads((run/(stage+'-execution.json')).read_text('utf-8'))
 assert receipt['returncode']==0 and receipt['helper_sha256']==helpers[helper]
for _ in range(count):
 prior=json.loads((run/proof).read_text('utf-8'));assert prior['checks'] and all(v is True for v in prior['checks'].values()) and prior['native_devour_calendar_ready'] and prior['maximum_days_to_native_bite_boundary']>=30
 a=json.loads((run/(before+'.audit.json')).read_text('utf-8'));y,m,d=map(int,a['date'].split('.'));assert d==1;m+=1
 if m==13:y+=1;m=1
 end=f'{y:04}.{m:02}.01';after=f'terravore-project3-normal-month-{y:04}{m:02}01'
 call(after+'-calendar','priority_terravore_labs_native_calendar_v7_20261013.py',[before,end,after,'30',proof,execution])
 call(after+'-boundary-observation-v4','priority_terravore_labs_native_observer_v8_20261013.py',[before,after,end,'30'])
 call(after+'-remaining-labs-guard-v8','priority_terravore_remaining_labs_month_guard_v8_20261013.py',[before,after,proof,execution])
 proof=after+'-remaining-labs-month-v8-proof.json';execution=after+'-remaining-labs-guard-v8';before=after;p=json.loads((run/proof).read_text('utf-8'))
 print(json.dumps({'MONTH_COMPLETE':end,'project3':p['project3_progress'],'zone':p['front_lab_progress'],'boundaries':p['boundaries']}),flush=True)
 if not p['native_devour_calendar_ready']:break
