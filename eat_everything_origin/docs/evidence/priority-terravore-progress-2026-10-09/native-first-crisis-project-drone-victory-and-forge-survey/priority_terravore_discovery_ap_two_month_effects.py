"""Read-only actual month after two paid Discovery nodes and first earned AP."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before='terravore-one-vision-earned';after='terravore-discovery-ap-month2'
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
mid=json.loads((run/'terravore-discovery-ap-month.audit.json').read_text('utf-8'));mc=mid['countries']['0'];first=json.loads((run/'terravore-discovery-ap-month-native-effects-proof.json').read_text('utf-8'));first_receipt=json.loads((run/'terravore-discovery-ap-month-calendar-receipt.json').read_text('utf-8'));wait=json.loads((run/(after+'-paid-wait-v2-proof.json')).read_text('utf-8'));receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
with zipfile.ZipFile(run/(after+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
roots={k:v for k,v,o in q.fields(t) if o};growth=q.scalars(q.block(q.block(q.block(roots['colony'],'0'),'last_month_growth_data'),'growth_and_size'))
resources=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
def nets(c):return {k:sum((D(str(v.get(k,0))) for v in c['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
bn,an=nets(bc),nets(ac);residual={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(mc['effective_stockpile'].get(k,0)))-an[k] for k in resources}
research=['calculator_physicist','calculator_biologist','calculator_engineer']
def workers(v):return {j['type']:j for j in v['pop_jobs'].values() if j['planet']==0 and j['type'] in research}
bw,aw=workers(b),workers(a)
checks={'bound_all20_hold_checks_pass':wait['status']=='PASS_TERRAVORE_PAID_CONSTRUCTION_WAIT_COMPONENT' and all(wait['checks'].values()) and wait['before_sha256']==mid['save_sha256'] and wait['after_sha256']==a['save_sha256'],
 'original_first_month_unique_research_budget_lag_FAIL':first['status']=='FAIL' and [k for k,v in first['checks'].items() if not v]==['all_three_native_research_budget_income_increased'] and sum(first['checks'].values())==10,
 'original_SHA_pair':h.sha256(run/'terravore-discovery-ap-month.sav')==mid['save_sha256']==first['after_sha256'] and h.sha256(run/(before+'.sav'))==b['save_sha256']==first['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_full60_via_two30_receipts':first_receipt['status']==receipt['status']=='CALENDAR_CONFIRMED' and first_receipt['days']==receipt['days']==30 and first_receipt['start_date']==b['date']=='2212.08.02' and first_receipt['date']==mid['date']==receipt['start_date']=='2212.09.02' and receipt['date']==a['date']=='2212.10.02',
 'first_AP_one_vision_only':bc['ascension_perks']==ac['ascension_perks']==['ap_one_vision'],
 'completed_Discovery_tree_held':bc['traditions']==ac['traditions'] and set(ac['traditions'])=={'tr_discovery_adopt','tr_discovery_to_boldly_go','tr_discovery_databank_uplinks','tr_discovery_science_division','tr_discovery_polytechnic_education','tr_discovery_faith_in_science','tr_discovery_finish'},
 'actual_native_growth_only':first['actual_native_growth']['month_start_size']==b['colonies']['0']['actual_pop_sum'] and mid['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+first['actual_native_growth']['growth'] and growth['month_start_size']==mid['colonies']['0']['actual_pop_sum'] and a['colonies']['0']['actual_pop_sum']==mid['colonies']['0']['actual_pop_sum']+growth['growth'],
 'all_eight_actual_current_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'all_three_native_research_caps_increased_and_staffed':all(aw[k]['max_workforce']>bw[k]['max_workforce'] and aw[k]['workforce']==aw[k]['max_workforce'] for k in research),
 'all_three_native_research_budget_income_increased':all(D(str(ac['budget_categories']['current_month']['income'][cat][res]))>D(str(bc['budget_categories']['current_month']['income'][cat][res])) for cat,res in [('planet_physicists','physics_research'),('planet_biologists','society_research'),('planet_engineers','engineering_research')]),
 'scientist_upkeep_native12_to10point2':bc['budget_categories']['current_month']['expenses']['leader_scientists']['unity']==12 and ac['budget_categories']['current_month']['expenses']['leader_scientists']['unity']==10.2,
 'actual_unity_net_increased_energy_minerals_positive':an['unity']>bn['unity'] and an['energy']>0 and an['minerals']>0}
p={'status':'PASS_TERRAVORE_DISCOVERY_FIRST_AP_TWO_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_research_workers_before_after':[bw,aw],'actual_native_growth_first_second':[first['actual_native_growth'],growth],'actual_budget_residuals':{k:str(v) for k,v in residual.items()},'actual_current_month_net_before_after':[{k:str(v) for k,v in n.items()} for n in [bn,an]],'actual_stockpile':ac['effective_stockpile'],'actual_completed_technology_additions':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),'scope':'Two native months, with last30-day budget residuals only, after normally paid Discovery completion and normally earned One Vision. No second AP, Shroud, crisis or long-term acceptance claim.'}
out=run/(after+'-native-effects-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native effect FAIL retained; inspect triggers before further calendar'
