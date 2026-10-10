"""Normal crisis introduction ACK enables exactly the unstarted psionic project."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-nemesis-ap-selected';after='terravore-nemesis-intro-ack'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def lex(t):return [v for v,b,e in q.tokens(t)]
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];brc,arc=q.block(br['country'],'0'),q.block(ar['country'],'0');be,ae=q.block(brc,'events'),q.block(arc,'events')
pre=json.loads((run/(before+'-nemesis-ap-v2-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-v2-execution.json')).read_text('utf-8'))
bp,ap=vals(bt,'player_event'),vals(at,'player_event');assert len(bp)==1;scope=q.block(bp[0],'scope');bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==205 and q.scalars(v).get('receiver')==0]
bs,ass=vals(be,'special_project'),vals(ae,'special_project');new=[v for v in ass if v not in bs];assert len(new)==1;p=new[0]
chains=lambda t:[v for v in vals(t,'event_chain') if q.scalars(v).get('event_chain')=='become_the_crisis_chain'];bch,ach=chains(be),chains(ae);assert len(bch)==len(ach)==1
src=h.GAME_EXE.parent/'events/nemesis_crisis_events.txt';proj=h.GAME_EXE.parent/'common/special_projects/00_projects_nemesis.txt';trigger=h.GAME_EXE.parent/'common/scripted_triggers/08_scripted_triggers_shroud.txt'
ev=[v for k,v,o in q.fields(src.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='crisis.4140'];assert len(ev)==1;option=vals(ev[0],'option')[0];psi=q.block(option,'if');psdef=[v for k,v,o in q.fields(proj.read_text('utf-8-sig')) if o and q.scalars(v).get('key')=='CRISIS_SPECIAL_PROJECT_PSIONIC_1'];assert len(psdef)==1
checks={
 'bound28_AP_V2_PASS_exit0_exact_input':pre['status']=='PASS_TERRAVORE_NORMALLY_EARNED_NEMESIS_AP_V2_COMPONENT' and len(pre['checks'])==28 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date']=='2258.11.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'exact205_pending_removed_no_new':q.scalars(bp[0])=={'id':205,'event':'crisis.4140','date':'2261.02.02','country':0} and not ap,
 'exact_matching_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
 'single205_human1_option0_history':selected_history(at)==selected_history(bt)+[{'player_event':205,'human':1,'option':0}],
 'original_projects_raw_held_exact_one_added':ass==bs+new and len(bs)==1 and q.scalars(bs[0]).get('special_project')=='CLOUDS_PROJECT',
 'exact_new_unstarted_psionic_project2':q.scalars(p)=={'id':2,'special_project':'CRISIS_SPECIAL_PROJECT_PSIONIC_1','ai_research_date':'2258.11.14'} and [(k,o) for k,v,o in q.fields(p)]==[('id',False),('special_project',False),('scope',True),('coordinate',True),('carrier',True),('ai_research_date',False)],
 'project_scope_all_ordered_tokens_equal_original_event':lex(q.block(p,'scope'))==lex(scope),
 'project_mother_coordinate_and_carrier7':q.scalars(q.block(p,'coordinate'))=={'type':2,'id':7} and q.scalars(q.block(p,'carrier'))=={'type':'planet','reference':7},
 'project_allocator_exact2_to3':q.scalars(be).get('next_special_project_id')==2 and q.scalars(ae).get('next_special_project_id')==3,
 'same_crisis_chain_only_counter1_added':omit(bch[0],{'counter'})==omit(ach[0],{'counter'}) and not vals(bch[0],'counter') and len(vals(ach[0],'counter'))==1 and q.scalars(vals(ach[0],'counter')[0])=={'crisis_level_reached':1},
 'other_event_chains_raw_held':[(k,v,o) for k,v,o in q.fields(be) if k=='event_chain' and v not in bch]==[(k,v,o) for k,v,o in q.fields(ae) if k=='event_chain' and v not in ach],
 'all_other_event_fields_ordered_raw_held':omit(be,{'special_project','next_special_project_id','event_chain'})==omit(ae,{'special_project','next_special_project_id','event_chain'}),
 'all_country0_except_events_raw_held':omit(brc,{'events'})==omit(arc,{'events'}),
 'all_other_countries_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'random_exact_plus1_allocator_held':q.scalars(bt)['random_count']==52825415 and q.scalars(at)['random_count']==52825416 and q.scalars(bt)['last_event_id']==q.scalars(at)['last_event_id']==205,
 'all_other_ordered_top_raw_held':omit(bt,{'country','player_event','message','open_player_event_selection_history','random_count'})==omit(at,{'country','player_event','message','open_player_event_selection_history','random_count'}),
 'actual_EEP_cash_bank_population_jobs_all_held':all(bc[k]==ac[k] for k in ['effective_stockpile','research_stockpile','flags','variables','tech_status']) and all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','species','situations']),
 'native_level1_held_no_project_completion_or_menace':q.block(brc,'crisis_progression')==q.block(arc,'crisis_progression') and q.scalars(q.block(arc,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and 'crisis_special_project_1_complete' not in q.scalars(q.block(arc,'flags')),
 'source_option_one_counter1_and_psionic_priority':q.scalars(option).get('name')=='crisis.4140.a' and q.scalars(q.block(option,'add_event_chain_counter'))=={'event_chain':'become_the_crisis_chain','counter':'crisis_level_reached','amount':1} and q.scalars(q.block(psi,'limit'))=={'is_psionic':'yes'} and q.scalars(q.block(psi,'enable_special_project'))=={'name':'CRISIS_SPECIAL_PROJECT_PSIONIC_1','owner':'ROOT'},
 'source_psionic_project3000_society_success_flag_and4120':q.scalars(psdef[0]).get('cost')==3000 and q.scalars(psdef[0]).get('days_to_research')==0 and q.scalars(psdef[0]).get('tech_department')=='society_technology' and q.scalars(q.block(psdef[0],'on_success'))=={'set_country_flag':'crisis_special_project_1_complete'} and q.scalars(q.block(q.block(psdef[0],'on_success'),'country_event'))=={'id':'crisis.4120'},
 'normal_click_save_actual_exit0':all(json.loads((run/(after+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-select','-save']) and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['client_point']==[510,507],
 'unfiltered_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
out=run/(after+'-nemesis-intro-ack-proof.json');assert not out.exists();proof={'status':'PASS_TERRAVORE_NEMESIS_INTRO_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not ap,'sources':[{'path':str(s),'sha256':h.sha256(s)} for s in [src,proj,trigger]],'actual_project_raw':p,'scope':'Native intro ACK only enables unstarted psionic project2 and chain counter1; no project completion, menace or mineral ships.'};h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original native intro ACK FAIL retained'
