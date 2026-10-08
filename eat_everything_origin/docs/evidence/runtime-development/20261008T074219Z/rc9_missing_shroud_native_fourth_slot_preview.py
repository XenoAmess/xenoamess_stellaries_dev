import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['dlc_variant']=='shroud';dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest);stem='rc9-missing-shroud-native-fourth-slot'
r.gpu_click(730,185,stem+'-close-first-preview');r.gpu_click(907,341,stem+'-locked-fourth-preview');r.gpu_capture(stem+'-before-top');r.gpu_scroll(1,541,471,stem+'-reset-top',500)
for n in range(3):
 h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(.5);f=r.gpu_capture(stem+'-top-'+str(n));print(json.dumps({'image':f['image'],'rows':[x['text'] for x in f['rows'] if min(p[0] for p in x['box'])>370 and max(p[0] for p in x['box'])<728 and min(p[1] for p in x['box'])>217 and max(p[1] for p in x['box'])<550]},ensure_ascii=False),flush=True)
 if n<2:r.gpu_scroll(-1,541,471,stem+'-scroll-'+str(n),10)
