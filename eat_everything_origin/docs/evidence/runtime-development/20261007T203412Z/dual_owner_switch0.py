import json
import logging
from pathlib import Path
import shutil
import sys
import zipfile
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
control = json.loads((run / 'rc7-dual33-no-report-reloaded-native-control.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, control['countries']))
h.press_scan_code(0x29, 'rc7-dual-player0-console-open', 1)
h.type_text('play 0', True, 'rc7-dual-player0-native-control')
r.gpu_capture('rc7-dual-player0-control-result')
h.press_scan_code(0x29, 'rc7-dual-player0-console-close', 1)
switched = r.native_save('rc7-dual0-report-before-native', '2204.03.01', identities)
with zipfile.ZipFile(run / 'rc7-dual0-report-before-native.sav') as archive:
    player = q.block(archive.read('gamestate').decode('utf-8-sig'), 'player')
assert 'country=0' in player
assert switched['countries'] == control['countries']
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert switched[key] == control[key], key
print(r.gpu_capture('rc7-dual-player0-actual-outliner')['image'], flush=True)
