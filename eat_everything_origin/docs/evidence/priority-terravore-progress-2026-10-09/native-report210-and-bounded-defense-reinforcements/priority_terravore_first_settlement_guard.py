"""Read-only actual first Terravore settlement with native message/population conservation."""
import json,logging,re,shutil,sys
from decimal import Decimal as D,ROUND_HALF_UP
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(__file__,run/Path(__file__).name)
before='terravore-month41-day1';after='terravore-first-settlement'
b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'))
obs=json.loads((run/(after+'-boundary-observation.json')).read_text(encoding='utf-8'));bc,ac=b['countries']['0'],a['countries']['0'];source=a['planets']['90'];core=a['planets']['7']
msgs=[q.scalars(x) for x in obs['after_native_bite_messages']];kinds=[x['localization'] for x in msgs]
prefix='MESSAGE_TERRAVORE_CONSUME_WORLD_';popn=kinds.count(prefix+'POP_TEXT');alloyn=kinds.count(prefix+'ALLOYS_TEXT');minn=kinds.count(prefix+'MINERALS_TEXT')
returned=b['colonies']['15']['actual_pop_sum']+100*popn
expected=dict(bc['variables']);expected.update(eep_c=17,eep_g=0,eep_d=6,eep_worlds=1,eep_previous_capacity=2,eep_last_capacity=4,eep_last_return=returned,eep_entitled=0,eep_delta=0)
gross=lambda resource:sum((D(str(v.get(resource,0))) for v in bc['budget_categories']['current_month']['income'].values()),D(0))
reward=lambda mult,res:max(D(100),min(D(1000),gross(res)*mult)).to_integral_value(rounding=ROUND_HALF_UP)
expected_minerals=(minn-1)*reward(5,'minerals')+reward(3,'minerals');expected_alloys=alloyn*reward(3,'alloys')
steps={'eep_bites_done','eep_credit_done','eep_return_done','eep_population_done','eep_crisis_done','eep_destroy_done'}
checks={'actual_adjacent_date_and_receipt':b['date']=='2210.04.01' and a['date']=='2210.04.02' and all(obs['checks'].values()),
 'source_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'before_progress41_not_settled':b['situations']['16777223']['progress']==41 and bc['variables']['eep_worlds']==0,
 'five_native_messages_exact_order':kinds==[prefix+'ALLOYS_TEXT',prefix+'MINERALS_TEXT',prefix+'POP_TEXT',prefix+'ALLOYS_TEXT',prefix+'MINERALS_TEXT'],
 'native_messages_same_actual_day_source_owner':all(x['date']=='2210.04.02' and x['receiver']==0 and x['target_planet']==90 for x in msgs),
 'original_native_remaining_slots_nine':b['planets']['90']['planet_size']==17 and sum(a1['type']=='d_lithoid_devastation' for a1 in b['deposits'].values() if a1.get('deposit_holder',{}).get('id')==90)==6 and sum(a1['type']=='d_toxic_kelp' for a1 in b['deposits'].values() if a1.get('deposit_holder',{}).get('id')==90)==1 and sum(b['districts'][str(i)]['level'] for i in b['colonies']['15']['districts'])==1,
 'exact_country_EEP_ledger':ac['variables']==expected,
 'return440_independent_native_pop_message':returned==440==source['variables']['eep_return_amount']==ac['variables']['eep_last_return'],
 'mother_exact_return_without_extra_manufacture':a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+returned==6470,
 'country_exact_native100_only':sum(a['colonies'][str(i)]['actual_pop_sum'] for i in ac['owned_colonies'])-sum(b['colonies'][str(i)]['actual_pop_sum'] for i in bc['owned_colonies'])==100*popn==100,
 'exact_founder_population_conservation':obs['before_species_population']=={'0:3321888769':6030,'15:3321888769':340} and obs['after_species_population']=={'0:3321888769':6470},
 'no_source_actual_population':a['colonies']['15']['actual_pop_sum']==0 and not a['colonies']['15']['pop_groups'] and not any(p['planet']==15 and p['size']>0 for p in a['pop_groups'].values()),
 'only_source_removed_from_owned_colonies':ac['owned_colonies']==[i for i in bc['owned_colonies'] if i!=15],
 'source_unowned_shattered_no_deposits':source.get('owner') is None and source.get('controller') is None and source['planet_class']=='pc_shattered' and not source['deposits'],
 'source_all_steps_complete_active_cleared':steps<=set(source['flags']) and not set(source['flags'])&{'eep_active','eep_pending','eep_native','being_devoured','colony_event','eep_owned_colony_event'} and not source['modifiers'],
 'original_task_killed_no_active_task':a['situations']['16777223'].get('killed')=='yes' and not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'exact_one_pending_notice_flag':ac['flags']=={**bc['flags'],'eep_notice_pending':source['flags']['eep_credit_done']},
 'no_premature_displayed_notice':not obs['after_pending'],
 'unique_original_core_owned':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0,
 'size18_and_capacity6':core['planet_size']==18 and core['variables']['eep_capacity_value']==6,
 'one_permanent_capacity6':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*6\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
 'one_original_court':core['modifiers'].count('modifier="eep_court"')==1,
 'original_core_deposit_held':[(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'mother_all_real_districts_held':a['colonies']['0']['districts']==b['colonies']['0']['districts'] and all(a['districts'][str(i)]==b['districts'][str(i)] for i in b['colonies']['0']['districts']),
 'real_mineral997_matches_two_native_integer_rewards':D(obs['actual_stock_deltas']['minerals'])==expected_minerals==997,
 'real_alloys200_matches_two_native_rewards':D(obs['actual_stock_deltas']['alloys'])==expected_alloys==200,
 'all_other_real_economy_and_banks_held':all(D(v)==0 for k,v in obs['actual_stock_deltas'].items() if k not in ['minerals','alloys']),
 'AP_traditions_species_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'] and b['species']==a['species'],
 'original_government_held':bc['government']==ac['government'],
 'no_free_completed_technologies':bc['completed_technologies']==ac['completed_technologies'],
 'global_targets_held':b['event_targets']==a['event_targets']}
p={'status':'PASS_FIRST_NATIVE_TERRAVORE_SETTLEMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_return':returned,'native_created_population':100*popn,'EEP_manufactured':ac['variables']['eep_made'],'actual_EEP_ledger':ac['variables'],'native_reward_integer_formula':{'minerals_gross':str(gross('minerals')),'alloys_gross':str(gross('alloys')),'mineral_expected':str(expected_minerals),'alloy_expected':str(expected_alloys),'rounding_scope':'This observed case reproduction only; not a general engine rounding theorem.'},'before_research_queues':bc['research_queues'],'after_research_queues':ac['research_queues'],'source_cached_colony15_retained_empty':source.get('colony')==15,'scope':'Actual first native Q17/T41 adjacent-day settlement, independent native rewards and exact founder conservation, capacity and task cleanup. Queen acknowledgment, native reload, economic closure and full civic route still pending.'}
out=run/(after+'-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({k:v for k,v in p.items() if k not in ['before_research_queues','after_research_queues']}),flush=True);assert all(checks.values()),'Original first settlement FAIL retained; do not replay'
