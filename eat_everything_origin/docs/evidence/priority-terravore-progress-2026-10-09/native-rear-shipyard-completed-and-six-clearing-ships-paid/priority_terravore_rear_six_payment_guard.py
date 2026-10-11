"""Read-only exact native six-corvette payment, before any calendar."""
import json, logging, math, re, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO); h = r.harness; run, user, metadata = h.load_run()
def load(name): return json.loads((run/name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:
        fs = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'), fs, {k:v for k,v,o in fs if o}
def omit(raw, names): return [(k,v,o) for k,v,o in q.fields(raw) if k not in names]
def fields(raw): return {k:(v,o) for k,v,o in q.fields(raw)}
b,bf,br=read(before); a,af,ar=read(after)
bc,ac=b['countries']['0'],a['countries']['0']
bcs,acs=[{k:v for k,v,o in q.fields(t['country']) if o} for t in [br,ar]]
cb,ca=br['construction'],ar['construction']
qm=[q.block(t,'queue_mgr') for t in [cb,ca]]; qs=[q.block(t,'queues') for t in qm]
bq,aq=[q.block(t,'2287') for t in qs]; new=q.ids(q.block(aq,'items'))
im=[q.block(t,'item_mgr') for t in [cb,ca]]; its=[q.block(t,'items') for t in im]
bi,ai=[fields(t) for t in its]; added=set(ai)-set(bi); removed=set(bi)-set(ai)
items=[ai[str(i)][0] for i in new]
bm,am=[q.block(t['0'],'modules') for t in [bcs,acs]]
be,ae=[q.block(t,'standard_economy_module') for t in [bm,am]]
pre=load(before+'-war1-battle-v58-proof.json'); ex=load(before+'-battle-v58-execution.json')
quote=load('terravore-rear-clearing-corvette-quote.json'); design=q.block(ar['ship_design'],'134219607')
clicks=[(load('terravore-rear-clearing-six-click-'+str(i).zfill(2)+'.action.json'),load('terravore-rear-clearing-six-click-'+str(i).zfill(2)+'-execution.json')) for i in range(1,7)]
bfleets,afleets=[fields(t['fleet']) for t in [br,ar]]
dirty={'526','16777857'}; fleet_valid=bfleets.keys()==afleets.keys()
for k in bfleets:
    if k not in dirty: fleet_valid &= bfleets[k]==afleets[k]
    else:
        rb,ra=bfleets[k][0],afleets[k][0]
        fleet_valid &= (omit(rb,{'properties'})==omit(ra,{'properties'})
            and q.scalars(q.block(rb,'properties'))=={'civilian':'yes','mobile':'yes','valid_for_combat':'yes'}
            and q.scalars(q.block(ra,'properties'))=={'civilian':'yes','mobile':'yes','valid_for_combat':'yes','dirty_cloaking_strength':'yes'})
checks={
 'prior_actual94_PASS_exit0_source_SHA':pre['status'].startswith('PASS_') and len(pre['checks'])==94 and all(v is True for v in pre['checks'].values()) and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v58.py')=='4c25bf40720e1b1423228985a4eebf13b3be7554498ee65699c82f93cad60f63' and pre['after_sha256']==b['save_sha256']=='e72ded2b20c6d26b135fb792f331c1f8f6b9e5836e6906264233845a5519f453',
 'same_day_original_SHA_pair':b['date']==a['date']=='2271.11.03' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav'))=='d962aa132aa1f4fdfbc4dcb210e4544d2c8b8c8941c2a4a5bfcb2a634f67654f',
 'six_actual_unique_normal_clicks':len(clicks)==6 and all(c['action']=='left-click' and c['client_point']==[566,403] and c['foreground_after']==c['expected_hwnd'] and e['returncode']==0 and e['helper_sha256']=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' for c,e in clicks),
 'only_six_unique_orders_in_original_empty_queue2287':not q.ids(q.block(bq,'items')) and new==[50331689,83886123,33554472,33554471,1241513995,67108908] and len(set(new))==6 and omit(bq,{'items'})==omit(aq,{'items'}) and q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'ships'} and q.scalars(q.block(aq,'location'))=={'type':0,'id':67109591},
 'native_payer_queue_work_exact':all(q.scalars(t)=={'queue':2287,'paying_country':0,'progress':0,'progress_needed':60} for t in items),
 'native_each101point5_total609_UIceil102':all(q.scalars(q.block(t,'resources'))=={'alloys':101.5} for t in items) and sum((D(str(q.scalars(q.block(t,'resources'))['alloys'])) for t in items),D(0))==609 and math.ceil(D('101.5'))==quote['UI_total_alloys']==102 and 609<=quote['max_UI_total_alloys']==612,
 'true_stock_exact609_paid_other_stocks_held':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==609 and {k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'},
 'actual_native_quote_design_image_OCR_source_bound':quote['before_sha256']==b['save_sha256'] and quote['base']==153 and quote['queue']==2287 and quote['design']==134219607 and quote['native_base_work']==60 and quote['UI_list_days']==37 and quote['design_sha256']==h.sha256(run/'terravore-rear-clearing-corvette-native-design.txt')=='cab785c8955b97b73fcfb1baeeca4f7bd0081ecc9683ac464558a43149b1c60f' and (run/'terravore-rear-clearing-corvette-native-design.txt').read_text('utf-8')==design and quote['image_sha256']==h.sha256(run/'terravore-rear-corvette-price-visible.jpg')==load('terravore-rear-corvette-price-visible.ocr.json')['image_sha256'] and quote['ocr_sha256']==h.sha256(run/'terravore-rear-corvette-price-visible.ocr.json') and load('terravore-rear-corvette-price-hover-execution.json')['returncode']==load('terravore-rear-corvette-price-capture-execution.json')['returncode']==0,
 'six_current_ordinary_corvettes_legal_design_base153':all(q.scalars(q.block(q.block(t,'buildable_ship'),'ship_design_implementation'))=={'design':134219607,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(q.block(t,'buildable_ship'),'orbitable'))=={'starbase':153} for t in items) and bool(re.search(r'ship_size="corvette"',design)) and 134219607 in q.ids(q.block(q.block(acs['0'],'ship_design_collection'),'ship_design')),
 'only_named_fields_in_orders':all([(k,o) for k,v,o in q.fields(t)]==[('queue',False),('paying_country',False),('progress',False),('progress_needed',False),('resources',True),('buildable_ship',True)] and [(k,o) for k,v,o in q.fields(q.block(t,'buildable_ship'))]==[('ship_design_implementation',True),('orbitable',True)] for t in items),
 'all_other_queues_and_queue_manager_raw_held':omit(qs[0],{'2287'})==omit(qs[1],{'2287'}) and omit(qm[0],{'queues'})==omit(qm[1],{'queues'}),
 'exact_six_none_generation_replacements_only':added==set(map(str,new)) and removed=={'16777255','16777256','33554473','50331692','67108907','1224736779'} and all(bi[k]==('none',False) and str(int(k)+16777216) in added for k in removed),
 'other_items_manager_construction_raw_held':omit(its[0],removed)==omit(its[1],added) and omit(im[0],{'items'})==omit(im[1],{'items'}) and omit(cb,{'queue_mgr','item_mgr'})==omit(ca,{'queue_mgr','item_mgr'}),
 'economy_only_alloys_exact_no_research_bank_or_mirror_change':omit(q.block(be,'resources'),{'alloys'})==omit(q.block(ae,'resources'),{'alloys'}) and omit(be,{'resources'})==omit(ae,{'resources'}) and bc['research_stockpile']==ac['research_stockpile'] and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}),
 'country0_other_fields_and_all_other_countries_raw_held':omit(bcs['0'],{'modules'})==omit(acs['0'],{'modules'}) and bcs.keys()==acs.keys() and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'only_two_exact_native_civilian_cloak_dirty_flags_all_other_fleet_fields_held':bool(fleet_valid),
 'all_other_top_fields_raw_held_including_ships_wars_armies_pending':[(k,v,o) for k,v,o in bf if k not in {'country','construction','fleet'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','fleet'}],
 'actual_native_save_exit0_and_error_baseline_held':load(after+'-native-save-execution.json')['returncode']==0 and (run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'production_language_held':metadata['version']=='0.2.0' and metadata['language']=='l_simp_chinese',
}
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
out=run/(after+'-rear-six-payment-proof.json'); assert not out.exists()
p={'status':'PASS_TERRAVORE_NATIVE_REAR_SIX_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_per_ship_alloys':'101.5','actual_total_alloys':'609','native_order_ids':new,'native_order_raw':items,'native_queue':2287,'native_design':134219607,'native_base_work':60,'UI_estimated_days':37,'calendar_ready':False,'first_day_calibration_ready':all(checks.values()),'scope':'Six ordinary rear corvettes actually paid; zero births or mineral ships, no new maintenance/route/whole-route acceptance.'}
h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert all(checks.values()),'Payment FAIL retained; no replay or calendar'
