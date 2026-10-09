"""No-mod isolated native preFTL event reproduction from an original-byte world."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris()
prod,pu,pm=h.load_run();pointer=h.CURRENT_RUN.read_bytes();backup=Path('_runtime/heart-of-devouring/priority-preftl-production-pointer.json');assert not backup.exists();backup.write_bytes(pointer)
source=prod/'terravore-second-postsettlement-month.sav';assert h.sha256(source)=='58a0eb48e92ec37286fa4084d8b33a4f98de1de4bcfbf4f5e0bc4eaa4d9e682e'
logs=prod/'logs-before-preftl-control';assert not logs.exists();shutil.copytree(pu/'logs',logs)
h.write_json(prod/'preftl-control-production-normal-exit.json',{'status':'OBSERVED_NORMAL_GUI_EXIT','pid':23824,'forced':False,'running_after':False,'method':'Actual exit-to-desktop menu and confirmation, no termination command','resume_save':'terravore-second-psionic-wait-year1.sav','resume_sha256':'4e5cbaa57e7f166803e83ab143f0a85a68be3d75b8fccf8683fcf9f2fa426bed','pointer_sha256':h.sha256(backup)})
d=h.prepare('l_simp_chinese',[]);run=Path(d['artifact_dir']);user=Path(d['userdir']);shutil.copyfile(Path(__file__),run/Path(__file__).name)
alias=user/'save games/acceptance-fixtures/preftl-source.sav';alias.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,alias);assert h.sha256(alias)==h.sha256(source)
d.update(version='0.2.0',role='No-mod isolated preftl.199 event error reproduction',scope='Original-byte Mod-derived world with actual enabled_mods empty; missing EEP load errors are baseline. Only native country29 event reproduction, no Mod acceptance or clean vanilla-origin world claim.',original_seed={'path':str(source.resolve()),'sha256':h.sha256(source),'alias':str(alias)},production_pointer_backup=str(backup.resolve()))
h.write_json(run/'manifest.json',d);actual=json.loads((user/'dlc_load.json').read_text('utf-8'));assert actual=={'enabled_mods':[],'disabled_dlcs':[]}
h.write_json(run/'preftl-no-mod-isolation-preflight.json',{'status':'PASS_ISOLATION_ONLY','actual_enabled_mods':[],'disabled_dlcs':[],'seed_sha256':h.sha256(alias),'production_pointer_backup':str(backup.resolve()),'scope':d['scope']})
print(json.dumps({'run_id':run.name,'actual_enabled_mods':[],'source_sha256':h.sha256(alias)}),flush=True);print(json.dumps(h.launch(60,False)),flush=True)
