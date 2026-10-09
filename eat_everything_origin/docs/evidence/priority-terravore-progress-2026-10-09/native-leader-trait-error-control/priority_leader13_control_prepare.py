"""Empty-mod branch for one native leader.13 diagnostic, original world bytes."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris()
prod,pu,pm=h.load_run();backup=Path('_runtime/heart-of-devouring/priority-leader13-production-pointer.json');assert not backup.exists();backup.write_bytes(h.CURRENT_RUN.read_bytes())
source=prod/'terravore-defense-post-battle-repair-month.sav';sha='d2daf0d4bc7cfd690abb5c573f657a7bd97121d4babaf7b703d3beeef7d69c6f';assert h.sha256(source)==sha
shutil.copytree(pu/'logs',prod/'logs-before-leader13-control')
h.write_json(prod/'leader13-production-normal-exit.json',{'status':'OBSERVED_NORMAL_GUI_EXIT','pid':12528,'forced':False,'running_after':False,'resume_sha256':sha,'pointer_sha256':h.sha256(backup)})
d=h.prepare('l_simp_chinese',[]);run=Path(d['artifact_dir']);user=Path(d['userdir']);shutil.copyfile(__file__,run/Path(__file__).name)
alias=user/'save games/acceptance-fixtures/leader13-source.sav';alias.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,alias);assert h.sha256(alias)==sha
d.update(version='0.2.0',role='Isolated native leader.13 trait rejection diagnosis',scope='Original-byte Mod-derived world, enabled_mods empty. Missing EEP definitions are separate load baseline; not vanilla-origin generation or Mod acceptance.',original_seed={'path':str(source.resolve()),'sha256':sha,'alias':str(alias)},production_pointer_backup=str(backup.resolve()))
h.write_json(run/'manifest.json',d);assert json.loads((user/'dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]}
h.write_json(run/'leader13-isolation-preflight.json',{'status':'PASS_ISOLATION_ONLY','seed_sha256':sha,'enabled_mods':[],'scope':d['scope']})
print(json.dumps({'run_id':run.name,'source_sha256':sha,'enabled_mods':[]}),flush=True);print(json.dumps(h.launch(60,False)),flush=True)
