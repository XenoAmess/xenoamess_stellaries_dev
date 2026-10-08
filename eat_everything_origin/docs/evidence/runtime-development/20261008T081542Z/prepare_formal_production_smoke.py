import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;assert not h.running_stellaris();assert Path('eat_everything_origin/VERSION').read_text(encoding='utf-8').strip()=='0.2.0'
seed=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T063908Z/rc9-missing-nemesis-legal-fresh-initial.sav');assert h.sha256(seed)=='fb41124035c2cad09ed817cbdd252386e9572dc5e1366b3dae6038465e090136'
with zipfile.ZipFile(seed) as z:t=z.read('gamestate').decode('utf-8-sig')
assert 'eep_probe' not in t
m=h.prepare('l_simp_chinese',[],None);run=Path(m['artifact_dir']);user=Path(m['userdir']);shutil.copyfile(Path(__file__),run/Path(__file__).name)
folder=user/'save games'/'acceptance-fixtures';folder.mkdir();destination=folder/'prod-clean-start.sav';shutil.copyfile(seed,destination);assert h.sha256(destination)==h.sha256(seed)
assert all('eep_probe' not in f['path'] and not f['path'].startswith('testing/') for f in m['copied_mod_files'])
m['role']='Final 0.2.0 production-only CN offline smoke';m['version']='0.2.0';m['scope']='Original-byte clean legal initial world from prior fixture run, no probe references in save and no testing module in this process; not a new random generation.'
m['original_seed']={'path':str(seed.resolve()),'sha256':h.sha256(seed),'alias':str(destination)};h.write_json(run/'manifest.json',m);print(json.dumps({'run':str(run),'production_sha256':m['copied_mod_tree_sha256'],'scope':m['scope']}),flush=True)
