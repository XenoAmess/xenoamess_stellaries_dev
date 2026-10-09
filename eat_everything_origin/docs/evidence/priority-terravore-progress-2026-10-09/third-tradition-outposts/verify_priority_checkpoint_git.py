"""Check staged raw bytes of a priority checkpoint and its preparation inputs."""
import hashlib,json,subprocess,sys
from pathlib import Path
label=sys.argv[1]
checkpoint=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09')/label
preparation=Path('eat_everything_origin/docs/evidence/priority-terravore-preparation-2026-10-09')
expected={}
for root in [checkpoint,preparation]:
    snapshot=json.loads((root/'source-snapshot.json').read_text(encoding='utf-8'))
    for row in snapshot['files']:expected[(root/row['file']).as_posix()]=row['sha256']
    for name in ['source-snapshot.json','.gitattributes']:
        path=root/name;expected[path.as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
for path in Path('eat_everything_origin/docs/evidence').glob('priority-*.json'):
    expected[path.as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
p=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
total=0
try:
    for path,wanted in expected.items():
        p.stdin.write((':'+path+'\n').encode('utf-8'));p.stdin.flush()
        header=p.stdout.readline().decode('ascii').strip().split()
        assert len(header)==3 and header[1]=='blob',(path,header)
        size=int(header[2]);remaining=size;sha=hashlib.sha256()
        while remaining:
            raw=p.stdout.read(min(1048576,remaining));assert raw
            sha.update(raw);remaining-=len(raw)
        assert p.stdout.read(1)==b'\n';assert sha.hexdigest()==wanted,path
        total+=size
    p.stdin.close();assert p.wait(timeout=15)==0 and p.stderr.read()==b''
finally:
    if p.poll() is None:p.kill();p.wait()
out=Path('eat_everything_origin/docs/evidence')/('priority-'+label+'-staged-verification-2026-10-09.json')
assert not out.exists()
proof={'status':'PASS_STAGED_RAW_PRIORITY_CHECKPOINT','files':len(expected),'bytes':total,
       'checkpoint':checkpoint.as_posix(),
       'scope':'Raw bytes only; preparation and actual initial/month components remain scoped. Original failures retained.'}
out.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(proof),flush=True)
