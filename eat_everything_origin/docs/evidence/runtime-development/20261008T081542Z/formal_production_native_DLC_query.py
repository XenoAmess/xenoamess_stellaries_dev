import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
eb=(user/'logs/game.log').read_bytes();(run/'formal-prod-dlc-query-before.log').write_bytes(eb);h.press_scan_code(0x29,'formal-prod-dlc-console-open',1)
cmd='effect root = { if = { limit = { host_has_dlc = "Nemesis" } log = "EEP_PROD_DLC Nemesis=YES" } else = { log = "EEP_PROD_DLC Nemesis=NO" } if = { limit = { host_has_dlc = "Shadows of the Shroud" } log = "EEP_PROD_DLC Shroud=YES" } else = { log = "EEP_PROD_DLC Shroud=NO" } }'
h.type_text(cmd,True,'formal-prod-native-dlc-query');f=r.gpu_capture('formal-prod-native-dlc-query-receipt');h.press_scan_code(0x29,'formal-prod-dlc-console-close',1)
ea=(user/'logs/game.log').read_bytes();(run/'formal-prod-dlc-query-after.log').write_bytes(ea);assert ea.startswith(eb);delta=ea[len(eb):].decode('utf-8-sig');assert all(x in delta for x in ['EEP_PROD_DLC Nemesis=YES','EEP_PROD_DLC Shroud=YES']),delta
h.write_json(run/'formal-prod-native-DLC-proof.json',{'status':'PASS','actual_native_delta':delta,'config_sha256':h.sha256(user/'dlc_load.json'),'production_tree':m['copied_mod_tree_sha256'],'scope':'Actual native host_has_dlc only, builtin conditional log; no test events loaded or grants.'});print(json.dumps({'status':'PASS','actual_DLC':['Nemesis=YES','Shroud=YES']}),flush=True)
