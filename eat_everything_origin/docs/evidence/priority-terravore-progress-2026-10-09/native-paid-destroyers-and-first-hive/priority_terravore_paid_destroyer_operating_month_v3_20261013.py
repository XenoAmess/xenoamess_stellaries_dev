"""Bounded normal shipyard months, one independent native autosave ledger per month."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
mode,before,other,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def day(date):
 y,mo,d=map(int,date.split('.'));return y*360+(mo-1)*30+d-1
def date(n):
 y,v=divmod(n,360);mo,d=divmod(v,30);return f'{y:04d}.{mo+1:02d}.{d+1:02d}'
def checked(x):
 return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
def flags(s):
 return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
def queue(c,k):
 raw=c['research_queues'][k];ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]])
b=read_state(run,before);ba=b['audit'];bc=ba['countries']['0'];p=load(prior);px=load(execution+'-execution.json')
ids=q.ids(q.block(b['queues']['3'],'items'));head=D(str(q.scalars(b['items'][str(ids[0])])['progress']));eps=D('.00002')
basic=p['status'].startswith('PASS') and p['checks'] and all(v is True for v in p['checks'].values()) and checked(px) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav'))
package=m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
if mode=='review':
 end=other
 checks={
  'prior_business_PASS_actual0_source_SAV_bound':basic,
  'exact30days_month1_window_September1_to_May1':ba['date'].endswith('.01') and end.endswith('.01') and day(end)-day(ba['date'])==30 and day('2284.09.01')<=day(ba['date'])<day(end)<=day('2285.05.01'),
  'paid_parallel_hulls_and_hive_no_completion_or_pending':not b['pending'] and len(ids)>=2 and len(ids)%2==0 and q.scalars(b['queues']['3'])=={'owner':0,'simultaneous':2,'type':'ships'} and all(q.scalars(q.block(b['items'][str(i)],'resources'))=={'minerals':412.5} and q.scalars(b['items'][str(i)])['progress']==(float(head) if n<2 else 0) for n,i in enumerate(ids)) and D(str(q.scalars(b['items']['268435492'])['progress']))+42<480,
  'CN41_and_unfiltered_live_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 }
 out=run/(before+'-operating-month-review-v3.json');assert not out.exists();passed=all(v is True for v in checks.values())
 h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':ba['save_sha256'],'start_date':ba['date'],'end_date':end,'days':30,'maximum_days':30,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-operating-month-review-v3','scope':'One normal30day shipyard operating interval, within documented eight month window. No authorization beyond May1.'})
 print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed;sys.exit(0)
assert mode=='guard'
after=other;a=read_state(run,after);aa=a['audit'];ac=aa['countries']['0'];ob=load(after+'-construction-boundary-observation-v4.json');ox=load(after+'-boundary-observation-v4-execution.json');cal=load(after+'-calendar-receipt.json');cx=load(after+'-calendar-execution.json');reviewstem=next(before+suffix for suffix in ['-operating-month-review-v3','-operating-month-review-v2','-operating-month-review'] if (run/(before+suffix+'.json')).exists());review=load(reviewstem+'.json');rx=load(reviewstem+'-execution.json')
bp,ap=queue(bc,'society_queue'),queue(ac,'society_queue');be,ae=queue(bc,'engineering_queue'),queue(ac,'engineering_queue')
income=lambda c:{k:sum((D(str(v.get(k,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bi,ai=income(bc),income(ac);draw=min(bi['society_research'],D(str(bc['research_stockpile']['society_research'])))
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade'];net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
expected={k:D(str(bc['effective_stockpile'].get(k,0)))+v for k,v in net.items()};expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade']);residual={k:D(str(ac['effective_stockpile'].get(k,0)))-v for k,v in expected.items()}
total=head+45;birth=total>=60;removed=ids[:2] if birth else [];remaining=ids[2:] if birth else ids;work=total-60 if birth else total
born_date=date(day(ba['date'])+int((60-head)/D('1.5'))) if birth else None
new=set(a['ships'])-set(b['ships']);bf=flags(b);ef={k:dict(v,flag_days=v['flag_days']-30) if isinstance(v,dict) and 'flag_days' in v else v for k,v in bf.items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>30}
if birth:ef['built_artificial_ship']=63539112+24*(day(born_date)-day('2284.08.14'))
zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295};builds={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
raw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(raw));growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
army=q.ids(q.block(b['country'],'owned_armies'));news=ob['new_country0_messages_raw'];ex=ac['budget_categories']['current_month']['expenses']
sourceproof=load('terravore-destroyer-first-upkeep-22840901-destroyer-first-upkeep-proof.json');sources=sourceproof['native_sources']+load('terravore-destroyer-first-pair-born-22840814-destroyer-first-pair-birth-v3-proof.json')['sources']
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
native304=after=='terravore-paid-destroyer-operating-22850101'
if native304:ef['sr_zro_found']=63542280
fleet_ok=set(b['fleets'])<=set(a['fleets']);appended=[]
for fid,rawfleet in a['fleets'].items():
 members=q.ids(q.block(rawfleet,'ships'));old=q.ids(q.block(b['fleets'].get(fid,''),'ships'))
 fleet_ok=fleet_ok and members[:len(old)]==old
 additions=members[len(old):];appended.extend(additions)
 if additions:
  sizes=[]
  for sid in members:
   did=str(q.scalars(q.block(a['ships'][str(sid)],'ship_design_implementation'))['design'])
   stage_raw=q.block(a['designs'][did],'growth_stages');stage_tokens=list(q.tokens(stage_raw));size=q.scalars(stage_raw[stage_tokens[0][2]:stage_tokens[-1][1]])['ship_size']
   sizes.append({'crisis_corvette':4,'crisis_destroyer':8}.get(size,999))
  fleet_ok=fleet_ok and bool(members) and set(map(str,additions))<=new and sum(sizes)<=90 and q.scalars(rawfleet)['ship_class']=='shipclass_military' and q.scalars(q.block(q.block(q.block(rawfleet,'movement_manager'),'orbit'),'orbitable'))=={'starbase':0}
fleet_ok=fleet_ok and set(map(str,appended))==new and len(appended)==len(new) and len(set(a['fleets'])-set(b['fleets']))<=len(new)
known_pending=not a['pending']
known_news=all(q.scalars(v).get('type')=='SYSTEM_SURVEYED' and q.scalars(v).get('localization')=='MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED' or aa['date'].endswith('.01.01') and q.scalars(v).get('type')=='LEADER_POOL_REFRESHED_MESSAGE_TYPE' and q.scalars(v).get('localization')=='LEADER_POOL_REFRESHED_TITLE' for v in news)
if native304:
 known_pending=len(a['pending'])==1 and q.scalars(a['pending'][0])=={'id':304,'event':'utopia.2602','date':'2287.03.21','country':0} and q.scalars(q.block(q.block(a['pending'][0],'scope'),'from'))['id']==16777219
 known_news=len(news)==3 and len([v for v in news if q.scalars(v).get('event')==304 and q.scalars(v).get('date')=='2284.12.21' and q.scalars(v).get('type')=='EVENT_MESSAGE_TYPE'])==1 and len([v for v in news if q.scalars(v).get('type')=='MESSAGE_STRATEGIC_RESOURCE_FOUND_ZRO' and q.scalars(v).get('target_planet')==270 and q.scalars(v).get('date')=='2284.12.26'])==1 and len([v for v in news if q.scalars(v).get('type')=='LEADER_POOL_REFRESHED_MESSAGE_TYPE' and q.scalars(v).get('date')=='2285.01.01'])==1
for rel in ['events/utopia_on_action_events.txt','events/on_action_events_1.txt','common/message_types/00_message_types.txt']:
 src=h.GAME_EXE.parent/rel;dest=run/('native-january304-'+src.name)
 if native304:
  assert not dest.exists();dest.write_bytes(src.read_bytes())
 sources.append({'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)})
checks={
 'prior_preflight_calendar_observer_actual0_sources_exactSAV':basic and len(ob['checks'])==7 and all(v is True for pp in [ob,review] for v in pp['checks'].values()) and all(checked(v) for v in [ox,cx,rx]) and ob['before_sha256']==ba['save_sha256'] and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'documented_normal30day_month1_within_window':cal['days']==30 and cal['start_date']==ba['date'] and cal['date']==aa['date'] and review['end_date']==aa['date'] and day(aa['date'])-day(ba['date'])==30 and aa['date'].endswith('.01') and day(aa['date'])<=day('2285.05.01'),
 'cash8_native_new_budget_caps_exact_no_new_payment':all(abs(v)<eps for v in residual.values()) and all(ac['effective_stockpile'].get(k,0)>=0 for k in resources),
 'one_society_tick_and_truebank_exact':bi==ai and bi['society_research']==D('61.7104') and bp['special_project']==ap['special_project']==9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-bi['society_research']*D('1.35')-draw)<eps and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+draw)<eps and ap['progress']<12000,
 'one_E_tick_P_idle_bank_exact_no_tech_unlock':be['technology']==ae['technology']=='tech_alloys_2' and abs(D(str(ae['progress']))-D(str(be['progress']))-bi['engineering_research']*D('1.35'))<eps and abs(D(str(ac['research_stockpile']['physics_research']))-D(str(bc['research_stockpile']['physics_research']))-bi['physics_research']*D('1.35'))<eps and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0 and ae['progress']<2600,
 'all_other_tech_fields_and_projects_raw_held':dict(bp,progress=ap['progress'])==ap and dict(be,progress=ae['progress'])==ae and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'paid_queue_only_expected_two_consume_and_remainder_work':q.ids(q.block(a['queues']['3'],'items'))==remaining and q.scalars(b['queues']['3'])==q.scalars(a['queues']['3'])=={'owner':0,'simultaneous':2,'type':'ships'} and all(str(i) not in a['items'] for i in removed) and all(omit(b['items'][str(i)],{'progress'})==omit(a['items'][str(i)],{'progress'}) and q.scalars(q.block(a['items'][str(i)],'resources'))=={'minerals':412.5} and abs(D(str(q.scalars(a['items'][str(i)])['progress']))-(work if n<2 else 0))<eps for n,i in enumerate(remaining)),
 'only_expected_paid_full_native_hulls_actual_birth_date':len(new)==len(removed) and set(b['ships'])<=set(a['ships']) and all(q.scalars(q.block(a['ships'][i],'ship_design_implementation'))=={'design':83887141,'upgrade':4294967295,'growth_stage':0} and q.scalars(a['ships'][i])['construction_date']==born_date and str(q.scalars(a['ships'][i])['fleet']) in a['fleets'] and q.scalars(q.block(a['ships'][i],'coordinate'))['origin']==0 and all(q.scalars(a['ships'][i])[k]==q.scalars(a['ships'][i])[mk]==val for k,mk,val in [('hitpoints','max_hitpoints',1500),('shield_hitpoints','max_shield_hitpoints',480),('armor_hitpoints','max_armor_hitpoints',765)]) for i in new),
 'all_original_ships_identity_design_name_birth_life_held':all(all(q.scalars(v).get(k)==q.scalars(a['ships'][i]).get(k) for k in ['construction_date','hitpoints','max_hitpoints','armor_hitpoints','shield_hitpoints']) and q.block(v,'ship_design_implementation')==q.block(a['ships'][i],'ship_design_implementation') and q.block(v,'name')==q.block(a['ships'][i],'name') for i,v in b['ships'].items()),
 'all_original_fleets_members_held_only_paid_mineral_append_within90':fleet_ok,
 'naval_size_exact_new_size8_hulls':q.scalars(a['country'])['used_naval_capacity']==q.scalars(a['country'])['fleet_size']==q.scalars(b['country'])['used_naval_capacity']+8*len(new),
 'EEP_variables_flags_gov_AP_traditions_crisis_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==2930,
 'mother_only_natural_growth_species73_OTHER0':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+growth.get('GROWTH_CAT_GROWTH',0) and set(growth)<={'GROWTH_CAT_GROWTH','GROWTH_CAT_OTHER','GROWTH_CAT_PROMOTION'} and 0<=growth.get('GROWTH_CAT_GROWTH',0)<=10 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'mother39_paid27_all_original_buildings_zones_research_jobs':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27 and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in builds) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']),
 'six_paid400_hives_only_front_plus42_no_completion':q.ids(q.block(a['queues']['0'],'items'))==q.ids(q.block(b['queues']['0'],'items')) and omit(b['items']['268435492'],{'progress'})==omit(a['items']['268435492'],{'progress'}) and abs(D(str(q.scalars(a['items']['268435492'])['progress']))-D(str(q.scalars(b['items']['268435492'])['progress']))-42)<eps and q.scalars(a['items']['268435492'])['progress']<480 and all(a['items'][str(i)]==b['items'][str(i)] for i in q.ids(q.block(b['queues']['0'],'items'))[1:]),
 'destroyed_source_no_active_EEP_no_return':aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0 and all(v.get('killed')=='yes' for v in aa['situations'].values()),
 'all15_original_armies_raw_held':len(army)==15 and army==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in army),
 'country_timers_exact_expiry_only_native_birth_flag_refresh':flags(a)==ef,
 'native_contact63_unassigned_raw80_held':q.block(q.block(a['roots']['first_contacts'],'contacts'),'63')==q.block(q.block(b['roots']['first_contacts'],'contacts'),'63') and q.scalars(q.block(q.block(a['roots']['first_contacts'],'contacts'),'63'))['days_left']==80,
 'only_reviewed_lowtrade_piracy_no_storm_or_other_delay':len(delays)<=1 and all(v['event']=='pirate.6' and 1<=v['days']<=30 for v in delays) and sum(D(str(v.get('trade',0))) for v in ac['budget_categories']['current_month']['income'].values())<300 and 'birth_of_piracy' not in ac['flags'],
 'no_unknown_messages_pending_combat_wars_truces_or_orders':known_pending and known_news and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0),
 'positive_housing_amenities_no_crime':aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'CN41_native_sources_unfiltered_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
if native304:
 original=load(after+'-operating-month-proof.json');original_x=load(after+'-operating-month-guard-execution.json')
 expected_fail={'only_expected_paid_full_native_hulls_actual_birth_date','same34fleets_only_mineral_members_append_still_docked','country_timers_exact_expiry_only_native_birth_flag_refresh','no_unknown_messages_pending_combat_wars_truces_or_orders'}
 checks['original23_fourFAIL_actual1_source_sameSAV_retained']=len(original['checks'])==23 and {k for k,v in original['checks'].items() if v is False}==expected_fail and original_x['returncode']==1 and original_x['helper_sha256']==h.sha256(Path(original_x['command'][1]))=='2e5ca8ce78ec97a28f7e9ce0300da7946cdfb9d6005216f957d3b1ada97e2924' and original['before_sha256']==ba['save_sha256'] and original['after_sha256']==aa['save_sha256']
 ut=Path(sources[-3]['path']).read_text('utf-8-sig');ev=next(v for k,v,obj in q.fields(ut) if obj and q.scalars(v).get('id')=='utopia.2602');opts=[v for k,v,obj in q.fields(ev) if obj and k=='option']
 checks['native304_all_four_options_only_name_trigger_no_effect_no_immediate']=len(opts)==4 and all(set(k for k,v,obj in q.fields(opt))<={'name','trigger'} for opt in opts) and not q.block(ev,'immediate') and 'trait_psionic' in q.block(q.block(a['roots']['species_db'],'73'),'traits')
 checks['native_zro_old_deposit358_message_definition_and_no_reward']=q.block(b['roots']['deposit'],'358')==q.block(a['roots']['deposit'],'358') and 358 in q.ids(q.block(q.block(q.block(a['roots']['planets'],'planet'),'270'),'deposits')) and 'MESSAGE_STRATEGIC_RESOURCE_FOUND_ZRO' in Path(sources[-2]['path']).read_text('utf-8-sig') and 'sr_zro_found' in Path(sources[-2]['path']).read_text('utf-8-sig') and 'LEADER_POOL_REFRESHED_MESSAGE_TYPE' in Path(sources[-1]['path']).read_text('utf-8-sig')
if after=='terravore-paid-destroyer-operating-22850201':
 old=load(after+'-operating-month-v2-proof.json');oldx=load(after+'-operating-month-guard-v2-execution.json')
 checks['original23_only_survey_localization_field_FAIL_actual1_bound']=len(old['checks'])==23 and [k for k,v in old['checks'].items() if v is not True]==['no_unknown_messages_pending_combat_wars_truces_or_orders'] and oldx['returncode']==1 and oldx['helper_sha256']==h.sha256(Path(oldx['command'][1]))=='a678ff892ee35e8290b740000e3416297f86cf460d57a0b903e624614aa19084' and old['before_sha256']==ba['save_sha256'] and old['after_sha256']==aa['save_sha256']
passed=all(v is True for v in checks.values());out=run/(after+'-operating-month-v3-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_PAID_DESTROYER_OPERATING_MONTH' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'sources':sources,'new_ship_ids':sorted(new,key=int),'expected_birth_date':born_date,'consumed_paid_orders':removed,'remaining_paid_orders':remaining,'shipyard_work':str(work),'project3_progress':ap['progress'],'engineering_progress':ae['progress'],'hive_work':q.scalars(a['items']['268435492'])['progress'],'growth_details':growth,'cash_residual':{k:str(v) for k,v in residual.items()},'ships_upkeep':ex.get('ships'),'component_upkeep':ex.get('ship_components'),'new_messages_raw':news,'boundaries':['native_psionic304_ack_review'] if native304 else ['paid_destroyer_operating_month_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One independently checked native operating month within documented window, not full Terravore acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'new_paid_hulls':len(new),'orders_left':len(remaining),'project3':ap['progress'],'hive_work':q.scalars(a['items']['268435492'])['progress']}),flush=True);assert passed
