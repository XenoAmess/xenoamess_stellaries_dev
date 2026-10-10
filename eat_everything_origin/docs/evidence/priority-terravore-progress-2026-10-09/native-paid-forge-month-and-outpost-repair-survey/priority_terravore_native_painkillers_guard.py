"""Read-only exact normally paid native psionic painkiller selection."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-attunement1-pending';after='terravore-native-painkillers-paid'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
def anonymous(t):
 depth=0;start=None;out=[]
 for token,beg,end in q.tokens(t):
  if token=='{':
   if depth==0:start=end
   depth+=1
  elif token=='}':
   depth-=1;assert depth>=0
   if depth==0:out.append(t[start:beg])
  elif depth==0:raise ValueError('Unexpected scalar between native anonymous items')
 assert depth==0;return out
b,bt,bf,br=read(before);a,at,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];pre=json.loads((run/(before+'-attunement-pending-supplement.json')).read_text('utf-8'));ex=json.loads((run/(before+'-supplement-execution.json')).read_text('utf-8'))
bp=[v for k,v,o in bf if k=='player_event' and o];ap=[v for k,v,o in af if k=='player_event' and o];target=[v for v in bp if q.scalars(v).get('id')==174 and q.scalars(v).get('event')=='shroud.2420' and q.scalars(v).get('country')==0]
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message'];removed=[v for v in bm if q.scalars(v).get('event')==174 and q.scalars(v).get('receiver')==0]
checks={'same_actual_date':a['date']==b['date']=='2248.05.02','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
'bound_prior10_component_PASS_exit0':pre['status']=='PASS_NATIVE_MEDITATE_ATTUNEMENT_PENDING_COMPONENT' and len(pre['checks'])==10 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
'only_native174_pending_removed_no_new_country0':len(target)==1 and ap==[v for v in bp if v not in target] and not [v for v in ap if q.scalars(v).get('country')==0],
'exact_once_human_option1_history':selected_history(at)==selected_history(bt)+[{'player_event':174,'human':1,'option':1}],
'only_matching_native_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
'all_other_ordered_top_level_raw_held':[x for x in bf if x[0] not in {'country','fleet','starbase_mgr','message','player_event','open_player_event_selection_history','random_count'}]==[x for x in af if x[0] not in {'country','fleet','starbase_mgr','message','player_event','open_player_event_selection_history','random_count'}],
'exact_one_random_counter_increment':q.scalars(bt)['random_count']==119020581 and q.scalars(at)['random_count']==119020582}
click=json.loads((run/'terravore-native-painkillers-paid-select.action.json').read_text('utf-8'));checks['normal_exact_UI_selection_and_save_exit0']=click['action']=='left-click' and click['client_point']==[510,567] and json.loads((run/'terravore-native-painkillers-paid-select-execution.json').read_text('utf-8'))['returncode']==0 and json.loads((run/'terravore-native-painkillers-paid-save-execution.json').read_text('utf-8'))['returncode']==0
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];btm,atm=[q.block(c,'timed_modifier') for c in [bcr,acr]];bmods,amods=[anonymous(q.block(tm,'items')) for tm in [btm,atm]]
checks['only_new_ten_year_native_painkiller_modifier']=len(bmods)==1 and len(amods)==2 and amods[0]==bmods[0] and q.scalars(bmods[0])=={'modifier':'weaponized_psionics_gestalt_modifier','days':2610} and q.scalars(amods[1])=={'modifier':'psionic_painkillers_gestalt','days':3600} and [(k,o) for k,v,o in q.fields(amods[1])]==[('modifier',False),('days',False)] and omit(btm,{'items'})==omit(atm,{'items'})
checks['country_all_raw_except_exact_modifier_and_modules_held']=omit(bcr,{'timed_modifier','modules'})==omit(acr,{'timed_modifier','modules'}) and omit(br['country'],{'0'})==omit(ar['country'],{'0'})
bmodule,amodule=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(c,'standard_economy_module') for c in [bmodule,amodule]];bres,ares=[q.block(c,'resources') for c in [be,ae]];bs,ass=q.scalars(bres),q.scalars(ares)
checks['only_real_energy1000_paid_other_effective_stocks_held']=D(str(bc['effective_stockpile']['energy']))-D(str(ac['effective_stockpile']['energy']))==D('1000') and {k:v for k,v in bc['effective_stockpile'].items() if k!='energy'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='energy'}
checks['only_exact_native_research_mirrors_refreshed']=bs['physics_research']==993.4875 and bs['engineering_research']==1063.2375 and bs['society_research']==1497.85302 and 'physics_research' not in ass and 'engineering_research' not in ass and ass['society_research']==1776.25272==ac['research_stockpile']['society_research'] and omit(bres,{'energy','physics_research','society_research','engineering_research'})==omit(ares,{'energy','physics_research','society_research','engineering_research'})
checks['all_other_economy_and_modules_raw_held']=omit(bmodule,{'standard_economy_module'})==omit(amodule,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'})
for k in ['research_stockpile','tech_status','budget_categories','variables','flags','government','traditions','ascension_perks','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['all_ships_construction_zones_buildings_raw_held']=all(br[k]==ar[k] for k in ['ships','construction','zones','buildings'])
bss,asss=[q.block(rt['starbase_mgr'],'starbases') for rt in [br,ar]];bs0,as0=[q.block(v,'0') for v in [bss,asss]]
checks['only_starbase0_update_flag2048']=omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'}) and omit(bss,{'0'})==omit(asss,{'0'}) and omit(bs0,{'update_flag'})==omit(as0,{'update_flag'}) and 'update_flag' not in q.scalars(bs0) and q.scalars(as0).get('update_flag')==2048
bfl,afl=objs(br['fleet']),objs(ar['fleet']);changed=[i for i,v in bfl.items() if afl.get(i)!=v]
expected=['0','1','2','136','137','138','139','140','161','166','167','171','172','178','183','196','198','477','490','16777797','602']
checks['exact21_fleet_dirty_properties_only']=set(bfl)==set(afl) and set(changed)==set(expected) and all(omit(bfl[i],{'properties'})==omit(afl[i],{'properties'}) and omit(q.block(bfl[i],'properties'),{'dirty_cloaking_strength'})==omit(q.block(afl[i],'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(bfl[i],'properties')) and q.scalars(q.block(afl[i],'properties')).get('dirty_cloaking_strength')=='yes' for i in changed) and [(k,v,o) for k,v,o in q.fields(br['fleet']) if not o]==[(k,v,o) for k,v,o in q.fields(ar['fleet']) if not o]


checks['unfiltered_errors_held']=(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';effects=h.GAME_EXE.parent/'common/scripted_effects/shroud_shadows_scripted_effects.txt';mods=h.GAME_EXE.parent/'common/static_modifiers/24_static_modifiers_shroud.txt';variables=h.GAME_EXE.parent/'common/scripted_variables/09_scripted_variables_shroud.txt'
ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2420'];assert len(ev)==1;opts=[v for k,v,o in q.fields(ev[0]) if k=='option' and o];owner=q.block(opts[1],'owner');eff=q.block(effects.read_text('utf-8-sig'),'add_modifier_psionic_painkillers');vs=q.scalars(variables.read_text('utf-8-sig'))
checks['native_option1_exact_paid1000_ten_year_request']=q.scalars(q.block(owner,'add_modifier_psionic_painkillers'))=={'YEARS':10} and q.scalars(q.block(owner,'add_resource'))=={'energy':-1000} and q.scalars(q.block(owner,'add_attunement'))=={'the_instrument_of_desire':'@breach_the_shroud_full_attunement'} and vs['@breach_the_shroud_full_attunement']==150
checks['native_non_machine_gestalt_modifier_branch_and_unity10percent']=q.scalars(q.block(q.block(q.block(eff,'if'),'else'),'add_modifier'))=={'modifier':'psionic_painkillers_gestalt','years':'$YEARS$'} and q.scalars(q.block(mods.read_text('utf-8-sig'),'psionic_painkillers_gestalt'))=={'country_unity_produces_mult':0.1} and bc['native']['founder_species_ref']==66 and 'trait_lithoid' in str(b['species']['66'])
p={'status':'PASS_NATIVE_TERRAVORE_PAID_PAINKILLERS_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not [v for v in ap if q.scalars(v).get('country')==0],'actual_energy_before_after':[bc['effective_stockpile']['energy'],ac['effective_stockpile']['energy']],'actual_modifiers':[q.scalars(v) for v in amods],'actual_EEP':ac['variables'],'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,effects,mods,variables]],'scope':'One exact paid native painkiller option, no observable attunement storage delta; not monthly income, full Shroud or full-route acceptance.'}
out=run/(after+'-paid-painkillers-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original paid native painkiller FAIL retained'
