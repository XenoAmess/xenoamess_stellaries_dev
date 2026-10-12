"""Same-date acknowledgement of only three independently reviewed empty-effect native options."""
import json,logging,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-paid-destroyer-operating-22841001';after='terravore-native-discovery300-302-ack-22841001';b,a=[read_state(run,s) for s in [before,after]]
texts=[]
for stage in [before,after]:
 with zipfile.ZipFile(run/(stage+'.sav')) as z:texts.append(z.read('gamestate').decode('utf-8-sig'))
bt,at=texts;p=load(before+'-native-discovery300-302-proof.json');px=load(before+'-native-discovery300-302-guard-execution.json');sx=load(after+'-save-execution.json')
names=['terravore-gateway302-normal-ack-click','terravore-first-contact300-normal-ack-click','terravore-first-contact301-normal-ack-click'];clicks=[load(n+'-execution.json') for n in names]
checked=lambda x:x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
bc,ac=[{k:v for k,v,obj in q.fields(q.block(st['roots']['first_contacts'],'contacts')) if obj} for st in [b,a]]
skip={'player_event','open_player_event_selection_history','message','first_contacts','camera_focus'};removed=[v for v in b['messages'] if q.scalars(v).get('event') in [300,301,302]]
checks={
 'prior30PASS_actual0_originalSHA_and_source':len(p['checks'])==30 and all(v is True for v in p['checks'].values()) and checked(px) and p['after_sha256']==b['audit']['save_sha256'],
 'three_normal_clicks_actual0_after_review_before_save_sources':all(checked(x) for x in clicks+[sx]) and px['finished_at_utc']<clicks[0]['started_at_utc']<clicks[0]['finished_at_utc']<clicks[1]['started_at_utc']<clicks[1]['finished_at_utc']<clicks[2]['started_at_utc']<clicks[2]['finished_at_utc']<sx['started_at_utc'],
 'original_same_date_SAV_pair':b['audit']['date']==a['audit']['date']=='2284.10.01' and all(st['audit']['save_sha256']==h.sha256(run/(name+'.sav')) for st,name in [(b,before),(a,after)]),
 'only_pending300_301_302_consumed_no_unknown_event':{q.scalars(v)['id'] for v in b['pending']}=={300,301,302} and not a['pending'],
 'history_exact302_300_301_once_human1_option0':selected_history(at)==selected_history(bt)+[{'player_event':i,'human':1,'option':0} for i in [302,300,301]],
 'country_all_raw_and_all_audit_business_held':b['roots']['country']==a['roots']['country'] and all(v==a['audit'][k] for k,v in b['audit'].items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']),
 'all_other_top_level_ordered_raw_held_except_native_camera':omit(bt,skip)==omit(at,skip),
 'only_matching_event_message302_removed_contact_discoveries_held':len(removed)==1 and q.scalars(removed[0])['event']==302 and a['messages']==[v for v in b['messages'] if v not in removed],
 'contacts_only64_65_current_event_links_removed':set(bc)==set(ac) and all(v==ac[k] for k,v in bc.items() if k not in ['64','65']) and all(omit(bc[k],{'event'})==omit(ac[k],{'event'}) and q.scalars(q.block(bc[k],'event'))['player_event']==eid and not q.block(ac[k],'event') for k,eid in [('64',300),('65',301)]) and omit(b['roots']['first_contacts'],{'contacts'})==omit(a['roots']['first_contacts'],{'contacts'}),
 'all_native_sources_bound_empty_options_no_new_error_CN41':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in p['sources']) and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-discovery-ack-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_DISCOVERY300_302_ACKNOWLEDGEMENT' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'date':a['audit']['date'],'camera_before':[(v,obj) for k,v,obj in q.fields(bt) if k=='camera_focus'],'camera_after':[(v,obj) for k,v,obj in q.fields(at) if k=='camera_focus'],'boundaries':['paid_destroyer_operating_month_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Only three original empty-effect native acknowledgement options, same date and all business unchanged. Resume through independent month review.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
