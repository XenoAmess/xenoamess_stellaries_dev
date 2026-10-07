import json
import logging
from pathlib import Path
import shutil
import sys
import time

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
run, user, manifest = r.harness.load_run()
order = manifest['conflict_order']
shutil.copyfile(Path(__file__), run / 'bootstrap_decision_conflict_recovered.py')
for attempt in range(20):
    frame = r.gpu_capture('conflict-' + order + '-title-ready-' + str(attempt))
    matches = [row for row in frame['rows'] if row['text'] == '关闭' and row['score'] >= .8]
    if len(matches) == 1:
        row = matches[0]
        r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'conflict-' + order + '-close-startup')
        break
    if any(row['text'] == '载入游戏' for row in frame['rows']):
        break
    time.sleep(10)
else:
    raise RuntimeError('native title did not become ready')
loaded = r.native_load('eep-zero', 'conflict-' + order + '-restore-exact-zero')
assert loaded['source_sha256'] == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5'
before = r.native_save('conflict-' + order + '-restored', '2200.01.01', (0,))
assert before['countries']['0']['native']['num_sapient_pops'] == 5700
assert before['countries']['0']['variables']['eep_d'] == 2
assert len([value for value in before['planets'].values() if 'perf_constructed' in value['flags']]) == 50
frame = r.gpu_capture('conflict-' + order + '-restored-outliner')
print(json.dumps({'run': run.name, 'order': order, 'sha': before['save_sha256'], 'image': frame['image'], 'rows': [row['text'] for row in frame['rows']]}, ensure_ascii=False), flush=True)
