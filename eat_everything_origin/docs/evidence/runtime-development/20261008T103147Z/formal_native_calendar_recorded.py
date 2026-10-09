import hashlib,json,subprocess,sys
from pathlib import Path
start,end,stage,days=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');helper=Path('_runtime/heart-of-devouring/formal_production_native_calendar.py');source=Path(__file__);dest=run/source.name
if not dest.exists():dest.write_bytes(source.read_bytes())
assert dest.read_bytes()==source.read_bytes();out=run/(stage+'-calendar-execution.json');assert not out.exists()
command=[sys.executable,str(helper),start,end,stage,days];result=subprocess.run(command,capture_output=True)
files=[]
for suffix,data in (('stdout.txt',result.stdout),('stderr.txt',result.stderr)):
 p=run/(stage+'-calendar-'+suffix);assert not p.exists();p.write_bytes(data);files.append({'name':p.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
receipt={'status':'COMPLETED_CALENDAR_HELPER' if result.returncode==0 else 'FAILED_CALENDAR_HELPER','command':command,'returncode':result.returncode,'calendar_helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'recording_wrapper_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_output_files':files,'scope':'Exact original stdout/stderr byte recording only. No retry or extra date advance.'};out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(result.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(result.stderr.decode('utf-8',errors='replace'),end='',flush=True);print(json.dumps(receipt),flush=True);sys.exit(result.returncode)
