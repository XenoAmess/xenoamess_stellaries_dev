"""Capture original native autosaves while one existing checked calendar runs."""
import io,json,logging,subprocess,sys,threading,time,zipfile
from datetime import datetime,timezone
args=sys.argv[1:];assert len(args)==6
before,end,after,days,proof,execution=args
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
output=run/(after+'-autosave-capture.json');assert not output.exists()
baseline={str(p):p.stat().st_mtime_ns for p in (user/'save games').rglob('autosave_*.sav')}
stop=threading.Event();copies={};errors=[];incomplete={}
def capture():
 while not stop.wait(.1):
  for p in (user/'save games').rglob('autosave_*.sav'):
   try:
    signature=p.stat().st_mtime_ns
    if signature<=baseline.get(str(p),0) or (str(p),signature) in copies:continue
    data=p.read_bytes()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
     assert z.testzip() is None
     header=q.scalars(z.read('meta').decode('utf-8-sig'));date=header['date']
    if p.stat().st_mtime_ns!=signature:continue
    destination=run/(after+'-original-'+p.name);assert not destination.exists()
    destination.write_bytes(data)
    copies[(str(p),signature)]={'source':str(p),'source_mtime_ns':signature,'captured_at_utc':datetime.now(timezone.utc).isoformat(),'preserved':destination.name,'date':date,'bytes':len(data),'sha256':h.sha256(destination)}
   except (OSError,zipfile.BadZipFile,KeyError) as e:incomplete[str(p)]=type(e).__name__
   except Exception as e:errors.append(repr(e));stop.set();return
thread=threading.Thread(target=capture);thread.start()
try:
 command=[sys.executable,str(run/'record_current_helper.py'),after+'-calendar',str(run/'formal_production_native_calendar_checked_v4.py'),before,end,after,days,proof,execution]
 result=subprocess.run(command,capture_output=True)
 (run/(after+'-autosave-calendar-driver-stdout.txt')).write_bytes(result.stdout)
 (run/(after+'-autosave-calendar-driver-stderr.txt')).write_bytes(result.stderr)
finally:
 time.sleep(.5);stop.set();thread.join()
observations=[]
for entry in copies.values():
 au=q.audit(run/entry['preserved'],(0,));h.write_json(run/(entry['preserved']+'.audit.json'),au);entry['audit_file']=entry['preserved']+'.audit.json';observations.append(entry)
checks={'checked_calendar_actual0':result.returncode==0,'watcher_no_unhandled_error':not errors,'at_least_one_complete_original_autosave':bool(observations),'all_preserved_bytes_original_bound':all(x['sha256']==h.sha256(run/x['preserved']) for x in observations)}
h.write_json(output,{'status':'OBSERVED_NATIVE_AUTOSAVES' if all(checks.values()) else 'FAIL','checks':checks,'command':command,'actual_returncode':result.returncode,'autosaves':observations,'errors':errors,'incomplete_read_attempts':incomplete,'scope':'Original native autosave collection only; timing and business parity require independent review.'})
print(json.dumps({'checks':checks,'autosaves':[{'file':x['preserved'],'date':x['date'],'sha256':x['sha256']} for x in observations],'errors':errors}),flush=True);assert all(checks.values())
