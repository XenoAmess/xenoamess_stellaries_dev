"""Three paid mines, one actual budget cycle; negative E/A explicitly retained."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
load=lambda name:json.loads((run/name).read_text('utf-8'))
before='terravore-war1-idle21-step2';after='terravore-war1-idle22-step1'
b,a=[load(st+'.audit.json') for st in [before,after]];bc,ac=b['countries']['0'],a['countries']['0']
def valid(st,version,count,sha):
 p=load(st+'-war1-battle-v'+str(version)+'-proof.json');e=load(st+'-battle-v'+str(version)+'-execution.json')
 return p['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(p['checks'])==count and all(v is True for v in p['checks'].values()) and p['after_sha256']==h.sha256(run/(st+'.sav')) and e['returncode']==0 and e['helper_sha256']==h.sha256(run/('priority_terravore_war1_battle_observer_v'+str(version)+'.py'))==sha
chain=[];previous=before;chain_valid=True
for st,days in [('terravore-mother-clear-first-work',1),(after,29)]:
 p=load(st+'-war1-battle-v32-proof.json');cal=load(st+'-calendar-receipt.json');ex=load(st+'-calendar-execution.json');old=load(previous+'.audit.json')
 chain_valid &= valid(st,32,50,'01747d1c4dc472f10f46cf644492cf4ea705252a13d887902c38624c62603f57') and cal['days']==p['days']==days and cal['start_date']==old['date'] and cal['date']==p['date'] and p['before_sha256']==old['save_sha256']==h.sha256(run/(previous+'.sav')) and ex['returncode']==0 and ex['helper_sha256']=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc'
 chain.append({'stage':st,'date':p['date'],'days':days,'save_sha256':p['after_sha256']});previous=st
cur=ac['budget_categories']['current_month'];keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
net={k:sum((D(str(v.get(k,0))) for v in cur['balance'].values()),D(0)) for k in keys};delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in keys};residual={k:delta[k]-net[k] for k in keys}
driver=load('terravore-war1-idle22-driver-execution.json');batch=load('terravore-war1-idle22-batch-result.json')
with zipfile.ZipFile(run/(after+'.sav')) as z:top={k:v for k,v,o in q.fields(z.read('gamestate').decode('utf-8-sig')) if o}
last=[q.block(q.block(top['colony'],str(i)),'last_month_growth_data') for i in [0,37]]
growth=[q.scalars(q.block(v,'growth_and_size')) for v in last]
detail=[[(k,q.unquote(v),o) for k,v,o in q.fields(q.block(raw,'current_month_growth_details'))] for raw in last]
checks={
 'production02_Chinese_package_tree_held':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'exact_completion_and_30day_endpoint_SHA_pair':b['date']=='2270.04.15' and a['date']=='2270.05.15' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='77b4165921b01ebe079d0dc9013dd97054e8eeac42a0ab9780481f221ca721f3' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='359451ce1ca32684e54c78ab7288de105360db23e1317e7ba718d9d7b59ca930',
 'three_mines_completion49_PASS_actual0_bound':valid(before,31,49,'32e76bbf006df276ba5e01958ec653ee491e89182343d268a20eecac89399338'),
 'two_contiguous_calendars_1plus29days_50PASS_actual0_each':bool(chain_valid) and sum(v['days'] for v in chain)==30,
 'native_idle22_driver_actual0_exact_single29day_step':driver['returncode']==0 and driver['helper_sha256']==h.sha256(run/'priority_terravore_idle_war_driver_v19.py')=='200bf7d43e75f959e252db3ebe0045c7a3321d305c66e1a9ff0ad5db0d17c892' and batch['days']==29 and batch['last_stage']==after and len(batch['steps'])==1,
 'six_uncapped_resources_budget_residual_zero':all(abs(residual[k])<D('0.00005') for k in keys if k not in ['trade','influence']),
 'two_capped_incomes_exact_discarded':all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap and delta[k]==0 and residual[k]==-net[k] for k,cap in [('trade',50000),('influence',1000)]) and net['trade']==D('84.92302') and net['influence']==7,
 'last_month_matches_original_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'mining3000_full_exact222point75_income13point5_upkeep':all(a['pop_jobs']['29'][k]==v for k,v in {'workforce':3000,'max_workforce':3000,'bonus_workforce':750,'workforce_limit':3000,'automated_workforce':0,'automated_workforce_limit':2999}.items()) and cur['income']['planet_miners']=={'minerals':222.75} and cur['expenses']['planet_districts_mining']=={'energy':13.5},
 'same_mother_districts_hive5_generator6_mining15':all(b['districts'][str(i)]==a['districts'][str(i)] for i in [1,2,3]) and {a['districts'][str(i)]['type']:a['districts'][str(i)]['level'] for i in [1,2,3]}=={'district_hive':5,'district_generator':6,'district_mining':15},
 'housing13800_positive_amenities_stability80_crime0':all(a['colonies']['0'][k]==v for k,v in {'total_housing':13800,'stability':80,'crime':0}.items()) and a['colonies']['0']['free_housing']>0 and a['colonies']['0']['free_amenities']>0,
 'native_migration16_growth6_exact_no_EEP_population_reward':growth==[{'month_start_size':10806,'growth':-10},{'month_start_size':135,'growth':16}] and detail==[[('key','GROWTH_CAT_EMIGRATION',False),('value',16,False),('key','GROWTH_CAT_GROWTH',False),('value',6,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)],[('key','GROWTH_CAT_IMMIGRATION',False),('value',16,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)]] and sum(a['colonies'][str(i)]['actual_pop_sum']-b['colonies'][str(i)]['actual_pop_sum'] for i in ac['owned_colonies'])==6,
 'EEP_ledger_flags_C37_D11_and_menace105_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and ac['variables']['eep_c']==37 and ac['variables']['eep_d']==11 and bc['effective_stockpile']['menace']==ac['effective_stockpile']['menace']==105,
 'actual_situation2_to3_with_Q12_T29_and_clear0_to30':b['situations']['100663299']['progress']==2 and a['situations']['100663299']['progress']==3 and b['planets']['1085']['variables']==a['planets']['1085']['variables'] and a['planets']['1085']['variables']['eep_months']==29 and load(before+'-war1-battle-v31-proof.json')['actual_clear_progress']==0 and load(after+'-war1-battle-v32-proof.json')['actual_clear_progress']==30,
 'positive_stocks_record_negative_energy_alloys_net':all(ac['effective_stockpile'][k]>0 for k in ['energy','minerals','alloys','unity']) and net['energy']==D('-12.86972') and net['alloys']==D('-3.11069') and net['minerals']==D('52.78863') and net['unity']>0,
 'exact2814_error_baseline_through_full_cycle':all((run/(st+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes() for st in [before,*[v['stage'] for v in chain]]) and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
proof={'status':'PASS_TERRAVORE_THREE_PAID_MINES_ONE_BUDGET_CYCLE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'observed_native_days':30,'chain':chain,'native_budget_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'residuals':{k:str(v) for k,v in residual.items()},'scope':'One real budget cycle with all three paid mines, full jobs and housing; native migration and caps reconciled. E/A monthly nets remain negative, operating repair pending; not full route or industry conversion acceptance.'}
out=run/'terravore-three-mines-budget-cycle-proof.json';assert not out.exists();h.write_json(out,proof);print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original budget differences retained'
