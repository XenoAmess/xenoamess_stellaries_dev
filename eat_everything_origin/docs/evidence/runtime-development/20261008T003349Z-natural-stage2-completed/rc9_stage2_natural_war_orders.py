import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run();copy=run/Path(__file__).name
assert not copy.exists();shutil.copyfile(Path(__file__),copy)
stem='rc9-stage2-existing-war-orders'
b=json.loads((run/'rc9-stage2-natural-war80-restored.audit.json').read_text(encoding='utf-8'))
assert b['date']=='2280.01.02' and b['countries']['0']['stockpile']['menace']==135
eb=(user/'logs/error.log').read_bytes();(run/(stem+'-error-before.log')).write_bytes(eb)
frame=r.gpu_capture(stem+'-paused-before-mode-check')
assert any(v['text']=='\u6682\u505c' for v in frame['rows'])
h.press_scan_code(0x29,stem+'-console-open',1)
def mode(frame):
 hits=[]
 for row in frame['rows']:
  found=re.search(r'human\s+a[il]\s*is\s+now\s+(ON|OFF)',row['text'],re.I)
  if found:hits.append((max(y for _,y in row['box']),found.group(1).upper(),row['text']))
 assert hits,frame['stage']
 return max(hits)
h.type_text('human_ai',True,stem+'-native-human-ai-mode-check')
f=r.gpu_capture(stem+'-native-human-ai-first-receipt');modes=[mode(f)]
if modes[-1][1]=='ON':
 h.type_text('human_ai',True,stem+'-native-human-ai-off')
 f=r.gpu_capture(stem+'-native-human-ai-off-receipt');modes.append(mode(f))
assert modes[-1][1]=='OFF'
cmd='effect root = { every_country = { limit = { is_at_war_with = root } save_global_event_target_as = eep_stage2_enemy every_owned_planet = { limit = { is_planet_class = pc_volcanic } planet = { save_global_event_target_as = eep_stage2_enemy_world } } } every_owned_fleet = { limit = { is_ship_class = shipclass_military fleet_power > 6000 } save_global_event_target_as = eep_stage2_war_fleet } event_target:eep_stage2_war_fleet = { clear_orders = yes queue_actions = { orbit_planet = event_target:eep_stage2_enemy_world } } }'
h.type_text(cmd,True,stem+'-native-existing-fleet-order')
r.gpu_capture(stem+'-native-order-receipt')
h.press_scan_code(0x29,stem+'-console-close',1)
a=r.native_save(stem,b['date'],(0,16777219))
with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
f=q.block(q.block(t,'fleet'),'16778456')
targets={v['name']:v['id'] for v in a['event_targets']}
checks={
 'actual_player0':q.block(t,'player').count('country=0')==1,
 'native_human_ai_off':modes[-1][1]=='OFF',
 'actual_enemy16777219':targets.get('eep_stage2_enemy')==16777219,
 'actual_enemy_world660':targets.get('eep_stage2_enemy_world')==660,
 'actual_original_fleet16778456':targets.get('eep_stage2_war_fleet')==16778456,
 'actual_original28_ships':len(q.ids(q.block(f,'ships')))==28,
 'actual_same_system53':q.scalars(q.block(q.block(f,'movement_manager'),'coordinate')).get('origin')==53,
 'actual_firestorm_kept':q.scalars(f).get('ground_support_stance')=='firestorm',
 'actual_enemy_orbit_action660':q.scalars(q.block(q.block(q.block(f,'actions'),'orbit_planet'),'orbitable')).get('planet')==660,
 'actual_enemy_population3155':a['colonies']['37']['actual_pop_sum']==3155,
 'root_stock_same':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'root_eep_variables_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'root_eep_flags_same':a['countries']['0']['flags']==b['countries']['0']['flags'],
 'root_actual_populations_same':all(a['colonies'][str(i)]['actual_pop_sum']==b['colonies'][str(i)]['actual_pop_sum'] for i in b['countries']['0']['owned_colonies']),
 'root_ap_same':a['countries']['0']['ascension_perks']==b['countries']['0']['ascension_perks'],
 'root_tech_same':a['countries']['0']['completed_technologies']==b['countries']['0']['completed_technologies'],
 'no_new_error_bytes':(user/'logs/error.log').read_bytes()==eb,
}
ea=(user/'logs/error.log').read_bytes();(run/(stem+'-error-after.log')).write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'mode_receipts':modes,'save_sha256':a['save_sha256'],'fleet_raw':f,'source_raw':q.block(q.block(q.block(t,'planets'),'planet'),'660'),'war_raw':q.block(t,'war'),'scope':'Actual existing natural war and ordinary orders to original ships; no free ships, resources, Menace, AP, crisis levels or notification grants.'}
h.write_json(run/(stem+'-proof.json'),proof)
print(json.dumps({k:v for k,v in proof.items() if not k.endswith('_raw')}),flush=True);assert all(checks.values())
