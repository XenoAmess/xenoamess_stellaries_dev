"""Native postcombat regeneration, operating ledger and original orbit; bounded before border."""
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
 raw=c['research_queues'][k];ts=list(q.tokens(raw));x=q.scalars(raw[ts[0][2]:ts[-1][1]]);x.setdefault('progress',0);return x
def flags(s):
 return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
b=read_state(run,before);ba=b['audit'];bc=ba['countries']['0'];p=load(prior);eps=D('.00003')
income=lambda c:{k:sum((D(str(v.get(k,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bi=income(bc);bp=rq(bc,'society_queue');be=rq(bc,'engineering_queue');ids=q.ids(q.block(b['queues']['0'],'items'));head=D(str(q.scalars(b['items']['251658284'])['progress']))
basic=p['status'].startswith('PASS') and bool(p['checks']) and all(v is True for v in p['checks'].values()) and checked(execution) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav'))
days=day(other)-day(ba['date']) if mode=='review' else day(load(other+'.audit.json')['date'])-day(ba['date'])
end=other if mode=='review' else load(other+'.audit.json')['date']
ticks=sum(1 for n in range(1,days+1) if (day(ba['date'])+n)%30==1)
months=sum(1 for n in range(1,days+1) if (day(ba['date'])+n)%30==0)
package=m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
if mode=='review':
 checks={
  'prior_PASS_actual0_source_originalSAV':basic,
  'bounded1_to30_days_before_or_at_March30_border_review':1<=days<=30 and day('2286.02.22')<=day(ba['date'])<day(other)<=day('2286.03.30'),
  'no_pending_or_technology_hive_project_completion':not b['pending'] and ids==[251658284,1191182345,117440553,1476395019,117440546] and head+D(days)*D('1.4')<480 and D(str(be['progress']))+D(ticks)*bi['engineering_research']*D('1.35')<550 and D(str(bp['progress']))+D(ticks)*bi['society_research']*D('2.35')<12000 and not q.ids(q.block(b['queues'].get('3',''),'items')),
  'CN41_unfiltered_live_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 }
 passed=all(v is True for v in checks.values());out=run/(before+'-postcombat-v3-review.json');assert not out.exists()
 h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':ba['save_sha256'],'start_date':ba['date'],'end_date':other,'days':days,'maximum_days':days,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-postcombat-v3-review'})
 print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed;sys.exit(0)
assert mode=='guard';after=other;a=read_state(run,after);aa=a['audit'];ac=aa['countries']['0'];ap=rq(ac,'society_queue');ae=rq(ac,'engineering_queue');ai=income(ac)
ob=load(after+'-construction-boundary-observation-v4.json');cal=load(after+'-calendar-receipt.json');review=load(before+('-postcombat-v1-review.json' if before=='terravore-crystal164-22860222' else '-postcombat-v3-review.json'))
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade'];net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources};expected={k:D(str(bc['effective_stockpile'].get(k,0)))+D(months)*v for k,v in net.items()};expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade']);residual={k:D(str(ac['effective_stockpile'].get(k,0)))-v for k,v in expected.items()}
draw=min(bi['society_research'],D(str(bc['research_stockpile']['society_research'])));ef={k:dict(v,flag_days=v['flag_days']-days) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>days}
raw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(raw));growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
routes={};route_ok=True
for fid in ['83886903','50332250','917']:
 am=q.block(a['fleets'][fid],'movement_manager');bm=q.block(b['fleets'][fid],'movement_manager');path=q.block(am,'path');nodes=[q.scalars(q.block(v,'coordinate'))['origin'] for k,v,obj in q.fields(path) if obj and k=='node'];remain=[i for i,_ in groupby(nodes)];current=q.scalars(q.block(am,'coordinate'))['origin'];previous=q.scalars(q.block(bm,'coordinate'))['origin'];order=q.block(q.block(a['fleets'][fid],'current_order'),'orbit_planet_order');routes[fid]={'current':current,'remaining':remain,'eta':q.scalars(path).get('date'),'target':q.scalars(q.block(am,'target_coordinate'))}
 if fid in ['50332250','917']:
  route_ok=route_ok and current==previous==188 and not remain and not q.block(a['fleets'][fid],'current_order') and q.scalars(am)['state']=='move_idle' and q.scalars(q.block(am,'target_coordinate'))=={'x':0,'y':0,'origin':4294967295} and q.block(am,'orbit')==q.block(bm,'orbit') and q.scalars(a['fleets'][fid])['order_id']==q.scalars(b['fleets'][fid])['order_id']
  continue
 full=[164]
 route_ok=route_ok and q.scalars(a['fleets'][fid])['order_id']==q.scalars(b['fleets'][fid])['order_id'] and current in full and previous in full and full.index(current)>=full.index(previous)
 if q.scalars(am)['state']=='move_idle':
  coord=q.scalars(q.block(am,'coordinate'))
  center=abs(coord['x']-10.62)<.5 and abs(coord['y']-10.62)<.5
  orbit=q.scalars(q.block(q.block(am,'orbit'),'orbitable'))
  route_ok=route_ok and not remain and q.scalars(q.block(am,'target_coordinate'))=={'x':0,'y':0,'origin':4294967295}
  if order:
   route_ok=route_ok and q.scalars(order).get('can_reach')=='yes' and q.scalars(q.block(order,'orbitable'))=={'planet':1732} and not q.block(order,'sub_order') and (orbit=={'planet':1732} or (not orbit and center))
  else:route_ok=route_ok and orbit=={'planet':1732}
 else:
  route_ok=route_ok and remain==[164] and q.scalars(q.block(am,'target_coordinate'))['origin']==164 and q.scalars(order).get('can_reach')=='yes' and q.scalars(q.block(order,'orbitable'))=={'planet':1732}

zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295};builds={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295};army=q.ids(q.block(b['country'],'owned_armies'));news=ob['new_country0_messages_raw'];ex=ac['budget_categories']['current_month']['expenses']
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']

mainids=set(q.ids(q.block(b['fleets']['83886903'],'ships')));life=len(mainids)==16;health={}
for i,v in b['ships'].items():
 av=a['ships'].get(i,'');bs,ass=q.scalars(v),q.scalars(av)
 life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and bs.get('construction_date')==ass.get('construction_date') and bs.get('killed')==ass.get('killed') and all(bs.get(k)==ass.get(k) for k in ['max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
 if int(i) not in mainids:
  life=life and all(bs.get(k)==ass.get(k) for k in ['hitpoints','armor_hitpoints','shield_hitpoints'])
 else:
  record={}
  for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
   maximum=D(str(bs[cap]));expected_health=min(maximum,D(str(bs.get(key,0)))+maximum*D('.0005')*D(5)*D(days));actual=D(str(ass.get(key,0)))
   record[key]={'before':str(bs.get(key,0)),'after':str(actual),'expected':str(expected_health),'residual':str(actual-expected_health)}
   life=life and abs(actual-expected_health)<D('.0001')
  life=life and ass.get('shield_hitpoints',0)==0 and ass.get('hitpoints',0)>0
  health[i]=record


level_news=False
if after=='terravore-recovery-22860301':
 lb=q.block(b['roots']['leaders'],'80');la=q.block(a['roots']['leaders'],'80');lbs,las=q.scalars(lb),q.scalars(la)
 level_news=len(news)==1 and q.scalars(news[0])=={'type':'LEADER_LEVEL_UP','localization':'LEADER_LEVEL_UP_NEXT_LEVEL_DESC','receiver':0,'target_leader':80,'end':'2286.04.16','date':'2286.03.01','notification':313,'message_type':'level'} and lbs['level']==5 and las['level']==6 and lbs['experience']==4991.25 and las['experience']==2.75 and lbs['available_trait_selections']==2 and las['available_trait_selections']==3 and omit(lb,{'level','experience','available_trait_selections'})==omit(la,{'level','experience','available_trait_selections'})

checks={
 'prior_review_calendar_observer_actual0_originalSAV':basic and len(ob['checks']) in [6,7] and all(v is True for pp in [ob,review] for v in pp['checks'].values()) and all(checked(s) for s in [after+'-boundary-observation-v4',after+'-calendar',review['execution_stage']]) and ob['before_sha256']==ba['save_sha256'] and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'single_bounded_native_interval_before_or_at_border':cal['days']==days and cal['start_date']==ba['date'] and cal['date']==aa['date']==end and 1<=days<=30 and day(aa['date'])<=day('2286.03.30'),
 'cash8_exact_new_native_budget_caps_no_payments':all(abs(v)<eps for v in residual.values()) and all(ac['effective_stockpile'].get(k,0)>=0 for k in resources),
 'project3_one_tick_and_true_bank_exact':bi==ai and bi=={'physics_research':D('32.6914'),'society_research':D('68.1742'),'engineering_research':D('76.4242')} and bp['special_project']==ap['special_project']==9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-D(ticks)*(bi['society_research']*D('1.35')+draw))<eps and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+D(ticks)*draw)<eps and ap['progress']<12000,
 'engineering_one_tick_and_idle_physics_bank_exact':be['technology']==ae['technology']=='tech_industrial_storm_protection' and abs(D(str(ae['progress']))-D(str(be['progress']))-D(ticks)*bi['engineering_research']*D('1.35'))<eps and abs(D(str(ac['research_stockpile']['physics_research']))-D(str(bc['research_stockpile']['physics_research']))-D(ticks)*bi['physics_research']*D('1.35'))<eps and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0 and ae['progress']<550,
 'all_other_technology_projects_held':dict(bp,progress=ap['progress'])==ap and dict(be,progress=ae['progress'])==ae and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'all75_original_ships_identity_and_exact_native_regeneration':len(b['ships'])==len(a['ships'])==75 and set(b['ships'])==set(a['ships']) and life,
 'all35_original_fleets_same_members':len(b['fleets'])==len(a['fleets'])==35 and set(b['fleets'])==set(a['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()),
 'main_legal_native_travel164_and_two_idle_mineral_fleets':route_ok,
 'no_new_ships_shiporders_naval251':not q.ids(q.block(a['queues'].get('3',''),'items')) and q.scalars(a['country'])['used_naval_capacity']==q.scalars(a['country'])['fleet_size']==251,
 'EEP_government_AP_traditions_crisis_menace_no_rewards':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==3065,
 'mother_only_species73_natural_growth_OTHER0':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+months*growth.get('GROWTH_CAT_GROWTH',0) and set(growth)<={'GROWTH_CAT_GROWTH','GROWTH_CAT_OTHER','GROWTH_CAT_PROMOTION'} and 0<=growth.get('GROWTH_CAT_GROWTH',0)<=10 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'mother39_paid28_original_zones_labs_research_jobs_held':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==28 and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in builds) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']),
 'five_paid400_hives_only_head_daily1_4_no_completion':q.ids(q.block(a['queues']['0'],'items'))==ids and omit(b['items']['251658284'],{'progress'})==omit(a['items']['251658284'],{'progress'}) and abs(D(str(q.scalars(a['items']['251658284'])['progress']))-head-D(days)*D('1.4'))<eps and q.scalars(a['items']['251658284'])['progress']<480 and all(a['items'][str(i)]==b['items'][str(i)] for i in ids[1:]),
 'all15_original_armies_raw_held':len(army)==15 and army==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in army),
 'native_country_flags_only_normal_timers_expire':flags(a)==ef,
 'native_player_contacts63_64_65_held':all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'only_reviewed_lowtrade_pirate6_delay':len(delays)<=1 and all(v['event']=='pirate.6' and 1<=v['days']<=30 for v in delays) and sum(D(str(v.get('trade',0))) for v in ac['budget_categories']['current_month']['income'].values())<300 and 'birth_of_piracy' not in ac['flags'],
 'no_pending_unknown_news_wars_truces_or_combat':not a['pending'] and (level_news or all(q.scalars(v).get('type')=='SYSTEM_SURVEYED' and q.scalars(v).get('localization')=='MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED' for v in news)) and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'all_other_owned_queues_held':all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0),
 'native23_mineral_hulls_away_M_upkeep_no_dock_discount':abs(D(str(ex['ships']['minerals']))-(D('77.70204')*D(251)/D(261) if before=='terravore-crystal164-22860222' else D('74.72517')))<D('.001'),
 'destroyed_source_no_active_EEP_no_return':aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0 and all(v.get('killed')=='yes' for v in aa['situations'].values()),
 'positive_housing_amenities_no_crime':aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'CN41_unfiltered_live_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}

if after=='terravore-recovery-22860301':
 op=load(after+'-postcombat-v1-proof.json');ox=load(after+'-postcombat-v1-guard-execution.json')
 checks['original24_only_three_FAIL_actual1_source_pair_retained']=len(op['checks'])==24 and [k for k,v in op['checks'].items() if v is not True]==['main_legal_native_travel164_and_two_idle_mineral_fleets','no_pending_unknown_news_wars_truces_or_combat','native23_mineral_hulls_away_M_upkeep_no_dock_discount'] and ox['returncode']==1 and ox['helper_sha256']=='2b6e7ae4f825b4ef49ac4424a1ff2aa16a04d72f9c0a6740d66f1a6f65a04c5c' and op['before_sha256']==ba['save_sha256'] and op['after_sha256']==aa['save_sha256']
 checks['exact_native_regulatory_node80_level6_notification_no_trait_choice']=level_news
 vx=load(after+'-postcombat-v2-guard-execution.json')
 checks['V2_review_stage_FileNotFound_actual1_source_retained']=vx['returncode']==1 and vx['helper_sha256']=='bbc456244debb1bf245e67df681da6b0da078d3c6d0f743a0a8801a697a5acb8'

passed=all(v is True for v in checks.values());out=run/(after+'-postcombat-v3-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_TRAVEL164_MONTH' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'routes':routes,'project3_progress':ap['progress'],'engineering_progress':ae['progress'],'hive_head_work':q.scalars(a['items']['251658284'])['progress'],'growth_details':growth,'cash_residual':{k:str(v) for k,v in residual.items()},'ships_upkeep':ex['ships'],'component_upkeep':ex['ship_components'],'new_messages_raw':news,'boundaries':['native_postcombat_next_window_or_border_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One bounded peaceful postcombat interval, including exact native regeneration; not full civic acceptance.','days':days,'research_ticks':ticks,'budget_settlements':months,'regeneration':health})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'project3':ap['progress'],'hive_work':q.scalars(a['items']['251658284'])['progress'],'routes':routes}),flush=True);assert passed
