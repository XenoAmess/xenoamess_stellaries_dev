import json,logging,re,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h=r.harness;run,user,m=h.load_run()
copy=run/Path(__file__).name;assert not copy.exists();shutil.copyfile(Path(__file__),copy)
b=json.loads((run/'rc9-external-bombard-task-ready.audit.json').read_text(encoding='utf-8'))
assert b['colonies']['24']['actual_pop_sum']==100 and b['colonies']['0']['actual_pop_sum']==7721
assert b['countries']['0']['native']['founder_species_ref']==3321888769
error=user/'logs/error.log';eb=error.read_bytes();(run/'rc9-external-bombard-prepare-error-before.log').write_bytes(eb)
ships=' '.join('create_ship = { name = "EEP-FIRE-'+str(i)+'" design = "NAME_Mindwarden_Battleship" }' for i in range(10))
commands=[
 'effect root = { save_global_event_target_as = eep_bombard_victim owner_main_species = { save_global_event_target_as = eep_bombard_species } }',
 'effect root = { create_country = { name = "EEP-FIRESTORM-ATTACKER" type = default auto_delete = no default_ships = no ignore_initial_colony_error = yes authority = auth_hive_mind civics = { civic = civic_hive_scorched_earth civic = civic_hive_ascetic } ethos = { ethic = ethic_gestalt_consciousness } species = event_target:eep_bombard_species graphical_culture = "mammalian_01" effect = { save_global_event_target_as = eep_bombard_attacker set_policy = { policy = orbital_bombardment option = orbital_bombardment_devastation cooldown = no } create_ship_design = { design = "NAME_Mindwarden_Battleship" } add_ship_design = last_created_design } } }',
 'effect root = { event_target:eep_bombard_attacker = { create_fleet = { name = "EEP-FIRESTORM-TEST" settings = { spawn_debris = no can_change_composition = no uses_naval_capacity = no } effect = { set_owner = event_target:eep_bombard_attacker '+ships+' set_location = { target = event_target:eep_native_purge_source distance = 10 angle = 0 } set_fleet_stance = passive set_fleet_bombardment_stance = firestorm save_global_event_target_as = eep_bombard_fleet } } declare_war = { target = event_target:eep_bombard_victim attacker_war_goal = wg_end_threat } } event_target:eep_bombard_fleet = { queue_actions = { orbit_planet = event_target:eep_native_purge_source } } }',
]
h.press_scan_code(0x29,'rc9-external-bombard-controlled-prepare-console-open',1)
for n,cmd in enumerate(commands):h.type_text(cmd,True,'rc9-external-bombard-controlled-prepare-'+str(n))
r.gpu_capture('rc9-external-bombard-controlled-prepare-native-receipt')
h.press_scan_code(0x29,'rc9-external-bombard-controlled-prepare-console-close',1)
# Country id is read from actual global target after native saving, not assumed.
a=r.native_save('rc9-external-bombard-controlled-attacker-prepared',b['date'],(0,))
actor=next(t['id'] for t in a['event_targets'] if t['name']=='eep_bombard_attacker')
fleet_id=next(t['id'] for t in a['event_targets'] if t['name']=='eep_bombard_fleet')
with zipfile.ZipFile(run/'rc9-external-bombard-controlled-attacker-prepared.sav') as z:state=z.read('gamestate').decode('utf-8-sig')
actor_raw=q.block(q.block(state,'country'),str(actor));fleet=q.block(q.block(state,'fleet'),str(fleet_id))
actor_audit=q.audit(run/'rc9-external-bombard-controlled-attacker-prepared.sav',(0,actor))
h.write_json(run/'rc9-external-bombard-controlled-attacker-prepared-all-actors.audit.json',actor_audit)
owned_raw=q.block(q.block(actor_raw,'fleets_manager'),'owned_fleets')
ids=q.ids(q.block(fleet,'ships'));all_ships=q.block(state,'ships');designs=q.block(state,'ship_design')
ship_records={str(i):q.block(all_ships,str(i)) for i in ids}
design_records={i:q.block(designs,str(q.scalars(q.block(v,'ship_design_implementation'))['design'])) for i,v in ship_records.items()}
war=q.block(state,'war')
war_matches=[]
for k,v,o in q.fields(war):
 if o:
  attackers=[int(i) for i in re.findall(r'\bcountry\s*=\s*(\d+)',q.block(v,'attackers'))]
  defenders=[int(i) for i in re.findall(r'\bcountry\s*=\s*(\d+)',q.block(v,'defenders'))]
  if actor in attackers and 0 in defenders:war_matches.append(k)
checks={
 'actor_is_new_country':actor!=0,
 'actor_valid_scorched_hive':'civic_hive_scorched_earth' in actor_audit['countries'][str(actor)]['government'] and 'auth_hive_mind' in actor_audit['countries'][str(actor)]['government'],
 'actor_not_eep_origin':'origin_heart_of_devouring' not in actor_audit['countries'][str(actor)]['government'],
 'actual_actor_owner':fleet_id in [int(i) for i in re.findall(r'\bfleet\s*=\s*(\d+)',owned_raw)],
 'actual10_battleships':len(ids)==10 and all(re.findall(r'\bship_size\s*=\s*"([^"]+)"',q.block(v,'growth_stages'))==['battleship'] for v in design_records.values()),
 'actual_firestorm_stance':q.scalars(fleet).get('ground_support_stance')=='firestorm',
 'actual_source_system78':q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate')).get('origin')==78,
 'orbit_source84_action_queued':bool(re.search(r'\borbit_planet\s*=\s*\{\s*planet\s*=\s*84\b',q.block(fleet,'actions'))),
 'war_with_country0_observed':bool(war_matches),
 'actual_source100_kept':a['colonies']['24']['actual_pop_sum']==100,
 'actual_mother7721_kept':a['colonies']['0']['actual_pop_sum']==7721,
 'victim_stock_same':a['countries']['0']['stockpile']==b['countries']['0']['stockpile'],
 'victim_eep_vars_same':a['countries']['0']['variables']==b['countries']['0']['variables'],
 'source_task_same':a['situations']==b['situations'],
 'original_core_binding':next(v for v in a['event_targets'] if v['name']=='eep_core0')['id']==1,
 'no_new_error_bytes':error.read_bytes()==eb,
}
ea=error.read_bytes();(run/'rc9-external-bombard-prepare-error-after.log').write_bytes(ea)
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','checks':checks,'actor_id':actor,'fleet_id':fleet_id,'save_sha256':a['save_sha256'],'actor_raw':actor_raw,'fleet_raw':fleet,'ship_records':ship_records,'design_records':design_records,'war_raw':war,'error_delta_bytes':len(ea)-len(eb),'scope':'Controlled country/free10 official battleships/location/war and actual firestorm preparation. No actual bombardment, unity reward or clearing claim.'}
h.write_json(run/'rc9-external-bombard-prepare-proof.json',proof)
print(json.dumps({k:v for k,v in proof.items() if k not in ['actor_raw','fleet_raw','ship_records','design_records','war_raw']}),flush=True)
assert all(checks.values())
