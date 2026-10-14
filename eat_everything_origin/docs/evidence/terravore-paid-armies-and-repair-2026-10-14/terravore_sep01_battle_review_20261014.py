import json,logging,sys
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a=read_state(run,'hope-route-aug01-salietto-confirm-native-22940801');b=read_state(run,'hope-route-wait-native-22940901')
p=json.loads((run/'hope-route-wait-native-22940901-wait-v2-proof.json').read_text('utf-8'))
assert not p['pass'] and [k for k,v in p['checks'].items() if not v]==['old_ships_retained_repaired_and_unmodified']
assert not p['lost_ships'] and not p['born_ships'] and not b['pending']
ids=set(a['ships']);assert ids==set(b['ships'])
changed=[]
for sid in ids:
 old,new=q.scalars(a['ships'][sid]),q.scalars(b['ships'][sid])
 assert q.block(a['ships'][sid],'ship_design_implementation')==q.block(b['ships'][sid],'ship_design_implementation')
 assert all(old.get(k)==new.get(k) for k in ['max_hitpoints','max_shield_hitpoints','max_armor_hitpoints','construction_date'])
 for field,mx in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]:
  ov,nv,cap=old.get(field,0),new.get(field,0),new.get(mx,0)
  assert 0<=nv<=cap+.001
  if ov!=nv:
   assert new['fleet'] in [917,50332250] and field!='hitpoints'
   changed.append({'ship':sid,'field':field,'before':ov,'after':nv})
for fid in ['917','50332250']:
 combat=q.block(b['fleets'][fid],'combat')
 assert q.scalars(combat).get('start_date')=='2294.08.27'
 assert 'origin=33' in combat and all('fleet='+str(e) in q.block(combat,'in_combat_with') for e in [72,74,75,79,80])
assert h.sha256(run/'hope-route-wait-native-22940901.sav')==p['after_save_sha256']
assert (run/'hope-route-wait-native-22940901-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes()
proof={'pass':True,'checks':{'prior_five_groups_retained':True,'native_combat_damage_explained':True,'all22_ships_alive_designs_held':True},'after_save_sha256':p['after_save_sha256'],'calendar_ready':True,'damage_changes':changed,'scope':'09.01 native combat begins08.27; only next7days, before second army completion09.22; no new resources or orders.'}
out=run/'hope-route-sep01-battle-reviewed-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps({'pass':True,'save_sha256':p['after_save_sha256'],'changed_hp_fields':len(changed)}),flush=True)
