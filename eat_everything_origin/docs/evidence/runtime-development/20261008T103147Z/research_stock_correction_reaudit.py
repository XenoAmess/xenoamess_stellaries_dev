import hashlib,json,shutil,sys
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z')
vanilla=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T090850Z')
destination=Path('eat_everything_origin/docs/evidence/research-stock-correction-2026-10-08.json')
assert not destination.exists()
shutil.copyfile(__file__,run/Path(__file__).name)
shutil.copyfile(Path(q.__file__),run/'audit_save-after-research-stock-correction.py')
originals=[run/'organic-mother-factory-ordered-proof.json',
           vanilla/'postvanilla-native-begin-proof.json']
assert all(p.exists() for p in originals)
original_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in originals}
samples={}
for root,name in ((run,'organic-psionic-theory-month36'),(run,'organic-mother-factory-ordered'),
                  (vanilla,'postvanilla-source-native-nextday'),(vanilla,'postvanilla-native-Q20-begun')):
    path=root/(name+'.sav');before=path.read_bytes();a=q.audit(path,(0,))
    assert path.read_bytes()==before
    output=run/(name+'.research-v2.audit.json');assert not output.exists()
    output.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    samples[name]=a
b,a=[samples[n] for n in ('organic-psionic-theory-month36','organic-mother-factory-ordered')]
bc,ac=b['countries']['0'],a['countries']['0']
colony_changes={i:{k:[b['colonies'].get(i,{}).get(k),v] for k,v in c.items()
                   if b['colonies'].get(i,{}).get(k)!=v}
                for i,c in a['colonies'].items() if c!=b['colonies'].get(i)}
checks={'same_actual_date':b['date']==a['date']=='2294.12.02',
        'actual_minerals_paid400':Decimal(str(bc['effective_stockpile']['minerals']))-
                                    Decimal(str(ac['effective_stockpile']['minerals']))==400,
        'all_other_effective_stock_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}==
                                       {k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
        'native_three_research_banks_held':bc['research_stockpile']==ac['research_stockpile'] and bc['research_stockpile'] is not None,
        'raw_tech_status_held':bc['tech_status']==ac['tech_status'],
        'research_queues_held':bc['research_queues']==ac['research_queues'],
        'per_tech_progress_held':bc['research_progress_by_tech']==ac['research_progress_by_tech'],
        'only_expected_colony_last_building_changed':colony_changes=={'0':{'last_building_changed':['building_temple','building_factory_1']}},
        'all_original_failure_bytes_held':all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in original_hashes.items())}
for key in ('variables','flags','completed_technologies','traditions','ascension_perks','government'):
    checks[key+'_held']=bc[key]==ac[key]
for key in ('pop_groups','pop_jobs','planets','districts','deposits','situations','species'):
    checks[key+'_held']=b[key]==a[key]
vb,va=[samples[n] for n in ('postvanilla-source-native-nextday','postvanilla-native-Q20-begun')]
vbc,vac=vb['countries']['0'],va['countries']['0']
vchecks={'same_native_date':vb['date']==va['date']=='2200.01.02',
         'native_three_research_banks_held':vbc['research_stockpile']==vac['research_stockpile'] and vbc['research_stockpile'] is not None,
         'complete_effective_stocks_held':vbc['effective_stockpile']==vac['effective_stockpile'],
         'raw_tech_status_held':vbc['tech_status']==vac['tech_status'],
         'cached_mirror_initialization_observed':all(k not in vbc['stockpile'] and vac['stockpile'][k]==vac['research_stockpile'][k] for k in q.RESEARCH_RESOURCES),
         'no_EEP_variables_or_flags':not vbc['variables'] and not vac['variables'] and not vbc['flags'] and not vac['flags']}
result={'status':'PASS_SCOPED' if all(checks.values()) and all(vchecks.values()) else 'FAIL',
        'auditor_sha256':a['audit_tool_sha256'],'schema_version':2,
        'original_auditor_sha256':hashlib.sha256((run/'audit_save-before-research-stock-correction.py').read_bytes()).hexdigest(),
        'original_failure_file_hashes':original_hashes,
        'factory':{'checks':checks,'colony_changes':colony_changes,
                   'actual_research_bank_before':bc['research_stockpile'],'actual_research_bank_after':ac['research_stockpile'],
                   'raw_mirror_before':{k:bc['stockpile'].get(k) for k in q.RESEARCH_RESOURCES},
                   'raw_mirror_after':{k:ac['stockpile'].get(k) for k in q.RESEARCH_RESOURCES}},
        'true_no_mod_decision':{'checks':vchecks,'actual_research_bank':vac['research_stockpile']},
        'original_saves':{n:{'path':a['save'],'save_sha256':a['save_sha256'],'gamestate_sha256':a['gamestate_sha256']} for n,a in samples.items()},
        'scope':'Read-only re-audit of these two original pairs. No historical FAIL is overwritten or generalized to other pairs. No game mutation; published production unchanged.'}
destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'factory_checks':checks,'vanilla_checks':vchecks}),flush=True)
assert result['status']=='PASS_SCOPED'
