"""Read-only exact native Yomon outpost payment and unique constructor order."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
assert not dest.exists() or dest.read_bytes()==Path(__file__).read_bytes()
if not dest.exists():shutil.copyfile(__file__,dest)
before='terravore-war1-idle13-step3';after='terravore-yomon-outpost-paid'
def load(n):return json.loads((run/n).read_text('utf-8'))
def read(s):
 a=load(s+'.audit.json')
 with zipfile.ZipFile(run/(s+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def objects(raw):return {k:v for k,v,o in q.fields(raw) if o}
def omit(raw,keys):return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=[v['countries']['0'] for v in [b,a]];bfl,afl=[objects(t['fleet']) for t in [br,ar]];bct,act=[objects(t['country']) for t in [br,ar]]
bo,ao=bfl['2'],afl['2'];bm,am=[q.block(raw,'movement_manager') for raw in [bo,ao]];order=q.block(q.block(ao,'current_order'),'build_orbital_station_order');os=q.scalars(order);paid=q.scalars(q.block(order,'resources'))
eb,ea=[q.block(q.block(raw,'modules'),'standard_economy_module') for raw in [bct['0'],act['0']]];bres,ares=[q.block(raw,'resources') for raw in [eb,ea]]
pre=load(before+'-war1-battle-v23-proof.json');preex=load(before+'-battle-v23-execution.json');click=load(after+'-click.action.json');ce=load(after+'-click-execution.json');se=load(after+'-save-execution.json');ui=load('terravore-yomon-outpost-quote-visible.ocr.json')
surveyed={int(i) for typ,i in re.findall(r'\{\s*type=(\d+)\s+id=(\d+)\s*\}',q.block(bct['0'],'surveyed_deposit_holders')) if typ=='0'};system=q.block(br['galactic_object'],'37');body_ids=[int(v) for k,v,o in q.fields(system) if k=='planet' and not o];pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={
 'same_native_date_language_package':b['date']==a['date']=='2269.08.21' and m['language']=='l_simp_chinese' and m['version']=='0.2.0' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'exact_original_SAV_pair':b['save_sha256']==h.sha256(run/(before+'.sav'))=='56519c3409b7a4fefcb6b68cbde0ad3dc874339f6102a3d73c41c3a62674d70a' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='d753ea1c9faacd7d289653b5facc6d3a4593734ca575581c1b303d57e2402e57',
 'prior40_battle_PASS_actual0_source_bound':pre['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(pre['checks'])==40 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and preex['returncode']==0 and preex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v23.py')=='d86eb948e3fddfb8502fa2de83cc931f088ab316ab86af941a87e6163eeb2763',
 'normal_unique_quote_click_save_bound':h.sha256(run/'terravore-yomon-outpost-quote-visible.jpg')==ui['image_sha256']=='29b574d5365fce6b92e7d55e9df631c692e2b8d268646c9a90a987c155634db7' and click['action']=='left-click' and click['client_point']==[626,457] and ce['returncode']==se['returncode']==0 and ce['helper_sha256']=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and se['helper_sha256']=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e',
 'exact100_alloys37_influence_paid_matching_order':paid=={'influence':37,'alloys':100} and all(D(str(bc['effective_stockpile'][k]))-D(str(ac['effective_stockpile'][k]))==D(v) for k,v in paid.items()),
 'all_other_effective_stocks_and_true_research_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k not in paid}=={k:v for k,v in ac['effective_stockpile'].items() if k not in paid} and bc['research_stockpile']==ac['research_stockpile'],
 'system37_all14_known_surveyed_unowned_and_adjacent97':body_ids==list(range(518,532)) and set(body_ids)<=surveyed and q.ids(q.block(system,'starbases'))==[4294967295] and re.findall(r'to=(\d+)',q.block(system,'hyperlane'))==['97'] and a['planets']['523']['planet_class']=='pc_tropical' and a['planets']['523']['planet_size']==13 and 'colony' not in a['planets']['523'],
 'only_original_fleet2_three_order_fields_changed':set(bfl)==set(afl) and [k for k in bfl if bfl[k]!=afl[k]]==['2'] and omit(bo,{'order_id','movement_manager','current_order'})==omit(ao,{'order_id','movement_manager','current_order'}),
 'one_order_id_increment_original_idle_constructor':q.scalars(ao)['order_id']==q.scalars(bo)['order_id']+1==13 and bool(q.block(q.block(bo,'current_order'),'orbit_planet_order')) and os['order_id']==12,
 'exact_native_outpost_order_type_design_and_zero_work':os=={'progress':0,'cost':0,'in_progress':'no','class':'shipclass_starbase','can_reach':'yes','order_id':12,'commissioner':4294967295} and q.scalars(q.block(order,'deposit_holder'))=={'type':0,'id':518} and q.scalars(q.block(order,'ship_design'))=={'design':201326648,'upgrade':4294967295,'growth_stage':0},
 'exact_system37_target_coordinate':q.scalars(q.block(q.block(q.block(order,'sub_order'),'move_to_system_point_order'),'coordinate'))==q.scalars(q.block(am,'target_coordinate'))=={'x':18.27902,'y':-24.18672,'origin':37},
 'movement_other_fields_and_actual_original_coordinate_orbit_held':omit(bm,{'target','target_coordinate','path','time_since_last_path_update','state'})==omit(am,{'target','target_coordinate','path','time_since_last_path_update','state'}) and q.block(bm,'coordinate')==q.block(am,'coordinate') and q.block(bm,'orbit')==q.block(am,'orbit'),
 'all_other_top_fields_raw_held_including_ships_mines_colonies_war':[(k,v,o) for k,v,o in bf if k not in {'country','fleet','camera_focus','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','fleet','camera_focus','random_count'}],
 'exact_native_random_count_plus2':next(int(v) for k,v,o in af if k=='random_count')-next(int(v) for k,v,o in bf if k=='random_count')==2,
 'all_other_countries_raw_held':set(bct)==set(act) and all(bct[k]==act[k] for k in bct if k!='0'),
 'country0_direct_fields_except_modules_raw_held':omit(bct['0'],{'modules'})==omit(act['0'],{'modules'}),
 'country0_other_modules_and_economy_nonresources_raw_held':omit(q.block(bct['0'],'modules'),{'standard_economy_module'})==omit(q.block(act['0'],'modules'),{'standard_economy_module'}) and omit(eb,{'resources'})==omit(ea,{'resources'}),
 'economy_other_resources_raw_held_only_paid_and_true_bank_mirrors_refresh':omit(bres,{'alloys','influence','physics_research','society_research','engineering_research'})==omit(ares,{'alloys','influence','physics_research','society_research','engineering_research'}) and all(D(str(q.scalars(ares).get(k,0)))==D(str(ac['research_stockpile'].get(k,0))) for k in ['physics_research','society_research','engineering_research']),
 'EEP_real_economy_population_and_structure_held':all(bc[k]==ac[k] for k in ['variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']) and all(b[k]==a[k] for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']),
 'no_pending_and_exact_known2814_error_baseline_held':not pending and all(h.sha256(run/(stage+suffix))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb' for stage,suffix in [(before,'-error-after.log'),(after,'-error-before.log'),(after,'-error-after.log')]),
}
checks={k:bool(v) for k,v in checks.items()};proof={'status':'PASS_TERRAVORE_YOMON_NATIVE_OUTPOST_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'date':a['date'],'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_paid':paid,'actual_constructor_order_raw':order,'actual_constructor_order':os,'actual_system':37,'actual_star':518,'actual_design':201326648,'actual_pending':pending,'calendar_ready':False,'short_combat_calendar_ready':all(checks.values()) and not pending,'scope':'Unique normal native outpost payment only; target surveyed and legal. No completed outpost, colonization, free ships or full-route claim; existing native2814 error baseline retained.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids','actual_pending_destroyed_ship_ids','actual_naval_death_cache_credit']:proof[key]=pre[key]
out=run/(after+'-payment-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v]}),flush=True);assert all(checks.values()),'Native outpost payment original failure retained'
