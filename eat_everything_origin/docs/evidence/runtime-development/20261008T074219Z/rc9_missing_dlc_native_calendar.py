import json,logging,shutil,sys,time,zipfile
from datetime import datetime,timezone
from pathlib import Path
start,end,stage,raw_days=sys.argv[1:];days=int(raw_days);assert 1<=days<=360
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();assert m['dlc_variant'] in ['nemesis','shroud']
dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(Path(__file__),dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'))
eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stage+'-console-open',1);h.type_text('fast_forward '+str(days),True,stage+'-native-calendar-command')
for n in range(24):
    if n:time.sleep(10)
    f=r.gpu_capture(stage+'-calendar-poll-'+str(n));labels=[x['text'] for x in f['rows']]
    complete=end in labels and '\u6682\u505c' in labels and any(h.normalized(t) in {'fastforwarded'+str(days)+'days','fastforwarded'+str(days)+'d'} for t in labels)
    print(json.dumps({'poll':n,'date_seen':end in labels,'receipt_complete':complete}),flush=True)
    if complete:
        h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','start_date':b['date'],'date':end,'days':days,'frame_sha256':f['image_sha256'],'at_utc':datetime.now(timezone.utc).isoformat()});break
else:raise RuntimeError('Native date, paused state and correct completed days not confirmed')
h.press_scan_code(0x29,stage+'-console-close',1)
a=r.native_save(stage,end,(0,))
targets=[x for x in a['event_targets'] if x.get('name')=='eep_missing_dlc_source'];assert len(targets)==1
source=a['planets'].get(str(targets[0]['id']),{})
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
v={'status':'OBSERVED_NATIVE_CALENDAR','variant':m['dlc_variant'],'save_sha256':a['save_sha256'],'date':a['date'],
 'root_variables_before':b['countries']['0']['variables'],'root_variables_after':a['countries']['0']['variables'],
 'root_flags_after':a['countries']['0']['flags'],'source_world':source,
 'source_population':a['colonies'].get(str(source.get('colony')),{}).get('actual_pop_sum',0),
 'root_population':sum(a['colonies'].get(str(i),{}).get('actual_pop_sum',0) for i in a['countries']['0']['owned_colonies']),
 'AP_before':b['countries']['0']['ascension_perks'],'AP_after':a['countries']['0']['ascension_perks'],
 'stock_before':b['countries']['0']['stockpile'],'stock_after':a['countries']['0']['stockpile'],
 'new_error_bytes':len(ea)-len(eb),'scope':'Actual native days and production monthly progression only; no forced EEP completion, technology/AP/crisis stage grants.'}
h.write_json(run/(stage+'-state.json'),v)
print(json.dumps({k:z for k,z in v.items() if not k.startswith('stock_')}),flush=True)
