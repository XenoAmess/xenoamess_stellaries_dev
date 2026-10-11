"""Read-only exact native cutholoid first acknowledgement, pending264 retained."""
import json, logging, re, sys, zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv=['runtime']
import runtime as r, audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO)
h=r.harness;run,user,metadata=h.load_run()
before='terravore-dual-build2-step2';after='terravore-third-battle-cutholoid-first-ack'
def load(name):return json.loads((run/name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    fs=list(q.fields(t));return load(stage+'.audit.json'),t,fs,{k:v for k,v,o in fs if o}
def omit(text,keys):return [(k,v,o) for k,v,o in q.fields(text) if k not in keys]
def objs(text):return {k:v for k,v,o in q.fields(text) if o}
def compact(text):return re.sub(r'\s+','',text)
b,bt,bf,br=read(before);a,at,af,ar=read(after)
pre=load(before+'-war1-battle-v54-proof.json');ex=load(before+'-battle-v54-execution.json')
bp=[v for k,v,o in bf if k=='player_event'];ap=[v for k,v,o in af if k=='player_event']
target=[v for v in bp if q.scalars(v).get('id')==265]
bm=[v for k,v,o in bf if k=='message'];am=[v for k,v,o in af if k=='message']
removed=[v for v in bm if q.scalars(v).get('event')==265 and q.scalars(v).get('receiver')==0]
bcs,acs=[objs(top['country']) for top in [br,ar]];bc,ac=bcs['0'],acs['0']
bmods,amods=[q.block(c,'modules') for c in [bc,ac]]
be,ae=[q.block(c,'standard_event_module') for c in [bmods,amods]]
bd,ad=[[v for k,v,o in q.fields(c) if k=='delayed_event'] for c in [be,ae]]
new=[v for v in ad if v not in bd]
bfc,afc=[top['first_contacts'] for top in [br,ar]]
bcontacts,acontacts=[objs(q.block(c,'contacts')) for c in [bfc,afc]]
bcontact,acontact=bcontacts['16777275'],acontacts['16777275']
native={
 'events/grand_archive_events.txt':'1e3f769c1693d1cee3c137708f84eafebbbfedd726bc730eb41999b49f1c5ccf',
 'events/on_action_events_2.txt':'0a7ab4c043e3447f122fa48bc9baf74604cfb4d8236f1acd10f65f65de963e6a',
 'events/timeline_events.txt':'0474977cfe30c61d28c1852c2e522ec409b3cd127a2c1f97859e6e1aa30f93a2',
 'events/story_events.txt':'1ac49a4b66d1fb07192552e5af6d4d14dd0db7d1d6f0fb977cc6a2a9274b0055',
 'common/first_contact/01_first_contact_space_fauna_and_NPCs.txt':'cd650c3bdb80e27ef7318d31ef76c69475b38ea4601b39d6fe88e874485e6b08'}
ev=[v for k,v,o in q.fields((h.GAME_EXE.parent/'events/grand_archive_events.txt').read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='grand_archive.2800'][0]
opts=[v for k,v,o in q.fields(ev) if k=='option']
checks={
 'original_actual_date_and_SHA_pair':a['date']==b['date']=='2271.10.12' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior87_PASS_actual0_original_source':pre['status'].startswith('PASS_') and len(pre['checks'])==87 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v54.py')=='0dea27f03242d11f8836bc64ce2e385eeb859b4f2521ddf226ca4dc79fb36eef',
 'original_native_sources_and_option':all(h.sha256(h.GAME_EXE.parent/f)==sha and h.sha256(run/('native-third-battle-pending-'+Path(f).name))==sha for f,sha in native.items()) and len(opts)==1 and q.scalars(opts[0])=={'name':'grand_archive.2800.a','set_first_contact_starting_stage':'yes'},
 'only_pending265_removed_264_raw_held':len(target)==1 and q.scalars(target[0]).get('event')=='grand_archive.2800' and q.scalars(q.block(target[0],'scope')).get('id')==16777275 and ap==[v for v in bp if v not in target] and [(q.scalars(v)['id'],q.scalars(v)['event']) for v in ap if q.scalars(v).get('country')==0]==[(264,'grand_archive.2800')],
 'exact_native_history265_option0':selected_history(at)==selected_history(bt)+[{'player_event':265,'human':1,'option':0}],
 'all_other_top_level_ordered_raw_held':[(k,v,o) for k,v,o in bf if k not in {'country','first_contacts','message','player_event','open_player_event_selection_history','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','first_contacts','message','player_event','open_player_event_selection_history','random_count'}],
 'only_exact_original_notice265_removed':len(removed)==1 and q.scalars(removed[0]).get('type')=='EVENT_MESSAGE_TYPE' and am==[v for v in bm if v not in removed],
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(acs[i]==v for i,v in bcs.items() if i!='0'),
 'country0_except_precise_flags_and_delayed_raw_held':omit(bc,{'flags','modules'})==omit(ac,{'flags','modules'}),
 'country0_only_exact_recent_first_contact_expiry':omit(q.block(bc,'flags'),{'recent_first_contact_process_started'})==omit(q.block(ac,'flags'),{'recent_first_contact_process_started'}) and q.scalars(q.block(q.block(bc,'flags'),'recent_first_contact_process_started'))=={'flag_date':63365856,'flag_days':4603} and q.scalars(q.block(q.block(ac,'flags'),'recent_first_contact_process_started'))=={'flag_date':63428184,'flag_days':7200},
 'country0_only_native_story7_delayed_added':omit(bmods,{'standard_event_module'})==omit(amods,{'standard_event_module'}) and omit(be,{'delayed_event'})==omit(ae,{'delayed_event'}) and len(new)==1 and ad==bd+new and q.scalars(new[0])=={'event':'story.7','days':1} and compact(q.block(new[0],'scope'))=='type=countryid=0opener_id=4294967295random={01002395182}random_allowed=yesfrom={type=countryid=36opener_id=4294967295random={01332352412}random_allowed=yes}',
 'all_other_contacts_and_root_fields_raw_held':set(bcontacts)==set(acontacts) and all(acontacts[i]==v for i,v in bcontacts.items() if i!='16777275') and omit(bfc,{'contacts'})==omit(afc,{'contacts'}),
 'contact_only_exact_known_fields_changed':omit(bcontact,{'stage','difficulty','event','flags','completed'})==omit(acontact,{'stage','difficulty','event','flags','completed'}),
 'native_stage_and_difficulty_transition':q.scalars(bcontact)['stage']=='base_contact_set' and q.scalars(acontact)['stage']=='cutholoids_stage_1' and q.scalars(bcontact)['difficulty']==2 and q.scalars(acontact)['difficulty']==3,
 'active_event264_removed_events_array_held':q.scalars(q.block(bcontact,'event')).get('player_event')==264 and not q.block(acontact,'event') and q.block(bcontact,'events')==q.block(acontact,'events'),
 'contact_precise_flag_and_completed_stage':not q.block(bcontact,'flags') and q.scalars(q.block(acontact,'flags'))=={'cutholoids_first_contact':63428184} and not q.block(bcontact,'completed') and compact(q.block(acontact,'completed'))=='{date="2271.10.12"stage="base_contact_set"}',
 'native_random_counter_single_increment':q.scalars(bt)['random_count']==231697426 and q.scalars(at)['random_count']==231697427,
 'unfiltered_error_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
action=load(after+'-click.action.json')
checks['normal_click_and_native_save_actual0']=action['action']=='left-click' and action['client_point']==[510,500] and action['foreground_after']==action['expected_hwnd'] and all(load(s+'-execution.json')['returncode']==0 for s in [after+'-click',after+'-native-save'])
for k in ['effective_stockpile','variables','government','traditions','ascension_perks','tech_status','budget_categories','research_stockpile']:
    checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:
    checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_CUTHOLOID_FIRST_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'remaining_country0_pending':[[264,'grand_archive.2800']],'calendar_ready':False,'native_sources':native,'scope':'Normal first acknowledgement265 only;264 pending;not contact completion/full route.'}
for k in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids','actual_pending_destroyed_ship_ids','actual_naval_death_cache_credit','actual_alive_military_ship_ids']:proof[k]=pre[k]
out=run/(after+'-cutholoid-first-ack-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v],'after_sha256':a['save_sha256']}),flush=True)
assert all(checks.values()),'Original cutholoid first acknowledgement FAIL retained'
