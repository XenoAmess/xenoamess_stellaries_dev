"""Exact native engineering completion; preserve all15 unaffected monthly checks."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-project3-normal-month-22830601';after='terravore-project3-normal-month-22830701';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[s['countries']['0'] for s in [ba,aa]]
pre=load(before+'-remaining-labs-month-v8-proof.json');failed=load(after+'-remaining-labs-month-v8-proof.json');obs=load(after+'-construction-boundary-observation-v4.json')
xs=[load(st+'-execution.json') for st in [before+'-remaining-labs-guard-v8',after+'-remaining-labs-guard-v8',after+'-calendar',after+'-boundary-observation-v4']]
keys={'unused_physics_bank_engineering_tech_one_normal_research_tick','all_other_native_tech_fields_and_special_project_shapes_held','all_original61ships34fleets_same_birth_name_designs_no_revival','no_unreviewed_messages_pending_combat_or_war_changes'}
def queue(c,key):
 raw=c['research_queues'][key];ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]])
techs=lambda c:[q.unquote(v) for k,v,obj in q.fields(c['tech_status']) if k=='technology' and not obj]
source=h.GAME_EXE.parent/'common/technology/00_eng_tech.txt';preserved=run/'terravore-starbase4-native-00_eng_tech.txt'
impl=lambda state,i:q.scalars(q.block(state['ships'][i],'ship_design_implementation'))
changed={i for i in b['ships'] if impl(b,i)!=impl(a,i)};actual={'1','2','1049','16777910','67110450','117442177','50333283','50333369'}
upgrades={'33554923','16777746','33555519','50332791','50333147','50333149','83887852','1960','1961','1962'}
def exact_component_updates():
 for i in changed:
  old,new=impl(b,i),impl(a,i)
  for key in ['design','upgrade']:
   x,y=old.get(key),new.get(key)
   if x==y:continue
   if y==4294967295:return False
   ref=x if x!=4294967295 else old['design']
   if b['designs'][str(ref)].replace('SHIP_THRUSTER_1','SHIP_THRUSTER_2')!=a['designs'][str(y)]:return False
 return True
checks={k:v for k,v in failed['checks'].items() if k not in keys}
checks.update({
 'exact_native_thrusters_completion_auto_alloys2_and_original_records':len(pre['checks'])==len(failed['checks'])==19 and all(pre['checks'].values()) and {k for k,v in failed['checks'].items() if not v}==keys and [x['returncode'] for x in xs]==[0,1,0,0] and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs) and len(obs['checks'])==7 and all(obs['checks'].values()) and pre['after_sha256']==obs['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and obs['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')) and queue(bc,'engineering_queue')=={'progress':1217.53797,'technology':'tech_thrusters_2','date':'2282.03.02'} and queue(ac,'engineering_queue')=={'technology':'tech_alloys_2','date':'2283.06.02'} and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0 and abs(ac['research_stockpile']['physics_research']-bc['research_stockpile']['physics_research']-83.40097)<.00002,
 'only_one_native_tech_added_research_status_and_definition_source_held':techs(ac)==techs(bc)+['tech_thrusters_2'] and omit(bc['tech_status'],{'technology','level','last_increased_tech','alternatives','potential','engineering_queue','society_queue','stored_techpoints'})==omit(ac['tech_status'],{'technology','level','last_increased_tech','alternatives','potential','engineering_queue','society_queue','stored_techpoints'}) and q.scalars(ac['tech_status'])['auto_researching_engineering']=='yes' and h.sha256(source)==h.sha256(preserved)=='81ba55004e006bd7bdb280de4d10a372fe00a2d5807b0b18abce68be9b2781a5' and q.scalars(q.block(source.read_text('utf-8-sig'),'tech_thrusters_2'))['area']=='engineering',
 'all61ships34fleets_birth_name_held_only8_civil_actual10_upgrade_component_changes':set(b['ships'])==set(a['ships']) and len(a['ships'])==61 and set(b['fleets'])==set(a['fleets']) and len(a['fleets'])==34 and changed==actual|upgrades and exact_component_updates() and all(impl(b,i)['design']==impl(a,i)['design'] for i in set(b['ships'])-actual) and all(impl(b,i)['upgrade']==impl(a,i)['upgrade']==4294967295 for i in actual) and all(q.scalars(v)['construction_date']==q.scalars(a['ships'][i])['construction_date'] and q.block(v,'name')==q.block(a['ships'][i],'name') for i,v in b['ships'].items()),
 'only_native299_thrusters_completion_no_pending_war_or_combat':len(obs['new_country0_messages_raw'])==1 and q.scalars(obs['new_country0_messages_raw'][0])=={'type':'TECHNOLOGY_ORDER_FINISH_MESSAGE_TYPE','localization':'MESSAGE_TECHNOLOGY_RESEARCH_FINISH','receiver':0,'technology':'tech_thrusters_2','end':'2283.07.02','date':'2283.06.02','notification':299,'message_type':'none'} and not a['pending'] and q.block(b['roots']['war'],'1')==q.block(a['roots']['war'],'1') and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
})
passed=len(checks)==19 and all(v is True for v in checks.values());out=run/(after+'-native-thrusters2-design-review-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_NATIVE_THRUSTERS2_AND_DESIGN_MONTH' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'sources':[{'path':str(source),'preserved':preserved.name,'sha256':h.sha256(source)}],'boundaries':[],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Only observed completion and exact component changes. Overflow refund rule unconfirmed; no full route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
