"""Read-only second paid shipyard completion, four real corvettes, native district loss and sole contact."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def queue(rt,i):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),str(i))
def items(rt):return {k:v for k,v,o in q.fields(q.block(q.block(rt['construction'],'item_mgr'),'items')) if o}
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];pre=json.loads((run/(before+'-first-maintenance-proof.json')).read_text('utf-8'));receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
bs,ass=[q.block(q.block(rt['starbase_mgr'],'starbases'),'0') for rt in [br,ar]];bq,aq=queue(br,3),queue(ar,3);bids,aids=[q.ids(q.block(t,'items')) for t in [bq,aq]];bi,ai=items(br),items(ar)
ship_ids=[16777221,16778303,16778412,1564];ships=[q.block(ar['ships'],str(i)) for i in ship_ids];fleet=q.block(ar['fleet'],'16777797');core=a['planets']['7'];growthraw=q.block(q.block(ar['colony'],'0'),'last_month_growth_data');growth=q.scalars(q.block(growthraw,'growth_and_size'))
pending=[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0];nets={k:sum(v.get(k,0) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys','trade']}
checks={
 'bound_actual_prior37_maintenance_PASS':pre['status']=='PASS_NATIVE_TERRAVORE_FIRST_CORVETTE_MAINTENANCE_COMPONENT' and len(pre['checks'])==37 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual167_days_native_receipt':b['date']=='2236.06.02' and a['date']=='2236.11.19' and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==167 and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'unfiltered_error_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'all_EEP_ledger_and_country_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'C37_G0_D11_made0_worlds2':all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'unique_owned_core_capacity11_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']==b['planets']['7']['variables'] and core['variables']['eep_capacity_value']==11,
 'original_core_modifiers_and_deposit_held':core['modifiers']==b['planets']['7']['modifiers'] and core['modifiers'].count('modifier="eep_capacity"')==1 and [(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'both_sources_unowned_shattered_no_pop':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned_and_no_active_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'AP_traditions_government_held':all(bc[k]==ac[k] for k in ['ascension_perks','traditions','government']),
 'native_module_paid_order_completed':q.ids(q.block(queue(br,2),'items'))==[704643077] and not q.ids(q.block(queue(ar,2),'items')) and omit(queue(br,2),['items'])==omit(queue(ar,2),['items']),
 'actual_slot1_solar_to_second_shipyard_only':q.scalars(q.block(bs,'modules'))=={'0':'shipyard','1':'solar_panel_network'} and q.scalars(q.block(ass,'modules'))=={'0':'shipyard','1':'shipyard'} and omit(bs,['modules'])==omit(ass,['modules']),
 'ship_queue_capacity1_to2_other_metadata_held':q.scalars(bq)['simultaneous']==1 and q.scalars(aq)['simultaneous']==2 and omit(bq,['items','simultaneous'])==omit(aq,['items','simultaneous']),
 'exact_three_original_paid_orders_removed_only':len(bids)==19 and bids[:3]==[503316491,117440527,822083587] and aids==bids[3:] and len(aids)==16,
 'remaining_front_native45_of60_other15_raw_held':aids[0]==671088646 and q.scalars(ai[str(aids[0])])=={'queue':3,'paying_country':0,'progress':45,'progress_needed':60} and omit(bi[str(aids[0])],['progress'])==omit(ai[str(aids[0])],['progress']) and all(bi[str(i)]==ai[str(i)] for i in aids[1:]),
 'old_owned_fleet_set_held_and_actual_four_ships':owned(br)==owned(ar) and q.ids(q.block(fleet,'ships'))==ship_ids and q.scalars(fleet)['ship_class']=='shipclass_military',
 'new_three_actual_construction_dates':[(q.scalars(t)['construction_date'],q.scalars(t)['fleet']) for t in ships[1:]]==[('2236.07.07',16777797),('2236.08.25',16777797),('2236.10.13',16777797)],
 'all_four_original_paid_corvette_design_full_hull':all(q.scalars(q.block(t,'ship_design_implementation'))['design']==67110548 and q.scalars(t)['hitpoints']==q.scalars(t)['max_hitpoints']==250 for t in ships),
 'old_two_upgrade_markers_only_real_design_held':[(q.scalars(q.block(t,'ship_design_implementation'))['upgrade']) for t in ships]==[134219419,134219419,4294967295,4294967295] and 'required_component="HYPER_DRIVE_2"' in q.block(ar['ship_design'],'134219419'),
 'actual_naval_size20_and_power334_0625':q.scalars(q.block(ar['country'],'0'))['fleet_size']==20 and q.scalars(fleet)['military_power']==334.0625,
 'four_corvettes_actual_monthly_maintenance7_energy1_5_alloys':ac['budget_categories']['current_month']['expenses']['ships']=={'energy':7,'alloys':1.5},
 'all_primary_stocks_positive_and_increased':all(ac['effective_stockpile'][k]>bc['effective_stockpile'][k]>0 for k in nets),
 'final_current_month_primary_nets_nonnegative':all(v>=0 for v in nets.values()),
 'observed_population_delta30_and_last_month_birth6':b['colonies']['0']['actual_pop_sum']==8900 and a['colonies']['0']['actual_pop_sum']==8930 and growth=={'month_start_size':8924,'growth':6} and list(q.fields(q.block(growthraw,'current_month_growth_details')))==[('key','"GROWTH_CAT_GROWTH"',False),('value','6',False),('key','"GROWTH_CAT_PROMOTION"',False),('value','0',False)],
 'only_actual_generator_district4_to3':b['districts']['2']['level']==4 and a['districts']['2']['level']==3 and {k:v for k,v in b['districts']['2'].items() if k!='level'}=={k:v for k,v in a['districts']['2'].items() if k!='level'} and {k:v for k,v in b['districts'].items() if k!='2'}=={k:v for k,v in a['districts'].items() if k!='2'},
 'unique_new_native_ruined_district_on_mother':set(a['deposits'])-set(b['deposits'])=={'33554567'} and a['deposits']['33554567']=={'type':'d_ruined_district','deposit_holder':{'type':0,'id':7}} and all(v==a['deposits'].get(k) for k,v in b['deposits'].items()),
 'mining2000_generator600_now_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',600)]),
 'Theory_selected_growing_special_points_held':all('tech_psionic_theory' not in c['completed_technologies'] and q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])['technology']=='tech_psionic_theory' for c in [bc,ac]) and q.scalars(q.block(ac['tech_status'],'society_queue').strip()[1:-1])['progress']>q.scalars(q.block(bc['tech_status'],'society_queue').strip()[1:-1])['progress'] and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'only_two_observed_native_other_technologies_complete':set(ac['completed_technologies'])-set(bc['completed_technologies'])=={'tech_hyper_drive_2','tech_orbital_arc_furnace'},
 'true_research_banks_and_species_binding_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints') and b['species']==a['species'] and b['event_targets']==a['event_targets'],
 'only_known_native_first_contact118_pending':len(pending)==1 and q.scalars(pending[0])=={'id':118,'event':'first_contact.1','date':'2239.02.11','country':0} and q.scalars(q.block(pending[0],'scope'))['type']=='first_contact' and q.scalars(q.block(pending[0],'scope'))['id']==32,
 'native_contact32_bound_country14_and_event118':q.scalars(contact:=q.block(q.block(ar['first_contacts'],'contacts'),'32'))['owner']==0 and q.scalars(contact)['country']==14 and q.scalars(q.block(contact,'event'))['player_event']==118,
 'enemy_still_bombarding_not_defense_success':core['ground_support_stance']=='voidworm_invasion' and core['last_bombardment']==a['date'] and core['bombardment_damage']==15.34338 and q.ids(q.block(q.block(ar['fleet'],'18'),'ships'))==[44],
}
p={'status':'PASS_NATIVE_TERRAVORE_SECOND_SHIPYARD_COMPLETION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'remaining_paid_order_ids':aids,'actual_own_corvettes':ship_ids,'native_ship_queue_capacity':2,'population':8930,'current_month_nets':nets,'sole_pending_native_event':118,'scope':'Paid second module completed,4 actual paid corvettes,16 original orders remain. Native generator district loss documented. Sole native contact118 still requires normal ACK before calendar. No full interval budget reconstruction, active parallel progress, defense victory or full-route claim.'}
out=run/(after+'-second-shipyard-completion-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original module completion FAIL retained; no next GUI/calendar'
