"""Exact same-day payment for two native defense platforms; read-only saves."""
import json, logging, re, shutil, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists(): assert dest.read_bytes()==Path(__file__).read_bytes()
else: shutil.copyfile(__file__,dest)
before='terravore-war1-sixth-pair-birth';after='terravore-war1-two-platforms-paid'
def load(name):return json.loads((run/name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def omit(raw,keys):return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=load(before+'-war1-battle-v12-proof.json');ex=load(before+'-battle-v12-execution.json')
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bm,am=[q.block(c,'modules') for c in [bcr,acr]]
be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
bres,ares=[q.block(e,'resources') for e in [be,ae]]
bcon,acon=br['construction'],ar['construction']
bqm,aqm=[q.block(c,'queue_mgr') for c in [bcon,acon]];bqs,aqs=[q.block(c,'queues') for c in [bqm,aqm]]
bq,aq=[q.block(c,'2') for c in [bqs,aqs]]
bim,aim=[q.block(c,'item_mgr') for c in [bcon,acon]];bi,ai=[q.block(c,'items') for c in [bim,aim]]
ids=[201326606,117440537];oldids=[184549390,100663321];orders=[q.block(ai,str(i)) for i in ids]
oldfleet,newfleet=[q.block(t['fleet'],'807') for t in [br,ar]]
pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
game=Path('C:/SteamLibrary/steamapps/common/Stellaris')
sources={'common/ship_sizes/00_ship_sizes.txt':'5d8fb948b2197e8a39e021a8501574e043d3c1fd3db7e0c8b9b0b1142da65c2f','common/scripted_variables/03_scripted_variables_ships.txt':'44ce49d52ad1d5d127149ed61b6c5ee497eca873f5836c7787946e75e11d97dc','localisation/simp_chinese/main_1_l_simp_chinese.yml':'bb9843957cd341d0f39beed436bd17e2e07ecb1fd515b3a86f36673c35ca08c5'}
for name,sha in sources.items():
    source=game/name;archived=run/('native-two-platforms-'+source.name)
    assert h.sha256(source)==sha
    if archived.exists():assert archived.read_bytes()==source.read_bytes()
    else:shutil.copyfile(source,archived)
design=q.block(ar['ship_design'],'150995587')
checks={
 'production02_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese',
 'prior30_PASS_actual0_exact_source_and_SHA':pre['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' and len(pre['checks'])==30 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v12.py')=='2a40809a741812caabbf28f40532f5105dbf351db048ea904253f45d579b7a5f',
 'same_native_date_exact_SHA_pair':b['date']==a['date']=='2268.11.25' and b['save_sha256']=='1db2089b788247aa99e8211b884bbcf219674dc66c435c61883707a0b08e4dce' and a['save_sha256']=='189878161ed9d6d67fad2dcc0e343cec2e894e0c3c827fca500ad1a781ce6cef' and all(h.sha256(run/(s+'.sav'))==v['save_sha256'] for s,v in [(before,b),(after,a)]),
 'exact_real_alloy1086_payment_and_budget':D(str(bc['effective_stockpile']['alloys']))==D('2289.61884') and D(str(ac['effective_stockpile']['alloys']))==D('1203.61884') and 1203.61884>=1000 and 1086<=1200,
 'all_other_real_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'} and bc['research_stockpile']==ac['research_stockpile']=={'physics_research':0,'society_research':5971.13195,'engineering_research':0},
 'all_other_countries_country0_nonmodules_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(bcr,{'modules'})==omit(acr,{'modules'}),
 'all_other_modules_and_nonresource_economy_held':omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}),
 'only_alloy_resource_changed_no_research_mirror_exception':omit(bres,{'alloys'})==omit(ares,{'alloys'}) and q.scalars(ares)['alloys']==1203.61884,
 'all_other_ordered_top_raw_ships_starbase_designs_war_population_held':[(k,v,o) for k,v,o in bf if k not in {'country','construction','fleet'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','fleet'}],
 'only_fleet807_dirty_cloaking_cache_added':omit(br['fleet'],{'807'})==omit(ar['fleet'],{'807'}) and omit(oldfleet,{'properties'})==omit(newfleet,{'properties'}) and omit(q.block(oldfleet,'properties'),{'dirty_cloaking_strength'})==omit(q.block(newfleet,'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(oldfleet,'properties')) and q.scalars(q.block(newfleet,'properties'))['dirty_cloaking_strength']=='yes',
 'construction_other_manager_fields_held':omit(bcon,{'queue_mgr','item_mgr'})==omit(acon,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'only_base0_queue2_changed_from_empty_to_two_exact_items':omit(bqs,{'2'})==omit(aqs,{'2'}) and omit(bq,{'items'})==omit(aq,{'items'}) and not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==ids,
 'queue2_true_owner0_native_starbase0_serial':q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'starbase'} and q.scalars(q.block(aq,'location'))=={'type':0,'id':0},
 'only_two_recycled_none_slots':all(q.scalars(bi).get(str(old))=='none' and not any(k==str(new) for k,v,o in q.fields(bi)) and not any(k==str(old) for k,v,o in q.fields(ai)) and new==old+16777216 for old,new in zip(oldids,ids)) and omit(bi,set(map(str,oldids)))==omit(ai,set(map(str,ids))),
 'two_exact_native_payer0_progress0_work60':all(q.scalars(v)=={'queue':2,'paying_country':0,'progress':0,'progress_needed':60} for v in orders),
 'two_exact_alloy543_prices':all(q.scalars(q.block(v,'resources'))=={'alloys':543} for v in orders),
 'two_exact_platform_base0_implementation_orders':all(q.scalars(q.block(v,'buildable_defense_platform'))=={'starbase':0} and q.scalars(q.block(q.block(v,'buildable_defense_platform'),'ship_design_implementation'))=={'design':150995587,'upgrade':4294967295,'growth_stage':0} and [k for k,val,o in q.fields(v)]==['queue','paying_country','progress','progress_needed','resources','buildable_defense_platform'] for v in orders),
 'actual_existing_platform_design_unchanged_dual_native_hangars':design==q.block(br['ship_design'],'150995587') and 'ship_size="military_station_small"' in design and len(re.findall(r'template\s*=\s*"HANGAR_MILITARY_STATION_SECTION"',design))==2 and len(re.findall(r'template\s*=\s*"STRIKE_CRAFT_HANGAR_1"',design))==2,
 'all_mother_colony_jobs_and_EEP_flags_ledger_research_held':b['pop_jobs']==a['pop_jobs'] and b['colonies']==a['colonies'] and all(bc[k]==ac[k] for k in ['flags','variables','tech_status','government','owned_colonies']) and all(b[k]==a[k] for k in ['species','event_targets','situations']),
 'eighteen_paid_corvette_mines_and_rear_orders_all_held':len(q.ids(q.block(q.block(aqs,'3'),'items')))==18 and all(q.block(bqs,str(i))==q.block(aqs,str(i)) for i in [0,3,2278]) and q.block(bi,'234881044')==q.block(ai,'234881044'),
 'no_pending_country0':not pending,
 'unfiltered_error2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and (run/(after+'-error-after.log')).stat().st_size==2670,
 'native_sources_archived_SHA_bound':all(h.sha256(run/('native-two-platforms-'+Path(name).name))==sha for name,sha in sources.items()),
 'native_UI_quote_image_bound':h.sha256(run/'terravore-war1-platform-price-visible.jpg')==load('terravore-war1-platform-price-visible.ocr.json')['image_sha256'],
}
save=load(after+'-save-execution.json')
checks['unique_native_save_actual0_source_bound']=save['returncode']==0 and save['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and save['wrapper_sha256']=='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3'
for index,label in [(1,'one'),(2,'two')]:
    click=load('terravore-war1-platform-paid-'+label+'.action.json');receipt=load('terravore-war1-platform-paid-click'+str(index)+'-execution.json')
    checks['normal_click'+str(index)+'_actual0_source_bound']=click['action']=='left-click' and click['client_point']==[568,265] and receipt['returncode']==0 and receipt['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f'
passed=all(v is True for v in checks.values())
proof={'status':'PASS_TERRAVORE_TWO_NATIVE_DEFENSE_PLATFORMS_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'date':a['date'],'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_paid_alloys':1086,'actual_order_ids':ids,'actual_order_raw':orders,'actual_design_id':150995587,'actual_pending':pending,'calendar_ready':False,'short_combat_calendar_ready':passed,'scope':'Only two normally paid native platforms, queue2 progress0. No completed platforms, free naval credit, victory or full-route claim.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids','actual_pending_destroyed_ship_ids','actual_naval_death_cache_credit']:proof[key]=pre[key]
out=run/(after+'-two-platforms-payment-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed,'Original payment FAIL retained; never repeat the purchase'
