"""Read-only exact two first-contact acknowledgements and no economic awards."""
import json,logging,shutil,sys,zipfile,re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-colonization-wait-year2';after='terravore-contacts-ack'
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
 contacts={k:v for k,v,o in q.fields(q.block(roots['first_contacts'],'contacts')) if o}
 return a,t,roots,pending,contacts
b,bt,br,bp,bf=read(before);a,at,ar,ap,af=read(after);bc,ac=b['countries']['0'],a['countries']['0'];b0,a0=bf['0'],af['0']
changed={'stage','status','clues','event','completed'}
checks={'same_actual_date':a['date']==b['date']=='2206.05.01','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'only_pending5_6_removed':[(v['id'],v['event']) for v in bp]==[(5,'first_contact_critters.80'),(6,'first_contact.1')] and not ap,
 'two_once_normal_histories':selected_history(at)==selected_history(bt)+[{'player_event':5,'human':1,'option':0},{'player_event':6,'human':1,'option':0}],
 'contact0_exact_native_stage_unlock':q.scalars(b0)['stage']=='void_clouds_stage_1' and q.scalars(a0)['stage']=='void_clouds_stage_2' and q.scalars(b0)['status']=='locked' and q.scalars(a0)['status']=='in_progress' and q.scalars(b0)['clues']==7 and q.scalars(a0)['clues']==0 and not q.block(a0,'event'),
 'contact0_other_fields_held':[(k,v,o) for k,v,o in q.fields(b0) if k not in changed]==[(k,v,o) for k,v,o in q.fields(a0) if k not in changed],
 'contact0_exact_completed_stage_added':[t for t,_,_ in q.tokens(q.block(a0,'completed'))]==[t for t,_,_ in q.tokens(q.block(b0,'completed'))]+['{','date','=','"2206.05.01"','stage','=','"void_clouds_stage_1"','}'],
 'contact1_only_event_removed':bool(q.block(bf['1'],'event')) and not q.block(af['1'],'event') and [(k,v,o) for k,v,o in q.fields(bf['1']) if k!='event']==list(q.fields(af['1'])),
 'all_other_contacts_held':set(af)==set(bf) and all(af[i]==v for i,v in bf.items() if i not in ['0','1']),
 'native_full_country_raw_held':q.block(br['country'],'0')==q.block(ar['country'],'0'),
 'no_new_errors':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-colonization-wait-year2-error-before.log').read_bytes()}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_FIRST_CONTACT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'scope':'Only original contact0 stage/unlock and two selected histories. No EEP or native economic award; not contact completion or full route.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original first contact difference retained; do not replay'
