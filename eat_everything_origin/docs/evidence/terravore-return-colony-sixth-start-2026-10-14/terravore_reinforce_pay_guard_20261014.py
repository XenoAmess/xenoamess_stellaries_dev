"""Independently account the three normal paid reinforcements."""
import json, logging, sys
from pathlib import Path
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
a, b = [read_state(run, s) for s in ('hope-route-own-mia-sep08-native-22950908', 'hope-route-sep08-reinforce3-native-22950908')]
ac, bc = [s['audit']['countries']['0'] for s in (a, b)]
new = {k:v for k,v in b['items'].items() if k not in a['items'] and q.scalars(v).get('paying_country') == 0}
expected = dict(ac['effective_stockpile'])
expected['minerals'] -= 1237.5
orders = {}
for k,v in new.items():
    reinforcement = q.block(v, 'buildable_ship_reinforcement')
    orders[k] = {'item':q.scalars(v), 'cost':q.scalars(q.block(v, 'resources')), 'reinforcement':q.scalars(reinforcement), 'design':q.scalars(q.block(reinforcement, 'ship_design_implementation')), 'orbitable':q.scalars(q.block(reinforcement, 'orbitable'))}
executions = [json.loads((run/(s+'-execution.json')).read_text('utf-8')) for s in ('hope-route-sep08-reinforce2-pay-20261014', 'hope-route-sep08-reinforce3-pay-20261014')]
checks = {
 'same_native_date_and_bound_physical_payments':a['audit']['date'] == b['audit']['date'] == '2295.09.08' and all(e['returncode']==0 and h.sha256(Path(e['command'][1]))==e['helper_sha256'] for e in executions),
 'exact1237_5_minerals_only':all(abs(float(expected[k])-float(bc['effective_stockpile'].get(k,0)))<1e-4 for k in expected),
 'three_paid_destroyer_orders':len(new)==3 and all(v['cost']=={'minerals':412.5} and v['item']['progress']==0 and v['item']['progress_needed']==60 and v['design']=={'design':83887141,'upgrade':4294967295,'growth_stage':0} and v['reinforcement']['fleet_template'] in (33554475,268435546) and v['orbitable']['starbase'] in (153,158) and q.scalars(b['queues'][str(v['item']['queue'])]).get('owner')==0 and int(k) in q.ids(q.block(b['queues'][str(v['item']['queue'])],'items')) and int(k) in q.ids(q.block(q.block(b['templates'][str(v['reinforcement']['fleet_template'])],'all_queued'),'construction_queue_items')) for k,v in orders.items()) and sum(v['reinforcement']['fleet_template']==33554475 for v in orders.values())==1 and all(b['items'].get(k)==v for k,v in a['items'].items() if q.scalars(v).get('paying_country')==0),
 'old_assets_mod_population_crisis_held':ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['colonies']==b['audit']['colonies'] and a['ships']==b['ships'] and a['fleets']==b['fleets'] and a['roots']['army']==b['roots']['army'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'messages_pending_errors_held':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-sep08-reinforce3-native-22950908-error-before.log').read_bytes()==(run/'hope-route-sep08-reinforce3-native-22950908-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()), 'checks':checks, 'before_save_sha256':a['audit']['save_sha256'], 'after_save_sha256':b['audit']['save_sha256'], 'orders':orders, 'calendar_ready':all(checks.values())}
out=run/'hope-route-sep08-reinforce3-payment-proof.json'
assert not out.exists()
h.write_json(out,proof)
print(json.dumps(proof),flush=True)
sys.exit(0 if proof['pass'] else 1)
