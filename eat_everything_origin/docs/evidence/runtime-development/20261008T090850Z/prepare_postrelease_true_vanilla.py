import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris()
source=Path('eat_everything_origin/docs/evidence/runtime-development/20261007T184149Z/vanilla-shared-world-native-initial.sav');assert h.sha256(source)=='6c312b601b1bff74c6f66029e5a0e7faaeef9f8e76f8d68d9753496ff18db736'
with zipfile.ZipFile(source) as z:t=z.read('gamestate').decode('utf-8-sig')
assert 'eep_probe' not in t and 'origin_heart_of_devouring' not in t
d=h.prepare('l_simp_chinese',[]);run=Path(d['artifact_dir']);user=Path(d['userdir']);shutil.copyfile(Path(__file__),run/Path(__file__).name)
alias=user/'save games/acceptance-fixtures/vanilla-start.sav';alias.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,alias);assert h.sha256(alias)==h.sha256(source)
d['version']='0.2.0';d['role']='Post-release actual no-mod native Terravore Q20 boundary control';d['scope']='No enabled mods, no testing/probes; original-byte native default-origin Lithoid Hive initial world, controlled single-source setup to follow.';d['original_seed']={'path':str(source.resolve()),'sha256':h.sha256(source),'alias':str(alias)};h.write_json(run/'manifest.json',d)
actual=json.loads((user/'dlc_load.json').read_text(encoding='utf-8'));assert actual=={'enabled_mods':[],'disabled_dlcs':[]}
h.write_json(run/'true-vanilla-isolation-preflight.json',{'status':'PASS_SCOPED','enabled_mods':[],'disabled_dlcs':[],'dlc_config_sha256':h.sha256(user/'dlc_load.json'),'seed_sha256':h.sha256(alias),'no_probe_or_EEP_origin_in_seed':True,'source_only_copied_unused_mod_directory':'The prepare harness copies production files, but actual enabled_mods is empty; no mod scripts are loaded.','scope':d['scope']})
print(json.dumps({'run_id':run.name,'actual_enabled_mods':[],'seed_sha256':h.sha256(alias)}),flush=True);print(json.dumps(h.launch(60,False)),flush=True)
