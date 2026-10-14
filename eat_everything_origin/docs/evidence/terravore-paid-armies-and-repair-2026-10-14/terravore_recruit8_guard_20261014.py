import json,logging,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a=read_state(run,'hope-route-mar22-return2-native-22940322')
b=read_state(run,'hope-route-mar22-recruit8-native-22940322')
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
e=json.loads((run/'hope-route-mar22-recruit8-20261014-execution.json').read_text('utf-8'))
new={k:v for k,v in b['items'].items() if k not in a['items']}
expected=dict(ac['effective_stockpile']);expected['minerals']-=800
checks={
 'bound_same_date_native_payment':a['audit']['date']==b['audit']['date']=='2294.03.22' and e['returncode']==0 and h.sha256(Path(e['command'][1]))==e['helper_sha256'],
 'exact800_minerals_only':all(abs(float(expected[k])-float(bc['effective_stockpile'].get(k,0)))<1e-4 for k in expected) and ac['budget']==bc['budget'],
 'eight_paid_founder_assault_orders':len(new)==8 and all(q.scalars(v)=={'queue':1,'paying_country':0,'progress':0,'progress_needed':90} and q.scalars(q.block(v,'resources'))=={'minerals':100} and q.scalars(q.block(v,'buildable_army'))=={'army_type':'assault_army','species':73,'planet':0,'starbase':4294967295} for v in new.values()) and all(b['items'].get(k)==v for k,v in a['items'].items()),
 'mod_population_assets_crisis_held':ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['colonies']==b['audit']['colonies'] and a['ships']==b['ships'] and a['fleets']==b['fleets'] and a['roots']['army']==b['roots']['army'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'messages_pending_errors_held':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-mar22-recruit8-native-22940322-error-before.log').read_bytes()==(run/'hope-route-mar22-recruit8-native-22940322-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'army_item_ids':list(new),'calendar_ready':all(checks.values())}
out=run/'hope-route-mar22-recruit8-guard-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof),flush=True)
sys.exit(0 if proof['pass'] else 1)
