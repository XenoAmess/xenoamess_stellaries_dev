"""At most seven individually reviewed normal months after the first verified month."""
import hashlib,json,os,subprocess,sys
from pathlib import Path

before,proof,execution,raw_count=sys.argv[1:]
count=int(raw_count);assert 1<=count<=7
root=Path('_runtime/heart-of-devouring');run=root/'runs/20261009T044016Z'
helpers={
 'review':('priority_terravore_post_society_month_review_v2_20261013.py','381b02f47d2573c77f3dc5b3feb1225e023a405024205d131ad1b30acee51fb9'),
 'calendar':('priority_terravore_labs_native_calendar_v7_20261013.py','659c34fe713d76de674b97d2f455278034efb51a125d291f32fa2a4cd9d4a3c1'),
 'observer':('priority_terravore_labs_native_observer_v8_20261013.py','b2a7d6de08f1897cdd05654ea02e02abeb30889eab95e29f0e3976bd6820f98a'),
 'guard':('priority_terravore_post_society_month_guard_20261013.py','3e4d4c426c682ee0796ab377f35a2c773a382e1cba8f191c5dfefa2c4815fa94'),
}
for name,sha in helpers.values():
    assert hashlib.sha256((run/name).read_bytes()).hexdigest()==sha
environment=os.environ.copy();environment['PYTHONPATH']=os.pathsep.join(str(p.resolve()) for p in [run,root,Path('eat_everything_origin/tools')])
wrapper=run/'record_current_helper.py'
assert wrapper.is_file()

def call(stage,kind,args):
    name,sha=helpers[kind];source=run/name
    assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
    result=subprocess.run([sys.executable,str(wrapper),stage,str(source),*args],capture_output=True,env=environment)
    for suffix,raw in [('stdout.txt',result.stdout),('stderr.txt',result.stderr)]:
        dest=run/(stage+'-driver-child-'+suffix);assert not dest.exists();dest.write_bytes(raw)
    print(json.dumps({'stage':stage,'actual':result.returncode}),flush=True)
    assert result.returncode==0,'Original child streams and return code retained; no calendar retry'
    receipt=json.loads((run/(stage+'-execution.json')).read_text('utf-8'))
    assert receipt['returncode']==0 and receipt['helper_sha256']==sha

for _ in range(count):
    p=json.loads((run/proof).read_text('utf-8'))
    x=json.loads((run/(execution+'-execution.json')).read_text('utf-8'))
    audit=json.loads((run/(before+'.audit.json')).read_text('utf-8'))
    assert p['status'].startswith('PASS') and p['checks'] and all(v is True for v in p['checks'].values()) and x['returncode']==0 and p['after_sha256']==audit['save_sha256']
    y,m,d=map(int,audit['date'].split('.'));assert d==1
    ny,nm=(y+1,1) if m==12 else (y,m+1)
    end=f'{ny:04}.{nm:02}.01';assert end<='2287.10.01'
    after=f'terravore-post-second-society-month-{ny:04}{nm:02}01'
    review=before+'-post-second-society-month-review-v2'
    call(review,'review',[before,end,proof,execution])
    call(after+'-calendar','calendar',[before,end,after,'30',proof,execution,review+'.json'])
    call(after+'-boundary-observation-v4','observer',[before,after,end,'30'])
    call(after+'-post-second-society-month-guard','guard',[before,after,proof,execution])
    before=after;proof=after+'-post-second-society-month-proof.json';execution=after+'-post-second-society-month-guard'
    result=json.loads((run/proof).read_text('utf-8'))
    print(json.dumps({'MONTH_COMPLETE':end,'project3':result['project3_progress'],'hive_work':result['hive_front_work'],'after_sha256':result['after_sha256']}),flush=True)
