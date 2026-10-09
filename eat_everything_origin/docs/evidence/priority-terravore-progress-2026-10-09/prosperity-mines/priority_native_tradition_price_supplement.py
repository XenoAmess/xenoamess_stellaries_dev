"""Exact first decimal native tradition payment; original integer FAIL retained."""
import json,logging,shutil,sys
from decimal import Decimal as D,ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-paid-economy-stable-month';after='terravore-polytechnic-paid'
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'));p=json.loads((run/(after+'-paid-tradition-proof.json')).read_text('utf-8'))
cost=D(str(b['countries']['0']['effective_stockpile']['unity']))-D(str(a['countries']['0']['effective_stockpile']['unity']))
checks={'original_unique_integer_cost_FAIL':p['status']=='FAIL' and [k for k,v in p['checks'].items() if not v]==['actual_displayed_unity_cost_paid'],
 'original_SHA_pair_bound':h.sha256(run/(before+'.sav'))==b['save_sha256']==p['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==p['after_sha256'],
 'exact_actual_decimal_cost':cost==D('202.98709'),
 'exact_UI_ceiling203':cost.to_integral_value(rounding=ROUND_CEILING)==203,
 'all_other_original12_true':len(p['checks'])==13 and sum(p['checks'].values())==12}
out={'status':'PASS_SCOPED_NATIVE_DECIMAL_TRADITION_PRICE' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_cost':str(cost),'displayed_UI_cost':203,'scope':'Exact first observed decimal payment and its integer display only. Original FAIL preserved; no engine rounding universality or full route claim.'}
dest=run/(after+'-decimal-price-supplement.json');assert not dest.exists();h.write_json(dest,out);print(json.dumps(out),flush=True);assert all(checks.values())
