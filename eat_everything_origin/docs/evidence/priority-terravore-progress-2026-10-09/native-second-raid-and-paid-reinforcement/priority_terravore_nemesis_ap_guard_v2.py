"""Normal fourth earned Nemesis AP: precise native state and cache transitions."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-postbreach-stable-month';after='terravore-nemesis-ap-selected'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
def anon(t):
 out=[];depth=0
 for tok,b,a in q.tokens(t):
  if tok=='{':
   if depth==0:start=a
   depth+=1
  elif tok=='}':
   assert depth>0;depth-=1
   if depth==0:out.append(t[start:b])
  elif depth==0:raise ValueError('Expected anonymous list object')
 assert depth==0;return out
b,bt,bf,br=read(before);a,at,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];brc,arc=q.block(br['country'],'0'),q.block(ar['country'],'0')
pre=json.loads((run/(before+'-postbreach-month-proof.json')).read_text('utf-8'));bound=json.loads((run/(before+'-postbreach-boundary-proof.json')).read_text('utf-8'))
bp,ap=vals(bt,'player_event'),vals(at,'player_event');bm,am=vals(bt,'message'),vals(at,'message');assert len(ap)==1;scope=q.block(ap[0],'scope')
be,ae=q.block(brc,'events'),q.block(arc,'events');chains=[v for v in vals(ae,'event_chain') if v not in vals(be,'event_chain')];assert len(chains)==1
btl,atl=anon(q.block(brc,'timeline_events')),anon(q.block(arc,'timeline_events'));newtl=atl[len(btl):]
bfleet,afleet={k:v for k,v,o in q.fields(br['fleet']) if o},{k:v for k,v,o in q.fields(ar['fleet']) if o};changed=[k for k,v in bfleet.items() if afleet.get(k)!=v];expected=['0','1','2','136','137','138','139','140','161','166','167','171','172','178','183','196','198','477','490','16777797','602']
bs,ass=q.block(q.block(br['starbase_mgr'],'starbases'),'0'),q.block(q.block(ar['starbase_mgr'],'starbases'),'0')
root=h.GAME_EXE.parent;sources=[root/'common/ascension_perks/00_ascension_perks.txt',root/'common/crisis_levels/00_crisis_levels.txt',root/'events/nemesis_crisis_events.txt',root/'events/timeline_events.txt']
apdef=q.block(sources[0].read_text('utf-8-sig'),'ap_become_the_crisis');enabled=q.block(apdef,'on_enabled');hidden=q.block(enabled,'hidden_effect');level=q.block(sources[1].read_text('utf-8-sig'),'crisis_level_1')
events={q.scalars(v).get('id'):v for k,v,o in q.fields(sources[2].read_text('utf-8-sig')) if o};timelines={q.scalars(v).get('id'):v for k,v,o in q.fields(sources[3].read_text('utf-8-sig')) if o}
checks={
 'bound44_boundary17_month_PASS_actual_exit0':pre['status'].startswith('PASS') and bound['status']=='PASS_TERRAVORE_POSTBREACH_STABLE_BOUNDARY_COMPONENT' and len(pre['checks'])==17 and len(bound['checks'])==44 and all(v is True for v in pre['checks'].values()) and all(v is True for v in bound['checks'].values()) and pre['after_sha256']==bound['after_sha256']==b['save_sha256'] and all(json.loads((run/(before+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-guard','-month-guard']),
 'same_date_original_SHA_pair':b['date']==a['date']=='2258.11.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'exact_fourth_earned_AP_prior_four_paid_trees':bc['ascension_perks']==['ap_one_vision','ap_technological_ascendancy','ap_mind_over_matter'] and ac['ascension_perks']==bc['ascension_perks']+['ap_become_the_crisis'] and bc['traditions']==ac['traditions'] and all(k in ac['traditions'] for k in ['tr_discovery_finish','tr_prosperity_finish','tr_synchronicity_finish','tr_psionics_shroud_finish']),
 'source_on_enabled_exact_native_activation':q.scalars(enabled)=={'activate_crisis_progression':'nemesis_path'} and q.scalars(hidden)=={'set_ai_personality':'became_the_crisis'} and q.scalars(q.block(hidden,'country_event'))=={'id':'timeline.69'},
 'native_personality_exact_transition':q.scalars(brc)['personality']=='devouring_swarm' and q.scalars(arc)['personality']=='became_the_crisis',
 'exact_new_level1_no_menace_grant':not q.block(brc,'crisis_progression') and list(q.fields(q.block(arc,'crisis_progression')))==[('path','"nemesis_path"',False),('level','"crisis_level_1"',False)],
 'source_level1_zero_requirement_and4140_unlock':q.scalars(level)['required_crisis_currency']==0 and q.scalars(q.block(q.block(q.block(q.block(level,'on_unlock'),'hidden_effect'),'owner'),'country_event'))=={'id':'crisis.4140'},
 'unique205_4140_country0_future_expiry':not bp and q.scalars(ap[0])=={'id':205,'event':'crisis.4140','date':'2261.02.02','country':0},
 'country0_scope_and_from_country0':q.scalars(scope).get('type')=='country' and q.scalars(scope).get('id')==0 and q.scalars(q.block(scope,'from')).get('type')=='country' and q.scalars(q.block(scope,'from')).get('id')==0,
 'single_matching_message_added':not bm and len(am)==1 and q.scalars(am[0]).get('event')==205 and q.scalars(am[0]).get('receiver')==0 and q.scalars(am[0]).get('date')=='2258.11.02',
 'new_chain_exact_scope_and_all_prior_events_raw_held':q.scalars(chains[0])=={'event_chain':'become_the_crisis_chain'} and [v for v,b,e in q.tokens(q.block(chains[0],'scope'))]==[v for v,b,e in q.tokens(scope)] and omit(ae,{'event_chain'})==omit(be,{'event_chain'}) and vals(ae,'event_chain')==vals(be,'event_chain')+chains,
 'source4140_immediate_only_begin_same_chain':[(k,o) for k,v,o in q.fields(q.block(events['crisis.4140'],'immediate'))]==[('begin_event_chain',True)] and q.scalars(q.block(q.block(events['crisis.4140'],'immediate'),'begin_event_chain'))=={'event_chain':'become_the_crisis_chain','target':'root'},
 'one_timeline_append_other_entries_exact_raw_held':atl[:len(btl)]==btl and len(newtl)==1 and q.scalars(newtl[0])=={'date':'2258.11.02','definition':'timeline_become_the_crisis'} and q.ids(q.block(newtl[0],'data'))==[0] and [x for x,b,e in q.tokens(q.block(newtl[0],'types'))]==['country'],
 'source_timeline69_same_definition_country_target':q.scalars(q.block(q.block(timelines['timeline.69'],'immediate'),'add_timeline_event')).get('override_id')=='timeline_become_the_crisis' and q.scalars(timelines['timeline.69']).get('hide_window')=='yes',
 'all_country0_except_five_native_fields_raw_held':omit(brc,{'personality','ascension_perks','crisis_progression','events','timeline_events'})==omit(arc,{'personality','ascension_perks','crisis_progression','events','timeline_events'}),
 'all_other_countries_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'actual_stocks_true_banks_EEP_flags_and_variables_held':all(bc[k]==ac[k] for k in ['effective_stockpile','research_stockpile','variables','flags','tech_status']),
 'actual_population_jobs_buildings_districts_planets_species_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','colonies','districts','planets','deposits','species','event_targets']),
 'all_fleet_objects_identity_held_exact21_cache_targets':set(bfleet)==set(afleet) and set(changed)==set(expected),
 'each21_only_new_dirty_cloaking_strength_all_other_fields_held':all(omit(bfleet[k],{'properties'})==omit(afleet[k],{'properties'}) and q.scalars(q.block(afleet[k],'properties'))==dict(q.scalars(q.block(bfleet[k],'properties')),dirty_cloaking_strength='yes') and 'dirty_cloaking_strength' not in q.scalars(q.block(bfleet[k],'properties')) for k in expected),
 'all_other_fleet_objects_raw_held':all(afleet[k]==v for k,v in bfleet.items() if k not in expected),
 'base0_only_new_update2048_other_manager_raw_held':omit(bs,{'update_flag'})==omit(ass,{'update_flag'}) and 'update_flag' not in q.scalars(bs) and q.scalars(ass)['update_flag']==2048 and omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'}) and omit(q.block(br['starbase_mgr'],'starbases'),{'0'})==omit(q.block(ar['starbase_mgr'],'starbases'),{'0'}),
 'allocation204_to205_random_exact_plus2':q.scalars(bt)['last_event_id']==204 and q.scalars(at)['last_event_id']==205 and q.scalars(bt)['random_count']==52825413 and q.scalars(at)['random_count']==52825415,
 'selection_history_held_no_intro_ack_yet':selected_history(bt)==selected_history(at),
 'all_other_ordered_top_raw_held':omit(bt,{'country','fleet','starbase_mgr','player_event','message','last_event_id','random_count'})==omit(at,{'country','fleet','starbase_mgr','player_event','message','last_event_id','random_count'}),
 'normal_UI_list_select_confirm_and_save_actual_exit0':all(json.loads((run/(n+'-execution.json')).read_text('utf-8'))['returncode']==0 for n in ['terravore-nemesis-open-ap-list','terravore-nemesis-ap-select','terravore-nemesis-ap-confirm',after+'-save']) and all(json.loads((run/(n+'.action.json')).read_text('utf-8'))['client_point']==point for n,point in [('terravore-nemesis-open-ap-list',[908,338]),('terravore-nemesis-ap-select',[510,347]),('terravore-nemesis-ap-confirm',[587,432])]),
 'unfiltered_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
original=json.loads((run/(after+'-nemesis-ap-proof.json')).read_text('utf-8'));original_ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
checks['bound_original27_exact_scope_whitespace_failure']=original['status']=='FAIL' and len(original['checks'])==27 and [k for k,v in original['checks'].items() if v is not True]==['new_chain_exact_scope_and_all_prior_events_raw_held'] and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'] and original_ex['returncode']==1 and original_ex['helper_sha256']=='fd082aa612d3796b36cd8adc6246208a96ef2dc51f06c43ec9435b5bf8239d59'
p={'status':'PASS_TERRAVORE_NORMALLY_EARNED_NEMESIS_AP_V2_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'sources':[{'path':str(s),'sha256':h.sha256(s)} for s in sources],'actual_crisis_progression':q.scalars(q.block(arc,'crisis_progression')),'actual_new_timeline':newtl,'actual_changed_fleet_cache_ids':changed,'scope':'Normal fourth paid-tree earned AP and native level1 only. No menace, project completion, mineral ship or whole-route claim.'}
out=run/(after+'-nemesis-ap-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original Nemesis AP FAIL retained'
