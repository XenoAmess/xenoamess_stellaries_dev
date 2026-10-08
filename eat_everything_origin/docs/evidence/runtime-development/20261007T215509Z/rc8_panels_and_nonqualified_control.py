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
before = json.loads((run / 'rc8-bound-mother-direct-report-closed.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, before['countries']))
panels = r.native_save('rc8-fleet-country-mother-panels-same-day', '2204.03.01', identities)
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert panels[key] == before[key], key
h.press_scan_code(0x29, 'rc8-nonqualified-native-player1-console-open', 1)
h.type_text('play 1', True, 'rc8-nonqualified-native-player1-control')
r.gpu_capture('rc8-nonqualified-native-player1-control-result')
h.press_scan_code(0x29, 'rc8-nonqualified-native-player1-console-close', 1)
controlled = r.native_save('rc8-nonqualified-player1-confirmed-native', '2204.03.01', identities)
with zipfile.ZipFile(run / 'rc8-nonqualified-player1-confirmed-native.sav') as archive:
    native = archive.read('gamestate').decode('utf-8-sig')
assert 'country=1' in q.block(native, 'player')
country1 = q.block(q.block(native, 'country'), '1')
assert q.scalars(country1)['origin'] != 'origin_heart_of_devouring'
assert not controlled['countries']['1']['flags'] and not controlled['countries']['1']['variables']
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert controlled[key] == panels[key], key
print(r.gpu_capture('rc8-nonqualified-player1-actual-outliner')['image'], flush=True)
