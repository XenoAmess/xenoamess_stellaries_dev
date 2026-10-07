import json
import logging
from pathlib import Path
import shutil
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
shutil.copyfile(Path(__file__), run / Path(__file__).name)
previous = json.loads((run / 'rc7-dual-separate-new33-real100-seed-task0-native.audit.json').read_text(encoding='utf-8'))
identities = tuple(map(int, previous['countries']))
h.press_scan_code(0x29, 'rc7-dual-separate-first-month-console-open', 1)
h.type_text('fast_forward 28', True, 'rc7-dual-separate-first-month-actual-calendar')
for attempt in range(15):
    frame = r.gpu_capture('rc7-dual-separate-first-month-complete-' + str(attempt))
    labels = [row['text'] for row in frame['rows']]
    if '2204.03.01' in labels and any('fastforwarded28days' in h.normalized(label) for label in labels):
        break
    time.sleep(5)
else:
    raise RuntimeError('separate first month was not confirmed')
h.press_scan_code(0x29, 'rc7-dual-separate-first-month-console-close', 1)
month = r.native_save('rc7-dual-separate-first-month-stable-owner33-native', '2204.03.01', identities)
assert month['planets']['196']['owner'] == 33 and month['planets']['196']['controller'] == 33
assert month['planets']['8']['owner'] == 0 and month['planets']['2014']['owner'] == 33
assert all(month['countries']['0']['variables'][key] == value for key, value in [('eep_c', 20), ('eep_g', 0), ('eep_d', 7), ('eep_made', 0)])
assert all(month['countries']['33']['variables'][key] == value for key, value in [('eep_c', 0), ('eep_g', 0), ('eep_d', 2), ('eep_made', 0)])
tasks = [value for value in month['situations'].values() if value['type'] == 'situation_eep_devouring' and value.get('killed') != 'yes' and value['target']['id'] == 196]
assert len(tasks) == 1 and tasks[0]['country'] == 33 and tasks[0]['progress'] == 1
groups = [month['pop_groups'][str(identity)] for identity in month['colonies']['19']['pop_groups']]
frame = r.gpu_capture('rc7-dual-separate-player33-first-month-ui')
result = {'phase': 'actual first month with source and starbase transferred', 'source': 196, 'owner': 33, 'sha256': month['save_sha256'], 'date': month['date'], 'source_groups': groups, 'source_task': tasks[0], 'frame': frame['image'], 'labels': [row['text'] for row in frame['rows']]}
(run / 'rc7-dual-separate-first-month-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False), flush=True)
