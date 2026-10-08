import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(Path(__file__),run/Path(__file__).name)
b=json.loads((run/'postvanilla-initial.audit.json').read_text(encoding='utf-8'));assert b['countries']['0']['owned_colonies']==[0];assert not any('vanilla_boundary_source' in p['flags'] for p in b['planets'].values());eb=(run/'postvanilla-create-error-before.log').read_bytes()
a=json.loads((run/'postvanilla-source-prepared.audit.json').read_text(encoding='utf-8'));sources={k:p for k,p in a['planets'].items() if 'vanilla_boundary_source' in p['flags']};assert len(sources)==1;(pid,p),=sources.items();cid=str(p['colony']);c=a['countries']['0'];total=lambda x:sum(x['colonies'][str(i)]['actual_pop_sum'] for i in x['countries']['0']['owned_colonies'])
checks={'source_single_real_colony':len(c['owned_colonies'])==2 and a['colonies'][cid]['actual_pop_sum']==100,'mother5600':a['colonies']['0']['actual_pop_sum']==5600,'total5700_conserved':total(a)==total(b)==5700,
 'natural_physical_continental_Q20':p['planet_class']=='pc_continental' and p['planet_size']==20,'source_owned0':p['owner']==0,'no_lithoid_damage':not any(a['deposits'][str(i)].get('type')=='d_lithoid_devastation' for i in p['deposits']),
 'all_stock_before_setup_same':c['stockpile']==b['countries']['0']['stockpile'],'no_EEP_country_variables':not any(k.startswith('eep_') for k in c['variables']),'no_EEP_country_flags':not any(k.startswith('eep_') for k in c['flags']),
 'no_started_situation':not a['situations'],'all_source_pops_founder_template':all(a['pop_groups'][str(i)]['key']['species']==c['native']['founder_species_ref'] for i in a['colonies'][cid]['pop_groups']),
 'no_new_errors':(user/'logs/error.log').read_bytes()==eb}
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'source_physical':int(pid),'source_colony':int(cid),'mother_physical':3,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
 'scope':'Controlled single-source builtin native colony and actual100 resettlement in true no-mod process; not natural colonization cost and not a forced progress/reward.'};h.write_json(run/'postvanilla-single-source-proof.json',v);print(json.dumps(v),flush=True);assert all(checks.values())
