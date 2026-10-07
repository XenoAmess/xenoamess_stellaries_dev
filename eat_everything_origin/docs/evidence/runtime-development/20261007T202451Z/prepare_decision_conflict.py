import json
import logging
from pathlib import Path
import shutil
import sys

order = sys.argv[1]
assert order in ('eep-first', 'eep-last')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
seed = Path('_runtime/heart-of-devouring/runs/20261007T193619Z/rc6-paired-mod-zero-frozen.sav')
assert h.sha256(seed) == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5'
control = Path('_runtime/heart-of-devouring/fixtures/decision-conflict-control-20261008/mod')
package = json.loads(Path('eat_everything_origin/docs/evidence/decision-conflict-control-package-2026-10-08.json').read_text(encoding='utf-8-sig'))
assert package['status'] == 'PASS'
manifest = h.prepare('l_simp_chinese', [], seed)
run, user, _ = h.load_run()
destination = user / 'mod/eep-conflict'
shutil.copytree(control, destination)
source_files, source_hash = h.tree_manifest(control)
copied_files, copied_hash = h.tree_manifest(destination)
assert source_files == copied_files and source_hash == copied_hash
outer = user / 'mod/ugc_eep-conflict.mod'
outer.write_text((destination / 'descriptor.mod').read_text(encoding='utf-8-sig') + '\npath="' + destination.as_posix() + '"\n', encoding='utf-8', newline='\n')
enabled = ['mod/ugc_eep-local.mod', 'mod/ugc_eep-conflict.mod']
if order == 'eep-last':
    enabled.reverse()
h.write_json(user / 'dlc_load.json', {'enabled_mods': enabled, 'disabled_dlcs': []})
manifest.update(role='Controlled native decision conflict, two actual enabled_mods orders',
                conflict_order=order, enabled_mods=enabled,
                conflict_mod={'source': str(control.resolve()), 'copied': str(destination),
                              'tree_sha256': copied_hash, 'files': copied_files,
                              'outer_descriptor_sha256': h.sha256(outer)},
                dlc_load_sha256=h.sha256(user / 'dlc_load.json'))
h.write_json(run / 'manifest.json', manifest)
alias = user / 'save games/acceptance-fixtures/eep-zero.sav'
assert not alias.exists()
shutil.copyfile(seed, alias)
assert h.sha256(alias) == h.sha256(seed)
shutil.copyfile(Path(__file__), run / 'prepare_decision_conflict.py')
print(json.dumps({'run': run.name, 'order': order, 'enabled_mods': enabled, 'control_tree': copied_hash}), flush=True)
process = h.launch(45, False)
print(json.dumps(process), flush=True)
