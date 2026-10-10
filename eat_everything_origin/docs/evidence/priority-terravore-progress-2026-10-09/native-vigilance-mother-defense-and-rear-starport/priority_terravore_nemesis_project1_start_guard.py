"""Native psionic project research start; precise queue only, no grants."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-nemesis-intro-ack';after='terravore-nemesis-project1-started'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];brc,arc=q.block(br['country'],'0'),q.block(ar['country'],'0');bts,ats=q.block(brc,'tech_status'),q.block(arc,'tech_status')
pre=json.loads((run/(before+'-nemesis-intro-ack-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
soc=q.block(ats,'society_queue').strip();p=[v for k,v,o in q.fields(q.block(arc,'events')) if k=='special_project' and q.scalars(v).get('id')==2];assert len(p)==1
checks={
 'bound23_intro_PASS_actual_exit0_exact_input':pre['status']=='PASS_TERRAVORE_NEMESIS_INTRO_ACK_COMPONENT' and len(pre['checks'])==23 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date']=='2258.11.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'exact_one_new_society_project2_queue':not q.block(bts,'society_queue') and soc.startswith('{') and soc.endswith('}') and q.scalars(soc[1:-1])=={'special_project':2,'date':'2258.11.02'},
 'all_other_tech_status_ordered_raw_held':omit(bts,{'society_queue'})==omit(ats,{'society_queue'}),
 'all_other_country0_raw_held':omit(brc,{'tech_status'})==omit(arc,{'tech_status'}),
 'all_other_countries_ordered_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'all_other_ordered_top_raw_held':omit(bt,{'country','random_count'})==omit(at,{'country','random_count'}),
 'native_random_exact_plus2':q.scalars(bt)['random_count']==52825416 and q.scalars(at)['random_count']==52825418,
 'all_true_cash_and_research_bank_held':bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'] and ac['research_stockpile']['society_research']==4979.90395,
 'old_colonization_progress607_25288_held':bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_colonization_2':607.25288},
 'all_EEP_flags_and_variables_held':bc['flags']==ac['flags'] and bc['variables']==ac['variables'],
 'actual_population_workforce_mother_species_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','situations','event_targets']),
 'no_pending_or_completion_flag':not [v for k,v,o in q.fields(at) if k=='player_event'] and 'crisis_special_project_1_complete' not in q.scalars(q.block(arc,'flags')),
 'exact_project2_unprogressed_and_crisis_level1_held':q.scalars(p[0])=={'id':2,'special_project':'CRISIS_SPECIAL_PROJECT_PSIONIC_1','ai_research_date':'2258.11.14'} and q.scalars(q.block(arc,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'},
 'all_bound_native_source_SHA_still_current':all(h.sha256(Path(s['path']))==s['sha256'] for s in pre['sources']),
 'normal_click_and_save_exit0':json.loads((run/('terravore-nemesis-project1-start-click-execution.json')).read_text('utf-8'))['returncode']==0 and json.loads((run/('terravore-nemesis-project1-start-click.action.json')).read_text('utf-8'))['client_point']==[355,395] and json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0,
 'unfiltered_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
out=run/(after+'-project1-start-proof.json');assert not out.exists();p={'status':'PASS_TERRAVORE_NEMESIS_PROJECT1_NATIVE_START_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':True,'actual_society_queue':soc,'actual_true_bank':ac['research_stockpile'],'sources':pre['sources'],'scope':'Normal native project research start only. No resource deduction, progress completion, menace or mineral-ship claim.'};h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original project start FAIL retained'
