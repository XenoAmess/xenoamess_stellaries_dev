import json,logging,sys
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
stage='hope-route-mar22-recruit8-native-22940322'
a=read_state(run,'hope-route-mar22-return2-native-22940322')
prior=json.loads((run/'hope-route-mar22-return-guard-22940322-proof.json').read_text('utf-8'))
quote=json.loads((run/'hope-route-mar22-assault-tooltip-after.ocr.json').read_text('utf-8'))
assert prior['pass'] and prior['after_save_sha256']==a['audit']['save_sha256']
assert quote['image_sha256']=='226adaf73dd0c7f99849e8be78b6724102ed982c51a2b311abbecb2ac8d2bac1'
assert a['audit']['countries']['0']['effective_stockpile']['minerals']>800
assert not list(run.glob(stage+'*'))
error=(user/'logs/error.log').read_bytes()
assert error==(run/'hope-route-mar22-return2-native-22940322-error-after.log').read_bytes()
frame=r.gpu_capture(stage+'-pre')
labels=[x['text'] for x in frame['rows']]
assert all(x in labels for x in ['2294.03.22','暂停','EEP-Core','招募','进攻部队：0'])
assert h.tree_manifest(r.ROOT/'mod')[1]==meta['repository_mod_tree_sha256']
(run/(stage+'-error-before.log')).write_bytes(error)
for n in range(8):
 r.gpu_click(574,327,stage+'-recruit-'+str(n+1))
frame=r.gpu_capture(stage+'-queued')
h.write_json(run/(stage+'-action-proof.json'),{'quote_sha256':quote['image_sha256'],'recruit_clicks':8,'queued_ui_sha256':frame['image_sha256']})
saved=r.native_save(stage,'2294.03.22',(0,1,15))
after=(user/'logs/error.log').read_bytes()
(run/(stage+'-error-after.log')).write_bytes(after)
assert after==error
print(json.dumps({'save_sha256':saved['save_sha256'],'date':saved['date']}),flush=True)
