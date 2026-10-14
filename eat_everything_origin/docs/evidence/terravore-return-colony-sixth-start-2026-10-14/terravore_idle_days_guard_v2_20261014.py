import json,logging,math,sys
start,end=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();a,b=[read_state(run,s) for s in [start,end]]
ac,bc=[s['audit']['countries']['0'] for s in [a,b]]
valid=[];hp_changes=[]
for sid in set(a['ships'])&set(b['ships']):
 av,bv=q.scalars(a['ships'][sid]),q.scalars(b['ships'][sid])
 ok=q.block(a['ships'][sid],'ship_design_implementation')==q.block(b['ships'][sid],'ship_design_implementation') and all(av.get(k)==bv.get(k) for k in ['fleet','construction_date','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
 for field,mx in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]:
  ov,nv,cap=av.get(field,0),bv.get(field,0),bv.get(mx,0)
  ok=ok and all(isinstance(x,(int,float)) and math.isfinite(x) for x in [nv,cap]) and 0<=nv<=cap+.001 and nv+.001>=ov
  if ov!=nv:hp_changes.append({'ship':sid,'field':field,'before':ov,'after':nv})
 valid.append(ok)
def army(s):return {k:v for k,v,x in q.fields(s['roots']['army']) if x and q.scalars(v).get('owner')==0}
def paid(s):return {k for k,v in s['items'].items() if q.scalars(v).get('paying_country')==0}
messages=[q.scalars(v) for v in b['messages'] if v not in a['messages']]
states={fid:{'return_date':q.scalars(b['fleets'][fid]).get('return_date'),'position':q.scalars(q.block(q.block(b['fleets'][fid],'movement_manager'),'coordinate')),'ships':q.ids(q.block(b['fleets'][fid],'ships')),'order':q.block(b['fleets'][fid],'current_order')} for fid in ['917','50332250']}
research=('physics_research','society_research','engineering_research')
monthly_tick=int(a['audit']['date'].split('.')[-1])==1 and int(b['audit']['date'].split('.')[-1])>=2
research_delta={k:bc['effective_stockpile'][k]-ac['effective_stockpile'][k] for k in research}
research_expected={k:(1.35 if monthly_tick else 0)*sum(float(v.get(k,0)) for v in bc['budget_categories']['current_month']['income'].values()) for k in research}
checks={
 'bound_same_month_original_sources':a['audit']['date'][:7]==b['audit']['date'][:7] and all(h.sha256(run/(stem+'.sav'))==s['audit']['save_sha256'] for stem,s in [(start,a),(end,b)]),
 'all_original_ships_designs_valid_repair_only':set(a['ships'])==set(b['ships']) and all(valid),
 'cash_mod_colonial_population_crisis_held':all(ac['effective_stockpile'].get(k)==bc['effective_stockpile'].get(k) for k in set(ac['effective_stockpile'])|set(bc['effective_stockpile']) if k not in research) and all(abs(research_delta[k]-research_expected[k])<.001 for k in research) and ac['completed_technologies']==bc['completed_technologies'] and ac['research_queues']==bc['research_queues'] and ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and all(a['audit']['colonies'][str(cid)]['actual_pop_sum']==b['audit']['colonies'][str(cid)]['actual_pop_sum'] for cid in [0,40]) and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'army_orders_and_no_active_combat':army(a)==army(b) and paid(a)==paid(b) and all(not q.block(q.block(v,'combat'),'in_combat_with') for v in b['fleets'].values()),
 'no_pending_and_error_held':not b['pending'] and (run/(end+'-error-before.log')).read_bytes()==(run/(end+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'calendar_ready':all(checks.values()) and not messages,'research_delta':research_delta,'research_expected':research_expected,'states':states,'HP_changes':hp_changes,'new_messages':messages}
out=run/(end+'-idle-v2-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof),flush=True);sys.exit(0 if proof['pass'] else 1)
