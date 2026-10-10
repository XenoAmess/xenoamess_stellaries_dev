"""Read-only native building completion and filled coordinator jobs component."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,building,zone=sys.argv[1:];zone=str(int(zone))
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
 zids=[]
 for d in a['colonies']['0']['districts']:
  zids.extend(str(i) for i in a['districts'][str(d)]['zones'] if i!=4294967295)
 zones={i:q.block(roots['zones'],i) for i in zids}
 buildings={i:{str(j):q.block(roots['buildings'],str(j)) for j in q.ids(q.block(v,'buildings'))} for i,v in zones.items()}
 cons=roots['construction'];queue=q.block(q.block(q.block(cons,'queue_mgr'),'queues'),'0')
 orders={str(i):q.block(q.block(q.block(cons,'item_mgr'),'items'),str(i)) for i in q.ids(q.block(queue,'items'))}
 return a,zones,buildings,orders
b,bz,bb,bo=read(before);a,az,ab,ao=read(after)
wait=json.loads((run/(after+'-paid-wait-v2-proof.json')).read_text('utf-8'))
added={i:{j:v for j,v in bs.items() if j not in bb.get(i,{})} for i,bs in ab.items()}
new=[(i,j,v) for i,bs in added.items() for j,v in bs.items()]
def coordinator(a):
 jobs=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='coordinator'];assert len(jobs)==1
 return jobs[0]
bj,aj=coordinator(b),coordinator(a)
checks={
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'bound_wait20_PASS':wait['status']=='PASS_TERRAVORE_PAID_CONSTRUCTION_WAIT_COMPONENT' and all(wait['checks'].values()) and wait['before_sha256']==b['save_sha256'] and wait['after_sha256']==a['save_sha256'],
 'same_original_mother_zones':set(bz)==set(az) and zone in bz,
 'all_original_mother_buildings_raw_held':all(ab.get(i,{}).get(j)==v for i,bs in bb.items() for j,v in bs.items()),
 'exact_one_new_requested_building_in_zone':len(new)==1 and new[0][0]==zone and q.scalars(new[0][2]).get('type')==building,
 'other_mother_zone_raw_held':all(az[i]==v for i,v in bz.items() if i!=zone),
 'target_zone_other_fields_held':[(k,v,o) for k,v,o in q.fields(bz[zone]) if k!='buildings']==[(k,v,o) for k,v,o in q.fields(az[zone]) if k!='buildings'],
 'only_prepaid_requested_order_and_empty_final_queue':len(bo)==1 and not ao and q.scalars(q.block(next(iter(bo.values()),''),'buildable_planet_building'))=={'building':building,'planet':0,'zone':int(zone)},
 'coordinator_capacity_increased_and_full':aj['max_workforce']>bj['max_workforce'] and aj['workforce']==aj['max_workforce']
}
p={'status':'PASS_NATIVE_COMPLETED_BUILDING_AND_JOBS_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'new_mother_buildings':new,'coordinator_before_after':[bj,aj],'actual_population_before_after':[b['colonies']['0']['actual_pop_sum'],a['colonies']['0']['actual_pop_sum']],'scope':'One normally prepaid native building actually completed and coordinator jobs filled. Unity income and full civic route need separate verification.'}
out=run/(after+'-completed-building-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original completion FAIL retained; do not buy again or advance calendar'
