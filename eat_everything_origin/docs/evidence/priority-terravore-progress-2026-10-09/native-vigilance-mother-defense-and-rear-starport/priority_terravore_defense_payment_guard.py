"""Read-only exact twenty-corvette native queue and fractional payment proof."""
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
pre=json.loads((run/(before+'-native-voidworm-ack-proof.json')).read_text('utf-8'))
obs=json.loads((run/(after+'-observation.json')).read_text('utf-8'))
clicks=[]
for stage in obs['click_stages']:
 clicks.append((json.loads((run/(stage+'.action.json')).read_text('utf-8')),json.loads((run/(stage+'-execution.json')).read_text('utf-8'))))
items=[ai[str(i)][0] for i in new]
design=q.block(ar['ship_design'],'67110548')
checks={
 'bound_actual_prior26_ACK_PASS':pre['status']=='PASS_NATIVE_TERRAVORE_VOIDWORM_ACK_COMPONENT' and len(pre['checks'])==26 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SHA_pair':b['date']==a['date']=='2236.04.01' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact20_unique_normal_paid_clicks':len(clicks)==len(set(obs['click_stages']))==20 and all(c['action']=='left-click' and c['client_point']==[565,403] and c['foreground_after']==c['expected_hwnd'] and e['returncode']==0 for c,e in clicks),
 'only20_appended_original_empty_shipyard_queue':old==[] and len(new)==len(set(new))==20 and omit(bq,['items'])==omit(aq,['items']),
 'each_native_payer0_queue3_progress0_base60':all(q.scalars(t)=={'queue':3,'paying_country':0,'progress':0,'progress_needed':60} for t in items),
 'each_native_actual_alloy89_6_total1792':all(q.scalars(q.block(t,'resources'))=={'alloys':89.6} for t in items) and sum((D(str(q.scalars(q.block(t,'resources'))['alloys'])) for t in items),D(0))==D(1792),
 'actual_stock_exact1792_paid':D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==D(1792),
 'UI90_is_ceiling_of_actual89_6':math.ceil(D('89.6'))==90 and h.sha256(run/'terravore-defense-design-prices-capture.jpg')=='397ced1c8e929a753123398e9be916d72c588adeed7a360ad268ea0d721e68f3',
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='alloys'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='alloys'},
 'all20_original_corvette_design_at_starbase0':all(q.scalars(q.block(q.block(t,'buildable_ship'),'ship_design_implementation'))=={'design':67110548,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(q.block(t,'buildable_ship'),'orbitable'))=={'starbase':0} for t in items) and q.scalars(q.block(design,'name'))=={'key':'HUMAN1_SHIP_Surik'} and bool(re.search(r'ship_size="corvette"',design)) and 67110548 in q.ids(q.block(q.block(acs['0'],'ship_design_collection'),'ship_design')),
 'only_named_fields_in20_items':all([(k,o) for k,v,o in q.fields(t)]==[('queue',False),('paying_country',False),('progress',False),('progress_needed',False),('resources',True),('buildable_ship',True)] and [(k,o) for k,v,o in q.fields(q.block(t,'buildable_ship'))]==[('ship_design_implementation',True),('orbitable',True)] for t in items),
 'all_other_queue_records_raw_held':omit(bqs,['3'])==omit(aqs,['3']),
 'queue_mgr_other_fields_raw_held':omit(bqm,['queues'])==omit(aqm,['queues']),
 'only20_new_items_and11_none_generation_replacements':added==set(map(str,new)) and len(removed)==11 and all(bi[k]==('none',False) and str(int(k)+16777216) in added for k in removed) and len([k for k in added if int(k)&16777215>=18])==9,
 'all_other_original_item_fields_raw_held':omit(bis,removed)==omit(ais,added),
 'item_mgr_other_fields_raw_held':omit(bim,['items'])==omit(aim,['items']),
 'construction_other_fields_raw_held':omit(consb,['queue_mgr','item_mgr'])==omit(consa,['queue_mgr','item_mgr']),
 'only_economy_actual_alloy_field_changed':omit(q.block(be,'resources'),['alloys'])==omit(q.block(ae,'resources'),['alloys']) and omit(be,['resources'])==omit(ae,['resources']) and omit(bm,['standard_economy_module'])==omit(am,['standard_economy_module']),
 'all_other_country0_fields_raw_held':omit(bcs['0'],['modules'])==omit(acs['0'],['modules']),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in ['country','construction']]==[(k,v,o) for k,v,o in af if k not in ['country','construction']],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['research_queues','tech_status','completed_technologies','variables','flags','traditions','ascension_perks','government','budget_categories','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TERRAVORE_DEFENSE_CORVETTE_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_per_ship_alloys':'89.6','actual_total_alloys':'1792','native_base_work':60,'UI_estimated_days':48,'native_design':67110548,'native_queue_ids':new,'replaced_old_none_handles':sorted(removed,key=int),'scope':'Normal paid20 corvette orders only. UI rounded90 is not exact price; no ships spawned yet, no completion/maintenance/defense/crisis or full route claim.'}
out=run/(after+'-defense-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original defense payment FAIL retained; do not repeat batch or calendar'
