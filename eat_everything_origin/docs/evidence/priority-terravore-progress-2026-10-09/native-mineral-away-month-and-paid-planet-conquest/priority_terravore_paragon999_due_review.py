"""Read-only native paragon source and current Lithoid leader eligibility review."""
import json,logging,sys,zipfile,shutil
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-away-first-month-22800601';stage='terravore-paragon999-due-review'
pre=load(before+'-campaign-v12-proof.json');px=load(before+'-campaign-guard-v12-execution.json');a=load(before+'-construction-boundary-observation-v4.json')['after_state']
with zipfile.ZipFile(run/(before+'.sav')) as z:rr={k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
source=Path('C:/SteamLibrary/steamapps/common/Stellaris/events/paragon_events.txt');preserved=run/(stage+'-paragon_events.txt');assert not preserved.exists();shutil.copyfile(source,preserved);text=source.read_text('utf-8-sig')
leaders={str(i):q.block(rr['leaders'],str(i)) for i in q.ids(q.block(a['country0_raw'],'owned_leaders'))};species=q.block(rr['species_db'],'73')
delays=[v for k,v,x in q.fields(q.block(q.block(a['country0_raw'],'modules'),'standard_event_module')) if k=='delayed_event' and x and q.scalars(v).get('event')=='paragon.999']
checks={
 'prior26_PASS_actual0_source_original_SAV':len(pre['checks'])==26 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(before+'.sav')),
 'only_exact_paragon_due_boundary':pre['boundaries']==['original_native_paragon999_due_review'] and a['audit']['date']=='2280.06.01',
 'one_original_country0_delay_exact14':len(delays)==1 and q.scalars(delays[0])['days']==14 and q.scalars(q.block(delays[0],'scope'))['id']==0,
 'all_owned_leaders_species73_lithoid':len(leaders)==10 and all(q.scalars(v)['species']==73 and q.scalars(v)['country']==0 for v in leaders.values()) and q.scalars(species)['class']=='LITHOID',
 'native999_gestalt_branch_1045_or_empty':all(v in text for v in ['id = paragon.999','limit = { owner = { is_gestalt = yes } }','10 = { leader_event = { id = paragon.1045 } }','90 = {}']),
 'native1045_robot_machine_requirement':all(v in text[text.index('\tid = paragon.1045\n'):text.index('\tid = paragon.1050\n')] for v in ['is_species_class = ROBOT','is_species_class = MACHINE','is_ruler = no']),
 'native_source_original_copy_SHA_held':h.sha256(source)==h.sha256(preserved),
 'CN_no_pending_error_exact_held':m['language']=='l_simp_chinese' and not a['pending_country0_raw'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':pre['after_sha256'],'after_sha256':pre['after_sha256'],'start_date':'2280.06.01','end_date':'2280.06.15','days':14,'maximum_days':14,'allowed_boundaries':pre['boundaries'],'execution_stage':stage,'source':str(source),'source_sha256':h.sha256(source),'preserved_source':preserved.name,'delay_original':delays,'owned_leaders_raw':leaders,'species73_raw':species,'scope':'Observe original delayed event expiry only. Actual resulting state requires independent checks; no event injection or rewards.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
