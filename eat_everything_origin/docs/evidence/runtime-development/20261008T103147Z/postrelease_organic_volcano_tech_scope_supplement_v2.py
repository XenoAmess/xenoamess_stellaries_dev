import hashlib,json,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
names=['organic-temple-year1-marauder-withdraw-ack','organic-temple-year1-dead-volcano-ack'];a=[];sha=[]
for name in names:
    p=run/(name+'.sav');sha.append(hashlib.sha256(p.read_bytes()).hexdigest());a.append(json.loads((run/(name+'.audit.json')).read_text(encoding='utf-8')))
    assert sha[-1]==a[-1]['save_sha256']
b,c=[v['countries']['0'] for v in a];old,new=b['tech_status'],c['tech_status'];original=json.loads((run/'organic-temple-year1-dead-volcano-ack-proof.json').read_text(encoding='utf-8'));wrong='last_increased_tech_volcano'
def other_fields(t):
    out=[]
    for k,v,o in q.fields(t):
        if k=='stored_techpoints_for_tech' or (k=='always_available_tech' and not o and q.unquote(v)=='tech_volcano'):continue
        if k=='alternatives':
            v=re.sub(r'\n[ \t]*"tech_volcano"','',v)
        out.append((k,v,o))
    return out
checks={'original_FAIL_preserved':original['status']=='FAIL' and original['checks'][wrong] is False,'all_original_other33_checks_true':len(original['checks'])==34 and all(v for k,v in original['checks'].items() if k!=wrong),'same_original_SHA_pair':sha==[original['before_sha256'],original['after_sha256']],'strict_full_tech_only_partial_and_two_same_option_references_changed':other_fields(old)==other_fields(new),'last_increased_tech_exactly_held':q.scalars(old)['last_increased_tech']==q.scalars(new)['last_increased_tech']=='tech_psionic_theory','exact_one_society_option_line_added':q.block(q.block(new,'alternatives'),'society').count('"tech_volcano"')==1 and '"tech_volcano"' not in q.block(q.block(old,'alternatives'),'society'),'exact_volcano1116_partial_only':c['research_progress_by_tech']==dict(b['research_progress_by_tech'],tech_volcano=1116)}
p={'status':'PASS_NATIVE_VOLCANO_EFFECT_PENDING_COST_VERIFICATION' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':sha[0],'after_sha256':sha[1],'actual_volcano_partial':1116,'original_status':'FAIL','scope':'Read-only narrow technology supplement. Native25% still requires same-date F4 cost. Original event not replayed.'};out=run/'organic-temple-year1-volcano-tech-scope-supplement-v2-proof.json';assert not out.exists();out.write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');print(json.dumps(p),flush=True);assert all(checks.values())
