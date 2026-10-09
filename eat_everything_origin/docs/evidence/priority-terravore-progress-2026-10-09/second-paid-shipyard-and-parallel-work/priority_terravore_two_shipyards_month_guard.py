"""Read-only first monthly economics after second paid shipyard, real fifth corvette."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,list(q.fields(t)),{k:v for k,v,o in q.fields(t) if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def queue(rt,i):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),str(i))
def items(rt):return {k:v for k,v,o in q.fields(q.block(q.block(rt['construction'],'item_mgr'),'items')) if o}
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-parallel-shipyards-proof.json')).read_text('utf-8'));receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
bids,aids=[q.ids(q.block(queue(rt,3),'items')) for rt in [br,ar]];bi,ai=items(br),items(ar)
bs,ass=[q.ids(q.block(q.block(rt['fleet'],'16777797'),'ships')) for rt in [br,ar]];new=[i for i in ass if i not in bs]
growthraw=q.block(q.block(ar['colony'],'0'),'last_month_growth_data');growth=q.scalars(q.block(growthraw,'growth_and_size'))
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']}
residual={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-v for k,v in net.items()}
residual['influence']=D(str(ac['effective_stockpile'].get('influence',0)))-min(D(1000),D(str(bc['effective_stockpile'].get('influence',0)))+net['influence'])
checks={
 'bound_actual_parallel30_PASS':pre['status']=='PASS_NATIVE_TWO_SHIPYARDS_ACTUALLY_WORKING_COMPONENT' and len(pre['checks'])==30 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/'terravore-defense-two-shipyards-working-guard-execution.json').read_text('utf-8'))['returncode']==0,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual11_native_days':b['date']=='2236.11.20' and a['date']=='2236.12.01' and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==11 and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'eight_month_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'complete_last_month_equals_prior_current':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'original_first_paid_order_only_completed':len(bids)==16 and bids[0]==671088646 and aids==bids[1:] and len(aids)==15,
 'remaining_front_progress15_other14_raw_held':aids[0]==335544337 and q.scalars(ai[str(aids[0])])['progress']==15 and omit(bi[str(aids[0])],['progress'])==omit(ai[str(aids[0])],['progress']) and all(bi[str(i)]==ai[str(i)] for i in aids[1:]),
 'original_four_held_one_new_ship':bs==[16777221,16778303,16778412,1564] and len(ass)==5 and len(new)==1 and ass==bs+new,
 'new_actual_corvette_original_design_date_hull':len(new)==1 and q.scalars(s:=q.block(ar['ships'],str(new[0])))['construction_date']=='2236.12.01' and q.scalars(s)['fleet']==16777797 and q.scalars(s)['hitpoints']==q.scalars(s)['max_hitpoints']==250 and q.scalars(q.block(s,'ship_design_implementation'))['design']==67110548,
 'original_four_real_design_hull_held':all(q.scalars(q.block(br['ships'],str(i)))==q.scalars(q.block(ar['ships'],str(i))) and q.block(q.block(br['ships'],str(i)),'ship_design_implementation')==q.block(q.block(ar['ships'],str(i)),'ship_design_implementation') for i in bs),
 'actual_naval_capacity25':q.scalars(q.block(ar['country'],'0'))['fleet_size']==25,
 'actual_starbase_raw_held':q.block(q.block(br['starbase_mgr'],'starbases'),'0')==q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),
 'actual_five_ship_maintenance7_75_energy1_875_alloys':bc['budget_categories']['current_month']['expenses']['ships']=={'energy':7,'alloys':1.5} and ac['budget_categories']['current_month']['expenses']['ships']=={'energy':7.75,'alloys':1.875},
 'solar_module_income6_removed_shipyard_upkeep1_to2':bc['budget_categories']['current_month']['income'].get('starbase_modules')=={'energy':6} and not ac['budget_categories']['current_month']['income'].get('starbase_modules') and bc['budget_categories']['current_month']['expenses']['starbase_modules']=={'energy':1} and ac['budget_categories']['current_month']['expenses']['starbase_modules']=={'energy':2},
 'actual_population_only_birth5':growth=={'month_start_size':8930,'growth':5} and a['colonies']['0']['actual_pop_sum']==8935 and list(q.fields(q.block(growthraw,'current_month_growth_details')))==[('key','"GROWTH_CAT_GROWTH"',False),('value','5',False),('key','"GROWTH_CAT_PROMOTION"',False),('value','0',False)],
 'mining2000_generator600_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',600)]),
 'actual_districts_and_deposits_held':b['districts']==a['districts'] and b['deposits']==a['deposits'],
 'EEP_ledger_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'unique_core_owned_capacity11_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and a['planets']['7']['owner']==a['planets']['7']['controller']==0 and a['planets']['7']['planet_size']==18 and b['planets']['7']['variables']==a['planets']['7']['variables'] and a['planets']['7']['variables']['eep_capacity_value']==11,
 'original_core_modifiers_held':b['planets']['7']['modifiers']==a['planets']['7']['modifiers'],
 'both_sources_still_unowned_shattered_zero_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned_no_new_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'Theory_selected_and_growing':all('tech_psionic_theory' not in c['completed_technologies'] and q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])['technology']=='tech_psionic_theory' for c in [bc,ac]) and q.scalars(q.block(ac['tech_status'],'society_queue').strip()[1:-1])['progress']>q.scalars(q.block(bc['tech_status'],'society_queue').strip()[1:-1])['progress'],
 'Theory650_former607_25288_and_true_bank_held':bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288} and q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints'),
 'positive_energy_mineral_unity_alloy_stocks_nets':all(ac['effective_stockpile'][k]>0 and net[k]>=0 for k in ['energy','minerals','unity','alloys']),
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['ascension_perks','traditions','government']:checks[k+'_held']=bc[k]==ac[k]
for k in ['species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TWO_SHIPYARDS_FIRST_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_new_ships':new,'actual_growth':growth,'actual_budget_residuals':{k:str(v) for k,v in residual.items()},'actual_month_nets':{k:str(v) for k,v in net.items()},'scope':'First native month after second paid shipyard. Real paid fifth corvette and module/ship maintenance. No defense victory or full-route claim.'}
out=run/(after+'-two-shipyards-month-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original monthly FAIL retained; no next calendar'
