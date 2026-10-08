import json,shutil,sys,zipfile
from pathlib import Path
stem=sys.argv[1];sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
p=Path('_runtime/heart-of-devouring/runs/20261008T003349Z');copy=p/Path(__file__).name
if not copy.exists():shutil.copyfile(Path(__file__),copy)
assert copy.read_bytes()==Path(__file__).read_bytes()
a=q.audit(p/(stem+'.sav'),(0,16777244))
(p/(stem+'-all-actors.audit.json')).write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(p/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
f=q.block(q.block(t,'fleet'),'50331809');w=q.block(q.block(q.block(t,'planets'),'planet'),'84');co=q.block(q.block(t,'colony'),'24')
co_s=q.scalars(co);actor=a['countries']['16777244'];root=a['countries']['0']
obs={'status':'OBSERVED_ONLY','date':a['date'],'save_sha256':a['save_sha256'],
 'player_raw':q.block(t,'player'),'fleet_raw':f,'source_raw':w,'colony_raw':co,
 'source_population':sum(q.scalars(q.block(q.block(t,'pop_groups'),str(i)))['size'] for i in q.ids(q.block(co,'pop_groups'))),
 'source_colony_present':bool(co),
 'source_devastation':q.scalars(w).get('bombardment_damage',0),
 'source_last_bombardment':q.scalars(w).get('last_bombardment'),
 'actor_unity':actor['stockpile'].get('unity',0),'actor_owned_colonies':actor['owned_colonies'],
 'actual_ship_count':len(q.ids(q.block(f,'ships'))),
 'actual_orbit':q.block(q.block(f,'movement_manager'),'orbit'),
 'current_order':q.block(f,'current_order'),
 'root_ledger':{k:root['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']},
 'root_flags':root['flags'],'root_owned_colonies':root['owned_colonies'],
 'situations':a['situations'],
 'scope':'Read-only actual native-state observation; no result acceptance is assigned.'}
(p/(stem+'-firestorm-observation.json')).write_text(json.dumps(obs,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in obs.items() if not k.endswith('_raw') and k not in ['root_flags','situations']},ensure_ascii=True))
