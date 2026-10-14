"""Normal Chinese search camera only; no orders/calendar or clipboard."""
import json,logging,subprocess,sys,time
stage,date,*points=sys.argv[1:]
name=''.join(chr(int(p,16)) for p in points)
assert name and len(name)<=20
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
assert not list(run.glob(stage+'*')) and meta['language']=='l_simp_chinese'
error=(user/'logs/error.log').read_bytes()
frame=r.gpu_capture(stage+'-pre')
assert date in [x['text'] for x in frame['rows']] and '暂停' in [x['text'] for x in frame['rows']]
def click(x,y,label):
 h.pyautogui.moveTo(*r.desktop_point(x,y),duration=.1);time.sleep(.25)
 h.pyautogui.mouseDown(button='left')
 try:time.sleep(.15)
 finally:h.pyautogui.mouseUp(button='left')
 h.write_json(run/(stage+'-'+label+'.action.json'),{'action':'normal_held_left_click','client_point':[x,y],'hold_seconds':.15,'pre_dwell_seconds':.25})
h.press_scan_code(0x21,stage+'-open-F',1)
frame=r.gpu_capture(stage+'-search')
assert '搜索已知恒星系' in [x['text'] for x in frame['rows']]
click(670,141,'edit');h.press_scan_code(0x0e,stage+'-clear',30)
result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/record_current_helper.py',stage+'-unicode-exec','_runtime/heart-of-devouring/priority_native_ui_input_v3.py','unicode',stage+'-unicode',*points],capture_output=True)
assert result.returncode==0,result.stderr.decode('utf-8',errors='replace')
frame=r.gpu_capture(stage+'-results')
rows=[x for x in frame['rows'] if x['text']==name and min(p[0] for p in x['box'])>=580 and 154<min(p[1] for p in x['box'])<330]
assert len(rows)==1,'No unique native Chinese search candidate; no camera click'
row=rows[0];click(round(sum(p[0] for p in row['box'])/4),round(sum(p[1] for p in row['box'])/4),'locate')
click(778,101,'close-search')
frame=r.gpu_capture(stage+'-located')
assert error==(user/'logs/error.log').read_bytes()
h.write_json(run/(stage+'-navigation.json'),{'name':name,'date':date,'image_sha256':frame['image_sha256'],'scope':'Native search and camera only; no fleet order, payment or calendar.'})
print(json.dumps({'name':name,'date':date,'image_sha256':frame['image_sha256'],'labels':[x['text'] for x in frame['rows']]},ensure_ascii=False),flush=True)
