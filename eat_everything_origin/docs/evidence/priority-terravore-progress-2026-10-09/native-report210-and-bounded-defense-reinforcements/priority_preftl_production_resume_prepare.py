"""Return to preserved production run after independent no-mod control; no save import."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris();control,cu,cm=h.load_run();assert cm['enabled_mods']==[]
pre=json.loads((control/'preftl-control-growth-pairs-supplement.json').read_text('utf-8'));assert pre['status']=='PASS_SCOPED_NO_MOD_PRE_FTL_REPRODUCTION_SUPPLEMENT' and all(pre['checks'].values())
shutil.copytree(cu/'logs',control/'logs-final-after-normal-exit')
h.write_json(control/'normal-control-exit.json',{'status':'OBSERVED_NORMAL_GUI_EXIT','pid':24792,'forced':False,'running_after':False,'method':'Actual native exit-to-desktop menu and confirmation, no termination command'})
backup=Path('_runtime/heart-of-devouring/priority-preftl-production-pointer.json');ptr=json.loads(backup.read_text('utf-8'));prod=Path(ptr['artifact_dir']);shutil.copyfile(h.CURRENT_RUN,prod/'preftl-control-pointer.json')
h.CURRENT_RUN.write_bytes(backup.read_bytes());run,user,m=h.load_run();assert run==prod and m['version']=='0.2.0' and m['enabled_mods']==['mod/ugc_eep-local.mod']
assert json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':['mod/ugc_eep-local.mod'],'disabled_dlcs':[]}
assert h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
assert h.sha256(run/'terravore-second-psionic-wait-year1.sav')=='4e5cbaa57e7f166803e83ab143f0a85a68be3d75b8fccf8683fcf9f2fa426bed'
shutil.copyfile(run/'process.json',run/'process-before-preftl-control.json');shutil.copyfile(Path(__file__),run/Path(__file__).name)
h.write_json(run/'preftl-production-resume-preflight.json',{'status':'PASS_PRODUCTION_RESUME_PACKAGE_ONLY','actual_enabled_mods':m['enabled_mods'],'production_tree_sha256':h.tree_manifest(h.MOD_ROOT)[1],'resume_source_sha256':h.sha256(run/'terravore-second-psionic-wait-year1.sav'),'control_run':str(control),'scope':'Original production pointer/package and original SAV restored as inputs, native load/reload proof still pending. No control save imported.'})
print(json.dumps(h.launch(60,False)),flush=True)
