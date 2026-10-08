import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
stem='rc9-external-bombard-player0-returned'
b=q.audit(run/'rc9-external-bombard-real-total270days.sav',(0,16777244))
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stem+'-console-open',1)
h.type_text('effect root = { event_target:eep_bombard_victim = { set_player = event_target:eep_bombard_attacker } }',True,stem+'-actual-player-return')
r.gpu_capture(stem+'-native-player-receipt')
h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],(0,16777244))
with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
co=q.block(q.block(t,'colony'),'24');f=q.block(q.block(t,'fleet'),'50331809')
checks={
 'actual_player0':q.block(t,'player').count('country=0')==1,
 'actual_source_population0':sum(q.scalars(q.block(q.block(t,'pop_groups'),str(i)))['size'] for i in q.ids(q.block(co,'pop_groups')))==0,
 'only_original_mother_owned':a['countries']['0']['owned_colonies']==[0],
 'no_live_eep_task':not any(v.get('type')=='situation_eep_devouring' and v.get('killed')!='yes' for v in a['situations'].values()),
 'source_flags_cleared':not ({'eep_active','eep_pending'}&set(a['planets']['84']['flags'])),
 'both_stocks_same':all(a['countries'][str(i)]['stockpile']==b['countries'][str(i)]['stockpile'] for i in [0,16777244]),
 'root_eep_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'root_eep_flags_same':a['countries']['0']['flags']==b['countries']['0']['flags'],
 'source_complete_same':a['planets']['84']==b['planets']['84'],
 'core_complete_same':a['planets']['1']==b['planets']['1'],
 'same_tasks':a['situations']==b['situations'],
 'same_targets':a['event_targets']==b['event_targets'],
 'same10_native_firestorm_ships':len(q.ids(q.block(f,'ships')))==10 and q.scalars(f).get('ground_support_stance')=='firestorm',
 'no_new_errors':(user/'logs/error.log').read_bytes()==eb,
}
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'date':a['date'],'save_sha256':a['save_sha256'],'before_sha256':b['save_sha256'],'source_colony_raw':co,'fleet_raw':f,'player_raw':q.block(t,'player'),'scope':'Actual firestorm clearing and return to original player; original controlled attacker preparation remains explicit. No claim of natural war or full release acceptance.'}
h.write_json(run/'rc9-external-bombard-real-clearing-proof.json',proof)
print(json.dumps({k:v for k,v in proof.items() if not k.endswith('_raw')}),flush=True);assert all(checks.values())
