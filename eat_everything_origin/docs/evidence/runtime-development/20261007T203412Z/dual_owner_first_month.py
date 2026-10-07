import json
import logging
from pathlib import Path
import shutil
import sys
import time
import zipfile
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / 'dual_owner_first_month.py')
previous = json.loads((run / 'rc7-dual-new-owner44-actual100-seed-task0.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, previous['countries']))
h.press_scan_code(0x29, 'rc7-dual-player33-console-open', 1)
h.type_text('play 33', True, 'rc7-dual-player33-native-control')
r.gpu_capture('rc7-dual-player33-control-result')
h.press_scan_code(0x29, 'rc7-dual-player33-console-close', 1)
controlled = r.native_save('rc7-dual-player33-native-controller-confirmed', '2204.01.03', identities)
with zipfile.ZipFile(run / 'rc7-dual-player33-native-controller-confirmed.sav') as archive:
    player = q.block(archive.read('gamestate').decode('utf-8-sig'), 'player')
assert 'country=33' in player and 'country=16777218' not in player
assert all(controlled['countries'][str(identity)]['stockpile'] == previous['countries'][str(identity)]['stockpile'] for identity in (0, 33))
h.press_scan_code(0x29, 'rc7-dual-first-month-console-open', 1)
h.type_text('fast_forward 28', True, 'rc7-dual-first-month-actual-calendar')
for attempt in range(15):
    frame = r.gpu_capture('rc7-dual-first-month-complete-' + str(attempt))
    texts = [row['text'] for row in frame['rows']]
    if '2204.02.01' in texts and any('fastforwarded28days' in h.normalized(label) for label in texts):
        break
    time.sleep(5)
else:
    raise RuntimeError('dual first month was not confirmed')
h.press_scan_code(0x29, 'rc7-dual-first-month-console-close', 1)
month = r.native_save('rc7-dual-first-month-foreign-rights-native', '2204.02.01', identities)
assert all(month['countries']['0']['variables'][key] == value for key, value in [('eep_c', 20), ('eep_g', 0), ('eep_d', 7), ('eep_made', 0)])
assert all(month['countries']['33']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)])
tasks = [value for value in month['situations'].values() if value['type'] == 'situation_eep_devouring' and value.get('killed') != 'yes' and value['target']['id'] == 13]
assert len(tasks) == 1 and tasks[0]['country'] == 33 and tasks[0]['progress'] == 1
groups = [month['pop_groups'][str(identity)] for identity in month['colonies']['17']['pop_groups']]
frame = r.gpu_capture('rc7-dual-player33-first-month-queen-ui')
print(json.dumps({'phase': 'actual first month and native rights', 'sha256': month['save_sha256'], 'date': month['date'],
                  'source_groups': groups, 'source_task': tasks[0], 'queen_image': frame['image'], 'rows': [row['text'] for row in frame['rows']]}, ensure_ascii=False), flush=True)
