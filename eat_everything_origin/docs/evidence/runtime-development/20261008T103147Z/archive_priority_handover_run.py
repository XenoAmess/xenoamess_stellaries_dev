"""Preserve the actual forced-stop result and all partial-route evidence."""
import hashlib,json,shutil,sys,zipfile
from pathlib import Path
from datetime import datetime,timezone
import psutil
sys.stdout.reconfigure(encoding='utf-8')
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z')
m=json.loads((run/'manifest.json').read_text(encoding='utf-8'))
user=Path(m['userdir']);stop=json.loads((run/'stop.json').read_text(encoding='utf-8'))
assert stop['forced'] is True and stop['running_after'] is False
assert not psutil.pid_exists(int(stop['pid']))
seed=run/'organic-temple-year1-cleared.sav'
seed_sha='580d9344053ce71fed697384bc247bb8911aa3806170d113051b92a51f33dbb2'
assert hashlib.sha256(seed.read_bytes()).hexdigest()==seed_sha
with zipfile.ZipFile(seed) as z:
    assert z.testzip() is None
    state=z.read('gamestate').decode('utf-8-sig')
    assert '2309.05.02' in state and 'eep_probe' not in state
captures=[]
for name in [Path(__file__).name,'verify_priority_archive_git_blobs.py','native_selected_history.py']:
    src=Path('_runtime/heart-of-devouring')/name;dest=run/name
    assert not dest.exists()
    shutil.copyfile(src,dest)
    captures.append({'name':name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
                     'timing':'Captured during archival, not a retroactive execution-time binding.'})
(run/'priority-handover-archival-source-captures.json').write_text(json.dumps(captures,indent=2)+'\n',encoding='utf-8',newline='\n')
target=Path('eat_everything_origin/docs/evidence/runtime-development')/run.name
assert not target.exists()
target.mkdir(parents=True);files=[]
def copy(src,rel):
    out=target/rel;out.parent.mkdir(parents=True,exist_ok=True)
    raw=src.read_bytes();out.write_bytes(raw);assert out.read_bytes()==raw
    files.append({'file':rel.as_posix(),'original_source':str(src.resolve()),
                  'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
for src in sorted(run.rglob('*')):
    if src.is_file():copy(src,src.relative_to(run))
for src in sorted((user/'logs').rglob('*')):
    if src.is_file():copy(src,Path('final-logs')/src.relative_to(user/'logs'))
for name in ['settings.txt','pdx_settings.txt','dlc_load.json','commands_at_date.txt']:
    src=user/name
    if src.is_file():copy(src,Path('userdir-config')/name)
(target/'.gitattributes').write_text('* binary\n** binary\n',encoding='utf-8',newline='\n')
proof={'schema':'immutable-priority-handover-source-snapshot-v1','run_id':run.name,
       'archived_at_utc':datetime.now(timezone.utc).isoformat(),'version':'0.2.0',
       'exit_acceptance':'FAIL_FORCED_STOP','stop':stop,
       'scope':'Entire stopped Simplified Chinese partial organic route; all failures and unfiltered final logs. Integrity only, not normal exit, reload or full route acceptance.',
       'continuation_seed':{'file':seed.name,'sha256':seed_sha,'date':'2309.05.02','zip_integrity':'PASS'},
       'archival_source_captures':captures,'source_files':len(files),
       'source_bytes':sum(x['bytes'] for x in files),'files':files}
(target/'source-snapshot.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in proof.items() if k!='files'},ensure_ascii=False),flush=True)
