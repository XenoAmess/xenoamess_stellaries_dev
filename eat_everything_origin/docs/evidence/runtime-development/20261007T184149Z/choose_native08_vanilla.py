import json
import logging
import sys

sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--vanilla']
import runtime as r
logging.disable(logging.INFO)
for i in range(5):
    frame=r.gpu_capture('vanilla-shared-world-select-native08-page-'+str(i))
    if not any(x['text']=='选择帝国' and x['score']>=.8 for x in frame['rows']):
        raise RuntimeError('native empire selection window not verified')
    choices=[x for x in frame['rows'] if max(p[0] for p in x['box'])<220
             and x['score']>=.8 and r.harness.normalized('EEP 08') in r.harness.normalized(x['text'])]
    if len(choices)==1:
        row=choices[0]
        r.gpu_click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),
                    'vanilla-shared-world-native08-row-click')
        frame=r.gpu_capture('vanilla-shared-world-native08-selected-inspection')
        print(json.dumps({'image':frame['image'],'rows':[x['text'] for x in frame['rows']]},ensure_ascii=False))
        break
    if choices:
        raise RuntimeError('native08 row is ambiguous')
    r.gpu_scroll(-3,130,520,'vanilla-shared-world-select-native08-scroll-'+str(i),80)
else:
    raise RuntimeError('native08 not visible after bounded scrolling')
