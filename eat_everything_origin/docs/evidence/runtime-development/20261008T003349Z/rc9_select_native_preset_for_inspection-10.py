import json,logging,shutil,sys
from pathlib import Path
number=sys.argv[1];assert number in ['06','07','10']
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();dest=run/(Path(__file__).stem+'-'+number+'.py')
assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-native-preset-'+number
for i in range(6):
    f=r.gpu_capture(stem+'-selection-page-'+str(i))
    assert any(x['text']=='\u9009\u62e9\u5e1d\u56fd' and x['score']>=.8 for x in f['rows'])
    choices=[x for x in f['rows'] if max(p[0] for p in x['box'])<220 and x['score']>=.8 and h.normalized('EEP '+number) in h.normalized(x['text'])]
    if len(choices)==1:
        row=choices[0];r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),stem+'-row-click')
        f=r.gpu_capture(stem+'-selected');print(json.dumps({'image':f['image'],'rows':[x['text'] for x in f['rows']]},ensure_ascii=False),flush=True)
        break
    assert not choices,choices
    r.gpu_scroll(-3,130,520,stem+'-selection-scroll-'+str(i),80)
else:raise RuntimeError('requested native preset not found')
