import json,logging,sys
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
p=json.loads((run/'hope-route-wait-native-22950101-wait-v2-proof.json').read_text('utf-8'))
assert p['pass'] and p['boundaries']==['new_native_messages'] and not p['new_tech']
assert len(p['new_messages'])==1
m=p['new_messages'][0]
assert m['type']=='LEADER_POOL_REFRESHED_MESSAGE_TYPE' and m['localization']=='LEADER_POOL_REFRESHED_TITLE' and m['receiver']==0 and m['date']=='2295.01.01'
assert h.sha256(run/'hope-route-wait-native-22950101.sav')==p['after_save_sha256']
assert (run/'hope-route-wait-native-22950101-error-after.log').read_bytes()==(user/'logs/error.log').read_bytes()
out=run/'hope-route-jan95-leader-pool-reviewed-proof.json';assert not out.exists()
h.write_json(out,{'pass':True,'checks':{'all_six_monthly_groups_passed':True,'unique_native_leader_pool_notice_only':True},'after_save_sha256':p['after_save_sha256'],'calendar_ready':True,'scope':'Vanilla1800-day leader candidate pool refresh; no hire, Queen event or reward.'})
print(json.dumps({'pass':True,'calendar_ready':True}),flush=True)
