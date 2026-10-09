import hashlib,json,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools')
import audit_save as q
from native_selected_history import selected_history
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');shutil.copyfile(__file__,run/Path(__file__).name)
hs=Path(__file__).parent/'native_selected_history.py';hd=run/hs.name
if not hd.exists():shutil.copyfile(hs,hd)
assert hd.read_bytes()==hs.read_bytes()
before='organic-mine4-completed';after='organic-mine4-native-crime-ack'
def read(stem):
    a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    return a,t
b,bt=read(before);a,at=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pending=lambda t:[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
err=run/(after+'-stderr.txt');original=err.read_bytes();eb=(run/(after+'-error-before.log')).read_bytes();ea=(run/(after+'-error-after.log')).read_bytes()
checks={'same_actual_date':a['date']==b['date']=='2305.01.02','no_new_errors':eb==ea,'actual_pending420_only_removed':len(pending(bt))==1 and pending(bt)[0]['id']==420 and not pending(at),'actual_history_prefix_and_one_human_option0':selected_history(at)==selected_history(bt)+[{'player_event':420,'human':1,'option':0}],'original_parser_error_bytes_held':err.read_bytes()==original and b'unexpected delimiter at field boundary' in original}
for k in ('effective_stockpile','research_stockpile','tech_status','variables','flags','completed_technologies','research_queues','research_progress_by_tech','traditions','ascension_perks','government','owned_colonies'):checks[k+'_held']=bc[k]==ac[k]
for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species'):checks[k+'_held']=a[k]==b[k]
p={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'history_added':selected_history(at)[len(selected_history(bt)):],'original_parser_stderr_sha256':hashlib.sha256(original).hexdigest(),'scope':'Independent read-only proof of already executed crime40 acknowledgement; original parser error unchanged, no new game input or replay.'};out=run/(after+'-independent-proof.json');assert not out.exists();out.write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');print(json.dumps(p),flush=True);assert all(checks.values())
