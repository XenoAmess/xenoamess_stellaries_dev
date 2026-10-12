"""Only30 native days; exact cost2600 UI and paid360work conversion boundaries."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-society-zone-priority-22831001';a=read_state(run,before);c=a['audit']['countries']['0'];p=load(before+'-queue-priority-proof.json');x=load(before+'-queue-priority-guard-execution.json')
rels=['common/inline_scripts/zones/shared_research_physics_zone.txt','common/inline_scripts/zones/shared_research_society_zone.txt','common/buildings/05_research_buildings.txt','common/technology/00_eng_tech.txt','events/pirate_events.txt'];sources=[]
for rel in rels:
 f=h.GAME_EXE.parent/rel;dest=run/('terravore-society-conversion-native-'+f.name)
 if dest.exists():assert dest.read_bytes()==f.read_bytes()
 else:dest.write_bytes(f.read_bytes())
 sources.append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event'];projects=[q.scalars(v) for k,v,obj in q.fields(q.block(a['country'],'events')) if obj and k=='special_project']
checks={
 'prior8PASS_actual0_source_exact_SAV':len(p['checks'])==8 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='b6075d9c76dd0978938101709ea3db7188b1fb209039ecf40130059e52cdc60c' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'exact_front_paid800_work0_of360_and_six_tail22p4held':a['audit']['date']=='2283.10.01' and q.ids(q.block(a['queues']['0'],'items'))==[83886115,268435492,251658284,1191182345,117440553,1476395019,117440546] and q.scalars(a['items']['83886115'])['progress']==0 and q.scalars(a['items']['83886115'])['progress_needed']==360 and q.scalars(q.block(a['items']['83886115'],'resources'))=={'minerals':800},
 'native_research_cost_and_timers_no_other_boundaries_before30':h.sha256(run/'terravore-society-project3-research-panel-frame-v2.jpg')=='4a5d057b7c44ea5a5efd96667e0dd13bdef50bd830d562777d5f36dc5a3109df' and c['research_stockpile']['society_research']>10000 and {v['event']:v['days'] for v in delays}=={'cstorms.1815':273,'pirate.6':17} and all(v.get('days_left',999)>30 for v in projects) and not a['pending'] and c['owned_colonies']==[0] and all(v.get('killed')=='yes' for v in a['audit']['situations'].values()),
 'CN_same_package_error627_and_native_source_preserved':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(before+'-society-construction-first-month-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2283.10.01','end_date':'2283.11.01','days':30,'maximum_days':30,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-society-construction-first-month-review','sources':sources,'scope':'One normal construction/research month; no completed replacement or project.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
