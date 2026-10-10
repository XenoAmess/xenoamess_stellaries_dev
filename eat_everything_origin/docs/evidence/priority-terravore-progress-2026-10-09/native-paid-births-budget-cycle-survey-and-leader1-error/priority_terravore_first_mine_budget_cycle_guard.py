"""Read-only one budget cycle after the first paid mine; native caps explicit."""
import json,logging,shutil,sys,re
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
assert not dest.exists() or dest.read_bytes()==Path(__file__).read_bytes()
if not dest.exists():shutil.copyfile(__file__,dest)
def load(name):return json.loads((run/name).read_text('utf-8'))
before='terravore-war1-first-mine-complete';after='terravore-war1-idle10-step3'
b=load(before+'.audit.json');a=load(after+'.audit.json');bc,ac=[v['countries']['0'] for v in [b,a]]
first=load(before+'-war1-battle-v21-proof.json');firstex=load(before+'-battle-v21-execution.json')
observer_sha='25a72330367ddb31328665dd068d47c0e8e05b2f8c1fb4d46388be44a894b173'
wrapper_sha='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3'
def valid(proof,ex,count):return proof['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(proof['checks'])==count and all(v is True for v in proof['checks'].values()) and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v21.py')==observer_sha and ex['wrapper_sha256']==wrapper_sha
chain=[];previous=before;days=0;chain_valid=True
for i in range(1,4):
 stage=f'terravore-war1-idle10-step{i}';p=load(stage+'-war1-battle-v21-proof.json');ex=load(stage+'-battle-v21-execution.json');cal=load(stage+'-calendar-receipt.json');ce=load(stage+'-calendar-execution.json');old=load(previous+'.audit.json')
 chain_valid &= valid(p,ex,39) and p['before_sha256']==old['save_sha256']==h.sha256(run/(previous+'.sav')) and p['after_sha256']==h.sha256(run/(stage+'.sav')) and cal['start_date']==old['date'] and cal['date']==p['date'] and cal['days']==p['days'] and ce['returncode']==0 and ce['helper_sha256']=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc'
 days+=cal['days'];chain.append({'stage':stage,'date':p['date'],'days':cal['days'],'save_sha256':p['after_sha256']});previous=stage
cur=ac['budget_categories']['current_month'];keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence'];net={k:sum((D(str(v.get(k,0))) for v in cur['balance'].values()),D(0)) for k in keys};delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in keys};residual={k:delta[k]-net[k] for k in keys}
source=h.GAME_ROOT/'common/strategic_resources/00_strategic_resources.txt' if hasattr(h,'GAME_ROOT') else Path('C:/SteamLibrary/steamapps/common/Stellaris/common/strategic_resources/00_strategic_resources.txt')
source_sha='140dea921a77f76726f361eca99f59f0c7755e4e728dec4699d3b732457911a4';target=run/'native-first-mine-budget-00_strategic_resources.txt';assert h.sha256(source)==source_sha
if target.exists():assert h.sha256(target)==source_sha
else:shutil.copyfile(source,target)
ui=load('terravore-trade-cap-exact-visible.ocr.json');driver=load('terravore-war1-idle10-driver-execution.json');batch=load('terravore-war1-idle10-batch-result.json')
checks={
 'production_language_version_and_package_held':m['version']=='0.2.0' and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'exact_first_mine_and_cycle_SAV_pair':b['date']=='2269.05.01' and a['date']=='2269.06.05' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='f27135be8da8d895a474d4db9d5be4252db370f87e79d305f275d22613c1c62b' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='15a97e2ab03112419c72557fb081205cfa9f95fd16741006d415ab18318e063b',
 'first40_PASS_actual0_source_bound':valid(first,firstex,40),
 'three_contiguous_native_calendars_39_PASS_each_actual0_total34_one_month_boundary':bool(chain_valid) and days==34 and [v['days'] for v in chain]==[14,14,6] and [v['date'] for v in chain]==['2269.05.15','2269.05.29','2269.06.05'],
 'original_driver_actual0_and_exact_three_step_result':driver['returncode']==0 and driver['helper_sha256']==h.sha256(run/'priority_terravore_idle_war_driver_v12.py')=='c02a68f9110aeb24ae0a289803db1389b2b19bae9e50a6be63ba17532d7cf581' and batch['stop']=='new_paid_birth' and batch['days']==34 and batch['last_stage']==after,
 'six_uncapped_stock_deltas_equal_native_budget':all(abs(residual[k])<D('0.00005') for k in keys if k not in ['trade','influence']),
 'last_month_equals_original_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'actual_positive_energy_minerals_alloys_unity':all(net[k]>0 for k in ['energy','minerals','alloys','unity']),
 'two_native_capped_stocks_no_fabricated_income':all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap and net[k]>0 and delta[k]==0 and residual[k]==-net[k] for k,cap in [('influence',1000),('trade',50000)]),
 'exact_native_capped_income_not_stored':net['influence']==7 and net['trade']==D('94.55669'),
 'native_cap_source_and_current_July13_UI50000_of50000_bound':h.sha256(target)==source_sha and h.sha256(run/'terravore-trade-cap-exact-visible.jpg')==ui['image_sha256']=='a75d109f58197435b1ef8d25a380383c7d2e90d2d1031b6059a41e9fb529e0d6' and any('50000/50000' in v['text'] for v in ui['rows']) and any('2269.07.13' in v['text'] for v in ui['rows']),
 'actual_mining_full2600_and_income193point05_upkeep11point7':a['pop_jobs']['29']['workforce']==a['pop_jobs']['29']['max_workforce']==2600 and cur['income']['planet_miners']=={'minerals':193.05} and cur['expenses']['planet_districts_mining']=={'energy':11.7},
 'mother_structures_same_and_mining13':all(b['districts'][str(i)]==a['districts'][str(i)] for i in [1,2,3]) and a['districts']['3']['level']==13,
 'actual_housing13200_positive_amenities_stability80_crime0':all(a['colonies']['0'][k]==v for k,v in {'total_housing':13200,'stability':80,'crime':0}.items()) and a['colonies']['0']['free_housing']>0 and a['colonies']['0']['free_amenities']>0,
 'native_population_growth7_no_mine_created_population':a['colonies']['0']['actual_pop_sum']-b['colonies']['0']['actual_pop_sum']==7 and a['colonies']['0']['actual_pop_sum']==10776,
 'EEP_flags_variables_and_bound_capacity_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and ac['variables']['eep_c']==37 and ac['variables']['eep_d']==11 and a['planets']['7']['variables']['eep_capacity_value']==11,
 'original_cycle_unfiltered2670_errors_no_increment':all((run/(stage+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes() and (run/(stage+'-error-after.log')).stat().st_size==2670 for stage in [before,*[v['stage'] for v in chain]]),
}
checks={k:bool(v) for k,v in checks.items()};proof={'status':'PASS_TERRAVORE_FIRST_PAID_MINE_ONE_BUDGET_CYCLE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'observed_native_days':days,'chain':chain,'native_budget_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'uncapped_and_capped_residuals':{k:str(v) for k,v in residual.items()},'actual_mining_job':a['pop_jobs']['29'],'actual_colony':a['colonies']['0'],'calendar_ready':False,'scope':'One budget cycle across34 native days following first mine; six stocks close and two capped positive incomes discarded. Capacity UI observed later July13, not at May/June endpoints. Existing2670 errors held for this cycle; later June19 native error separately retained. Not all three mines, heavy industry conversion, strict zero game errors or full-route acceptance.'};out=run/'terravore-war1-first-mine-budget-cycle-proof.json';assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v]}),flush=True);assert all(checks.values()),'Budget cycle original failure retained'
