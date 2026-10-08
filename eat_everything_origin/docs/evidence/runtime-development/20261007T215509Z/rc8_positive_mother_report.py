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
restored = json.loads((run / 'rc8-queen-pending-original-restored.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, restored['countries']))
def acknowledge(stage):
    frame = r.gpu_capture(stage + '-guard')
    options = [row for row in frame['rows'] if row['text'] == '退下。' and row['score'] >= .8]
    assert len(options) == 1
    row = options[0]
    r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), stage + '-click')
acknowledge('rc8-restored-report-native-ack')
acked = r.native_save('rc8-first-pending-report-acked', '2204.03.01', identities)
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert acked[key] == restored[key], key
r.gpu_click(870, 293, 'rc8-select-actual-bound-mother')
frame = r.gpu_capture('rc8-bound-mother-direct-button-guard')
assert any('波特的储藏室' in row['text'] for row in frame['rows'])
buttons = [row for row in frame['rows'] if '觐见女王' in row['text'] and row['score'] >= .8]
assert len(buttons) == 1
row = buttons[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc8-bound-mother-direct-button-click')
frame = r.gpu_capture('rc8-bound-mother-direct-report-ui')
assert any('6594' in row['text'] for row in frame['rows'])
pending = r.native_save('rc8-bound-mother-direct-report-pending', '2204.03.01', identities)
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert pending[key] == acked[key], key
acknowledge('rc8-direct-mother-report-native-ack')
closed = r.native_save('rc8-bound-mother-direct-report-closed', '2204.03.01', identities)
for key in ['countries', 'colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert closed[key] == pending[key], key
r.gpu_click(870, 326, 'rc8-select-owned-nonmother')
frame = r.gpu_capture('rc8-owned-nonmother-button-hidden-ui')
assert any('菲伦港口' in row['text'] for row in frame['rows'])
assert not any('觐见女王' in row['text'] for row in frame['rows'])
shutil.copyfile(user / 'logs/error.log', run / 'rc8-positive-and-nonmother-stage-error.log')
assert "Wrong scope for trigger 'is_owned_by'" not in (run / 'rc8-positive-and-nonmother-stage-error.log').read_text(encoding='utf-8-sig')
print(json.dumps({'phase': 'rc8 pending native reload ACK, direct mother report open/ACK and actual own nonmother hidden', 'all37_and_all9': 'strictly unchanged', 'sha256': closed['save_sha256']}), flush=True)
