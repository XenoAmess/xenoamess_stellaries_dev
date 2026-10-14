import json,logging,math,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
a=read_state(run,'hope-route-fauna-sep11-native-22940911');b=read_state(run,'hope-route-fauna-sep11-retreat-native-22940911')
ac,bc=[s['audit']['countries']['0'] for s in [a,b]]
fids=['50332250','917'];changes=[];valid=[]
for sid,raw in a['ships'].items():
 av,bv=q.scalars(raw),q.scalars(b['ships'][sid]);ok=q.block(raw,'ship_design_implementation')==q.block(b['ships'][sid],'ship_design_implementation') and all(av.get(k)==bv.get(k) for k in ['fleet','construction_date','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
 hp={}
 for field,mx in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]:
  ov,nv,cap=av.get(field,0),bv.get(field,0),bv.get(mx,0)
  ok=ok and all(isinstance(x,(int,float)) and math.isfinite(x) for x in [nv,cap]) and 0<=nv<=cap+.001
  if ov!=nv:hp[field]=[ov,nv]
 if hp:changes.append({'ship':sid,'hp_changes':hp})
 valid.append(ok)
new_messages=[q.scalars(v) for v in b['messages'] if v not in a['messages']]
states={fid:q.scalars(b['fleets'][fid]) for fid in fids}
e=json.loads((run/'hope-route-fauna-sep11-retreat-save-20261014-execution.json').read_text('utf-8'))
checks={
 'bound_same_date_save_and_real_input':a['audit']['date']==b['audit']['date']=='2294.09.11' and h.sha256(run/'hope-route-fauna-sep11-retreat-native-22940911.sav')==b['audit']['save_sha256'] and e['returncode']==0 and h.sha256(Path(e['command'][1]))==e['helper_sha256'] and all(json.loads((run/('hope-route-sep11-retreat'+n+'-click-20261014-execution.json')).read_text('utf-8'))['returncode']==0 for n in ['2','3']),
 'same_twenty_survivors_valid_designs_HP':set(a['ships'])==set(b['ships']) and all(valid) and all(q.ids(q.block(a['fleets'][fid],'ships'))==q.ids(q.block(b['fleets'][fid],'ships')) for fid in fids),
 'both_native_MIA_empty_orders_and_combat':all(states[fid].get('mia_type')=='mia_emergency_ftl' and q.scalars(q.block(q.block(b['fleets'][fid],'movement_manager'),'coordinate')).get('origin')==4294967295 and not q.block(b['fleets'][fid],'current_order') and not q.block(q.block(b['fleets'][fid],'combat'),'in_combat_with') for fid in fids) and states['50332250'].get('return_date')=='2295.09.07' and states['917'].get('return_date')=='2295.09.03',
 'other_assets_payments_population_mod_crisis_held':all(a['fleets'][fid]==b['fleets'][fid] for fid in a['fleets'] if fid not in fids) and a['items']==b['items'] and a['queues']==b['queues'] and a['roots']['army']==b['roots']['army'] and ac['effective_stockpile']==bc['effective_stockpile'] and ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['colonies']==b['audit']['colonies'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'only_expected_native_notifications_no_error':len(new_messages)==3 and sorted(x['type'] for x in new_messages)==['COMBAT_STATS','EMERGENCY_FTL_CASUALTIES','EMERGENCY_FTL_CASUALTIES'] and all(x['date']=='2294.09.11' for x in new_messages) and not b['pending'] and (run/'hope-route-fauna-sep11-retreat-native-22940911-error-before.log').read_bytes()==(run/'hope-route-fauna-sep11-retreat-native-22940911-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'calendar_ready':all(checks.values()),'survivors':{'50332250':13,'917':7},'return_dates':{fid:states[fid].get('return_date') for fid in fids},'ship_HP_changes':changes,'native_notifications':new_messages}
out=run/'hope-route-fauna-sep11-retreat-guard-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof),flush=True);sys.exit(0 if proof['pass'] else 1)
