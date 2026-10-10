"""Empty-mod source-byte native Shroud tooltip control, production preserved."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris()
prod,pu,pm=h.load_run();assert prod.name=='20261009T044016Z';backup=Path('_runtime/heart-of-devouring/priority-shroud2780-production-pointer.json');assert not backup.exists();backup.write_bytes(h.CURRENT_RUN.read_bytes())
source=prod/'terravore-native-stage3-pending.sav';sha='544e3f225293364c1335d633877f4fbe2622841974d6e2db566a8dd48121b873';assert h.sha256(source)==sha
resume=prod/'terravore-native-stage3-ack.sav';assert h.sha256(resume)=='4ee788da978bd7721c8f5f27fcdd1af1abd4266c0b8dbeb0854ef11f64bdadef'
assert all(json.loads((prod/('terravore-native2780-production-exit-'+st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['desktop','confirm'])
shutil.copytree(pu/'logs',prod/'logs-before-shroud2780-control');h.write_json(prod/'shroud2780-production-normal-exit.json',{'status':'OBSERVED_NORMAL_GUI_EXIT','pid':23712,'forced':False,'running_after':False,'resume_sha256':h.sha256(resume),'pointer_sha256':h.sha256(backup)})
d=h.prepare('l_simp_chinese',[]);run=Path(d['artifact_dir']);user=Path(d['userdir']);shutil.copyfile(__file__,run/Path(__file__).name)
alias=user/'save games/acceptance-fixtures/shroud2780-source.sav';alias.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,alias);assert h.sha256(alias)==sha
d.update(version='0.2.0',role='Isolated native shroud2780 option tooltip diagnosis',scope='Original-byte Mod-derived world, enabled_mods empty. Missing EEP definitions are separate load baseline; not pure vanilla-origin generation or Mod acceptance.',original_seed={'path':str(source.resolve()),'sha256':sha,'alias':str(alias)},production_pointer_backup=str(backup.resolve()))
h.write_json(run/'manifest.json',d);assert json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]}
h.write_json(prod/'shroud2780-control-pointer.json',{'artifact_dir':str(run),'userdir':str(user)})
h.write_json(run/'shroud2780-isolation-preflight.json',{'status':'PASS_ISOLATION_ONLY','seed_sha256':sha,'enabled_mods':[],'scope':d['scope']});print(json.dumps(h.launch(60,False)),flush=True)
