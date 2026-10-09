"""Exact original survey FAIL supplement: departing orbit link only, no replay."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-synchronicity-kinship-paid';after='terravore-survey-auto-enabled'
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 roots={k:v for k,v,o in q.fields(t) if o};planets={k:v for k,v,o in q.fields(q.block(roots['planets'],'planet')) if o}
 return a,roots,planets
b,br,bp=read(before);a,ar,ap=read(after)
original=json.loads((run/(after+'-survey-order-proof.json')).read_text('utf-8'))
bf,af=q.block(br['fleet'],'1'),q.block(ar['fleet'],'1')
checks={
 'bound_original_exact_one_FAIL_and_other29_true':original['status']=='FAIL' and len(original['checks'])==30 and [k for k,v in original['checks'].items() if not v]==['planets_root_raw_held'],
 'bound_original_SHA_pair':original['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and original['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'same_actual_date':b['date']==a['date']=='2221.01.02',
 'planet_root_outer_fields_raw_held':[(k,v,o) for k,v,o in q.fields(br['planets']) if k!='planet']==[(k,v,o) for k,v,o in q.fields(ar['planets']) if k!='planet'],
 'all_planet_IDs_held_only164_raw_changed':set(bp)==set(ap) and [k for k in bp if bp[k]!=ap[k]]==['164'],
 'planet164_only_orbital_reference_field_changed':[(k,v,o) for k,v,o in q.fields(bp['164']) if k!='planet_orbitals']==[(k,v,o) for k,v,o in q.fields(ap['164']) if k!='planet_orbitals'],
 'exact_old_fleet1_reference_removed':q.scalars(q.block(bp['164'],'planet_orbitals'))=={'0':1} and not q.block(ap['164'],'planet_orbitals').strip(),
 'bind_old_fleet1_orbit164_new_empty':q.scalars(q.block(q.block(q.block(bf,'movement_manager'),'orbit'),'orbitable'))=={'planet':164} and not q.block(q.block(af,'movement_manager'),'orbit').strip()
}
p={'status':'PASS_EXACT_NATIVE_SURVEY_ORBIT_REFERENCE_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Only original survey order planets FAIL: the exact old fleet1 orbital reference is removed. Original 30-check FAIL remains; not an arrival, second source or full route.'}
out=run/(after+'-survey-orbit-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original supplement FAIL retained; no next calendar'
