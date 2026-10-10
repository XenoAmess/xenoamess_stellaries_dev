"""Read-only actual month after all three normally paid districts complete."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,mining,generator=sys.argv[1:];mining,generator=int(mining),int(generator);assert mining>0 and generator>0
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
wait=json.loads((run/(after+'-postwar-boundary-proof.json')).read_text('utf-8'))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
with zipfile.ZipFile(run/(after+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,o in q.fields(t) if o};growth=q.scalars(q.block(q.block(q.block(roots['colony'],'0'),'last_month_growth_data'),'growth_and_size'))
net={};residual={}
for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']:
 net[k]=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
 residual[k]=D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-net[k]
resource_source=h.GAME_EXE.parent/'common/strategic_resources/00_strategic_resources.txt'
influence_spec=q.scalars(q.block(resource_source.read_text('utf-8-sig'),'influence'))
raw_residual=dict(residual)
expected_influence=min(D('1000'),D(str(bc['effective_stockpile']['influence']))+net['influence'])
residual['influence']=D(str(ac['effective_stockpile']['influence']))-expected_influence
workers={j['type']:{k:j[k] for k in ['workforce','max_workforce','workforce_limit']} for j in a['pop_jobs'].values() if j['planet']==0 and j['type'] in ['mining_drone','technician_drone']}
with zipfile.ZipFile(run/(before+'.sav')) as z:bt=z.read('gamestate').decode('utf-8-sig')
br={k:v for k,v,o in q.fields(bt) if o}
queue_ids=lambda rt:q.ids(q.block(q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),'0'),'items'))
levels=lambda v:{v['districts'][str(i)]['type']:v['districts'][str(i)]['level'] for i in v['colonies']['0']['districts']}
bl,al=levels(b),levels(a)
checks={'original_fixed_influence_cap1000':influence_spec.get('max')==1000 and influence_spec.get('fixed_max_amount')=='yes','passed_bound_construction_wait':wait['status']=='PASS_NATIVE_TERRAVORE_POSTWAR_COMPONENT' and all(wait['checks'].values()) and wait['before_sha256']==b['save_sha256'] and wait['after_sha256']==a['save_sha256'],
 'actual_one_month_calendar':receipt['days']==30 and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'expected_paid_districts_completed_empty_queue':not queue_ids(br) and not queue_ids(roots) and bl==al and al['district_mining']==mining and al['district_generator']==generator,
 'expected_mining_generator_actual_full_workers':workers['mining_drone']['workforce']==workers['mining_drone']['max_workforce']==mining*200 and workers['technician_drone']['workforce']==workers['technician_drone']['max_workforce']==generator*200,
 'native_month_growth_exact_population_change':growth['month_start_size']==b['colonies']['0']['actual_pop_sum'] and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+growth['growth'],
 'all_eight_actual_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'independent_last_month_equals_prior_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'actual_energy_and_minerals_net_positive':net['energy']>0 and net['minerals']>0}
checks['actual_calendar_and_boundary_execution_zero']=json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0 and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==0
proof={'status':'PASS_TERRAVORE_PAID_ECONOMY_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_native_growth':growth,'original_resource_source_sha256':h.sha256(resource_source),'expected_mining_generator_levels':[mining,generator],'raw_uncapped_budget_residuals':{k:str(v) for k,v in raw_residual.items()},'expected_influence_after_cap':str(expected_influence),'actual_budget_residuals':{k:str(v) for k,v in residual.items()},'actual_current_month_net':{k:str(v) for k,v in net.items()},'actual_stockpile':ac['effective_stockpile'],'actual_native_maintenance':{k:ac['budget_categories']['current_month']['expenses'].get(k,{}) for k in ['ships','ship_components','starbase_modules','planet_districts_generator','planet_buildings']},'actual_last_month_categories':ac['budget_categories']['last_month'],'actual_current_month_categories':ac['budget_categories']['current_month'],'scope':'One actual post-construction month, paid districts and actual staffed workers. No 20-year, ascension, crisis or first-reload acceptance claim.'}
out=run/(after+'-postwar-month-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original paid economy month FAIL retained'
