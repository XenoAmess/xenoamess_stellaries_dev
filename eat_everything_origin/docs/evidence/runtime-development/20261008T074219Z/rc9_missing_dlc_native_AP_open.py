import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest);stem='rc9-missing-'+variant+'-native-AP'
options=['\u4f59\u70ec\u5f52\u4e8e\u541e\u566c\u4e4b\u5fc3','\u738b\u5ea7\u4e4b\u5916\uff0c\u7686\u53ef\u541e\u566c']
for n in range(2):
 f=r.gpu_capture(stem+'-queen-before-ack-'+str(n));rows=[x for x in f['rows'] if any(h.normalized(x['text'])==h.normalized(o) for o in options) and min(p[1] for p in x['box'])>500];assert len(rows)==1,[(x['text'],x['box']) for x in f['rows']]
 row=rows[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),stem+'-queen-normal-ack-'+str(n));time.sleep(.5)
h.press_scan_code(0x3d,stem+'-F3-native-society',1);f=r.gpu_capture(stem+'-traditions-before-preview');assert any(x['text']=='\u4f20\u7edf' for x in f['rows'])
r.gpu_click(775,341,stem+'-locked-slot-preview');f=r.gpu_capture(stem+'-native-preview-before-unavailable');assert any('\u663e\u793a\u4e0d\u53ef\u7528' in x['text'] for x in f['rows'])
r.gpu_click(596,198,stem+'-show-unavailable-check');h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(.5);f=r.gpu_capture(stem+'-unavailable-inclusive-preview');print(json.dumps({'image':f['image'],'rows':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
