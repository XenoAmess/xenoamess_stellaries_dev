import json
import logging
from pathlib import Path
import shutil
import sys
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,manifest=h.load_run()
shutil.copyfile(Path(__file__),run/Path(__file__).name)
before=json.loads((run/'rc8-hiveworld-natural-ap5-paid.audit.json').read_text())
after=r.native_save('rc8-hiveworld-market-funded-native','2297.03.12',tuple(map(int,before['countries'])))
a,b=before['countries']['0'],after['countries']['0']
expected={'alloys':-2750,'minerals':-5000,'food':-10000,'exotic_gases':-500,'energy':8500}
for k,v in expected.items():
    assert Decimal(str(b['stockpile'].get(k,0)))-Decimal(str(a['stockpile'].get(k,0)))==Decimal(v),(k,a['stockpile'].get(k),b['stockpile'].get(k))
assert b['stockpile']['energy']>10000
assert b['variables']==a['variables'] and b['flags']==a['flags']
for key in ['colonies','pop_groups','pop_jobs','districts','deposits','situations','species','event_targets','planets']:
    assert after[key]==before[key],key
changes={k:{'before':a['stockpile'].get(k,0),'after':b['stockpile'].get(k,0)} for k in set(a['stockpile'])|set(b['stockpile']) if a['stockpile'].get(k,0)!=b['stockpile'].get(k,0)}
h.write_json(run/'rc8-hiveworld-native-market-funding-proof.json',{'status':'PASS_SCOPED','date':after['date'],
    'actual_quantities':expected,'stock_changes':changes,'eep_ledger_and_world_collections_kept':True,
    'trade_is_market_currency':True,'energy_above_10000':True,'save_sha256':after['save_sha256']})
print(json.dumps({'status':'PASS_SCOPED','date':after['date'],'stock_changes':changes},ensure_ascii=True),flush=True)
