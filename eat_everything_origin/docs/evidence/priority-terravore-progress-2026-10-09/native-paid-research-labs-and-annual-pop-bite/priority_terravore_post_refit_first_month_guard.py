"""Exact first resource month: native processing, migration and seven docked refits."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-mineral-refit-day-22801114';after='terravore-post-refit-month-22801201'
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
ob=load(after+'-construction-boundary-observation-v4.json');ox=load(after+'-boundary-observation-v4-execution.json');cx=load(after+'-calendar-execution.json');pre=load('terravore-post-refit-first-month-baseline-proof.json');px=load('terravore-post-refit-first-month-baseline-execution.json')
extras={'minerals':D(36),'food':D(36)};net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in ['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']}
expected={k:D(str(bc['effective_stockpile'].get(k,0)))+v+extras.get(k,D(0)) for k,v in net.items()}
expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade'])
residual={k:D(str(ac['effective_stockpile'].get(k,0)))-v for k,v in expected.items()}
def details(col):
 raw=q.block(q.block(q.block(a['roots']['colony'],col),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(raw));return {q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
gd={i:details(i) for i in ['0','30']};old_armies=q.ids(q.block(b['country'],'owned_armies'));new_armies=q.ids(q.block(a['country'],'owned_armies'))
zones={str(i) for col in bc['owned_colonies'] for d in ba['colonies'][str(col)]['districts'] for i in ba['districts'][str(d)]['zones'] if i!=4294967295}
buildings={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
source_paths=['events/utopia_on_action_events.txt','events/on_action_events_1.txt','common/on_actions/00_on_actions.txt','common/buildings/00_capital_buildings.txt']
sources=load('terravore-post-refit-native-sources.json')['sources']
for rel in source_paths:
 src=h.GAME_EXE.parent/rel;dest=run/('terravore-post-refit-native-source-'+src.name);raw=src.read_bytes()
 if dest.exists():assert dest.read_bytes()==raw
 else:dest.write_bytes(raw)
 sources.append({'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)})
mineral_ids={16777746,50333149,50333147,33554923,1960,1961,1962};ex=ac['budget_categories']['current_month']['expenses']
projects=lambda s:{q.scalars(v)['id']:v for k,v,obj in q.fields(q.block(s['country'],'events')) if obj and k=='special_project'}
bp,ap=projects(b),projects(a)
delays=lambda s:[v for k,v,obj in q.fields(q.block(q.block(s['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
bd,ad=delays(b),delays(a)
checks={
 'baseline8_and_observer6_PASS_actual0_sources':len(pre['checks'])==8 and len(ob['checks'])==6 and all(v is True for obj in [pre,ob] for v in obj['checks'].values()) and px['returncode']==ox['returncode']==cx['returncode']==0 and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in [px,ox,cx]),
 'original_SAVs_exact17days_and_first_month':pre['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav'))=='497933e37b34d40ce5d44dee1e9bb839dcb3cec4d59165b9e29d1701d4eb81a0' and ba['date']=='2280.11.14' and aa['date']=='2280.12.01' and load(after+'-calendar-receipt.json')['days']==17,
 'all_eight_cash_ledgers_native_processing36_and_caps_exact':all(abs(v)<D('.00005') for v in residual.values()) and ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'native_research_purge3_and_all_queues_projects_held':ac['research_stockpile']==dict(bc['research_stockpile'],society_research=bc['research_stockpile']['society_research']+3) and omit(ac['tech_status'],{'stored_techpoints'})==omit(bc['tech_status'],{'stored_techpoints'}),
 'special_projects_same_shape_only_native_timer17days':bp.keys()==ap.keys() and all(omit(v,{'days_left'})==omit(ap[i],{'days_left'}) and ('days_left' not in q.scalars(v) or q.scalars(ap[i])['days_left']==q.scalars(v)['days_left']-17) for i,v in bp.items()),
 'original_one_storm_delay17days_next30days_safe':len(bd)==len(ad)==1 and omit(bd[0],{'days'})==omit(ad[0],{'days'}) and q.scalars(ad[0])['days']==q.scalars(bd[0])['days']-17>30 and q.scalars(ad[0])['event']=='cstorms.1815' and q.scalars(a['fleets']['33555278'])['return_date']=='2281.06.27',
 'species_aggregate_and_no_foreign_mother_exact':ob['before_state']['species_population_by_colony']=={'0:73':11975,'30:73':100,'30:61':27,'30:2':366} and ob['after_state']['species_population_by_colony']=={'0:73':11966,'30:73':116,'30:2':66},
 'native_growth7_migration15_decline327_original_month_records':gd['0']=={'GROWTH_CAT_EMIGRATION':15,'GROWTH_CAT_GROWTH':6,'GROWTH_CAT_OTHER':-100,'GROWTH_CAT_PROMOTION':0} and gd['30']=={'GROWTH_CAT_DECLINE':-327,'GROWTH_CAT_GROWTH':1,'GROWTH_CAT_IMMIGRATION':15,'GROWTH_CAT_OTHER':100,'GROWTH_CAT_PROMOTION':0} and aa['colonies']['0']['actual_pop_sum']+aa['colonies']['30']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+ba['colonies']['30']['actual_pop_sum']+7-327,
 'native_purge_Menace45_EEP_no_rewards_all_flags_held':ac['effective_stockpile']['menace']==bc['effective_stockpile']['menace']+45==2180 and all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis','owned_colonies']),
 'original61ships34fleets_same_birth_design_name_no_revival':len(b['ships'])==len(a['ships'])==61 and set(b['ships'])==set(a['ships']) and set(b['fleets'])==set(a['fleets']) and all(q.scalars(v)['construction_date']==q.scalars(a['ships'][i])['construction_date'] and q.block(v,'ship_design_implementation')==q.block(a['ships'][i],'ship_design_implementation') and q.block(v,'name')==q.block(a['ships'][i],'name') for i,v in b['ships'].items()),
 'original_ship_life_not_lowered_caps_held':all(0<q.scalars(v).get('hitpoints',0)<=q.scalars(a['ships'][i]).get('hitpoints',0) and all(q.scalars(v).get(k)==q.scalars(a['ships'][i]).get(k) for k in ['max_hitpoints','max_armor_hitpoints','max_shield_hitpoints']) for i,v in b['ships'].items()),
 'seven_original_new_minerals_docked0_full_no_order':set(q.ids(q.block(a['fleets']['50332250'],'ships')))==mineral_ids and not q.block(a['fleets']['50332250'],'current_order') and q.scalars(q.block(q.block(q.block(a['fleets']['50332250'],'movement_manager'),'orbit'),'orbitable'))=={'starbase':0} and all(q.scalars(q.block(a['ships'][str(i)],'ship_design_implementation'))=={'design':218105405,'upgrade':4294967295,'growth_stage':0} for i in mineral_ids),
 'docked_ship_fees_exact_components_and_no_extra_alloys':{k:ex['ships'][k] for k in ['energy','minerals','alloys']}=={'energy':29.65054,'minerals':5.33008,'alloys':10.66023} and ex['ship_components']==bc['budget_categories']['current_month']['expenses']['ship_components']=={'energy':19.38267,'alloys':3.29466},
 'original15_armies_held_only_source_native_defense237_added':set(new_armies)-set(old_armies)=={237} and set(old_armies)<=set(new_armies) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in old_armies) and q.scalars(q.block(a['roots']['army'],'237'))=={'type':'defense_army','health':250,'max_health':250,'jump_drive_cooldown':'0.01.01','owner':0,'species':73,'colony':30,'spawning_colony':30,'morale':250} and q.scalars(q.block(a['roots']['buildings'],'16777355'))['type']=='building_hive_capital',
 'paid800M_zone39p2_and_all_owned_assets_held':q.ids(q.block(a['queues']['0'],'items'))==[1627389955] and q.scalars(a['items']['1627389955'])['progress']==39.2 and omit(a['items']['1627389955'],{'progress'})==omit(b['items']['1627389955'],{'progress'}) and not q.ids(q.block(a['queues']['1'],'items')) and not q.ids(q.block(a['queues']['3'],'items')) and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in buildings),
 'mother35_paid27_districts_science_jobs_positive':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for col in bc['owned_colonies'] for i in ba['colonies'][str(col)]['districts']) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27 and all(aa['pop_jobs'].get(i)==v for i,v in ba['pop_jobs'].items() if v['planet']==0 and v['type'] in ['calculator_physicist','calculator_biologist','calculator_engineer']) and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'source14_34months_situation1_only_no_bite_or_settlement':all(ba['planets']['1578'][k]==aa['planets']['1578'][k] for k in ['owner','controller','planet_size','variables','deposits']) and set(aa['situations'])=={'167772163'} and aa['situations']['167772163']==dict(ba['situations']['167772163'],progress=1,last_month_progress=1),
 'no_new_messages_pending_war_battles_or_combat':not ob['new_country0_messages_raw'] and not a['pending'] and q.block(b['roots']['war'],'1')==q.block(a['roots']['war'],'1') and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'all_original_native_sources_exact_live_and_preserved':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
 'production41_CN_error_module_held':m['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850' and pre['state_module_sha256']==h.sha256(run/'priority_terravore_native_state.py')==h.sha256(Path(__file__).with_name('priority_terravore_native_state.py')),
}
passed=all(v is True for v in checks.values());out=run/(after+'-post-refit-first-month-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_POST_REFIT_FIRST_RESOURCE_MONTH_NATIVE_PURGE_RECONCILED' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'cash_residual':{k:str(v) for k,v in residual.items()},'growth_details':gd,'sources':sources,'state_module_sha256':h.sha256(run/'priority_terravore_native_state.py'),'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':30 if passed else 0,'scope':'First17days resource month reconciled. Allows only next native30days, requires independent full maintenance month checks afterward; no complete maintenance month or full route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'cash_residual':{k:str(v) for k,v in residual.items()}}),flush=True);assert passed
