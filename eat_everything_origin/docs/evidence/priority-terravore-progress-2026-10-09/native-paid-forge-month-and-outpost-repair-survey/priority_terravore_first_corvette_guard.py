"""Read-only actual paid first corvette completion, 18 native days, invasion still active."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stage):
 a=json.loads((run/(stage+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 return a,fs,roots
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
def queue(rt):
 c=rt['construction'];queue=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'3')
 return q.ids(q.block(queue,'items')),{k:(v,o) for k,v,o in q.fields(q.block(q.block(c,'item_mgr'),'items'))}
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-defense-first-month-proof.json')).read_text('utf-8'))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
bids,bi=queue(br);aids,ai=queue(ar);bo,ao=owned(br),owned(ar)
fleet=q.block(ar['fleet'],'16777797');ship=q.block(ar['ships'],'16777221');ds=q.block(ar['ship_design'],'67110548')
pending=lambda fs:[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
bites=lambda fs:[v for k,v,o in fs if k=='message' and o and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD']
core=a['planets']['7'];source_ids=['90','124'];theory=lambda c:q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])
pgb,pga=b['pop_groups']['1'],a['pop_groups']['1'];cached=['power','crime','housing_usage']
checks={
 'bound_actual_prior31_PASS':pre['status']=='PASS_NATIVE_TERRAVORE_DEFENSE_FIRST_MONTH_COMPONENT' and len(pre['checks'])==31 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual18_native_days_and_receipt':b['date']=='2236.05.01' and a['date']=='2236.05.19' and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and receipt['days']==18,
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'no_pending_or_repeat_Queen_notice':not pending(bf) and not pending(af),
 'no_new_native_bite_message':bites(bf)==bites(af),
 'all_EEP_ledger_and_country_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'C37_G0_D11_made0_worlds2':all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'no_new_active_task':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'only_mother_owned':bc['owned_colonies']==ac['owned_colonies']==[0],
 'both_sources_unowned_shattered_without_deposits':all(a['planets'][pid].get('owner') is None and a['planets'][pid].get('controller') is None and a['planets'][pid]['planet_class']=='pc_shattered' and not a['planets'][pid]['deposits'] for pid in source_ids),
 'no_actual_population_at_sources':not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'original_AP_traditions_government_held':all(bc[k]==ac[k] for k in ['ascension_perks','traditions','government']),
 'unique_core_capacity11_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']==b['planets']['7']['variables'] and core['variables']['eep_capacity_value']==11,
 'core_permanent_modifiers_and_deposit_held':core['modifiers']==b['planets']['7']['modifiers'] and core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*11\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])) and [(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'actual_population8894_held':b['colonies']['0']['actual_pop_sum']==a['colonies']['0']['actual_pop_sum']==8894 and b['colonies']['0']['pop_groups']==a['colonies']['0']['pop_groups'],
 'only_exact_prior_birth6_population_cache_refresh':{k:v for k,v in pgb.items() if k not in cached}=={k:v for k,v in pga.items() if k not in cached} and [pgb[k] for k in cached]==[32.96,32.96,3296] and [pga[k] for k in cached]==[33.02,33.02,3302] and {k:v for k,v in b['pop_groups'].items() if k!='1'}=={k:v for k,v in a['pop_groups'].items() if k!='1'},
 'all_jobs_and_districts_held':b['pop_jobs']==a['pop_jobs'] and b['districts']==a['districts'] and b['colonies']['0']['districts']==a['colonies']['0']['districts'],
 'mother_mining2000_generator800_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)]),
 'all_effective_stocks_and_budget_categories_held':bc['effective_stockpile']==ac['effective_stockpile'] and bc['budget_categories']==ac['budget_categories'],
 'true_research_banks_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints'),
 'Theory_selected_growing_not_completed':all(theory(c)['technology']=='tech_psionic_theory' and 'tech_psionic_theory' not in c['completed_technologies'] for c in [bc,ac]) and theory(ac)['progress']>theory(bc)['progress'],
 'specialized650_and_former607_25288_held':bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'source_species_and_event_binding_held':a['species']==b['species'] and a['event_targets']==b['event_targets'],
 'exact_first_paid_order_completed_other19_held':len(bids)==20 and bids[0]==687865861 and aids==bids[1:] and ai['687865861']==('none',False) and all(bi[str(i)]==ai[str(i)] for i in aids),
 'prior_work37_5_and18_at1_25_equal_base60':q.scalars(bi['687865861'][0])=={'queue':3,'paying_country':0,'progress':37.5,'progress_needed':60} and 37.5+18*1.25==60,
 'only_new_own_fleet16777797_old_owned_order_held':ao==bo+[16777797] and q.ids(q.block(fleet,'ships'))==[16777221] and q.scalars(fleet)['ship_class']=='shipclass_military',
 'new_actual_ship_design_and_construction_date':q.scalars(ship)['fleet']==16777797 and q.scalars(ship)['construction_date']==a['date'] and q.scalars(q.block(ship,'ship_design_implementation'))=={'design':67110548,'upgrade':4294967295,'growth_stage':0} and bool(re.search(r'ship_size="corvette"',ds)),
 'new_ship_at_own_shipyard_system0_idle':q.scalars(q.block(q.block(q.block(fleet,'movement_manager'),'orbit'),'orbitable'))=={'starbase':0} and q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate'))['origin']==0 and q.scalars(q.block(fleet,'movement_manager'))['state']=='move_idle' and not q.block(fleet,'orders'),
 'new_ship_full_hull250_armor250_shield160':all(q.scalars(ship)[k]==v for k,v in {'hitpoints':250,'max_hitpoints':250,'armor_hitpoints':250,'max_armor_hitpoints':250,'shield_hitpoints':160,'max_shield_hitpoints':160}.items()),
 'native_used_naval_size0_to5':q.scalars(q.block(br['country'],'0'))['used_naval_capacity']==0 and q.scalars(q.block(ar['country'],'0'))['used_naval_capacity']==q.scalars(q.block(ar['country'],'0'))['fleet_size']==5,
 'enemy44_still_bombarding_actual_mother':q.ids(q.block(q.block(ar['fleet'],'18'),'ships'))==[44] and q.scalars(q.block(q.block(q.block(q.block(ar['fleet'],'18'),'movement_manager'),'orbit'),'orbitable'))=={'planet':7} and core['last_bombardment']==a['date'] and core['ground_support_stance']=='voidworm_invasion' and core['bombardment_damage']==3.54078,
}
p={'status':'PASS_NATIVE_TERRAVORE_FIRST_PAID_CORVETTE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'completed_paid_item':687865861,'remaining_paid_queue':aids,'new_own_fleet':16777797,'new_own_ship':16777221,'military_power':q.scalars(fleet)['military_power'],'Theory_queue_before':theory(bc),'Theory_queue_after':theory(ac),'population':8894,'mother_bombardment_damage':core['bombardment_damage'],'station_ship0_actual_hitpoints':{k:v for k,v in q.scalars(q.block(ar['ships'],'0')).items() if 'hitpoints' in k},'scope':'Only first normal paid corvette completion after18 native days,19 paid orders still unstarted. Active invasion, no defense victory, completed20-fleet or crisis/full-route claim.'}
out=run/(after+'-first-corvette-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original first corvette FAIL retained; no next GUI/calendar'
