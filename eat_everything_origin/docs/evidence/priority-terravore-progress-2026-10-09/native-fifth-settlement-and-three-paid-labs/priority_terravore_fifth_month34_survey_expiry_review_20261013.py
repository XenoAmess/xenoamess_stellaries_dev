"""Exact original survey notice and one expired debris project; no economy exceptions."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-project3-normal-month-22830801';after='terravore-fifth-month34-22830901';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[s['countries']['0'] for s in [ba,aa]]
p=load(after+'-remaining-labs-month-v9-proof.json');obs=load(after+'-construction-boundary-observation-v4.json');x=load(after+'-remaining-labs-guard-v9-execution.json')
keys={'all_other_native_tech_fields_and_special_project_shapes_held','no_unreviewed_messages_pending_combat_or_war_changes'}
projects=lambda s:{q.scalars(v)['id']:v for k,v,obj in q.fields(q.block(s['country'],'events')) if obj and k=='special_project'}
bd,ad=projects(b),projects(a);msg=obs['new_country0_messages_raw']
checks={k:v for k,v in p['checks'].items() if k not in keys}
checks.update({
 'only_original_debris7_expires_after10days_other_projects_and_tech_held':len(p['checks'])==19 and {k for k,v in p['checks'].items() if not v}==keys and x['returncode']==1 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='770fe540a37fd1fe36c2de3decbccd4222f4e97e74dce01177295569d9f317aa' and bd.keys()-ad.keys()=={7} and not ad.keys()-bd.keys() and q.scalars(bd[7])=={'id':7,'days_left':10,'debris':33554436} and all(omit(v,{'days_left'})==omit(bd[i],{'days_left'}) and ('days_left' not in q.scalars(v) or q.scalars(v)['days_left']==q.scalars(bd[i])['days_left']-30) for i,v in ad.items()) and omit(bc['tech_status'],{'stored_techpoints','society_queue','engineering_queue'})==omit(ac['tech_status'],{'stored_techpoints','society_queue','engineering_queue'}) and p['before_sha256']==obs['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and p['after_sha256']==obs['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')) and ba['date']=='2283.08.01' and aa['date']=='2283.09.01',
 'only_original300_system24_survey_notice_no_pending_combat_war_changes':len(msg)==1 and q.scalars(msg[0])=={'type':'SYSTEM_SURVEYED','localization':'MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED','receiver':0,'target_system':24,'end':'2283.11.20','date':'2283.08.20','notification':300,'message_type':'none'} and q.scalars(q.block(q.block(a['fleets']['1'],'movement_manager'),'coordinate'))['origin']==24 and 'settings_survey=yes' in a['fleets']['1'] and not a['pending'] and q.block(b['roots']['war'],'1')==q.block(a['roots']['war'],'1') and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and len(obs['checks'])==7 and all(obs['checks'].values()) and load(after+'-calendar-execution.json')['returncode']==load(after+'-boundary-observation-v4-execution.json')['returncode']==0,
})
passed=len(checks)==19 and all(v is True for v in checks.values());out=run/(after+'-survey-expiry-reviewed-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_MONTH34_NATIVE_SURVEY_AND_EXPIRY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'boundaries':p['boundaries'],'project3_progress':p['project3_progress'],'front_lab_progress':p['front_lab_progress'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Original17 monthly checks retained. Only native survey notice and expired debris removed. Fifth settlement not yet accepted.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
