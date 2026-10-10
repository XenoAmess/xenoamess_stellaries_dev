"""Read-only exact thirty-corvette native war1 payment proof."""
import json,logging,math,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bcs,acs=[{k:v for k,v,o in q.fields(rt['country']) if o} for rt in [br,ar]]
consb,consa=br['construction'],ar['construction']
bqm,aqm=[q.block(c,'queue_mgr') for c in [consb,consa]];bqs,aqs=[q.block(c,'queues') for c in [bqm,aqm]]
bq,aq=q.block(bqs,'3'),q.block(aqs,'3');old,new=q.ids(q.block(bq,'items')),q.ids(q.block(aq,'items'))
bim,aim=[q.block(c,'item_mgr') for c in [consb,consa]];bis,ais=[q.block(c,'items') for c in [bim,aim]]
bi,ai=[{k:(v,o) for k,v,o in q.fields(c)} for c in [bis,ais]]
removed=set(bi)-set(ai);added=set(ai)-set(bi)
bm,am=[q.block(c['0'],'modules') for c in [bcs,acs]]
be,ae=[q.block(c,'standard_economy_module') for c in [bm,am]]
pre=json.loads((run/(before+'-colonization-started-war-observation-proof.json')).read_text('utf-8'))
obs=json.loads((run/(after+'-observation.json')).read_text('utf-8'))
clicks=[]
click_stages=['terravore-war1-reinforce-click-'+str(i).zfill(2) for i in range(1,31)]
for stage in click_stages:
 clicks.append((json.loads((run/(stage+'.action.json')).read_text('utf-8')),json.loads((run/(stage+'-execution.json')).read_text('utf-8'))))
items=[ai[str(i)][0] for i in new]
design=q.block(ar['ship_design'],'385877628')
checks={
 'bound_actual_prior16_war_observation_PASS_exit0_SHA':pre['status']=='PASS_TERRAVORE_NATIVE_COLONIZATION_AND_REMOTE_WAR_OBSERVATION_COMPONENT' and len(pre['checks'])==16 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/(before+'-started-war-guard-v3-execution.json')).read_text('utf-8'))['returncode']==0 and h.sha256(run/'priority_terravore_colony1085_started_war_guard_v3.py')=='193c3d17a9314b7d1cf73fe2a6397dd8c66e5d867482ed9ae362813d69ba67c1',
 'same_date_original_SHA_pair':b['date']==a['date']=='2268.03.17' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact30_unique_normal_paid_clicks':len(clicks)==len(set(click_stages))==30 and all(c['action']=='left-click' and c['client_point']==[565,403] and c['foreground_after']==c['expected_hwnd'] and e['returncode']==0 for c,e in clicks),
 'only30_appended_original_empty_shipyard_queue':old==[] and len(new)==len(set(new))==30 and omit(bq,['items'])==omit(aq,['items']),
 'each_native_payer0_queue3_progress0_base60':all(q.scalars(t)=={'queue':3,'paying_country':0,'progress':0,'progress_needed':60} for t in items),
 'each_native_actual_alloy98_total2940':all(q.scalars(q.block(t,'resources'))=={'alloys':98} for t in items) and sum((D(str(q.scalars(q.block(t,'resources'))['alloys'])) for t in items),D(0))==D(2940),
 'actual_stock_exact2940_paid':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==D(2940),
 'UI98_is_ceiling_of_actual98':math.ceil(D('98'))==98 and h.sha256(run/'terravore-war-corvette-price-visible.jpg')==json.loads((run/'terravore-war-corvette-price-visible.ocr.json').read_text('utf-8'))['image_sha256'],
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'},
 'all30_original_corvette_design_at_starbase0':all(q.scalars(q.block(q.block(t,'buildable_ship'),'ship_design_implementation'))=={'design':385877628,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(q.block(t,'buildable_ship'),'orbitable'))=={'starbase':0} for t in items) and q.scalars(q.block(design,'name'))=={'key':'HUMAN1_SHIP_Surik'} and bool(re.search(r'ship_size="corvette"',design)) and 385877628 in q.ids(q.block(q.block(acs['0'],'ship_design_collection'),'ship_design')),
 'only_named_fields_in30_items':all([(k,o) for k,v,o in q.fields(t)]==[('queue',False),('paying_country',False),('progress',False),('progress_needed',False),('resources',True),('buildable_ship',True)] and [(k,o) for k,v,o in q.fields(q.block(t,'buildable_ship'))]==[('ship_design_implementation',True),('orbitable',True)] for t in items),
 'all_other_queue_records_raw_held':omit(bqs,['3'])==omit(aqs,['3']),
 'queue_mgr_other_fields_raw_held':omit(bqm,['queues'])==omit(aqm,['queues']),
 'only30_new_items_and16_exact_none_generation_replacements':added==set(map(str,new)) and len(removed)==16 and all(bi[k]==('none',False) and str(int(k)+16777216) in added for k in removed),
 'all_other_original_item_fields_raw_held':omit(bis,removed)==omit(ais,added),
 'item_mgr_other_fields_raw_held':omit(bim,['items'])==omit(aim,['items']),
 'construction_other_fields_raw_held':omit(consb,['queue_mgr','item_mgr'])==omit(consa,['queue_mgr','item_mgr']),
 'only_economy_alloy_and_exact_native_research_mirror_sync':omit(q.block(be,'resources'),['alloys','physics_research','society_research','engineering_research'])==omit(q.block(ae,'resources'),['alloys','physics_research','society_research','engineering_research']) and bc['research_stockpile']==ac['research_stockpile']=={k:q.scalars(q.block(ae,'resources')).get(k,0) for k in ['physics_research','society_research','engineering_research']} and omit(be,['resources'])==omit(ae,['resources']) and omit(bm,['standard_economy_module'])==omit(am,['standard_economy_module']),
 'all_other_country0_fields_raw_held':omit(bcs['0'],['modules'])==omit(acs['0'],['modules']),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in ['country','construction','camera_focus']]==[(k,v,o) for k,v,o in af if k not in ['country','construction','camera_focus']],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['research_queues','tech_status','completed_technologies','variables','flags','traditions','ascension_perks','government','budget_categories','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['no_country0_pending']=not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks['two_native_shipyard_slots_and_actual_save_exit0']=q.scalars(aq)['simultaneous']==2 and json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0
checks['exact_camera97_to0_and_random_count_held']=q.scalars('\n'.join(k+'='+v for k,v,o in bf if not o and k in ['camera_focus','random_count']))=={'camera_focus':97,'random_count':180547719} and q.scalars('\n'.join(k+'='+v for k,v,o in af if not o and k in ['camera_focus','random_count']))=={'camera_focus':0,'random_count':180547719}
checks['exact14_new_generation0_IDs30_to43']=added-set(str(int(k)+16777216) for k in removed)==set(map(str,range(30,44)))
p={'status':'PASS_TERRAVORE_WAR1_REINFORCEMENT_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_per_ship_alloys':'98','actual_total_alloys':'2940','native_base_work':60,'UI_estimated_days':48,'native_design':385877628,'native_queue_ids':new,'replaced_old_none_handles':sorted(removed,key=int),'calendar_ready':False,'short_combat_calendar_ready':all(checks.values()),'scope':'Normal paid30 orders, exact98 alloys each,16 recycled and14 new slots; original8 military ships, remote war1 combat and incomplete colony held. Only short combat calendar eligible. No completed ships, free actual upgrade, victory or full-route claim.'}
out=run/(after+'-war1-reinforcement-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original defense payment FAIL retained; do not repeat batch or calendar'
