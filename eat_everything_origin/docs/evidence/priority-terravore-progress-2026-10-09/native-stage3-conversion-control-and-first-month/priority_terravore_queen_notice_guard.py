"""Read-only one normal eep.11 acknowledgment with no additional award."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and q.scalars(v).get('country')==0]
b,bt,bp=read(before);a,at,ap=read(after);bc,ac=b['countries']['0'],a['countries']['0']
checks={'same_actual_date':b['date']==a['date']=='2210.05.01','source_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'unique_eep11_pending18_removed':[(p['id'],p['event']) for p in bp]==[(18,'eep.11')] and not ap,
 'one_normal_option0_history':selected_history(at)==selected_history(bt)+[{'player_event':18,'human':1,'option':0}],
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-first-queen-notice-error-before.log').read_bytes()}
for k in ['effective_stockpile','research_stockpile','variables','flags','tech_status','traditions','ascension_perks','government','owned_colonies','budget']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','deposits','districts','species','situations','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_FIRST_TERRAVORE_QUEEN_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'One normal first-world Queen acknowledgment; all actual economy, populations and EEP state held. Not full civic/ascension/economic route acceptance.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original Queen ACK FAIL retained; do not replay'
