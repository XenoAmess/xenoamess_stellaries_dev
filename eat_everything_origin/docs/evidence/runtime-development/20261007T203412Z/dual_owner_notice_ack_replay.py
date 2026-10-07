import json
import logging
from pathlib import Path
import shutil
import sys
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
pending = json.loads((run / 'rc7-dual-both-after-five-replays-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, pending['countries']))
frame = r.gpu_capture('rc7-dual33-first-notice-ack-guard')
options = [row for row in frame['rows'] if '余烬归于吞噬之心' in row['text'] and row['score'] >= .8]
assert len(options) == 1
row = options[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-dual33-first-notice-native-ack')
acked = r.native_save('rc7-dual33-first-notice-acked-native', '2204.03.01', identities)
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert acked[key] == pending[key], key
calls = ' country_event = { id = eep.2 }' * 5
h.press_scan_code(0x29, 'rc7-dual-after-ack-five-again-console-open', 1)
h.type_text('effect event_target:eep_probe_original_country = {' + calls + ' } event_target:eep_probe_foreign = {' + calls + ' }', True, 'rc7-dual-after-ack-five-again-command')
r.gpu_capture('rc7-dual-after-ack-five-again-result')
h.press_scan_code(0x29, 'rc7-dual-after-ack-five-again-console-close', 1)
replayed = r.native_save('rc7-dual-both-after-ack-five-again-native', '2204.03.01', identities)
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert replayed[key] == acked[key], key
print(json.dumps({'phase': 'both owners five plus five monthly calls and same-day new33 notice ACK', 'all37_state': 'unchanged', 'sha256': replayed['save_sha256']}), flush=True)
