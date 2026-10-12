"""Read-only targeted native campaign checks, preserving full source SAVs."""
import json,logging,re,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
before,after=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_native_reviewed_error_baseline import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda name:json.loads((run/name).read_text('utf-8-sig'))
o=load(after+'-construction-boundary-observation-v3.json');b,a=o['before_state'],o['after_state'];ba,aa=b['audit'],a['audit'];bc,ac=[s['countries']['0'] for s in [ba,aa]]
cal=load(after+'-calendar-receipt.json');cx=load(after+'-calendar-execution.json');ox=load(after+'-boundary-observation-v3-execution.json');pre=load(cal['prior_proof_file']);px=load(cal['prior_execution_stage']+'-execution.json')
def roots(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:return {k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
br,ar=roots(before),roots(after)
omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
def ordinal(date):
 y,mo,d=map(int,date.split('.'));return y*360+(mo-1)*30+d-1
days=ordinal(aa['date'])-ordinal(ba['date']);months=ordinal(aa['date'])//30-ordinal(ba['date'])//30
def tick(date):
 y,mo,d=map(int,date.split('.'));return y*12+mo+int(d>=2)
ticks=tick(aa['date'])-tick(ba['date'])
def items(st):return {i:v for i,v,x in q.fields(q.block(q.block(st['raw_roots']['construction'],'item_mgr'),'items')) if x and q.scalars(v).get('paying_country')==0}
bi,ai=items(b),items(a);expected={};completed=[];left=days
for i in q.ids(q.block(q.block(q.block(q.block(b['raw_roots']['construction'],'queue_mgr'),'queues'),'1'),'items')):
 raw=bi[str(i)];s=q.scalars(raw);assert s['progress_needed']==90 and q.scalars(q.block(raw,'buildable_army'))['army_type']=='assault_army'
 work=min(left,90-s['progress']);left-=work
 if s['progress']+work==90:completed.append(str(i))
 else:expected[str(i)]=s['progress']+work
orders_ok=ai.keys()==expected.keys() and all(omit(bi[i],{'progress'})==omit(ai[i],{'progress'}) and q.scalars(ai[i])['progress']==v for i,v in expected.items())
old_armies=q.ids(q.block(b['country0_raw'],'owned_armies'));new_armies=set(q.ids(q.block(a['country0_raw'],'owned_armies')))-set(old_armies)
army_births=[]
for i in new_armies:
 raw=q.block(ar['army'],str(i));s=q.scalars(raw);ship=a['owned_ships_raw'].get(str(s.get('ship')),'');ss=q.scalars(ship)
 army_births.append({'army':i,'army_raw':raw,'ship':s.get('ship'),'ship_raw':ship,'valid':s.get('type')=='assault_army' and s.get('owner')==0 and s.get('species')==73 and s.get('health')==s.get('max_health') and s.get('max_health') in [200,330] and s.get('morale')==200 and ss.get('army')==i and ba['date']<ss.get('construction_date','')<=aa['date'] and q.scalars(q.block(ship,'coordinate')).get('origin')==0})
army_ok=len(new_armies)==len(completed) and all(x['valid'] for x in army_births) and set(old_armies)<=set(q.ids(q.block(a['country0_raw'],'owned_armies'))) and all(omit(q.block(br['army'],str(i)),{'health','max_health'})==omit(q.block(ar['army'],str(i)),{'health','max_health'}) and q.scalars(q.block(ar['army'],str(i)))['health']==q.scalars(q.block(ar['army'],str(i)))['max_health'] for i in old_armies)
bornships={x['ship'] for x in army_births};added=set(a['owned_ship_ids'])-set(b['owned_ship_ids']);captures=[]
enemy_owned=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(br['country'],'1'),'fleets_manager'),'owned_fleets'))))
enemy_after=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(ar['country'],'1'),'fleets_manager'),'owned_fleets'))))
for i in added-bornships:
 raw=q.block(br['ships'],str(i));ss=q.scalars(raw);oldfleet=q.block(br['fleet'],str(ss.get('fleet')));new=a['owned_ships_raw'][str(i)];ns=q.scalars(new);fid=ss.get('fleet');cls=q.scalars(oldfleet).get('ship_class');origin=q.scalars(q.block(new,'coordinate')).get('origin')
 captures.append({'ship':i,'fleet':fid,'class':cls,'system':origin,'before_ship_raw':raw,'after_ship_raw':new,'valid':fid in enemy_owned and fid not in enemy_after and fid in a['owned_fleets'] and ns.get('fleet')==fid and cls in ['shipclass_starbase','shipclass_mining_station','shipclass_research_station'] and origin in [146,96,53,147] and ss.get('construction_date')==ns.get('construction_date')<ba['date']})
def objects(raw):
 depth=0;start=0
 for token,x,y in q.tokens(raw):
  if token=='{':
   if depth==0:start=y
   depth+=1
  elif token=='}':
   depth-=1
   if depth==0:yield raw[start:x]
 assert depth==0
messages_ok=True;reports=[];storms=[]
for raw in o['new_country0_messages_raw']:
 s=q.scalars(raw)
 if s.get('type')=='COMBAT_STATS':
  cs=q.block(raw,'combat_stats');ours=list(objects(q.block(cs,'fleets')));enemies=list(objects(q.block(cs,'enemy')));origin=q.scalars(q.block(raw,'coordinate')).get('origin')
  valid=len(ours)==len(enemies)==1 and q.scalars(ours[0]).get('fleet')==83886903 and q.ids(q.block(ours[0],'ship_size_count'))==[18] and q.ids(q.block(ours[0],'ship_size_count_lost'))==[0] and q.scalars(enemies[0]).get('country')==1 and q.scalars(enemies[0]).get('ship_class')=='shipclass_starbase' and q.ids(q.block(enemies[0],'ship_size_count'))==[1] and q.ids(q.block(enemies[0],'ship_size_count_lost'))==[0] and origin in [146,96,53,147] and q.scalars(cs).get('reason')=='no_more_enemies'
  reports.append({'system':origin,'raw':raw,'valid':valid});messages_ok &= valid
 elif s.get('message_type')=='cosmic_storm' and s.get('type')=='STORM_GRAVITY_STORM_VISIBLE':
  storms.append(raw)
  messages_ok &= s.get('cosmic_storm') is not None and q.scalars(q.block(q.block(ar['storms'],'storms'),str(s['cosmic_storm']))).get('type')=='gravity_storm'
 else:messages_ok=False
cash=['energy','minerals','alloys','unity'];net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in cash};deltas={k:D(str(ac['effective_stockpile'][k]))-D(str(bc['effective_stockpile'][k])) for k in cash}
def queue(c,name):
 raw=q.block(c['tech_status'],name);ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]]) if ts else {}
bp,ap=queue(bc,'physics_queue'),queue(ac,'physics_queue');be,ae=queue(bc,'engineering_queue'),queue(ac,'engineering_queue');epsilon=D('.00001')*max(ticks,1)
expense=ac['budget_categories']['current_month']['expenses'];ds=[q.scalars(v) for k,v,x in q.fields(q.block(q.block(a['country0_raw'],'modules'),'standard_event_module')) if k=='delayed_event' and x]
storm_review=load('terravore-native-cstorm1815-delayed-source-review.json')
storm_source_ok=h.sha256(run/'terravore-native-cstorm1815-delayed-source-review.json')=='d273e65bdc3a8f53da58911a4b14e5dca940d83d1ea3c44c56d8831eba11f322' and h.sha256(Path(storm_review['native_source']))==h.sha256(run/storm_review['preserved_source'])==storm_review['native_source_sha256']
def stormdelays(st):return [v for k,v,x in q.fields(q.block(q.block(st['country0_raw'],'modules'),'standard_event_module')) if k=='delayed_event' and x and q.scalars(v).get('event')=='cstorms.1815']
sdb,sda=stormdelays(b),stormdelays(a)
storm_delay_ok=storm_source_ok and len(sda)<=1 and (sda==[storm_review['new_delay_original']] and ba['save_sha256']==storm_review['before_sha256'] and aa['save_sha256']==storm_review['after_sha256'] if not sdb and sda else len(sdb)==len(sda) and all(omit(v,{'days'})==omit(sda[i],{'days'}) and q.scalars(sda[i])['days']==q.scalars(v)['days']-days and q.scalars(sda[i])['days']>0 for i,v in enumerate(sdb)))
checks={
 'prior_and_observation_and_calendar_actual0_original_SAVs':all(pre['checks'].values()) and all(o['checks'].values()) and px['returncode']==cx['returncode']==ox['returncode']==0 and pre['after_sha256']==ba['save_sha256'] and all(au['save_sha256']==h.sha256(run/(st+'.sav')) for st,au in [(before,ba),(after,aa)]) and all(ex['helper_sha256']==h.sha256(Path(ex['command'][1])) for ex in [px,cx,ox]) and 1<=days<=30 and months in [0,1],
 'paid_army_serial_work_and_exact_native_birth_association':orders_ok and army_ok,
 'existing_original_ships_designs_alive_no_removal_or_revival':set(b['owned_ship_ids'])<=set(a['owned_ship_ids']) and all(q.block(raw,'ship_design_implementation')==q.block(a['owned_ships_raw'][i],'ship_design_implementation') and q.scalars(a['owned_ships_raw'][i]).get('hitpoints',0)>0 for i,raw in b['owned_ships_raw'].items()) and not set(a['owned_ship_ids'])&{1807,1895,1896,67110639,16779140},
 'new_assets_only_paid_army_transport_or_preexisting_enemy_stations':all(x['valid'] for x in captures) and all(x['system'] in {v['system'] for v in reports} for x in captures) and len(added)==len(captures)+len(bornships),
 'only_documented_zero_loss_native_route_reports_and_real_storm_visibility':messages_ok and not a['pending_country0_raw'],
 'all_four_cash_ledgers_exact_month_net':deltas=={k:v*months for k,v in net.items()} and (ac['budget_categories']['last_month']==bc['budget_categories']['current_month'] if months else True),
 'rare_crystals_ordinary_captured_station_monthly_income':D(str(ac['effective_stockpile'].get('rare_crystals',0)))-D(str(bc['effective_stockpile'].get('rare_crystals',0)))==sum((D(str(v.get('rare_crystals',0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))*months,
 'EEP_government_AP_crisis_Menace_no_reward':all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis']) and ac['effective_stockpile']['menace']==bc['effective_stockpile']['menace']==1635,
 'mother35_capacity27_paid_levels_only_natural_growth_positive':aa['planets']['7']['variables']==ba['planets']['7']['variables'] and aa['colonies']['0']['districts']==ba['colonies']['0']['districts'] and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27 and bc['owned_colonies']==ac['owned_colonies']==[0] and set(a['species_population_by_colony'])=={'0:73'} and 0<=aa['colonies']['0']['actual_pop_sum']-ba['colonies']['0']['actual_pop_sum']<=10*months and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0,
 'true_research_banks_and_project2_original_engineering_ticks':bp.get('special_project')==ap.get('special_project')==8 and ap['progress']<6000 and abs(D(str(ap['progress']))-D(str(bp['progress']))-D('129.98954')*ticks)<=epsilon and abs(D(str(ae['progress']))-D(str(be['progress']))-D('37.72669')*ticks)<=epsilon and ae['technology']==be['technology']=='tech_starbase_4' and abs(D(str(ac['research_stockpile']['physics_research']))-D(str(bc['research_stockpile']['physics_research']))+D('55.31470')*ticks)<=epsilon and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))-D('26.58919')*ticks)<=epsilon and ac['research_stockpile']['engineering_research']==bc['research_stockpile']['engineering_research']==0,
 'mineral_ship_native_birth_and075M_no_added_ship_alloys':q.scalars(a['owned_ships_raw']['16777746'])['construction_date']=='2278.11.24' and expense['ships']['minerals']==.75 and expense['ships']['energy']==22.75 and expense['ships']['alloys']==10 and expense['ship_components']==bc['budget_categories']['current_month']['expenses']['ship_components'],
 'known_pirate_delay_only_no_birth':storm_delay_ok and len([s for s in ds if s.get('event')=='pirate.6'])<=1 and all((s.get('event')=='pirate.6' and 1<=s.get('days',0)<=30) or (s.get('event')=='cstorms.1815' and s.get('days',0)>0) for s in ds) and 'birth_of_piracy' not in q.scalars(q.block(a['country0_raw'],'flags')),
 'production_CN_error_exact_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),(run/(after+'-error-after.log')).read_bytes(),run),
}
bprojects,aprojects=[{q.scalars(v)['id']:v for k,v,x in q.fields(q.block(st['country0_raw'],'events')) if k=='special_project' and x} for st in [b,a]]
checks['all_special_project_timers_only_and_research_shape_held']=bprojects.keys()==aprojects.keys() and all(omit(v,{'days_left'})==omit(aprojects[i],{'days_left'}) and (q.scalars(aprojects[i]).get('days_left')==q.scalars(v)['days_left']-days if 'days_left' in q.scalars(v) else 'days_left' not in q.scalars(aprojects[i])) for i,v in bprojects.items()) and omit(bc['tech_status'],{'physics_queue','engineering_queue','stored_techpoints'})==omit(ac['tech_status'],{'physics_queue','engineering_queue','stored_techpoints'}) and {k:v for k,v in bp.items() if k!='progress'}=={k:v for k,v in ap.items() if k!='progress'} and {k:v for k,v in be.items() if k!='progress'}=={k:v for k,v in ae.items() if k!='progress'}
checks['all_mother_district_objects_and_science_workforce_held']=all(q.block(b['raw_roots']['districts'],str(i))==q.block(a['raw_roots']['districts'],str(i)) for i in ba['colonies']['0']['districts']) and all(sum(j['workforce'] for j in aa['pop_jobs'].values() if j['planet']==0 and j['type']==typ)==n for typ,n in [('calculator_physicist',780),('calculator_biologist',180),('calculator_engineer',180)])
checks['new_owned_fleets_contain_only_justified_added_ships']=all(set(q.ids(q.block(a['owned_fleets_raw'][str(i)],'ships')))<=added for i in set(a['owned_fleets'])-set(b['owned_fleets']))
checks['all_three_original_MIA_identities_dates_held']=all(q.scalars(q.block(a['owned_fleets_raw'][i],'properties')).get('mia')=='yes' and q.scalars(a['owned_fleets_raw'][i]).get('return_date')==date for i,date in [('2','2280.03.16'),('33555013','2280.01.03'),('33555278','2281.06.27')])
boundaries=[]
if sda and q.scalars(sda[0])['days']<=30:boundaries.append('original_native_storm1815_due_review')
if any(re.search(r'\bfleet\s*=',q.block(q.block(v,'combat'),'in_combat_with')) for v in a['owned_fleets_raw'].values()):boundaries.append('native_active_combat_review')
if ap.get('progress',0)>=6000-129.98954:boundaries.append('project2_completion_review')
if any(0<=ordinal(date)-ordinal(aa['date'])<=30 for date in ['2280.01.03','2280.03.16','2281.06.27']):boundaries.append('original_native_MIA_return_review')
passed=all(v is True for v in checks.values());out=run/(after+'-campaign-v3-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_TERRAVORE_NATIVE_CAMPAIGN_INTERVAL' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'days':days,'months':months,'research_ticks':ticks,'completed_paid_army_orders':completed,'new_paid_armies':army_births,'captured_existing_stations':captures,'native_reports':reports,'native_storm_notifications':storms,'cash_delta':{k:str(v) for k,v in deltas.items()},'boundaries':boundaries,'native_devour_calendar_ready':passed and not boundaries,'maximum_days_to_native_bite_boundary':30 if passed and not boundaries else 0,'scope':'Native paid recruitment and route campaign; no crisis/Queen/devour completion claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'captures':[x['ship'] for x in captures],'paid_births':len(new_armies),'boundaries':boundaries}),flush=True);assert passed
