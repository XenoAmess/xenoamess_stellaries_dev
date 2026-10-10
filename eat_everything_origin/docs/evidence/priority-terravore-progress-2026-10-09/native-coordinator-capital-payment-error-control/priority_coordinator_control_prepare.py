"""Prepare empty-mod native capital-tooltip diagnosis, preserve production bytes."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris()
prod,pu,pm=h.load_run();backup=Path('_runtime/heart-of-devouring/priority-coordinator-production-pointer.json');assert not backup.exists();backup.write_bytes(h.CURRENT_RUN.read_bytes())
source=prod/'terravore-ascension-generator5-month.sav';sha='4371182e222afb2b0ad278c0b1e06f8b767ac28049ad39d1edccf6f6e10b6214';assert h.sha256(source)==sha
shutil.copytree(pu/'logs',prod/'logs-before-coordinator-control')
h.write_json(prod/'coordinator-production-normal-exit.json',{'status':'OBSERVED_NORMAL_GUI_EXIT','pid':20440,'forced':False,'running_after':False,'resume_sha256':'b5deb05a847f7463e2cf64c7cd1e3f15fc04381245bfe74f07bbbeda85f0f53c','pointer_sha256':h.sha256(backup)})
d=h.prepare('l_simp_chinese',[]);run=Path(d['artifact_dir']);user=Path(d['userdir']);shutil.copyfile(__file__,run/Path(__file__).name)
alias=user/'save games/acceptance-fixtures/coordinator-source.sav';alias.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,alias);assert h.sha256(alias)==sha
d.update(version='0.2.0',role='Isolated native coordinator capital tooltip diagnosis',scope='Original-byte Mod-derived world with enabled_mods empty. Missing EEP definitions form separate load baseline; not pure vanilla-origin generation or Mod acceptance.',original_seed={'path':str(source.resolve()),'sha256':sha,'alias':str(alias)},production_pointer_backup=str(backup.resolve()))
h.write_json(run/'manifest.json',d);assert json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]}
h.write_json(prod/'coordinator-control-pointer.json',{'artifact_dir':str(run),'userdir':str(user)})
h.write_json(run/'coordinator-isolation-preflight.json',{'status':'PASS_ISOLATION_ONLY','seed_sha256':sha,'enabled_mods':[],'scope':d['scope']})
print(json.dumps({'run_id':run.name,'source_sha256':sha,'enabled_mods':[]}),flush=True);print(json.dumps(h.launch(60,False)),flush=True)
