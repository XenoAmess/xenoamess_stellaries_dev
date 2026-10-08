import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');start,stage=sys.argv[1:];sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(Path(__file__),dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
b=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();c=lambda x:x['countries']['0']
def invariants(x):
 p=x['planets']['1'];v=c(x)['variables']
 return {'legal_government_and_origin':q.scalars(c(x)['government']).get('authority')=='auth_hive_mind' and q.scalars(c(x)['government']).get('origin')=='origin_heart_of_devouring' and 'civic_hive_scorched_earth' in c(x)['government'],
  'ledger_no_awards':all(v.get(k)==0 for k in ['eep_c','eep_g','eep_made','eep_worlds','eep_stage','eep_fleet_stage']),
  'capacity2':v['eep_d']==2 and p['variables']['eep_capacity_value']==2,'one_capacity_modifier':len(re.findall(r'modifier="eep_capacity"',p['modifiers']))==1,
  'one_court_modifier':len(re.findall(r'modifier="eep_court"',p['modifiers']))==1,'one_core_deposit':sum(x['deposits'][str(i)].get('type')=='d_eep_core' for i in p['deposits'])==1,
  'no_situations':not x['situations'],'AP_empty':c(x)['ascension_perks']==[],'no_ascension_or_crisis_notice':not any(k in c(x)['flags'] for k in ['eep_psi_notice','eep_fleet_notice','eep_notice_pending']),
  'core_bound_original':any(t['name']=='eep_core0' and t['id']==1 for t in x['event_targets'])}
if False:
 checks=invariants(b);checks['actual_month_date']=b['date']=='2200.02.04';checks['native_population_growth_only']=b['colonies']['0']['actual_pop_sum']>=5300
 checks['native_month_incomes_present']=c(b)['stockpile'].get('minerals',0)>250 and c(b)['stockpile'].get('unity',0)>50
 with zipfile.ZipFile(run/(start+'.sav')) as z:text=z.read('gamestate').decode('utf-8-sig')
 checks['no_probe_references']='eep_probe' not in text;checks['no_pending_eep_messages']=not any(k=='player_event' and o and str(q.scalars(v).get('event','')).startswith('eep.') for k,v,o in q.fields(text))
 proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'save_sha256':b['save_sha256'],'date':b['date'],'mother_population':b['colonies']['0']['actual_pop_sum'],'actual_stockpile':c(b)['stockpile'],'scope':'Actual thirty-day final-production first month; native income/growth retained, no EEP production award or fixture callback.'};h.write_json(run/'formal-prod-first-month-invariants-proof.json',proof);print(json.dumps(proof),flush=True);assert all(checks.values())
alias='prod-stable';path=user/'save games/acceptance-fixtures'/(alias+'.sav');assert not path.exists();path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(run/(start+'.sav'),path);assert h.sha256(path)==b['save_sha256']
r.native_load(alias,stage+'-load');a=r.native_save(stage,b['date'],(0,))
checks=invariants(a);checks.update({'same_date':a['date']==b['date'],'all_stock_same':c(a)['stockpile']==c(b)['stockpile'],'all_pop_groups_same':a['pop_groups']==b['pop_groups'],'all_pop_jobs_same':a['pop_jobs']==b['pop_jobs'],
 'all_EEP_variables_same':c(a)['variables']==c(b)['variables'],'all_EEP_flags_same':c(a)['flags']==c(b)['flags'],'traditions_same':c(a).get('traditions')==c(b).get('traditions'),
 'technology_same':c(a)['completed_technologies']==c(b)['completed_technologies'],'research_queues_same':c(a)['research_queues']==c(b)['research_queues']})
checks.update({key+'_same':a[key]==b[key] for key in ['colonies','planets','districts','deposits','situations','event_targets','species']});checks['no_new_errors']=(user/'logs/error.log').read_bytes()==eb
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'alias_sha256':h.sha256(path),'after_sha256':a['save_sha256'],'scope':'Original-byte native Chinese load and native post-load save in final production-only process; complete audited economic, population, ledger and world collections.'};h.write_json(run/(stage+'-proof.json'),v);print(json.dumps(v),flush=True);assert all(checks.values())
