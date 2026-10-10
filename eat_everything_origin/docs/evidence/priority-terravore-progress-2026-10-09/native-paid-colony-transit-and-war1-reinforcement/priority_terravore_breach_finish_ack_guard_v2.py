"""Actual native2800 after: exact breach flags, one killed situation, no reward."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-breach-finish-pending';after='terravore-native-breach-finish-ack'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
b,bt,br=read(before);a,at,ar=read(after);pre=json.loads((run/(before+'-finish-pending-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-supplement-execution.json')).read_text('utf-8'))
bp,ap=vals(bt,'player_event'),vals(at,'player_event');target=[v for v in bp if q.scalars(v)=={'id':201,'event':'shroud.2800','date':'2260.12.01','country':0}]
bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==201 and q.scalars(v).get('receiver')==0]
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];bs,ass=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]]
checks={
 'bound_prior10_PASS_exit0_SHA':pre['status']=='PASS_NATIVE_TERRAVORE_BREACH_FINISH_PENDING_COMPONENT' and len(pre['checks'])==10 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date']=='2258.09.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'unique_pending201_removed_no_new_country0_pending':len(target)==1 and ap==[v for v in bp if v not in target] and not [v for v in ap if q.scalars(v).get('country')==0],
 'exact_once_human1_option0_history':selected_history(at)==selected_history(bt)+[{'player_event':201,'human':1,'option':0}],
 'only_matching_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
 'all_other_ordered_top_raw_held':omit(bt,{'country','situations','player_event','message','open_player_event_selection_history'})==omit(at,{'country','situations','player_event','message','open_player_event_selection_history'}),
 'country0_only_two_native_breach_flags_appended':list(q.fields(q.block(acr,'flags')))==list(q.fields(q.block(bcr,'flags')))+[('breached_shroud','63314904',False),('psionic_traditions_unlocked','63314904',False)] and omit(bcr,{'flags'})==omit(acr,{'flags'}),
 'all_other_countries_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'only_native16777221_killed_marker_added':q.scalars(ass).get('killed')=='yes' and 'killed' not in q.scalars(bs) and omit(bs,{'killed'})==omit(ass,{'killed'}),
 'all_other_situations_and_manager_raw_held':omit(q.block(br['situations'],'situations'),{'16777221'})==omit(q.block(ar['situations'],'situations'),{'16777221'}) and omit(br['situations'],{'situations'})==omit(ar['situations'],{'situations'}),
 'actual_full_tree_psionic_species_and_EEP_no_fake_reward':a['species']['73']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_psionic'] and 'tr_psionics_shroud_finish' in a['countries']['0']['traditions'] and a['countries']['0']['variables']==b['countries']['0']['variables'] and a['countries']['0']['variables']['eep_psi']==0 and 'eep_psi_notice' not in a['countries']['0']['flags'],
 'normal_click_save_exit0':all(json.loads((run/(after+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-select','-save']) and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['client_point']==[510,579],
 'unfiltered_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2800'];assert len(ev)==1;end=q.block(ev[0],'after');owner=q.block(q.block(end,'hidden_effect'),'owner');branch=q.block(owner,'if');opts=vals(ev[0],'option')
checks['native_after_non_shroud_forged_breach_then_flag_and_destroy']=q.scalars(a['countries']['0']['government']).get('origin')=='origin_heart_of_devouring' and q.scalars(q.block(branch,'limit'))=={'has_origin':'origin_shroud_forged'} and q.scalars(q.block(owner,'else'))=={'breach_shroud':'yes'} and q.scalars(owner)=={'set_country_flag':'psionic_traditions_unlocked'} and [(k,o) for k,v,o in q.fields(owner)]==[('if',True),('else',True),('set_country_flag',False)] and q.scalars(end)=={'destroy_situation':'this'} and [(k,o) for k,v,o in q.fields(end)]==[('hidden_effect',True),('destroy_situation',False)]
checks['native_unique_option_only_tooltip_and_inapplicable_origin_contact']=len(opts)==1 and [(k,o) for k,v,o in q.fields(opts[0])]==[('name',False),('custom_tooltip',False),('owner',True)] and q.scalars(q.block(q.block(q.block(opts[0],'owner'),'if'),'limit'))=={'has_origin':'origin_shroud_forged'}
oldex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
checks['bound_original_attribute_error_exit1_no_proof']=oldex['returncode']==1 and oldex['helper_sha256']=='2fc3f05f715087b093eb6ccd20a5767ae3506eedcd3be1bec2b2e8278458b186' and (run/(after+'-guard-stdout.txt')).read_bytes()==b'' and b"AttributeError: 'str' object has no attribute 'get'" in (run/(after+'-guard-stderr.txt')).read_bytes() and not (run/(after+'-full-breach-ack-proof.json')).exists()
p={'status':'PASS_NATIVE_TERRAVORE_FULL_BREACH_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not [v for v in ap if q.scalars(v).get('country')==0],'native_source':{'path':str(source),'sha256':h.sha256(source)},'scope':'Actual normal2800 option0 and after, complete native breach flags and deferred killed marker. No EEP psi reward or Queen notice until monthly check; not full civic route.'}
out=run/(after+'-full-breach-ack-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original breach ACK FAIL retained'
