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
settled = json.loads((run / 'rc7-dual-separate-new33-settled-old0-isolated-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, settled['countries']))
before = r.native_save('rc7-dual33-report-before-native', '2204.03.01', identities)
r.gpu_click(870, 293, 'rc7-dual33-report-select-mother')
frame = r.gpu_capture('rc7-dual33-report-mother-button-guard')
assert any('波特的储藏室' in row['text'] for row in frame['rows'])
buttons = [row for row in frame['rows'] if '觐见女王' in row['text'] and row['score'] >= .8]
assert len(buttons) == 1
row = buttons[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-dual33-report-direct-button')
frame = r.gpu_capture('rc7-dual33-report-actual-own-core-ui')
assert any('6594' in row['text'] for row in frame['rows'])
pending = r.native_save('rc7-dual33-report-pending-native', '2204.03.01', identities)
assert pending['planets']['2014']['variables']['eep_actual_pop'] == 6594
assert pending['planets']['8']['variables'] == before['planets']['8']['variables']
assert all(pending['countries'][key]['stockpile'] == before['countries'][key]['stockpile'] for key in before['countries'])
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets']:
    assert pending[key] == before[key], key
alias = user / 'save games' / 'acceptance-fixtures' / 'dual33-report.sav'
assert not alias.exists()
shutil.copyfile(run / 'rc7-dual33-report-pending-native.sav', alias)
assert h.sha256(alias) == pending['save_sha256']
h.write_json(run / 'rc7-dual33-report-reload-alias.json', {'source': str(run / 'rc7-dual33-report-pending-native.sav'), 'alias': str(alias), 'sha256': pending['save_sha256']})
print(json.dumps({'phase': 'country33 direct native report', 'sha256': pending['save_sha256'], 'population': 6594, 'image': frame['image']}, ensure_ascii=False), flush=True)
