import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
stem='rc9-stage2-original-fleet-hold-at-star'
b=json.loads((run/'rc9-stage2-original-war-real-sixmonths-all-actors.audit.json').read_text(encoding='utf-8'))
r.gpu_click_text('\u660e\u767d\u4e86\u3002',stem+'-native-tutorial-ack')
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
h.press_scan_code(0x29,stem+'-console-open',1)
h.type_text('effect root = { event_target:eep_stage2_enemy_world = { solar_system = { star = { save_global_event_target_as = eep_stage2_enemy_star } } } if = { limit = { exists = event_target:eep_stage2_enemy_star } event_target:eep_stage2_war_fleet = { clear_orders = yes queue_actions = { orbit_planet = event_target:eep_stage2_enemy_star } } } }',True,stem+'-native-original-fleet-star-order')
r.gpu_capture(stem+'-native-order-receipt');h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],(0,16777219))
with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
d={k:v for k,v,o in q.fields(t) if o};f=q.block(d['fleet'],'16778456')
checks={
 'actual_star651':next((v['id'] for v in a['event_targets'] if v['name']=='eep_stage2_enemy_star'),None)==651,
 'actual_orbit_star_action651':q.scalars(q.block(q.block(q.block(f,'actions'),'orbit_planet'),'orbitable')).get('planet')==651,
 'actual_original28_ships':len(q.ids(q.block(f,'ships')))==28,
 'actual_same_system53':q.scalars(q.block(q.block(f,'movement_manager'),'coordinate')).get('origin')==53,
 'both_stocks_same':all(a['countries'][str(i)]['stockpile']==b['countries'][str(i)]['stockpile'] for i in [0,16777219]),
 'actual_source1640_kept':a['colonies']['37']['actual_pop_sum']==1640,
 'actual_source_damage_same':a['planets']['660']['bombardment_damage']==b['planets']['660']['bombardment_damage'],
 'root_eep_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'root_eep_flags_same':a['countries']['0']['flags']==b['countries']['0']['flags'],
 'no_new_error_bytes':(user/'logs/error.log').read_bytes()==eb,
}
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':a['save_sha256'],'fleet_raw':f,'scope':'Ordinary movement of original military fleet to the same-system star to await original transport. No population/damage/resources/army/crisis grants.'}
h.write_json(run/(stem+'-proof.json'),proof);print(json.dumps({k:v for k,v in proof.items() if not k.endswith('_raw')}),flush=True);assert all(checks.values())
