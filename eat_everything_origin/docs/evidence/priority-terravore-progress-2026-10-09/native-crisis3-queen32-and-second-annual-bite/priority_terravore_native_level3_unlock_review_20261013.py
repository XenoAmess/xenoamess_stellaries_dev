"""Read-only four-day legal native crisis advancement preflight."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-project2-event-acknowledged';a=read_state(run,before);p=load(before+'-event-ack-proof.json');x=load(before+'-event-ack-guard-execution.json')
native=run/'terravore-project2-finish-native-00_crisis_levels.txt';levels=[q.unquote(v) for k,v,obj in q.fields(q.block(a['country'],'crisis_progression')) if k=='level' and not obj]
checks={
 'prior8PASS_actual0_originalSHA_source_bound':len(p['checks'])==8 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='d080ee16672966df3d173818e00d224a74c8cfc9a327df3cbd69ba407f5f9f3c' and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'native_flag_level2_Menace2180_no_pending_exact_boundary':q.scalars(q.block(a['country'],'flags')).get('crisis_special_project_2_complete')==63522984 and levels==['crisis_level_1','crisis_level_2'] and a['audit']['countries']['0']['effective_stockpile']['menace']==2180 and not a['pending'] and p['boundaries']==['native_level3_unlock_and_delayed4150_review'],
 'native_level3_legality_and_3day_notification_sources_preserved':h.sha256(native)==h.sha256(h.GAME_EXE.parent/'common/crisis_levels/00_crisis_levels.txt') and 'crisis.4150 days = 3' in q.block(native.read_text('utf-8-sig'),'crisis_level_3') and q.scalars(q.block(native.read_text('utf-8-sig'),'crisis_level_3'))['required_crisis_currency']==2000,
 'CN_production_same_error627_no_near_lab_completion':a['audit']['date']=='2282.10.03' and q.scalars(a['items']['184549419'])['progress']==243.6 and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')=='627e51825f38d8ab28ff788c58d44b2e769c4dfcaa563be1b64feb1035508592',
}
passed=all(v is True for v in checks.values());out=run/(before+'-native-level3-unlock-review.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['after_sha256'],'after_sha256':p['after_sha256'],'start_date':'2282.10.03','end_date':'2282.10.07','days':4,'maximum_days':4,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-native-level3-unlock-review','scope':'Four normal days; native level3 and delayed4150 must be observed and independently checked. No gifts or EEP stage assertion.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
