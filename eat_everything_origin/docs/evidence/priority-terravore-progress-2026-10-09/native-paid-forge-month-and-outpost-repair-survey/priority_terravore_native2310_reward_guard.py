"""Exact source-bound native shroud.2310 lithoid mineral reward; read-only."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-attunement2-pending';after='terravore-native-attunement2-native-reward'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-attunement2-pending-supplement.json')).read_text('utf-8'));ex=json.loads((run/(before+'-supplement-execution.json')).read_text('utf-8'))
bp,ap=vals(bt,'player_event'),vals(at,'player_event');target=[v for v in bp if q.scalars(v)=={'id':185,'event':'shroud.2310','date':'2255.05.01','country':0}]
bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==185 and q.scalars(v).get('receiver')==0]
checks={
 'bound_prior10_PASS_exit0_SHA':pre['status']=='PASS_NATIVE_MEDITATE_ATTUNEMENT_PENDING_COMPONENT' and len(pre['checks'])==10 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_actual_date_original_SHA_pair':b['date']==a['date']=='2253.02.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'exact_unique_pending185_removed_no_new_player_pending':len(target)==1 and q.scalars(q.block(target[0],'scope')).get('type')=='situation' and q.scalars(q.block(target[0],'scope')).get('id')==16777221 and ap==[v for v in bp if v not in target] and not [v for v in ap if q.scalars(v).get('country')==0],
 'exact_once_human1_option1_history':selected_history(at)==selected_history(bt)+[{'player_event':185,'human':1,'option':1}],
 'only_matching_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
 'all_other_ordered_top_raw_held':omit(bt,{'country','player_event','message','open_player_event_selection_history','random_count'})==omit(at,{'country','player_event','message','open_player_event_selection_history','random_count'}),
 'exact_random_count_increment':q.scalars(bt)['random_count']==180336040 and q.scalars(at)['random_count']==180336041,
 'real_minerals_exact2000_other_effective_stocks_held':D(str(ac['effective_stockpile']['minerals']))-D(str(bc['effective_stockpile']['minerals']))==D('2000') and {k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'normal_UI_click_and_save_exit0':all(json.loads((run/(after+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-select','-save']) and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['client_point']==[510,582],
 'unfiltered_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];bmod,amod=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(c,'standard_economy_module') for c in [bmod,amod]];bres,ares=[q.block(c,'resources') for c in [be,ae]];bs,ass=q.scalars(bres),q.scalars(ares)
checks['all_other_country_raw_held']=omit(bcr,{'modules'})==omit(acr,{'modules'}) and omit(br['country'],{'0'})==omit(ar['country'],{'0'})
checks['only_exact_economy_mirrors_refreshed']=bs['physics_research']==485.705 and bs['engineering_research']==519.805 and bs['society_research']==3077.16017 and 'physics_research' not in ass and 'engineering_research' not in ass and ass['society_research']==3214.93671==ac['research_stockpile']['society_research'] and omit(bres,{'minerals','physics_research','society_research','engineering_research'})==omit(ares,{'minerals','physics_research','society_research','engineering_research'}) and omit(be,{'resources'})==omit(ae,{'resources'})
checks['all_other_modules_raw_held']=omit(bmod,{'standard_economy_module','standard_shroud_module'})==omit(amod,{'standard_economy_module','standard_shroud_module'})
bsh,ash=[q.block(md,'standard_shroud_module') for md in [bmod,amod]]
checks['only_exact_eater_attunement_coordinate_change']=q.scalars(q.block(bsh,'attunement'))=={'x':0,'y':0.15} and q.scalars(q.block(ash,'attunement'))=={'x':-0.15,'y':0.15} and omit(bsh,{'attunement'})==omit(ash,{'attunement'})
for k in ['research_stockpile','tech_status','budget_categories','variables','flags','government','traditions','ascension_perks','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';variables=h.GAME_EXE.parent/'common/scripted_variables/00_scripted_variables.txt';shroudvars=h.GAME_EXE.parent/'common/scripted_variables/09_scripted_variables_shroud.txt'
ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2310'];assert len(ev)==1;opts=vals(ev[0],'option');owner=q.block(opts[1],'owner');lith=q.block(owner,'else_if');sv=q.scalars(variables.read_text('utf-8-sig'));shv=q.scalars(shroudvars.read_text('utf-8-sig'))
checks['native_option1_lithoid_reward_branch_and_caps']=len(opts)==3 and q.scalars(q.block(lith,'limit'))=={'founder_species_is_lithoid':'yes'} and q.scalars(q.block(lith,'add_monthly_resource_mult'))=={'resource':'minerals','value':'@tier2materialreward','min':'@tier2materialmin','max':'@tier2materialmax'} and [sv[k] for k in ['@tier2materialreward','@tier2materialmin','@tier2materialmax']]==[12,150,2000]
checks['native_other_choices_exclude_homicidal_and_eater_request150']=all(q.scalars(q.block(q.block(opts[i],'trigger'),'owner'))=={'is_homicidal':'no'} for i in [0,2]) and not q.block(opts[1],'trigger') and q.scalars(q.block(owner,'add_attunement'))=={'the_eater_of_worlds':'@breach_the_shroud_full_attunement'} and shv['@breach_the_shroud_full_attunement']==150 and not q.block(ev[0],'after') and a['species']['66']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_latent_psionic']
p={'status':'PASS_NATIVE_TERRAVORE_2310_MINERAL_REWARD_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not [v for v in ap if q.scalars(v).get('country')==0],'actual_minerals_before_after':[bc['effective_stockpile']['minerals'],ac['effective_stockpile']['minerals']],'actual_attunement_before_after':[q.scalars(q.block(v,'attunement')) for v in [bsh,ash]],'source_eater_request':150,'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,variables,shroudvars]],'scope':'One normally selected native shroud.2310 mineral reward. No Mod devouring/world settlement, psi reward or full-route claim.'}
out=run/(after+'-2310-reward-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Native2310 original FAIL retained; no replay'
