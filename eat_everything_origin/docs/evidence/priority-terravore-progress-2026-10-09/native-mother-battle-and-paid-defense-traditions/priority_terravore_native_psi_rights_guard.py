"""Exact raw native species rights cloning for the already paid hive adoption."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before,after='terravore-unity-theory-complete','terravore-native-psi-adopted'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,q.block(q.block(t,'country'),'0')
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def anonymous(t):
 out=[];depth=0;start=None
 for token,before,after in q.tokens(t):
  if token=='{':
   if depth==0:start=after
   depth+=1
  elif token=='}':
   assert depth>0;depth-=1
   if depth==0:out.append(q.scalars(t[start:before]))
  elif depth==0:raise ValueError('Expected anonymous rights object')
 assert depth==0
 return out
b,bc=read(before);a,ac=read(after);bm,am=[q.block(c,'modules') for c in [bc,ac]]
br,ar=[q.block(c,'standard_species_rights_module') for c in [bm,am]]
bp,ap=[q.scalars(q.block(t,'primary')) for t in [br,ar]]
rights=anonymous(q.block(ar,'species_rights'));old,new=3321888769,66
pre=json.loads((run/(after+'-psi-adoption-proof.json')).read_text('utf-8'))
checks={
 'bound_adoption25_PASS_exit0':pre['status']=='PASS_NATIVE_TERRAVORE_PSI_ADOPTION_COMPONENT' and len(pre['checks'])==25 and all(pre['checks'].values()) and pre['before_sha256']==b['save_sha256'] and pre['after_sha256']==a['save_sha256'] and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==0,
 'actual_original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'default_and_robot_rights_all_raw_held':omit(br,{'primary','species_rights'})==omit(ar,{'primary','species_rights'}),
 'primary_only_species_index_changed':bp['species_index']==old and ap=={**bp,'species_index':new},
 'old_rights_list_absent_two_exact_native_copies':not q.block(br,'species_rights').strip() and len(rights)==2 and {v['species_index'] for v in rights}=={old,new} and all(v=={**bp,'species_index':v['species_index']} for v in rights),
 'full_native_hive_rights_preserved':all(ap[k]==v for k,v in {'living_standard':'living_standard_hive_mind','citizenship':'citizenship_full','military_service':'military_service_full','population_control':'population_control_no','colonization_control':'colonization_control_no','migration_control':'migration_control_no'}.items()),
 'other_modules_except_reported_economy_raw_held':omit(bm,{'standard_species_rights_module','standard_economy_module'})==omit(am,{'standard_species_rights_module','standard_economy_module'}),
 'default_species_only_exact_old_new_map':not q.block(bc,'default_species').strip() and q.scalars(q.block(ac,'default_species'))=={str(old):new},
 'actual_banks_and_tech_specials_held':all(b['countries']['0'][k]==a['countries']['0'][k] for k in ['tech_status','research_stockpile','research_progress_by_tech']),
}
p={'status':'PASS_NATIVE_TERRAVORE_PSI_RIGHTS_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'primary_before_after':[bp,ap],'exact_native_rights':rights,'scope':'Exact native old/new species rights copies and primary rights only; no native event, calendar or full-route claim.'}
out=run/'terravore-native-psi-rights-proof.json';assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original rights FAIL retained'
