"""Read-only second-settlement milestone month: narration, growth, budget, no repeated award."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));p=[q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0]
 msgs=[v for k,v,o in fs if k=='message' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD']
 growth=q.scalars(q.block(q.block(q.block(t,'colony'),'0'),'last_month_growth_data'))
 gc=q.block(q.block(q.block(q.block(t,'colony'),'0'),'last_month_growth_data'),'growth_and_size')
 return a,t,p,msgs,q.scalars(gc)
b,bt,bp,bm,bg=read(before);a,at,ap,am,ag=read(after)
bc,ac=b['countries']['0'],a['countries']['0'];core=a['planets']['7']
pre=json.loads((run/(before+'-second-settlement-proof.json')).read_text('utf-8'))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
net={};residual={}
for k in ['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']:
 net[k]=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
 expected=D(str(bc['effective_stockpile'].get(k,0)))+net[k]
 if k=='influence':expected=min(D(1000),expected)
 residual[k]=D(str(ac['effective_stockpile'].get(k,0)))-expected
expected_vars={**bc['variables'],'eep_stage':1}
expected_flags={k:v for k,v in bc['flags'].items() if k!='eep_notice_pending'}
steps={'eep_bites_done','eep_credit_done','eep_return_done','eep_population_done','eep_crisis_done','eep_destroy_done'}
checks={
 'bound_original_second_settlement35_PASS':pre['status']=='PASS_SECOND_NATIVE_TERRAVORE_SETTLEMENT_COMPONENT' and len(pre['checks'])==35 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual29_day_date_and_receipt':b['date']=='2233.07.02' and a['date']=='2233.08.01' and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==29 and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'only_one_new_native_eep13_pending':not bp and len(ap)==1 and ap[0]['event']=='eep.13',
 'exact_stage1_only_EEP_change':bc['variables']['eep_stage']==0 and ac['variables']==expected_vars,
 'notice_pending_consumed_first_notice_held':bc['flags'].get('eep_first_notice') is not None and 'eep_notice_pending' in bc['flags'] and ac['flags']==expected_flags,
 'core_only_correct_report_display_change':core['variables']=={**b['planets']['7']['variables'],'eep_actual_pop':a['colonies']['0']['actual_pop_sum'],'eep_free_districts':10},
 'native_growth_only_no_additional_manufacture':ag['month_start_size']==b['colonies']['0']['actual_pop_sum'] and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']+ag['growth'] and ag['growth']>=0,
 'only_original_mother_owned':bc['owned_colonies']==ac['owned_colonies']==[0],
 'no_new_native_bite_message':bm==am,
 'all_eight_current_month_budget_residuals_zero':all(abs(v)<D('0.00005') for v in residual.values()),
 'last_month_equals_previous_current_month':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'],
 'true_research_banks_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints'),
 'both_sources_unowned_shattered_and_empty':all(a['planets'][pid].get('owner') is None and a['planets'][pid].get('controller') is None and a['planets'][pid]['planet_class']=='pc_shattered' and not a['planets'][pid]['deposits'] and not any(g['planet']==col and g['size']>0 for g in a['pop_groups'].values()) for pid,col in [('90',15),('124',24)]),
 'both_source_receipts_and_step_flags_held':all(a['planets'][pid]['variables']==b['planets'][pid]['variables'] and steps<=set(a['planets'][pid]['flags']) and not set(a['planets'][pid]['flags'])&{'eep_active','eep_pending','eep_native','being_devoured','colony_event','eep_owned_colony_event'} for pid in ['90','124']),
 'no_new_active_devouring_situation':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'unique_original_core_owned_capacity11_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11,
 'one_permanent_capacity11_and_court':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*11\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])) and core['modifiers'].count('modifier="eep_court"')==1,
 'original_core_deposit_held':[(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'mother19_paid_districts_held':a['colonies']['0']['districts']==b['colonies']['0']['districts'] and all(a['districts'][str(i)]==b['districts'][str(i)] for i in b['colonies']['0']['districts']) and sum(a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts'])==19,
 'mother_mining2000_generator800_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)]),
 'AP_traditions_species_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'] and b['species']==a['species'],
 'legal_original_government_types_and_civics':all(q.scalars(bc['government'])[k]==q.scalars(ac['government'])[k] for k in ['type','authority','origin']) and q.block(bc['government'],'civics')==q.block(ac['government'],'civics'),
 'original_global_targets_held':b['event_targets']==a['event_targets'],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_SECOND_TERRAVORE_NOTICE_MONTH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_pending':ap,'actual_growth':ag,'current_month_net':{k:str(v) for k,v in net.items()},'budget_residuals':{k:str(v) for k,v in residual.items()},'actual_population':a['colonies']['0']['actual_pop_sum'],'actual_EEP_variables':ac['variables'],'actual_core_variables':core['variables'],'scope':'Only second settlement next monthly growth/budget, stage1 Queen notice and no repeated award; notice acknowledgement/reload/full route pending.'}
out=run/(after+'-second-notice-month-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True)
assert all(checks.values()),'Original second notice month FAIL retained'
