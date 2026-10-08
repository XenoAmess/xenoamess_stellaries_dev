import hashlib,json,shutil
from pathlib import Path
from datetime import datetime,timezone
source=Path('_runtime/heart-of-devouring/runs/20261008T003349Z')
target=Path('eat_everything_origin/docs/evidence/runtime-development/20261008T003349Z-natural-stage2-completed')
assert not target.exists()
names=['rc9-stage2-natural-war80-restored-source-precondition-proof.json','rc9-stage2-existing-war-orders-proof.json',
 'rc9-stage2-original-transport-count-orders-proof.json','rc9-stage2-original-fleet-hold-at-star-proof.json',
 'rc9-stage2-native-landing-order-proof.json','rc9-stage2-natural-conquered-source12-begin-scoped-proof.json',
 'rc9-stage2-natural-source12-calendar-settlement-proof.json','rc9-stage2-native-first-queen-reload-proof.json',
 'rc9-stage2-native-first-queen-ack-proof.json','rc9-stage2-native-first-queen-five-replays-preconditions.json',
 'rc9-stage2-native-first-queen-five-replays-proof.json','rc9-stage2-completed-first-queen-calendar-proof.json']
count=0
for name in names:
    data=json.loads((source/name).read_text(encoding='utf-8'))
    assert data['status'] in ['PASS_SCOPED','SOURCE_RESTORED'],(name,data['status'])
    checkpoints=data.get('checkpoints',[data])
    for cp in checkpoints:
        assert all(cp['checks'].values()),name
        count+=len(cp['checks'])
shutil.copyfile(Path(__file__),source/Path(__file__).name)
target.mkdir(parents=True)
(target/'.gitattributes').write_text('* binary\n**/* binary\n',encoding='utf-8')
entries=[]
def take(path,name):
    data=path.read_bytes();out=target/name;out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists()
    out.write_bytes(data);digest=hashlib.sha256(data).hexdigest();assert hashlib.sha256(out.read_bytes()).hexdigest()==digest
    entries.append({'path':name,'source':str(path.resolve()),'bytes':len(data),'sha256':digest})
extras={'manifest.json','process.json','rc9-original-native-source-preflight.json','rc9-recovery-extra-source-preflight.json',
 'rc9_restore_native_source.py','rc9_forward_native_days.py',Path(__file__).name}
for path in sorted(source.rglob('*')):
    if path.is_file() and (path.name.startswith(('rc9-stage2','rc9_stage2')) or path.name in extras):
        take(path,path.relative_to(source).as_posix())
take(Path('_runtime/heart-of-devouring/runs/20261007T031421Z/native-psi80-natural.sav'),'original-natural-war80-source.sav')
take(Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261008T003349Z/logs/error.log'),'stage-full-error-through-natural-stage2.log')
meta={'status':'SNAPSHOT_BYTE_VERIFIED','snapshot_at_utc':datetime.now(timezone.utc).isoformat(),'run':source.name,
 'version':'0.2.0-rc.9','language':'l_simp_chinese','scope':'Original existing natural war and troops, real conquest and Q12 29-month swallow, native level2 and first Queen fleet notification, reload/ack/replay/real next day/month. Not full civic acceptance or final run log.',
 'original_files':len(entries),'original_bytes':sum(e['bytes'] for e in entries),'checked_reports':len(names),
 'checks_passed':count,'proof_files':names,'natural_stage2_first_notice_complete':True,'first_release_complete':False,
 'final_error_log_required_after_normal_stop':True,
 'preserved_failures':['rc9-stage2-original-transport-orders-proof.json','rc9-stage2-natural-conquered-source12-begin-proof.json'],
 'files':entries}
(target/'source-snapshot.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in meta.items() if k!='files'}),flush=True)
