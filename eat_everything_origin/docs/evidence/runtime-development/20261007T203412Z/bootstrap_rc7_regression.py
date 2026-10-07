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
h = r.harness
run, user, manifest = h.load_run()
assert manifest['copied_mod_tree_sha256'] == 'ceb0ec4cd6968bde2ca0c06ba50568e52a6b6ccd520178b475adf8bcd25df2bc'
shutil.copyfile(Path(__file__), run / 'bootstrap_rc7_regression.py')
sources = {
    'eep-zero': Path('_runtime/heart-of-devouring/runs/20261007T193619Z/rc6-paired-mod-zero-frozen.sav'),
    'old-damage': Path('_runtime/heart-of-devouring/runs/20261007T154144Z/rc6-native-old-damage-day1-before-restart.sav'),
    'dual-owner': Path('_runtime/heart-of-devouring/runs/20261007T154144Z/rc6-mixed-generic-q20-current-start-no-native-flag.sav'),
    'hive-natural': Path('_runtime/heart-of-devouring/runs/20261007T100241Z/rc4-native-cruiser-eight-uv-refit-complete.sav'),
    'fleet2-natural': Path('_runtime/heart-of-devouring/runs/20261007T031421Z/nemesis-project1-completed-before-ack.sav'),
}
receipts = []
for alias, source in sources.items():
    destination = user / 'save games/acceptance-fixtures' / (alias + '.sav')
    assert not destination.exists()
    shutil.copyfile(source, destination)
    assert h.sha256(source) == h.sha256(destination)
    receipts.append({'alias': alias, 'original_source': str(source.resolve()), 'copied': str(destination), 'bytes': source.stat().st_size, 'sha256': h.sha256(source)})
h.write_json(run / 'borrowed-original-source-aliases.json', receipts)
for attempt in range(20):
    stage = 'rc7-title-ready-' + str(attempt)
    try:
        frame = r.gpu_capture(stage)
    except RuntimeError as error:
        if 'did not produce a fresh GPU screenshot' not in str(error):
            raise
        h.write_json(run / (stage + '-no-frame.json'), {'status': 'NO_FRAME_NOT_READY', 'error': str(error)})
        time.sleep(10)
        continue
    close = [row for row in frame['rows'] if row['text'] == '关闭' and row['score'] >= .8]
    if len(close) == 1:
        row = close[0]
        r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc7-close-startup')
        break
    if any(row['text'] == '载入游戏' for row in frame['rows']):
        break
    time.sleep(10)
else:
    raise RuntimeError('rc7 native title readiness was not confirmed')
loaded = r.native_load('eep-zero', 'rc7-common-zero-original-restored')
assert loaded['source_sha256'] == '796f0fe3083641b413cae3e2f62674548da96e146e11760dd5211a10cfd11be5'
before = r.native_save('rc7-common-zero-native-restored', '2200.01.01', (0,))
assert before['countries']['0']['native']['num_sapient_pops'] == 5700
assert before['colonies']['0']['actual_pop_sum'] == 700
assert before['countries']['0']['variables']['eep_d'] == 2
print(json.dumps({'run': run.name, 'version': '0.2.0-rc.7', 'restored_sha256': before['save_sha256'], 'date': before['date']}), flush=True)
