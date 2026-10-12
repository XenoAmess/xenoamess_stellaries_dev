"""Three fixed reviewed native project2 countdown intervals, fail closed on every subprocess."""
import json,subprocess,sys
from pathlib import Path
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z');wrapper=run/'record_current_helper.py'
before='terravore-project2-first-tick-date';proof=before+'-project2-wait-v3-proof.json';execution=before+'-wait-guard-v3'
def call(stage,helper,*args):
 print(json.dumps({'phase':stage,'helper':helper}),flush=True)
 subprocess.run([sys.executable,str(wrapper),stage,str(run/helper),*args],check=True,stdout=subprocess.DEVNULL)
 e=json.loads((run/(stage+'-execution.json')).read_text('utf-8-sig'));assert e['returncode']==0
for n,(end,days) in enumerate([('2279.01.09',7),('2279.01.16',7),('2279.01.19',3)],1):
 after=f'terravore-project2-pirate-watch-{n:02}';review=f'terravore-project2-countdown-review-{n:02}'
 call(review,'priority_terravore_project2_wait_review.py',before,end,str(days),proof,execution,review)
 call(after+'-calendar','formal_production_native_calendar_checked_v3.py',before,end,after,str(days),proof,execution,review+'-proof.json')
 call(after+'-boundary-observation-v2','priority_terravore_construction_boundary_observation_v2.py',before,after,end,str(days))
 call(after+'-wait-guard-v3','priority_terravore_project2_wait_guard_v3.py',before,after)
 proof=after+'-project2-wait-v3-proof.json';execution=after+'-wait-guard-v3';p=json.loads((run/proof).read_text('utf-8'));assert len(p['checks'])==23 and all(v is True for v in p['checks'].values())
 print(json.dumps({'step':n,'date':end,'physics_progress':p['physics_progress'],'pirate_remaining':p['pirate_remaining'],'after_sha256':p['after_sha256']}),flush=True);before=after
print('PASS_FIXED_COUNTDOWN_DRIVER',flush=True)
