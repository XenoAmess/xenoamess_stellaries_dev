"""A single explicitly reviewed native empty-effect option, same-date original saves only."""
import json,logging,sys,zipfile
from pathlib import Path
before,after,eid,event,prior,execution,clickstage,option=sys.argv[1:];eid,option=int(eid),int(option);assert (event,option) in {('enclave.100',0),('utopia.2602',3)}
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
b,a=[read_state(run,s) for s in [before,after]];texts=[]
for stage in [before,after]:
 with zipfile.ZipFile(run/(stage+'.sav')) as z:texts.append(z.read('gamestate').decode('utf-8-sig'))
bt,at=texts;p=load(prior);px=load(execution+'-execution.json');click=load(clickstage+'-execution.json');sx=load(after+'-save-execution.json');checked=lambda x:x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
src=next(Path(v['path']) for v in p['sources'] if Path(v['path']).name==('utopia_on_action_events.txt' if event=='utopia.2602' else 'overlord_enclaves_events.txt'));ev=next(v for k,v,obj in q.fields(src.read_text('utf-8-sig')) if obj and q.scalars(v).get('id')==event);opts=[v for k,v,obj in q.fields(ev) if obj and k=='option']
skip={'player_event','open_player_event_selection_history','message','camera_focus'};removed=[v for v in b['messages'] if q.scalars(v).get('event')==eid]
checks={
 'reviewed_native_business_PASS_actual0_source_and_SAV':p['status'].startswith('PASS') and p['checks'] and all(v is True for v in p['checks'].values()) and checked(px) and p['after_sha256']==b['audit']['save_sha256'],
 'normal_click_and_save_actual0_source_in_order':checked(click) and checked(sx) and px['finished_at_utc']<click['started_at_utc']<click['finished_at_utc']<sx['started_at_utc'],
 'same_date_original_SAV_SHA_pair':b['audit']['date']==a['audit']['date'] and all(s['audit']['save_sha256']==h.sha256(run/(name+'.sav')) for s,name in [(b,before),(a,after)]),
 'native_unique_option_only_name_no_effects_sources_held':0<=option<len(opts) and all({k for k,v,obj in q.fields(opt)}<={'name','trigger'} for opt in opts) and (event!='utopia.2602' or len(opts)==4 and 'trait_psionic' in q.block(q.block(b['roots']['species_db'],'73'),'traits')) and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in p['sources']),
 'only_exact_pending_consumed':len(b['pending'])==1 and q.scalars(b['pending'][0])['id']==eid and q.scalars(b['pending'][0])['event']==event and not a['pending'],
 'history_exact_one_human1_option0':selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':option}],
 'all_country_raw_all_audit_business_held':b['roots']['country']==a['roots']['country'] and all(v==a['audit'][k] for k,v in b['audit'].items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']),
 'all_other_ordered_top_level_raw_held_except_native_camera':omit(bt,skip)==omit(at,skip),
 'only_matching_event_message_removed':len(removed)==1 and q.scalars(removed[0])['type']=='EVENT_MESSAGE_TYPE' and a['messages']==[v for v in b['messages'] if v not in removed],
 'CN41_and_unfiltered_errors_same':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-empty-native-ack-v2-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_EMPTY_EFFECT_ACKNOWLEDGEMENT' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'native_event':event,'player_event':eid,'boundaries':['paid_destroyer_operating_month_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Single normal previously independently reviewed empty native option. Business unchanged, month review required next.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
