import json,logging,sys
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
stage='hope-route-aug01-salietto-orders-native-22940801'
assert not list(run.glob(stage+'*'))
a=read_state(run,'hope-route-wait-native-22940801')
prior=json.loads((run/'hope-route-wait-native-22940801-wait-v2-proof.json').read_text('utf-8'))
assert prior['pass'] and prior['boundaries']==['new_native_messages']
assert sorted(x['target_fleet'] for x in prior['new_messages'])==[917,50332250] and all(x['type']=='FLEET_REPARATIONS_DONE_MESSAGE_TYPE' for x in prior['new_messages'])
assert h.sha256(run/'hope-route-wait-native-22940801.sav')==a['audit']['save_sha256']==prior['after_save_sha256']
error=(user/'logs/error.log').read_bytes()
assert error==(run/'hope-route-wait-native-22940801-error-after.log').read_bytes()
frame=r.gpu_capture(stage+'-pre')
labels=[x['text'] for x in frame['rows']]
assert all(x in labels for x in ['2294.08.01','暂停','搜索已知恒星系','萨列托'])
(run/(stage+'-error-before.log')).write_bytes(error)
r.gpu_click(778,101,stage+'-close-search')
for number,y in [(2,368),(3,276)]:
 r.gpu_click(883,y,stage+'-select-'+str(number))
 frame=r.gpu_capture(stage+'-selected-'+str(number))
 assert any(x['text']=='第'+str(number)+'舰队' and max(p[0] for p in x['box'])<450 for x in frame['rows'])
 h.pyautogui.click(*r.desktop_point(516,383),button='right')
 h.write_json(run/(stage+'-order-'+str(number)+'.action.json'),{'action':'native_right_click','client_point':[516,383],'selected_fleet_number':number,'target_system_label':'萨列托','date':'2294.08.01'})
 frame=r.gpu_capture(stage+'-ordered-'+str(number))
 print(json.dumps({'fleet':number,'labels':[x['text'] for x in frame['rows']]},ensure_ascii=False),flush=True)
saved=r.native_save(stage,'2294.08.01',(0,1,15))
after=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(after)
assert after==error
print(json.dumps({'date':saved['date'],'save_sha256':saved['save_sha256']}),flush=True)
