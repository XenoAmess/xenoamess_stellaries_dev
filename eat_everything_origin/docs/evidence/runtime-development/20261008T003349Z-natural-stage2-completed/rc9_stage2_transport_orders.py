import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();copy=run/Path(__file__).name
assert not copy.exists();shutil.copyfile(Path(__file__),copy)
stem='rc9-stage2-original-transport-orders'
b=json.loads((run/'rc9-stage2-war-real-firstmonth.audit.json').read_text(encoding='utf-8'))
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stem+'-console-open',1)
h.type_text('effect root = { every_owned_fleet = { limit = { is_ship_class = shipclass_transport fleet_power > 800 } save_global_event_target_as = eep_stage2_transport } event_target:eep_stage2_transport = { clear_orders = yes queue_actions = { orbit_planet = event_target:eep_stage2_enemy_world } } }',True,stem+'-native-original-transport-orders')
r.gpu_capture(stem+'-native-order-receipt')
h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],(0,16777219))
with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
f=q.block(q.block(t,'fleet'),'880');targets={v['name']:v['id'] for v in a['event_targets']}
ba=q.audit(run/'rc9-stage2-war-real-firstmonth.sav',(0,16777219))
checks={
 'actual_original_transport880':targets.get('eep_stage2_transport')==880,
 'actual_original20_transport_ships':len(q.ids(q.block(f,'ships')))==20 and q.scalars(f).get('ship_class')=='shipclass_transport',
 'actual_enemy_world660':targets.get('eep_stage2_enemy_world')==660,
 'actual_enemy_orbit_action660':q.scalars(q.block(q.block(q.block(f,'actions'),'orbit_planet'),'orbitable')).get('planet')==660,
 'both_stock_same':all(a['countries'][str(i)]['stockpile']==ba['countries'][str(i)]['stockpile'] for i in [0,16777219]),
 'root_eep_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'root_eep_flags_same':a['countries']['0']['flags']==b['countries']['0']['flags'],
 'all_owned_actual_populations_same':all(a['colonies'][str(i)]['actual_pop_sum']==ba['colonies'][str(i)]['actual_pop_sum'] for i in ba['countries']['16777219']['owned_colonies']+ba['countries']['0']['owned_colonies']),
 'root_ap_same':a['countries']['0']['ascension_perks']==b['countries']['0']['ascension_perks'],
 'root_tech_same':a['countries']['0']['completed_technologies']==b['countries']['0']['completed_technologies'],
 'no_new_error_bytes':(user/'logs/error.log').read_bytes()==eb,
}
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':a['save_sha256'],'fleet_raw':f,'scope':'Ordinary movement orders to original existing 20 transport ships only; no land/occupation or new army grants.'}
h.write_json(run/(stem+'-proof.json'),proof)
print(json.dumps({k:v for k,v in proof.items() if not k.endswith('_raw')}),flush=True);assert all(checks.values())
