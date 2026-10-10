"""Exact normally paid foundry replacement of native warren2."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-project1-crisis4120-acked';after='terravore-native-forge-paid'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(v,ks):return [(k,x,o) for k,x,o in q.fields(v) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
pre=json.loads((run/(before+'-empty-ack-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
bm,am=[q.block(cr,'modules') for cr in [bcr,acr]];be,ae=[q.block(v,'standard_economy_module') for v in [bm,am]];bres,ares=[q.block(v,'resources') for v in [be,ae]]
bim,aim=[q.block(rt['construction'],'item_mgr') for rt in [br,ar]];bi,ai=[q.block(v,'items') for v in [bim,aim]]
bqm,aqm=[q.block(rt['construction'],'queue_mgr') for rt in [br,ar]];bqs,aqs=[q.block(v,'queues') for v in [bqm,aqm]];bq,aq=[q.block(v,'0') for v in [bqs,aqs]];item=q.block(ai,'83886102')
checks={
 'same_date_original_SHA_pair':b['date']==a['date']=='2263.05.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior13_empty_ACK_PASS_actual_exit0':pre['status']=='PASS_NATIVE_EMPTY_EFFECT_ACK_COMPONENT' and len(pre['checks'])==13 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='62d850f93d60a09265eec3b68171a595062c99e9ffdfc46dc7a7227cc5e850cb',
 'all_other_ordered_top_raw_held':[(k,v,o) for k,v,o in bf if k not in {'country','colony','construction','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','colony','construction','random_count'}],
 'country_only0_modules_economy_resources_changed':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(bcr,{'modules'})==omit(acr,{'modules'}) and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}),
 'exact_mineral320_and_three_research_mirrors_only':omit(bres,{'minerals','physics_research','society_research','engineering_research'})==omit(ares,{'minerals','physics_research','society_research','engineering_research'}) and D(str(q.scalars(bres)['minerals']))-D(str(q.scalars(ares)['minerals']))==320 and q.scalars(bres)['physics_research']==29.2595 and q.scalars(bres)['engineering_research']==30.8095 and all(k not in q.scalars(ares) for k in ['physics_research','engineering_research']) and q.scalars(bres)['society_research']==3727.17037 and q.scalars(ares)['society_research']==3674.85137,
 'actual_mineral320_all_other_true_stocks_and_bank_held':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==320 and {k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'} and bc['research_stockpile']==ac['research_stockpile'],
 'all_budget_categories_held':bc['budget_categories']==ac['budget_categories'],
 'only_colony0_last_building_changed':omit(br['colony'],{'0'})==omit(ar['colony'],{'0'}) and omit(q.block(br['colony'],'0'),{'last_building_changed'})==omit(q.block(ar['colony'],'0'),{'last_building_changed'}) and q.scalars(q.block(ar['colony'],'0'))['last_building_changed']=='building_foundry_1',
 'construction_only_item_and_queue_containers_changed':omit(br['construction'],{'item_mgr','queue_mgr'})==omit(ar['construction'],{'item_mgr','queue_mgr'}) and omit(bim,{'items'})==omit(aim,{'items'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}),
 'only_recycled67108886_none_to83886102_new_item':q.scalars(bi).get('67108886')=='none' and not any(k=='67108886' for k,v,o in q.fields(ai)) and omit(bi,{'67108886','83886102'})==omit(ai,{'67108886','83886102'}) and not any(k=='83886102' for k,v,o in q.fields(bi)),
 'only_one_native_mother_order':not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==[83886102] and omit(bqs,{'0'})==omit(aqs,{'0'}) and omit(bq,{'items'})==omit(aq,{'items'}),
 'native_order_exact_payer_progress_cost_target':q.scalars(item)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(item,'resources'))=={'minerals':320} and q.scalars(q.block(item,'buildable_planet_replace_building'))=={'building':'building_foundry_1','planet':0,'zone':0,'replace_building':2},
 'actual_original_warren2_slot2_remains':q.scalars(q.block(ar['buildings'],'2'))=={'type':'building_hive_warren','position':2} and q.ids(q.block(q.block(ar['zones'],'0'),'buildings'))==[33554466,1,2,33554454,46,48],
 'all_buildings_districts_fleets_ships_jobs_raw_held':all(br[k]==ar[k] for k in ['buildings','districts','zones','fleet','ships','pop_jobs','pop_groups','species_db']),
 'mother_real_housing_and_amenities_surplus':q.scalars(q.block(ar['colony'],'0'))['free_housing']==4086 and q.scalars(q.block(ar['colony'],'0'))['free_amenities']==22181.5,
 'exact_random_plus1':[(v,o) for k,v,o in bf if k=='random_count']==[('113725536',False)] and [(v,o) for k,v,o in af if k=='random_count']==[('113725537',False)],
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'normal_click_and_save_actual_exit0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in ['terravore-native-forge-paid-click',after+'-save']) and json.loads((run/'terravore-native-forge-paid-click.action.json').read_text('utf-8'))['client_point']==[807,172],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
}
p={'status':'PASS_TERRAVORE_NATIVE_FOUNDRY_REPLACEMENT_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_item_id':83886102,'native_item_raw':item,'calendar_ready':all(checks.values()),'scope':'One actual320M native replacement order for warren2. No completion, alloy income or full-route claim.'}
out=run/(after+'-forge-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original payment FAIL retained'
