"""Read-only native tradition payment and actual population/EEP invariants."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,perk=sys.argv[1:]
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

def only_declared(v):
 c=v['countries']['0'];owned=c['owned_colonies']
 if owned==[0]:return True
 p=v['planets'].get('124',{})
 return owned==[0,24] and p.get('colony')==24 and p.get('owner')==p.get('controller')==0 and p.get('planet_class')=='pc_continental' and p.get('planet_size')==20

checks={'same_actual_date':a['date']==b['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'all_actual_stocks_and_true_banks_held':bc['effective_stockpile']==ac['effective_stockpile'],
 'other_actual_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='unity'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='unity'},
 'all_native_traditions_held':ac['traditions']==bc['traditions'],
 'exact_one_normally_earned_AP':ac['ascension_perks']==bc['ascension_perks']+[perk],
 'full_EEP_ledger_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'original_owned_colonies_held_only_mother_and_declared124':bc['owned_colonies']==ac['owned_colonies'] and only_declared(b) and only_declared(a),
 'population_group_membership_actual_size_species_held':set(b['pop_groups'])==set(a['pop_groups']) and all({k:c.get(k) for k in ['size','planet','key']}=={k:a['pop_groups'][i].get(k) for k in ['size','planet','key']} for i,c in b['pop_groups'].items()),
 'all_planets_core_districts_species_deposits_held':all(b[k]==a[k] for k in ['planets','districts','deposits','species','event_targets']),
 'native_tech_AP_gov_and_tasks_held':all(bc[k]==ac[k] for k in ['tech_status','government']) and b['situations']==a['situations'],
 'no_country_pending':not bp and not ap,
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-postsettlement-month-error-after.log').read_bytes()}
p={'status':'PASS_NATIVE_NORMALLY_EARNED_AP_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_unity_before_after':[bc['effective_stockpile']['unity'],ac['effective_stockpile']['unity']],'expected_native_AP':perk,'actual_AP':ac['ascension_perks'],'actual_traditions':ac['traditions'],'actual_job_changes':{i:{'before':b['pop_jobs'].get(i),'after':a['pop_jobs'].get(i)} for i in b['pop_jobs'].keys()|a['pop_jobs'].keys() if b['pop_jobs'].get(i)!=a['pop_jobs'].get(i)},'scope':'One actual native normally earned AP choice; legitimate job changes reported separately. No completed psionic route or crisis acceptance claim.'}
out=run/(after+'-earned-ap-v2-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original tradition FAIL retained; do not repeat purchase'
