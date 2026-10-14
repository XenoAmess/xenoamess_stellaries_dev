"""The new5000 normal mineral purchase uses its actual quote and saved payment."""
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
a,b=[read_state(run,s) for s in ('hope-route-wait-native-22960601','hope-route-jun96-market-native-22960601')]
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
delta={k:float(bc['effective_stockpile'].get(k,0))-float(ac['effective_stockpile'].get(k,0)) for k in set(ac['effective_stockpile'])|set(bc['effective_stockpile'])}
quote=json.loads((run/'hope-route-jun96-market-quote5000.ocr.json').read_text('utf-8'))
labels=[row['text'] for row in quote['rows']]
execution=json.loads((run/'hope-route-jun96-market-buy5000-20261014-execution.json').read_text('utf-8'))
checks={
 'same_paused_day_bound_quote_and_payment':a['audit']['date']==b['audit']['date']=='2296.06.01' and execution['returncode']==0 and h.sha256(Path(execution['command'][1]))==execution['helper_sha256'] and quote['image_sha256']==h.sha256(run/'hope-route-jun96-market-quote5000.jpg') and any('5000.00' in label for label in labels) and any('17308' in label for label in labels),
 '5000_minerals_exact_and_actual_trade_quote':abs(delta['minerals']-5000)<1e-4 and abs(delta['trade']+17308)<1 and all(abs(v)<1e-4 for k,v in delta.items() if k not in ('minerals','trade')) and bc['effective_stockpile']['trade']>=0,
 'mod_crisis_and_digest_held':ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['situations']==b['audit']['situations'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'population_ships_armies_orders_held':a['audit']['colonies']==b['audit']['colonies'] and a['ships']==b['ships'] and a['fleets']==b['fleets'] and a['roots']['army']==b['roots']['army'] and a['items']==b['items'],
 'pending_messages_errors_held':a['pending']==b['pending']==[] and a['messages']==b['messages'] and (run/'hope-route-jun96-market-native-22960601-error-before.log').read_bytes()==(run/'hope-route-jun96-market-native-22960601-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'calendar_ready':all(checks.values()),'payment':delta,'stockpile':bc['effective_stockpile']}
out=run/'hope-route-jun96-market-native-22960601-payment-proof.json'
assert not out.exists()
h.write_json(out,proof)
print(json.dumps(proof),flush=True)
sys.exit(0 if proof['pass'] else 1)
