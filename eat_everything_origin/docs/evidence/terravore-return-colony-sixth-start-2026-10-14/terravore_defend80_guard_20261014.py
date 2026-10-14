import json,logging,re,sys
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
a=read_state(run,'hope-route-wait-native-22950101');b=read_state(run,'hope-route-jan95-defend80-native-22950101')
ac,bc=[s['audit']['countries']['0'] for s in [a,b]]
fid='83886903';order=q.block(b['fleets'][fid],'current_order');path=q.block(q.block(b['fleets'][fid],'movement_manager'),'path')
parts=re.findall(r'\borigin=(\d+)',path);route=[v for i,v in enumerate(parts) if i==0 or v!=parts[i-1]]
base=q.scalars(q.block(q.block(b['roots']['starbase_mgr'],'starbases'),'169'))
ui=json.loads((run/'hope-route-jan95-defend80-native-22950101-pre.ocr.json').read_text('utf-8'))
checks={
 'bound_native_same_date_and_UI':a['audit']['date']==b['audit']['date']=='2295.01.01' and h.sha256(run/'hope-route-jan95-defend80-native-22950101.sav')==b['audit']['save_sha256'] and h.sha256(run/'hope-route-jan95-defend80-native-22950101-pre.jpg')==ui['image_sha256'] and any(q.scalars(path).get('date','unset') in row['text'] for row in ui['rows']),
 'exact_owned_base169_reachable80_order':str(base['station']) in b['ships'] and 'starbase=169' in order and 'planet=908' in order and 'origin=80' in order and order.count('can_reach=yes')==2 and route==['97','80'] and omit(a['fleets'][fid],{'movement_manager','order_id','current_order'})==omit(b['fleets'][fid],{'movement_manager','order_id','current_order'}),
 'all_sixteen_ships_other_fleets_and_paid_construction_held':a['ships']==b['ships'] and len(q.ids(q.block(b['fleets'][fid],'ships')))==16 and all(a['fleets'][other]==b['fleets'][other] for other in a['fleets'] if other!=fid) and a['items']==b['items'] and a['queues']==b['queues'],
 'cash_colonies_mod_and_crisis_held':ac['effective_stockpile']==bc['effective_stockpile'] and ac['variables']==bc['variables'] and ac['flags']==bc['flags'] and ac['owned_colonies']==bc['owned_colonies'] and a['audit']['colonies']==b['audit']['colonies'] and q.block(a['country'],'crisis_progression')==q.block(b['country'],'crisis_progression'),
 'messages_pending_and_errors_held':a['messages']==b['messages'] and a['pending']==b['pending']==[] and (run/'hope-route-jan95-defend80-native-22950101-error-before.log').read_bytes()==(run/'hope-route-jan95-defend80-native-22950101-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes(),
}
proof={'pass':all(checks.values()),'checks':checks,'before_save_sha256':a['audit']['save_sha256'],'after_save_sha256':b['audit']['save_sha256'],'calendar_ready':all(checks.values()),'route':route,'target_base':169,'target_system':80,'ETA':q.scalars(path).get('date')}
out=run/'hope-route-jan95-defend80-guard-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof),flush=True);sys.exit(0 if proof['pass'] else 1)
