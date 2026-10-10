"""Read-only three native research automation toggles; exact no-grant state."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-contacts-ack';after='terravore-auto-research'
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
 return a,roots,pending
b,br,bp=read(before);a,ar,ap=read(after);bc,ac=b['countries']['0'],a['countries']['0'];braw=q.block(br['country'],'0');araw=q.block(ar['country'],'0');expected=braw
for area in ['physics','society','engineering']:
 old='auto_researching_'+area+'=no';new='auto_researching_'+area+'=yes';assert braw.count(old)==1;expected=expected.replace(old,new)
checks={'same_actual_date':a['date']==b['date']=='2206.05.01','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_pending':not bp and not ap,'exact_country_only_three_toggles':araw==expected,
 'actual_three_flags_yes':all(q.scalars(ac['tech_status']).get('auto_researching_'+k)=='yes' for k in ['physics','society','engineering']),
 'all_effective_stock_and_banks_held':bc['effective_stockpile']==ac['effective_stockpile'],
 'no_free_technology':bc['completed_technologies']==ac['completed_technologies'],
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-contacts-ack-error-before.log').read_bytes()}
for k in ['variables','flags','traditions','ascension_perks','government','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_RESEARCH_AUTOMATION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_research_queues':ac['research_queues'],'scope':'Only three native auto-research flags; actual queued work after later calendar is separate. No human_ai toggle, AP or grants.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original automation difference retained'
