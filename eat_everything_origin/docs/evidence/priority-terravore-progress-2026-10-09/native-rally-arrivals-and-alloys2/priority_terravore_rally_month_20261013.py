"""Four documented native rally/operating months; stop before technology boundary."""
import json,logging,sys
from decimal import Decimal as D
from itertools import groupby
from pathlib import Path
mode,before,other,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def day(s):
 y,mo,d=map(int,s.split('.'));return y*360+(mo-1)*30+d-1
def checked(stage):
 x=load(stage+'-execution.json');return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
def rq(c,k):
 raw=c['research_queues'][k];ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]])
def flags(s):
 return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
b=read_state(run,before);ba=b['audit'];bc=ba['countries']['0'];p=load(prior);eps=D('.00003')
income=lambda c:{k:sum((D(str(v.get(k,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bi=income(bc);bp=rq(bc,'society_queue');be=rq(bc,'engineering_queue');ids=q.ids(q.block(b['queues']['0'],'items'));head=D(str(q.scalars(b['items']['251658284'])['progress']))
basic=p['status'].startswith('PASS') and bool(p['checks']) and all(v is True for v in p['checks'].values()) and checked(execution) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav'))
package=m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
if mode=='review':
 checks={
  'prior_PASS_actual0_source_originalSAV':basic,
  'exact30days_month1_June1_through_October1_only':ba['date'].endswith('.01') and other.endswith('.01') and day(other)-day(ba['date'])==30 and day('2285.06.01')<=day(ba['date'])<day(other)<=day('2285.10.01'),
  'no_pending_or_technology_hive_project_completion':not b['pending'] and ids==[251658284,1191182345,117440553,1476395019,117440546] and head+42<480 and D(str(be['progress']))+bi['engineering_research']*D('1.35')<2600 and D(str(bp['progress']))+bi['society_research']*D('2.35')<12000 and not q.ids(q.block(b['queues'].get('3',''),'items')),
  'CN41_unfiltered_live_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 }
 passed=all(v is True for v in checks.values());out=run/(before+'-rally-month-review.json');assert not out.exists()
 h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':ba['save_sha256'],'start_date':ba['date'],'end_date':other,'days':30,'maximum_days':30,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-rally-month-review'})
 print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed;sys.exit(0)
assert mode=='guard';after=other;a=read_state(run,after);aa=a['audit'];ac=aa['countries']['0'];ap=rq(ac,'society_queue');ae=rq(ac,'engineering_queue');ai=income(ac)
ob=load(after+'-construction-boundary-observation-v4.json');cal=load(after+'-calendar-receipt.json');review=load(before+'-rally-month-review.json')
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade'];net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources};expected={k:D(str(bc['effective_stockpile'].get(k,0)))+v for k,v in net.items()};expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade']);residual={k:D(str(ac['effective_stockpile'].get(k,0)))-v for k,v in expected.items()}
draw=min(bi['society_research'],D(str(bc['research_stockpile']['society_research'])));ef={k:dict(v,flag_days=v['flag_days']-30) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>30}
raw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(raw));growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
routespec={'83886903':(30,[188,139,171,70,30]),'50332250':(188,[0,103,151,188]),'917':(188,[0,103,151,188])};routes={};route_ok=True
for fid,(target,full) in routespec.items():
 am=q.block(a['fleets'][fid],'movement_manager');bm=q.block(b['fleets'][fid],'movement_manager');path=q.block(am,'path');nodes=[q.scalars(q.block(v,'coordinate'))['origin'] for k,v,obj in q.fields(path) if obj and k=='node'];remain=[i for i,_ in groupby(nodes)];current=q.scalars(q.block(am,'coordinate'))['origin'];previous=q.scalars(q.block(bm,'coordinate'))['origin'];order=q.block(q.block(a['fleets'][fid],'current_order'),'orbit_planet_order');routes[fid]={'current':current,'remaining':remain,'eta':q.scalars(path).get('date'),'target':q.scalars(q.block(am,'target_coordinate'))}
 route_ok=route_ok and current in full and previous in full and full.index(current)>=full.index(previous) and remain in [full[n:] for n in range(len(full))] and full.index(current)<=full.index(remain[0])<=full.index(current)+1 and q.scalars(q.block(am,'target_coordinate'))['origin']==target and q.scalars(order).get('can_reach')=='yes' and q.block(order,'orbitable')==q.block(q.block(q.block(b['fleets'][fid],'current_order'),'orbit_planet_order'),'orbitable') and q.scalars(path)['date']<'2286.03.30' and q.scalars(a['fleets'][fid])['order_id']==q.scalars(b['fleets'][fid])['order_id']
zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295};builds={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295};army=q.ids(q.block(b['country'],'owned_armies'));news=ob['new_country0_messages_raw'];ex=ac['budget_categories']['current_month']['expenses']
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
checks={
 'prior_review_calendar_observer_actual0_originalSAV':basic and len(ob['checks'])==7 and all(v is True for pp in [ob,review] for v in pp['checks'].values()) and all(checked(s) for s in [after+'-boundary-observation-v4',after+'-calendar',before+'-rally-month-review']) and ob['before_sha256']==ba['save_sha256'] and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'single30day_native_month1_before_October_tech_boundary':cal['days']==30 and cal['start_date']==ba['date'] and cal['date']==aa['date'] and day(aa['date'])-day(ba['date'])==30 and aa['date'].endswith('.01') and day(aa['date'])<=day('2285.10.01'),
 'cash8_exact_new_native_budget_caps_no_payments':all(abs(v)<eps for v in residual.values()) and all(ac['effective_stockpile'].get(k,0)>=0 for k in resources),
 'project3_one_tick_and_true_bank_exact':bi==ai and bi=={'physics_research':D('32.6914'),'society_research':D('68.1742'),'engineering_research':D('76.4242')} and bp['special_project']==ap['special_project']==9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-bi['society_research']*D('1.35')-draw)<eps and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+draw)<eps and ap['progress']<12000,
 'engineering_one_tick_and_idle_physics_bank_exact':be['technology']==ae['technology']=='tech_alloys_2' and abs(D(str(ae['progress']))-D(str(be['progress']))-bi['engineering_research']*D('1.35'))<eps and abs(D(str(ac['research_stockpile']['physics_research']))-D(str(bc['research_stockpile']['physics_research']))-bi['physics_research']*D('1.35'))<eps and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0 and ae['progress']<2600,
 'all_other_technology_projects_held':dict(bp,progress=ap['progress'])==ap and dict(be,progress=ae['progress'])==ae and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'all77_original_ships_identity_design_birth_name_life_held':len(b['ships'])==len(a['ships'])==77 and set(b['ships'])==set(a['ships']) and all(all(q.scalars(v).get(k)==q.scalars(a['ships'][i]).get(k) for k in ['construction_date','hitpoints','max_hitpoints','armor_hitpoints','shield_hitpoints']) and q.block(v,'ship_design_implementation')==q.block(a['ships'][i],'ship_design_implementation') and q.block(v,'name')==q.block(a['ships'][i],'name') for i,v in b['ships'].items()),
 'all35_original_fleets_same_members':len(b['fleets'])==len(a['fleets'])==35 and set(b['fleets'])==set(a['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()),
 'three_legal_native_rally_routes_can_reach_target_before_border_expiry':route_ok,
 'no_new_ships_shiporders_naval261':not q.ids(q.block(a['queues'].get('3',''),'items')) and q.scalars(a['country'])['used_naval_capacity']==q.scalars(a['country'])['fleet_size']==261,
 'EEP_government_AP_traditions_crisis_menace_no_rewards':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==2930,
 'mother_only_species73_natural_growth_OTHER0':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+growth.get('GROWTH_CAT_GROWTH',0) and set(growth)<={'GROWTH_CAT_GROWTH','GROWTH_CAT_OTHER','GROWTH_CAT_PROMOTION'} and 0<=growth.get('GROWTH_CAT_GROWTH',0)<=10 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'mother39_paid28_original_zones_labs_research_jobs_held':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==28 and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in builds) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']),
 'five_paid400_hives_only_head_plus42_no_completion':q.ids(q.block(a['queues']['0'],'items'))==ids and omit(b['items']['251658284'],{'progress'})==omit(a['items']['251658284'],{'progress'}) and abs(D(str(q.scalars(a['items']['251658284'])['progress']))-head-42)<eps and q.scalars(a['items']['251658284'])['progress']<480 and all(a['items'][str(i)]==b['items'][str(i)] for i in ids[1:]),
 'all15_original_armies_raw_held':len(army)==15 and army==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in army),
 'native_country_flags_only_normal_timers_expire':flags(a)==ef,
 'native_player_contacts63_64_65_held':all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'only_reviewed_lowtrade_pirate6_delay':len(delays)<=1 and all(v['event']=='pirate.6' and 1<=v['days']<=30 for v in delays) and sum(D(str(v.get('trade',0))) for v in ac['budget_categories']['current_month']['income'].values())<300 and 'birth_of_piracy' not in ac['flags'],
 'no_pending_unknown_news_wars_truces_or_combat':not a['pending'] and all(q.scalars(v).get('type')=='SYSTEM_SURVEYED' and q.scalars(v).get('localization')=='MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED' for v in news) and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'all_other_owned_queues_held':all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0),
 'native23_mineral_hulls_away_M_upkeep_no_dock_discount':abs(D(str(ex['ships']['minerals']))-D('58.27653')/D('.75'))<D('.001'),
 'destroyed_source_no_active_EEP_no_return':aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0 and all(v.get('killed')=='yes' for v in aa['situations'].values()),
 'positive_housing_amenities_no_crime':aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'CN41_unfiltered_live_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-rally-month-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_RALLY_MONTH' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'routes':routes,'project3_progress':ap['progress'],'engineering_progress':ae['progress'],'hive_head_work':q.scalars(a['items']['251658284'])['progress'],'growth_details':growth,'cash_residual':{k:str(v) for k,v in residual.items()},'ships_upkeep':ex['ships'],'component_upkeep':ex['ship_components'],'new_messages_raw':news,'boundaries':['native_rally_next_month_or_tech_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One normal rally/operating month, not arrival/battle/full Terravore acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'project3':ap['progress'],'hive_work':q.scalars(a['items']['251658284'])['progress'],'routes':routes}),flush=True);assert passed
