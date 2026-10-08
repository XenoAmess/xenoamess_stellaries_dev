import json,logging,shutil,sys,time
from pathlib import Path
number=sys.argv[1];assert number in ['07','10']
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();dest=run/(Path(__file__).stem+'-'+number+'.py')
assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-native-origin-refusal-'+number
for i in range(15):
    h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(1)
    f=r.gpu_capture(stem+'-list-'+str(i))
    choices=[x for x in f['rows'] if x['text']=='\u541e\u566c\u4e4b\u5fc3' and min(p[0] for p in x['box'])>210 and max(p[0] for p in x['box'])<710]
    if len(choices)==1:
        row=choices[0];x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4)
        h.pyautogui.moveTo(*r.desktop_point(x,y-40),duration=.2);time.sleep(1.5)
        r.gpu_capture(stem+'-native-requirement-tooltip')
        r.gpu_click(x,y-40,stem+'-actual-origin-card-attempt')
        h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(1)
        f=r.gpu_capture(stem+'-after-native-attempt')
        print(json.dumps({'image':f['image'],'rows':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
        break
    assert not choices,choices
    r.gpu_scroll(-3,470,525,stem+'-scroll-'+str(i),80)
else:raise RuntimeError('custom origin card not found in bounded native scrolling')
