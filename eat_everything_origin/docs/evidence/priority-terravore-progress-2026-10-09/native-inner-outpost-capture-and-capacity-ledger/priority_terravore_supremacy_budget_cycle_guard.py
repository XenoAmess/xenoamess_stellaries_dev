"""Actual original 30-day post-Supremacy ledger; no game actions."""
import json, logging, sys
from decimal import Decimal as D
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
def load(name):return json.loads((run/name).read_text('utf-8'))
before='terravore-dual-build2-step1';after='terravore-dual-build2-step2'
b,a=[load(s+'.audit.json') for s in [before,after]]
bc,ac=[x['countries']['0'] for x in [b,a]]
pre=load(before+'-war1-battle-v53-proof.json');post=load(after+'-war1-battle-v54-proof.json')
be=load(before+'-battle-v53-execution.json');ae=load(after+'-battle-v54-execution.json')
cal=load(after+'-calendar-receipt.json');ce=load(after+'-calendar-execution.json')
paid_stage='terravore-supremacy-adopt-paid'
paid=load(paid_stage+'-supremacy-payment-proof.json');pe=load(paid_stage+'-guard-execution.json')
paid_audit=load(paid_stage+'.audit.json')['countries']['0']
keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in keys}
delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in keys}
residual={k:delta[k]-net[k] for k in keys}
costs={'ships':{'energy':-26.18679,'trade':-4.5,'alloys':-11.59326},'ship_components':{'energy':-20.73857,'alloys':-3.52326},'starbases':{'energy':-6},'starbase_buildings':{'energy':-0.8},'starbase_modules':{'energy':-1.6}}
old_costs={'ships':{'energy':-32.49003,'trade':-4.5,'alloys':-14.74497},'ship_components':{'energy':-25.50732,'alloys':-4.31572},'starbases':{'energy':-7},'starbase_buildings':{'energy':-0.8},'starbase_modules':{'energy':-1.6}}
checks={
 'production02_simp_chinese_original_tree':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'original_SHA_pair_exact_30days':b['date']=='2271.09.12' and a['date']=='2271.10.12' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='6e4245e8c62deb1af97583c54562664c819d8c601b9c61d293f2568762bb4dfa' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='8885a9a8ffde0f65d70d2b258ab06122ade6101663afdfd4a64b737d16414473',
 'original85_and87_PASS_actual0_source_bound':all(p['status'].startswith('PASS_') and len(p['checks'])==n and all(v is True for v in p['checks'].values()) and p['after_sha256']==au['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/source)==sha for p,n,au,ex,source,sha in [(pre,85,b,be,'priority_terravore_war1_battle_observer_v53.py','4d1bfd03965c3dbd25e9d46469c0ba81cc29cadbf823d44a4104eb2a2579341f'),(post,87,a,ae,'priority_terravore_war1_battle_observer_v54.py','0dea27f03242d11f8836bc64ce2e385eeb859b4f2521ddf226ca4dc79fb36eef')]),
 'actual_unique_calendar30_zero':cal['days']==post['days']==30 and cal['start_date']==b['date'] and cal['date']==a['date'] and post['before_sha256']==b['save_sha256'] and ce['returncode']==0 and ce['helper_sha256']=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc',
 'original_paid_supremacy19_PASS_actual0_bound':paid['status'].startswith('PASS_') and len(paid['checks'])==19 and all(v is True for v in paid['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_supremacy_adopt_payment_guard.py')=='050cbcc600863e6de74558f9374e40283806458d4158cca10ba520237f7e5142' and paid['after_sha256']==h.sha256(run/(paid_stage+'.sav'))=='ff8dfe7781f94b767cd9eda9ab49e2abe16a3e6b6d30c42dfb40725492aec015',
 'six_uncapped_actual_ledger_residuals_zero':all(abs(residual[k])<D('0.00005') for k in keys if k not in ['trade','influence']),
 'two_capped_incomes_discarded_exactly':all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap and delta[k]==0 and residual[k]==-net[k] for k,cap in [('trade',50000),('influence',1000)]),
 'actual_positive_nets_exact_native_values':all(net[k]>0 for k in ['energy','minerals','alloys','unity']) and {k:str(net[k]) for k in ['energy','minerals','alloys','unity']}=={'energy':'30.41085','minerals':'41.94451','alloys':'28.20848','unity':'96.51796'},
 'native_last_month_rolls_original_current':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'post_adoption_ship_and_station_costs_same_in_both_native_months':all(c['budget_categories']['current_month']['balance'][k]==v for c in [bc,ac] for k,v in costs.items()),
 'original_before_adoption_costs_preserved_separate_from_capacity_effect':all(paid_audit['budget_categories']['current_month']['balance'][k]==v for k,v in old_costs.items()),
 'same27_military_ledger_and_naval135_no_new_or_lost':pre['actual_alive_military_ship_ids']==post['actual_alive_military_ship_ids'] and len(post['actual_alive_military_ship_ids'])==27 and pre['actual_owned_military']==post['actual_owned_military'] and pre['actual_naval_cache']==post['actual_naval_cache']=='135' and not post['actual_new_paid_ships'] and not post['actual_lost_military_requires_separate_combat_evidence'] and pre['cumulative_paid_lost']==post['cumulative_paid_lost'] and pre['cumulative_original_lost']==post['cumulative_original_lost'],
 'core_C37_D11_worlds2_PSI1_menace105_no_early_settlement':all(bc['variables'][k]==ac['variables'][k]==v for k,v in {'eep_c':37,'eep_d':11,'eep_worlds':2,'eep_g':0,'eep_made':0,'eep_psi':1}.items()) and bc['effective_stockpile']['menace']==ac['effective_stockpile']['menace']==105,
 'supremacy_adopt_held_no_unbought_logistical_corps':all('tr_supremacy_adopt' in c['traditions'] and 'tr_supremacy_fleet_logistical_corps_hive' not in c['traditions'] and 'tr_supremacy_fleet_logistical_corps' not in c['traditions'] for c in [bc,ac]),
 'all_unfiltered_errors_original2814_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
proof={'status':'PASS_TERRAVORE_POST_SUPREMACY_ACTUAL_BUDGET_CYCLE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_days':30,'actual_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'residuals':{k:str(v) for k,v in residual.items()},'native_costs_before':old_costs,'native_costs_after':costs,'scope':'Actual original27 fleet maintenance and30-day ledger after capacity adoption; not future6 ships, restored route, mineral ships or full acceptance.'}
out=run/'terravore-supremacy-budget-cycle-proof.json';assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v]}),flush=True)
assert all(checks.values()),'Original budget check FAIL retained'
