import hashlib
import json
import logging
from pathlib import Path
import shutil
import sys

variant = sys.argv[1]
dlcs = {
    'nemesis': 'dlc/dlc025_nemesis/dlc025.dlc',
    'shroud': 'dlc/dlc037_shadows_shroud/dlc037.dlc',
}
assert variant in dlcs
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
assert not h.running_stellaris()
installed = Path('C:/SteamLibrary/steamapps/common/Stellaris') / dlcs[variant]
assert installed.is_file(), installed
data = h.prepare('l_simp_chinese', [], None)
run = Path(data['artifact_dir'])
user = Path(data['userdir'])
shutil.copyfile(Path(__file__), run / Path(__file__).name)
config_path = user / 'dlc_load.json'
config = json.loads(config_path.read_text(encoding='utf-8'))
assert len(config['enabled_mods']) == 1 and not config['disabled_dlcs']
config['disabled_dlcs'] = [dlcs[variant]]
h.write_json(config_path, config)
digest = hashlib.sha256(config_path.read_bytes()).hexdigest()
data['role'] = 'Simplified Chinese isolated missing-' + variant + ' DLC compatibility run'
data['dlc_variant'] = variant
data['disabled_dlcs'] = config['disabled_dlcs']
data['dlc_load_sha256'] = digest
data['dlc_actual_runtime_verified'] = False
data['scope'] = 'Disabled config is a request only; require native host_has_dlc YES/NO and legal gameplay evidence.'
h.write_json(run / 'manifest.json', data)
h.write_json(run / 'dlc-load-request.json', {
    'status': 'CONFIG_REQUEST_ONLY', 'variant': variant, 'config': config,
    'isolated_path': str(config_path), 'sha256': digest,
    'game_dlc_descriptor': str(installed), 'game_dlc_descriptor_sha256': h.sha256(installed),
})
print(json.dumps({'status': 'CONFIG_REQUEST_ONLY', 'run': str(run), 'userdir': str(user),
                  'variant': variant, 'dlc_load_sha256': digest}), flush=True)
