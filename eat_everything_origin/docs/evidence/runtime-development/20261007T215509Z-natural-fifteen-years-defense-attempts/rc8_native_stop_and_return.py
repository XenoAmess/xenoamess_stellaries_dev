import json
import logging
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone

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
frame = r.gpu_capture('rc8-native-stop-return-before')
labels = [row['text'] for row in frame['rows']]
assert '2314.03.12' in labels and '暂停' in labels
assert any('正在跟随第41运输舰队' in t for t in labels)
r.gpu_click(68, 63, 'rc8-native-stop-existing-main-fleet')
stopped = r.gpu_capture('rc8-native-stop-existing-main-fleet-after')
point = [525, 546]
desktop = r.desktop_point(*point)
h.pyautogui.click(*desktop, button='right')
h.write_json(run / 'rc8-native-right-click-actual-mother-icon.action.json', {
    'action': 'native_right_click_actual_mother_icon_after_stop',
    'client_point': point, 'desktop_point': list(desktop),
    'source_frame_sha256': stopped['image_sha256'], 'actual_paused_date': '2314.03.12',
    'own_native_fleet_id': 1273, 'target_physical_planet_id': 1,
    'clicked_at_utc': datetime.now(timezone.utc).isoformat()})
after = r.gpu_capture('rc8-native-stop-return-after')
print(json.dumps({'image': after['image'], 'texts': [row['text'] for row in after['rows']]}, ensure_ascii=True))
