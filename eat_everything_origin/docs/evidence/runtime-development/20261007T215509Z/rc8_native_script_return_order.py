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
frame = r.gpu_capture('rc8-native-script-return-before')
labels = [row['text'] for row in frame['rows']]
assert '2314.03.12' in labels and '暂停' in labels and '无指令' in labels
# Close the selected fleet; effect then runs in the player country context.
r.gpu_click(387, 63, 'rc8-close-selected-fleet-before-country-order')
h.press_scan_code(0x29, 'rc8-native-return-console-open', 1)
command = 'effect capital_scope = { save_global_event_target_as = eep_runtime_defense_target } every_owned_fleet = { limit = { fleet_power > 10000 } clear_fleet_actions = this auto_move_to_planet = { target = event_target:eep_runtime_defense_target clear_auto_move_on_arrival = yes } }'
h.type_text(command, True, 'rc8-existing-fleet-native-auto-move-order')
receipt = r.gpu_capture('rc8-existing-fleet-native-auto-move-console')
h.press_scan_code(0x29, 'rc8-native-return-console-close', 1)
r.gpu_click(924, 363, 'rc8-reselect-existing-main-fleet-after-native-order')
after = r.gpu_capture('rc8-native-script-return-after')
print(json.dumps({'image': after['image'], 'texts': [row['text'] for row in after['rows']]}, ensure_ascii=True))
