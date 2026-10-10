"""Exact normal hive death acknowledgement, with original native modifier and deferred clone flag."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-yodd-transit-year1';after='terravore-raid-paragon213-ack'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
b,bt,bf,br=read(before);a,at,af,ar=read(after)
omit=lambda v,ks:[(k,x,o) for k,x,o in q.fields(v) if k not in ks]
objects=lambda v:{k:x for k,x,o in q.fields(v)}
pre=json.loads((run/(before+'-raid-observation-v2-proof.json')).read_text('utf-8'))
bc,ac=[q.block(rt['country'],'0') for rt in [br,ar]]
bp,ap=[[v for k,v,o in fs if k=='player_event' and o] for fs in [bf,af]]
target=[v for v in bp if q.scalars(v).get('id')==213 and q.scalars(v).get('event')=='paragon.571' and q.scalars(v).get('country')==0]
bm,am=[[v for k,v,o in fs if k=='message'] for fs in [bf,af]]
removed=[v for v in bm if q.scalars(v).get('event')==213 and q.scalars(v).get('receiver')==0]
checks={
 'same_actual_date':b['date']==a['date']=='2261.07.02',
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'bound_22_observation_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_NATIVE_RAID_OBSERVATION_COMPONENT' and len(pre['checks'])==22 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pre['calendar_ready'] is False and json.loads((run/(before+'-raid-observation-guard-v2-execution.json')).read_text('utf-8'))['returncode']==0,
 'exact_213_only_removed_other_pending_raw_held':len(target)==1 and ap==[v for v in bp if v not in target] and [(q.scalars(v)['id'],q.scalars(v)['event']) for v in ap if q.scalars(v).get('country')==0]==[(211,'first_contact.1'),(214,'first_contact.1')],
 'exact_once_normal_selection':selected_history(at)==selected_history(bt)+[{'player_event':213,'human':1,'option':0}],
 'only_exact_event_message_removed':len(removed)==1 and q.scalars(removed[0])['type']=='EVENT_MESSAGE_TYPE' and am==[v for v in bm if v not in removed],
 'all_other_top_level_ordered_raw_held':[(k,v,o) for k,v,o in bf if k not in {'country','leaders','fleet','starbase_mgr','player_event','message','open_player_event_selection_history'}]==[(k,v,o) for k,v,o in af if k not in {'country','leaders','fleet','starbase_mgr','player_event','message','open_player_event_selection_history'}],
 'country0_only_timed_modifier':omit(bc,{'timed_modifier'})==omit(ac,{'timed_modifier'}),
 'all_other_countries_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
}
def mods(country):
 raw=q.block(q.block(country,'timed_modifier'),'items');matches=list(re.finditer(r'\{[^{}]*\}',raw));assert not re.sub(r'\{[^{}]*\}','',raw).strip();return [x.group()[1:-1] for x in matches]
bmods,amods=mods(bc),mods(ac)
checks['exact_five_year_hive_modifier_appended_old_raw_held']=len(amods)==len(bmods)+1 and amods[:-1]==bmods and q.scalars(amods[-1])=={'modifier':'paragon_death_the_hive_endures','days':1800} and omit(q.block(bc,'timed_modifier'),{'items'})==omit(q.block(ac,'timed_modifier'),{'items'})
bl,al=[objects(rt['leaders']) for rt in [br,ar]]
checks['deferred_clone_exact_450_to482_only']=set(bl)==set(al) and q.scalars(bl['150995190'])['leader_flags']==450 and q.scalars(al['150995190'])['leader_flags']==482 and omit(bl['150995190'],{'leader_flags'})==omit(al['150995190'],{'leader_flags'}) and all(v==al[i] for i,v in bl.items() if i!='150995190')
bfl,afl=[objects(rt['fleet']) for rt in [br,ar]]
dirty={'0','1','2','136','137','138','139','140','161','166','167','172','178','183','196','198','477','490','602','16777797'}
checks['exact20_native_dirty_flags_only']=set(bfl)==set(afl) and {i for i,v in bfl.items() if v!=afl[i]}==dirty and all(omit(bfl[i],{'properties'})==omit(afl[i],{'properties'}) and omit(q.block(afl[i],'properties'),{'dirty_cloaking_strength'})==list(q.fields(q.block(bfl[i],'properties'))) and q.scalars(q.block(afl[i],'properties')).get('dirty_cloaking_strength')=='yes' for i in dirty)
bs,ass=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]]
checks['exact_native_starbase0_update2048_only']=omit(bs,{'update_flag'})==omit(ass,{'update_flag'}) and 'update_flag' not in q.scalars(bs) and q.scalars(ass)['update_flag']==2048 and omit(q.block(br['starbase_mgr'],'starbases'),{'0'})==omit(q.block(ar['starbase_mgr'],'starbases'),{'0'}) and omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'})
for k in ['effective_stockpile','research_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:
 checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:
 checks[k+'_held']=b[k]==a[k]
checks['actual_original_scientist_held']=q.block(br['ships'],'1')==q.block(ar['ships'],'1') and q.scalars(q.block(ar['ships'],'1'))['leader']==150994969
checks['unfiltered_error2670_held']=(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670
action=json.loads((run/'terravore-raid-paragon213-click.action.json').read_text('utf-8'))
checks['actual_normal_click_and_save_exit0']=action['action']=='left-click' and action['client_point']==[510,491] and action['foreground_after']==action['expected_hwnd'] and all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-raid-paragon213-click-execution',after+'-save'])
source=h.GAME_EXE.parent/'events/paragon_events.txt';static=h.GAME_EXE.parent/'common/static_modifiers/16_static_modifiers_paragon.txt'
event=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='paragon.571'];assert len(event)==1
opt=q.block(event[0],'option');effect=q.block(q.block(opt,'else'),'add_modifier')
checks['original_native_option_and_after_cleanup_source']=h.sha256(source)=='5dc68cbce05d753590dba3d33d5d3e1c41ccaac7106a239c6cbc64f84dbccdc1' and q.scalars(effect)=={'modifier':'paragon_death_the_hive_endures','years':5} and q.scalars(q.block(q.block(q.block(event[0],'after'),'from'),'kill_leader'))=={'show_notification':'no'}
checks['native_modifier_exact_leader_benefits']=q.scalars(q.block(static.read_text('utf-8-sig'),'paragon_death_the_hive_endures'))=={'country_leader_pool_size':1,'species_leader_exp_gain':0.25}
proof={'status':'PASS_TERRAVORE_NATIVE_PARAGON571_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'native_sources':[{'path':str(p),'sha256':h.sha256(p)} for p in [source,static]],'remaining_country0_pending':[211,214],'scope':'Only normal native paragon.571 option, exact five-year leader modifier and deferred clone flag. Real raid unresolved, no EEP reward or calendar clearance.'}
out=run/(after+'-paragon571-ack-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original paragon571 acknowledgement FAIL retained'
