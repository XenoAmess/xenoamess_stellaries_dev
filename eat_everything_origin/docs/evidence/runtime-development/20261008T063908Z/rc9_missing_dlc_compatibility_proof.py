import hashlib,json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();variant=m['dlc_variant'];assert variant in ['nemesis','shroud']
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest);stem='rc9-missing-'+variant
read=lambda n:json.loads((run/n).read_text(encoding='utf-8'));checks={};refs=[]
def ref(n):
 p=run/n;refs.append({'path':n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});return read(n)
for stage,progress in [('month12',12),('month19',19),('month20',None),('first-notice-month',None)]:
 n=stem+'-native-Q8-'+stage+'.audit.json';a=ref(n);c=a['countries']['0'];v=c['variables'];pids=[x['id'] for x in a['event_targets'] if x['name']=='eep_missing_dlc_source'];assert len(pids)==1;p=a['planets'][str(pids[0])]
 checks[stage+'_AP_empty']=c['ascension_perks']==[];checks[stage+'_no_psy_or_fleet']=v.get('eep_psi',0)==0 and v['eep_fleet_stage']==0
 checks[stage+'_no_absent_DLC_notice']=('eep_fleet_notice' if variant=='nemesis' else 'eep_psi_notice') not in c['flags']
 if progress is not None:
  tasks=[x for x in a['situations'].values() if x.get('country')==0 and x.get('type')=='situation_eep_devouring' and x.get('killed')!='yes'];checks[stage+'_actual_progress']=len(tasks)==1 and tasks[0]['progress']==progress
  checks[stage+'_no_early_awards']=all(v[k]==z for k,z in {'eep_c':0,'eep_g':0,'eep_d':2,'eep_made':0,'eep_worlds':0}.items());checks[stage+'_source_alive']=p['planet_class']=='pc_volcanic' and a['colonies'][str(p['colony'])]['actual_pop_sum']>=100
 else:
  checks[stage+'_actual_full_ledger']=all(v[k]==z for k,z in {'eep_c':8,'eep_g':8,'eep_d':4,'eep_made':100,'eep_worlds':1}.items());checks[stage+'_source_shattered_empty']=p['planet_class']=='pc_shattered' and a['colonies'].get(str(p.get('colony')),{}).get('actual_pop_sum',0)==0
  checks[stage+'_five_receipts']=all(k in p['flags'] for k in ['eep_population_done','eep_crisis_done','eep_destroy_done','eep_return_done','eep_credit_done'])
  checks[stage+'_return_receipt_consistent']=p['variables']['eep_return_amount']==v['eep_last_return'] and v['eep_last_return']>=100
  checks[stage+'_only_bound_mother_owned']=len(c['owned_colonies'])==1
 if stage=='first-notice-month':checks['real_first_swallow_notice']='eep_first_notice' in c['flags']
 s=ref(stem+'-native-Q8-'+stage+'-state.json');checks[stage+'_no_new_error']=s['new_error_bytes']==0
for name in ['native-dlc-confirmed.json','completed-five-replays-proof.json','native-AP-readonly-finished-proof.json','native-AP-DLC-gate-visual-review.json']:
 p=ref(stem+'-'+name);checks[name+'_passed']=p['status']=='PASS_SCOPED'
 if 'checks' in p:checks[name+'_all_checks']=all(p['checks'].values())
v={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','variant':variant,'checks':checks,'evidence':refs,'version':'0.2.0-rc.9','scope':'Actual missing DLC native CN configuration, normal Q8 decision, natural 20-month production completion, first queen notification and five guarded replay callbacks. Controlled source/100 transfer explicitly retained; this does not claim full government or release acceptance.'};h.write_json(run/(stem+'-compatibility-proof.json'),v);print(json.dumps({'status':v['status'],'checks':len(checks),'failed':[k for k,z in checks.items() if not z]},ensure_ascii=False),flush=True);assert all(checks.values())
