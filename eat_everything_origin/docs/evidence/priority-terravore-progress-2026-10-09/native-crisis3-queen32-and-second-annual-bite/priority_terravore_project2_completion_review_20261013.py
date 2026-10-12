"""Read-only exact two-day native project completion preflight; no grants."""
import json,logging,sys
from pathlib import Path
from decimal import Decimal as D
before,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
a=read_state(run,before);p=load(prior);x=load(execution+'-execution.json');audit=a['audit'];c=audit['countries']['0'];start=audit['date'];end=start[:-2]+'03'
raw=c['research_queues']['physics_queue'];ts=list(q.tokens(raw));pq=q.scalars(raw[ts[0][2]:ts[-1][1]]);income=sum((D(str(v.get('physics_research',0))) for v in c['budget_categories']['current_month']['income'].values()),D(0));draw=min(income,D(str(c['research_stockpile']['physics_research'])))
projects=[v for k,v,o in q.fields(q.block(a['country'],'events')) if o and k=='special_project' and q.scalars(v).get('id')==8]
rels=['common/special_projects/00_projects_nemesis.txt','events/nemesis_crisis_events.txt','common/crisis_levels/00_crisis_levels.txt','localisation/simp_chinese/nemesis_content_l_simp_chinese.yml'];sources=[]
for rel in rels:
 f=h.GAME_EXE.parent/rel;dest=run/('terravore-project2-finish-native-'+f.name)
 if dest.exists():assert dest.read_bytes()==f.read_bytes()
 else:dest.write_bytes(f.read_bytes())
 sources.append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
native_project=next(v for k,v,o in q.fields(Path(sources[0]['path']).read_text('utf-8-sig')) if o and k=='special_project' and q.scalars(v).get('key')=='CRISIS_SPECIAL_PROJECT_PSIONIC_2')
checks={
 'prior18PASS_actual0_originalSHA_bound_source':len(p['checks'])==18 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==audit['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_project2_boundary_one_cached_tick_legally_crosses6000':p['boundaries']==['native_project2_completion_review'] and start.endswith('.01') and pq['special_project']==8 and D(str(pq['progress']))<6000<=D(str(pq['progress']))+income*D('1.35')+draw and len(projects)==1 and q.scalars(projects[0])['special_project']=='CRISIS_SPECIAL_PROJECT_PSIONIC_2' and q.scalars(native_project)['cost']==6000 and q.scalars(native_project)['tech_department']=='physics_technology',
 'no_pending_no_cash_or_EEP_grants_Menace2180_level2':not a['pending'] and c['effective_stockpile']['menace']==2180 and c['variables']['eep_c']==62 and c['variables']['eep_fleet_stage']==2 and q.scalars(q.block(Path(sources[2]['path']).read_text('utf-8-sig'),'crisis_level_3'))['required_crisis_currency']==2000,
 'CN_same_production_exact_error627_sources_preserved':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(before+'-project2-completion-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':start,'end_date':end,'days':2,'maximum_days':2,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-project2-completion-review','sources':sources,'scope':'Native two-day project2 completion, original pending event must be reviewed and normally confirmed before advancement.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'start':start,'end':end}),flush=True);assert passed
