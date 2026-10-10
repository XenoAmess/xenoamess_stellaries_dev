"""Read-only exact native node83 repair order and paid160 minerals."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bmod,amod=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(c,'standard_economy_module') for c in [bmod,amod]];bres,ares=[q.block(c,'resources') for c in [be,ae]]
conb,cona=[rt['construction'] for rt in [br,ar]];bqm,aqm=[q.block(c,'queue_mgr') for c in [conb,cona]];bqs,aqs=[q.block(c,'queues') for c in [bqm,aqm]];bq,aq=[q.block(c,'0') for c in [bqs,aqs]]
bim,aim=[q.block(c,'item_mgr') for c in [conb,cona]];bi,ai=[q.block(c,'items') for c in [bim,aim]];item=q.block(ai,'620757018');sc=q.scalars(item)
pre=json.loads((run/(before+'-paid-outpost-v2-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-v2-execution.json')).read_text('utf-8'))
ids=q.ids(q.block(aq,'items'));new_items=[q.block(ai,str(i)) for i in ids]
checks={
 'exact_same_date_SHA_pair':before=='terravore-yodd-outpost-paid' and after=='terravore-postrepair-two-mines-paid' and b['date']==a['date']=='2262.05.17' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior49_paid_outpost_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_YODD_NATIVE_PAID_OUTPOST_V2_COMPONENT' and len(pre['checks'])==49 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='f6a0f932cdcb3c18fbe14dc2410ab7c8ed648d2592ee0c1b77dd98066db9880a',
 'exact480_real_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==480,
 'all_other_actual_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'} and bc['research_stockpile']==ac['research_stockpile'],
 'all_other_top_raw_held_including_frontier_order_ten_ships_and_mother':[(k,v,o) for k,v,o in bf if k not in {'country','construction','colony','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','colony','random_count'}],
 'all_other_country_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'country0_except_modules_raw_held':omit(bcr,{'modules'})==omit(acr,{'modules'}),
 'all_other_country_modules_raw_held':omit(bmod,{'standard_economy_module'})==omit(amod,{'standard_economy_module'}),
 'economy_except_resources_raw_held':omit(be,{'resources'})==omit(ae,{'resources'}),
 'only_economy_mineral_field_changed_no_mirror_flush':omit(bres,{'minerals'})==omit(ares,{'minerals'}) and q.scalars(bres)['minerals']==10583.62829 and q.scalars(ares)['minerals']==10103.62829,
 'empty_mother_queue_exact_two_new_paid_orders':q.ids(q.block(bq,'items'))==[] and ids==[1207959557,771751943] and omit(bq,{'items'})==omit(aq,{'items'}),
 'all_other_construction_queues_raw_held':omit(bqs,{'0'})==omit(aqs,{'0'}),
 'two_recycled_none_handles_only':all(q.scalars(bi).get(str(old))=='none' and not any(k==str(new) for k,v,o in q.fields(bi)) and not any(k==str(old) for k,v,o in q.fields(ai)) and new==old+16777216 for old,new in [(1191182341,1207959557),(754974727,771751943)]) and omit(bi,{'1191182341','754974727'})==omit(ai,{'1207959557','771751943'}),
 'all_other_construction_manager_fields_raw_held':omit(conb,{'queue_mgr','item_mgr'})==omit(cona,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'both_native_orders_exact_payer0_work240_progress0':all(q.scalars(v)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':240} for v in new_items),
 'both_native_orders_exact240_minerals':all(q.scalars(q.block(v,'resources'))=={'minerals':240} for v in new_items),
 'both_native_orders_exact_mining_planet0_no_extra_fields':all(q.scalars(q.block(v,'buildable_district'))=={'district':'district_mining','planet':0} and set(k for k,v,o in q.fields(v))=={'queue','paying_country','progress','progress_needed','resources','buildable_district'} for v in new_items),
 'all_other_colonies_and_mother_fields_raw_held':omit(br['colony'],{'0'})==omit(ar['colony'],{'0'}) and omit(q.block(br['colony'],'0'),{'last_district_changed'})==omit(q.block(ar['colony'],'0'),{'last_district_changed'}),
 'native_last_district_generator_to_mining_only':q.scalars(q.block(br['colony'],'0'))['last_district_changed']=='district_generator' and q.scalars(q.block(ar['colony'],'0'))['last_district_changed']=='district_mining',
 'exact_native_random_count_plus6':[v for k,v,o in bf if k=='random_count']==['99982416'] and [v for k,v,o in af if k=='random_count']==['99982422'],
 'tech_status_raw_held':bc['tech_status']==ac['tech_status'],
 'EEP_ledger_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_errors2670_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
 'native_save_actual_exit0':json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0,
 'UI_quote_image_bound':h.sha256(run/'terravore-postrepair-mining-quote-visible.jpg')==json.loads((run/'terravore-postrepair-mining-quote-visible.ocr.json').read_text('utf-8'))['image_sha256'],
}
for n in [11,12]:
 stage='terravore-postrepair-mine'+str(n)+'-click';click=json.loads((run/(stage+'.action.json')).read_text('utf-8'));checks['unique_normal_mine'+str(n)+'_click_exit0']=click['action']=='left-click' and click['client_point']==[459,439] and json.loads((run/(stage+'-execution.json')).read_text('utf-8'))['returncode']==0
p={'status':'PASS_TERRAVORE_TWO_NATIVE_MINES_PAID_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_paid_minerals':480,'actual_original_order_ids':ids,'calendar_ready':all(checks.values()),'scope':'Two normal paid240 mineral district_mining orders only; existing ten ships and prepaid outpost raw held. No completed districts or added workforce, frontier arrival, menace or full-route claim.'}
out=run/(after+'-two-mines-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original two-mine payment FAIL retained; no repeat purchase'
