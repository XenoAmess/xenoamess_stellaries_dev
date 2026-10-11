"""Exact one normal paid rear colonizer, independent of later completion."""
import json, logging, re, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools'); sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO); h=r.harness; run,user,metadata=h.load_run()
def load(name): return json.loads((run/name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z: fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def omit(t,keys): return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def fmap(t): return {k:(v,o) for k,v,o in q.fields(t)}
b,bf,br=read(before); a,af,ar=read(after); bc,ac=b['countries']['0'],a['countries']['0']
pre=load(before+'-mia-v2-proof.json'); ex=load(before+'-mia-guard-v2-execution.json')
cb,ca=br['construction'],ar['construction']; qm=[q.block(t,'queue_mgr') for t in [cb,ca]]; qs=[q.block(t,'queues') for t in qm]
bq,aq=[q.block(t,'3') for t in qs]; im=[q.block(t,'item_mgr') for t in [cb,ca]]; its=[q.block(t,'items') for t in im]; bi,ai=[fmap(t) for t in its]
item=ai['100663340'][0]; build=q.block(item,'buildable_colony_ship'); design=q.block(ar['ship_design'],'150995039')
bcs,acs=[dict((k,v) for k,v,o in q.fields(t['country']) if o) for t in [br,ar]]
bm,am=[q.block(t['0'],'modules') for t in [bcs,acs]]; be,ae=[q.block(t,'standard_economy_module') for t in [bm,am]]
actions=[(load(s+'.action.json'),load(s+'-execution.json'),xy) for s,xy in [('terravore-mother-colonizer3-pick',[579,332]),('terravore-mother-colonizer3-confirm',[502,269])]]
checks={
 'prior12_MIA_PASS_actual0_original_source_SHA':pre['status'].startswith('PASS_') and len(pre['checks'])==12 and all(v is True for v in pre['checks'].values()) and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_rear97_colonizer_mia_guard_v2.py')=='c48beb964e5cefa0ab0486d385f0d1f0a135d4eec44249e4c3fed2b34fe4608c' and pre['after_sha256']==b['save_sha256'],
 'original_same_day_SHA_pair':b['date']==a['date']=='2272.09.27' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='d73af65431a2c2a182afdd40281a4d4ee38404821473ab00818ab3107b9407ea' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='02ba2c61e4238d4b704c26e83cad61daf008f086a47de0398cefaedd51df05e2',
 'two_normal_unique_clicks_actual0':all(c['action']=='left-click' and c['client_point']==xy and c['foreground_after']==c['expected_hwnd'] and e['returncode']==0 and e['helper_sha256']=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' for c,e,xy in actions),
 'actual_quote_GPU_OCR_bound_exit0':h.sha256(run/'terravore-mother-true-shipyard-ui.jpg')==load('terravore-mother-true-shipyard-ui.ocr.json')['image_sha256']=='4a325506e319c8ee420a7063e8557c07c03c901ad4ffcd2cf6786a46b2e7a857',
 'actual375_minerals150_alloys_only_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==375 and D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==150 and {k:v for k,v in bc['effective_stockpile'].items() if k not in {'minerals','alloys'}}=={k:v for k,v in ac['effective_stockpile'].items() if k not in {'minerals','alloys'}},
 'only_one_order_original_empty_rear_queue':not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==[100663340] and omit(bq,{'items'})==omit(aq,{'items'}),
 'exact_payer_queue_zero_work360_native_cost':q.scalars(item)=={'queue':3,'paying_country':0,'progress':0,'progress_needed':360} and q.scalars(q.block(item,'resources'))=={'minerals':375,'alloys':150},
 'exact_colonizer_design_base0_species73':q.scalars(q.block(build,'ship_design_implementation'))=={'design':150995039,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(build,'orbitable'))=={'starbase':0} and q.scalars(q.block(build,'colonization_data'))=={'species':73} and re.findall(r'\bship_size="([^"]+)"',design)==['colonizer'] and 150995039 in q.ids(q.block(q.block(acs['0'],'ship_design_collection'),'ship_design')),
 'no_target_or_extra_effect_in_new_native_order':[(k,o) for k,v,o in q.fields(item)]==[('queue',False),('paying_country',False),('progress',False),('progress_needed',False),('resources',True),('buildable_colony_ship',True)] and [(k,o) for k,v,o in q.fields(build)]==[('ship_design_implementation',True),('orbitable',True),('colonization_data',True)],
 'exact_none_handle_generation_only_other_items_held':set(ai)-set(bi)=={'100663340'} and set(bi)-set(ai)=={'83886124'} and bi['83886124']==('none',False) and 100663340==83886124+16777216 and omit(its[0],{'83886124'})==omit(its[1],{'100663340'}),
 'all_other_queues_and_construction_managers_held':omit(qs[0],{'3'})==omit(qs[1],{'3'}) and omit(qm[0],{'queues'})==omit(qm[1],{'queues'}) and omit(im[0],{'items'})==omit(im[1],{'items'}) and omit(cb,{'queue_mgr','item_mgr'})==omit(ca,{'queue_mgr','item_mgr'}),
 'economy_only_two_resources_true_research_held':omit(q.block(be,'resources'),{'minerals','alloys'})==omit(q.block(ae,'resources'),{'minerals','alloys'}) and omit(be,{'resources'})==omit(ae,{'resources'}) and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and bc['research_stockpile']==ac['research_stockpile'],
 'all_other_country_fields_countries_held':omit(bcs['0'],{'modules'})==omit(acs['0'],{'modules'}) and bcs.keys()==acs.keys() and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'all_other_top_raw_held_including27_military_MIA_colonizer_target523_core':[(k,v,o) for k,v,o in bf if k not in {'country','construction','camera_focus'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','camera_focus'}],
 'native_save_actual0_and_unfiltered_error_held':load(after+'-native-save-execution.json')['returncode']==0 and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'production41_same_tree_simp_chinese':metadata['version']=='0.2.0' and metadata['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
p={'status':'PASS_TERRAVORE_NATIVE_MOTHER_COLONIZER3_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_order_id':100663340,'native_queue':3,'native_base':0,'native_design':150995039,'native_species':73,'actual_minerals_paid':'375','actual_alloys_paid':'150','native_base_work':360,'first_day_calibration_ready':all(checks.values()),'short_building_interval_ready':all(checks.values()),'maximum_days_to_before_month_end':3,'calendar_ready':False,'scope':'One additional normally paid mother colonizer, original MIA ship retained. No birth, transit, colony or mineral-ship acceptance.'}
out=run/(after+'-mother-colonizer3-payment-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert all(checks.values()),'Original payment FAIL retained; no replay or calendar'
