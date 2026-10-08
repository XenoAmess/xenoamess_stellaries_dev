import json
import logging
from pathlib import Path
import shutil
import sys

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
frame = r.gpu_capture('rc9-paid-boundary-recovered-news')
labels = [v['text'] for v in frame['rows']]
assert '关闭' in labels and any('Cygnus' in t for t in labels)
r.gpu_click_text('关闭','rc9-paid-boundary-native-news-close')
title = r.gpu_capture('rc9-paid-boundary-recovered-title')
assert '载入游戏' in [v['text'] for v in title['rows']]
receipt = r.native_load('hive-before-end', 'rc9-paid-boundary-recovered-original-load')
assert receipt['source_sha256'] == 'aa8c5f3a64ecec03cfd902c2823a95c619dfaa5048641c3a956f0615277d7092'
after = r.native_save('rc9-hiveworld-original-paid-day7199', '2319.03.11', (0,))
c = after['countries']['0']
before = json.loads(Path('_runtime/heart-of-devouring/runs/20261007T215509Z/rc8-hiveworld-terraform-final-day-before.audit.json').read_text(encoding='utf-8'))
checks = {
 'all_stockpile_same':c['stockpile'] == before['countries']['0']['stockpile'],
 'ledger_same':all(c['variables'][k] == before['countries']['0']['variables'][k] for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),
 'class_volcanic':after['planets']['1']['planet_class'] == 'pc_volcanic',
 'physical_colony':after['planets']['1']['colony'] == 0,
 'population':after['colonies']['0']['actual_pop_sum'] == 1981,
 'one_core_deposit':sum(after['deposits'][str(i)]['type'] == 'd_eep_core' for i in after['planets']['1']['deposits']) == 1,
}
result = {'status':'PAID_NATIVE_BOUNDARY_RESTORED' if all(checks.values()) else 'FAILED_PRECONDITION',
          'date':after['date'],'save_sha256':after['save_sha256'],'source_sha256':receipt['source_sha256'],
          'checks':checks,'scope':'Authoritative paid source preconditions, not full native cache equality.'}
h.write_json(run / 'rc9-paid-boundary-recovered-preconditions.json',result)
print(json.dumps(result,ensure_ascii=True),flush=True)
assert all(checks.values())
