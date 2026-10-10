"""Read-only first completed corvette maintenance month, existing13-day recovery after target error."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)

b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
def extra(stem):
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o};col=q.block(roots['colony'],'0')
 return [q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0],[v for k,v,o in fs if k=='message' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD'],q.block(col,'last_month_growth_data')
bp,bm,bg=extra(before);ap,am,ag=extra(after);growth=q.scalars(q.block(ag,'growth_and_size'))
resources=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence'];residual={};net={}
for k in resources:
 net[k]=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
 residual[k]=D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))-net[k]
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text(encoding='utf-8'));core=a['planets']['7'];source=a['planets']['90']
residual['influence']=D(str(ac['effective_stockpile'].get('influence',0)))-min(D(1000),D(str(bc['effective_stockpile'].get('influence',0)))+net['influence'])
pre=json.loads((run/(before+'-second-shipyard-payment-proof.json')).read_text('utf-8'))
checks={'actual13_days_date_and_recovered_receipt':b['date']=='2236.05.19' and a['date']=='2236.06.02' and receipt['status']=='CALENDAR_CONFIRMED_EXISTING_COMMAND_AFTER_TARGET_FAILURE' and receipt['days']==13 and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_pending_or_repeat_Queen_notice':not bp and not ap,
 'all_EEP_ledger_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'C37_G0_D11_made0_worlds2':all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'no_new_bite_message':bm==am,
 'no_new_active_task':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'source_still_unowned_shattered':all(a['planets'][pid].get('owner') is None and a['planets'][pid].get('controller') is None and a['planets'][pid]['planet_class']=='pc_shattered' and not a['planets'][pid]['deposits'] for pid in ['90','124']),
 'source_no_actual_population':not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned':bc['owned_colonies']==ac['owned_colonies']==[0],
 'native_month_growth_exact_population_change':growth['month_start_size']==b['colonies']['0']['actual_pop_sum'] and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+growth['growth'],
 'all_eight_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'original_AP_and_traditions_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'unique_core_owned_capacity11_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11,
 'one_permanent_capacity11':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*11\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
 'court_and_original_deposit_held':core['modifiers'].count('modifier="eep_court"')==1 and [(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'mother_actual_districts_held':a['colonies']['0']['districts']==b['colonies']['0']['districts'] and all(a['districts'][str(i)]==b['districts'][str(i)] for i in b['colonies']['0']['districts']),
 'source_species_and_binding_held':a['species']==b['species'] and a['event_targets']==b['event_targets'],
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()}
checks.update({
 'bound_actual_second_shipyard_payment40_PASS':pre['status']=='PASS_NATIVE_TERRAVORE_SECOND_SHIPYARD_PAYMENT_COMPONENT' and len(pre['checks'])==40 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'independent_last_month_equals_prior_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'true_research_banks_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints'),
 'mother_mining2000_generator800_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)]),
})
def queues(s):
 with zipfile.ZipFile(run/(s+'.sav')) as z:roots={k:v for k,v,o in q.fields(z.read('gamestate').decode('utf-8-sig')) if o}
 cons=roots['construction'];queue=q.block(q.block(q.block(cons,'queue_mgr'),'queues'),'3');ids=q.ids(q.block(queue,'items'));items={k:v for k,v,o in q.fields(q.block(q.block(cons,'item_mgr'),'items')) if o}
 return ids,items,roots
bids,bi,br=queues(before);aids,ai,ar=queues(after)
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
checks.update({
 'all19_paid_order_ids_held':bids==aids and len(aids)==19,
 'first_native_work_only0_to16_25_of60':q.scalars(bi[str(bids[0])])=={'queue':3,'paying_country':0,'progress':0,'progress_needed':60} and q.scalars(ai[str(aids[0])])=={'queue':3,'paying_country':0,'progress':16.25,'progress_needed':60} and omit(bi[str(bids[0])],['progress'])==omit(ai[str(aids[0])],['progress']),
 'all_other18_orders_complete_raw_held':all(bi[str(i)]==ai[str(i)] for i in bids[1:]),
 'only_birth6_no_native_population_loss_this_month':growth=={'month_start_size':8894,'growth':6} and list(q.fields(q.block(ag,'current_month_growth_details')))==[('key','"GROWTH_CAT_GROWTH"',False),('value','6',False),('key','"GROWTH_CAT_PROMOTION"',False),('value','0',False)],
 'single_own_military_naval_size5_held':q.scalars(q.block(br['country'],'0'))['fleet_size']==q.scalars(q.block(ar['country'],'0'))['fleet_size']==5,
 'Theory_still_selected_and_growing':all('tech_psionic_theory' not in c['completed_technologies'] and q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1])['technology']=='tech_psionic_theory' for c in [bc,ac]) and q.scalars(q.block(ac['tech_status'],'society_queue').strip()[1:-1])['progress']>q.scalars(q.block(bc['tech_status'],'society_queue').strip()[1:-1])['progress'],
 'specialized650_and_former607_25288_held':bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'mineral_energy_unity_net_nonnegative':all(net[k]>=0 for k in ['minerals','energy','unity']),
})

checks.update({
 'original_target_failure_preserved_actual_exit1':json.loads((run/'terravore-defense-first-maintenance-month-observe-execution.json').read_text('utf-8'))['returncode']==1 and receipt['original_expected_date']=='2236.06.01',
 'independent_recovery_actual_exit0_and_SHA_pair':json.loads((run/'terravore-defense-first-maintenance-recovery-execution.json').read_text('utf-8'))['returncode']==0 and (recovery:=json.loads((run/(after+'-recovery-observation.json')).read_text('utf-8')))['before_sha256']==b['save_sha256'] and recovery['after_sha256']==a['save_sha256'] and recovery['new_error_bytes']==0,
 'module_original0_to13_of180_only':q.scalars(bi['704643077'])=={'queue':2,'paying_country':0,'progress':0,'progress_needed':180} and q.scalars(ai['704643077'])=={'queue':2,'paying_country':0,'progress':13,'progress_needed':180} and omit(bi['704643077'],['progress'])==omit(ai['704643077'],['progress']),
 'original_paid_module_queue2_ID_held':q.ids(q.block(q.block(q.block(q.block(br['construction'],'queue_mgr'),'queues'),'2'),'items'))==[704643077] and q.ids(q.block(q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'2'),'items'))==[704643077],
 'actual_ships_maintenance4_to4_75_energy_and0_375_alloys':bc['budget_categories']['current_month']['expenses']['ships']=={'energy':4} and ac['budget_categories']['current_month']['expenses']['ships']=={'energy':4.75,'alloys':0.375} and ac['budget_categories']['current_month']['balance']['ships']=={'energy':-4.75,'alloys':-0.375},
 'original_actual_corvette_alive_same_design_fleet':q.scalars(q.block(ar['ships'],'16777221'))['fleet']==16777797 and q.scalars(q.block(q.block(ar['ships'],'16777221'),'ship_design_implementation'))['design']==67110548 and q.ids(q.block(q.block(ar['fleet'],'16777797'),'ships'))==[16777221],
})

p={'status':'PASS_NATIVE_TERRAVORE_FIRST_CORVETTE_MAINTENANCE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_native_growth':growth,'budget_residuals':{k:str(v) for k,v in residual.items()},'actual_current_month_net':{k:str(v) for k,v in net.items()},'stockpile':ac['effective_stockpile'],'newly_completed_technologies':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),'scope':'Actual existing13-day interval toJune2 after original wrong-target failure, no calendar replay. First existing corvette maintenance, module13/180 and first remaining order16.25/60. Original failure retained; no defense or full-route success.'}
out=run/(after+'-first-maintenance-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original first maintenance FAIL retained; no next calendar'
