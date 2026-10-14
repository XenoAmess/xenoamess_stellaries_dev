"""Record one helper invocation against the actual resulting isolated run."""
import hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
sys.stdout.reconfigure(encoding='utf-8')
stage,helper,*args=sys.argv[1:]
pointer=Path('_runtime/heart-of-devouring/runs/current-run.json')
before=json.loads(pointer.read_text(encoding='utf-8')) if pointer.exists() else None
source=Path(helper);raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest()
started=datetime.now(timezone.utc).isoformat()
result=subprocess.run([sys.executable,helper,*args],capture_output=True)
after=json.loads(pointer.read_text(encoding='utf-8'))
run=Path(after['artifact_dir'])
for src,data in [(Path(__file__),Path(__file__).read_bytes()),(source,raw)]:
    dest=run/src.name
    if dest.exists():assert dest.read_bytes()==data
    else:dest.write_bytes(data)
records=[]
for suffix,data in [('stdout.txt',result.stdout),('stderr.txt',result.stderr)]:
    out=run/(stage+'-'+suffix);assert not out.exists();out.write_bytes(data)
    records.append({'file':out.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
receipt={'started_at_utc':started,'finished_at_utc':datetime.now(timezone.utc).isoformat(),
         'command':[sys.executable,helper,*args],'helper_sha256':sha,
         'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'returncode':result.returncode,'run_pointer_before':before,'run_pointer_after':after,
         'outputs':records,'scope':'One invocation; original streams and return code. No retries.'}
out=run/(stage+'-execution.json');assert not out.exists()
out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(result.stdout.decode('utf-8',errors='replace'),end='',flush=True)
print(result.stderr.decode('utf-8',errors='replace'),end='',flush=True)
print(json.dumps(receipt),flush=True);sys.exit(result.returncode)
