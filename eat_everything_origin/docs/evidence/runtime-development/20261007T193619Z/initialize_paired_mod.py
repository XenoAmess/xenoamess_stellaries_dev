import json
import logging
from pathlib import Path
import shutil
import sys

sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime', '--fixture']
import runtime as r

logging.disable(logging.INFO)
artifacts, userdir, manifest = r.harness.load_run()
frame = r.gpu_capture('rc6-paired-close-startup-guard')
matches = [row for row in frame['rows'] if row['text'] == '关闭' and row['score'] >= .8]
assert len(matches) == 1, matches
row = matches[0]
r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc6-paired-close-startup')
loaded = r.native_load('native-frozen', 'rc6-paired-load-native-base')
assert loaded['source_sha256'] == '962b7ab20132e76ec41bbe87120db2ece05f7252823634db017d94420512588f'
before = r.native_save('rc6-paired-native-before-origin-switch', '2200.01.01', (0,))
print(json.dumps({'stage': 'native original restored', 'sha': before['save_sha256'], 'country': before['countries']['0']['native']}, ensure_ascii=False), flush=True)
assert 'origin="origin_default"' in before['countries']['0']['government']
assert before['countries']['0']['variables'] == {}
assert before['countries']['0']['native']['num_sapient_pops'] == 5700
r.harness.press_scan_code(0x29, 'rc6-paired-init-console-open', 1)
r.harness.type_text('event eep_probe.60', True, 'rc6-paired-init-origin-switch-only')
r.gpu_capture('rc6-paired-init-console-result')
r.harness.press_scan_code(0x29, 'rc6-paired-init-console-close', 1)
zero = r.native_save('rc6-paired-mod-zero-frozen', '2200.01.01', (0,))
country = zero['countries']['0']
assert 'origin="origin_heart_of_devouring"' in country['government']
assert country['native']['num_sapient_pops'] == 5700
assert country['stockpile'] == before['countries']['0']['stockpile']
assert country['variables']['eep_c'] == country['variables']['eep_g'] == country['variables']['eep_made'] == 0
assert country['variables']['eep_d'] == 2
assert not any(value['type'] == 'situation_eep_devouring' for value in zero['situations'].values())
assert len([value for value in zero['planets'].values() if 'perf_constructed' in value['flags']]) == 50
assert zero['planets']['3']['planet_size'] == 20
destination = userdir / 'save games' / 'acceptance-fixtures' / 'eep-zero.sav'
assert not destination.exists()
shutil.copyfile(artifacts / 'rc6-paired-mod-zero-frozen.sav', destination)
assert r.harness.sha256(destination) == zero['save_sha256']
print(json.dumps({'stage': 'paired mod zero frozen', 'sha': zero['save_sha256'], 'date': zero['date'], 'vars': country['variables'], 'target': zero['event_targets']}, ensure_ascii=False), flush=True)
