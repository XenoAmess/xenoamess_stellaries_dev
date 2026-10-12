"""Bind inspected, unedited native workshop candidates to actual passed checkpoints."""
import json,sys
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
assert m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
rows=[]
for img,sha,save,proof,execution,features,limits in [
 ('terravore-first-upkeep-destroyer-row-tooltip','05b084b2cda44a0fe3691326f2bf1700e49fed3a9518c8375a7966684af7e750','terravore-destroyer-first-upkeep-22840901','terravore-destroyer-first-upkeep-22840901-destroyer-first-upkeep-proof.json','terravore-destroyer-first-upkeep-22840901-destroyer-first-upkeep-guard',['Native official 威慑级驱逐舰 name','Actual1.70energy and1.70mineral hull upkeep, no alloy hull upkeep'],['This screenshot has first2 paid destroyers, not all16','Old ordinary ships and components may still consume alloys']),
 ('terravore-first-upkeep-destroyer-detail','eaaf5dca0344c292feb3abdaa1608d1d0e2cd2b93b09310d6624bd940a10892b','terravore-destroyer-first-upkeep-22840901','terravore-destroyer-first-upkeep-22840901-destroyer-first-upkeep-proof.json','terravore-destroyer-first-upkeep-22840901-destroyer-first-upkeep-guard',['Actual native destroyer hull1500/shield480/armor765','Normal paid ship and real components'],['Native hull display, not custom Queen art']),
 ('terravore-paid-hive-mother39-gallery-v2','addc7782b26026f9fd207209a8d75f416048e4a3e13fd28d7676021a7f738b02','terravore-full-paid-fleet-budget-22850601','terravore-full-paid-fleet-budget-22850601-final-paid-budget-proof.json','terravore-full-paid-fleet-budget-22850601-final-paid-budget-guard',['Shared mother capacity39 and real paid district levels28','Six paid hive levels and retained society/engineering laboratories','摄政女王·白绮 native label','Actual all16 paid fleet total naval261/131 visible'],['Native lithoid governor at left is not Queen Baiqi portrait','39capacity is not39 built districts','C76/project3 still incomplete, not C200/full acceptance'])]:
 p=load(proof);x=load(execution+'-execution.json');capture=load(img+'-execution.json')
 assert p['status'].startswith('PASS') and all(v is True for v in p['checks'].values()) and x['returncode']==capture['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) and capture['helper_sha256']==h.sha256(Path(capture['command'][1]))
 assert p['after_sha256']==h.sha256(run/(save+'.sav')) and h.sha256(run/(img+'.jpg'))==sha
 rows.append({'image':img+'.jpg','image_sha256':sha,'date':p['date'],'save':save+'.sav','save_sha256':p['after_sha256'],'guard_proof':proof,'guard_actual_returncode':0,'guard_checks':len(p['checks']),'features':features,'limits':limits})
out=run/'terravore-paid-destroyers-and-first-hive-workshop-candidates.json';assert not out.exists()
h.write_json(out,{'status':'LOCAL_NATIVE_WORKSHOP_CANDIDATES_ONLY','language':'l_simp_chinese','capture':'Steam F12 GPU backbuffer, original unedited1024x768 bytes','candidates':rows,'production_version':'0.2.0','at_utc':datetime.now(timezone.utc).isoformat(),'limits':['No upload or public gallery replacement','Only纵火本能 full route passed/recommended; Terravore still under acceptance']})
print(json.dumps({'status':'PASS','candidates':len(rows),'uploaded':False}),flush=True)
