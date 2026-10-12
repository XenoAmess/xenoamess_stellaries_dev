"""Read-only exact natural conquest, native transport recreation and reward ledger."""
import collections,json,logging,re,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-balthasar-landing-day-22801102';after='terravore-balthasar-conquest-day-22801103'
o=load(after+'-construction-boundary-observation-v4.json');b,a=o['before_state'],o['after_state'];ba,aa=b['audit'],a['audit'];bc,ac=ba['countries']['0'],aa['countries']['0']
pre=load(before+'-campaign-v17-proof.json');px=load(before+'-campaign-guard-v17-execution.json');review=load('terravore-balthasar-ground-endpoint-review-proof.json');rx=load('terravore-balthasar-ground-endpoint-review-execution.json')
roots=[]
for st in [before,after]:
 with zipfile.ZipFile(run/(st+'.sav')) as z:roots.append({k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x})
br,ar=roots;omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
def source_pops(rr):
 result=collections.Counter();records=[]
 for i in q.ids(q.block(q.block(rr['colony'],'30'),'pop_groups')):
  raw=q.block(rr['pop_groups'],str(i));s=q.scalars(raw);key=q.scalars(q.block(raw,'key'));result[key['species']]+=s['size'];records.append({'id':i,'species':key['species'],'size':s['size'],'category':key['category'],'raw':raw})
 return dict(result),records
bp,bpop=source_pops(br);ap,apop=source_pops(ar)
associations={50331728:117442177,33554574:67110450,33554634:16777910};paid=set(associations);transport_ids=set(associations.values())
armies_b=set(q.ids(q.block(b['country0_raw'],'owned_armies')));armies_a=set(q.ids(q.block(a['country0_raw'],'owned_armies')))
old_station=q.block(br['ships'],'33556087');new_station=q.block(ar['ships'],'33556087')
enemy_fleets=lambda rr:set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rr['country'],'1'),'fleets_manager'),'owned_fleets'))))
newtransports=[]
for army,ship in associations.items():
 raw=q.block(ar['ships'],str(ship));s=q.scalars(raw);arm=q.block(ar['army'],str(army));ars=q.scalars(arm)
 newtransports.append({'army':army,'ship':ship,'ship_raw':raw,'army_raw':arm,'valid':s['army']==army and s['fleet']==33555320 and s['construction_date']==aa['date'] and q.scalars(q.block(raw,'ship_design_implementation'))=={'design':117440603,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(raw,'coordinate'))['origin']==147 and all(s[k]==v for k,v in {'hitpoints':125,'max_hitpoints':125,'armor_hitpoints':225,'max_armor_hitpoints':225,'shield_hitpoints':320,'max_shield_hitpoints':320}.items()) and ars['ship']==ship and ars['owner']==0 and ars['species']==73 and ars['health']==ars['max_health']==330 and ars['morale']==200 and 'colony' not in ars and 'ground_combat' not in ars and omit(q.block(br['army'],str(army)),{'fleet_name','ship','targeting','colony','ground_combat','retreat_date'})==omit(arm,{'fleet_name','ship','targeting','colony','ground_combat','retreat_date'})})
msg=o['new_country0_messages_raw'];ms=q.scalars(msg[0]);mplanet=q.scalars(q.block(q.block(ar['planets'],'planet'),'7'));pold=q.scalars(q.block(q.block(br['planets'],'planet'),'1578'));pnew=q.scalars(q.block(q.block(ar['planets'],'planet'),'1578'))
jobs=lambda audit:sorted((i,j['type'],j['workforce'],j.get('max_workforce')) for i,j in audit['pop_jobs'].items() if j['planet']==0)
checks={
 'original29_PASS_actual0_same_SAV_prior':len(pre['checks'])==29 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==ba['save_sha256'],
 'independent_ground_review_source_actual0_held':all(v is True for v in review['checks'].values()) and rx['returncode']==0 and rx['helper_sha256']==h.sha256(Path(rx['command'][1])) and h.sha256(Path(review['source']))==h.sha256(run/review['preserved_source'])==review['source_sha256'],
 'exact_original_single_day_SAVs_and_calendar_observer_actual0':(ba['save_sha256'],aa['save_sha256'])==('59dc39d74aea96f20138b3e47ecbcdb667525c37e0a3e1a29b0d337064875f11','8e10a5a711d7cca62b9342754ca4c5795a9dabc48b2947a495f5a6306fa1d8b5') and ba['date']=='2280.11.02' and aa['date']=='2280.11.03' and all(v is True for v in o['checks'].values()) and all(load(after+n+'-execution.json')['returncode']==0 for n in ['-calendar','-boundary-observation-v4']) and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,ba),(after,aa)]),
 'original_target14_only_conquered_colony_added':bc['owned_colonies']==[0] and ac['owned_colonies']==[0,30] and pold['owner']==pold['controller']==1 and pnew['owner']==pnew['controller']==0 and all(pold[k]==pnew[k] for k in ['planet_class','planet_size','original_owner','colony']) and pnew['planet_size']==14,
 'source_population_per_species_conserved_native_purge_regrouping':bp==ap=={61:27,2:366} and all(v['category']=='purge' for v in apop) and a['species_population_by_colony']=={'0:73':12075,'30:61':27,'30:2':366} and b['species_population_by_colony']=={'0:73':12075},
 'mother_original35_capacity27_districts_all_science_jobs_population_held':mplanet['owner']==mplanet['controller']==0 and aa['planets']['7']['variables']==ba['planets']['7']['variables'] and aa['colonies']['0']['districts']==ba['colonies']['0']['districts'] and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27 and all(aa['districts'][str(i)]==ba['districts'][str(i)] for i in aa['colonies']['0']['districts']) and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']==12075 and jobs(ba)==jobs(aa) and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0,
 'EEP_Queen_government_AP_traditions_crisis_no_reward':all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis']) and ac['variables']['eep_c']==62 and ac['variables']['eep_stage']==ac['variables']['eep_crisis']==ac['variables']['eep_fleet_stage']==2,
 'all_cash_and_resources_held_only_native_conquest500_Menace':all(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))==(D(500) if k=='menace' else D(0)) for k in set(bc['effective_stockpile'])|set(ac['effective_stockpile'])) and bc['effective_stockpile']['menace']==1635 and ac['effective_stockpile']['menace']==2135,
 'true_research_banks_and_full_queues_held_no_tick':bc['research_stockpile']==ac['research_stockpile'] and bc['tech_status']==ac['tech_status'],
 'all_original_owned_ships_designs_alive_no_removal_or_revival':set(b['owned_ship_ids'])<=set(a['owned_ship_ids']) and all(q.block(raw,'ship_design_implementation')==q.block(a['owned_ships_raw'][i],'ship_design_implementation') and q.scalars(a['owned_ships_raw'][i]).get('hitpoints',0)>0 for i,raw in b['owned_ships_raw'].items()) and not set(a['owned_ship_ids'])&{1807,1895,1896,67110639,16779140,100664961,50333234,16777713},
 'only_three_original_army_transport_recreations_and_preexisting_station_added':set(a['owned_ship_ids'])-set(b['owned_ship_ids'])==transport_ids|{33556087} and set(a['owned_fleets'])-set(b['owned_fleets'])=={33555320,673} and set(b['owned_fleets'])<=set(a['owned_fleets']) and all(v['valid'] for v in newtransports) and set(q.ids(q.block(a['owned_fleets_raw']['33555320'],'ships')))==transport_ids,
 'original_captured147_station_old_identity_design_birth':673 in enemy_fleets(br) and 673 not in enemy_fleets(ar) and q.ids(q.block(a['owned_fleets_raw']['673'],'ships'))==[33556087] and q.scalars(old_station)['construction_date']==q.scalars(new_station)['construction_date']=='2247.08.24' and q.block(old_station,'ship_design_implementation')==q.block(new_station,'ship_design_implementation'),
 'all15_original_armies_no_new_armies_or_losses':armies_b==armies_a and len(armies_a)==15 and all(q.block(br['army'],str(i))==q.block(ar['army'],str(i)) for i in armies_b-paid) and all(v['valid'] for v in newtransports),
 'native_ground_combat_removed_unique_victory293_no_pending':[(v,x) for k,v,x in q.fields(ar['ground_combat']) if k=='150994944']==[('none',False)] and len(msg)==1 and ms['type']=='INVASION_ATTACKER_WIN' and ms['notification']==293 and ms['date']==aa['date'] and q.scalars(q.block(msg[0],'coordinate'))['origin']==147 and not a['pending_country0_raw'],
 'original_seven_minerals_naval133_recorded_away_fees_held':ac['native']['used_naval_capacity']==bc['native']['used_naval_capacity']==133 and len(q.ids(q.block(a['owned_fleets_raw']['50332250'],'ships')))==7 and ac['budget_categories']['current_month']['expenses']['ships']==bc['budget_categories']['current_month']['expenses']['ships'] and ac['budget_categories']['current_month']['expenses']['ship_components']==bc['budget_categories']['current_month']['expenses']['ship_components'],
 'production41_CN_full_error_exact_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(after+'-conquest-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_PAID_THREE_ARMY_CONQUEST' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'source_population_before':bpop,'source_population_after':apop,'original_army_new_native_transports':newtransports,'native_conquest_Menace':500,'original_victory_message':msg,'boundaries':['new_conquered_source_devour_or_purge_phase'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Exact conquest endpoint only; no devour, Queen C200, further crisis or full route acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
