"""Read-only exact native PSI Corps replacement payment, no UI actions."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:];building='building_psi_corps';zone=0;price=400
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
 'native_progress0_480':sc.get('progress')==0 and sc.get('progress_needed')==480,
 'native_building_mother_zone':q.scalars(q.block(item,'buildable_planet_replace_building'))=={'building':building,'planet':0,'zone':zone,'replace_building':45},
 'actual_error_original_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','planets','districts','deposits','species','situations','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['mother_last_building_changed_exact']=a['colonies']['0'].get('last_building_changed')==building
checks['all_colonies_except_exact_mother_building_record_held']=set(a['colonies'])==set(b['colonies']) and all(({k:v for k,v in a['colonies'][i].items() if k!='last_building_changed'}=={k:v for k,v in c.items() if k!='last_building_changed'}) if i=='0' else a['colonies'][i]==c for i,c in b['colonies'].items())
checks['all_zones_and_buildings_raw_held']=br['zones']==ar['zones'] and br['buildings']==ar['buildings']

prior=json.loads((run/(before+'-unity-nodes-month-proof.json')).read_text('utf-8'))
ex=json.loads((run/'terravore-unity-nodes-month-ledger-execution.json').read_text('utf-8'))
click=json.loads((run/'terravore-psi-replace-paid-click.action.json').read_text('utf-8'))
clickex=json.loads((run/'terravore-psi-replace-paid-click-execution.json').read_text('utf-8'))
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
checks['prior_month16_PASS_actual_execution_zero']=prior['status']=='PASS_TERRAVORE_PAID_ECONOMY_MONTH_COMPONENT' and len(prior['checks'])==16 and all(prior['checks'].values()) and prior['after_sha256']==b['save_sha256'] and ex['returncode']==0
checks['unique_native_UI_click_bound']=click['action']=='left-click' and click['client_point']==[835,279] and clickex['returncode']==0
checks['all_other_original_construction_items_raw_held']=set(bi)<=set(ai) and all(ai[i]==v for i,v in bi.items()) and set(ai)-set(bi)==set(map(str,added))
bqs=q.block(q.block(br['construction'],'queue_mgr'),'queues');aqs=q.block(q.block(ar['construction'],'queue_mgr'),'queues')
checks['other_queues_raw_held']=omit(bqs,{'0'})==omit(aqs,{'0'}) and omit(bq,{'items'})==omit(aq,{'items'})
checks['all_ships_raw_held']=br['ships']==ar['ships']
checks['source_node45_correct_slot3']=q.scalars(q.block(br['buildings'],'45'))=={'type':'building_hive_node','position':3} and q.ids(q.block(q.block(br['zones'],'0'),'buildings'))==[33554466,1,2,45,46,48]
def pending(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return [q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
checks['no_pending_native_events']=not pending(before) and not pending(after)
sources=[h.GAME_EXE.parent/'common/buildings/02_government_buildings.txt',h.GAME_EXE.parent/'common/scripted_variables/00_scripted_variables.txt']
checks['native_psi_base480_upkeep5']=q.scalars(q.block(sources[0].read_text('utf-8-sig'),'building_psi_corps')).get('base_buildtime')=='@b2_time' and q.scalars(sources[1].read_text('utf-8-sig')).get('@b2_time')==480 and q.scalars(sources[1].read_text('utf-8-sig')).get('@b2_upkeep')==5

proof={'status':'PASS_NATIVE_PAID_PSI_REPLACEMENT_ORDER' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'expected_actual_price':price,'native_sources':[{'path':str(p),'sha256':h.sha256(p)} for p in sources],'native_item_raw':item,'mineral_before_after':[bc['effective_stockpile']['minerals'],ac['effective_stockpile']['minerals']],'scope':'Actual one paid order only; completion, jobs and monthly maintenance require later evidence.'}
out=run/(after+'-psi-replacement-paid-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original order failure retained; do not repeat purchase'
