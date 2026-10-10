"""Native CN title wait then existing strict reload of preserved production SAV."""
import json,logging,shutil,subprocess,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==['mod/ugc_eep-local.mod'];shutil.copyfile(__file__,run/Path(__file__).name)
for n in range(15):
 try:f=r.gpu_capture('coordinator-production-title-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('coordinator-production-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'coordinator-production-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN production menu')
p=subprocess.run([sys.executable,'_runtime/heart-of-devouring/priority_native_checkpoint_reload.py','terravore-ascension-capital-paid','terravore-ascension-capital-resumed','coordinator-resume-source'],capture_output=True)
print(p.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(p.stderr.decode('utf-8',errors='replace'),end='',flush=True);sys.exit(p.returncode)
