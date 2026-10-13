"""At most eight individually reviewed native months, stop on any nonzero or unknown boundary."""
import hashlib, json, os, subprocess, sys
from pathlib import Path
before, proof, execution, raw_count = sys.argv[1:]; count=int(raw_count); assert 1<=count<=8
root=Path('_runtime/heart-of-devouring');run=root/'runs/20261009T044016Z'
helpers={
 'guard':(root/'priority_terravore_support_zone_v1_20261013.py','d0eb9bbe7e51df0d9894b0030bc8c32f50121e8186e9be37f3417cbedf434cce'),
 'calendar':(run/'priority_terravore_labs_native_calendar_v7_20261013.py','659c34fe713d76de674b97d2f455278034efb51a125d291f32fa2a4cd9d4a3c1'),
 'observer':(run/'priority_terravore_labs_native_observer_v8_20261013.py','b2a7d6de08f1897cdd05654ea02e02abeb30889eab95e29f0e3976bd6820f98a'),
}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(path)==expected for path,expected in helpers.values())
env=os.environ.copy();env['PYTHONPATH']=os.pathsep.join(str(p.resolve()) for p in [run,root,Path('eat_everything_origin/tools')])
def call(stage,kind,args):
 path,expected=helpers[kind]
 assert sha(path)==expected
 result=subprocess.run([sys.executable,str(run/'record_current_helper.py'),stage,str(path),*args],capture_output=True,env=env)
 for suffix,data in [('stdout.txt',result.stdout),('stderr.txt',result.stderr)]:
  dest=run/(stage+'-driver-child-'+suffix);assert not dest.exists();dest.write_bytes(data)
 print(json.dumps({'stage':stage,'actual':result.returncode}),flush=True)
 assert result.returncode==0,'Child failed; originals retained, no continuation or retry'
 rec=json.loads((run/(stage+'-execution.json')).read_text('utf-8'))
 assert rec['returncode']==0 and rec['helper_sha256']==expected
for _ in range(count):
 p=json.loads((run/proof).read_text('utf-8'));assert p['status'].startswith('PASS') and p['checks'] and all(v is True for v in p['checks'].values())
 a=json.loads((run/(before+'.audit.json')).read_text('utf-8'));y,m,d=map(int,a['date'].split('.'));assert d==1
 m+=1
 if m==13:y+=1;m=1
 end=f'{y:04}.{m:02}.01';assert end<='2287.01.01';after=f'terravore-second-society-month-{y:04}{m:02}01'
 review=before+'-support-zone-v1-review'
 call(review,'guard',['review',before,end,proof,execution])
 call(after+'-calendar','calendar',[before,end,after,'30',proof,execution,review+'.json'])
 call(after+'-boundary-observation-v4','observer',[before,after,end,'30'])
 call(after+'-support-zone-v1-guard','guard',['guard',before,after,proof,execution])
 proof=after+'-support-zone-v1-proof.json';execution=after+'-support-zone-v1-guard';before=after
 p=json.loads((run/proof).read_text('utf-8'))
 print(json.dumps({'MONTH_COMPLETE':end,'project3':p['project3_progress'],'zone_work':p['paid_zone_head_work'],'routes':p['routes'],'after_sha256':p['after_sha256']}),flush=True)
