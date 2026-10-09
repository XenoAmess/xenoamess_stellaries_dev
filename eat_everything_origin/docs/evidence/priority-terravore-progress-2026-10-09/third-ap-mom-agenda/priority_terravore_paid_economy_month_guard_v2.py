"""Read-only actual month after all three normally paid districts complete."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
wait=json.loads((run/(after+'-paid-wait-v2-proof.json')).read_text('utf-8'))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
with zipfile.ZipFile(run/(after+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,o in q.fields(t) if o};growth=q.scalars(q.block(q.block(q.block(roots['colony'],'0'),'last_month_growth_data'),'growth_and_size'))
net={};residual={}
for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']:
 net[k]=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
 residual[k]=D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-net[k]
workers=wait['actual_workers_before_after'][1]
checks={'passed_bound_construction_wait':wait['status']=='PASS_TERRAVORE_PAID_CONSTRUCTION_WAIT_COMPONENT' and all(wait['checks'].values()) and wait['before_sha256']==b['save_sha256'] and wait['after_sha256']==a['save_sha256'],
 'actual_one_month_calendar':receipt['days']==30 and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'all_three_paid_orders_completed':not wait['actual_queue_before_after'][0] and not wait['actual_queue_before_after'][1] and wait['actual_district_levels_before_after'][0]==wait['actual_district_levels_before_after'][1] and wait['actual_district_levels_before_after'][1]['district_mining']==8 and wait['actual_district_levels_before_after'][1]['district_generator']==3,
 'mining1600_generator600_actual_full_workers':workers['mining_drone']['workforce']==workers['mining_drone']['max_workforce']==1600 and workers['technician_drone']['workforce']==workers['technician_drone']['max_workforce']==600,
 'native_month_growth_exact_population_change':growth['month_start_size']==b['colonies']['0']['actual_pop_sum'] and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+growth['growth'],
 'all_eight_actual_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'independent_last_month_equals_prior_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'actual_energy_and_minerals_net_positive':net['energy']>0 and net['minerals']>0}
proof={'status':'PASS_TERRAVORE_PAID_ECONOMY_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_native_growth':growth,'actual_budget_residuals':{k:str(v) for k,v in residual.items()},'actual_current_month_net':{k:str(v) for k,v in net.items()},'actual_stockpile':ac['effective_stockpile'],'actual_last_month_categories':ac['budget_categories']['last_month'],'actual_current_month_categories':ac['budget_categories']['current_month'],'scope':'One actual post-construction month, paid districts and actual staffed workers. No 20-year, ascension, crisis or first-reload acceptance claim.'}
out=run/(after+'-paid-economy-month-v2-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original paid economy month FAIL retained'
