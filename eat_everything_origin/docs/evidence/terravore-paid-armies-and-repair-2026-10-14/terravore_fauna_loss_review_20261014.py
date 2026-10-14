import json,logging,sys
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
p=json.loads((run/'hope-route-fauna-sep08-native-22940908-fauna-proof.json').read_text('utf-8'))
ui=json.loads((run/'hope-route-sep08-retreat-tooltip.ocr.json').read_text('utf-8'))
assert p['pass'] and p['boundaries']==['actual_own_ship_loss'] and p['own_lost']==['16779175']
assert p['enemy_destroyed']==['299','337','340','349','360','441'] and p['menace']==3515
assert ui['image_sha256']=='55d2aa239261ae09fd04d1cd6a750e0f73cad9e6ee74cf1be03ff053f57ec2d1' and h.sha256(run/'hope-route-sep08-retreat-tooltip.jpg')==ui['image_sha256']
assert any('还需3天' in x['text'] for x in ui['rows'])
assert h.sha256(run/'hope-route-fauna-sep08-native-22940908.sav')==p['after_save_sha256']
assert (run/'hope-route-fauna-sep08-native-22940908-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes()
out=run/'hope-route-fauna-sep08-loss-reviewed-proof.json';assert not out.exists()
h.write_json(out,{'pass':True,'checks':{'real_loss_and_menace_reviewed':True,'native_retreat_requires3days':True},'after_save_sha256':p['after_save_sha256'],'calendar_ready':True,'maximum_days':3,'scope':'Only09.08 to09.11 to normal retreat availability; one actual loss preserved, no asset or resource grants.'})
print(json.dumps({'pass':True,'calendar_ready':True,'maximum_days':3}),flush=True)
