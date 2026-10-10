"""Read-only bounded defense calendar validation; no victory or full-route claim."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.path.insert(0,'_runtime/heart-of-devouring');sys.argv=['runtime']
import runtime as r,audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
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
def owned(rt):return [int(x) for x in re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(rt['country'],'0'),'fleets_manager'),'owned_fleets'))]
def ordinal(d):
 y,m,day=map(int,d.split('.'));return y*360+(m-1)*30+day-1
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'));days=receipt['days'];validate_native_interval(b['date'],a['date'],days)
pre=json.loads((run/receipt['prior_proof_file']).read_text('utf-8'));ex=json.loads((run/(receipt['prior_execution_stage']+'-execution.json')).read_text('utf-8'))
bids,aids=[q.ids(q.block(queue(rt,3),'items')) for rt in [br,ar]];bi,ai=items(br),items(ar)
bs,ass=[q.ids(q.block(q.block(rt['fleet'],'16777797'),'ships')) for rt in [br,ar]];new=[i for i in ass if i not in bs];removed=len(bids)-len(aids)
progress=lambda c:q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])
gov=lambda c:omit(c['government'],{'council_agenda_progress','council_agenda_cooldowns'})
core=a['planets']['7'];nets={k:sum(v.get(k,0) for v in ac['budget_categories']['current_month']['balance'].values()) for k in ['energy','minerals','unity','alloys','trade']}
growthraw=q.block(q.block(ar['colony'],'0'),'last_month_growth_data')
checks={
 'bound_prior_actual_PASS_and_execution_zero':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_native_date_receipt_and_execution_zero':1<=days<=180 and receipt['status']=='CALENDAR_CONFIRMED' and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'original20_paid_batch_conserved':len(bs)+len(bids)==len(ass)+len(aids)==20 and 0<=removed and len(new)==removed and set(bs)<=set(ass),
 'only_contiguous_paid_front_orders_complete':aids==bids[removed:] and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'}) and 0<=q.scalars(ai[str(i)])['progress']<60 and q.scalars(ai[str(i)])['progress']>=q.scalars(bi[str(i)])['progress'] for i in aids),
 'ship_queue_capacity2_native_metadata_held':q.scalars(queue(ar,3))['simultaneous']==2 and omit(queue(br,3),{'items'})==omit(queue(ar,3),{'items'}),
 'actual_two_paid_shipyards_crew_quarters_held':omit(q.block(q.block(br['starbase_mgr'],'starbases'),'0'),{'update_flag'})==omit(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),{'update_flag'}) and q.scalars(q.block(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),'modules'))=={'0':'shipyard','1':'shipyard'},
 'real_old_ships_design_dates_full_hull_fleet_held':all(all(q.scalars(s:=q.block(br['ships'],str(i)))[k]==q.scalars(t:=q.block(ar['ships'],str(i)))[k] for k in ['construction_date','fleet','hitpoints','max_hitpoints']) and q.scalars(t)['hitpoints']==250 and q.block(s,'ship_design_implementation')==q.block(t,'ship_design_implementation') for i in bs),
 'real_new_ships_original_design_full_hull_owned_in_date_interval':all(q.scalars(s:=q.block(ar['ships'],str(i)))['fleet']==16777797 and q.scalars(s)['hitpoints']==q.scalars(s)['max_hitpoints']==250 and q.scalars(q.block(s,'ship_design_implementation'))['design']==67110548 and ordinal(b['date'])<ordinal(q.scalars(s)['construction_date'])<=ordinal(a['date']) for i in new),
 'same_native_owned_fleet_set_and_naval_size':owned(br)==owned(ar) and 16777797 in owned(ar) and q.scalars(q.block(ar['country'],'0'))['fleet_size']==5*len(ass),
 'EEP_ledger_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'unique_owned_core_capacity11_and_original_modifiers':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']==b['planets']['7']['variables'] and core['variables']['eep_capacity_value']==11 and core['modifiers']==b['planets']['7']['modifiers'],
 'both_sources_unowned_shattered_no_population':all(a['planets'][i].get('owner') is None and a['planets'][i].get('controller') is None and a['planets'][i]['planet_class']=='pc_shattered' and not a['planets'][i]['deposits'] for i in ['90','124']) and not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned_and_no_new_EEP_task':bc['owned_colonies']==ac['owned_colonies']==[0] and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'government_core_AP_traditions_held':gov(bc)==gov(ac) and bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'Theory_selected_not_regressed_no_completion_claim':all('tech_psionic_theory' not in c['completed_technologies'] and progress(c)['technology']=='tech_psionic_theory' for c in [bc,ac]) and progress(ac)['progress']>=progress(bc)['progress'],
 'true_bank_and_special650_former607_25288_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints') and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'all_primary_actual_stocks_positive':all(ac['effective_stockpile'][k]>0 for k in nets),
 'actual_mother_population_positive_no_disappearance':a['colonies']['0']['actual_pop_sum']>0 and all(p['size']>=0 for p in a['pop_groups'].values()),
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
if days==1 and b['date'][:7]==a['date'][:7]:
 for k in ['effective_stockpile','budget_categories']:checks['one_day_'+k+'_held']=bc[k]==ac[k]
 for k in ['pop_jobs','districts','deposits']:checks['one_day_'+k+'_held']=b[k]==a[k]
 checks['one_day_pop_groups_identity_size_growth_held']={i:{k:v for k,v in p.items() if k not in {'power','crime','housing_usage'}} for i,p in b['pop_groups'].items()}=={i:{k:v for k,v in p.items() if k not in {'power','crime','housing_usage'}} for i,p in a['pop_groups'].items()}
 checks['one_day_population_held']=a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']
for k in ['species','event_targets']:checks[k+'_held']=b[k]==a[k]

if after=='terravore-defense-december-research-update':
 old=json.loads((run/(after+'-defense-boundary-proof.json')).read_text('utf-8'))
 checks['original30_two_FAIL_and_actual_exit1_retained']=old['status']=='FAIL' and len(old['checks'])==30 and [k for k,v in old['checks'].items() if not v]==['actual_two_paid_shipyards_crew_quarters_held','one_day_pop_groups_held'] and sum(v is True for v in old['checks'].values())==28 and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'] and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==1
 checks['exact_only_native_starbase_flag_added2048']=not any(k=='update_flag' for k,v,o in q.fields(q.block(q.block(br['starbase_mgr'],'starbases'),'0'))) and q.scalars(q.block(q.block(ar['starbase_mgr'],'starbases'),'0'))['update_flag']==2048
 checks['exact_native_pop_group1_three_cached_values_only']=b['pop_groups']['1']['size']==a['pop_groups']['1']['size']==3543 and {k:(b['pop_groups']['1'].get(k),a['pop_groups']['1'].get(k)) for k in b['pop_groups']['1'] if b['pop_groups']['1'].get(k)!=a['pop_groups']['1'].get(k)}=={'power':(35.38,35.43),'crime':(35.38,35.43),'housing_usage':(3538,3543)} and {k:v for k,v in b['pop_groups'].items() if k!='1'}=={k:v for k,v in a['pop_groups'].items() if k!='1'}

enemy=q.block(ar['fleet'],'18');enemy_ships=q.ids(q.block(enemy,'ships'))
p={'status':'PASS_NATIVE_TERRAVORE_DEFENSE_BOUNDARY_V2_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'days':days,'actual_ships':ass,'new_real_ships':new,'remaining_paid_orders':aids,'front_order_progress':[q.scalars(ai[str(i)])['progress'] for i in aids[:2]],'own_military_power':q.scalars(q.block(ar['fleet'],'16777797'))['military_power'],'population_before':b['colonies']['0']['actual_pop_sum'],'population_after':a['colonies']['0']['actual_pop_sum'],'last_month_growth_raw':growthraw,'native_bombardment_damage':core['bombardment_damage'],'actual_districts':a['districts'],'new_deposits':{k:v for k,v in a['deposits'].items() if k not in b['deposits']},'Theory_queue_before':progress(bc),'Theory_queue_after':progress(ac),'current_month_nets':nets,'energy_reserve_months_if_negative':None if nets['energy']>=0 else ac['effective_stockpile']['energy']/-nets['energy'],'actual_stocks':ac['effective_stockpile'],'native_pop_cache_changes':{i:{k:[p.get(k),a['pop_groups'].get(i,{}).get(k)] for k in ['power','crime','housing_usage'] if p.get(k)!=a['pop_groups'].get(i,{}).get(k)} for i,p in b['pop_groups'].items() if p!=a['pop_groups'].get(i)},'enemy_fleet18_ships':enemy_ships,'scope':'Bounded native defense construction interval, paid batch conserved; native population/district/budget changes reported. Multiple-month final budget is not whole-period accounting. No defense victory, full Shroud or full-route acceptance.'}
out=run/(after+'-defense-boundary-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original defense boundary FAIL retained; no next calendar'
