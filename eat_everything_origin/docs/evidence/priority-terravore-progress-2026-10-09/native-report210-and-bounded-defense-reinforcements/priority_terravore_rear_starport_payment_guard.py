"""One normal native rear starport upgrade payment; read-only exact state guard."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-war1-defense-three-days4';after='terravore-war1-rear-starport-paid'
def load(n):return json.loads((run/n).read_text('utf-8'))
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=load(before+'-war1-battle-v6-proof.json');ex=load(before+'-battle-v6-execution.json')
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bm,am=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
bfleet,afleet=[q.block(t['fleet'],'16778043') for t in [br,ar]]
bcon,acon=br['construction'],ar['construction']
bqm,aqm=[q.block(c,'queue_mgr') for c in [bcon,acon]];bqs,aqs=[q.block(c,'queues') for c in [bqm,aqm]]
bq,aq=[q.block(c,'2278') for c in [bqs,aqs]]
bim,aim=[q.block(c,'item_mgr') for c in [bcon,acon]];bis,ais=[q.block(c,'items') for c in [bim,aim]]
item=q.block(ais,'234881044')
checks={
 'production02_simp_chinese_prior25_PASS_actual0_source_bound':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and pre['status'].startswith('PASS_') and len(pre['checks'])==25 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='8fb7ccb67c97ec9e979f894736e409d11806eeaf7ae6e0eceb7af2bf51ac2ab4' and h.sha256(run/Path(ex['command'][1]).name)==ex['helper_sha256'],
 'same_date_original_SHA_pair':b['date']==a['date']=='2268.08.13' and all(h.sha256(run/(s+'.sav'))==v['save_sha256'] for s,v in [(before,b),(after,a)]),
 'exact_real_alloy125_payment':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==125,
 'all_other_stocks_and_true_research_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'} and bc['research_stockpile']==ac['research_stockpile'],
 'country_only_economy_module_changed_other_countries_held':omit(bcr,{'modules'})==omit(acr,{'modules'}) and br['country'].replace(bcr,acr,1)==ar['country'] and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}),
 'economy_only_alloy_mirror_exact_paid':omit(be,{'resources'})==omit(ae,{'resources'}) and omit(q.block(be,'resources'),{'alloys'})==omit(q.block(ae,'resources'),{'alloys'}) and D(str(q.scalars(q.block(ae,'resources'))['alloys']))==D(str(ac['effective_stockpile']['alloys'])),
 'fleet_only16778043_dirty_cache':br['fleet'].replace(bfleet,afleet,1)==ar['fleet'] and omit(bfleet,{'properties'})==omit(afleet,{'properties'}) and omit(q.block(bfleet,'properties'),{'dirty_cloaking_strength'})==omit(q.block(afleet,'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(bfleet,'properties')) and q.scalars(q.block(afleet,'properties'))['dirty_cloaking_strength']=='yes',
 'construction_other_manager_fields_held':omit(bcon,{'queue_mgr','item_mgr'})==omit(acon,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'only_rear2278_queue_changed_exact_single_new_item':omit(bqs,{'2278'})==omit(aqs,{'2278'}) and omit(bq,{'items'})==omit(aq,{'items'}) and not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==[234881044] and q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'starbase'} and q.scalars(q.block(aq,'location'))=={'type':0,'id':67109591},
 'only_consumed_none_slot_replaced_exact_new_order':omit(bis,{'218103828','234881044'})==omit(ais,{'218103828','234881044'}) and [(v,o) for k,v,o in q.fields(bis) if k=='218103828']==[('none',False)] and not [k for k,v,o in q.fields(bis) if k=='234881044'] and not [k for k,v,o in q.fields(ais) if k=='218103828'],
 'exact_order_payer_progress_resources_target':q.scalars(item)=={'queue':2278,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(item,'resources'))=={'alloys':125} and q.scalars(q.block(item,'buildable_starbase_upgrade'))=={'starbase_upgrade':'starbase_level_starport','starbase':153} and [k for k,v,o in q.fields(item)]==['queue','paying_country','progress','progress_needed','resources','buildable_starbase_upgrade'],
 'rear153_still_owned_outpost_no_completion':q.scalars(q.block(q.block(ar['starbase_mgr'],'starbases'),'153'))=={'level':'starbase_level_outpost','build_queue':2278,'shipyard_build_queue':4294967295,'station':67109591} and q.scalars(q.block(ar['ships'],'67109591'))['fleet']==804 and 'fleet=804' in q.block(q.block(acr,'fleets_manager'),'owned_fleets').replace(' ', '').replace('\t','').replace('\n','').replace('\r',''),
 'mother24_paid_orders_full_raw_held':q.block(q.block(q.block(br['construction'],'queue_mgr'),'queues'),'3')==q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'3') and len(q.ids(q.block(q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'3'),'items')))==24,
 'all_other_top_raw_random_ships_mother_colony_held':[(k,v,o) for k,v,o in bf if k not in {'country','fleet','construction','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'country','fleet','construction','camera_focus'}],
 'audit_population_EEP_technology_buildings_species_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','event_targets','situations']) and all(bc[k]==ac[k] for k in ['flags','variables','government','tech_status','owned_colonies']),
 'normal_click_save_actual0':load('terravore-war1-rear-upgrade-paid-click-execution.json')['returncode']==load(after+'-save-execution.json')['returncode']==0 and load('terravore-war1-rear-upgrade-paid-click.action.json')['client_point']==[415,376],
 'UI_quote_original_image_bound':h.sha256(run/'terravore-war1-rear-upgrade-price-visible.jpg')==load('terravore-war1-rear-upgrade-price-visible.ocr.json')['image_sha256'],
 'native_starbase_sources_bound':h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/common/starbase_levels/00_starbase_levels.txt'))=='495d5c5d13b80502c8cd121cd8817dc76e1690e8bd584a6a1d91845af006f94d' and h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/common/ship_sizes/00_starbases.txt'))=='bf3719e954596118f046f49f4b672b0e1f88d11c192bd179170a651d12c1f1ce',
 'no_pending_country0':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'full_unfiltered_error_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(checks.values());out={'status':'PASS_TERRAVORE_NATIVE_REAR_STARPORT_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'paid_alloys':125,'rear_order_id':234881044,'rear_order_raw':item,'calendar_ready':False,'short_combat_calendar_ready':passed,'scope':'One native paid rear upgrade order, still an outpost without shipyards; no battle victory, completed upgrade or full-route claim.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids']:out[key]=pre[key]
p=run/(after+'-rear-starport-payment-proof.json');assert not p.exists();h.write_json(p,out)
print(json.dumps({'status':out['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v]}),flush=True);assert passed,'Preserve FAIL; do not repeat payment'
