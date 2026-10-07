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
before = json.loads((run / 'rc7-dual0-report-before-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, before['countries']))
r.gpu_click(870, 293, 'rc7-dual0-report-select-bound-mother')
frame = r.gpu_capture('rc7-dual0-report-mother-button-guard')
assert any('EEP-Core' in row['text'] for row in frame['rows'])
buttons = [row for row in frame['rows'] if '觐见女王' in row['text'] and row['score'] >= .8]
assert len(buttons) == 1
row = buttons[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-dual0-report-direct-bound-mother-button')
frame = r.gpu_capture('rc7-dual0-report-actual-own-core-ui')
assert any('5838' in row['text'] for row in frame['rows'])
pending = r.native_save('rc7-dual0-report-pending-native', '2204.03.01', identities)
assert pending['planets']['8']['variables']['eep_actual_pop'] == 5838
assert pending['planets']['2014'] == before['planets']['2014']
assert all(pending['countries'][key]['stockpile'] == before['countries'][key]['stockpile'] for key in before['countries'])
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets']:
    assert pending[key] == before[key], key
frame = r.gpu_capture('rc7-dual0-report-still-pending-ack-guard')
options = [row for row in frame['rows'] if row['text'] == '退下。' and row['score'] >= .8]
assert len(options) == 1
row = options[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-dual0-report-native-ack')
acked = r.native_save('rc7-dual0-report-acked-native', '2204.03.01', identities)
assert acked['countries'] == pending['countries']
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert acked[key] == pending[key], key
print(json.dumps({'phase': 'old0 direct bound-mother report and same-day ACK', 'population': 5838, 'extra_capacity': 7, 'generic_matter': 0, 'manufactured': 0, 'sha256': acked['save_sha256']}), flush=True)
