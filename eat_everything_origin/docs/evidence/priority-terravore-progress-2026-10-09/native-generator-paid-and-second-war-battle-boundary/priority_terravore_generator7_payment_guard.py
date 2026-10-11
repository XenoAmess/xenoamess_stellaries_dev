"""One native paid generator district, with after-click UI quote explicitly scoped."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
load=lambda n:json.loads((run/n).read_text('utf-8'))
before='terravore-heavy-full-budget-month';after='terravore-generator7-paid'
def read(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return load(st+'.audit.json'),fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=[x['countries']['0'] for x in [b,a]]
cb,ca=[q.block(t['country'],'0') for t in [br,ar]];mb,ma=[q.block(t,'modules') for t in [cb,ca]];eb,ea=[q.block(t,'standard_economy_module') for t in [mb,ma]];rb,ra=[q.block(t,'resources') for t in [eb,ea]]
bcon,acon=[t['construction'] for t in [br,ar]];bqm,aqm=[q.block(t,'queue_mgr') for t in [bcon,acon]];bim,aim=[q.block(t,'item_mgr') for t in [bcon,acon]];bqs,aqs=[q.block(t,'queues') for t in [bqm,aqm]];bis,ais=[q.block(t,'items') for t in [bim,aim]];bq,aq=[q.block(t,'0') for t in [bqs,aqs]];item=q.block(ais,'788529161')
pre=load(before+'-war1-battle-v49-proof.json');ex=load(before+'-battle-v49-execution.json');budget=load('terravore-heavy-budget-cycle-v2-proof.json');budgetex=load('terravore-heavy-budget-cycle-guard-v2-execution.json')
checks={
 'production02_simp_chinese_exact_tree':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'prior77_PASS_actual0_source_bound':pre['status'].startswith('PASS_') and len(pre['checks'])==77 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v49.py')=='e2c6ef5c01e1550c90bf843c5bbe61195e8281355031a125303818d48f480ca8',
 'budget16_PASS_actual0_source_bound':budget['status'].startswith('PASS_') and len(budget['checks'])==16 and all(v is True for v in budget['checks'].values()) and budget['after_sha256']==b['save_sha256'] and budgetex['returncode']==0 and budgetex['helper_sha256']==h.sha256(run/'priority_terravore_heavy_budget_cycle_guard_v2.py')=='67f22d6b7ee78c8999152d8db3a4d3959fcdc557bbe5d94a00217ca485147b5e',
 'same_date_exact_SHA_pair':b['date']==a['date']=='2271.07.01' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='cbe2bed75f87370687b7ca46da759a400b0fba8dbaa86395e44c057243657d3a' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='f92dff154f53c84753490723697be281a0b1efc009c02047f8ec3935df7a3c4a',
 'actual240_mineral_payment_all_other_true_banks_held':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==240 and {k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'} and bc['research_stockpile']==ac['research_stockpile'],
 'only_country0_economy_resources_other_country_fields_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(cb,{'modules'})==omit(ca,{'modules'}) and omit(mb,{'standard_economy_module'})==omit(ma,{'standard_economy_module'}) and omit(eb,{'resources'})==omit(ea,{'resources'}),
 'exact_native_research_mirror_refresh_only':omit(rb,{'minerals',*q.RESEARCH_RESOURCES})==omit(ra,{'minerals',*q.RESEARCH_RESOURCES}) and {k:q.scalars(rb).get(k) for k in q.RESEARCH_RESOURCES}=={'physics_research':58.719,'society_research':7067.21485,'engineering_research':61.919} and {k:q.scalars(ra).get(k,0) for k in q.RESEARCH_RESOURCES}==ac['research_stockpile'] and q.scalars(ra)['minerals']==9692.73814,
 'only_queue0_one_generator_order':omit(bqs,{'0'})==omit(aqs,{'0'}) and omit(bq,{'items'})==omit(aq,{'items'}) and q.ids(q.block(bq,'items'))==[] and q.ids(q.block(aq,'items'))==[788529161] and q.scalars(aq)=={'owner':0,'simultaneous':1,'type':'planet'} and q.scalars(q.block(aq,'location'))=={'type':2,'id':7},
 'exact_one_old_none_generation_slot9_reuse':omit(bis,{'771751945'})==omit(ais,{'788529161'}) and [(v,o) for k,v,o in q.fields(bis) if k=='771751945']==[('none',False)] and not any(k=='788529161' for k,v,o in q.fields(bis)) and not any(k=='771751945' for k,v,o in q.fields(ais)) and 788529161-771751945==16777216,
 'exact_native_generator_order_schema':q.scalars(item)=={'queue':0,'paying_country':0,'progress':0,'progress_needed':240} and q.scalars(q.block(item,'resources'))=={'minerals':240} and q.scalars(q.block(item,'buildable_district'))=={'district':'district_generator','planet':0} and [k for k,v,o in q.fields(item)]==['queue','paying_country','progress','progress_needed','resources','buildable_district'],
 'all_other_construction_manager_fields_held':omit(bcon,{'item_mgr','queue_mgr'})==omit(acon,{'item_mgr','queue_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'only_mother_last_district_selection_changed':omit(br['colony'],{'0'})==omit(ar['colony'],{'0'}) and omit(q.block(br['colony'],'0'),{'last_district_changed'})==omit(q.block(ar['colony'],'0'),{'last_district_changed'}) and q.scalars(q.block(br['colony'],'0'))['last_district_changed']=='district_mining' and q.scalars(q.block(ar['colony'],'0'))['last_district_changed']=='district_generator',
 'exact_native_random_counter_plus3':[(v,o) for k,v,o in bf if k=='random_count']==[('227682456',False)] and [(v,o) for k,v,o in af if k=='random_count']==[('227682459',False)],
 'all_other_top_raw_fleet_population_jobs_structures_held':[(k,v,o) for k,v,o in bf if k not in {'country','construction','colony','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','colony','random_count'}],
 'generator6_still_unbuilt_other_districts_held':q.scalars(q.block(ar['districts'],'2'))=={'type':'district_generator','level':6} and b['districts']==a['districts'] and b['pop_groups']==a['pop_groups'] and b['pop_jobs']==a['pop_jobs'],
 'normal_click_and_save_actual0_after_click_quote_explicit':load('terravore-generator7-open-build-execution.json')['returncode']==load(after+'-native-save-execution.json')['returncode']==0 and load('terravore-generator7-open-build-action.action.json')['client_point']==[249,438] and h.sha256(run/'terravore-generator7-build-list-visible.jpg')==load('terravore-generator7-build-list-visible.ocr.json')['image_sha256'],
 'native_rural_full_source_bound':h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/common/districts/02_rural_districts.txt'))==h.sha256(run/'native-three-mines-02_rural_districts.txt')=='90e6faea595af0c662dfd4847d37c9af77bbaa4bc3c8c5894f83e26fe02f98ec',
 'exact2814_error_no_pending_country0':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb' and not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
}
passed=all(v is True for v in checks.values());proof={'status':'PASS_TERRAVORE_NATIVE_GENERATOR7_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'paid_minerals':240,'native_order_id':788529161,'native_order_raw':item,'short_idle_war_calendar_ready':False,'colony523_order_recovery_pending':True,'scope':'One paid seventh generator district still0/240, exact bank/mirror accounting; quote is after native purchase. No completion or future maintenance acceptance; only documented next one-day calibration.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids']:proof[key]=pre[key]
out=run/(after+'-generator-payment-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed,'Preserve native payment evidence; no repeated purchase'
