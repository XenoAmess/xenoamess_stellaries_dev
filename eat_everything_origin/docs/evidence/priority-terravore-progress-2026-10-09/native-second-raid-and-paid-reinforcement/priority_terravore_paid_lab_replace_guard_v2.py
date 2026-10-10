"""Read-only exact native PSI Corps replacement payment, no UI actions."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,raw_old,raw_pos,raw_price,clickstage,raw_x,raw_y,priorfile,priorstage,raw_count=sys.argv[1:];oldid,position,price,x,y,expected_count=map(int,[raw_old,raw_pos,raw_price,raw_x,raw_y,raw_count]);building='building_research_lab_1';zone=2
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 roots={k:v for k,v,o in q.fields(t) if o};c=roots['construction']
 queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0')
 items={k:v for k,v,o in q.fields(q.block(q.block(c,'item_mgr'),'items')) if o}
 return a,roots,queue,items
b,br,bq,bi=read(before);a,ar,aq,ai=read(after);bc,ac=b['countries']['0'],a['countries']['0']
old=q.ids(q.block(bq,'items'));new=q.ids(q.block(aq,'items'));added=[i for i in new if i not in old]
item=ai.get(str(added[0]),'') if len(added)==1 else '';sc=q.scalars(item)
checks={'same_actual_date':a['date']==b['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_expected_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==price,
 'all_other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'only_one_appended_mother_order':len(added)==1 and new==old+added,
 'old_mother_orders_raw_held':all(ai.get(str(i))==bi[str(i)] for i in old),
 'native_paid_country_queue':sc.get('queue')==sc.get('paying_country')==0,
 'native_resources_expected_price':q.scalars(q.block(item,'resources'))=={'minerals':price},
 'native_progress0_360':sc.get('progress')==0 and sc.get('progress_needed')==360,
 'native_building_mother_zone':q.scalars(q.block(item,'buildable_planet_replace_building'))=={'building':building,'planet':0,'zone':zone,'replace_building':oldid},
 'actual_error_original_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','planets','districts','deposits','species','situations','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['mother_last_building_changed_exact']=a['colonies']['0'].get('last_building_changed')==building
checks['all_colonies_except_exact_mother_building_record_held']=set(a['colonies'])==set(b['colonies']) and all(({k:v for k,v in a['colonies'][i].items() if k!='last_building_changed'}=={k:v for k,v in c.items() if k!='last_building_changed'}) if i=='0' else a['colonies'][i]==c for i,c in b['colonies'].items())
checks['all_zones_and_buildings_raw_held']=br['zones']==ar['zones'] and br['buildings']==ar['buildings']

prior=json.loads((run/(priorfile)).read_text('utf-8'))
ex=json.loads((run/(priorstage+'-execution.json')).read_text('utf-8'))
click=json.loads((run/(clickstage+'.action.json')).read_text('utf-8'))
clickex=json.loads((run/(clickstage+'-execution.json')).read_text('utf-8'))
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
checks['prior_exact_PASS_actual_execution_zero']=prior['status'] in ['PASS_TERRAVORE_NEMESIS_PROJECT1_FIRST_MONTH_LEDGER_COMPONENT','PASS_NATIVE_PAID_LAB_REPLACEMENT_ORDER_V2'] and len(prior['checks'])==expected_count and all(prior['checks'].values()) and prior['after_sha256']==b['save_sha256'] and ex['returncode']==0
checks['unique_native_UI_click_bound']=click['action']=='left-click' and click['client_point']==[x,y] and clickex['returncode']==0
checks['all_other_original_construction_items_raw_held']=set(bi)<=set(ai) and all(ai[i]==v for i,v in bi.items()) and set(ai)-set(bi)==set(map(str,added))
bqs=q.block(q.block(br['construction'],'queue_mgr'),'queues');aqs=q.block(q.block(ar['construction'],'queue_mgr'),'queues')
checks['other_queues_raw_held']=omit(bqs,{'0'})==omit(aqs,{'0'}) and omit(bq,{'items'})==omit(aq,{'items'})
checks['all_ships_raw_held']=br['ships']==ar['ships']
checks['source_node_correct_zone2_slot']=oldid in [38,41] and position in [0,2] and q.scalars(q.block(br['buildings'],str(oldid)))=={'type':'building_hive_node','position':position} and q.ids(q.block(q.block(br['zones'],'2'),'buildings'))==[38,16777251,41]
def pending(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return [q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
checks['no_pending_native_events']=not pending(before) and not pending(after)
sources=[h.GAME_EXE.parent/part for part in ['common/buildings/05_research_buildings.txt','common/scripted_variables/00_scripted_variables.txt','common/scripted_variables/100_scripted_variables_zones.txt','common/inline_scripts/jobs/researchers_add.txt']]
base=q.scalars(q.block(sources[0].read_text('utf-8-sig'),building));values=q.scalars(sources[1].read_text('utf-8-sig'));job_values=q.scalars(sources[2].read_text('utf-8-sig'))
checks['native_lab_base360_cost400_upkeep2_each60']=base.get('base_buildtime')=='@b1_time' and values.get('@b1_time')==360 and values.get('@b1_minerals')==400 and values.get('@b1_upkeep')==2 and job_values.get('@building_static_jobs_3')==60
checks['native_project_events_and_crisis_held']=all(q.block(q.block(br['country'],'0'),k)==q.block(q.block(ar['country'],'0'),k) for k in ['events','crisis_progression'])
checks['all_true_research_banks_held']=bc['research_stockpile']==ac['research_stockpile']
checks['all_budget_categories_raw_audit_held']=bc['budget_categories']==ac['budget_categories']
checks['save_actual_exit0']=json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0

if oldid==38:
 original=json.loads((run/(after+'-lab-replacement-paid-proof.json')).read_text('utf-8'));oldex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
 checks['bound_original41_exact_old_prior_failure_or_second_V2_chain']=original['status']=='FAIL' and len(original['checks'])==41 and [k for k,v in original['checks'].items() if v is not True]==['prior_month16_PASS_actual_execution_zero'] and original['before_sha256']==b['save_sha256'] and original['after_sha256']==a['save_sha256'] and oldex['returncode']==1 and oldex['helper_sha256']=='6493e9c52afe573e8f8a9b29077b823470f1b12606600d03b493099af44ee58f'
else:
 checks['bound_original41_exact_old_prior_failure_or_second_V2_chain']=oldid==41 and before=='terravore-lab-node38-paid' and prior['status']=='PASS_NATIVE_PAID_LAB_REPLACEMENT_ORDER_V2' and len(prior['checks'])==42 and ex['returncode']==0

proof={'status':'PASS_NATIVE_PAID_LAB_REPLACEMENT_ORDER_V2' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'expected_actual_price':price,'native_sources':[{'path':str(p),'sha256':h.sha256(p)} for p in sources],'native_item_raw':item,'mineral_before_after':[bc['effective_stockpile']['minerals'],ac['effective_stockpile']['minerals']],'scope':'Actual one paid order only; completion, jobs and monthly maintenance require later evidence.'}
out=run/(after+'-lab-replacement-paid-v2-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original order failure retained; do not repeat purchase'
