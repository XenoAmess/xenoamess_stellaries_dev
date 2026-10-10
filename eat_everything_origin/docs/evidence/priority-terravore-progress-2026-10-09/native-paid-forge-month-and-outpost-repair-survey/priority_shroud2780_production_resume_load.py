"""Native CN title wait then existing strict reload of preserved production SAV."""
import json,logging,shutil,subprocess,sys,time,pywintypes
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==['mod/ugc_eep-local.mod'];shutil.copyfile(__file__,run/Path(__file__).name)
for n in range(15):
 try:f=r.gpu_capture('shroud2780-production-title-'+str(n))
 except (RuntimeError,pywintypes.error) as e:
  if not ('did not produce a fresh GPU screenshot' in str(e) or (isinstance(e,pywintypes.error) and len(e.args)>1 and e.args[1]=='SetForegroundWindow')):raise
  h.write_json(run/('shroud2780-production-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'shroud2780-production-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN production menu')
p=subprocess.run([sys.executable,'_runtime/heart-of-devouring/priority_native_checkpoint_reload.py','terravore-native-stage3-ack','terravore-native-stage3-resumed','shroud2780-resume-source'],capture_output=True)
print(p.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(p.stderr.decode('utf-8',errors='replace'),end='',flush=True);sys.exit(p.returncode)
