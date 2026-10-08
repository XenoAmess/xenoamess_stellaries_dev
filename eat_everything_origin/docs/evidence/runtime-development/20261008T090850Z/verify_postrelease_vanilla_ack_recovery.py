"""Read-only verification of the corrected ACK phase against original saves."""
import json, re, shutil, sys, zipfile
from pathlib import Path
sys.path.insert(0, 'eat_everything_origin/tools')
import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T090850Z')
dest=run/Path(__file__).name
assert not dest.exists();shutil.copyfile(Path(__file__),dest)
proof=json.loads((run/'postvanilla-native-completion-ack-readonly-proof.json').read_text(encoding='utf-8'))
failed=json.loads((run/'postvanilla-normal-ack-retry-proof.json').read_text(encoding='utf-8'))
assert failed['status']=='FAIL' and failed['checks']['expected_native_terminal_transition'] is False
assert all(v for k,v in failed['checks'].items() if k!='expected_native_terminal_transition')
pattern=r'\{\s*player_event=38\s*human=1\s*option=0\s*\}'
for stage,field,sha_field in [('postvanilla-ack-restored-before','native_selection_history_before','before_sha256'),('postvanilla-normal-ack-retry','native_selection_history_after','after_sha256')]:
 source=run/(stage+'.sav');a=q.audit(source,(0,));assert a['save_sha256']==proof[sha_field]==failed[sha_field]
 with zipfile.ZipFile(source) as z:text=z.read('gamestate').decode('utf-8-sig')
 assert q.block(text,'open_player_event_selection_history')==proof[field]
assert len(re.findall(pattern,proof['native_selection_history_before']))==0
assert len(re.findall(pattern,proof['native_selection_history_after']))==1
assert proof['status']=='PASS_SCOPED' and len(proof['checks'])==25 and all(proof['checks'].values())
print('25 ACK invariants and original human selection verified; original premature cleanup FAIL retained')
