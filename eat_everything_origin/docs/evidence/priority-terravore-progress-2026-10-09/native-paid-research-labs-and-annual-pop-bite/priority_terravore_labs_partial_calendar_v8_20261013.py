"""One normal native calendar input with date, prior proof and stage checks before GUI."""
import io,json,logging,shutil,sys,time,zipfile
import audit_save
from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair
from pathlib import Path
def validate_native_interval(start,end,days):
 def ordinal(value):
  year,month,day=map(int,value.split('.'));assert year>=1 and 1<=month<=12 and 1<=day<=30
  return year*360+(month-1)*30+day-1
 assert 1<=days<=360 and ordinal(end)-ordinal(start)==days,'Native30-day date mismatch; no GUI action allowed'
 return end
def validate_business_interval(pre,start,end,days,review=None):
 boundaries=pre.get('boundaries',[])
 ready=pre.get('native_devour_calendar_ready',False)
 maximum=pre.get('maximum_days_to_native_bite_boundary',0)
 if not boundaries and ready and 1<=days<=maximum:
  assert review is None,'Unexpected review for ordinary ready interval'
  return
 assert isinstance(review,dict),'Business boundary or unready interval requires independent review before GUI'
 assert review.get('status')=='PASS_REVIEWED_NATIVE_BOUNDARY'
 assert review.get('checks') and all(v is True for v in review['checks'].values())
 assert review.get('before_sha256')==pre.get('after_sha256')
 assert (review.get('start_date'),review.get('end_date'),review.get('days'))==(start,end,days)
 assert sorted(review.get('allowed_boundaries',[]))==sorted(boundaries)
 assert 1<=days<=review.get('maximum_days',0)

if __name__=='__main__':
 start,end,stage,raw_days,preproof_file,preexecution_stage,*review_names=sys.argv[1:];days=int(raw_days);assert len(review_names)<=1
 sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
 logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0' and m['language']=='l_simp_chinese'
 dest=run/Path(__file__).name
 if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
 else:shutil.copyfile(__file__,dest)
 b=json.loads((run/(start+'.audit.json')).read_text('utf-8'));validate_native_interval(b['date'],end,days)
 assert not list(run.glob(stage+'*')),'Stage already has artifacts; do not repeat calendar'
 pre=json.loads((run/preproof_file).read_text('utf-8'));execution=json.loads((run/(preexecution_stage+'-execution.json')).read_text('utf-8'))
 assert pre['status'].startswith('PASS') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and execution['returncode']==0
 review=json.loads((run/review_names[0]).read_text('utf-8-sig')) if review_names else None
 if review is not None:
  re=json.loads((run/(review['execution_stage']+'-execution.json')).read_text('utf-8-sig'))
  assert re['returncode']==0 and re['helper_sha256']==h.sha256(Path(re['command'][1]))
  assert review['after_sha256']==pre['after_sha256']
 validate_business_interval(pre,b['date'],end,days,review)
 assert h.sha256(run/(start+'.sav'))==b['save_sha256']
 eb=(user/'logs/error.log').read_bytes();assert reviewed_error_pair((run/(start+'-error-after.log')).read_bytes(),eb,run);(run/(stage+'-error-before.log')).write_bytes(eb)
 assert 1<=days<=30 and end.endswith('.01'),'Native autosave interval must end at the next month boundary'
 target_name='autosave_'+end+'.sav';initial={str(p):p.stat().st_mtime_ns for p in (user/'save games').rglob(target_name)}
 h.press_scan_code(0x29,stage+'-console-open',1);h.type_text('fast_forward '+str(days),True,stage+'-native-days')
 deadline=time.monotonic()+180;source=None;data=None
 while time.monotonic()<deadline:
  for candidate in (user/'save games').rglob(target_name):
   try:
    sig=candidate.stat().st_mtime_ns
    if sig<=initial.get(str(candidate),0):continue
    raw=candidate.read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
     if z.testzip() is not None:continue
     metadata=audit_save.scalars(z.read('meta').decode('utf-8-sig'))
     if metadata.get('date')!=end:continue
    if candidate.stat().st_mtime_ns!=sig:continue
    source=candidate;data=raw;source_mtime=sig;break
   except (OSError,zipfile.BadZipFile,KeyError):continue
  if source is not None:break
  time.sleep(.2)
 assert source is not None,'No complete fresh target native autosave; do not repeat clock'
 time.sleep(1);h.press_scan_code(0x29,stage+'-console-close',1)
 destination=run/(stage+'.sav');assert not destination.exists();destination.write_bytes(data)
 a=audit_save.audit(destination,(0,));h.write_json(run/(stage+'.audit.json'),a);assert a['date']==end
 ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);assert ea==eb,'New error retained; no continuation'
 h.write_json(run/(stage+'.native-save.json'),{'written_at':str(source),'archived':str(destination),'sha256':a['save_sha256'],'date':a['date'],'source_mtime_ns':source_mtime,'evidence_type':'original_native_autosave','manual_save_UI_used':False})
 h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','evidence_type':'original_native_autosave_gamestate_date','date':end,'start_date':b['date'],'days':days,'prior_proof_file':preproof_file,'prior_execution_stage':preexecution_stage,'business_preflight':True,'review_file':review_names[0] if review_names else None,'review_sha256':h.sha256(run/review_names[0]) if review_names else None,'original_native_autosave_source':str(source),'save_sha256':a['save_sha256'],'scope':'Exact30 native calendar verified by newly written complete native autosave date. No fabricated OCR/control-console output receipt.'})
 v={'status':'OBSERVED_NATIVE_CALENDAR','date':a['date'],'save_sha256':a['save_sha256'],'population':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in a['countries']['0']['owned_colonies']),'new_error_bytes':len(ea)-len(eb),'scope':'One native month; original autosave endpoint, independent business checks required.'};h.write_json(run/(stage+'-state.json'),v);print(json.dumps(v),flush=True)
