import json,logging,shutil,sys,time
from pathlib import Path
start,end,stage,raw_days=sys.argv[1:];days=int(raw_days);assert 1<=days<=360
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(Path(__file__),dest)
assert dest.read_bytes()==Path(__file__).read_bytes();b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stage+'-console-open',1);h.type_text('fast_forward '+str(days),True,stage+'-native-days')
for n in range(36):
 if n:time.sleep(10)
 f=r.gpu_capture(stage+'-calendar-poll-'+str(n));labels=[x['text'] for x in f['rows']];complete=end in labels and '\u6682\u505c' in labels and any(h.normalized(t).startswith('fastforwarded'+str(days)+'day') or h.normalized(t)=='fastforwarded'+str(days)+'d' for t in labels)
 print(json.dumps({'poll':n,'date_seen':end in labels,'receipt_complete':complete}),flush=True)
 if complete:
  h.write_json(run/(stage+'-calendar-receipt.json'),{'status':'CALENDAR_CONFIRMED','date':end,'start_date':b['date'],'days':days,'image_sha256':f['image_sha256'],'actual_receipt_labels':[t for t in labels if 'fastforward' in h.normalized(t)]});break
else:raise RuntimeError('Native calendar not confirmed')
h.press_scan_code(0x29,stage+'-console-close',1);a=r.native_save(stage,end,(0,));ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
proof=json.loads((run/'postvanilla-single-source-proof.json').read_text(encoding='utf-8'));pid=str(proof['source_physical']);from postrelease_vanilla_raw_source import inspect;raw=inspect(run/(stage+'.sav'));p=raw['source'];cid=str(p.get('colony'));tasks={k:s for k,s in a['situations'].items() if s.get('type')=='situation_terravore_consume_planet' and s.get('country')==0}
v={'status':'OBSERVED_NATIVE_NO_MOD_CALENDAR','date':a['date'],'save_sha256':a['save_sha256'],'source_physical':int(pid),'source_class':p['planet_class'],'source_variables':p['variables'],'source_flags':p['flags'],
 'source_population':a['colonies'].get(cid,{}).get('actual_pop_sum',0),'native_damage_blockers':sum(a['deposits'].get(str(i),{}).get('type')=='d_lithoid_devastation' for i in p['deposits']),
 'native_situations':tasks,'actual_root_stock':a['countries']['0']['stockpile'],'mother_population':a['colonies']['0']['actual_pop_sum'],'new_error_bytes':len(ea)-len(eb),'scope':'Actual native day/month progress in enabled_mods=[] process; observed native random effects, no forced progress, resource compensation or EEP scripts.'};h.write_json(run/(stage+'-state.json'),v);print(json.dumps(v),flush=True)
