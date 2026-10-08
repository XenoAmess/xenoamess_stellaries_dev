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
shutil.copyfile(Path(__file__), run / Path(__file__).name)
source = Path('_runtime/heart-of-devouring/runs/20261007T100241Z/rc4-native-cruiser-eight-uv-refit-complete.sav')
receipt = r.native_load('hive-natural', 'rc8-hiveworld-natural2297-original-load')
assert receipt['source_sha256'] == h.sha256(source)
previous = json.loads(source.with_suffix('.audit.json').read_text(encoding='utf-8'))
after = r.native_save('rc8-hiveworld-natural2297-loaded', '2297.03.12', tuple(map(int, previous['countries'])))
h.write_json(run / 'rc8-hiveworld-natural-load-original-country-compare.json',
             {'date':after['date'], 'before_sha256':h.sha256(source), 'after_sha256':after['save_sha256'],
              'country0_equal':after['countries']['0'] == previous['countries']['0'],
              'comparison_required':'Native load may rebuild native caches; all differences retained in both full audits.'})
frame = r.gpu_capture('rc8-hiveworld-natural2297-outliner')
print(json.dumps({'date':after['date'], 'image':frame['image'], 'country0':after['countries']['0']}, ensure_ascii=True), flush=True)
