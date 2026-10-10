"""Prepare a legal native Terravore empire with published production only."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness
assert not h.running_stellaris()
assert Path('eat_everything_origin/VERSION').read_text(encoding='utf-8').strip()=='0.2.0'
preflight=Path('eat_everything_origin/docs/evidence/priority-terravore-package-preflight-2026-10-09.json')
assert json.loads(preflight.read_text(encoding='utf-8'))['status']=='PASS'
source=Path('_runtime/heart-of-devouring/fixtures/20261008T003321Z/mod/prescripted_countries/eep_probe_presets.txt')
original=source.read_text(encoding='utf-8')
design=original[:original.index('\neep_probe_02_hive')]
assert design.startswith('eep_probe_01_terravore = {')
design=design.replace('eep_probe_01_terravore','eep_priority_terravore',1)
design=design.replace('EEP 01 石质噬岩者','吞噬之心·噬岩者',1)
assert 'eep_probe' not in design and 'origin_heart_of_devouring' in design
assert 'auth_hive_mind' in design and 'trait_lithoid' in design and 'civic_hive_devouring_swarm' in design
m=h.prepare('l_simp_chinese',[])
run,user=Path(m['artifact_dir']),Path(m['userdir'])
assert m['copied_mod_tree_sha256']=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
assert len(m['repository_mod_files'])==41 and m['seeded_save'] is None and m['scheduled_commands']==[]
destination=user/'user_empire_designs_v3.4.txt'
assert not destination.exists()
destination.write_text(design,encoding='utf-8',newline='\n')
shutil.copyfile(source,run/'native-terravore-design-original-source.txt')
shutil.copyfile(destination,run/'native-terravore-user-empire-design.txt')
shutil.copyfile(Path(__file__),run/Path(__file__).name)
actual=json.loads((user/'dlc_load.json').read_text(encoding='utf-8'))
assert actual=={'enabled_mods':['mod/ugc_eep-local.mod'],'disabled_dlcs':[]}
m.update({'version':'0.2.0','role':'Priority route4 natural lithoid Terravore, production-only new campaign',
          'scope':'Legal native empire design; actual initial state/settings require runtime evidence. Not full route acceptance.',
          'mandatory_preflight':{'path':str(preflight.resolve()),'sha256':h.sha256(preflight)},
          'native_empire_design':{'source':str(source.resolve()),'source_sha256':h.sha256(source),
                                  'destination':str(destination),'sha256':h.sha256(destination),
                                  'changes':'Only outer empire ID and custom empire display name.',
                                  'runtime_verified':False},
          'requested_galaxy_settings':{'stars':200,'ai_empires':3,'advanced_ai':0,
                                      'technology_cost':0.5,'tradition_cost':0.25,
                                      'scope':'UI requested values, actual saved values must be verified.'}})
h.write_json(run/'manifest.json',m)
h.write_json(run/'priority-terravore-production-isolation-proof.json',
             {'status':'PASS_PACKAGE_ISOLATION_ONLY','actual_dlc_config':actual,
              'production_tree_sha256':m['copied_mod_tree_sha256'],'production_files':m['repository_mod_files'],
              'native_design_sha256':h.sha256(destination),'no_seed_save':m['seeded_save'] is None,
              'no_scheduled_commands':m['scheduled_commands']==[],
              'scope':'No probe mod or seeded world. Native legality and game settings are not yet verified.'})
print(json.dumps({'run_id':run.name,'tree_sha256':m['copied_mod_tree_sha256'],'files':41}),flush=True)
print(json.dumps(h.launch(30,False)),flush=True)
