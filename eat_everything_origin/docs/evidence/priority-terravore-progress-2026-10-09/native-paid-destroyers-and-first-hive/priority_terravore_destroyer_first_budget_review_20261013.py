"""Only27 native days before first destroyer birth, with exactly16 paid0work orders."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-sixteen-destroyers-paid-22840704';a=read_state(run,before);p=load(before+'-destroyer-paid-order-v2-proof.json');x=load(before+'-destroyer-paid-order-guard-v2-execution.json');ids=q.ids(q.block(a['queues']['3'],'items'))
checks={
 'prior13PASS_actual0_exactSAV_source':len(p['checks'])==13 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'only27days_two_parallel_paid16_zero_work_no_pending':p['boundaries']==['paid_destroyer_birth_review'] and a['audit']['date']=='2284.07.04' and not a['pending'] and len(ids)==16 and all(q.scalars(a['items'][str(i)])=={'queue':3,'paying_country':0,'progress':0,'progress_needed':60} and q.scalars(q.block(a['items'][str(i)],'resources'))=={'minerals':412.5} for i in ids) and q.scalars(a['queues']['3'])['simultaneous']==2,
 'mother_hive43_4_and_no_unreviewed_delay':q.scalars(a['items']['268435492'])['progress']==43.4 and all(q.scalars(v)['event']=='pirate.6' for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event'),
 'CN41_package_and_unfiltered_error_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(before+'-destroyer-first-budget-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2284.07.04','end_date':'2284.08.01','days':27,'maximum_days':27,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-destroyer-first-budget-review','scope':'Normal shipyard construction to first native budget; no birth before first40days.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
