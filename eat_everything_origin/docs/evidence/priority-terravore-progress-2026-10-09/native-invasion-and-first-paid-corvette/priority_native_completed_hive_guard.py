"""Read-only native hive district completion, existing buildings and actual jobs."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 roots={k:v for k,v,o in q.fields(t) if o}
 zones={str(z):q.block(roots['zones'],str(z)) for d in a['colonies']['0']['districts'] for z in a['districts'][str(d)]['zones'] if z!=4294967295}
 buildings={i:{str(j):q.block(roots['buildings'],str(j)) for j in q.ids(q.block(v,'buildings'))} for i,v in zones.items()}
 c=roots['construction'];queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0')
 orders={str(i):q.block(q.block(q.block(c,'item_mgr'),'items'),str(i)) for i in q.ids(q.block(queue,'items'))}
 levels={a['districts'][str(i)]['type']:a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts']}
 jobs={j['type']:j for j in a['pop_jobs'].values() if j['planet']==0}
 return a,zones,buildings,orders,levels,jobs
b,bz,bb,bo,bl,bj=read(before);a,az,ab,ao,al,aj=read(after)
w=json.loads((run/(after+'-paid-wait-v3-proof.json')).read_text('utf-8'))
deltas={'coordinator':40,'calculator_physicist':24,'calculator_biologist':24,'calculator_engineer':24,'fabricator':100}
checks={
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'bound_wait21_PASS':w['status']=='PASS_TERRAVORE_PAID_CONSTRUCTION_WAIT_COMPONENT' and len(w['checks'])==21 and all(w['checks'].values()) and w['before_sha256']==b['save_sha256'] and w['after_sha256']==a['save_sha256'],
 'exact_hive4_to5_other_levels_held':bl.get('district_hive')==4 and al==dict(bl,district_hive=5),
 'same_original_zones':set(bz)==set(az),
 'all_zone_building_references_and_original_buildings_held':bb==ab and all(q.block(bz[i],'buildings')==q.block(az[i],'buildings') for i in bz),
 'only_prepaid_hive_order_and_empty_final_queue':len(bo)==1 and not ao and q.scalars(q.block(next(iter(bo.values()),''),'buildable_district'))=={'district':'district_hive','planet':0} and q.scalars(next(iter(bo.values()),'')).get('progress_needed')==480 and q.scalars(q.block(next(iter(bo.values()),''),'resources'))=={'minerals':450},
 'exact_new_jobs_capacity_and_filled':all(aj[k]['max_workforce']==bj[k]['max_workforce']+d and aj[k]['workforce']==aj[k]['max_workforce'] and bj[k]['workforce']==bj[k]['max_workforce'] for k,d in deltas.items()),
 'all_other_nonmaintenance_jobs_actual_workforce_and_capacity_held':set(aj)==set(bj) and all((aj[k]['workforce'],aj[k]['max_workforce'])==(bj[k]['workforce'],bj[k]['max_workforce']) for k in bj if k not in deltas and k!='maintenance_drone')
}
p={'status':'PASS_NATIVE_COMPLETED_HIVE_AND_FILLED_JOBS_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_district_levels_before_after':[bl,al],'actual_jobs_before_after':[{k:j[k] for k in j if k in deltas or k=='maintenance_drone'} for j in [bj,aj]],'actual_population_before_after':[b['colonies']['0']['actual_pop_sum'],a['colonies']['0']['actual_pop_sum']],'scope':'One normally prepaid hive district actually completed and five job capacities filled. Later actual budget and full civic route remain separate.'}
out=run/(after+'-completed-hive-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original hive completion FAIL retained; no further calendar'
