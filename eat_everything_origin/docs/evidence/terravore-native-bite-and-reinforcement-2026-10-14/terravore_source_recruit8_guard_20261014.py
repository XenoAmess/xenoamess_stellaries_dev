"""Eight source-colony paid orders; original armies and Mod state held."""
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
a,b=[read_state(run,s) for s in ('hope-route-wait-native-22961201','hope-route-source-recruit8-native-22961201')]
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
execution=json.loads((run/'hope-route-source-recruit8-20261014-execution.json').read_text('utf-8'))
new={k:v for k,v in b['items'].items() if k not in a['items'] and q.scalars(v).get('paying_country')==0}
expected=dict(ac['effective_stockpile']);expected['minerals']-=800
checks={
 'same_native_date_and_normal_recorded_recruitment':a['audit']['date']==b['audit']['date']=='2296.12.01' and execution['returncode']==0 and h.sha256(Path(execution['command'][1]))==execution['helper_sha256'],
 '800_minerals_only_payment':all(abs(float(expected[k])-float(bc['effective_stockpile'].get(k,0)))<1e-4 for k in expected),
 'eight_real_source_founder_orders':len(new)==8 and all(q.scalars(v)=={'queue':2311,'paying_country':0,'progress':0,'progress_needed':90} and q.scalars(q.block(v,'resources'))=={'minerals':100} and q.scalars(q.block(v,'buildable_army'))=={'army_type':'assault_army','species':73,'planet':40,'starbase':4294967295} for v in new.values()) and q.scalars(q.block(b['queues']['2311'],'location')).get('id')==544 and set(q.ids(q.block(b['queues']['2311'],'items')))==set(map(int,new)),
 'old_armies_ships_population_digest_and_crisis_held':a['roots']['army']==b['roots']['army'] and a['ships']==b['ships'] and a['fleets']==b['fleets'] and a['audit']['colonies']==b['audit']['colonies'] and a['audit']['situations']==b['audit']['situations'] and ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression') and all(b['items'].get(k)==v for k,v in a['items'].items() if q.scalars(v).get('paying_country')==0),
 'no_messages_pending_errors':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-source-recruit8-native-22961201-error-before.log').read_bytes()==(run/'hope-route-source-recruit8-native-22961201-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'army_item_ids':list(new),'calendar_ready':all(checks.values())}
out=run/'hope-route-source-recruit8-native-22961201-payment-proof.json'
assert not out.exists()
h.write_json(out,proof)
print(json.dumps(proof),flush=True)
sys.exit(0 if proof['pass'] else 1)
