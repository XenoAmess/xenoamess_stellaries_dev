"""Exact native enclave discovery; no extra economy or relaxed future events."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-society-construction-month-22840401';after='terravore-society-construction-month-22840501';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];old=load(after+'-society-construction-month-v4-proof.json');ox=load(after+'-society-construction-month-guard-v4-execution.json');ob=load(after+'-construction-boundary-observation-v4.json');dx=load('terravore-society-construction-next-six-months-v2-execution.json')
rawflags=lambda state:{k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(state['country'],'flags'))};expected={k:dict(v,flag_days=v['flag_days']-30) if isinstance(v,dict) and 'flag_days' in v else v for k,v in rawflags(b).items()};expected['recent_first_contact_process_started']={'flag_date':63536424,'flag_days':7191}
contact=q.block(q.block(a['roots']['first_contacts'],'contacts'),'63');sources=[]
for rel in ['common/scripted_effects/first_contact_effects.txt','events/first_contact_events.txt']:
 f=h.GAME_EXE.parent/rel;dest=run/('terravore-enclave-contact-native-'+f.name)
 if dest.exists():assert dest.read_bytes()==f.read_bytes()
 else:dest.write_bytes(f.read_bytes())
 sources.append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
checks={
 'original_V4_exact19PASS2FAIL_actual1_driver_stopped_no_June':len(old['checks'])==21 and [k for k,v in old['checks'].items() if v is not True]==['raw_country_timed_flags_only_minus30','no_pending_or_new_unreviewed_messages_combat_war_truce_changes'] and ox['returncode']==dx['returncode']==1 and ox['helper_sha256']==h.sha256(Path(ox['command'][1]))=='adb27f776010d0d7f2c3d9fc29052002496967907ec5bf94008d329aceed123c' and not(run/'terravore-society-construction-month-22840601.sav').exists(),
 'original_SAV_pair_calendar0_observer7PASS_actual0':ba['date']=='2284.04.01' and aa['date']=='2284.05.01' and old['before_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and old['after_sha256']==ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')) and len(ob['checks'])==7 and all(ob['checks'].values()) and all(load(after+suffix+'-execution.json')['returncode']==0 for suffix in ['-calendar','-boundary-observation-v4']),
 'only_new_contact63_enclave_stage_country7_unassigned80days':not q.block(q.block(b['roots']['first_contacts'],'contacts'),'63') and q.scalars(contact)=={'owner':0,'country':7,'location':0,'leader':4294967295,'date':'2284.04.22','last_roll':0,'days_left':80,'difficulty':3,'clues':0,'stage':'enclave_stage_1','status':'in_progress'} and q.scalars(q.block(contact,'flags'))=={'enclave_first_contact':63536424} and q.scalars(q.block(contact,'event'))['event_id']=='first_contact.1',
 'only_native_message305_exact_contact63_date':len(ob['new_country0_messages_raw'])==1 and q.scalars(ob['new_country0_messages_raw'][0])=={'type':'MESSAGE_FIRST_CONTACT_DISCOVERED','localization':'MESSAGE_FIRST_CONTACT_DISCOVERED_DESC','receiver':0,'target_first_contact':63,'end':'2284.07.22','date':'2284.04.22','notification':305,'message_type':'first_contact'} and not a['pending'],
 'only_recent_contact_timer_reset_native20years_minus9_all_other_minus30':rawflags(a)==expected and q.scalars(q.block(q.block(Path(sources[0]['path']).read_text('utf-8-sig'),'set_first_contact_starting_stage'),'hidden_effect'))=={} and 'recent_first_contact_process_started' in Path(sources[0]['path']).read_text('utf-8-sig'),
 'all19_original_economy_research_growth_assets_checks_PASS':sum(v is True for v in old['checks'].values())==19 and not old['boundaries'] and old['project3_progress']==1144.52163 and old['conversion_work']==294 and not a['pending'],
 'CN41_native_sources_error627_exact_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-enclave-contact-review-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_NATIVE_ENCLAVE_CONTACT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'sources':sources,'contact63_raw':contact,'message_raw':ob['new_country0_messages_raw'],'scope':'Exact discovery pair only; no future contact completion or Mod route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
