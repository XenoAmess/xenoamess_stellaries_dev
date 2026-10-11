"""One actual30-day post-conversion native budget ledger, no game actions."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
load=lambda n:json.loads((run/n).read_text('utf-8'))
before='terravore-heavy-first-new-month';after='terravore-heavy-full-budget-month'
b,a=[load(st+'.audit.json') for st in [before,after]];bc,ac=[x['countries']['0'] for x in [b,a]]
cur=ac['budget_categories']['current_month'];keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
net={k:sum((D(str(v.get(k,0))) for v in cur['balance'].values()),D(0)) for k in keys}
delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in keys}
residual={k:delta[k]-net[k] for k in keys}
def valid(st):
 p=load(st+'-war1-battle-v49-proof.json');e=load(st+'-battle-v49-execution.json')
 return p['status'].startswith('PASS_') and len(p['checks'])==77 and all(v is True for v in p['checks'].values()) and e['returncode']==0 and e['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v49.py')=='e2c6ef5c01e1550c90bf843c5bbe61195e8281355031a125303818d48f480ca8' and p['after_sha256']==h.sha256(run/(st+'.sav'))
with zipfile.ZipFile(run/(after+'.sav')) as z:top={k:v for k,v,o in q.fields(z.read('gamestate').decode('utf-8-sig')) if o}
growth_raw=[q.block(q.block(top['colony'],str(i)),'last_month_growth_data') for i in [0,37]]
growth=[q.scalars(q.block(raw,'growth_and_size')) for raw in growth_raw]
details=[[(k,q.unquote(v),o) for k,v,o in q.fields(q.block(raw,'current_month_growth_details'))] for raw in growth_raw]
pre,post=[load(st+'-war1-battle-v49-proof.json') for st in [before,after]]
cal=load(after+'-calendar-receipt.json');ex=load(after+'-calendar-execution.json')
checks={
 'production02_simp_chinese_exact_tree':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'exact_30day_SHA_pair':b['date']=='2271.06.01' and a['date']=='2271.07.01' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='6f5642e55fd35ea04fd08fe6dca2e1d06d245357b2307664ec02c74c26793e54' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='cbe2bed75f87370687b7ca46da759a400b0fba8dbaa86395e44c057243657d3a',
 'both_endpoints77_PASS_actual0_source_bound':valid(before) and valid(after),
 'one_unique_native_calendar30_actual0':cal['days']==post['days']==30 and cal['start_date']==b['date'] and cal['date']==a['date'] and post['before_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
 'six_uncapped_resource_ledger_residuals_zero':all(abs(residual[k])<D('0.00005') for k in keys if k not in ['influence','trade']),
 'actual_positive_E_M_A_U_nets_not_old_cached_budget':all(net[k]>0 for k in ['energy','minerals','alloys','unity']) and net['energy']==D('18.42840') and net['minerals']==D('43.43325') and net['alloys']==D('24.26431') and net['unity']==D('94.39504'),
 'two_capped_resources_income_discarded_exactly':all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap and delta[k]==0 and residual[k]==-net[k] for k,cap in [('influence',1000),('trade',50000)]) and net['influence']==D('7.1') and net['trade']==D('93.02406'),
 'last_month_equals_original_current':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'full700_fabricator900_coordinator3000_miner1200_technician':all(len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind and j['workforce']==j['max_workforce']==n])==1 for kind,n in [('fabricator',700),('coordinator',900),('mining_drone',3000),('technician_drone',1200)]),
 'original_hive5_generator6_mining15_and_foundry_zone104':all(b['districts'][str(i)]==a['districts'][str(i)] for i in [1,2,3]) and {a['districts'][str(i)]['type']:a['districts'][str(i)]['level'] for i in [1,2,3]}=={'district_hive':5,'district_generator':6,'district_mining':15} and q.scalars(q.block(top['zones'],'104'))=={'type':'zone_foundry'} and q.ids(q.block(q.block(top['districts'],'1'),'zones'))==[0,2,104],
 'housing13800_stability80_crime0_amenities_positive':all(a['colonies']['0'][k]==v for k,v in {'total_housing':13800,'stability':80,'crime':0}.items()) and a['colonies']['0']['free_housing']>0 and a['colonies']['0']['free_amenities']>0,
 'actual_native_growth7_no_generic_EEP_population_reward':growth==[{'month_start_size':10750,'growth':7},{'month_start_size':284,'growth':0}] and details==[[('key','GROWTH_CAT_GROWTH',False),('value',7,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)],[]] and a['colonies']['0']['actual_pop_sum']-b['colonies']['0']['actual_pop_sum']==7 and a['colonies']['37']['actual_pop_sum']==b['colonies']['37']['actual_pop_sum']==284,
 'EEP_C37_D11_worlds2_Menace105_and_true_research_held_or_grown':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_d':11,'eep_worlds':2,'eep_g':0,'eep_made':0,'eep_psi':1}.items()) and bc['effective_stockpile']['menace']==ac['effective_stockpile']['menace']==105 and all(D(str(ac['research_stockpile'].get(k,0)))>=D(str(bc['research_stockpile'].get(k,0))) for k in q.RESEARCH_RESOURCES),
 'paid_rear_work29_to59_colony_still_parked_and_no_new_combat':D(pre['actual_rear_shipyard_progress'])==29 and D(post['actual_rear_shipyard_progress'])==59 and post['colony523_order_recovery_pending'] is True and post['short_idle_war_calendar_ready'] is False and not post['actual_pending'] and not post['actual_active_owned_combat'] and len(post['actual_alive_military_ship_ids'])==27,
 'full_unfiltered_error_exact2814_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed=all(v is True for v in checks.values())
proof={'status':'PASS_TERRAVORE_HEAVY_POSTCONVERSION_ONE_BUDGET_CYCLE_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'observed_native_days':30,'native_budget_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'residuals':{k:str(v) for k,v in residual.items()},'scope':'One real positive postconversion economy cycle under original27-corvette maintenance; no proof for future reinforcements, colony route restoration, mineral ships or full route.'}
out=run/'terravore-heavy-budget-cycle-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed,'Preserve original budget result; do not repeat calendar'
