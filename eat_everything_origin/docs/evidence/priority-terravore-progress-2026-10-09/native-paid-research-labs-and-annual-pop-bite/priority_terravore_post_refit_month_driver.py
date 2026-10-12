"""At most five real native months; every actual nonzero/boundary stops."""
import json,os,subprocess,sys
from pathlib import Path
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z')
before='terravore-post-refit-full-month-22810101';proof=before+'-post-refit-stable-month-v2-proof.json';execution=before+'-stable-month-guard-v2'
env=os.environ.copy();env['PYTHONPATH']=str(Path('_runtime/heart-of-devouring').resolve())+os.pathsep+str(Path('eat_everything_origin/tools').resolve())
helpers={'formal_production_native_calendar_checked_v5.py':'736473506dec7a0255508961f4e3a163fbf7b06375528fce2371737a46d595b3','priority_terravore_construction_boundary_observation_v4.py':'973488fd0aa6b21741c1a038e12f4c1e925501fe7db8d82817ada6ba601e3f05','priority_terravore_post_refit_stable_month_guard_v2.py':'9933c862f0b14416bd64d0024c0568917b83e99e643bca035cbb8d9d949ae61c'}
import hashlib
assert all(hashlib.sha256((run/k).read_bytes()).hexdigest()==v for k,v in helpers.items())
def call(stage,helper,args):
 x=subprocess.run([sys.executable,str(run/'record_current_helper.py'),stage,str(run/helper),*args],capture_output=True,env=env)
 print(x.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(x.stderr.decode('utf-8',errors='replace'),end='',flush=True);assert x.returncode==0,'Actual failure retained; do not continue'
for _ in range(5):
 a=json.loads((run/(before+'.audit.json')).read_text('utf-8'));y,m,d=map(int,a['date'].split('.'));assert d==1;m+=1
 if m==13:y+=1;m=1
 end=f'{y:04}.{m:02}.01';after=f'terravore-post-refit-normal-month-{y:04}{m:02}01'
 call(after+'-calendar','formal_production_native_calendar_checked_v5.py',[before,end,after,'30',proof,execution])
 call(after+'-boundary-observation-v4','priority_terravore_construction_boundary_observation_v4.py',[before,after,end,'30'])
 call(after+'-stable-month-guard-v2','priority_terravore_post_refit_stable_month_guard_v2.py',[before,after,proof,execution])
 proof=after+'-post-refit-stable-month-v2-proof.json';execution=after+'-stable-month-guard-v2';before=after;p=json.loads((run/proof).read_text('utf-8'))
 print(json.dumps({'MONTH_COMPLETE':end,'project2':p['project2_progress'],'zone':p['engineering_zone_progress'],'boundaries':p['boundaries']}),flush=True)
 if not p['native_devour_calendar_ready']:break
