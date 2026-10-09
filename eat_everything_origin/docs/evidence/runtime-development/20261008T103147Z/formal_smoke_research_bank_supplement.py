import hashlib,json,shutil,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
root=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T081542Z')
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z')
out=Path('eat_everything_origin/docs/evidence/formal-smoke-research-bank-supplement-2026-10-08.json');assert not out.exists()
shutil.copyfile(__file__,run/Path(__file__).name)
paths={hashlib.sha256(p.read_bytes()).hexdigest():p for p in root.glob('*.sav')};cache={};rows=[]
for name in ('formal-prod-intro-ack-proof.json','formal-prod-native-report-readonly-proof.json','formal-prod-report-repeat-readonly-proof.json','formal-prod-native-month-stable-reloaded-proof.json'):
 proof=root/name;original=proof.read_bytes();source=json.loads(original)
 for key in ('before_sha256','after_sha256'):
  sha=source[key]
  if sha not in cache:
   p=paths[sha];a=q.audit(p,(0,));assert a['save_sha256']==sha==hashlib.sha256(p.read_bytes()).hexdigest();cache[sha]=a
 b,a=[cache[source[key]] for key in ('before_sha256','after_sha256')];bc,ac=b['countries']['0'],a['countries']['0']
 checks={'same_native_date':b['date']==a['date'],'actual_research_banks_available':bc['research_stockpile'] is not None and ac['research_stockpile'] is not None,
  'native_three_banks_held':bc['research_stockpile']==ac['research_stockpile'],'complete_effective_stock_held':bc['effective_stockpile']==ac['effective_stockpile'],
  'complete_tech_status_held':bc['tech_status']==ac['tech_status'],'original_source_proof_bytes_held':proof.read_bytes()==original}
 rows.append({'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','original_proof':str(proof),'original_proof_sha256':hashlib.sha256(original).hexdigest(),'checks':checks,'date':a['date'],
  'before_save':b['save'],'before_sha256':b['save_sha256'],'before_gamestate_sha256':b['gamestate_sha256'],
  'after_save':a['save'],'after_sha256':a['save_sha256'],'after_gamestate_sha256':a['gamestate_sha256'],
  'before_native_bank':bc['research_stockpile'],'after_native_bank':ac['research_stockpile']})
 print(json.dumps({'proof':name,'checks':checks}),flush=True)
result={'status':'PASS_SCOPED' if all(row['status']=='PASS_SCOPED' for row in rows) else 'FAIL','schema_version':2,'audit_tool_sha256':a['audit_tool_sha256'],'rows':rows,'scope':'Read-only supplement for four critical original final-production smoke pairs; no original proof, save, production or remote content changed. Does not re-audit all historical cases.'}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert result['status']=='PASS_SCOPED'
