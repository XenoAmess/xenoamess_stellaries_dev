"""Observe one already executed native command after wrong expected-date failure; never advance."""
import importlib.util,json,logging,shutil,sys
from pathlib import Path
before,original,after,date=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0' and m['language']=='l_simp_chinese'
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
assert not list(run.glob(after+'*'))
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));pre=json.loads((run/(before+'-second-shipyard-payment-proof.json')).read_text('utf-8'))
original_execution=run/(original+'-observe-execution.json');exe=json.loads(original_execution.read_text('utf-8'))
assert exe['returncode']!=0 and exe['command'][-4:]==[before,'2236.06.01',original,'13']
assert pre['status']=='PASS_NATIVE_TERRAVORE_SECOND_SHIPYARD_PAYMENT_COMPONENT' and len(pre['checks'])==40 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav'))
assert json.loads((run/'terravore-defense-second-shipyard-payment-guard-execution.json').read_text('utf-8'))['returncode']==0
action=json.loads((run/(original+'-native-days.action.json')).read_text('utf-8'));enter=json.loads((run/(original+'-native-days-enter.action.json')).read_text('utf-8'))
assert action['action']=='type_text' and action['text']=='fast_forward 13' and action['submitted'] is True and enter['scan_code']==28 and enter['repeat']==1
vp=Path('_runtime/heart-of-devouring/formal_production_native_calendar_checked_v2.py');validation=json.loads((run/'checked-calendar-v2-date-validation.json').read_text('utf-8'))
assert validation['status']=='PASS_CALENDAR_DATE_VALIDATION_NO_GUI' and all(validation['checks'].values()) and validation['helper_sha256']==h.sha256(vp)
spec=importlib.util.spec_from_file_location('native_checked_calendar_v2',vp);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.validate_native_interval(b['date'],date,13)
vd=run/vp.name
if vd.exists():assert vd.read_bytes()==vp.read_bytes()
else:shutil.copyfile(vp,vd)
polls=sorted(run.glob(original+'-calendar-poll-*.ocr.json'),key=lambda p:p.stat().st_mtime);assert polls
labels=[x['text'] for x in json.loads(polls[-1].read_text('utf-8'))['rows']]
def matched(labels):return date in labels and '\u6682\u505c' in labels and any(h.normalized(t).startswith('fastforwarded13day') for t in labels)
assert matched(labels)
eb=(user/'logs/error.log').read_bytes();assert eb==(run/(original+'-error-before.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()
f=r.gpu_capture(after+'-existing-command-receipt');labels=[x['text'] for x in f['rows']];assert matched(labels)
(run/(after+'-error-before.log')).write_bytes(eb)
h.write_json(run/(after+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED_EXISTING_COMMAND_AFTER_TARGET_FAILURE','start_date':b['date'],'date':date,'days':13,'original_expected_date':'2236.06.01','original_failure_execution':original_execution.name,'original_failure_execution_sha256':h.sha256(original_execution),'unique_submitted_action_sha256':h.sha256(run/(original+'-native-days.action.json')),'image_sha256':f['image_sha256'],'original_polls':[{'file':p.name,'sha256':h.sha256(p)} for p in polls],'scope':'Independent observation of already executed command only. Original expected-date failure preserved; no second calendar input.'})
h.press_scan_code(0x29,after+'-close-existing-console',1);a=r.native_save(after,date,(0,));ea=(user/'logs/error.log').read_bytes();(run/(after+'-error-after.log')).write_bytes(ea)
p={'status':'OBSERVED_EXISTING_NATIVE_CALENDAR_AFTER_TARGET_FAILURE','date':a['date'],'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'original_failed_stage':original,'original_returncode':exe['returncode'],'new_error_bytes':len(ea)-len(eb),'scope':'Normal native save and receipt recovery only, no new calendar command. Independent economy/construction/state guard still required.'}
h.write_json(run/(after+'-recovery-observation.json'),p);print(json.dumps(p),flush=True)
