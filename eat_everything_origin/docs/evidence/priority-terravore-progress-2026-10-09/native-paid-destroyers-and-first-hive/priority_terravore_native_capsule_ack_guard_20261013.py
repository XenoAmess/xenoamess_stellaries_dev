"""Normal capsule ACK consumes299 and creates one unstarted native investigation project."""
import json,logging,re,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-storm-capsule-22840704';after='terravore-native-capsule-ack-22840704';b,a=[read_state(run,s) for s in [before,after]]
p=load(before+'-native-storm-capsule-proof.json');px=load(before+'-native-storm-capsule-guard-execution.json');click=load('terravore-capsule299-normal-ack-click-execution.json');sx=load(after+'-save-execution.json')
projects=lambda s:{q.scalars(v)['id']:v for k,v,obj in q.fields(q.block(s['country'],'events')) if obj and k=='special_project'};bp,ap=projects(b),projects(a);new={i:v for i,v in ap.items() if i not in bp}
history=lambda s:[q.scalars(v) for v in re.findall(r'\{([^{}]*)\}',s['roots']['open_player_event_selection_history'])]
removed=[v for v in b['messages'] if q.scalars(v).get('event')==299]
checks={
 'prior25PASS_actual0_source_SAV_click_after_guard':len(p['checks'])==25 and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and p['after_sha256']==b['audit']['save_sha256'] and click['started_at_utc']>px['finished_at_utc'],
 'normal_click_and_same_date_original_SAV_actual0':all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in [click,sx]) and b['audit']['date']==a['audit']['date']=='2284.07.04' and all(h.sha256(run/(stage+'.sav'))==s['audit']['save_sha256'] for s,stage in [(b,before),(a,after)]),
 'only_pending299_consumed_corresponding_message_removed':len(b['pending'])==1 and q.scalars(b['pending'][0])['id']==299 and not a['pending'] and len(removed)==1 and a['messages']==[v for v in b['messages'] if v not in removed],
 'history_only299_human1_option0':history(a)==history(b)+[{'player_event':299,'human':1,'option':0}],
 'country_all_non_project_raw_held':omit(b['country'],{'events'})==omit(a['country'],{'events'}),
 'original_four_projects_raw_held_only_one_new_investigation':len(bp)==4 and all(ap[i]==v for i,v in bp.items()) and len(new)==1 and set(new)=={10} and q.scalars(new[10])=={'id':10,'special_project':'STORM_IN_A_BOX_INVESTIGATE_PROJECT','ambient_object':218103972,'ai_research_date':'2284.08.01'} and q.block(new[10],'scope')==q.block(b['pending'][0],'scope') and q.scalars(q.block(new[10],'coordinate'))=={'type':2,'id':1070} and q.scalars(q.block(new[10],'carrier'))=={'type':'planet','reference':1070},
 'all_economy_research_POP_EEP_government_crisis_held':b['audit']['countries']['0']==a['audit']['countries']['0'] and all(b['audit'][k]==a['audit'][k] for k in ['colonies','pop_groups','pop_jobs','planets','districts','situations']),
 'all_owned_ships_fleets_orders_armies_buildings_held':all(b[k]==a[k] for k in ['ships','fleets','queues','items']) and all(b['roots'][k]==a['roots'][k] for k in ['army','zones','buildings','districts','deposit','situations','war','truce','first_contacts']),
 'CN_same41_package_error_no_new_bytes':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(user/'logs/error.log').read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-capsule-ack-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_CAPSULE299_ACK' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'new_project_raw':new,'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':27 if passed else 0,'scope':'One unstarted native project, no rewards; next27days only reaches next month with no research tick.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'new_project_scalars':{i:q.scalars(v) for i,v in new.items()}}),flush=True);assert passed
