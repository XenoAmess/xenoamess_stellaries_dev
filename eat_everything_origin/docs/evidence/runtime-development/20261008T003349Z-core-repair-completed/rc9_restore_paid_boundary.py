import json
import logging
from pathlib import Path
import shutil
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h = r.harness
run, user, manifest = h.load_run()
copy = run / Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__), copy)
for n in range(30):
    frame = r.gpu_capture('rc9-paid-boundary-boot-' + str(n))
    labels = [v['text'] for v in frame['rows']]
    if '载入游戏' in labels and '新游戏' in labels:
        break
    time.sleep(5)
else:
    raise RuntimeError('Native Chinese title menu was not confirmed; no load input sent.')
receipt = r.native_load('hive-before-end', 'rc9-paid-boundary-original-load')
assert receipt['source_sha256'] == 'aa8c5f3a64ecec03cfd902c2823a95c619dfaa5048641c3a956f0615277d7092'
after = r.native_save('rc9-hiveworld-original-paid-day7199', '2319.03.11', (0,))
c = after['countries']['0']
before = json.loads(Path('_runtime/heart-of-devouring/runs/20261007T215509Z/rc8-hiveworld-terraform-final-day-before.audit.json').read_text(encoding='utf-8'))
assert c['stockpile'] == before['countries']['0']['stockpile']
assert all(c['variables'][k] == before['countries']['0']['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds'])
assert after['planets']['1']['planet_class'] == 'pc_volcanic'
assert after['planets']['1']['colony'] == 0
assert after['colonies']['0']['actual_pop_sum'] == 1981
assert sum(after['deposits'][str(i)]['type'] == 'd_eep_core' for i in after['planets']['1']['deposits']) == 1
print(json.dumps({'status':'PAID_NATIVE_BOUNDARY_RESTORED','date':after['date'],
                  'save_sha256':after['save_sha256'],'source_sha256':receipt['source_sha256'],
                  'stockpile_same':True,'population':1981,'core_deposit_count':1},ensure_ascii=True),flush=True)
