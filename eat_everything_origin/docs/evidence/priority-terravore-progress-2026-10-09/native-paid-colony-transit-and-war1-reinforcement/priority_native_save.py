"""Observe a uniquely named native Chinese save; no economic or event actions."""
import json,logging,shutil,sys
from pathlib import Path
stage,date=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
assert m['version']=='0.2.0' and m['language']=='l_simp_chinese'
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
bindings=[{'path':str(p.resolve()),'sha256':h.sha256(p)} for p in
          [Path(r.__file__),Path(h.__file__),Path('eat_everything_origin/tools/audit_save.py')]]
before=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(before)
a=r.native_save(stage,date,(0,))
after=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(after)
proof={'status':'OBSERVED_NATIVE_SAVE','date':a['date'],'save_sha256':a['save_sha256'],
       'new_error_bytes':len(after)-len(before),'error_prefix_held':after.startswith(before),
       'dependency_bindings':bindings,
       'scope':'Normal unique native save only. Native legality, pending events and route acceptance require separate checks.'}
h.write_json(run/(stage+'-observation.json'),proof);print(json.dumps(proof),flush=True)
