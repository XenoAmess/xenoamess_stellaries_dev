"""Single normal advisor.17 acknowledgement, no economic effects."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
for src in [Path(__file__),Path('_runtime/heart-of-devouring/native_selected_history.py')]:
 dest=run/src.name
 if dest.exists():assert dest.read_bytes()==src.read_bytes()
 else:shutil.copyfile(src,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0]
 return a,t,fs,pending
b,bt,bf,bp=read(before);a,at,af,ap=read(after);bh,ah=selected_history(bt),selected_history(at)
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message'];removed=[v for v in bm if q.scalars(v).get('event')==81 and q.scalars(v).get('receiver')==0]
skip={'player_event','open_player_event_selection_history','message'}
checks={
 'same_actual_date':b['date']==a['date']=='2227.03.02',
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'only_original_advisor81_pending_then_none':[(x['id'],x['event']) for x in bp]==[(81,'advisor.17')] and not ap,
 'exact_once_native_history':ah==bh+[{'player_event':81,'human':1,'option':0}],
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in skip]==[(k,v,o) for k,v,o in af if k not in skip],
 'only_original_exact_advisor_notice_removed':len(removed)<=1 and all(q.scalars(v)['type']=='EVENT_MESSAGE_TYPE' for v in removed) and am==[v for v in bm if v not in removed],
 'all_country_roots_raw_held':q.block(bt,'country')==q.block(at,'country'),
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_COLONIZING_ADVISOR_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_history_added':ah[len(bh):],'removed_original_notices':removed,'scope':'Single informational acknowledgement. Original year2 wait FAIL retained; no colony established or full-route claim.'}
out=run/(after+'-advisor-ack-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original advisor acknowledgement FAIL retained'
