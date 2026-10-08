import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[];shutil.copyfile(Path(__file__),run/Path(__file__).name)
source=run/'postvanilla-normal-end.sav';alias=user/'save games/acceptance-fixtures/vanilla-ack.sav';assert not alias.exists();shutil.copyfile(source,alias);assert h.sha256(alias)==h.sha256(source)
r.native_load('vanilla-ack','postvanilla-ack-restore-load');a=r.native_save('postvanilla-ack-restored-before','2209.11.01',(0,));assert a['situations']['11']['progress']==1000
h.write_json(run/'postvanilla-ack-restored-before-source.json',{'status':'RESTORED_PENDING_NATIVE_EVENT','original_sha256':h.sha256(source),'alias_sha256':h.sha256(alias),'native_save_sha256':a['save_sha256'],'date':a['date']});print(json.dumps({'status':'RESTORED_PENDING_NATIVE_EVENT','sha256':a['save_sha256']}),flush=True)
