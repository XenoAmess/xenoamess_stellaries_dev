"""Read-only check of every staged immutable evidence blob in one git process."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
archive=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T103147Z')
manifest=json.loads((archive/'source-snapshot.json').read_text(encoding='utf-8'))
expected={row['file']:row['sha256'] for row in manifest['files']}
for name in ['source-snapshot.json','.gitattributes']:
    expected[name]=hashlib.sha256((archive/name).read_bytes()).hexdigest()
assert len(expected)==len(manifest['files'])+2
p=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
count=total=0
try:
    for rel,wanted in expected.items():
        path=(archive/rel).as_posix()
        p.stdin.write((':'+path+'\n').encode('utf-8'));p.stdin.flush()
        header=p.stdout.readline().decode('ascii').strip().split()
        assert len(header)==3 and header[1]=='blob',(path,header)
        size=int(header[2]);remaining=size;sha=hashlib.sha256()
        while remaining:
            chunk=p.stdout.read(min(1048576,remaining));assert chunk
            sha.update(chunk);remaining-=len(chunk)
        assert p.stdout.read(1)==b'\n'
        assert sha.hexdigest()==wanted,path
        count+=1;total+=size
    p.stdin.close();rc=p.wait(timeout=15)
    assert rc==0 and p.stderr.read()==b''
finally:
    if p.poll() is None:p.kill();p.wait()
result={'status':'PASS_STAGED_RAW_BLOBS','files':count,'bytes':total,
        'source_snapshot_sha256':expected['source-snapshot.json'],
        'exit_acceptance':manifest['exit_acceptance'],
        'scope':'Staged raw-byte archive integrity only; forced-stop failure retained.'}
out=Path('eat_everything_origin/docs/evidence/priority-handover-staged-blob-verification-2026-10-09.json')
assert not out.exists()
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result),flush=True)
