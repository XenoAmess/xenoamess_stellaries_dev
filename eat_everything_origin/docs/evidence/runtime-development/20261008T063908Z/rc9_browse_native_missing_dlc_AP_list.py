import json,logging,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
stem='rc9-missing-'+variant+'-native-AP-full-list'
target='\u661f\u6d77\u5929\u7f5a' if variant=='nemesis' else '\u5fc3\u80dc\u4e8e\u7269'
pages=[];previous=None;repeats=0;seen=[];found=[]
for n in range(35):
    h.pyautogui.moveTo(*r.desktop_point(20,740),duration=.2);time.sleep(.5)
    f=r.gpu_capture(stem+'-page-'+str(n))
    rows=[x for x in f['rows'] if min(p[0] for p in x['box'])>370 and max(p[0] for p in x['box'])<728 and min(p[1] for p in x['box'])>217 and max(p[1] for p in x['box'])<550]
    content=[x['text'] for x in rows];assert content
    pages.append({'image':Path(f['image']).name,'sha256':f['image_sha256'],'content':content});seen.extend(content)
    for row in rows:
        if target in row['text']:
            x=round(sum(p[0] for p in row['box'])/4);y=round(sum(p[1] for p in row['box'])/4)
            h.pyautogui.moveTo(*r.desktop_point(x,y),duration=.2);time.sleep(1.5)
            tip=r.gpu_capture(stem+'-target-tooltip-'+str(n));found.append({'page':n,'image':Path(tip['image']).name,'sha256':tip['image_sha256'],'rows':[x['text'] for x in tip['rows']]})
    repeats=repeats+1 if content==previous else 0;previous=content
    print(json.dumps({'page':n,'target_seen':any(target in x for x in content),'end_repeats':repeats}),flush=True)
    if repeats>=2:break
    r.gpu_scroll(-1,541,471,stem+'-scroll-'+str(n),1)
else:raise RuntimeError('native AP list bottom not established by repeated bounded content')
v={'status':'OBSERVED_COMPLETE_NATIVE_LIST','variant':variant,'target':target,'target_present':bool(found),'pages':pages,'target_tooltips':found,'all_UI_content':seen,'bottom_repeats':repeats,'scope':'Actual Simplified Chinese unavailable-inclusive AP preview. No resource/AP/technology/tradition grants or purchases; final missing-DLC gate status follows actual visibility/tooltips.'}
h.write_json(run/(stem+'-observation.json'),v);print(json.dumps({'status':v['status'],'target_present':v['target_present'],'pages':len(pages),'tooltips':len(found)}),flush=True)
