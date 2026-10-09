"""Strict original-byte native Chinese checkpoint reload; no replay or grants."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,alias=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(after+'-error-before.log')).write_bytes(eb)
p=user/'save games/acceptance-fixtures'/(alias+'.sav');assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(run/(before+'.sav'),p);assert h.sha256(p)==b['save_sha256']
r.native_load(alias,after+'-load');a=r.native_save(after,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(after+'-error-after.log')).write_bytes(ea)
def events(stem):
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return [v for k,v,o in q.fields(t) if k=='player_event' and q.scalars(v).get('country')==0],selected_history(t)
bc,ac=b['countries']['0'],a['countries']['0'];checks={'actual_same_date':a['date']==b['date'],'original_alias_SHA':h.sha256(p)==b['save_sha256'],'source_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],'pending_and_selection_history_held':events(before)==events(after),'no_new_error':ea==eb}
for k in ['effective_stockpile','research_stockpile','variables','flags','tech_status','traditions','ascension_perks','government','owned_colonies','budget']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','deposits','districts','species','situations','event_targets']:checks[k+'_held']=b[k]==a[k]
changes={k:{'before':bc[k],'after':ac[k]} for k in ['effective_stockpile','research_stockpile','variables','flags','tech_status','traditions','ascension_perks','government','owned_colonies','budget'] if bc[k]!=ac[k]}
objects={k:{'before':b[k],'after':a[k]} for k in ['pop_groups','pop_jobs','colonies','planets','deposits','districts','species','situations','event_targets'] if b[k]!=a[k]}
proof={'status':'PASS_STRICT_NATIVE_CHECKPOINT_RELOAD_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'alias_sha256':h.sha256(p),'after_sha256':a['save_sha256'],'country_changes':changes,'collection_changes':objects,'scope':'Original-byte native reload of this paused checkpoint only. No calendar/option replay and no full civic route acceptance.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({k:v for k,v in proof.items() if k not in ['country_changes','collection_changes']}),flush=True);assert all(checks.values()),'Original native checkpoint reload FAIL retained; no retry'
