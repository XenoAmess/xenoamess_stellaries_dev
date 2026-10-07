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
old = json.loads((run / 'rc7-dual0-report-acked-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, old['countries']))
def command(value, stage):
    h.press_scan_code(0x29, stage + '-console-open', 1)
    h.type_text(value, True, stage + '-command')
    r.gpu_capture(stage + '-result')
    h.press_scan_code(0x29, stage + '-console-close', 1)
command('play 33', 'rc7-dual33-replay-player-native-control')
before = r.native_save('rc7-dual33-before-five-replays-native', '2204.03.01', identities)
with zipfile.ZipFile(run / 'rc7-dual33-before-five-replays-native.sav') as archive:
    assert 'country=33' in q.block(archive.read('gamestate').decode('utf-8-sig'), 'player')
assert before['countries'] == old['countries']
calls = ' country_event = { id = eep.2 }' * 5
command('effect event_target:eep_probe_original_country = {' + calls + ' } event_target:eep_probe_foreign = {' + calls + ' }', 'rc7-dual-both-five-monthly-replays')
after = r.native_save('rc7-dual-both-after-five-replays-native', '2204.03.01', identities)
assert all(after['countries'][key]['stockpile'] == before['countries'][key]['stockpile'] for key in before['countries'])
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets']:
    assert after[key] == before[key], key
assert after['countries']['0'] == before['countries']['0']
for owner, values in [('0', [('eep_c', 20), ('eep_g', 0), ('eep_d', 7), ('eep_made', 0)]), ('33', [('eep_c', 20), ('eep_g', 20), ('eep_d', 7), ('eep_made', 300)])]:
    assert all(after['countries'][owner]['variables'][key] == value for key, value in values)
assert 'eep_notice_pending' not in after['countries']['33']['flags']
assert 'eep_first_notice' in after['countries']['33']['flags']
assert after['countries']['33']['variables']['eep_stage'] == 1
print(r.gpu_capture('rc7-dual33-first-notice-after-five-replays-ui')['image'], flush=True)
