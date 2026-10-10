"""Read-only actual native survey automation order, without economy or EEP mutation."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
 return a,roots,pending
b,br,bp=read(before);a,ar,ap=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bf={k:v for k,v,o in q.fields(br['fleet']) if o};af={k:v for k,v,o in q.fields(ar['fleet']) if o}
old,new=bf['1'],af['1'];osc,nsc=q.scalars(old),q.scalars(new)
allowed={'movement_manager','auto_movement','last_automation_settings','current_order','order_id'}
ofields={k:(v,o) for k,v,o in q.fields(old)};nfields={k:(v,o) for k,v,o in q.fields(new)}
changed={k for k in set(ofields)|set(nfields) if ofields.get(k)!=nfields.get(k)}
order=q.block(q.block(new,'current_order'),'automate_fleet_order');settings=q.scalars(order)
survey=q.block(q.block(order,'sub_order'),'survey_planet_order');holder=q.scalars(q.block(survey,'deposit_holder'))
bm,am=q.block(old,'movement_manager'),q.block(new,'movement_manager')
move_allowed={'target','target_coordinate','path','orbit','time_since_last_path_update'}
no_keys=['settings_anomalies','settings_astral_rifts','settings_digsites','settings_gravity_snares','do_special_projects','construct_mining_stations','construct_research_stations','construct_observation_posts']
automation=[q.unquote(t) for t,_,_ in q.tokens(q.block(new,'last_automation_settings'))]
checks={
 'same_actual_date':b['date']==a['date']=='2221.01.02',
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_pending':not bp and not ap,
 'all_countries_raw_held':br['country']==ar['country'],
 'all_actual_stocks_and_true_banks_held':bc['effective_stockpile']==ac['effective_stockpile'],
 'all_ships_raw_held':br['ships']==ar['ships'],
 'only_original_fleet1_changed':set(bf)==set(af) and [k for k in bf if bf[k]!=af[k]]==['1'],
 'exact_five_order_fields_changed':changed==allowed,
 'all_other_fleet1_fields_raw_held':[(k,v,o) for k,v,o in q.fields(old) if k not in allowed]==[(k,v,o) for k,v,o in q.fields(new) if k not in allowed],
 'native_next_order_counter':osc['order_id']==35 and nsc['order_id']==36 and settings.get('order_id')==35,
 'exact_explore_and_survey_only':automation==['AUTOMATION_EXPLORE','AUTOMATION_SURVEY'] and settings.get('settings_explore')==settings.get('settings_survey')=='yes' and all(settings.get(k)=='no' for k in no_keys),
 'single_automation_order':[(k,o) for k,v,o in q.fields(q.block(new,'current_order'))]==[('automate_fleet_order',True)],
 'real_zero_progress_survey_target59_in_system145':holder=={'type':0,'id':59} and q.scalars(survey).get('progress')==0 and any(k=='planet' and not o and q.unquote(v)==59 for k,v,o in q.fields(q.block(ar['galactic_object'],'145'))),
 'actual_original_position_and_noncommand_movement_raw_held':[(k,v,o) for k,v,o in q.fields(bm) if k not in move_allowed]==[(k,v,o) for k,v,o in q.fields(am) if k not in move_allowed],
 'new_path_and_target_system145':q.scalars(q.block(am,'target_coordinate')).get('origin')==145 and bool(q.block(q.block(am,'path'),'node')) and not q.block(am,'orbit').strip(),
 'old_arrived_auto_move_removed':q.scalars(q.block(old,'auto_movement'))=={'type':'auto_move_planet','auto_move_target':164,'clear_on_new_orders':'yes','has_arrived':'yes'} and not q.block(new,'auto_movement'),
 'error_original_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/'terravore-postsettlement-month-error-after.log').read_bytes()
}
for k in ['pop_groups','pop_jobs','colony','planets','buildings','districts','zones','deposit','construction','leaders','saved_event_target','species_db','situations']:
 checks[k+'_root_raw_held']=br[k]==ar[k]
p={'status':'PASS_NATIVE_SURVEY_AUTOMATION_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_fleet1_before_after':[old,new],'actual_stockpile':ac['effective_stockpile'],'scope':'Native survey order enabled for one existing ship; no actual arrival, colonization, second swallow or full civic route claim.'}
out=run/(after+'-survey-order-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({k:v for k,v in p.items() if k!='actual_fleet1_before_after'}),flush=True)
assert all(checks.values()),'Original native survey order FAIL retained; no next calendar'
