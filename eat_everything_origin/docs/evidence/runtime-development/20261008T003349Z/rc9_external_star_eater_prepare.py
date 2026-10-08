import json
import logging
import re
from pathlib import Path
import shutil
import sys
import zipfile
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run()
shutil.copyfile(Path(__file__),run/Path(__file__).name)
b=json.loads((run/'rc9-external-star-task-ready.audit.json').read_text(encoding='utf-8'))
assert b['colonies']['24']['actual_pop_sum']==100
with zipfile.ZipFile(run/'rc9-external-star-task-ready.sav') as z:bs=z.read('gamestate').decode('utf-8-sig')
planets=q.block(q.block(bs,'planets'),'planet')
assert q.scalars(q.block(planets,'83'))['planet_class']=='pc_g_star'
assert q.scalars(q.block(q.block(planets,'83'),'coordinate')).get('origin')==78
assert q.scalars(q.block(q.block(planets,'84'),'coordinate')).get('origin')==78
assert q.scalars(q.block(q.block(planets,'1'),'coordinate')).get('origin')==5
h.press_scan_code(0x29,'rc9-external-star-create-console-open',1)
commands=[
 'effect root = { event_target:eep_native_purge_source = { solar_system = { every_system_planet = { limit = { is_star = yes } save_global_event_target_as = eep_external_star } } } }',
 'effect root = { create_ship_design = { design = "NAME_Crisis_Star_Eater" } add_ship_design = last_created_design create_fleet = { name = "EEP-STAR-TEST" settings = { spawn_debris = no can_change_composition = no uses_naval_capacity = no } effect = { set_owner = root create_ship = { name = "EEP-Star-Eater" design = "NAME_Crisis_Star_Eater" } set_location = { target = event_target:eep_external_star distance = 20 angle = 0 } set_fleet_stance = passive save_global_event_target_as = eep_external_star_fleet } } }',
]
for n,cmd in enumerate(commands):h.type_text(cmd,True,'rc9-external-star-controlled-prototype-'+str(n))
r.gpu_capture('rc9-external-star-create-native-receipt')
h.press_scan_code(0x29,'rc9-external-star-create-console-close',1)
a=r.native_save('rc9-external-star-eater-controlled-prepared',b['date'],(0,))
with zipfile.ZipFile(run/'rc9-external-star-eater-controlled-prepared.sav') as z:state=z.read('gamestate').decode('utf-8-sig')
fleet_id=next(v['id'] for v in a['event_targets'] if v['name']=='eep_external_star_fleet')
fleet=q.block(q.block(state,'fleet'),str(fleet_id))
allships=q.block(state,'ships') or q.block(state,'ship')
ships={k:v for k,v,o in q.fields(allships) if o and k.isdigit()}
owned=[]
for k,v,o in q.fields(fleet):
 if k=='ships' and o:owned.extend(str(i) for i in q.ids(v))
selected={k:ships[k] for k in owned if k in ships}
country_raw=q.block(q.block(state,'country'),'0')
owned_fleet_raw=q.block(q.block(country_raw,'fleets_manager'),'owned_fleets')
designs=q.block(state,'ship_design')
selected_designs={k:q.block(designs,str(q.scalars(q.block(v,'ship_design_implementation'))['design'])) for k,v in selected.items()}
checks={
 'real_star_target83':next(v for v in a['event_targets'] if v['name']=='eep_external_star')['id']==83,
 'actual_fleet_exists':bool(fleet),
 'actual_owner_country0':fleet_id in [int(v) for v in re.findall(r'\bfleet\s*=\s*(\d+)',owned_fleet_raw)],
 'actual_fleet_in_source_system78':q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate')).get('origin')==78,
 'actual_official_star_eater_ship_size':bool(selected_designs) and all(re.findall(r'\bship_size\s*=\s*"([^"]+)"',q.block(v,'growth_stages'))==['star_eater'] for v in selected_designs.values()),
 'actual_star_cracker_installed':any('PLANET_KILLER_STAR_CRACKER' in s for s in selected.values()),
 'source100_kept':a['colonies']['24']['actual_pop_sum']==100,
 'mother7721_kept':a['colonies']['0']['actual_pop_sum']==7721,
 'stockpiles_unchanged':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'ledger_unchanged':all(a['countries']['0']['variables'].get(k)==b['countries']['0']['variables'].get(k) for k in ['eep_c','eep_g','eep_d','eep_made','eep_worlds']),
 'no_ap_grant':a['countries']['0']['ascension_perks']==b['countries']['0']['ascension_perks'],
 'no_technology_grant':a['countries']['0']['completed_technologies']==b['countries']['0']['completed_technologies'],
 'no_crisis_grant':a['countries']['0']['crisis']==b['countries']['0']['crisis'],
}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'save_sha256':a['save_sha256'],'fleet_id':fleet_id,'fleet_raw':fleet,'ship_records':selected,'design_records':selected_designs,'scope':'Controlled free official Star Eater prototype near own non-core star. Not natural fifth-tier unlock, paid construction, actual weapon fire or completed external destruction.'}
h.write_json(run/'rc9-external-star-eater-prepare-proof.json',proof)
print(json.dumps({'checks':checks,'fleet_id':fleet_id,'ship_ids':list(selected),'save_sha256':a['save_sha256']}),flush=True)
assert all(checks.values())
