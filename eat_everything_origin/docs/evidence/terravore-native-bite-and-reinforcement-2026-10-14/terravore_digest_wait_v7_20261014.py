"""At most90 native idle days; fresh monthly autosaves, independent guard each."""
import io,json,logging,subprocess,sys,time,zipfile
from pathlib import Path
start,count_text,prior_file,prior_execution=sys.argv[1:]
count=int(count_text);assert 1<=count<=3
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
old=json.loads((run/(start+'.audit.json')).read_text('utf-8'))
proof=json.loads((run/prior_file).read_text('utf-8'))
execution=json.loads((run/prior_execution).read_text('utf-8'))
assert proof['pass'] and proof.get('calendar_ready',True) and proof['after_save_sha256']==old['save_sha256']
assert execution['returncode']==0 and h.sha256(Path(execution['command'][1]))==execution['helper_sha256']
assert meta['language']=='l_simp_chinese' and meta['version']=='0.2.0'
assert h.tree_manifest(r.ROOT/'mod')[1]==meta['repository_mod_tree_sha256']
assert h.tree_manifest(Path(meta['copied_mod']))[1]==meta['copied_mod_tree_sha256']
assert h.sha256(run/(start+'.sav'))==old['save_sha256']
date=old['date'];stage_prefix='hope-route-wait-'+date.replace('.','')
frame=r.gpu_capture(stage_prefix+'-pre')
assert date in [x['text'] for x in frame['rows']] and '暂停' in [x['text'] for x in frame['rows']]
wait_until='2297.01.01'
total=0
for step in range(count):
 y,m,d=map(int,date.split('.'));days=31-d
 if m==12:y,m=y+1,1
 else:m+=1
 end=f'{y:04d}.{m:02d}.01';stage='hope-route-wait-native-'+end.replace('.','')
 assert total+days<=90 and end<=wait_until
 assert not list(run.glob(stage+'*'))
 error=(user/'logs/error.log').read_bytes()
 assert error==(run/(start+'-error-after.log')).read_bytes()
 (run/(stage+'-error-before.log')).write_bytes(error)
 target='autosave_'+end+'.sav'
 initial={str(p):p.stat().st_mtime_ns for p in (user/'save games').rglob(target)}
 h.press_scan_code(0x29,stage+'-console-open',1);h.type_text('fast_forward '+str(days),True,stage+'-native-days')
 deadline=time.monotonic()+180;source=None
 while time.monotonic()<deadline:
  for p in (user/'save games').rglob(target):
   try:
    sig=p.stat().st_mtime_ns
    if sig<=initial.get(str(p),0):continue
    data=p.read_bytes()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
     if z.testzip() is not None or q.scalars(z.read('meta').decode('utf-8-sig')).get('date')!=end:continue
    if sig!=p.stat().st_mtime_ns:continue
    source=p;break
   except (OSError,zipfile.BadZipFile,KeyError):continue
  if source is not None:break
  time.sleep(.2)
 assert source is not None,'No fresh complete native autosave; do not repeat calendar'
 time.sleep(1);h.press_scan_code(0x29,stage+'-console-close',1)
 destination=run/(stage+'.sav');destination.write_bytes(data)
 saved=q.audit(destination,(0,1,15));h.write_json(run/(stage+'.audit.json'),saved)
 assert saved['date']==end
 h.write_json(run/(stage+'.native-save.json'),{'evidence_type':'original_native_autosave','source':str(source),'source_mtime_ns':sig,'date':end,'save_sha256':saved['save_sha256'],'manual_save_UI_used':False})
 h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','evidence_type':'fresh_native_autosave_date','start':date,'date':end,'days':days,'save_sha256':saved['save_sha256']})
 after=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(after)
 assert after==error,'New errors retained; stop'
 guard_stage=stage+'-digest-guard-v6'
 result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/record_current_helper.py',guard_stage,'_runtime/heart-of-devouring/terravore_digest_guard_v6_20261014.py',start,stage],capture_output=True)
 print(result.stdout.decode('utf-8',errors='replace'),flush=True)
 if result.returncode:raise RuntimeError('Independent waiting guard failed; no next month')
 proof=json.loads((run/(stage+'-digest-v6-proof.json')).read_text('utf-8'))
 start,date=stage,end;total+=days
 if not proof['calendar_ready']:break
frame=r.gpu_capture(stage_prefix+'-end')
print(json.dumps({'date':date,'last_stage':start,'days':total,'calendar_ready':proof['calendar_ready'],'boundaries':proof.get('boundaries',[]),'UI_sha256':frame['image_sha256']}),flush=True)
