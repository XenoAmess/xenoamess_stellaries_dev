import json, logging, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[]
shutil.copyfile(Path(__file__),run/Path(__file__).name)
stage='postvanilla-q20-m096';assert not (run/(stage+'.sav')).exists()
f=r.gpu_capture(stage+'-retry-actual-dialog');rows=[x for x in f['rows'] if x['text']=='\u4fdd\u5b58' and x['score']>=.8];assert len(rows)==1
assert any(x['text']==stage for x in f['rows'])
row=rows[0];h.click_point(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),stage+'-retry-native-save')
for i in range(20):
 paths=list((user/'save games').rglob(stage+'.sav'))
 if paths:break
 time.sleep(1)
else:raise RuntimeError('Native retry still has no saved file')
assert len(paths)==1;time.sleep(1);src=paths[0];shutil.copyfile(src,run/(stage+'.sav'));a=q.audit(run/(stage+'.sav'),(0,));assert a['date']=='2208.01.02';h.write_json(run/(stage+'.audit.json'),a)
dest=user/'save games/eep-test-history'/src.name;assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);src.replace(dest);assert h.sha256(dest)==a['save_sha256']
h.write_json(run/(stage+'.native-save.json'),{'written_at':str(src),'history':str(dest),'archived':str(run/(stage+'.sav')),'sha256':a['save_sha256'],'date':a['date'],'retry':True})
h.press_scan_code(0x01,stage+'-retry-close-menu',1)
ea=(user/'logs/error.log').read_bytes();eb=(run/(stage+'-error-before.log')).read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
p=a['planets']['1641'];tasks=[s for s in a['situations'].values() if s.get('type')=='situation_terravore_consume_planet' and s.get('country')==0 and s.get('killed')!='yes'];c=a['countries']['0']
checks={'actual_date':a['date']=='2208.01.02','no_EEP_variables':c['variables']=={},'no_EEP_flags':c['flags']=={},'AP_empty':c['ascension_perks']==[],'no_EEP_core_deposit':not any(d.get('type')=='d_eep_core' for d in a['deposits'].values()),'new_error_zero':eb==ea,'original_source_owned':p.get('owner')==0,'source_not_destroyed':p['planet_class']=='pc_continental','one_native_task':len(tasks)==1,'fixed_Q20':p['variables']['num_districts_terravore']==20,'actual_progress_observed':len(tasks)==1 and tasks[0]['progress']==816}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','effective_month':96,'date':a['date'],'checks':checks,'save_sha256':a['save_sha256'],'scope':'Native save retry at already advanced actual month 96; no second calendar advance, original UI failure retained.'};h.write_json(run/(stage+'-calendar-scope-proof.json'),v);print(json.dumps(v));assert all(checks.values())
