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
frame = r.gpu_capture('rc8-native-physical-return-before')
labels = [row['text'] for row in frame['rows']]
assert '2314.03.13' in labels and '暂停' in labels
h.press_scan_code(0x29, 'rc8-physical-return-console-open', 1)
command = 'effect capital_scope = { planet = { save_global_event_target_as = eep_runtime_physical_defense } } every_owned_fleet = { limit = { fleet_power > 10000 } clear_fleet_actions = this auto_move_to_planet = { target = event_target:eep_runtime_physical_defense clear_auto_move_on_arrival = yes } }'
h.type_text(command, True, 'rc8-existing-fleet-physical-auto-move-order')
receipt = r.gpu_capture('rc8-existing-fleet-physical-auto-move-console')
h.press_scan_code(0x29, 'rc8-physical-return-console-close', 1)
after = r.gpu_capture('rc8-native-physical-return-after')
print(json.dumps({'image': after['image'], 'texts': [row['text'] for row in after['rows']]}, ensure_ascii=True))
