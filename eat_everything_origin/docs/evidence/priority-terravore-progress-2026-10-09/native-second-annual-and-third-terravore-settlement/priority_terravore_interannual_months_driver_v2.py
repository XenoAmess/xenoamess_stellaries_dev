"""Four bounded native intervals. Stop at first non-PASS; never retries or crosses final."""
import hashlib,json,subprocess,sys
from pathlib import Path
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z')
load=lambda n:json.loads((run/n).read_text('utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
calendar=run/'formal_production_native_calendar_checked_v2.py'
observer=run/'priority_terravore_interannual_build_observer_v3.py'
wrapper=run/'record_current_helper.py'
expected='83647aef996eb655c26d932ab6831093b58c8fca2529a64e7b35088c122e07d7'
plans=[('2272.04.23',30),('2272.05.23',30),('2272.06.23',30),('2272.06.30',7)]
before='terravore-interannual-months1-step1'
proof_file=before+'-interannual-build-v3-proof.json'
execution_stage=before+'-observer-v3'
completed=[]
receipt=run/'terravore-interannual-months2-driver-proof.json'
assert not receipt.exists()
def write(status):
    receipt.write_text(json.dumps({'status':status,'completed_steps':completed,'scope':'Four bounded interannual native components only; stops before final July1.'},indent=2),'utf-8')
def invoke(stage,helper,args):
    result=subprocess.run([sys.executable,'-X','utf8',str(wrapper),stage,str(helper),*args],check=False)
    execution=load(stage+'-execution.json')
    assert result.returncode==execution['returncode']==0 and execution['helper_sha256']==sha(helper),'Actual invocation failed; no retries'
    return execution
try:
    static=load('terravore-interannual-months-driver-v2-static.json')
    assert static['status']=='PASS' and not static['errors'] and static['helper_sha256']==sha(Path(__file__))
    ostatic=load('terravore-interannual-build-observer-v3-static.json')
    assert ostatic['status']=='PASS' and not ostatic['errors'] and ostatic['helper_sha256']==sha(observer)==expected
    assert sha(calendar)=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc'
    assert sha(wrapper)=='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3'
    assert sha(run/(before+'.sav'))=='36f22230ee0a24aa7c8ea4f7c39c40788d0037a233a0024eb62573dd20ee562a'
    assert all(not list(run.glob('terravore-interannual-months2-step'+str(i)+'*')) for i in range(1,5))
    for i,(end,days) in enumerate(plans,1):
        prior=load(proof_file);execution=load(execution_stage+'-execution.json')
        assert prior['status']=='PASS_NATIVE_TERRAVORE_INTERANNUAL_BUILD_COMPONENT' and len(prior['checks'])==32 and all(v is True for v in prior['checks'].values())
        assert prior['interannual_build_calendar_ready'] and days<=prior['maximum_days_to_final_boundary'] and not prior['housing_cache_refresh_pending']
        assert execution['returncode']==0 and execution['helper_sha256']==sha(observer)==expected and prior['after_sha256']==sha(run/(before+'.sav'))
        after='terravore-interannual-months2-step'+str(i)
        assert not list(run.glob(after+'*'))
        print(json.dumps({'dispatch':after,'before':before,'end':end,'days':days}),flush=True)
        invoke(after+'-calendar',calendar,[before,end,after,str(days),proof_file,execution_stage])
        invoke(after+'-observer-v3',observer,[before,after])
        new=load(after+'-interannual-build-v3-proof.json')
        assert new['status']=='PASS_NATIVE_TERRAVORE_INTERANNUAL_BUILD_COMPONENT' and len(new['checks'])==32 and all(v is True for v in new['checks'].values())
        assert new['date']==end and new['days']==days and new['after_sha256']==sha(run/(after+'.sav')) and not new['housing_cache_refresh_pending']
        completed.append({'stage':after,'date':end,'days':days,'after_sha256':new['after_sha256'],'checks':len(new['checks']),'third_progress':new['actual_third_progress']})
        write('IN_PROGRESS')
        before=after;proof_file=after+'-interannual-build-v3-proof.json';execution_stage=after+'-observer-v3'
        print(json.dumps({'completed':completed[-1]}),flush=True)
    assert new['date']=='2272.06.30' and new['interannual_build_calendar_ready'] is False and new['maximum_days_to_final_boundary']==0
    write('PASS_FOUR_NATIVE_INTERANNUAL_COMPONENTS_STOPPED_BEFORE_FINAL')
except BaseException:
    write('FAIL_STOPPED_NO_RETRY')
    raise
print(json.dumps({'status':'PASS_FOUR_NATIVE_INTERANNUAL_COMPONENTS_STOPPED_BEFORE_FINAL','completed_steps':len(completed)}),flush=True)
