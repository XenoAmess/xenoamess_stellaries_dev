"""Read-only exact native refused-by-timeout peace notification source review."""
import json,logging,sys,zipfile,shutil
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
before='terravore-balthasar-transit-22800901';after='terravore-balthasar-transit-22801001';stage='terravore-native-peace-timeout-review'
failed=load(after+'-campaign-v14-proof.json');fx=load(after+'-campaign-guard-v14-execution.json');o=load(after+'-construction-boundary-observation-v4.json')
roots=[]
for st in [before,after]:
 with zipfile.ZipFile(run/(st+'.sav')) as z:roots.append({k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x})
source_records=[]
for relative in ['common/diplomatic_actions/00_actions.txt','localisation/simp_chinese/messages_l_simp_chinese.yml']:
 source=Path('C:/SteamLibrary/steamapps/common/Stellaris')/relative;dest=run/(stage+'-'+source.name);assert not dest.exists();shutil.copyfile(source,dest);source_records.append({'path':str(source),'preserved':dest.name,'sha256':h.sha256(source)})
messages=o['new_country0_messages_raw'];raw=messages[0];s=q.scalars(raw);action=q.block(q.block(raw,'diplomatic_action_3rd_party'),'action_offer_peace');offer=q.scalars(q.block(action,'peace_offer'))
checks={
 'original27_exactly_one_message_FAIL_actual1_source':len(failed['checks'])==27 and {k for k,v in failed['checks'].items() if v is not True}=={'only_documented_zero_loss_native_route_reports_and_real_storm_visibility'} and fx['returncode']==1 and fx['helper_sha256']==h.sha256(Path(fx['command'][1])),
 'original_SAV_pair_calendar_observer_actual0':all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav')) for st,name in [(o['before_state'],before),(o['after_state'],after)]) and all(v is True for v in o['checks'].values()) and load(after+'-calendar-execution.json')['returncode']==load(after+'-boundary-observation-v4-execution.json')['returncode']==0,
 'single_exact_native292_expired_enemy_statusquo_proposal':len(messages)==1 and s['type']=='DIPLO_ACTION_OFFER_PEACE' and s['localization']=='ACTION_OFFER_PEACE_PROPOSAL_FAILED_RECIPIENT' and s['receiver']==0 and s['notification']==292 and s['date']=='2280.10.01' and offer=={'status':'status_quo','actor':1,'recipient':0,'war':1} and q.scalars(action)['timeout']=='2280.09.30',
 'official_CN_source_explicit_auto_refusal':('\u65f6\u9650\u5df2\u8fc7\uff0c\u5df2\u81ea\u52a8\u62d2\u7edd' in (run/source_records[1]['preserved']).read_text('utf-8-sig')) and 'action_offer_peace = {' in (run/source_records[0]['preserved']).read_text('utf-8-sig'),
 'complete_original_war1_still_active_raw_held':bool(q.block(roots[0]['war'],'1')) and q.block(roots[0]['war'],'1')==q.block(roots[1]['war'],'1'),
 'all_other26_contracts_true_no_pending':sum(v is True for v in failed['checks'].values())==26 and not o['after_state']['pending_country0_raw'],
 'official_sources_original_bytes_SHA_held':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in source_records),
 'production_CN_error_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and h.sha256(user/'logs/error.log')==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_PEACE_TIMEOUT_SOURCE' if passed else 'FAIL','checks':checks,'before_sha256':failed['before_sha256'],'after_sha256':failed['after_sha256'],'original_message':messages,'sources':source_records,'war1_original':q.block(roots[1]['war'],'1'),'scope':'Exact refused native peace notification only, not generic permission for peace or territory changes.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
