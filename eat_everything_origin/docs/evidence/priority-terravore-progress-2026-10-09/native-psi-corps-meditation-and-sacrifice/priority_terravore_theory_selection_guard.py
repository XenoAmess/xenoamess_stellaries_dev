"""Read-only normal Theory selection and exact specialized progress retention."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bt,at=bc['tech_status'],ac['tech_status']
bcs,acs=[{k:v for k,v,o in q.fields(rt['country']) if o} for rt in [br,ar]]
pre=json.loads((run/(before+'-research-cancel-proof.json')).read_text('utf-8'))
click=json.loads((run/'terravore-theory-native-select-click.action.json').read_text('utf-8'))
checks={
 'bound_actual_30_cancellation_PASS':pre['status'].startswith('PASS_') and len(pre['checks'])==30 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SHA_pair':b['date']==a['date']=='2235.04.01' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'normal_Theory_card_actual_click':click['action']=='left-click' and click['client_point']==[560,488] and click['foreground_after']==click['expected_hwnd'],
 'native_Theory_queue_only_added':not any(k=='society_queue' for k,v,o in q.fields(bt)) and len([1 for k,v,o in q.fields(at) if k=='society_queue' and o])==1 and q.scalars(q.block(at,'society_queue').strip()[1:-1])=={'technology':'tech_psionic_theory','date':'2235.04.01'},
 'both_specialized_progress_values_exact_held':q.scalars(q.block(bt,'stored_techpoints_for_tech'))==q.scalars(q.block(at,'stored_techpoints_for_tech'))=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'native_society_remains_manual':q.scalars(bt)['auto_researching_society']==q.scalars(at)['auto_researching_society']=='no',
 'all_other_tech_fields_raw_held':omit(bt,['society_queue'])==omit(at,['society_queue']),
 'other_country0_fields_raw_held':omit(bcs['0'],['tech_status'])==omit(acs['0'],['tech_status']),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k!='country']==[(k,v,o) for k,v,o in af if k!='country'],
 'true_three_banks_zero_held':q.research_stocks(bt)==q.research_stocks(at)==dict.fromkeys(q.RESEARCH_RESOURCES,0),
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','completed_technologies','variables','flags','traditions','ascension_perks','budget_categories','owned_colonies','government']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TERRAVORE_THEORY_SELECTION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'specialized_progress_after':ac['research_progress_by_tech'],'scope':'One normal Theory selection only adds its native zero-default queue; Theory650 and former607.25288 remain specialized progress. No research completion, Shroud or route acceptance claim.'}
out=run/(after+'-theory-selection-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original selection FAIL retained; no calendar'
