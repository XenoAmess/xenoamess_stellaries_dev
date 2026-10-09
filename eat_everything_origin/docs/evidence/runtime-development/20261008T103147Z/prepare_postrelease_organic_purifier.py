"""Resume a documented natural organic Purifier save with published production."""
import json
import logging
import shutil
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r

logging.disable(logging.INFO)
h = r.harness
assert not h.running_stellaris()
assert Path('eat_everything_origin/VERSION').read_text(encoding='utf-8').strip() == '0.2.0'
source = Path('eat_everything_origin/docs/evidence/runtime-development/20261006T202737Z/purifier-natural-recovery-positive.sav')
assert h.sha256(source) == 'f91dc6611ff6289a099cad1dcd6c64d3d61d124d2a7c88f05b92a0fb286cf0b4'
with zipfile.ZipFile(source) as z:
    text = z.read('gamestate').decode('utf-8-sig')
assert 'eep_probe' not in text
preflight = Path('eat_everything_origin/docs/evidence/post-release-package-preflight-2026-10-08.json')
checked = json.loads(preflight.read_text(encoding='utf-8'))
assert checked['status'] == 'PASS'
m = h.prepare('l_simp_chinese', [])
run, user = Path(m['artifact_dir']), Path(m['userdir'])
assert m['copied_mod_tree_sha256'] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
assert len(m['repository_mod_files']) == 41
assert all('eep_probe' not in f['path'] and not f['path'].startswith('testing/')
           for f in m['repository_mod_files'])
shutil.copyfile(Path(__file__), run / Path(__file__).name)
alias = user / 'save games/acceptance-fixtures/purifier-start.sav'
alias.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, alias)
assert h.sha256(alias) == h.sha256(source)
m.update({'version': '0.2.0',
          'role': 'Post-release organic Fanatic Purifier natural continuation',
          'scope': 'Original-byte 2281 natural economic campaign continuation and formal production compatibility; not a new 80-year replay or full route acceptance.',
          'original_seed': {'path': str(source.resolve()), 'sha256': h.sha256(source), 'alias': str(alias)},
          'mandatory_preflight': {'path': str(preflight.resolve()), 'sha256': h.sha256(preflight)}})
h.write_json(run / 'manifest.json', m)
actual = json.loads((user / 'dlc_load.json').read_text(encoding='utf-8'))
assert actual == {'enabled_mods': ['mod/ugc_eep-local.mod'], 'disabled_dlcs': []}
h.write_json(run / 'organic-purifier-production-isolation-proof.json',
             {'status': 'PASS_SCOPED', 'actual_dlc_config': actual,
              'seed_sha256': h.sha256(alias), 'production_tree_sha256': m['copied_mod_tree_sha256'],
              'production_files': m['repository_mod_files'], 'scope': m['scope']})
print(json.dumps({'run_id': run.name, 'production_tree_sha256': m['copied_mod_tree_sha256'],
                  'scope': m['scope']}), flush=True)
print(json.dumps(h.launch(60, False)), flush=True)
