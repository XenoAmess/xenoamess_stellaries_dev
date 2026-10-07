import json
import logging
from pathlib import Path
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
pending = json.loads((run / 'rc7-dual33-report-pending-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, pending['countries']))
loaded = r.native_load('dual33-report', 'rc7-dual33-pending-report-original-byte-load')
assert loaded['source_sha256'] == pending['save_sha256']
restored = r.native_save('rc7-dual33-report-reloaded-native', '2204.03.01', identities)
frame = r.gpu_capture('rc7-dual33-report-reloaded-still-pending-ui')
assert any('6594' in row['text'] for row in frame['rows'])
assert all(restored['countries'][key]['stockpile'] == pending['countries'][key]['stockpile'] for key in pending['countries'])
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets']:
    assert restored[key] == pending[key], key
options = [row for row in frame['rows'] if row['text'] == '退下。' and row['score'] >= .8]
assert len(options) == 1
row = options[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-dual33-report-reloaded-native-ack')
acked = r.native_save('rc7-dual33-report-reloaded-acked-native', '2204.03.01', identities)
assert all(acked['countries'][key]['stockpile'] == restored['countries'][key]['stockpile'] for key in restored['countries'])
assert acked['countries'] == restored['countries']
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert acked[key] == restored[key], key
print(json.dumps({'phase': 'country33 original-byte pending report reload and same-day acknowledgment', 'sha256': acked['save_sha256'], 'stocks': 'all37 preserved', 'collections': 'all9 preserved'}), flush=True)
