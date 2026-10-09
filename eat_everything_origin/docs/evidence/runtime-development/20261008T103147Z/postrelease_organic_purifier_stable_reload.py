import json,logging,shutil,sys
from pathlib import Path
start,stage,alias=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['role']=='Post-release organic Fanatic Purifier natural continuation'
dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(Path(__file__),dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
p=user/'save games/acceptance-fixtures'/(alias+'.sav');assert not p.exists();shutil.copyfile(run/(start+'.sav'),p);assert h.sha256(p)==b['save_sha256']
r.native_load(alias,stage+'-load');a=r.native_save(stage,b['date'],(0,));bc=b['countries']['0'];ac=a['countries']['0']
checks={'original_bytes_loaded':h.sha256(p)==b['save_sha256'],'same_date':a['date']==b['date'],'all_stock_same':bc['stockpile']==ac['stockpile'],'all_EEP_variables_same':bc['variables']==ac['variables'],'all_EEP_flags_same':bc['flags']==ac['flags'],'all_tech_same':bc['completed_technologies']==ac['completed_technologies'],'all_research_queues_same':bc['research_queues']==ac['research_queues'],'all_traditions_same':bc['traditions']==ac['traditions'],'all_AP_same':bc['ascension_perks']==ac['ascension_perks'],'one_actual_core':sum(d.get('type')=='d_eep_core' for d in a['deposits'].values())==1}
for key in ['pop_groups','pop_jobs','colonies','planets','deposits','districts','species','situations','event_targets']:checks[key+'_same']=a[key]==b[key]
ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea);checks['no_new_errors']=ea==eb
changes={key:{'before':b[key],'after':a[key]} for key in ['pop_groups','pop_jobs','colonies','planets','deposits','districts','species','situations','event_targets'] if a[key]!=b[key]}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'alias_sha256':h.sha256(p),'after_sha256':a['save_sha256'],'new_error_bytes':len(ea)-len(eb),'collection_changes':changes,'scope':'Strict original-byte native reload of inherited natural organic Purifier state under published production; no full civic/ascension/crisis acceptance claim.'}
h.write_json(run/(stage+'-proof.json'),proof);print(json.dumps({k:v for k,v in proof.items() if k!='collection_changes'}),flush=True);assert all(checks.values()),'Original native reload FAIL retained'
