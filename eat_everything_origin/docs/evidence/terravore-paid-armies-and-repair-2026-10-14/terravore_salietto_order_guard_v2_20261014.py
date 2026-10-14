import json,logging,re,sys
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
a=read_state(run,'hope-route-wait-native-22940801');b=read_state(run,'hope-route-aug01-salietto-confirm-native-22940801')
ac,bc=[s['audit']['countries']['0'] for s in (a,b)]
fids=['50332250','917'];expected_path=['97','33','171','139','188','146','96','53','147','65','178','107','77']
paths={};etas={};valid=[]
for fid in fids:
 af,bf=a['fleets'][fid],b['fleets'][fid]
 order=q.block(bf,'current_order');p=q.block(q.block(bf,'movement_manager'),'path')
 parts=re.findall(r'\borigin=(\d+)',p);paths[fid]=[v for i,v in enumerate(parts) if i==0 or v!=parts[i-1]]
 etas[fid]=q.scalars(p).get('date')
 old,new=q.scalars(q.block(af,'properties')),q.scalars(q.block(bf,'properties'));old['dirty_cloaking_strength']='yes'
 valid.append('orbit_planet_order' in order and 'planet=870' in order and 'origin=77' in order and order.count('can_reach=yes')==2 and paths[fid]==expected_path and old==new and omit(af,{'movement_manager','order_id','current_order','properties'})==omit(bf,{'movement_manager','order_id','current_order','properties'}))
ui_files={'50332250':'hope-route-aug01-salietto-confirm-native-22940801-pre','917':'hope-route-aug01-dwell-right3-ui-after'}
ui_match=[]
for fid,stem in ui_files.items():
 ui=json.loads((run/(stem+'.ocr.json')).read_text('utf-8'))
 ui_match.append(h.sha256(run/(stem+'.jpg'))==ui['image_sha256'] and any(etas[fid] in row['text'] for row in ui['rows']))
e=json.loads((run/'hope-route-aug01-salietto-confirm-save-20261014-execution.json').read_text('utf-8'))
checks={
 'bound_same_date_original_save_and_action':a['audit']['date']==b['audit']['date']=='2294.08.01' and h.sha256(run/'hope-route-aug01-salietto-confirm-native-22940801.sav')==b['audit']['save_sha256'] and e['returncode']==0 and h.sha256(Path(e['command'][1]))==e['helper_sha256'],
 'two_exact_reachable77_orders_and_native_properties':all(valid) and all(ui_match),
 'all_ships_other_fleets_and_paid_army_queue_held':a['ships']==b['ships'] and a['items']==b['items'] and a['queues']==b['queues'] and set(a['fleets'])==set(b['fleets']) and all(a['fleets'][fid]==b['fleets'][fid] for fid in a['fleets'] if fid not in fids),
 'cash_mod_population_and_crisis_held':ac['effective_stockpile']==bc['effective_stockpile'] and ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['colonies']==b['audit']['colonies'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'messages_pending_and_errors_held':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-aug01-salietto-confirm-native-22940801-error-before.log').read_bytes()==(run/'hope-route-aug01-salietto-confirm-native-22940801-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'paths':paths,'etas':etas,'calendar_ready':all(checks.values())}
out=run/'hope-route-aug01-salietto-order-guard-v2-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof),flush=True);sys.exit(0 if proof['pass'] else 1)
