import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();copy=run/Path(__file__).name
assert not copy.exists();shutil.copyfile(Path(__file__),copy)
stem='rc9-external-bombard-native-player-orders'
b=q.audit(run/'rc9-external-bombard-player-reordered.sav',(0,16777244))
assert b['date']=='2223.12.24'
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stem+'-console-open',1)
h.type_text('effect root = { event_target:eep_bombard_attacker = { set_player = event_target:eep_bombard_victim } }',True,stem+'-actual-player-switch')
h.type_text('effect root = { event_target:eep_bombard_fleet = { clear_orders = yes queue_actions = { orbit_planet = event_target:eep_native_purge_source } } }',True,stem+'-actual-orbit-order')
r.gpu_capture(stem+'-native-command-receipt')
h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],(0,16777244))
with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
f=q.block(q.block(t,'fleet'),'50331809')
checks={
 'actual_player16777244':q.block(t,'player').count('country=16777244')==1,
 'same10_real_ships':len(q.ids(q.block(f,'ships')))==10,
 'same_actual_firestorm':q.scalars(f).get('ground_support_stance')=='firestorm',
 'actual_orbit_action84':q.scalars(q.block(q.block(q.block(f,'actions'),'orbit_planet'),'orbitable')).get('planet')==84,
 'victim_population_same':a['colonies']['24']['actual_pop_sum']==b['colonies']['24']['actual_pop_sum'] and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum'],
 'both_stocks_same':all(a['countries'][str(i)]['stockpile']==b['countries'][str(i)]['stockpile'] for i in [0,16777244]),
 'victim_eep_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'source_task_same':a['situations']==b['situations'],
 'no_new_errors':(user/'logs/error.log').read_bytes()==eb,
}
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'before_sha256':b['save_sha256'],'save_sha256':a['save_sha256'],'fleet_raw':f,'player_raw':q.block(t,'player'),'error_delta_bytes':len(ea)-len(eb),'scope':'Actual player switch and ordinary order to the same controlled native fleet only; no bombardment completion claim.'}
h.write_json(run/(stem+'-proof.json'),proof)
print(json.dumps({k:v for k,v in proof.items() if k not in ['fleet_raw','player_raw']}),flush=True)
assert all(checks.values())
