"""Allow exactly the independently reviewed native lookup line; reject new errors."""
import hashlib,json
from pathlib import Path
from priority_native_reviewed_error_baseline import reviewed_error_pair as prior_pair
OLD='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850'
NEW='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592'
REVIEW='b3cdcb5ea07e33523dd4ceb655e01b3625a8f541a8aaaac7236bac8ec280d438'
sha=lambda data:hashlib.sha256(data).hexdigest()
def reviewed_error_pair(before,after,run):
 if prior_pair(before,after,run):return True
 file=run/'terravore-three-labs-normal-month-22811001-native-uplift-review-v2-proof.json'
 if sha(file.read_bytes())!=REVIEW:return False
 p=json.loads(file.read_text('utf-8'));x=json.loads((run/'terravore-three-labs-normal-month-22811001-native-uplift-review-v2-execution.json').read_text('utf-8'))
 return len(p['checks'])==7 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==sha((run/'priority_terravore_native_uplift_error_review_v2_20261013.py').read_bytes())=='231a8b7454d38eb08cd973fd0f3418af1a150c0f6442c1e8dc01d7ae5c26bd2d' and sha((run/p['old_error_file']).read_bytes())==OLD and sha((run/p['new_error_file']).read_bytes())==NEW and all(sha(Path(v['path']).read_bytes())==sha((run/v['preserved']).read_bytes())==v['sha256'] for v in p['sources']) and sha(before) in {OLD,NEW} and sha(after)==NEW and (after.startswith(before) if sha(before)==OLD else after==before)
