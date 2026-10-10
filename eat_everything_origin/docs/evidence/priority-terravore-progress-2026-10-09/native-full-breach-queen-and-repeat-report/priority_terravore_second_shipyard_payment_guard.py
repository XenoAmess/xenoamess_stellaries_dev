"""Read-only exact normal replacement shipyard payment; current modules remain until completion."""
import json,logging,shutil,sys,zipfile
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
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bcs,acs=[{k:(v,o) for k,v,o in q.fields(rt['country'])} for rt in [br,ar]]
cb,ca=br['construction'],ar['construction'];bqm,aqm=[q.block(t,'queue_mgr') for t in [cb,ca]];bqs,aqs=[q.block(t,'queues') for t in [bqm,aqm]]
bq,aq=q.block(bqs,'2'),q.block(aqs,'2');bim,aim=[q.block(t,'item_mgr') for t in [cb,ca]];bis,ais=[q.block(t,'items') for t in [bim,aim]]
bi,ai=[{k:(v,o) for k,v,o in q.fields(t)} for t in [bis,ais]];item=ai['704643077'][0]
bm,am=[q.block(t['0'][0],'modules') for t in [bcs,acs]];be,ae=[q.block(t,'standard_economy_module') for t in [bm,am]]
pre=json.loads((run/(before+'-first-corvette-proof.json')).read_text('utf-8'))
click=json.loads((run/'terravore-defense-second-shipyard-buy-click.action.json').read_text('utf-8'));exe=json.loads((run/'terravore-defense-second-shipyard-buy-click-execution.json').read_text('utf-8'))
checks={
 'bound_prior_actual_first_corvette32_PASS':pre['status']=='PASS_NATIVE_TERRAVORE_FIRST_PAID_CORVETTE_COMPONENT' and len(pre['checks'])==32 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SHA_pair':b['date']==a['date']=='2236.05.19' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'one_normal_UI_click585_588_exited0':click['action']=='left-click' and click['client_point']==[585,588] and click['foreground_after']==click['expected_hwnd'] and exe['returncode']==0,
 'actual50_alloys_paid':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==D(50),
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'},
 'only_empty_queue2_new_exact_item':not q.ids(q.block(bq,'items')) and q.ids(q.block(aq,'items'))==[704643077] and omit(bq,['items'])==omit(aq,['items']),
 'exact_payer0_queue2_work0_of180':q.scalars(item)=={'queue':2,'paying_country':0,'progress':0,'progress_needed':180},
 'exact_item50_alloys_and_slot1_shipyard_at_starbase0':q.scalars(q.block(item,'resources'))=={'alloys':50} and q.scalars(q.block(item,'buildable_starbase_module'))=={'starbase_module':'shipyard','slot':1,'starbase':0},
 'exact_complete_item_fields':[(k,o) for k,v,o in q.fields(item)]==[('queue',False),('paying_country',False),('progress',False),('progress_needed',False),('resources',True),('buildable_starbase_module',True)],
 'only_original_none_next_generation_replacement':set(bi)-set(ai)=={'687865861'} and set(ai)-set(bi)=={'704643077'} and bi['687865861']==('none',False) and 687865861+16777216==704643077,
 'all_other_items_raw_held':omit(bis,['687865861'])==omit(ais,['704643077']),
 'all_other_queues_raw_held_including19_ship_orders':omit(bqs,['2'])==omit(aqs,['2']) and len(q.ids(q.block(q.block(aqs,'3'),'items')))==19,
 'queue_mgr_other_fields_raw_held':omit(bqm,['queues'])==omit(aqm,['queues']),
 'item_mgr_other_fields_raw_held':omit(bim,['items'])==omit(aim,['items']),
 'construction_other_fields_raw_held':omit(cb,['queue_mgr','item_mgr'])==omit(ca,['queue_mgr','item_mgr']),
 'only_actual_alloy_resource_field_changed':omit(q.block(be,'resources'),['alloys'])==omit(q.block(ae,'resources'),['alloys']) and omit(be,['resources'])==omit(ae,['resources']) and omit(bm,['standard_economy_module'])==omit(am,['standard_economy_module']),
 'all_other_country0_raw_held':omit(bcs['0'][0],['modules'])==omit(acs['0'][0],['modules']),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'all_other_top_level_sequence_raw_held':[(k,v,o) for k,v,o in bf if k not in ['country','construction']]==[(k,v,o) for k,v,o in af if k not in ['country','construction']],
 'original_modules_and_starbase_raw_held':br['starbase_mgr']==ar['starbase_mgr'] and q.scalars(q.block(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),'modules'))=={'0':'shipyard','1':'solar_panel_network'},
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['research_queues','tech_status','completed_technologies','variables','flags','traditions','ascension_perks','government','budget_categories','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TERRAVORE_SECOND_SHIPYARD_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_alloys_paid':50,'order':704643077,'slot':1,'native_base_work':180,'scope':'Only normal paid module replacement order. Existing solar module and first shipyard remain; second shipyard not complete. No defense, maintenance or full route success claim.'}
out=run/(after+'-second-shipyard-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original module payment FAIL retained; no next calendar'
