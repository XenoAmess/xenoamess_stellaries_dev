import hashlib
import json
import logging
from pathlib import Path
import shutil
import sys
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,manifest=h.load_run()
copy=run / Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__),copy)
items=[
 ('hive-fixed',run/'rc9-hiveworld-paid-natural-complete.sav','49e2a32f58d292702f82b07ca771ea0bbe8475728c4b6e1874dcc3b0f3791488'),
 ('core-dead',Path('_runtime/heart-of-devouring/runs/20261007T145123Z/rc6-core-death-real-day-replay-restart-refused.sav'),'7d165bc463d92076fd969c0ae1eeaa29d4026e2b4872ef1cfb35f291862a86e1'),
]
rows=[]
for alias,source,expected in items:
 source=source.resolve()
 digest=hashlib.sha256(source.read_bytes()).hexdigest()
 assert digest==expected
 dest=user/'save games/acceptance-fixtures'/(alias+'.sav')
 assert not dest.exists()
 shutil.copyfile(source,dest)
 assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
 a=json.loads(source.with_suffix('.audit.json').read_text(encoding='utf-8'))
 rows.append({'alias':alias,'source':str(source),'copy':str(dest),'sha256':digest,'date':a['date'],'bytes':source.stat().st_size})
h.write_json(run/'rc9-recovery-extra-source-preflight.json',{'status':'ORIGINAL_BYTE_COPIES_ONLY','sources':rows})
print(json.dumps(rows,ensure_ascii=True))
