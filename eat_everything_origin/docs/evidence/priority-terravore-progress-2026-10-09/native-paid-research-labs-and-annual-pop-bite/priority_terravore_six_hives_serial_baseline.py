"""Bind exact six-order PASS and the new serial monthly contract before clock."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();stage='terravore-hive8-paid-order';load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
p=load(stage+'-six-paid-hives-proof.json');x=load(stage+'-six-hives-guard-execution.json');a=load(stage+'.audit.json')
contract=Path(__file__).with_name('priority_terravore_six_hives_serial_month_guard.py');dest=run/contract.name
if dest.exists():assert dest.read_bytes()==contract.read_bytes()
else:dest.write_bytes(contract.read_bytes())
checks={
 'six_paid_orders9PASS_actual0_and_source_SHA':len(p['checks'])==9 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(run/'priority_terravore_six_hives_paid_order_guard.py')=='af27c98f5093b921237921eb7a114d9e99efc9ce2825f89f1c2355e8bf13cb1f',
 'original_PAUSED_April1_native_save_bound':a['date']=='2281.04.01' and a['save_sha256']==p['after_sha256']==h.sha256(run/(stage+'.sav'))=='9a547b65efc28afd3063a1468c38e6642205ec705cf4a505cb7ce9ce7c3f4b2b',
 'serial_contract_source_preserved_and_prior18_checks_retained':h.sha256(contract)==h.sha256(dest) and contract.read_text('utf-8').count("':")>=18 and 'paid_engineering_work42_only_owned_assets_held' in contract.read_text('utf-8'),
 'original_production_CN_error_and_native_sources_held':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in p['sources']),
}
passed=all(v is True for v in checks.values());out=run/(stage+'-serial-baseline-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_SIX_HIVES_SERIAL_BASELINE' if passed else 'FAIL','checks':checks,'after_sha256':a['save_sha256'],'date':a['date'],'contract_sha256':h.sha256(contract),'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':30 if passed else 0,'scope':'Exactly one next normal30day construction/research month; no construction completion or route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
