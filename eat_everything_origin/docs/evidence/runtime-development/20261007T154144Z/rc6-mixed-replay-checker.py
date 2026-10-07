import copy
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261007T154144Z')
names=['rc6-mixed-native20-generic20-same-country-completed','rc6-mixed-native20-generic20-after-five-replays']
a=json.loads((run/(names[0]+'.all-countries.audit.json')).read_text(encoding='utf-8'))
b=q.audit(run/(names[1]+'.sav'),tuple(int(i) for i in a['countries']))
out=run/(names[1]+'.all-countries.audit.json')
assert not out.exists()
out.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]


def check(name,actual,expected):
    import hashlib
    def evidence(value):
        encoded=json.dumps(value,ensure_ascii=False,sort_keys=True).encode('utf-8')
        return value if len(encoded)<1400 else {'full_canonical_json_sha256':hashlib.sha256(encoded).hexdigest(),'json_bytes':len(encoded),'full_inputs':'retained native SAV and all-countries audits'}
    checks.append({'check':name,'status':'PASS' if actual==expected else 'FAIL','actual':evidence(actual),'expected':evidence(expected)})


check('same_date',[a['date'],b['date']],['2204.01.02']*2)
for f in ['colonies','pop_groups','pop_jobs','deposits','districts','species','event_targets','situations']:
    check('full_'+f+'_unchanged',b[f],a[f])
foreign=[i for i in a['countries'] if i!='0']
check('all36_foreign_complete_audit_unchanged',{i:b['countries'][i] for i in foreign},{i:a['countries'][i] for i in foreign})
raws=[]
for name in names:
    with zipfile.ZipFile(run/(name+'.sav')) as z:
        s=z.read('gamestate').decode('utf-8-sig')
    raws.append({i:v for i,v,o in q.fields(q.block(s,'country')) if o and i!='0'})
check('all36_foreign_raw_country_blocks_unchanged',raws[1],raws[0])
ac,bc=[copy.deepcopy(x['countries']['0']) for x in (a,b)]
for k,old,new in [('eep_tasks',1,0),('eep_stage',0,1),('eep_chunks',0,18),('eep_g_remainder',0,2)]:
    check('exact_known_display_cache_'+k,[ac['variables'].pop(k),bc['variables'].pop(k)],[old,new])
check('exact_notice_pending_consumed',[ac['flags'].pop('eep_notice_pending'),'eep_notice_pending' in bc['flags']],[62842584,False])
check('exact_first_notice_receipt',['eep_first_notice' in ac['flags'],bc['flags'].pop('eep_first_notice')],[False,62842584])
check('all_other_original_country_fields_unchanged',bc,ac)
ap,bp=[copy.deepcopy(x['planets']) for x in (a,b)]
for k,old,new in [('eep_actual_pop',5200,6337),('eep_free_districts',9,18)]:
    check('exact_known_core_display_'+k,[ap['8']['variables'].pop(k),bp['8']['variables'].pop(k)],[old,new])
check('all_other_physical_fields_unchanged',bp,ap)
result={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','checks':checks,'version':'0.2.0-rc.6','language':'l_simp_chinese',
        'saves':{n:x['save_sha256'] for n,x in zip(names,(a,b),strict=True)},
        'scope':'Five same-day replay requests after same-country mixed settlement. All37-country audited population/job/economic/physical/task collections and all36 foreign raw country blocks compared. Only exact known Queen/display fields allowed; C40/G20/D12/made300, stocks and all real population preserved. Killed tasks are not claimed as valid active callbacks; no full Mod acceptance claim.'}
dest=run/'rc6-mixed-same-country-five-replays-all-foreign-proof.json'
assert not dest.exists()
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c['check'] for c in checks if c['status']=='FAIL']}))
