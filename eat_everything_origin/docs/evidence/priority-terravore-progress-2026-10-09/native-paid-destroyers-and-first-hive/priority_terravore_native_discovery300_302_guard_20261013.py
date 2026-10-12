"""Independent review of three real native discoveries at the stopped October endpoint."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-destroyer-first-upkeep-22840901';after='terravore-paid-destroyer-operating-22841001';b,a=[read_state(run,s) for s in [before,after]]
p=load(after+'-operating-month-proof.json');px=load(after+'-operating-month-guard-execution.json');ob=load(after+'-construction-boundary-observation-v4.json')
failed={'country_timers_exact_expiry_only_native_birth_flag_refresh','no_unknown_messages_pending_combat_wars_truces_or_orders'}
flags=lambda s:{k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
expected={k:dict(v,flag_days=v['flag_days']-30) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items()}
expected.update(built_artificial_ship=63540072,encountered_first_gateway=63539712,first_gateway=63539712,recent_first_contact_process_started={'flag_date':63539616,'flag_days':7174})
sources=[];texts={}
for rel in ['events/first_contact_events.txt','common/scripted_effects/first_contact_effects.txt','events/apocalypse_events.txt','events/timeline_events.txt','common/on_actions/00_on_actions.txt']:
 src=h.GAME_EXE.parent/rel;dest=run/('native-discovery300-302-'+src.name);assert not dest.exists();dest.write_bytes(src.read_bytes());texts[src.name]=src.read_text('utf-8-sig');sources.append({'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)})
def event(file,id):
 return next(v for k,v,obj in q.fields(texts[file]) if obj and q.scalars(v).get('id')==id)
fc=event('first_contact_events.txt','first_contact.1');gate=event('apocalypse_events.txt','apoc.1');timeline=event('timeline_events.txt','timeline.44')
options=lambda v:[raw for k,raw,obj in q.fields(v) if k=='option' and obj]
contacts={k:v for k,v,obj in q.fields(q.block(a['roots']['first_contacts'],'contacts')) if obj}
pending={q.scalars(v)['id']:v for v in a['pending']};news=ob['new_country0_messages_raw']
checks={k:v for k,v in p['checks'].items() if k not in failed}
checks.update({
 'original23_two_unknown_boundary_FAIL_actual1_source_SAV_retained':p['status']=='FAIL' and len(p['checks'])==23 and {k for k,v in p['checks'].items() if v is False}==failed and all(v is True for k,v in p['checks'].items() if k not in failed) and px['returncode']==1 and px['helper_sha256']=='2e5ca8ce78ec97a28f7e9ce0300da7946cdfb9d6005216f957d3b1ada97e2924'==h.sha256(Path(px['command'][1])) and p['before_sha256']==b['audit']['save_sha256']==h.sha256(run/(before+'.sav')) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(after+'.sav')),
 'only_exact_known_native_pending300_301_302_scopes':set(pending)=={300,301,302} and all(q.scalars(pending[eid])['event']=='first_contact.1' and q.scalars(pending[eid])['country']==0 and q.scalars(q.block(pending[eid],'scope'))['id']==contact and q.scalars(q.block(q.block(pending[eid],'scope'),'from'))['id']==country for eid,contact,country in [(300,64,26),(301,65,22)]) and q.scalars(pending[302])['event']=='apoc.1' and q.scalars(q.block(pending[302],'scope'))=={'type':'ship','id':1,'opener_id':4294967295,'random_allowed':'yes'} and q.scalars(q.block(q.block(pending[302],'scope'),'from'))['id']==107,
 'exact_contacts_unassigned80_and_native_country_types':all(q.scalars(contacts[str(i)])['owner']==0 and q.scalars(contacts[str(i)])['country']==country and q.scalars(contacts[str(i)])['leader']==4294967295 and q.scalars(contacts[str(i)])['days_left']==80 and q.scalars(contacts[str(i)])['date']=='2284.09.05' and q.scalars(q.block(contacts[str(i)],'event'))['player_event']==eid and q.scalars(q.block(a['roots']['country'],str(country)))['type']==typ for i,country,eid,typ in [(64,26,300,'neutral_faction'),(65,22,301,'enclave')]),
 'exact_native_discovery_flags_and_all_other_timers':flags(a)==expected,
 'only_three_matching_native_messages':len(news)==3 and {q.scalars(v).get('target_first_contact') for v in news if q.scalars(v).get('type')=='MESSAGE_FIRST_CONTACT_DISCOVERED'}=={64,65} and len([v for v in news if q.scalars(v).get('type')=='EVENT_MESSAGE_TYPE' and q.scalars(v).get('event')==302])==1,
 'old_foreign_gateway2_still_ruined_no_activation_or_gift':q.block(b['roots']['megastructures'],'2')==q.block(a['roots']['megastructures'],'2') and q.scalars(q.block(a['roots']['megastructures'],'2'))['type']=='gateway_ruined' and q.scalars(q.block(a['roots']['megastructures'],'2'))['owner']==1 and 2 in q.ids(q.block(q.block(a['roots']['galactic_object'],'107'),'megastructures')) and 'abandoned_gateway' in q.scalars(q.block(q.block(a['roots']['galactic_object'],'107'),'flags')) and q.scalars(a['ships']['1'])['construction_date']=='2200.01.01' and q.scalars(a['ships']['1'])['fleet']==1 and '"gateway"' in q.block(a['country'],'seen_bypass_types'),
 'native_source_options_empty_and_immediate_flags_only':len(options(fc))==len(options(gate))==1 and list(q.fields(options(fc)[0]))==[('name','INTERESTING',False)] and list(q.fields(options(gate)[0]))==[('name','INTRIGUING',False)] and 'set_first_contact_starting_stage = yes' in q.block(fc,'immediate') and 'years = 20' in q.block(texts['first_contact_effects.txt'],'set_first_contact_starting_stage') and 'set_country_flag = encountered_first_gateway' in q.block(gate,'immediate') and 'set_country_flag = first_gateway' in q.block(timeline,'immediate') and 'apoc.1' in q.block(texts['00_on_actions.txt'],'on_entering_system_first_time'),
 'all_other_message_boundary_terms_wars_truces_orders_combat_held':all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0),
 'native_source_originals_unfiltered_live_error_bound':m['language']=='l_simp_chinese' and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
})
passed=all(v is True for v in checks.values());out=run/(after+'-native-discovery300-302-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_DISCOVERY_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':p['before_sha256'],'after_sha256':p['after_sha256'],'date':a['audit']['date'],'sources':sources,'native_pending_raw':a['pending'],'native_messages_raw':news,'new_ship_ids':p['new_ship_ids'],'project3_progress':p['project3_progress'],'hive_work':p['hive_work'],'boundaries':['native_discovery300_302_ack_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Independent native investigation supplements21 unchanged business checks. Only normal acknowledgement authorized next; no calendar.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
