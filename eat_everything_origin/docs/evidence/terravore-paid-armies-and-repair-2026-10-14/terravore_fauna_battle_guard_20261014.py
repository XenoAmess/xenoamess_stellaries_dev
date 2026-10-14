import json,logging,math,re,sys
from pathlib import Path
start,end,execution_file=sys.argv[1:]
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a,b=[read_state(run,s) for s in [start,end]]
ac,bc=[s['audit']['countries']['0'] for s in [a,b]]
pre=json.loads((run/(end+'-preflight.json')).read_text('utf-8'))
receipt=json.loads((run/(end+'-calendar-receipt.json')).read_text('utf-8'))
execution=json.loads((run/execution_file).read_text('utf-8'))
prior=json.loads((run/pre['prior_proof']).read_text('utf-8'))
ships=[{k:v for k,v,x in q.fields(s['roots']['ships']) if x} for s in [a,b]]
def enemy_ids(s):
 country=q.block(s['roots']['country'],'17')
 fids=re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(country,'fleets_manager'),'owned_fleets'))
 result=set()
 for fid in fids:
  raw=q.block(s['roots']['fleet'],fid)
  if q.scalars(q.block(q.block(raw,'movement_manager'),'coordinate')).get('origin')==33:
   result.update(str(i) for i in q.ids(q.block(raw,'ships')))
 return result
enemies=enemy_ids(a)
own_lost=set(a['ships'])-set(b['ships']);enemy_lost=enemies-set(ships[1])
own_born=set(b['ships'])-set(a['ships'])
wanted=set(a['ships'])|enemies
invalid=[];damage=[]
for sid in wanted&set(ships[1]):
 av,bv=q.scalars(ships[0][sid]),q.scalars(ships[1][sid])
 valid=q.block(ships[0][sid],'ship_design_implementation')==q.block(ships[1][sid],'ship_design_implementation') and all(av.get(k)==bv.get(k) for k in ['max_hitpoints','max_shield_hitpoints','max_armor_hitpoints','construction_date'])
 row={}
 for field,mx in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]:
  ov,nv,cap=av.get(field,0),bv.get(field,0),bv.get(mx,0)
  valid=valid and all(isinstance(x,(int,float)) and math.isfinite(x) for x in [nv,cap]) and 0<=nv<=cap+.001
  if ov!=nv:row[field]=[ov,nv,cap]
 if not valid:invalid.append(sid)
 if row:damage.append({'ship':sid,'country':'0' if sid in a['ships'] else '17','fleet':bv.get('fleet'),'hp':row})
def crisis(s):
 raw=q.block(s['country'],'crisis_progression')
 return {'path':q.scalars(raw).get('path'),'levels':[v for k,v,x in q.fields(raw) if not x and k=='level'],'objectives':{q.scalars(v)['objective']:q.scalars(v)['progress'] for k,v,x in q.fields(raw) if x and k=='objective'}}
def own_armies(s):return {k:v for k,v,x in q.fields(s['roots']['army']) if x and q.scalars(v).get('owner')==0}
ca,cb=crisis(a),crisis(b)
new_messages=[q.scalars(v) for v in b['messages'] if v not in a['messages']]
own_combat={fid:re.findall(r'fleet=(\d+)',q.block(q.block(b['fleets'].get(fid,''),'combat'),'in_combat_with')) for fid in ['917','50332250']}
checks={
 'bound_real_native_interval':prior['pass'] and prior['after_save_sha256']==a['audit']['save_sha256']==pre['start_sha256'] and receipt['date']==b['audit']['date']==pre['end_date'] and execution['returncode']==0 and h.sha256(Path(execution['command'][1]))==execution['helper_sha256'] and all(h.sha256(run/(stage+'.sav'))==s['audit']['save_sha256'] for stage,s in [(start,a),(end,b)]),
 'valid_original_ship_identities_and_HP':not invalid and not own_born and all(q.scalars(a['ships'][sid]).get('fleet') in [917,50332250] for sid in own_lost),
 'mod_population_colonization_same_month_cash_held':ac['variables']==bc['variables'] and ac['owned_colonies']==bc['owned_colonies']==[0,40] and all(a['audit']['colonies'][str(cid)]['actual_pop_sum']==b['audit']['colonies'][str(cid)]['actual_pop_sum'] for cid in [0,40]) and all(ac['effective_stockpile'].get(k)==bc['effective_stockpile'].get(k) for k in ['energy','minerals','alloys','trade','unity','astral_threads']) and all(q.scalars(q.block(q.block(s['roots']['planets'],'planet'),'544')).get('controller')==0 for s in [a,b]),
 'native_crisis_destroyed_ships_accounted':ca['path']==cb['path'] and ca['levels']==cb['levels'] and bc['effective_stockpile']['menace']-ac['effective_stockpile']['menace']==15*len(enemy_lost) and cb['objectives'].get('crisobj_destroy_enemy_ships',0)-ca['objectives'].get('crisobj_destroy_enemy_ships',0)==15*len(enemy_lost),
 'paid_armies_and_reserve_retained':own_armies(a)==own_armies(b) and a['fleets']['83886903']==b['fleets']['83886903'] and {k for k,v in a['items'].items() if q.scalars(v).get('paying_country')==0}=={k for k,v in b['items'].items() if q.scalars(v).get('paying_country')==0},
 'no_pending_or_new_error':not b['pending'] and (run/(end+'-error-before.log')).read_bytes()==(run/(end+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes(),
}
boundaries=[]
if own_lost:boundaries.append('actual_own_ship_loss')
if new_messages:boundaries.append('new_native_message')
if not all(own_combat.values()):boundaries.append('battle_end_or_disengagement')
proof={'pass':all(checks.values()),'checks':checks,'after_save_sha256':b['audit']['save_sha256'],'before_save_sha256':a['audit']['save_sha256'],'date':b['audit']['date'],'calendar_ready':all(checks.values()) and not boundaries,'boundaries':boundaries,'own_lost':sorted(own_lost),'enemy_destroyed':sorted(enemy_lost),'invalid_ships':invalid,'damage':damage,'own_combat':own_combat,'new_messages':new_messages,'menace':bc['effective_stockpile']['menace']}
out=run/(end+'-fauna-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({k:v for k,v in proof.items() if k!='damage'}),flush=True);sys.exit(0 if proof['pass'] else 1)
