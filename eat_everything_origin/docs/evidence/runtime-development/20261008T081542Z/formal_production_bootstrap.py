import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
for n in range(12):
 try:f=r.gpu_capture('formal-prod-title-ready-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('formal-prod-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'formal-prod-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN main menu')
loaded=r.native_load('prod-clean-start','formal-prod-original-clean-load');assert loaded['source_sha256']==m['original_seed']['sha256'];a=r.native_save('formal-prod-initial','2200.01.01',(0,));v=a['countries']['0']['variables'];assert a['countries']['0']['ascension_perks']==[] and all(v[k]==z for k,z in {'eep_c':0,'eep_g':0,'eep_d':2,'eep_made':0,'eep_worlds':0}.items());assert sum(a['colonies'][str(i)]['actual_pop_sum'] for i in a['countries']['0']['owned_colonies'])==5300
h.write_json(run/'formal-prod-initial-clean-identity.json',{'status':'PASS_SCOPED','save_sha256':a['save_sha256'],'legal_focus_government':a['countries']['0']['government'],'variables':v,'population':5300,'AP':[],'production_tree_sha256':m['copied_mod_tree_sha256']});print(json.dumps({'status':'PASS_SCOPED','date':a['date'],'sha256':a['save_sha256'],'population':5300}),flush=True)
