"""Verify the real sixth native decision without replaying it."""
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
a,b=[read_state(run,s) for s in ('hope-route-wait-native-22960201','hope-route-sixth-start-native-22960201')]
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
p=b['audit']['planets']['544']
new_situations={k:v for k,v in b['audit']['situations'].items() if k not in a['audit']['situations']}
execution=json.loads((run/'hope-route-feb96-sixth-native-decision-20261014-execution.json').read_text('utf-8'))
checks={
 'native_same_paused_day_and_bound_decision':a['audit']['date']==b['audit']['date']=='2296.02.01' and execution['returncode']==0 and h.sha256(Path(execution['command'][1]))==execution['helper_sha256'],
 '103_real_founder_seed_no_transfer_or_creation':a['audit']['colonies']['40']['actual_pop_sum']==b['audit']['colonies']['40']['actual_pop_sum']==103 and a['roots']['pop_groups']==b['roots']['pop_groups'] and a['audit']['colonies']['0']['actual_pop_sum']==b['audit']['colonies']['0']['actual_pop_sum'],
 'exact20_material48_months_native_flags':p['variables']=={'eep_q':20,'eep_old_damage':0,'eep_seed_existing':103,'eep_seed_need':-3,'eep_months':48} and all(k in p['flags'] for k in ('eep_active','eep_native','being_devoured','eep_owned_colony_event','recently_eaten_planet')) and p['flags']['recently_eaten_planet']['flag_days']==360 and 'being_devoured_modifier' in p['modifiers'] and p['deposits']==a['audit']['planets']['544']['deposits'],
 'one_new_native_situation48_months':len(new_situations)==1 and all(v.get('type')=='situation_eep_devouring' and v.get('country')==0 and v.get('progress')==0 and v.get('target',{}).get('id')==544 and v.get('approach')=='eep_devour_approach' for v in new_situations.values()),
 'no_early_cash_capacity_reward_or_ships':all(ac[k]==bc[k] for k in ('effective_stockpile','variables','owned_colonies','government','ascension_perks','traditions')) and a['ships']==b['ships'] and a['fleets']==b['fleets'] and a['items']==b['items'] and a['roots']['army']==b['roots']['army'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'no_pending_messages_errors':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-sixth-start-native-22960201-error-before.log').read_bytes()==(run/'hope-route-sixth-start-native-22960201-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'source':p,'situation':new_situations,'calendar_ready':all(checks.values())}
out=run/'hope-route-sixth-start-native-22960201-start-proof.json'
assert not out.exists()
h.write_json(out,proof)
print(json.dumps({'pass':proof['pass'],'checks':checks,'situation':new_situations}),flush=True)
sys.exit(0 if proof['pass'] else 1)
