"""Exact native disease weaponization sacrifice; never changes saves or game state."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime'];import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-meditate-year1';after='terravore-native-psi-disease-weaponized'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
b,bt,bf,br=read(before);a,at,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];pre=json.loads((run/(before+'-social-pending-supplement.json')).read_text('utf-8'));ex=json.loads((run/(before+'-social-supplement-execution.json')).read_text('utf-8'))
bp=[v for k,v,o in bf if k=='player_event' and o];ap=[v for k,v,o in af if k=='player_event' and o];target=[v for v in bp if q.scalars(v).get('id')==165 and q.scalars(v).get('event')=='shroud.2625' and q.scalars(v).get('country')==0]
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message'];removed=[v for v in bm if q.scalars(v).get('event')==165 and q.scalars(v).get('receiver')==0]
checks={'same_actual_date':a['date']==b['date']=='2245.08.02','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],'bound_prior9_component_PASS_exit0':pre['status']=='PASS_NATIVE_MEDITATE_YEAR_WITH_PENDING_COMPONENT' and len(pre['checks'])==9 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
'only_native_disease165_pending_removed':len(target)==1 and ap==[v for v in bp if v not in target] and [q.scalars(v).get('id') for v in ap if q.scalars(v).get('country')==0]==[162],
'exact_once_human_option1_history':selected_history(at)==selected_history(bt)+[{'player_event':165,'human':1,'option':1}],
'only_matching_disease_message_removed':len(removed)==1 and am==[v for v in bm if v not in removed],
'all_other_ordered_top_level_raw_held':[x for x in bf if x[0] not in {'pop_groups','colony','country','fleet','starbase_mgr','message','player_event','open_player_event_selection_history'}]==[x for x in af if x[0] not in {'pop_groups','colony','country','fleet','starbase_mgr','message','player_event','open_player_event_selection_history'}]}
click=json.loads((run/'terravore-native-disease-weaponized-select.action.json').read_text('utf-8'));checks['normal_exact_UI_selection_exit0']=click['action']=='left-click' and click['client_point']==[510,579] and json.loads((run/'terravore-native-disease-weaponized-select-execution.json').read_text('utf-8'))['returncode']==0
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];tm=q.block(acr,'timed_modifier');items=q.block(tm,'items').strip();mods=q.scalars(items[1:-1]) if items.startswith('{') and items.endswith('}') else {}
checks['unique_native_ten_year_weaponized_modifier']=not q.block(bcr,'timed_modifier') and mods=={'modifier':'weaponized_psionics_gestalt_modifier','days':3600} and [(k,o) for k,v,o in q.fields(tm)]==[('items',True)]
checks['country_all_raw_except_modifier_held']=omit(bcr,{'timed_modifier'})==omit(acr,{'timed_modifier'}) and omit(br['country'],{'0'})==omit(ar['country'],{'0'})
bg,ag=[q.block(rt['pop_groups'],'14') for rt in [br,ar]];skipg={'size','factions','wanted_factions','current_month_growth_details'}
checks['unique_group14_exact_minus200_no_identity_change']=q.scalars(bg)['size']==3892 and q.scalars(ag)['size']==3692 and omit(bg,skipg)==omit(ag,skipg) and q.scalars(q.block(ag,'current_month_growth_details'))=={'key':'GROWTH_CAT_OTHER','value':-200} and not q.block(bg,'current_month_growth_details') and q.block(ag,'factions').strip()==q.block(ag,'wanted_factions').strip()=='' and omit(br['pop_groups'],{'14'})==omit(ar['pop_groups'],{'14'})
checks['all_actual_population_exact_minus200']=b['colonies']['0']['actual_pop_sum']==9147 and a['colonies']['0']['actual_pop_sum']==8947 and sum(p['size'] for p in b['pop_groups'].values())-sum(p['size'] for p in a['pop_groups'].values())==200
bco,aco=[q.block(rt['colony'],'0') for rt in [br,ar]];skipco={'free_housing','housing_usage','employable_pops','num_sapient_pops','species_information','current_month_growth_data'}
checks['mother_only_exact_population_and_housing_cache_changes']=omit(bco,skipco)==omit(aco,skipco) and {k:q.scalars(bco)[k] for k in ['free_housing','housing_usage','employable_pops','num_sapient_pops']}=={'free_housing':4660,'housing_usage':9140,'employable_pops':9147,'num_sapient_pops':9147} and {k:q.scalars(aco)[k] for k in ['free_housing','housing_usage','employable_pops','num_sapient_pops']}=={'free_housing':4653,'housing_usage':9147,'employable_pops':8947,'num_sapient_pops':8947} and omit(br['colony'],{'0'})==omit(ar['colony'],{'0'})
bsi,asi=[q.block(c,'species_information') for c in [bco,aco]];bs66,as66=[q.block(s,'66') for s in [bsi,asi]]
checks['species_information_only_actual_count200_change']=omit(bsi,{'66'})==omit(asi,{'66'}) and omit(bs66,{'num_pops'})==omit(as66,{'num_pops'}) and q.scalars(bs66)['num_pops']==9147 and q.scalars(as66)['num_pops']==8947
bcg,acg=[q.block(c,'current_month_growth_data') for c in [bco,aco]]
checks['native_growth_details_exact_OTHER_minus200']=omit(bcg,{'current_month_growth_details'})==omit(acg,{'current_month_growth_details'}) and not q.block(bcg,'current_month_growth_details') and q.scalars(q.block(acg,'current_month_growth_details'))=={'key':'GROWTH_CAT_OTHER','value':-200}
for k in ['effective_stockpile','research_stockpile','tech_status','budget_categories','variables','flags','government','traditions','ascension_perks','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_jobs','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['all_ships_construction_zones_buildings_raw_held']=all(br[k]==ar[k] for k in ['ships','construction','zones','buildings'])
bss,asss=[q.block(rt['starbase_mgr'],'starbases') for rt in [br,ar]];bs0,as0=[q.block(v,'0') for v in [bss,asss]]
checks['only_starbase0_update_flag2048']=omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'}) and omit(bss,{'0'})==omit(asss,{'0'}) and omit(bs0,{'update_flag'})==omit(as0,{'update_flag'}) and 'update_flag' not in q.scalars(bs0) and q.scalars(as0).get('update_flag')==2048
bfl,afl=objs(br['fleet']),objs(ar['fleet']);changed=[i for i,v in bfl.items() if afl.get(i)!=v]
expected=['0','1','2','136','137','138','139','140','161','166','167','171','172','178','183','196','198','477','490','16777797','602']
checks['exact21_fleet_dirty_properties_only']=set(bfl)==set(afl) and set(changed)==set(expected) and all(omit(bfl[i],{'properties'})==omit(afl[i],{'properties'}) and omit(q.block(bfl[i],'properties'),{'dirty_cloaking_strength'})==omit(q.block(afl[i],'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(bfl[i],'properties')) and q.scalars(q.block(afl[i],'properties')).get('dirty_cloaking_strength')=='yes' for i in changed) and [(k,v,o) for k,v,o in q.fields(br['fleet']) if not o]==[(k,v,o) for k,v,o in q.fields(ar['fleet']) if not o]

checks['unfiltered_errors_held']=(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2625'];opts=[v for k,v,o in q.fields(ev[0]) if k=='option' and o];owner=q.block(opts[1],'owner');kill=q.block(q.block(q.block(owner,'if'),'random_owned_pop_group'),'kill_pop_group')
checks['native_option1_exact_kill200_and_ten_year_modifier']=q.scalars(kill)=={'pop_group':'this','amount':200} and 'weaponized_psionics_gestalt_modifier' in owner and 'years = 10' in owner
p={'status':'PASS_NATIVE_TERRAVORE_PSI_DISEASE_WEAPONIZED_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'actual_population_before_after':[9147,a['colonies']['0']['actual_pop_sum']],'actual_group14_before_after':[b['pop_groups']['14'],a['pop_groups']['14']],'actual_modifier':mods,'actual_EEP':ac['variables'],'remaining_country0_pending':[q.scalars(v) for v in ap if q.scalars(v).get('country')==0],'native_source':{'path':str(source),'sha256':h.sha256(source)},'scope':'One native weaponization sacrifice200, same-date exact state and caches;162 communications remains, no calendar clearance or next-month restaffing claim.'}
out=run/(after+'-disease-weaponized-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native disease choice FAIL retained'
