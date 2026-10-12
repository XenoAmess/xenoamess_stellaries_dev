"""Read-only eight-day first paid lab completion preflight."""
import json,logging,sys
from pathlib import Path
before,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
a=read_state(run,before);p=load(prior);x=load(execution+'-execution.json')
rels=['common/buildings/05_research_buildings.txt','common/inline_scripts/jobs/researchers_add.txt','common/scripted_variables/100_scripted_variables_zones.txt'];sources=[]
for rel in rels:
 f=h.GAME_EXE.parent/rel;dest=run/('terravore-three-paid-labs-native-'+f.name)
 if dest.exists():assert dest.read_bytes()==f.read_bytes()
 else:dest.write_bytes(f.read_bytes())
 sources.append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
checks={
 'prior18PASS_actual0_originalSHA_bound_source':len(p['checks'])==18 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'paid_first_lab350_of360_cost320_engineering_zone_queue_exact':p['boundaries']==['paid_first_research_lab_completion_review'] and q.scalars(a['items']['1644167171'])['progress']==350 and q.scalars(a['items']['1644167171'])['progress_needed']==360 and q.scalars(q.block(a['items']['1644167171'],'resources'))=={'minerals':320} and q.scalars(q.block(a['items']['1644167171'],'buildable_planet_building'))=={'building':'building_research_lab_1','planet':0,'zone':16777330} and q.ids(q.block(a['queues']['0'],'items'))[:3]==[1644167171,184549419,67108899],
 'no_pending_and_project2_under6000_native_lab_job60_sources':a['audit']['date']=='2282.04.01' and not a['pending'] and p['project2_progress']<6000 and q.scalars(Path(sources[2]['path']).read_text('utf-8-sig'))['@building_static_jobs_3']==60 and 'jobs/researchers_add' in q.block(Path(sources[0]['path']).read_text('utf-8-sig'),'building_research_lab_1'),
 'CN_same_production_exact_error627_sources_preserved':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(before+'-paid-lab-completion-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2282.04.01','end_date':'2282.04.09','days':8,'maximum_days':8,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-paid-lab-completion-review','sources':sources,'scope':'Paid320 first lab completion; one old cached research tick, no extra cash or EEP rewards.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
