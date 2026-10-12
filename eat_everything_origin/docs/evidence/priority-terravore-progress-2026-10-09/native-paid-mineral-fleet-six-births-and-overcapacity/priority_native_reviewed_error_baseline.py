"""Exact source-attributed native settings text error; reject all other additions."""
import hashlib,json
from pathlib import Path
OLD='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
NEW='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850'
REVIEW='db31e848d2a9a62652bd04d4158d53b5196868e032d937192bce261a621435ff'
sha=lambda data:hashlib.sha256(data).hexdigest()
def reviewed_error_pair(before,after,run):
 review=run/'terravore-native-settings-text-error-baseline-review.json'
 if sha(review.read_bytes())!=REVIEW:return False
 p=json.loads(review.read_text('utf-8'))
 return all(p['checks'].values()) and sha((run/p['old_error_file']).read_bytes())==OLD and sha((run/p['new_error_file']).read_bytes())==NEW and sha(Path(p['source']).read_bytes())==sha((run/p['preserved_source']).read_bytes())==p['source_sha256'] and sha(before) in {OLD,NEW} and sha(after)==NEW and (after.startswith(before) if sha(before)==OLD else after==before)
