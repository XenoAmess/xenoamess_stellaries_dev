import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime,timezone

source=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
target=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T003349Z-firestorm-completed')
assert not target.exists()
proof_names=['rc9-external-bombard-task-preconditions.json','rc9-external-bombard-reordered-prepare-proof.json','rc9-external-bombard-native-player-orders-proof.json','rc9-external-bombard-daily-unity-proof.json','rc9-external-bombard-real-clearing-proof.json','rc9-external-bombard-completed-negative-preconditions.json','rc9-external-bombard-completed-negative-replay-proof.json','rc9-external-bombard-final-calendar-negative-proof.json']
count=0
for name in proof_names:
 p=json.loads((source/name).read_text(encoding='utf-8'))
 assert p['status']=='PASS_SCOPED',name
 if 'checks' in p:
  assert all(p['checks'].values()),name
  count+=len(p['checks'])
 else:
  for cp in p['checkpoints']:
   assert all(cp['checks'].values())
   count+=len(cp['checks'])
shutil.copyfile(Path(__file__),source/Path(__file__).name)
target.mkdir(parents=True)
(target/'.gitattributes').write_text('* binary\n**/* binary\n',encoding='utf-8')
entries=[]
def take(path,name):
 data=path.read_bytes();out=target/name
 out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists()
 out.write_bytes(data);digest=hashlib.sha256(data).hexdigest()
 assert hashlib.sha256(out.read_bytes()).hexdigest()==digest
 entries.append({'path':name,'source':str(path.resolve()),'bytes':len(data),'sha256':digest})
names={'manifest.json','process.json','rc9-original-native-source-preflight.json',
 'rc9-recovery-extra-source-preflight.json','rc9-focus-finished69-original-byte-alias.json',
 'rc9-focus-developed-source69-before-begin.sav','rc9-focus-developed-source69-before-begin.audit.json',
 'rc9_forward_native_days.py','rc9_prepare_external_branch.py','rc9_prepare_external_bombard_branch.py','rc9_external_negative_replay.py','rc9_external_bombard_negative_replay.py','rc9_normal_calendar_probe.py','rc9_inspect_firestorm_native.py','rc9_external_firestorm_attacker_prepare.py','rc9_external_firestorm_attacker_prepare_reordered.py','rc9_external_firestorm_player_orders.py','rc9_external_firestorm_native_player_orders.py','rc9_external_firestorm_native_player_return.py',Path(__file__).name}
prefixes=('rc9-external-bombard','rc9-bombard','rc9_external_firestorm')
for path in sorted(source.rglob('*')):
 if path.is_file() and (path.name.startswith(prefixes) or path.name in names):
  take(path,path.relative_to(source).as_posix())
user=Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261008T003349Z')
take(user/'logs/error.log','stage-full-error-through-firestorm.log')
meta={'status':'SNAPSHOT_BYTE_VERIFIED','snapshot_at_utc':datetime.now(timezone.utc).isoformat(),
 'run':source.name,'version':'0.2.0-rc.9','language':'l_simp_chinese',
 'scope':'Completed controlled native firestorm daily unity, actual bombardment clearing, next day/month and five callbacks with no EEP rewards. Preserves original MIA/parser/player-switch failures and recovery. Not natural war or final complete-run log.',
 'original_files':len(entries),'original_bytes':sum(e['bytes'] for e in entries),
 'checked_reports':len(proof_names),'checks_passed':count,'proof_files':proof_names,
 'firestorm_loss_complete':True,'first_release_complete':False,
 'final_error_log_required_after_normal_stop':True,
 'preserved_failures':['rc9-external-bombard-prepare-proof.json','rc9-external-bombard-player-switch-original-failed-precondition.json'],
 'files':entries}
(target/'source-snapshot.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k!='files'}))
