"""Strict same-day empty-effect native ACK, with explicit original event and source."""
import json,logging,re,shutil,sys,zipfile
from pathlib import Path
before,after,event,eid,option,prior_file,prior_exec,source,source_sha,click_stage=sys.argv[1:];eid=int(eid);option=int(option)
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
b,bf,br=read(before);a,af,ar=read(after);pre=json.loads((run/prior_file).read_text('utf-8'));ex=json.loads((run/(prior_exec+'-execution.json')).read_text('utf-8'))
def selections(v):return re.findall(r'\{\s*player_event=(\d+)\s+human=(-?\d+)\s+option=(\d+)\s*\}',q.block(v,'selected'))
def retained(fs):return [(k,v,o) for k,v,o in fs if k!='open_player_event_selection_history' and not(k=='player_event' and o and q.scalars(v).get('id')==eid) and not(k=='message' and o and q.scalars(v).get('event')==eid)]
events=[v for k,v,o in q.fields(Path(source).read_text('utf-8-sig')) if o and q.scalars(v).get('id')==event];assert len(events)==1
options=[v for k,v,o in q.fields(events[0]) if k=='option' and o];selected=options[option]
checks={
 'same_date_original_SHA_pair':a['date']==b['date'] and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'prior_all_PASS_original_SHA_actual_exit0':pre['status'].startswith('PASS_') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and h.sha256(run/Path(ex['command'][1]).name)==ex['helper_sha256'],
 'all_other_ordered_top_raw_held':retained(bf)==retained(af),
 'unique_expected_native_pending_removed':len([v for k,v,o in bf if k=='player_event' and o and q.scalars(v).get('id')==eid and q.scalars(v).get('event')==event and q.scalars(v).get('country')==0])==1 and not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('id')==eid],
 'all_matching_event_messages_removed':not[v for k,v,o in af if k=='message' and o and q.scalars(v).get('event')==eid],
 'only_exact_native_choice_human1_appended':selections(ar['open_player_event_selection_history'])==selections(br['open_player_event_selection_history'])+[(str(eid),'1',str(option))],
 'all_countries_economy_research_EEP_raw_held':br['country']==ar['country'] and a['countries']==b['countries'],
 'all_ships_fleets_construction_planets_pop_species_raw_held':all(br[k]==ar[k] for k in ['ships','fleet','construction','planets','colony','pop_jobs','pop_groups','species_db']),
 'no_country0_pending':not[v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'native_source_SHA_bound':h.sha256(Path(source))==source_sha,
 'source_selected_option_has_no_effect_fields':all(k in {'name','trigger','allow','custom_gui','default_hide_option','exclusive_trigger','custom_tooltip'} for k,v,o in q.fields(selected)) and all(k=='custom_tooltip' for k,v,o in q.fields(q.block(events[0],'after'))),
 'normal_click_and_save_actual_exit0':all(json.loads((run/(st+'-execution.json')).read_text('utf-8'))['returncode']==0 for st in [click_stage,after+'-save']) and json.loads((run/(click_stage+'.action.json')).read_text('utf-8'))['action']=='left-click',
 'unfiltered_errors_exact_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_NATIVE_EMPTY_EFFECT_ACK_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_event':event,'native_player_event_id':eid,'native_option_index':option,'native_option_key':q.scalars(selected)['name'],'native_source':source,'native_source_sha256':source_sha,'calendar_ready':all(checks.values()),'scope':'Only explicit empty-effect native ACK, full same-day ordered state held except exact event/messages/one history addition. No rewards, upgrade or full-route claim.'}
out=run/(after+'-empty-ack-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert all(checks.values()),'Original native ACK FAIL retained'
