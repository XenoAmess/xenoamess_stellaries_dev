"""Exact same-day native payment for three mines; retains the battle loss ledger."""
import json, logging, shutil, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists(): assert dest.read_bytes()==Path(__file__).read_bytes()
else: shutil.copyfile(__file__,dest)
before='terravore-war1-bounded10-step3';after='terravore-war1-three-mines-paid'
def load(name): return json.loads((run/name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z: fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def omit(raw,keys): return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=load(before+'-war1-battle-v9-proof.json');ex=load(before+'-battle-v9-execution.json')
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bm,am=[q.block(c,'modules') for c in [bcr,acr]]
be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
bres,ares=[q.block(e,'resources') for e in [be,ae]]
bcon,acon=br['construction'],ar['construction']
bqm,aqm=[q.block(c,'queue_mgr') for c in [bcon,acon]];bqs,aqs=[q.block(c,'queues') for c in [bqm,aqm]]
bq,aq=[q.block(c,'0') for c in [bqs,aqs]]
bim,aim=[q.block(c,'item_mgr') for c in [bcon,acon]];bi,ai=[q.block(c,'items') for c in [bim,aim]]
ids=[1006632966,1207959563,905969668];oldids=[989855750,1191182347,889192452]
orders=[q.block(ai,str(i)) for i in ids]
oldfleet,newfleet=[q.block(t['fleet'],'835') for t in [br,ar]]
pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
source=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/districts/02_rural_districts.txt')
source_sha='90e6faea595af0c662dfd4847d37c9af77bbaa4bc3c8c5894f83e26fe02f98ec'
archived_source=run/'native-three-mines-02_rural_districts.txt'
assert h.sha256(source)==source_sha
if archived_source.exists(): assert archived_source.read_bytes()==source.read_bytes()
else: shutil.copyfile(source,archived_source)
checks={
    'production02_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese',
    'prior27_PASS_actual0_exact_source_and_SHA':pre['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' and len(pre['checks'])==27 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v9.py')=='a39f884b439203a964353ed00c8111f732aa1fcd34ab7b71f9bd0be3d52a0717',
    'same_native_date_exact_SHA_pair':b['date']==a['date']=='2268.11.09' and b['save_sha256']=='9e0ef0cbd15aab6b9171d9b2b4e876a9c69f4c89e1249703c0394d56d50cf9fd' and a['save_sha256']=='e7e169e2a49f06ee8a4cf134367f21dd80d299af2250953542ba4a87f03b52a8' and all(h.sha256(run/(s+'.sav'))==v['save_sha256'] for s,v in [(before,b),(after,a)]),
    'exact_real_mineral720_payment':D(str(bc['effective_stockpile']['minerals']))==D('10649.53427') and D(str(ac['effective_stockpile']['minerals']))==D('9929.53427'),
    'other_real_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'} and bc['research_stockpile']==ac['research_stockpile']=={'physics_research':0,'society_research':5971.13195,'engineering_research':0},
    'other_countries_and_country0_nonmodules_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(bcr,{'modules'})==omit(acr,{'modules'}),
    'other_modules_and_nonresource_economy_held':omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}),
    'only_exact_paid_mineral_and_native_research_mirror_refresh':omit(bres,{'minerals','physics_research','society_research','engineering_research'})==omit(ares,{'minerals','physics_research','society_research','engineering_research'}) and q.scalars(bres)['physics_research']==29.2595 and q.scalars(bres)['engineering_research']==30.8095 and q.scalars(bres)['society_research']==5962.49932 and all(k not in q.scalars(ares) for k in ['physics_research','engineering_research']) and q.scalars(ares)['society_research']==5971.13195 and q.scalars(ares)['minerals']==9929.53427,
    'all_other_top_raw_ships_army_war_population_zones_held':[(k,v,o) for k,v,o in bf if k not in {'country','construction','fleet','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','fleet','random_count'}],
    'only_fleet835_dirty_cloaking_cache_added':omit(br['fleet'],{'835'})==omit(ar['fleet'],{'835'}) and omit(oldfleet,{'properties'})==omit(newfleet,{'properties'}) and omit(q.block(oldfleet,'properties'),{'dirty_cloaking_strength'})==omit(q.block(newfleet,'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(oldfleet,'properties')) and q.scalars(q.block(newfleet,'properties'))['dirty_cloaking_strength']=='yes',
    'construction_other_manager_fields_held':omit(bcon,{'queue_mgr','item_mgr'})==omit(acon,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
    'only_mother_queue0_changed':omit(bqs,{'0'})==omit(aqs,{'0'}) and omit(bq,{'items'})==omit(aq,{'items'}) and not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==ids,
    'queue0_true_owner0_physical_planet7':q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'planet'} and q.scalars(q.block(aq,'location'))=={'type':2,'id':7},
    'only_three_recycled_none_slots':all(q.scalars(bi).get(str(old))=='none' and not any(k==str(new) for k,v,o in q.fields(bi)) and not any(k==str(old) for k,v,o in q.fields(ai)) and new==old+16777216 for old,new in zip(oldids,ids)) and omit(bi,set(map(str,oldids)))==omit(ai,set(map(str,ids))),
    'three_exact_native_payer0_work240_progress0':all(q.scalars(v)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':240} for v in orders),
    'three_exact_mineral240_prices':all(q.scalars(q.block(v,'resources'))=={'minerals':240} for v in orders),
    'three_exact_mining_colony0_orders_only':all(q.scalars(q.block(v,'buildable_district'))=={'district':'district_mining','planet':0} and [k for k,val,o in q.fields(v)]==['queue','paying_country','progress','progress_needed','resources','buildable_district'] for v in orders),
    'exact_random_count_plus9':[(v,o) for k,v,o in bf if k=='random_count']==[('189642962',False)] and [(v,o) for k,v,o in af if k=='random_count']==[('189642971',False)],
    'mother_still_mining12_and_all_old_jobs_held':q.scalars(q.block(ar['districts'],'3'))=={'type':'district_mining','level':12} and b['pop_jobs']==a['pop_jobs'] and b['colonies']==a['colonies'],
    'EEP_flags_ledger_technology_and_species_held':all(bc[k]==ac[k] for k in ['flags','variables','tech_status','government','owned_colonies']) and all(b[k]==a[k] for k in ['species','event_targets','situations']),
    'mother_twenty_ship_orders_and_rear_upgrade_held':q.block(bqs,'3')==q.block(aqs,'3') and len(q.ids(q.block(q.block(aqs,'3'),'items')))==20 and q.block(bqs,'2278')==q.block(aqs,'2278') and q.block(bi,'234881044')==q.block(ai,'234881044'),
    'no_pending_country0':not pending,
    'unfiltered_error2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and (run/(after+'-error-after.log')).stat().st_size==2670,
    'native_source_archived_and_SHA_bound':h.sha256(archived_source)==source_sha,
    'native_UI_quote_image_bound':h.sha256(run/'terravore-war1-three-mines-price-visible.jpg')==load('terravore-war1-three-mines-price-visible.ocr.json')['image_sha256'],
}
save=load(after+'-save-execution.json')
checks['unique_native_save_actual0_source_bound']=save['returncode']==0 and save['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and save['wrapper_sha256']=='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3'
for i in range(1,4):
    stage='terravore-war1-three-mines-click'+str(i);click=load(stage+'.action.json');receipt=load(stage+'-execution.json')
    checks['normal_click'+str(i)+'_actual0_source_bound']=click['action']=='left-click' and click['client_point']==[460,440] and receipt['returncode']==0 and receipt['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f'
passed=all(v is True for v in checks.values())
proof={'status':'PASS_TERRAVORE_THREE_NATIVE_MINES_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'date':a['date'],'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_paid_minerals':720,'actual_order_ids':ids,'actual_order_raw':orders,'actual_pending':pending,'calendar_ready':False,'short_combat_calendar_ready':passed,'scope':'Only three normally paid native mining orders, still level12/progress0. No completed districts, industry conversion, battle victory or full-route claim.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids']:proof[key]=pre[key]
out=run/(after+'-three-mines-payment-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed,'Original payment FAIL retained; never repeat the purchase'
