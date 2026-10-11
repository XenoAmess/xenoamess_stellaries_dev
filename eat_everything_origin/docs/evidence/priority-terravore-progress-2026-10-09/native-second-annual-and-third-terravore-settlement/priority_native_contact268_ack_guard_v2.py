"""Strict normal empty-effect acknowledgement, retain all other pending events."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];eid,event,option=268,'first_contact.1',0
pre_file='terravore-interannual-months2-step3-interannual-contact-boundary-proof.json';pre_stage='terravore-interannual-months2-step3-contact-boundary-observer'
allowed={('first_contact.1',0):'first_contact_events.txt'};assert (event,option) in allowed
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
skip={'player_event','open_player_event_selection_history','message','first_contacts','fleet'};omit=lambda t,ks:[(k,v,o) for k,v,o in q.fields(t) if k not in ks]
bc,ac=[q.block(rt.get('first_contacts',''),'contacts') for rt in [br,ar]];bcs,acs=[{k:v for k,v,o in q.fields(v) if o} for v in [bc,ac]];changed=[i for i,v in bcs.items() if acs.get(i)!=v]
checks={'same_actual_date':a['date']==b['date'],'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],'bound_prior_PASS_exit0':pre['status']=='PASS_NATIVE_TERRAVORE_INTERANNUAL_CONTACT_BOUNDARY_COMPONENT' and len(pre['checks'])==33 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256']=='b80940f77b462638309c8b282a70e3c49c2a2cadaeb0a334f2558e2643e384ca' and json.loads((run/(pre_stage+'-execution.json')).read_text('utf-8'))['returncode']==0 and json.loads((run/(pre_stage+'-execution.json')).read_text('utf-8'))['helper_sha256']==h.sha256(run/'priority_terravore_interannual_contact_boundary_observer.py')=='045d589c5bffb52b62b3a54d7da125a24464edef9edc45a73dbbae6ac5b174c3',
 'original_native_option_has_no_effect_fields':h.sha256(source)=='17e6402267e019f25b65a419cb2d8afd6666ebb362f9020e747c57551648ca46' and q.scalars(opts[option])=={'name':'INTERESTING'} and not [(k,o) for k,v,o in q.fields(opts[option]) if k not in ['name','trigger','exclusive_trigger','custom_gui','default_hide_option']],
 'only_exact_pending_removed_others_raw_held':len(target)==1 and ap==[v for v in bp if v not in target],
 'exact_once_native_selection_history':selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':option}],
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in skip]==[(k,v,o) for k,v,o in af if k not in skip],
 'all_countries_raw_held':br['country']==ar['country'],
 'only_matching_event_message_removed':len(removed)<=1 and all(q.scalars(v)['type']=='EVENT_MESSAGE_TYPE' for v in removed) and am==[v for v in bm if v not in removed],
 'first_contacts_only_matching_event_removed':set(bcs)==set(acs) and len(changed)<=1 and all(q.scalars(bcs[i]).get('owner')==0 and q.scalars(q.block(bcs[i],'event')).get('player_event')==eid and not q.block(acs[i],'event') and omit(bcs[i],{'event'})==list(q.fields(acs[i])) for i in changed) and omit(br.get('first_contacts',''),{'contacts'})==omit(ar.get('first_contacts',''),{'contacts'}),
 'unfiltered_current_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
action=json.loads((run/('terravore-third-contact268-ack-click.action.json')).read_text('utf-8'))
checks['actual_normal_click_and_save_exit0']=action['action']=='left-click' and action['client_point']==[374,546] and action['foreground_after']==action['expected_hwnd'] and all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-third-contact268-ack-click-execution',after+'-save'])
checks['exact_only_inactive264_remaining']=[(q.scalars(v)['id'],q.scalars(v)['event']) for v in ap if q.scalars(v).get('country')==0]==[(264,'grand_archive.2800')]

original=json.loads((run/'terravore-third-contact268-ack-contact268-info-ack-proof.json').read_text('utf-8'))
original_ex=json.loads((run/'terravore-third-contact268-ack-guard-execution.json').read_text('utf-8'))
cache=json.loads((run/'terravore-third-contact268-ack-fleet64-cache-investigation.json').read_text('utf-8'))
b64,a64=q.block(br['fleet'],'64'),q.block(ar['fleet'],'64')
checks['only_unrelated_caravaneer64_properties_exact_dirty_cloaking_cache']=(
    omit(br['fleet'],{'64'})==omit(ar['fleet'],{'64'}) and omit(b64,{'properties'})==omit(a64,{'properties'})
    and list(q.fields(q.block(b64,'properties')))==[('weapon','yes',False),('mobile','yes',False),('valid_for_combat','yes',False)]
    and list(q.fields(q.block(a64,'properties')))==[('weapon','yes',False),('mobile','yes',False),('valid_for_combat','yes',False),('dirty_cloaking_strength','yes',False)]
    and b64==cache['before_fleet64_raw'] and a64==cache['after_fleet64_raw'] and cache['fleet64_owner_country_ids']==['13']
    and h.sha256(run/'terravore-third-contact268-ack-fleet64-cache-investigation.json')=='9939e2a5f78f5a6a0a6bc520f74f3b07d2feb560f0ec49062cfb199faea80931')
checks['original30_single_raw_FAIL_actual1_source_same_SAV']=(original['status']=='FAIL' and len(original['checks'])==30
    and [k for k,v in original['checks'].items() if v is not True]==['all_other_top_level_raw_held']
    and original_ex['returncode']==1 and original_ex['helper_sha256']==h.sha256(run/'priority_native_contact268_ack_guard.py')=='e250ca6cd2aab1645694e58f6db56c4eab8332e02736e78bb838ef29159a8508'
    and original['before_sha256']==b['save_sha256']=='b80940f77b462638309c8b282a70e3c49c2a2cadaeb0a334f2558e2643e384ca'
    and original['after_sha256']==a['save_sha256']=='6aaa71c99bbd91a7e78b9aec240284864422717055e9fb535f778068b0b5bd01')

p={'status':'PASS_NATIVE_CONTACT268_INFORMATION_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'event':event,'event_id':eid,'option_index':option,'native_source':{'path':str(source),'sha256':h.sha256(source)},'remaining_country0_pending':[(q.scalars(v)['id'],q.scalars(v)['event']) for v in ap if q.scalars(v).get('country')==0],'calendar_ready':False,'scope':'Only specified normal empty native option, all other pending and actual state held. No full-route/calendar clearance while other pending remain.'};out=run/(after+'-contact268-info-ack-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original empty native acknowledgement FAIL retained'
