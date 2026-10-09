import hashlib,json,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
names=['organic-storm-marauder-response-ack','organic-storm-native-leader-awakened'];raw=[];sha=[]
for name in names:
    path=run/(name+'.sav');sha.append(hashlib.sha256(path.read_bytes()).hexdigest())
    with zipfile.ZipFile(path) as z:t=z.read('gamestate').decode('utf-8-sig')
    roots={k:v for k,v,o in q.fields(t) if o};raw.append(q.block(roots['leaders'],'50331766'))
old,new=raw;ot=[q.unquote(v) for k,v,o in q.fields(old) if k=='traits'];nt=[q.unquote(v) for k,v,o in q.fields(new) if k=='traits'];trait='leader_trait_psionic';clean,n=re.subn(r'\n[ \t]*traits="leader_trait_psionic"','',new)
original=json.loads((run/'organic-storm-native-leader-awakened-proof.json').read_text(encoding='utf-8'));wrong='target_exact_one_psionic_trait'
checks={'original_FAIL_preserved':original['status']=='FAIL' and original['checks'][wrong] is False,'all_other_original29_checks_true':len(original['checks'])==30 and all(v for k,v in original['checks'].items() if k!=wrong),'original_same_SHA_pair':sha==[original['before_sha256'],original['after_sha256']],'exact_one_added_trait_and_prior_sequence_held':trait not in ot and nt.count(trait)==1 and [v for v in nt if v!=trait]==ot,'target_exact_one_line_added_other_raw_held':n==1 and clean==old}
p={'status':'PASS_NATIVE_LEADER_TRAIT_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':sha[0],'after_sha256':sha[1],'native_target':50331766,'native_traits_before':ot,'native_traits_after':nt,'original_check_status':'FAIL','scope':'Read-only supplement for actual native trait insertion order; original29 other checks remain required. No event replay or new game input.'};out=run/'organic-storm-native-leader-trait-supplement-proof.json';assert not out.exists();out.write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');print(json.dumps(p),flush=True);assert all(checks.values())
