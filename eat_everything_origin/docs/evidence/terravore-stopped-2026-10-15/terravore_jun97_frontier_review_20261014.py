"""Actual native battle, two existing facilities transferred, one paid army, acknowledgement."""
import json,logging,math,re,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
stages=('hope-route-wait-native-22970501','hope-route-wait-native-22970601','hope-route-jun97-archive-ack-native-22970601')
a,b,c=[read_state(run,s) for s in stages]
ac,bc,cc=[s['audit']['countries']['0'] for s in (a,b,c)]
observation=json.loads((run/(stages[1]+'-native-bite-v9-proof.json')).read_text('utf-8'))
receipt=json.loads((run/(stages[1]+'-calendar-receipt.json')).read_text('utf-8'))
ack=json.loads((run/'hope-route-jun97-archive-native-ack-20261014-execution.json').read_text('utf-8'))
transferred={'33555437':'shipclass_starbase','100664466':'shipclass_mining_station'}
owners={str(fid):int(k) for k,v,x in q.fields(a['roots']['country']) if x for fid in map(int,re.findall(r'fleet=(\d+)',q.block(q.block(v,'fleets_manager'),'owned_fleets')))}
transfer_evidence={}
for sid,kind in transferred.items():
 old=q.scalars(q.block(a['roots']['ships'],sid));new=q.scalars(b['ships'][sid])
 fleet=b['fleets'][str(new['fleet'])]
 transfer_evidence[sid]={'previous_owner':owners.get(str(old['fleet'])),'previous':old,'current':new,'fleet_class':q.scalars(fleet).get('ship_class'),'same_construction_date':old.get('construction_date')==new.get('construction_date'),'system':q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate')).get('origin')}
ship_valid=[]
damage={}
for sid,raw in a['ships'].items():
 old,new=q.scalars(raw),q.scalars(b['ships'][sid])
 good=q.block(raw,'ship_design_implementation')==q.block(b['ships'][sid],'ship_design_implementation') and all(old.get(k)==new.get(k) for k in ('construction_date','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'))
 for hp,mx in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]:
  value=new.get(hp,0);maximum=new.get(mx,0)
  good=good and all(isinstance(v,(float,int)) and math.isfinite(v) for v in (value,maximum)) and 0<=value<=maximum+.001
  if value<old.get(hp,0):damage.setdefault(sid,{})[hp]=[old.get(hp,0),value]
 ship_valid.append(good)
messages=[q.scalars(v) for v in b['messages'] if v not in a['messages']]
reports=[q.block(v,'combat_stats') for v in b['messages'] if v not in a['messages'] and q.scalars(v).get('type')=='COMBAT_STATS']
paid=a['items']['268435486']
army=q.scalars(q.block(b['roots']['army'],'16777573'))
checks={
 'original_native_month_and_failed_observation_retained':a['audit']['date']=='2297.05.01' and b['audit']['date']==c['audit']['date']=='2297.06.01' and receipt['days']==30 and receipt['date']=='2297.06.01' and observation['after_save_sha256']==b['audit']['save_sha256'] and not observation['pass'] and all(h.sha256(run/(s+'.sav'))==v['audit']['save_sha256'] for s,v in zip(stages,(a,b,c),strict=True)),
 'six_exact_month_cash_and_no_menace_grant':observation['checks']['six_cash_exact_month_and_solvent'] and ac['effective_stockpile']['menace']==bc['effective_stockpile']['menace']==3530 and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'source_progress_population_mod_and_queen_held':observation['checks']['digest_progress_and_material_exact'] and observation['checks']['mod_crisis_and_colonial_identity_held'] and all(v['pass'] for v in observation['growth_evidence'].values()) and observation['digest_progress']==16 and ac['variables']==bc['variables'],
 'two_old_enemy_facilities_transferred_not_newly_built':set(b['ships'])-set(a['ships'])==set(transferred)|{'16777951'} and all(v['previous_owner']==1 and v['same_construction_date'] and v['fleet_class']==transferred[sid] and v['system']==71 for sid,v in transfer_evidence.items()),
 'all_old_ships_retained_actual_design_max_valid_HP':set(a['ships'])<=set(b['ships']) and all(ship_valid) and set(damage)=={'33554922','67110414'} and all(set(v)=={'armor_hitpoints'} for v in damage.values()) and len(q.ids(q.block(b['fleets']['50332250'],'ships')))==14 and len(q.ids(q.block(b['fleets']['917'],'ships')))==9,
 'actual_native_combat_and_archive_messages':len(reports)==1 and q.scalars(reports[0]).get('reason')=='no_more_enemies' and q.scalars(reports[0]).get('date')=='2297.05.15' and [v['type'] for v in messages]==['COMBAT_STATS','MESSAGE_SPECIMEN_ACQUIRED','MESSAGE_STOLEN_SPECIMEN_PERPETRATOR','EVENT_MESSAGE_TYPE'] and messages[1].get('specimen_name')=='脉动之心' and len(b['pending'])==1 and q.scalars(b['pending'][0]).get('id')==314 and q.scalars(b['pending'][0]).get('event')=='grand_archive.4510',
 'second_source_army_exact_paid_birth':q.scalars(q.block(paid,'resources'))=={'minerals':100} and q.scalars(q.block(paid,'buildable_army'))=={'army_type':'assault_army','species':73,'planet':40,'starbase':4294967295} and army.get('type')=='assault_army' and army.get('species')==73 and army.get('ship')==16777951 and q.scalars(b['ships']['16777951']).get('army')==16777573 and q.scalars(b['ships']['16777951']).get('construction_date')=='2297.06.01' and not b['items'].get('268435486') and len([v for v in b['items'].values() if q.scalars(v).get('paying_country')==0])==6,
 'acknowledgement_only_no_rewards_or_calendar':ack['returncode']==0 and h.sha256(Path(ack['command'][1]))==ack['helper_sha256'] and not c['pending'] and b['ships']==c['ships'] and b['fleets']==c['fleets'] and b['items']==c['items'] and b['roots']['army']==c['roots']['army'] and b['audit']['colonies']==c['audit']['colonies'] and b['audit']['situations']==c['audit']['situations'] and bc['effective_stockpile']==cc['effective_stockpile'] and bc['variables']==cc['variables'] and q.block(b['country'],'crisis_progression')==q.block(c['country'],'crisis_progression'),
 'production_chinese_and_errors_held':meta['language']=='l_simp_chinese' and meta['version']=='0.2.0' and h.tree_manifest(r.ROOT/'mod')[1]==meta['repository_mod_tree_sha256'] and (run/(stages[1]+'-error-before.log')).read_bytes()==(run/(stages[1]+'-error-after.log')).read_bytes()==(run/(stages[2]+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'combat_save_sha256':b['audit']['save_sha256'],'after_save_sha256':c['audit']['save_sha256'],'calendar_ready':all(checks.values()),'transfer_evidence':transfer_evidence,'damage':damage,'messages':messages,'army':army}
out=run/(stages[2]+'-frontier-reviewed-proof.json')
assert not out.exists()
h.write_json(out,proof)
print(json.dumps(proof,ensure_ascii=False),flush=True)
sys.exit(0 if proof['pass'] else 1)
