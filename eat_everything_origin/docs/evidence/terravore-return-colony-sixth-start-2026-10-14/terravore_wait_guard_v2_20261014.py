"""Independent native month accounting and safe idle-wait boundaries."""
import json,logging,math,sys
start,end=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a,b=[read_state(run,s) for s in (start,end)]
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
cash=('energy','minerals','alloys','unity','trade','rare_crystals')
budget=bc['budget_categories']['current_month']
net={k:sum(float(v.get(k,0)) for v in budget['income'].values())-sum(float(v.get(k,0)) for v in budget['expenses'].values()) for k in cash}
delta={k:float(bc['effective_stockpile'].get(k,0))-float(ac['effective_stockpile'].get(k,0)) for k in cash}
residual={k:delta[k]-net[k] for k in cash}
lost=set(a['ships'])-set(b['ships']);born=set(b['ships'])-set(a['ships'])
ship_checks=[]
for sid in set(a['ships'])&set(b['ships']):
 old,new=q.scalars(a['ships'][sid]),q.scalars(b['ships'][sid])
 checks=[q.block(a['ships'][sid],'ship_design_implementation')==q.block(b['ships'][sid],'ship_design_implementation')]
 checks += [old.get(k)==new.get(k) for k in ('max_hitpoints','max_shield_hitpoints','max_armor_hitpoints','construction_date')]
 for hp,mx in [('hitpoints','max_hitpoints'),('shield_hitpoints','max_shield_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
  ov,nv,maximum=old.get(hp,0),new.get(hp,0),new.get(mx,0)
  checks.append(all(isinstance(x,(float,int)) and math.isfinite(x) for x in (ov,nv,maximum)) and -0.001<=nv<=maximum+0.001 and nv+0.001>=ov)
 ship_checks.append(all(checks))
def armies(s):return {k:v for k,v,x in q.fields(s['roots']['army']) if x and q.scalars(v).get('owner')==0}
aa,ba=armies(a),armies(b)
army_born={k:q.scalars(v) for k,v in ba.items() if k not in aa}
items_a={k:v for k,v in a['items'].items() if q.scalars(v).get('paying_country')==0}
items_b={k:v for k,v in b['items'].items() if q.scalars(v).get('paying_country')==0}
done=set(items_a)-set(items_b)
new_messages=[q.scalars(v) for v in b['messages'] if v not in a['messages']]
new_tech=set(bc['completed_technologies'])-set(ac['completed_technologies'])
pop_delta={str(cid):b['audit']['colonies'][str(cid)]['actual_pop_sum']-a['audit']['colonies'][str(cid)]['actual_pop_sum'] for cid in ac['owned_colonies'] if str(cid) in b['audit']['colonies']}
planets=[q.scalars(q.block(q.block(s['roots']['planets'],'planet'),'544')) for s in (a,b)]
checks={
 'native_month_sources':b['audit']['date'].endswith('.01') and all(h.sha256(run/(s+'.sav'))==v['audit']['save_sha256'] for s,v in [(start,a),(end,b)]),
 'six_cash_exact_month_and_solvent':all(abs(v)<0.001 for v in residual.values()) and all(bc['effective_stockpile'].get(k,0)>=0 for k in cash),
 'mod_crisis_and_colonial_identity_held':ac['variables']==bc['variables'] and ac['owned_colonies']==bc['owned_colonies']==[0,40] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression') and all(p.get('owner')==p.get('controller')==0 and p.get('colony')==40 and p.get('bombardment_damage',0)==0 for p in planets),
 'old_ships_retained_repaired_and_unmodified':not lost and all(ship_checks),
 'paid_army_birth_accounted':set(aa)<=set(ba) and not (set(items_b)-set(items_a)) and len(army_born)==len(done)==len(born) and all(v.get('type')=='assault_army' and v.get('species')==73 and str(v.get('ship')) in born and q.scalars(b['ships'][str(v['ship'])]).get('army')==int(k) and q.scalars(b['fleets'][str(q.scalars(b['ships'][str(v['ship'])])['fleet'])]).get('ship_class')=='shipclass_transport' and a['audit']['date']<=q.scalars(b['ships'][str(v['ship'])])['construction_date']<b['audit']['date'] for k,v in army_born.items()) and all(q.scalars(q.block(items_a[k],'resources'))=={'minerals':100} and q.scalars(q.block(items_a[k],'buildable_army')).get('army_type')=='assault_army' and q.scalars(q.block(items_a[k],'buildable_army')).get('planet')==0 for k in done),
 'population_natural_and_no_pending_or_errors':all(0<=v<=200 for v in pop_delta.values()) and not b['pending'] and (run/(end+'-error-before.log')).read_bytes()==(run/(end+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes(),
}
boundaries=[]
if born and not any(q.scalars(v).get('type')=='assault_army' for v in aa.values()):boundaries.append('paid_army_birth_needs_UI_review')
if new_messages:boundaries.append('new_native_messages')
if new_tech:boundaries.append('native_research_completed')
if 'colonizing_species' not in q.scalars(q.block(b['roots']['colony'],'40')):boundaries.append('colony_completion')
if bc['effective_stockpile']['minerals']<700:boundaries.append('mineral_supply')
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'date':b['audit']['date'],'calendar_ready':all(checks.values()) and not boundaries,'boundaries':boundaries,'cash_delta':delta,'current_month_net':net,'residual':residual,'population_delta':pop_delta,'lost_ships':sorted(lost),'born_ships':sorted(born),'born_armies':army_born,'completed_paid_items':sorted(done),'new_messages':new_messages,'new_tech':sorted(new_tech)}
out=run/(end+'-wait-v2-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof,ensure_ascii=False),flush=True)
sys.exit(0 if proof['pass'] else 1)
