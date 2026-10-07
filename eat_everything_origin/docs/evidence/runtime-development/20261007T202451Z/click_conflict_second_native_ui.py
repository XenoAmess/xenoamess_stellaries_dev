import json
import logging
from pathlib import Path
import shutil
import sys

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r
logging.disable(logging.INFO)
run, user, manifest = r.harness.load_run()
assert manifest['conflict_order'] == 'eep-last'
prefix = 'conflict-eep-last'
shutil.copyfile(Path(__file__), run / 'click_conflict_second_native_ui.py')
def click(frame, label, stage, predicate=lambda row: True):
    matches = [row for row in frame['rows'] if row['text'] == label and row['score'] >= .8 and predicate(row)]
    assert len(matches) == 1, matches
    row = matches[0]
    r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), stage)
frame = r.gpu_capture(prefix + '-source-selection-guard')
click(frame, '春天', prefix + '-open-real-source', lambda row: min(point[0] for point in row['box']) > 850)
frame = r.gpu_capture(prefix + '-source-page-guard')
assert any(row['text'] == '春天' and max(point[0] for point in row['box']) < 250 for row in frame['rows'])
assert any(row['text'] == '规模：20' for row in frame['rows'])
click(frame, '决议', prefix + '-open-decisions')
frame = r.gpu_capture(prefix + '-decision-list-guard')
click(frame, '吞噬星球', prefix + '-native-original-decision-click',
      lambda row: min(point[0] for point in row['box']) > 700 and min(point[1] for point in row['box']) < 150)
frame = r.gpu_capture(prefix + '-original-decision-after-click')
print(json.dumps({'image': frame['image'], 'rows': [row['text'] for row in frame['rows']]}, ensure_ascii=False), flush=True)
