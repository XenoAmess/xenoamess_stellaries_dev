"""Exact month start review for genuine C60 Queen and native fleet notifications."""
import json,logging,sys,zipfile
from pathlib import Path
execution_stage=sys.argv[1];sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from formal_production_native_calendar_checked_v3 import validate_native_interval
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
stage='terravore-native-crisis4145-acked';name=stage+'-native-crisis4145-ack-proof.json';pre=load(name);ex=load(stage+'-native-crisis4145-ack-guard-execution.json');au=load(stage+'.audit.json');c=au['countries']['0']
with zipfile.ZipFile(run/(stage+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
country=q.block(next(v for k,v,o in fs if k=='country' and o),'0');module=q.block(q.block(country,'modules'),'standard_event_module');projects=[v for k,v,o in q.fields(q.block(country,'events')) if k=='special_project' and o and q.scalars(v).get('special_project')=='CRISIS_SPECIAL_PROJECT_PSIONIC_2']
validate_native_interval(au['date'],'2278.11.01',26)
checks={
 'current_ACK15_actual0_fixed_source_and_same_SAV':len(pre['checks'])==15 and all(v is True for v in pre['checks'].values()) and ex['returncode']==0 and ex['helper_sha256']==h.sha256(Path(ex['command'][1]))=='ccccc87cffa8a5e61ce0f583f6da85438ff9ce30b83fb30e2ed078fa411704bf' and pre['after_sha256']==au['save_sha256']==h.sha256(run/(stage+'.sav'))=='2e272b75fc4b9f688094ff01e124e2affe00416736639ebc6526492182c6a40f',
 'settlement_credit_POP_capacity_held_Queen_pending':all(c['variables'].get(k)==v for k,v in {'eep_c':62,'eep_d':17,'eep_worlds':4,'eep_g':0,'eep_made':0,'eep_stage':1,'eep_crisis':1,'eep_fleet_stage':0,'eep_last_return':491}.items()) and c['owned_colonies']==[0] and c['effective_stockpile']['menace']==1635 and au['colonies']['0']['actual_pop_sum']==11920 and au['planets']['7']['variables']['eep_capacity_value']==17 and au['planets']['523']['planet_class']=='pc_shattered' and 'eep_notice_pending' in c['flags'],
 'project8_unstarted_native_level2_no_country_delays_or_pending':len(projects)==1 and q.scalars(projects[0])=={'id':8,'special_project':'CRISIS_SPECIAL_PROJECT_PSIONIC_2','ai_research_date':'2278.10.11'} and [(q.scalars('level='+v)['level'],o) for k,v,o in q.fields(q.block(country,'crisis_progression')) if k=='level']==[('crisis_level_1',False),('crisis_level_2',False)] and not any(k=='delayed_event' and o for k,v,o in q.fields(module)) and not any(k=='player_event' and o and q.scalars(v).get('country')==0 for k,v,o in fs),
 'only_exact_month_notice_business_boundary':pre['boundaries']==['queen_monthly_notice'] and pre['native_devour_calendar_ready'] is False and pre['maximum_days_to_native_bite_boundary']==0,
 'original_error41_020_CN':h.sha256(run/(stage+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb' and meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed=all(v is True for v in checks.values());out=run/(execution_stage+'-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':au['save_sha256'],'after_sha256':au['save_sha256'],'start_date':'2278.10.05','end_date':'2278.11.01','days':26,'maximum_days':26,'allowed_boundaries':pre['boundaries'],'execution_stage':execution_stage,'source_proof_file':name,'source_proof_sha256':h.sha256(run/name),'scope':'Only next monthly Queen and fleet notice boundary. No project start or mineral ship creation.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
