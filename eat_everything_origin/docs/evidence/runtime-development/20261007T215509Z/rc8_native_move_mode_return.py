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
copy = run / Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__), copy)
frame = r.gpu_capture('rc8-native-move-mode-return-before')
labels = [row['text'] for row in frame['rows']]
assert '2314.07.13' in labels and '暂停' in labels and '无指令' in labels
r.gpu_click(119, 63, 'rc8-native-main-move-mode-click')
h.pyautogui.moveTo(*r.desktop_point(730, 510), duration=.2)
hover = r.gpu_capture('rc8-native-main-move-mode-home-space-hover')
r.gpu_click(730, 510, 'rc8-native-main-move-to-home-system-space')
after = r.gpu_capture('rc8-native-move-mode-return-after')
print(json.dumps({'image': after['image'], 'texts': [row['text'] for row in after['rows']]}, ensure_ascii=True))
