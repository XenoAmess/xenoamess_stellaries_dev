"""Read-only second Terravore adjacent-day settlement; native rewards independently counted."""
import json,logging,re,shutil,sys
from decimal import Decimal as D,ROUND_HALF_UP
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'));a=json.loads((run/(after+'.audit.json')).read_text('utf-8'))
bc,ac=b['countries']['0'],a['countries']['0'];source=a['planets']['124'];core=a['planets']['7']
obs=json.loads((run/(after+'-second-boundary-observation.json')).read_text('utf-8'))
pre=json.loads((run/(before+'-second-threshold-budget-supplement.json')).read_text('utf-8'))
bm,am=obs['before_native_bite_messages'],obs['after_native_bite_messages']
new=[v for v in am if v not in bm];msgs=[q.scalars(v) for v in new]
prefix='MESSAGE_TERRAVORE_CONSUME_WORLD_';kinds=[v.get('localization') for v in msgs]
popn=kinds.count(prefix+'POP_TEXT');alloyn=kinds.count(prefix+'ALLOYS_TEXT');minn=kinds.count(prefix+'MINERALS_TEXT')
returned=b['colonies']['24']['actual_pop_sum']+100*popn
expected=dict(bc['variables']);expected.update(eep_c=37,eep_g=0,eep_d=11,eep_worlds=2,eep_previous_capacity=6,eep_last_capacity=5,eep_last_return=returned,eep_entitled=0,eep_delta=0)
gross=lambda res:sum((D(str(v.get(res,0))) for v in bc['budget_categories']['current_month']['income'].values()),D(0))
reward=lambda mult,res:max(D(100),min(D(1000),gross(res)*mult)).to_integral_value(rounding=ROUND_HALF_UP)
expected_minerals=(minn-1)*reward(5,'minerals')+reward(3,'minerals')
expected_alloys=alloyn*reward(3,'alloys')
before_deposits=[b['deposits'][str(i)]['type'] for i in b['planets']['124']['deposits']]
steps={'eep_bites_done','eep_credit_done','eep_return_done','eep_population_done','eep_crisis_done','eep_destroy_done'}
checks={
 'bound_original_threshold_budget9_PASS':pre['status']=='PASS_NATIVE_TERRAVORE_SECOND_THRESHOLD_BUDGET_SUPPLEMENT' and len(pre['checks'])==9 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'actual_adjacent_day_and_receipt':b['date']=='2233.07.01' and a['date']=='2233.07.02' and obs['status']=='OBSERVED_NATIVE_TERRAVORE_BOUNDARY' and all(obs['checks'].values()) and obs['before_sha256']==b['save_sha256'] and obs['after_sha256']==a['save_sha256'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'before_progress48_uncredited':b['situations']['16777227']['progress']==48 and bc['variables']['eep_worlds']==1 and b['planets']['124']['owner']==0,
 'prior_annual_message_raw_held_not_recounted':len(bm)==1 and am==bm+new and q.scalars(bm[0])['date']=='2233.07.01' and q.scalars(bm[0])['localization']==prefix+'ALLOYS_TEXT',
 'four_new_native_messages_legal_and_same_source_day':len(msgs)==4 and all(v.get('receiver')==0 and v.get('target_planet')==124 and v.get('date')=='2233.07.02' and v.get('localization') in [prefix+'POP_TEXT',prefix+'ALLOYS_TEXT',prefix+'MINERALS_TEXT'] for v in msgs),
 'independent_remaining_slots7_and_four_bites':b['planets']['124']['planet_size']==20 and before_deposits.count('d_lithoid_devastation')==8 and all(before_deposits.count(k)==1 for k in ['d_dense_jungle','d_active_volcano','d_toxic_kelp']) and sum(b['districts'][str(i)]['level'] for i in b['colonies']['24']['districts'])==1 and (20-8-1-2-1-1)==7 and (7+1)//2==len(msgs),
 'last_odd_slot_native_mineral_branch':minn>=1 and kinds[-1]==prefix+'MINERALS_TEXT',
 'exact_accumulated_EEP_ledger':ac['variables']==expected,
 'native_return_equals_actual_source_plus_new_POP':source['variables']['eep_return_amount']==ac['variables']['eep_last_return']==returned,
 'mother_exact_return_without_manufacture_or_birth':a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+returned,
 'country_only_new_native_POP_created':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in ac['owned_colonies'])-sum(b['colonies'][str(i)]['actual_pop_sum'] for i in bc['owned_colonies'])==100*popn,
 'exact_founder_population_conservation':obs['before_species_population']=={'0:3321888769':b['colonies']['0']['actual_pop_sum'],'24:3321888769':b['colonies']['24']['actual_pop_sum']} and obs['after_species_population']=={'0:3321888769':b['colonies']['0']['actual_pop_sum']+returned},
 'source_no_actual_population':a['colonies']['24']['actual_pop_sum']==0 and not a['colonies']['24']['pop_groups'] and not any(g['planet']==24 and g['size']>0 for g in a['pop_groups'].values()),
 'only_source_removed_from_owned_colonies':bc['owned_colonies']==[0,24] and ac['owned_colonies']==[0],
 'source_unowned_shattered_no_deposits':source.get('owner') is None and source.get('controller') is None and source['planet_class']=='pc_shattered' and not source['deposits'],
 'source_all_steps_complete_active_cleared':steps<=set(source['flags']) and not set(source['flags'])&{'eep_active','eep_pending','eep_native','being_devoured','colony_event','eep_owned_colony_event'} and not source['modifiers'],
 'source_original_Q_T_seed_and_return_only':source['variables']=={**b['planets']['124']['variables'],'eep_return_amount':returned},
 'original_task_killed_no_active_task':a['situations']['16777227'].get('killed')=='yes' and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'one_new_pending_notice_flag':ac['flags']=={**bc['flags'],'eep_notice_pending':source['flags']['eep_credit_done']},
 'no_premature_displayed_notice':not obs['before_pending'] and not obs['after_pending'],
 'unique_original_core_owned_size18_capacity11':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11,
 'one_permanent_capacity11':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*11\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
 'court_and_original_deposit_held':core['modifiers'].count('modifier="eep_court"')==1 and [(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'mother19_paid_districts_held_within29':a['colonies']['0']['districts']==b['colonies']['0']['districts'] and all(a['districts'][str(i)]==b['districts'][str(i)] for i in b['colonies']['0']['districts']) and sum(a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts'])==19 and 19<=18+11==29,
 'mother_mining2000_generator800_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)]),
 'original_first_shattered_source_held':a['planets']['90']==b['planets']['90'] and not any(g['planet']==15 and g['size']>0 for g in a['pop_groups'].values()),
 'real_minerals_match_independent_native_rewards':D(obs['actual_stock_deltas']['minerals'])==expected_minerals,
 'real_alloys_match_only_new_native_rewards':D(obs['actual_stock_deltas']['alloys'])==expected_alloys,
 'all_other_real_economy_held':all(D(v)==0 for k,v in obs['actual_stock_deltas'].items() if k not in ['minerals','alloys']),
 'true_research_banks_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints'),
 'AP_traditions_species_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'] and b['species']==a['species'],
 'original_government_held':bc['government']==ac['government'],
 'no_free_completed_technologies':bc['completed_technologies']==ac['completed_technologies'],
 'global_targets_held':b['event_targets']==a['event_targets'],
}
p={'status':'PASS_SECOND_NATIVE_TERRAVORE_SETTLEMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_return':returned,'native_created_population':100*popn,'EEP_manufactured':ac['variables']['eep_made'],'new_native_message_kinds':kinds,'native_reward_formula':{'gross_minerals':str(gross('minerals')),'gross_alloys':str(gross('alloys')),'expected_minerals':str(expected_minerals),'expected_alloys':str(expected_alloys),'rounding_scope':'These observed native integer rewards only, not a general engine rounding theorem.'},'actual_EEP_ledger':ac['variables'],'scope':'Second native Q20/T48 adjacent-day settlement, actual return and independent final rewards, capacity and cleanup. Queen milestone, reload, long-term economy and full route still pending.'}
out=run/(after+'-second-settlement-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original second settlement FAIL retained; no calendar continuation'
