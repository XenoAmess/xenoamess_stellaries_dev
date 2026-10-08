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
frame = r.gpu_capture('rc8-natural-main-fleet-before-native-return-order')
labels = [row['text'] for row in frame['rows']]
assert '2314.03.12' in labels and '暂停' in labels
assert any('第5舰队' in text for text in labels)
assert any('第41运输舰队' in text for text in labels)
assert any('4.2K' in text for text in labels)
point = [541, 338]
desktop = r.desktop_point(*point)
h.pyautogui.click(*desktop, button='right')
h.write_json(run / 'rc8-native-right-click-hostile-home-starbase.action.json', {
    'action': 'native_right_click_selected_existing_fleet_to_hostile_home_starbase',
    'client_point': point, 'desktop_point': list(desktop),
    'source_frame_sha256': frame['image_sha256'], 'actual_paused_date': '2314.03.12',
    'own_native_fleet_id': 1273, 'target_native_starbase_fleet_id': 0,
    'target_system_id': 5, 'actual_enemy_controller': 16777218,
    'clicked_at_utc': datetime.now(timezone.utc).isoformat()})
after = r.gpu_capture('rc8-natural-main-fleet-after-native-return-order')
print(json.dumps({'image': after['image'], 'texts': [row['text'] for row in after['rows']]}, ensure_ascii=True))
