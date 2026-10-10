"""Exact normal native2505 option2, real state and precise modifier caches."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-attunement3-pending';after='terravore-native-attunement3-native-suppression'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
def anonymous(t):
 out=[];depth=0;start=None
 for tok,b,e in q.tokens(t):
  if tok=='{':
   if depth==0:start=e
   depth+=1
  elif tok=='}':
   depth-=1
   if depth==0:out.append(t[start:b])
  elif depth==0:raise ValueError('Expected anonymous object')
 assert depth==0
 return out
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-attunement3-pending-supplement-v2.json')).read_text('utf-8'));ex=json.loads((run/(before+'-supplement-v2-execution.json')).read_text('utf-8'))
bp,ap=vals(bt,'player_event'),vals(at,'player_event');target=[v for v in bp if q.scalars(v)=={'id':194,'event':'shroud.2505','date':'2258.12.01','country':0}]
bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==194 and q.scalars(v).get('receiver')==0]
checks={
 'bound_prior11_PASS_exit0_SHA':pre['status'].startswith('PASS') and len(pre['checks'])==11 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date']=='2256.09.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'unique_pending194_removed_no_new_player_pending':len(target)==1 and q.scalars(q.block(target[0],'scope')).get('id')==16777221 and ap==[v for v in bp if v not in target] and not [v for v in ap if q.scalars(v).get('country')==0],
 'exact_once_human1_option2_history':selected_history(at)==selected_history(bt)+[{'player_event':194,'human':1,'option':2}],
 'only_matching_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
 'all_other_ordered_top_raw_held':omit(bt,{'country','fleet','starbase_mgr','player_event','message','open_player_event_selection_history','random_count'})==omit(at,{'country','fleet','starbase_mgr','player_event','message','open_player_event_selection_history','random_count'}),
 'exact_random_count_plus2':q.scalars(bt)['random_count']==24291849 and q.scalars(at)['random_count']==24291851,
 'normal_click_save_exit0':all(json.loads((run/(after+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-select','-save']) and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['client_point']==[510,582],
 'unfiltered_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];bmd,amd=[q.block(c,'modules') for c in [bcr,acr]]
checks['country_other_raw_and_foreign_raw_held']=omit(bcr,{'modules','timed_modifier'})==omit(acr,{'modules','timed_modifier'}) and omit(br['country'],{'0'})==omit(ar['country'],{'0'})
btm,atm=[q.block(c,'timed_modifier') for c in [bcr,acr]];bitems,aitems=[anonymous(q.block(t,'items')) for t in [btm,atm]]
checks['exact_old_modifier_raw_and_unique3600_day_suppression']=len(bitems)==1 and q.scalars(bitems[0])=={'modifier':'psionic_painkillers_gestalt','days':600} and len(aitems)==2 and aitems[0]==bitems[0] and q.scalars(aitems[1])=={'modifier':'shroud_suppression','days':3600} and omit(btm,{'items'})==omit(atm,{'items'})
bsh,ash=[q.block(v,'standard_shroud_module') for v in [bmd,amd]]
checks['only_exact_two_request_attunement_change']=q.scalars(q.block(bsh,'attunement'))=={'x':-0.15,'y':0.15} and q.scalars(q.block(ash,'attunement'))=={'x':-0.225,'y':0.225} and omit(bsh,{'attunement'})==omit(ash,{'attunement'})
checks['all_other_modules_including_economy_raw_held']=omit(bmd,{'standard_shroud_module'})==omit(amd,{'standard_shroud_module'})
ids={'0','1','2','136','137','138','139','140','161','166','167','171','172','178','183','196','198','477','490','16777797','602'};bf,af=[{k:v for k,v,o in q.fields(rt['fleet'])} for rt in [br,ar]]
checks['exact21_fleet_dirty_cache_only']=bf.keys()==af.keys() and {k for k in bf if bf[k]!=af[k]}==ids and all(omit(bf[k],{'properties'})==omit(af[k],{'properties'}) and not vals(q.block(bf[k],'properties'),'dirty_cloaking_strength') and vals(q.block(af[k],'properties'),'dirty_cloaking_strength')==['yes'] and omit(q.block(bf[k],'properties'),{'dirty_cloaking_strength'})==omit(q.block(af[k],'properties'),{'dirty_cloaking_strength'}) for k in ids)
bs,ass=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]]
checks['exact_native_starbase0_update2048_only']=not vals(bs,'update_flag') and vals(ass,'update_flag')==['2048'] and omit(bs,{'update_flag'})==omit(ass,{'update_flag'}) and omit(q.block(br['starbase_mgr'],'starbases'),{'0'})==omit(q.block(ar['starbase_mgr'],'starbases'),{'0'}) and omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'})
for k in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies','budget_categories']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';mods=h.GAME_EXE.parent/'common/static_modifiers/24_static_modifiers_shroud.txt';variables=h.GAME_EXE.parent/'common/scripted_variables/09_scripted_variables_shroud.txt'
ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2505'];assert len(ev)==1;opts=vals(ev[0],'option');own=q.block(opts[2],'owner')
checks['native_only_legal_homicidal_option2_modifier_and_split_requests']=len(opts)==3 and all(q.scalars(q.block(q.block(o,'allow'),'owner')).get('is_homicidal')=='no' for o in opts[:2]) and not q.block(opts[2],'allow') and q.scalars(q.block(own,'add_modifier'))=={'modifier':'shroud_suppression','years':10} and q.scalars(q.block(own,'add_attunement'))=={'the_eater_of_worlds':'@breach_the_shroud_split_attunement','the_instrument_of_desire':'@breach_the_shroud_split_attunement'} and [(k,o) for k,v,o in q.fields(own)]==[('add_modifier',True),('add_attunement',True)] and not q.block(ev[0],'after') and q.scalars(variables.read_text('utf-8-sig'))['@breach_the_shroud_split_attunement']==75
checks['native_suppression_actual_maintenance_and_speed_modifiers']=q.scalars(q.block(mods.read_text('utf-8-sig'),'shroud_suppression'))=={'planet_telepaths_upkeep_mult':0.1,'breach_the_shroud_situation_progress_speed_mult':-0.1}
p={'status':'PASS_NATIVE_TERRAVORE_2505_SUPPRESSION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not [v for v in ap if q.scalars(v).get('country')==0],'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,mods,variables]],'scope':'One actual legal native2505 option2; exact ten-year modifier, attunement and cache changes only. Next stable month must verify reduced rate and maintenance. No EEP reward or full-route claim.'}
out=run/(after+'-2505-suppression-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original suppression FAIL retained; no replay'
