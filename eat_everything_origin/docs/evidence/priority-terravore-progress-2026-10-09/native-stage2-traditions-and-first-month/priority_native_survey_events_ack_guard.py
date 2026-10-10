"""Four native informational survey events; read-only strict raw-save checks."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-synchronicity-year4';after='terravore-survey-events-ack'
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0]
 contacts={k:v for k,v,o in q.fields(q.block(roots['first_contacts'],'contacts')) if o}
 return a,t,fs,roots,pending,contacts
b,bt,bfs,br,bp,bf=read(before);a,at,afs,ar,ap,af=read(after)
bh,ah=selected_history(bt),selected_history(at);added=ah[len(bh):]
checks={
 'same_actual_date':a['date']==b['date']=='2223.01.02',
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'exact_original_four_pending_then_none':[(v['id'],v['event']) for v in bp]==[(54,'anomaly.6660'),(60,'toxoids.500'),(61,'advisor.15'),(62,'first_contact.1')] and not ap,
 'exact_once_four_normal_histories':ah[:len(bh)]==bh and len(added)==4 and sorted(added,key=lambda x:x['player_event'])==[{'player_event':i,'human':1,'option':0} for i in [54,60,61,62]],
 'all_other_top_level_fields_raw_held':[(k,v,o) for k,v,o in bfs if k not in ['player_event','open_player_event_selection_history','first_contacts']]==[(k,v,o) for k,v,o in afs if k not in ['player_event','open_player_event_selection_history','first_contacts']],
 'all_country_roots_raw_held':br['country']==ar['country'],
 'contact18_only_event_removed':bool(q.block(bf['18'],'event')) and not q.block(af['18'],'event') and [(k,v,o) for k,v,o in q.fields(bf['18']) if k!='event']==list(q.fields(af['18'])),
 'all_other_contacts_raw_held':set(bf)==set(af) and all(v==af[i] for i,v in bf.items() if i!='18'),
 'first_contacts_outer_fields_held':[(k,v,o) for k,v,o in q.fields(br['first_contacts']) if k!='contacts']==[(k,v,o) for k,v,o in q.fields(ar['first_contacts']) if k!='contacts'],
 'original_unfiltered_error_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-before.log')).read_bytes(),
}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:
 checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:
 checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_FOUR_NATIVE_INFORMATIONAL_SURVEY_EVENTS' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_selected_history_added':added,'scope':'Only four normal informational acknowledgements; no replay, calendar, award or full-route claim.'}
out=run/(after+'-survey-events-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original event acknowledgement difference retained; no replay or next calendar'
