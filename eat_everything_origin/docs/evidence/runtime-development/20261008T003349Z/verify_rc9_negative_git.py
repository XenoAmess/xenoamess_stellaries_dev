import hashlib,json,re,subprocess
from pathlib import Path
root=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T003349Z-negative-abandon-purge-completed')
snapshot=json.loads((root/'source-snapshot.json').read_text(encoding='utf-8'))
for e in snapshot['files']:
 data=(root/e['path']).read_bytes()
 assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256']
 if e['path']!='stage-full-error-through-negative-abandon-purge.log':assert Path(e['source']).read_bytes()==data,e['path']
paths=sorted(p for p in root.rglob('*') if p.is_file())
requests=''.join(':'+p.as_posix()+'\n' for p in paths).encode()
raw=subprocess.run(['git','cat-file','--batch'],input=requests,capture_output=True,check=True).stdout
cursor=0
for p in paths:
 end=raw.index(b'\n',cursor);oid,kind,size=raw[cursor:end].decode().split();assert kind=='blob';size=int(size)
 assert raw[end+1:end+1+size]==p.read_bytes(),p
 cursor=end+1+size+1
assert cursor==len(raw)
error=root/'stage-full-error-through-negative-abandon-purge.log';content=error.read_text(encoding='utf-8-sig',errors='replace')
result={'status':'PASS','scope':'Immutable completed abandonment/purge-loss and return-conservation originals and staged Git blobs, not complete acceptance or final run log.',
 'source_files':snapshot['original_files'],'source_bytes':snapshot['original_bytes'],
 'git_checked_files':len(paths),'git_checked_bytes':sum(p.stat().st_size for p in paths),
 'stage_error_sha256':hashlib.sha256(error.read_bytes()).hexdigest(),
 'anonymous_console_scope_failure_preserved':'Wrong scope for effect' in content and 'file:  line: 1' in content,
 'eep_production_path_scope_error_present':bool(re.search(r'Wrong scope[^\n]*file: (?:common|events|interface)/[^\n]*(?:eep|planet_view)',content)),
 'checked_reports':snapshot['checked_reports'],'checks_passed':snapshot['checks_passed'],
 'abandon_and_native_purge_loss_complete':True,'first_release_complete':False,
 'final_complete_run_log_still_required':True,'preserved_failures':snapshot['preserved_failures']}
out=Path('eat_everything_origin/docs/evidence/rc9-completed-negative-git-object-check-2026-10-08.json');assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
