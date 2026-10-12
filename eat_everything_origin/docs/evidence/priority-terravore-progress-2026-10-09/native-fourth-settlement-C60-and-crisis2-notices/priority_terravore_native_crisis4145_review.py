"""Exact three native days to current crisis4145; no event acknowledgement."""
import json
import logging
import sys
from pathlib import Path
stage, execution_stage=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from formal_production_native_calendar_checked_v3 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
name=stage+'-native-final-settlement-v2-proof.json';pre=load(name)
ex=load(stage+'-native-final-settlement-guard-v2-execution.json')
a=pre['after_state'];au=a['audit'];c=au['countries']['0']
delays=[v for k,v,o in q.fields(q.block(q.block(a['country0_raw'],'modules'),'standard_event_module')) if k=='delayed_event' and o]
validate_native_interval(au['date'],'2278.10.05',3)
checks={
 'final20_PASS_actual0_fixed_proof_source_SAV':h.sha256(run/name)=='44a9d284581bb82cadf3ec459107d5fe4e6258a15a0e83b348d052e8efe9f4c1'
    and len(pre['checks'])==20 and all(v is True for v in pre['checks'].values())
    and ex['returncode']==0 and ex['helper_sha256']==h.sha256(Path(ex['command'][1]))
    =='812c022c3ffcd851fb6705c9c1b6e03ee24966d32b19113207182aa872f9416d'
    and pre['after_sha256']==au['save_sha256']==h.sha256(run/(stage+'.sav'))
    =='7e13a140ff372bb916ac3e06f97c6dfe2bdc32a7439fe76e669f2360a2c9f939',
 'only_exact_native_crisis4145_delay3_country0':len(delays)==1 and q.scalars(delays[0])=={'event':'crisis.4145','days':3}
    and all(q.scalars(q.block(delays[0],'scope')).get(k)==v for k,v in {'type':'country','id':0,'opener_id':4294967295}.items()),
 'settled_credit_capacity_POP_and_Queen_pending_held':all(c['variables'].get(k)==v for k,v in {'eep_c':62,'eep_d':17,'eep_worlds':4,'eep_g':0,'eep_made':0,'eep_stage':1,'eep_crisis':1}.items())
    and c['effective_stockpile']['menace']==1635 and c['owned_colonies']==[0]
    and au['colonies']['0']['actual_pop_sum']==11920 and au['planets']['523']['planet_class']=='pc_shattered'
    and 'eep_notice_pending' in c['flags'] and not a['pending_country0_raw'],
 'current_exact_business_boundaries_unready':pre['boundaries']==['native_crisis4145_day3','queen_monthly_notice']
    and pre['native_devour_calendar_ready'] is False and pre['maximum_days_to_native_bite_boundary']==0,
 'unfiltered_error_and_production41_simp_chinese_held':h.sha256(run/(stage+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
    and meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41
    and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed=all(v is True for v in checks.values())
out=run/(execution_stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':au['save_sha256'],'after_sha256':au['save_sha256'],
 'start_date':'2278.10.02','end_date':'2278.10.05','days':3,'maximum_days':3,'allowed_boundaries':pre['boundaries'],
 'execution_stage':execution_stage,'source_proof_file':name,'source_proof_sha256':h.sha256(run/name),
 'scope':'Only current native crisis event delay; capture and independently check actual pending before acknowledgement.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed
