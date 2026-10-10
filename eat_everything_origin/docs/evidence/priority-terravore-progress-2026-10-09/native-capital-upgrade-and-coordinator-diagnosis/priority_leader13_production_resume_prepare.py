"""Restore exact production pointer/package after native leader diagnostic."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris();control,cu,cm=h.load_run();assert cm['enabled_mods']==[]
p=json.loads((control/'leader13-control-fleet-error-reproduction-proof.json').read_text('utf-8'));assert p['status']=='PASS_SCOPED_NO_MOD_LEADER13_ERROR_REPRODUCTION' and all(p['checks'].values())
shutil.copytree(cu/'logs',control/'logs-final-after-normal-exit');h.write_json(control/'normal-control-exit.json',{'status':'OBSERVED_NORMAL_GUI_EXIT','pid':h.process_record(control)['pid'],'forced':False,'running_after':False})
backup=Path('_runtime/heart-of-devouring/priority-leader13-production-pointer.json');ptr=json.loads(backup.read_text('utf-8'));prod=Path(ptr['artifact_dir']);shutil.copyfile(h.CURRENT_RUN,prod/'leader13-control-pointer.json');h.CURRENT_RUN.write_bytes(backup.read_bytes());run,user,m=h.load_run()
assert run==prod and m['version']=='0.2.0' and m['enabled_mods']==['mod/ugc_eep-local.mod'];assert json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':m['enabled_mods'],'disabled_dlcs':[]}
tree=h.tree_manifest(h.MOD_ROOT)[1];assert tree=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7';source=run/'terravore-defense-post-battle-repair-month.sav';assert h.sha256(source)=='d2daf0d4bc7cfd690abb5c573f657a7bd97121d4babaf7b703d3beeef7d69c6f'
shutil.copyfile(run/'process.json',run/'process-before-leader13-control.json');shutil.copyfile(__file__,run/Path(__file__).name)
h.write_json(run/'leader13-production-resume-preflight.json',{'status':'PASS_PRODUCTION_RESUME_PACKAGE_ONLY','tree_sha256':tree,'source_sha256':h.sha256(source),'control_run':str(control),'scope':'Original production pointer, package and SAV inputs held. No control save imported. Native production reload proof pending.'});print(json.dumps(h.launch(60,False)),flush=True)
