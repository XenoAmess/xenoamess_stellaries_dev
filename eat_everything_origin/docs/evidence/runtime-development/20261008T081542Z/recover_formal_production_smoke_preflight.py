import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert run.name=='20261008T081542Z' and not h.running_stellaris();dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
files,tree=h.tree_manifest(Path(m['copied_mod']));assert files==m['repository_mod_files'] and tree==m['repository_mod_tree_sha256'];assert all('eep_probe' not in f['path'] and not f['path'].startswith('testing/') for f in files)
seed=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T063908Z/rc9-missing-nemesis-legal-fresh-initial.sav');destination=user/'save games/acceptance-fixtures/prod-clean-start.sav';assert h.sha256(seed)==h.sha256(destination)=='fb41124035c2cad09ed817cbdd252386e9572dc5e1366b3dae6038465e090136'
with zipfile.ZipFile(destination) as z:t=z.read('gamestate').decode('utf-8-sig')
assert 'eep_probe' not in t;m['role']='Final 0.2.0 production-only CN offline smoke';m['version']='0.2.0';m['scope']='Original-byte clean legal initial world, no probe references in save and no testing module in this process; not new random generation.';m['original_seed']={'path':str(seed.resolve()),'sha256':h.sha256(seed),'alias':str(destination)};h.write_json(run/'manifest.json',m)
h.write_json(run/'production-only-preflight.json',{'status':'PASS','production_files':{f['path']:f['sha256'] for f in files},'actual_copy_tree_sha256':tree,'source_and_copy_exact':True,'no_testing_module':True,'clean_native_seed':m['original_seed'],'original_helper_failure_preserved':True})
print(json.dumps({'run':str(run),'production_tree':tree,'files':len(files),'no_probe':True}),flush=True)
