import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
proof=json.loads((run/'hope-route-wait-native-22940701-wait-v2-proof.json').read_text('utf-8'))
execution=json.loads((run/'hope-route-wait-native-22940701-guard-v2-execution.json').read_text('utf-8'))
ui=json.loads((run/'hope-route-jul01-select-transport-after.ocr.json').read_text('utf-8'))
labels=[x['text'] for x in ui['rows']]
assert proof['pass'] and proof['boundaries']==['paid_army_birth_needs_UI_review']
assert execution['returncode']==0 and h.sha256(Path(execution['command'][1]))==execution['helper_sha256']
assert h.sha256(run/'hope-route-wait-native-22940701.sav')==proof['after_save_sha256']
assert ui['image_sha256']=='ef90f4fdf666ab1f7e0d45e1abb23147c605e2fe1dc8d0cd7247899d0db8478d'
assert all(x in labels for x in ['2294.07.01','暂停','第2运输舰队','有1支陆军位于此处。','运输舰EEP1远征部队'])
assert h.sha256(run/'hope-route-jul01-select-transport-after.jpg')==ui['image_sha256']
assert (run/'hope-route-wait-native-22940701-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes()
out=run/'hope-route-jul01-birth-reviewed-proof.json';assert not out.exists()
h.write_json(out,{'pass':True,'checks':{'native_v2_guard_and_UI_bound':True,'first_paid_army_visible':True},'after_save_sha256':proof['after_save_sha256'],'calendar_ready':True,'reviewed_boundary':'first_paid_army','guard': 'hope-route-wait-native-22940701-wait-v2-proof.json','UI_sha256':ui['image_sha256']})
print(json.dumps({'pass':True,'calendar_ready':True,'after_save_sha256':proof['after_save_sha256']}),flush=True)
