import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime,timezone
source=Path('_runtime/heart-of-devouring/runs/20261007T215509Z')
user=Path('C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261007T215509Z')
target=Path('eat_everything_origin/docs/evidence/runtime-development/20261007T215509Z-completed-checkpoints')
assert not target.exists()
shutil.copyfile(Path(__file__),source/Path(__file__).name)
target.mkdir(parents=True)
(target/'.gitattributes').write_text('* binary\n**/* binary\n',encoding='utf-8')
entries=[]
def take(path,name):
    data=path.read_bytes()
    destination=target/name
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(data)
    digest=hashlib.sha256(data).hexdigest()
    assert hashlib.sha256(destination.read_bytes()).hexdigest()==digest
    entries.append({'path':name,'source':str(path.resolve()),'bytes':len(data),'sha256':digest})
for path in sorted(source.rglob('*')):
    if path.is_file() and not path.relative_to(source).as_posix().startswith('rc8-hiveworld-terraform-five-real-years'):
        take(path,path.relative_to(source).as_posix())
for name in ['dlc_load.json','pdx_settings.txt','settings.txt','dlc_signature','settings-layout.json']:
    path=user/name
    if path.is_file(): take(path,'userdir-config/'+name)
error=user/'logs/error.log'
take(error,'stage-full-error-through-terraform-paid.log')
content=(target/'stage-full-error-through-terraform-paid.log').read_text(encoding='utf-8-sig',errors='replace')
assert 'Wrong scope for trigger' not in content
manifest={'status':'SNAPSHOT_BYTE_VERIFIED','snapshot_at_utc':datetime.now(timezone.utc).isoformat(),
    'run':'20261007T215509Z','version':'0.2.0-rc.8','language':'l_simp_chinese',
    'scope':'All generated completed-checkpoint files; current ongoing five-year prefix excluded. Partial run snapshot, not final run archive.',
    'excluded_currently_writing_prefix':'rc8-hiveworld-terraform-five-real-years',
    'original_files':len(entries),'original_bytes':sum(v['bytes'] for v in entries),'files':entries,
    'complete_stage_error_scope_errors':0,'final_error_log_required_after_normal_stop':True,
    'original_failures_preserved':['rc8_panels_and_nonqualified_control.py country top-level origin KeyError',
        'rc8_natural_hiveworld_ap_save.py integer-cost assertion FAIL',
        'rc8_natural_geothermal_queue.py all colonies assertion FAIL',
        'rc8_prove_geothermal_queue.py item_mgr container KeyError',
        'rc8_natural_terraform_paid_save.py strict research stock assertion FAIL']}
(target/'source-snapshot.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in manifest.items() if k!='files'},ensure_ascii=True))
