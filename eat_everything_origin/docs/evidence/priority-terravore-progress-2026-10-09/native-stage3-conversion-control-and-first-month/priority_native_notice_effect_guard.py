"""Read-only native greeting, hive progress and tutorial acknowledgement."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,eid,event,option,pre_file,pre_stage=sys.argv[1:];eid,option=int(eid),int(option)
allowed={('action.1',2):'on_action_events_1.txt',('progress.4',5):'progress_events.txt',('tutorial.63',0):'tutorial_events.txt'}
assert (event,option) in allowed
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def obj(t):return {k:v for k,v,o in q.fields(t) if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,obj(t)
b,bt,br=read(before);a,at,ar=read(after);bc,ac=obj(br['country']),obj(ar['country']);bp,ap=vals(bt,'player_event'),vals(at,'player_event')
pre=json.loads((run/pre_file).read_text('utf-8'));target=[v for v in bp if q.scalars(v).get('id')==eid and q.scalars(v).get('event')==event and q.scalars(v).get('country')==0]
source=h.GAME_EXE.parent/'events'/allowed[(event,option)];ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')==event];assert len(ev)==1
opts=vals(ev[0],'option');native_option=opts[option]
greeting=event=='action.1';flag='first_contact_event' if greeting else 'tutorial_63' if event=='tutorial.63' else None
children=[v for v in ap if q.scalars(v).get('id')==141 and q.scalars(v).get('event')=='progress.4' and q.scalars(v).get('country')==0] if greeting else []
skip={'country','player_event','message','open_player_event_selection_history'}|({'spy_networks','last_event_id'} if greeting else set())
checks={'same_date_original_SHA':a['date']==b['date']=='2239.10.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'prior_PASS_exit0':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/(pre_stage+'-execution.json')).read_text('utf-8'))['returncode']==0,
 'exact_pending_removal_native_child_only':len(target)==1 and len(children)==int(greeting) and ap==[v for v in bp if v not in target]+children,
 'exact_once_selection_history':selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':option}],
 'all_other_ordered_top_level_raw_held':omit(bt,skip)==omit(at,skip),
 'all_other_countries_raw_held':set(bc)==set(ac) and all(ac[i]==v for i,v in bc.items() if i not in (['0','1'] if greeting else ['0'])),
 'country0_only_native_flag_effect':omit(bc['0'],{'flags'})==omit(ac['0'],{'flags'}) and (omit(q.block(bc['0'],'flags'),{flag})==omit(q.block(ac['0'],'flags'),{flag}) and q.scalars(q.block(ac['0'],'flags')).get(flag)==63151464 if flag else bc['0']==ac['0']),
 'unfiltered_current_error_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()}
bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==eid and q.scalars(v).get('receiver')==0];added=[v for v in am if q.scalars(v).get('event')==141 and q.scalars(v).get('receiver')==0] if greeting else []
checks['only_corresponding_messages_changed']=len(removed)<=1 and len(added)==int(greeting) and am==[v for v in bm if v not in removed]+added
if greeting:
 checks['global_event_ID140_to141']=q.scalars(bt)['last_event_id']==140 and q.scalars(at)['last_event_id']==141
 checks['native_hostile_source_effect']=q.scalars(q.block(q.block(native_option,'else'),'event_target:contact_empire').strip()).get('add_opinion_modifier') is None and 'opinion_hostile_first_comms_greeting' in native_option and 'first_comms_hostility_preparations' in native_option and 'years = 15' in native_option and 'id = progress.4' in q.block(ev[0],'after')
 checks['country1_only_relations_changed']=omit(bc['1'],{'relations_manager'})==omit(ac['1'],{'relations_manager'})
 brel,arel=vals(q.block(bc['1'],'relations_manager'),'relation'),vals(q.block(ac['1'],'relations_manager'),'relation');rr=[v for v in brel if q.scalars(v).get('country')==0];ss=[v for v in arel if q.scalars(v).get('country')==0]
 newmods=[v for v in vals(ss[0],'modifier') if v not in vals(rr[0],'modifier')]
 checks['exact_native_hostile_opinion_added']=len(rr)==len(ss)==len(newmods)==1 and q.scalars(newmods[0])=={'modifier':'opinion_hostile_first_comms_greeting','start_date':'2239.10.02','value':-50,'decay':'yes'} and omit(rr[0],{'modifier'})==omit(ss[0],{'modifier'}) and vals(ss[0],'modifier')==vals(rr[0],'modifier')+newmods and [v for v in brel if v not in rr]==[v for v in arel if v not in ss]
 bs,ass=obj(br['spy_networks']),obj(ar['spy_networks']);changed=[i for i,v in bs.items() if ass.get(i)!=v];timed=q.block(q.block(ass['16777376'],'timed_modifiers'),'items')
 checks['exact_existing_spynetwork_15year_modifier']=set(bs)==set(ass) and changed==['16777376'] and q.scalars(bs['16777376'])=={'owner':0,'target':1} and omit(ass['16777376'],{'timed_modifiers'})==list(q.fields(bs['16777376'])) and q.scalars(timed.strip()[1:-1])=={'modifier':'first_comms_hostility_preparations','days':5400}
else:
 checks['native_option_only_expected_effect']=all(k in ['name','trigger','hidden_effect'] for k,v,o in q.fields(native_option)) and (q.scalars(q.block(native_option,'hidden_effect'))=={'set_country_flag':'tutorial_63'} if flag else not q.block(native_option,'hidden_effect'))
for k in ['effective_stockpile','variables','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_NOTICE_EFFECT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'event':event,'event_id':eid,'option_index':option,'native_source':{'path':str(source),'sha256':h.sha256(source)},'remaining_country0_pending':[(q.scalars(v)['id'],q.scalars(v)['event']) for v in ap if q.scalars(v).get('country')==0],'scope':'Native selected event effects only; no economic, research or EEP grant. Calendar requires no remaining pending events.'}
out=run/(after+'-notice-effect-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original notice-effect FAIL retained'
