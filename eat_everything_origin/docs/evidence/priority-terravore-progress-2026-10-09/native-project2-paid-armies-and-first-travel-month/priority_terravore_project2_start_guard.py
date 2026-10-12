"""Same-day native physical psionic project2 start, no grants."""
import json,logging,sys,zipfile
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();sha=h.sha256;load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-mineral-corvette-first-full-month-date';after='terravore-project2-started'
def read(st):
 a=load(st+'.audit.json')
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
omit=lambda raw,keys:[(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];brc,arc=[q.block(x['country'],'0') for x in [br,ar]];bts,ats=[q.block(x,'tech_status') for x in [brc,arc]];be,ae=[q.block(x,'events') for x in [brc,arc]]
bp=[v for k,v,o in q.fields(be) if k=='special_project' and q.scalars(v).get('id')==8];ap=[v for k,v,o in q.fields(ae) if k=='special_project' and q.scalars(v).get('id')==8];assert len(bp)==len(ap)==1
pq=q.block(ats,'physics_queue').strip();tokens=list(q.tokens(pq));queue=q.scalars(pq[tokens[0][2]:tokens[-1][1]]) if tokens else {}
pre=load(before+'-first-mineral-corvette-month-v2-proof.json');pe=load(before+'-first-mineral-corvette-month-guard-v2-execution.json');static=load('terravore-pre-project2-open-kaishek-report.json');sx=load('terravore-pre-project2-open-kaishek-execution.json')
checks={
 'prior24_actual0_exact_SAV_source':len(pre['checks'])==24 and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==sha(Path(pe['command'][1]))=='ad36490c06486d7d09a755ad3eba8f34cfc50056c7f282737bd05aa3b8e7ab07' and pre['after_sha256']==b['save_sha256'],
 'open_kaishek_PASS_actual0_production41_020_tree':static['status']=='PASS' and sx['returncode']==0 and sx['helper_sha256']==sha(Path(sx['command'][1])) and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and meta['language']=='l_simp_chinese' and meta['version']=='0.2.0',
 'same_date_actual_SAV_pair':a['date']==b['date']=='2279.01.01' and all(sha(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'only_one_new_physics_queue_project8':not q.block(bts,'physics_queue') and queue=={'special_project':8,'date':'2279.01.01'},
 'other_research_raw_held':omit(bts,{'physics_queue'})==omit(ats,{'physics_queue'}),
 'project8_adds_status_in_progress_only':q.scalars(bp[0])=={'id':8,'special_project':'CRISIS_SPECIAL_PROJECT_PSIONIC_2','ai_research_date':'2278.10.11'} and q.scalars(ap[0])==dict(q.scalars(bp[0]),status='in_progress') and omit(bp[0],{'status'})==omit(ap[0],{'status'}),
 'all_other_events_projects_raw_held':[(k,v,o) for k,v,o in q.fields(be) if not (k=='special_project' and v==bp[0])]==[(k,v,o) for k,v,o in q.fields(ae) if not (k=='special_project' and v==ap[0])],
 'other_country0_including_known_pirate18_raw_held':omit(brc,{'tech_status','events'})==omit(arc,{'tech_status','events'}),
 'all_other_countries_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'all_other_ordered_world_raw_held':omit(bt,{'country','random_count'})==omit(at,{'country','random_count'}),
 'native_random_count_only_plus2':q.scalars(at)['random_count']-q.scalars(bt)['random_count']==2,
 'all_true_cash_research_banks_and_population_held':bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'] and all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','situations','event_targets']),
 'EEP_crisis2_Menace1635_core_held':bc['flags']==ac['flags'] and bc['variables']==ac['variables'] and q.block(brc,'crisis_progression')==q.block(arc,'crisis_progression') and bc['variables']['eep_c']==62 and a['colonies']['0']['actual_pop_sum']==11938,
 'no_completion_new_pending_or_error':not [v for k,v,o in q.fields(at) if k=='player_event'] and 'crisis_special_project_2_complete' not in q.scalars(q.block(arc,'flags')) and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
 'one_normal_click_355_365_and_save_actual0':load('terravore-project2-start-click-execution.json')['returncode']==0 and load('terravore-project2-start-click.action.json')['client_point']==[355,365] and load(after+'-native-save-execution.json')['returncode']==0,
}
passed=all(v is True for v in checks.values());out=run/(after+'-project2-start-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_TERRAVORE_PROJECT2_NATIVE_START_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_random_before':q.scalars(bt)['random_count'],'native_random_after':q.scalars(at)['random_count'],'physics_queue':queue,'true_bank':ac['research_stockpile'],'boundaries':['known_native_pirate6_delayed_event','next_native_acceptance_plan_required'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':a['save_sha256']}),flush=True);assert passed
