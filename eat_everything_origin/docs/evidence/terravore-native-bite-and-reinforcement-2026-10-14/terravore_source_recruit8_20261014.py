"""One bounded normal source-colony recruitment, eight paid orders, no retry."""
import json,logging,sys,time
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
stage='hope-route-source-recruit8-native-22961201'
a=read_state(run,'hope-route-wait-native-22961201')
prior=json.loads((run/'hope-route-wait-native-22961201-digest-v5-proof.json').read_text('utf-8'))
quote=json.loads((run/'hope-route-dec96-source-army-quote.ocr.json').read_text('utf-8'))
assert prior['pass'] and prior['calendar_ready'] and prior['after_save_sha256']==a['audit']['save_sha256']
assert quote['image_sha256']==h.sha256(run/'hope-route-dec96-source-army-quote.jpg')=='7b12a8402d8b15b6f410155f144fb1b7948490ce817bff44bc1656f417eee677'
assert a['audit']['countries']['0']['effective_stockpile']['minerals']>1500 and not list(run.glob(stage+'*'))
error=(user/'logs/error.log').read_bytes()
assert error==(run/'hope-route-wait-native-22961201-error-after.log').read_bytes()
frame=r.gpu_capture(stage+'-pre')
labels=[row['text'] for row in frame['rows']]
assert all(any(text in label for label in labels) for text in ('2296.12.01','暂停','维米里恩','招募','进攻部队'))
assert h.tree_manifest(r.ROOT/'mod')[1]==meta['repository_mod_tree_sha256']
(run/(stage+'-error-before.log')).write_bytes(error)
for index in range(8):
 point=r.desktop_point(574,327)
 h.pyautogui.moveTo(*point,duration=.1);time.sleep(.25)
 h.pyautogui.mouseDown(button='left')
 try:time.sleep(.15)
 finally:h.pyautogui.mouseUp(button='left')
 h.write_json(run/(stage+'-recruit-'+str(index+1)+'.action.json'),{'action':'native_paid_recruit_click','client_point':[574,327],'hold_seconds':.15,'pre_dwell_seconds':.25})
frame=r.gpu_capture(stage+'-queued')
saved=r.native_save(stage,'2296.12.01',(0,1,15))
after=(user/'logs/error.log').read_bytes()
(run/(stage+'-error-after.log')).write_bytes(after)
assert after==error
print(json.dumps({'date':saved['date'],'save_sha256':saved['save_sha256'],'queued_UI_sha256':frame['image_sha256']}),flush=True)
