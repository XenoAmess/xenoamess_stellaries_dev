import json, logging, shutil, subprocess, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools'); sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO); h=r.harness; run,user,m=h.load_run()
shutil.copyfile(__file__,run/Path(__file__).name)
def state(stem): return json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
def native(stem):
    with zipfile.ZipFile(run/(stem+'.sav')) as z: raw=z.read('gamestate').decode('utf-8-sig')
    construction=q.block(raw,'construction')
    queue=q.block(q.block(q.block(construction,'queue_mgr'),'queues'),'0')
    items=q.block(q.block(construction,'item_mgr'),'items')
    ids=q.ids(q.block(queue,'items'))
    pending=[q.scalars(v) for k,v,o in q.fields(raw) if k=='player_event' and o and q.scalars(v).get('country')==0]
    return ids,{str(i):q.block(items,str(i)) for i in ids},pending
before='organic-third-postsettlement-nextmonth'; rows=[]
phases=[('organic-farm6-completed','2304.05.02',210,6,3,1800,600,7),('organic-mine4-completed','2305.01.02',240,6,4,1800,800,8)]
for stage,date,days,farmlevel,minelevel,farmcap,minecap,months in phases:
    b=state(before); bid,bi,bpending=native(before); assert not bpending,'Handle actual pending event before more calendar'
    driver=subprocess.run([sys.executable,'_runtime/heart-of-devouring/formal_native_calendar_recorded.py',before,date,stage,str(days)],capture_output=True)
    (run/(stage+'-completion-driver-stdout.txt')).write_bytes(driver.stdout)
    (run/(stage+'-completion-driver-stderr.txt')).write_bytes(driver.stderr)
    assert driver.returncode==0,'Original calendar failure retained; no date replay'
    a=state(stage); aid,ai,pending=native(stage); bc,ac=b['countries']['0'],a['countries']['0']
    eb=(run/(stage+'-error-before.log')).read_bytes(); ea=(run/(stage+'-error-after.log')).read_bytes()
    checks={'actual_date':a['date']==date,'no_new_errors':ea==eb,'EEP_variables_held':bc['variables']==ac['variables'],'EEP_flags_held':bc['flags']==ac['flags'],'AP_traditions_government_owned_colonies_held':all(bc[k]==ac[k] for k in ('ascension_perks','traditions','government','owned_colonies')),'latent_family_definitions_held':all(b['species'][k]==a['species'][k] for k in ('102','103')),'mother_core_unique_owned':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and a['planets']['7']['owner']==a['planets']['7']['controller']==0,'capacity12_held':a['planets']['7']['variables']['eep_capacity_value']==12,'farm_level_exact':a['districts']['3']['level']==farmlevel,'mine_level_exact':a['districts']['2']['level']==minelevel,'farmer_capacity_exact':a['pop_jobs']['27']['max_workforce']==farmcap,'miner_capacity_exact':a['pop_jobs']['26']['max_workforce']==minecap,'native_shroud_progress_exact':D(str(a['situations']['33554438']['progress']))-D(str(b['situations']['33554438']['progress']))==D('3.75')*months,'native_threads_exact':D(str(ac['effective_stockpile']['astral_threads']))-D(str(bc['effective_stockpile']['astral_threads']))==3*months,'all_primary_stock_positive':all(ac['effective_stockpile'][k]>0 for k in ('energy','minerals','food','consumer_goods','alloys','unity')),'no_pending_native_events':not pending}
    if stage=='organic-farm6-completed':
        checks.update(farm_item_removed=bid==[721420313,1241514008] and aid==[1241514008],second_mine_item_raw_held=ai.get('1241514008')==bi.get('1241514008'))
    else: checks.update(mine_item_removed=bid==[1241514008] and aid==[])
    balance=ac['budget_categories']['current_month']['balance']; net={k:str(sum((D(str(v.get(k,0))) for v in balance.values()),D(0))) for k in ('energy','minerals','food','consumer_goods','alloys','unity')}
    proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_date':a['date'],'native_queue_before':bid,'native_queue_after':aid,'pending_native_events':pending,'actual_primary_net':net,'actual_stocks':ac['effective_stockpile'],'mother_actual_pop':a['colonies']['0']['actual_pop_sum'],'actual_mother_jobs':{k:a['pop_jobs'][k] for k in ('26','27')},'scope':'Natural paid serial district completion and exact native progress guard. Population growth is observed; no grants or whole civic acceptance.'}
    h.write_json(run/(stage+'-proof.json'),proof); rows.append(proof); print(json.dumps(proof),flush=True)
    assert all(checks.values()),'Original completion guard FAIL retained; stop next phase'
    before=stage
h.write_json(run/'organic-farm6-mine4-completion-result.json',{'status':'PASS_SCOPED','completed':rows})
