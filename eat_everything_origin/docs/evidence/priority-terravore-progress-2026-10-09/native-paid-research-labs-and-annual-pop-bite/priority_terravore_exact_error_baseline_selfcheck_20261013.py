"""Positive and negative exact native error baseline probes; never alters logs."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();stage='terravore-three-labs-normal-month-22811001'
old=(run/(stage+'-error-before.log')).read_bytes();new=(run/(stage+'-error-after.log')).read_bytes();module=Path(__file__).with_name('priority_native_uplift_error_baseline_20261013.py')
checks={
 'exact_reviewed_old_to_new_allowed':reviewed_error_pair(old,new,run),
 'exact_new_unchanged_allowed':reviewed_error_pair(new,new,run),
 'new_to_old_rejected':not reviewed_error_pair(new,old,run),
 'any_other_new_error_rejected':not reviewed_error_pair(new,new+b'[unknown.cpp:1] test\r\n',run),
 'duplicate_native_error_rejected':not reviewed_error_pair(new,new+new[len(old):],run),
 'truncated_log_rejected':not reviewed_error_pair(new,new[:-1],run),
 'changed_original_timestamp_rejected':not reviewed_error_pair(old,new.replace(b'[00:54:06]',b'[00:54:07]'),run),
 'baseline_source_preserved_current_log_unchanged':h.sha256(module)==h.sha256(run/module.name) and (user/'logs/error.log').read_bytes()==new,
}
passed=all(v is True for v in checks.values());out=run/'terravore-native-uplift-error-baseline-selfcheck-proof.json';assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_ERROR_BASELINE_ALLOWED_AND_REJECTED_CASES' if passed else 'FAIL','checks':checks,'module_sha256':h.sha256(module),'scope':'Only original reviewed line allowed. Unknown additions, duplicate line and modified logs rejected; no log mutations.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
