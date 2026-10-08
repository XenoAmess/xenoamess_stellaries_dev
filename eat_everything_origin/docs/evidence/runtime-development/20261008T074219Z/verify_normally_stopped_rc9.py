import hashlib,json,subprocess,sys
from pathlib import Path
root=Path('eat_everything_origin/docs/evidence/runtime-development')/sys.argv[1]
s=json.loads((root/'source-snapshot.json').read_text(encoding='utf-8'))
for e in s['files']:
    data=(root/e['file']).read_bytes()
    assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256']
    assert Path(e['original_source']).read_bytes()==data
paths=sorted(p for p in root.rglob('*') if p.is_file())
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
total=0
for p in paths:
    proc.stdin.write((':'+p.as_posix()+'\n').encode());proc.stdin.flush()
    header=proc.stdout.readline().decode().split();assert len(header)==3 and header[1]=='blob',header
    n=int(header[2]);raw=proc.stdout.read(n);assert proc.stdout.read(1)==b'\n'
    assert raw==p.read_bytes(),p;total+=n
proc.stdin.close();assert proc.wait()==0
error=root/'final-logs/error.log';text=error.read_text(encoding='utf-8-sig',errors='replace')
v={'status':'PASS','scope':'Full normally stopped run archive and Git original bytes only; not runtime acceptance.',
 'run_id':root.name,'source_files':s['source_files'],'source_bytes':s['source_bytes'],'git_checked_files':len(paths),'git_checked_bytes':total,
 'normal_stop':s['stop']['forced'] is False and s['stop']['running_after'] is False,
 'final_error_sha256':hashlib.sha256(error.read_bytes()).hexdigest(),'final_error_bytes':error.stat().st_size,
 'wrong_scope_present':'Wrong scope for trigger' in text,'EEP_error_present':'eat_everything_origin' in text or 'eep_events.txt' in text,
 'full_government_acceptance_claimed':False,'release_claimed':False}
out=Path('eat_everything_origin/docs/evidence')/('rc9-full-run-'+root.name+'-git-object-check.json')
assert not out.exists();out.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(v))
