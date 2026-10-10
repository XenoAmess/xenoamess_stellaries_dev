"""Strict normal empty-effect acknowledgement, retain all other pending events."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,eid,event,option,pre_file,pre_stage,childid=sys.argv[1:];eid,option,childid=int(eid),int(option),int(childid)
allowed={('action.13',0):'on_action_events_1.txt'};assert (event,option) in allowed
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
b,bt,bf,br=read(before);a,at,af,ar=read(after);pre=json.loads((run/pre_file).read_text('utf-8'));bp=[v for k,v,o in bf if k=='player_event' and o];ap=[v for k,v,o in af if k=='player_event' and o];target=[v for v in bp if q.scalars(v).get('id')==eid and q.scalars(v).get('country')==0 and q.scalars(v).get('event')==event]
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message'];removed=[v for v in bm if q.scalars(v).get('event')==eid and q.scalars(v).get('receiver')==0]
source=h.GAME_EXE.parent/'events'/allowed[(event,option)];ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')==event];assert len(ev)==1;opts=[v for k,v,o in q.fields(ev[0]) if k=='option' and o]
skip={'player_event','open_player_event_selection_history','message','first_contacts','last_event_id'};omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
bc,ac=[q.block(rt.get('first_contacts',''),'contacts') for rt in [br,ar]];bcs,acs=[{k:v for k,v,o in q.fields(v) if o} for v in [bc,ac]];changed=[i for i,v in bcs.items() if acs.get(i)!=v]
children=[v for v in ap if q.scalars(v).get('id')==childid and q.scalars(v).get('country')==0 and q.scalars(v).get('event')=='action.1'];added=[v for v in am if q.scalars(v).get('event')==childid and q.scalars(v).get('receiver')==0]
sc=q.block(children[0],'scope') if len(children)==1 else '';targets=[]
while sc:
 targets.extend(q.scalars(v) for k,v,o in q.fields(sc) if k=='saved_event_target' and o);sc=q.block(sc,'from')

original=json.loads((run/(after+'-contact-forward-proof.json')).read_text('utf-8'));original_ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'));checks={'original_28_exact_one_FAIL_retained':len(original['checks'])==28 and [k for k,v in original['checks'].items() if v is not True]==['all_other_top_level_raw_held'] and original_ex['returncode']==1 and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'],'global_event_ID_exact_139_to_child140':q.scalars(bt)['last_event_id']==139 and q.scalars(at)['last_event_id']==childid==140,'same_actual_date':a['date']==b['date'],'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],'bound_prior_PASS_exit0':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/(pre_stage+'-execution.json')).read_text('utf-8'))['returncode']==0,
 'native_option_forwards_only_action1':[(k,o) for k,v,o in q.fields(opts[option]) if k not in ['name','trigger']]==[('hidden_effect',True)] and q.scalars(q.block(q.block(opts[option],'hidden_effect'),'country_event'))=={'id':'action.1'},
 'only_parent_replaced_by_exact_native_child':len(target)==len(children)==1 and ap==[v for v in bp if v not in target]+children and {v['name']:(v['type'],v['id']) for v in targets}=={'contact_empire':('country',1),'contact_speaker':('country',1)},
 'exact_once_native_selection_history':selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':option}],
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in skip]==[(k,v,o) for k,v,o in af if k not in skip],
 'all_countries_raw_held':br['country']==ar['country'],
 'only_parent_message_replaced_with_child_message':len(removed)==len(added)==1 and all(q.scalars(v)['type']=='EVENT_MESSAGE_TYPE' for v in removed+added) and am==[v for v in bm if v not in removed]+added,
 'first_contacts_only_matching_event_removed':set(bcs)==set(acs) and len(changed)<=1 and all(q.scalars(bcs[i]).get('owner')==0 and q.scalars(q.block(bcs[i],'event')).get('player_event')==eid and not q.block(acs[i],'event') and omit(bcs[i],{'event'})==list(q.fields(acs[i])) for i in changed) and omit(br.get('first_contacts',''),{'contacts'})==omit(ar.get('first_contacts',''),{'contacts'}),
 'unfiltered_current_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_ACTION13_FORWARD_COMPONENT_V2' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'event':event,'event_id':eid,'option_index':option,'native_source':{'path':str(source),'sha256':h.sha256(source)},'remaining_country0_pending':[(q.scalars(v)['id'],q.scalars(v)['event']) for v in ap if q.scalars(v).get('country')==0],'scope':'Normal action.13 option0 replaces parent136 by native action.1 child140 and exact local targets; all other pending and actual state held. Greeting not yet selected, no calendar clearance.'};out=run/(after+'-contact-forward-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original empty native acknowledgement FAIL retained'
