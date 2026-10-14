"""Two real paid fleets, native waypoint80 orders, no assets or date changed."""
import json,logging,re,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a,b=[read_state(run,s) for s in ('hope-route-wait-native-22970201','hope-route-feb97-main80-native-22970201')]
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
fleets=('50332250','917')
orders={fid:q.block(b['fleets'][fid],'current_order') for fid in fleets}
routes={}
for fid in fleets:
 path=q.block(q.block(b['fleets'][fid],'movement_manager'),'path')
 parts=re.findall(r'\borigin=(\d+)',path)
 routes[fid]={'route':[v for i,v in enumerate(parts) if i==0 or v!=parts[i-1]],'ETA':q.scalars(path).get('date')}
base=q.scalars(q.block(q.block(b['roots']['starbase_mgr'],'starbases'),'169'))
executions=[json.loads((run/(s+'-execution.json')).read_text('utf-8')) for s in ('hope-route-feb97-main2-march80-20261014','hope-route-feb97-main3-march80-20261014')]
checks={
 'same_date_and_bound_normal_orders':a['audit']['date']==b['audit']['date']=='2297.02.01' and h.sha256(run/'hope-route-feb97-main80-native-22970201.sav')==b['audit']['save_sha256'] and all(e['returncode']==0 and h.sha256(Path(e['command'][1]))==e['helper_sha256'] for e in executions),
 'both_reachable_owned80_avoid33':str(base['station']) in b['ships'] and all('origin=80' in orders[fid] and 'can_reach=yes' in orders[fid] and routes[fid]['route'][0]=='39' and routes[fid]['route'][-1]=='80' and '33' not in routes[fid]['route'] and omit(a['fleets'][fid],{'movement_manager','order_id','current_order','order'})==omit(b['fleets'][fid],{'movement_manager','order_id','current_order','order'}) for fid in fleets),
 '23_main_ships_and_other_assets_held':a['ships']==b['ships'] and len(q.ids(q.block(b['fleets']['50332250'],'ships')))==14 and len(q.ids(q.block(b['fleets']['917'],'ships')))==9 and all(v==b['fleets'][fid] for fid,v in a['fleets'].items() if fid not in fleets) and a['items']==b['items'] and a['roots']['army']==b['roots']['army'],
 'cash_population_digest_mod_crisis_held':ac['effective_stockpile']==bc['effective_stockpile'] and ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['colonies']==b['audit']['colonies'] and a['audit']['situations']==b['audit']['situations'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'messages_pending_errors_held':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-feb97-main80-native-22970201-error-before.log').read_bytes()==(run/'hope-route-feb97-main80-native-22970201-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'routes':routes,'orders':orders,'calendar_ready':all(checks.values())}
out=run/'hope-route-feb97-main80-native-22970201-orders-proof.json'
assert not out.exists()
h.write_json(out,proof)
print(json.dumps(proof),flush=True)
sys.exit(0 if proof['pass'] else 1)
