"""Read-only native tradition payment and actual population/EEP invariants."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D,ROUND_CEILING
from pathlib import Path
before,after,raw_cost,raw_add=sys.argv[1:];cost=D(raw_cost);addition=raw_add.split(',')
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 pending=[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and q.scalars(v).get('country')==0]
 return a,pending
b,bp=read(before);a,ap=read(after);bc,ac=b['countries']['0'],a['countries']['0']
def actual_population(v):
 out={}
 for g in v['pop_groups'].values():
  key=(g['planet'],g['key']['species']);out[key]=out.get(key,0)+g['size']
 return out
def only_declared(v):
 c=v['countries']['0'];owned=c['owned_colonies']
 if owned==[0]:return True
 p=v['planets'].get('124',{})
 return len(owned)==2 and sorted(owned)==sorted([0,p.get('colony',-1)]) and p.get('owner')==p.get('controller')==0 and p.get('planet_class')=='pc_continental' and p.get('planet_size')==20
checks={'same_actual_date':a['date']==b['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_decimal_payment_matches_UI_ceiling':0<D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']))<=cost and (D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']))).to_integral_value(rounding=ROUND_CEILING)==cost,
 'other_actual_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='unity'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='unity'},
 'exact_native_traditions_added':ac['traditions']==bc['traditions']+addition,
 'all_original_AP_held':ac['ascension_perks']==bc['ascension_perks'],
 'full_EEP_ledger_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'original_owned_colonies_held_only_mother_and_declared124':bc['owned_colonies']==ac['owned_colonies'] and only_declared(b) and only_declared(a),
 'actual_population_by_colony_and_species_held':actual_population(b)==actual_population(a),
 'all_planets_core_districts_species_deposits_held':all(b[k]==a[k] for k in ['planets','districts','deposits','species','event_targets']),
 'native_tech_AP_gov_and_tasks_held':all(bc[k]==ac[k] for k in ['tech_status','government']) and b['situations']==a['situations'],
 'no_country_pending':not bp and not ap,
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-postsettlement-month-error-after.log').read_bytes()}
p={'status':'PASS_NATIVE_PAID_TRADITION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_decimal_unity_paid':str(D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']))),'displayed_UI_price':str(cost),'actual_unity_before_after':[bc['effective_stockpile']['unity'],ac['effective_stockpile']['unity']],'expected_native_additions':addition,'actual_traditions':ac['traditions'],'actual_pop_group_changes':{i:{'before':b['pop_groups'].get(i),'after':a['pop_groups'].get(i)} for i in b['pop_groups'].keys()|a['pop_groups'].keys() if b['pop_groups'].get(i)!=a['pop_groups'].get(i)},'actual_job_changes':{i:{'before':b['pop_jobs'].get(i),'after':a['pop_jobs'].get(i)} for i in b['pop_jobs'].keys()|a['pop_jobs'].keys() if b['pop_jobs'].get(i)!=a['pop_jobs'].get(i)},'scope':'One actual native paid tradition choice; legitimate job changes reported separately. No completed psionic route or crisis acceptance claim.'}
out=run/(after+'-paid-tradition-v3-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original tradition FAIL retained; do not repeat purchase'
