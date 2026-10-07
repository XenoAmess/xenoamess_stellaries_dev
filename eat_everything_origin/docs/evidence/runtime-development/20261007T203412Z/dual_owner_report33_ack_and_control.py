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
restored = json.loads((run / 'rc7-dual33-report-reloaded-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, restored['countries']))
frame = r.gpu_capture('rc7-dual33-report-reloaded-recovery-pending-ui')
assert any('6594' in row['text'] for row in frame['rows'])
options = [row for row in frame['rows'] if row['text'] == '退下。' and row['score'] >= .8]
assert len(options) == 1
row = options[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-dual33-report-reloaded-recovery-native-ack')
acked = r.native_save('rc7-dual33-report-reloaded-acked-native', '2204.03.01', identities)
assert acked['countries'] == restored['countries']
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert acked[key] == restored[key], key
before = json.loads((run / 'rc7-dual33-report-before-native.audit.json').read_text(encoding='utf-8'))
alias = user / 'save games' / 'acceptance-fixtures' / 'dual33-no-report.sav'
assert not alias.exists()
shutil.copyfile(run / 'rc7-dual33-report-before-native.sav', alias)
assert h.sha256(alias) == before['save_sha256']
h.write_json(run / 'rc7-dual33-no-report-reload-alias.json', {'source': str(run / 'rc7-dual33-report-before-native.sav'), 'alias': str(alias), 'sha256': before['save_sha256']})
loaded = r.native_load('dual33-no-report', 'rc7-dual33-no-report-load-only-control')
assert loaded['source_sha256'] == before['save_sha256']
control = r.native_save('rc7-dual33-no-report-reloaded-native-control', '2204.03.01', identities)
print(json.dumps({'phase': 'full unchanged same-day report ACK and separate no-report original-byte reload control', 'acked_sha256': acked['save_sha256'], 'control_sha256': control['save_sha256']}), flush=True)
