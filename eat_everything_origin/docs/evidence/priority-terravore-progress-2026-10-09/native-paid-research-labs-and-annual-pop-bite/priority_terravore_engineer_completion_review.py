"""Read-only one native20day paid research-zone completion preflight."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();stage='terravore-six-hives-return-month-22810701';load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
a=read_state(run,stage);p=load(stage+'-serial-return-month-proof.json');x=load(stage+'-return-month-guard-execution.json')
rels=['common/zones/00_zones.txt','common/inline_scripts/zones/shared_research_engineering_zone.txt','common/inline_scripts/jobs/zone_engineers_add.txt','common/scripted_variables/100_scripted_variables_zones.txt'];sources=[]
for rel in rels:
 f=h.GAME_EXE.parent/rel;dest=run/('terravore-engineer-native-source-'+f.name)
 if dest.exists():assert dest.read_bytes()==f.read_bytes()
 else:dest.write_bytes(f.read_bytes())
 sources.append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
checks={
 'prior19PASS_actual0_originalSHA':len(p['checks'])==19 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(run/'priority_terravore_six_hives_return_month_guard.py')=='8415bb6b01c3f35463a7379cf4cfa9e5a92b48e879d642e5ee729ff4b42061bf' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(stage+'.sav')),
 'exact_paid_engineer_first333p2_then_six_hives_and_foundry104':p['boundaries']==['paid_engineering_zone_completion_review'] and q.scalars(a['items']['1627389955'])['progress']==333.2 and q.scalars(q.block(a['items']['1627389955'],'resources'))=={'minerals':800} and q.ids(q.block(a['queues']['0'],'items'))==[1627389955,268435492,251658284,1191182345,117440553,1476395019,117440546] and q.scalars(q.block(a['roots']['zones'],'104'))=={'type':'zone_foundry'},
 'original_colonizer_already_returned_no_pending_or_near_project2':q.scalars(q.block(a['fleets']['33555278'],'properties')).get('mia')!='yes' and not a['pending'] and p['project2_progress']<6000 and a['audit']['date']=='2281.07.01',
 'CN_same_production_error_and_four_original_sources_preserved':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(stage+'-engineer-completion-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2281.07.01','end_date':'2281.07.21','days':20,'maximum_days':20,'allowed_boundaries':p['boundaries'],'execution_stage':stage+'-engineer-completion-review','sources':sources,'scope':'One native20day paid800 engineer-zone completion, no monthly research tick or free construction.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
