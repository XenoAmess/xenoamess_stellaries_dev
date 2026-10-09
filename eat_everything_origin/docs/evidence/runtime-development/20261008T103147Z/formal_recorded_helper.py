import hashlib,json,subprocess,sys
from pathlib import Path
stage,helper,*args=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8')
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');source=Path(__file__);dest=run/source.name
if not dest.exists():dest.write_bytes(source.read_bytes())
assert dest.read_bytes()==source.read_bytes()
outputs={s:run/(stage+'-'+s) for s in ['stdout.txt','stderr.txt','execution.json']}
assert all(not p.exists() for p in outputs.values())
command=[sys.executable,helper,*args];helper_sha=hashlib.sha256(Path(helper).read_bytes()).hexdigest()
result=subprocess.run(command,capture_output=True);files=[]
for suffix,data in [('stdout.txt',result.stdout),('stderr.txt',result.stderr)]:
    outputs[suffix].write_bytes(data);files.append({'name':outputs[suffix].name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
receipt={'returncode':result.returncode,'command':command,'helper_sha256':helper_sha,'recording_wrapper_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_files':files,'scope':'Exact original outputs. One invocation only; no retry or new game command.'}
outputs['execution.json'].write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(result.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(result.stderr.decode('utf-8',errors='replace'),end='',flush=True);print(json.dumps(receipt),flush=True);sys.exit(result.returncode)
