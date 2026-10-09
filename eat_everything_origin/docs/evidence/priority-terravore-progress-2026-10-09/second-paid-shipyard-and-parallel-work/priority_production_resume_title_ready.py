"""Wait for actual native Chinese production menu after restart; no load or grants."""
import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==['mod/ugc_eep-local.mod'];shutil.copyfile(Path(__file__),run/Path(__file__).name)
for n in range(12):
 try:f=r.gpu_capture('production-resume-title-'+str(n))
 except RuntimeError as e:
  if 'did not produce a fresh GPU screenshot' not in str(e):raise
  h.write_json(run/('production-resume-title-no-frame-'+str(n)+'.json'),{'status':'NO_FRAME_NOT_READY','error':str(e)});time.sleep(10);continue
 rows=[x for x in f['rows'] if x['text']=='\u5173\u95ed' and x['score']>.8]
 if len(rows)==1:
  row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'production-resume-close-welcome');break
 if any(x['text']=='\u8f7d\u5165\u6e38\u620f' for x in f['rows']):break
 time.sleep(10)
else:raise RuntimeError('No native CN production main menu')
h.write_json(run/'production-resume-title-ready.json',{'status':'READY_NATIVE_CN_MENU_ONLY','image_sha256':f['image_sha256'],'scope':'Actual load menu ready, no state verification or load yet.'});print('Actual native Chinese production menu ready',flush=True)
