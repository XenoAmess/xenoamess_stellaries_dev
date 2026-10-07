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
assert manifest['copied_mod_tree_sha256'] == '42946a595c9b740c14cea9d1a96775b3a4efb6db8a7a9baa27fe89eb9bb22014'
shutil.copyfile(Path(__file__), run / Path(__file__).name)
sources = {
    'rc8-queen': Path('_runtime/heart-of-devouring/runs/20261007T203412Z/rc7-dual33-report-pending-native.sav'),
    'rc8-twin': Path('_runtime/heart-of-devouring/runs/20261007T203412Z/rc7-dual-both-after-ack-five-again-native.sav'),
    'hive-natural': Path('_runtime/heart-of-devouring/runs/20261007T100241Z/rc4-native-cruiser-eight-uv-refit-complete.sav'),
    'fleet2-natural': Path('_runtime/heart-of-devouring/runs/20261007T031421Z/nemesis-project1-completed-before-ack.sav'),
}
receipts = []
for alias, source in sources.items():
    destination = user / 'save games' / 'acceptance-fixtures' / (alias + '.sav')
    assert not destination.exists()
    shutil.copyfile(source, destination)
    assert h.sha256(source) == h.sha256(destination)
    receipts.append({'alias': alias, 'original_source': str(source.resolve()), 'copied': str(destination), 'bytes': source.stat().st_size, 'sha256': h.sha256(source)})
h.write_json(run / 'borrowed-original-source-aliases.json', receipts)
for attempt in range(20):
    stage = 'rc8-title-ready-' + str(attempt)
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
        r.gpu_click(round(sum(point[0] for point in row['box']) / 4), round(sum(point[1] for point in row['box']) / 4), 'rc8-close-startup')
        break
    if any(row['text'] == '载入游戏' for row in frame['rows']):
        break
    time.sleep(10)
else:
    raise RuntimeError('rc8 native title readiness was not confirmed')
loaded = r.native_load('rc8-queen', 'rc8-queen-pending-original-byte-load')
assert loaded['source_sha256'] == 'c7e32cc3c76f6a6d25bf97905e23efc2e09d7d48862d8e3619083f7ea5a9a767'
previous = json.loads(Path('_runtime/heart-of-devouring/runs/20261007T203412Z/rc7-dual33-report-reloaded-native.audit.json').read_text(encoding='utf-8'))
before = r.native_save('rc8-queen-pending-original-restored', '2204.03.01', tuple(map(int, previous['countries'])))
assert before['countries'] == previous['countries']
for key in ['colonies', 'pop_groups', 'pop_jobs', 'districts', 'deposits', 'situations', 'species', 'event_targets', 'planets']:
    assert before[key] == previous[key], key
frame = r.gpu_capture('rc8-queen-pending-original-restored-ui')
assert any('6594' in row['text'] for row in frame['rows'])
error = user / 'logs' / 'error.log'
assert "Wrong scope for trigger 'is_owned_by'" not in error.read_text(encoding='utf-8-sig')
shutil.copyfile(error, run / 'rc8-pending-report-load-stage-error.log')
print(json.dumps({'run': run.name, 'version': '0.2.0-rc.8', 'same_original_load_all37_and_all9': 'PASS', 'date': before['date'], 'sha256': before['save_sha256'], 'scope_error_at_current_stage': False}), flush=True)
