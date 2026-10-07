import json
from pathlib import Path
import shutil
from decimal import Decimal
run = Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
shutil.copyfile(Path(__file__), run / Path(__file__).name)
before = json.loads((run/'rc8-hiveworld-natural2297-loaded-all-countries.audit.json').read_text())
after = json.loads((run/'rc8-hiveworld-natural-ap5-paid.audit.json').read_text())
a,b = before['countries']['0'],after['countries']['0']
checks=[]
def check(name,actual,expected):
    checks.append({'check':name,'status':'PASS' if actual==expected else 'FAIL','actual':actual,'expected':expected})
check('date',after['date'],'2297.03.12')
check('legal_fifth_native_AP',b['ascension_perks'],a['ascension_perks']+['ap_hive_worlds'])
check('normal_final_tradition',b['traditions'],a['traditions']+['tr_expansion_galactic_ambition','tr_expansion_finish'])
paid=Decimal(str(a['stockpile']['unity']))-Decimal(str(b['stockpile']['unity']))
check('actual_unity_cost',str(paid),'6154.89983')
check('eep_variables',b['variables'],a['variables'])
check('eep_flags',b['flags'],a['flags'])
for key in a['stockpile']:
    if key not in ['unity','physics_research','society_research','engineering_research']:
        check('stock:'+key,b['stockpile'].get(key,0),a['stockpile'].get(key,0))
for key in ['colonies','pop_groups','pop_jobs','districts','deposits','situations','species','event_targets']:
    check('full_'+key,after[key]==before[key],True)
stock_changes={k:{'before':a['stockpile'].get(k,0),'after':b['stockpile'].get(k,0)} for k in set(a['stockpile'])|set(b['stockpile']) if a['stockpile'].get(k,0)!=b['stockpile'].get(k,0)}
result={'status':'PASS_SCOPED' if all(c['status']=='PASS' for c in checks) else 'FAIL',
        'scope':'Natural native fifth AP and actual final tradition purchase; not an assertion of all stockpiles being unchanged.',
        'date':after['date'],'countries_audited':len(after['countries']),
        'save_sha256':after['save_sha256'],'stock_changes':stock_changes,'checks':checks,
        'limitations':['Three actual research pools changed and their cause has not been independently isolated. Original integer cost assertion FAIL is preserved.']}
out=run/'rc8-hiveworld-natural-ap5-purchase-recovered-proof.json'
assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failures':[c['check'] for c in checks if c['status']!='PASS'],'stock_changes':stock_changes},ensure_ascii=True))
