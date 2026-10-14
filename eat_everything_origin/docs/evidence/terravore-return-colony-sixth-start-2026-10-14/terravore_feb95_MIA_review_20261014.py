import json,logging,sys
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
s=read_state(run,'hope-route-wait-native-22950201')
p=json.loads((run/'hope-route-wait-native-22950201-wait-v2-proof.json').read_text('utf-8'))
enemy=q.block(s['roots']['fleet'],'50332411');ev=q.scalars(enemy)
assert p['pass'] and p['calendar_ready'] and p['after_save_sha256']==s['audit']['save_sha256']
assert h.sha256(run/'hope-route-wait-native-22950201.sav')==s['audit']['save_sha256']
assert ev['mia_type']=='mia_emergency_ftl' and ev['return_date']=='2295.02.24' and len(q.ids(q.block(enemy,'ships')))==13
assert q.scalars(s['fleets']['50332250'])['return_date']=='2295.09.07' and q.scalars(s['fleets']['917'])['return_date']=='2295.09.03'
assert all(not q.block(q.block(v,'combat'),'in_combat_with') for v in s['fleets'].values()) and not s['pending']
assert (run/'hope-route-wait-native-22950201-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes()
out=run/'hope-route-feb95-MIA-reviewed-proof.json';assert not out.exists()
h.write_json(out,{'pass':True,'checks':{'all_six_monthly_groups':True,'native_enemy13_MIA_return_bound':True,'own_MIA_bound_and_no_active_combat':True},'after_save_sha256':s['audit']['save_sha256'],'calendar_ready':True,'wait_until':'2295.09.01','first_interval':['2295.02.01','2295.03.01',30],'scope':'Native enemy MIA return observed in next month; no guaranteed position/safety, no enemy or asset edits.'})
print(json.dumps({'pass':True,'wait_until':'2295.09.01','first_end':'2295.03.01'}),flush=True)
