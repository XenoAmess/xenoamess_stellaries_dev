import json
import logging
from pathlib import Path
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime','--fixture']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,m=h.load_run()
copy=run/Path(__file__).name
assert not copy.exists()
shutil.copyfile(Path(__file__),copy)
start=json.loads((run/'rc9-focus-source-natural-development-330days.audit.json').read_text(encoding='utf-8'))
assert start['date']=='2223.12.02'
assert start['colonies']['24']['actual_pop_sum']==102
assert len(start['colonies']['24']['pop_groups'])==1
assert 'colonizing_species' not in start['colonies']['24']
assert set(start['countries']['0']['owned_colonies'])=={0,24}
h.press_scan_code(0x29,'rc9-focus-seed69-console-open',1)
cmd='effect root = { event_target:eep_core@this = { save_global_event_target_as = eep_seed69_mother } every_owned_planet = { limit = { is_capital = no } planet = { save_global_event_target_as = eep_native_purge_source every_owned_pop_group = { limit = { eep_founder_pop = yes } resettle_pop_group = { POP_GROUP = this PLANET = event_target:eep_seed69_mother AMOUNT = 33 } } } } }'
h.type_text(cmd,True,'rc9-focus-controlled-resettle33-to-original-mother')
h.type_text('effect root = { event_target:eep_native_purge_source = { if = { limit = { eep_source_valid = yes } log = "RC9_DEVELOPED_SOURCE_VALID_YES" } else = { log = "RC9_DEVELOPED_SOURCE_VALID_NO" } } }',True,'rc9-focus-seed69-source-valid-query')
r.gpu_capture('rc9-focus-seed69-native-resettle-receipt')
h.press_scan_code(0x29,'rc9-focus-seed69-console-close',1)
after=r.native_save('rc9-focus-developed-source69-before-begin','2223.12.02',(0,))
before_c,after_c=start['countries']['0'],after['countries']['0']
game_log=(user/'logs/game.log').read_bytes()
(run/'rc9-focus-seed69-full-game.log').write_bytes(game_log)
checks={
 'source_actual69':after['colonies']['24']['actual_pop_sum']==69,
 'mother_actual7752':after['colonies']['0']['actual_pop_sum']==7752,
 'total_population_conserved':sum(after['colonies'][str(i)]['actual_pop_sum'] for i in after_c['owned_colonies'])==7821,
 'source_development_not_reopened':'colonizing_species' not in after['colonies']['24'],
 'original_stockpiles_preserved':before_c['stockpile']==after_c['stockpile'],
 'original_ledger_preserved':before_c['variables']==after_c['variables'],
 'original_core_bindings_preserved':[{k:v for k,v in t.items()} for t in after['event_targets'] if t['name'] in ('eep_core0','eep_core_actor1')]==[{k:v for k,v in t.items()} for t in start['event_targets'] if t['name'] in ('eep_core0','eep_core_actor1')],
 'real_source_valid_after_move':b'RC9_DEVELOPED_SOURCE_VALID_YES' in game_log and b'RC9_DEVELOPED_SOURCE_VALID_NO' not in game_log,
 'no_task_yet':not any(s.get('type')=='situation_eep_devouring' for s in after['situations'].values()),
}
result={'status':'PASS_SCOPED' if all(checks.values()) else 'FAILED_PRECONDITION','scope':'Natural finished colony then controlled native33 resettlement; actual69 founder setup, no deletion or finished-flag grant. Not yet devouring waiting acceptance.','checks':checks,'before_sha256':start['save_sha256'],'after_sha256':after['save_sha256'],'date':after['date']}
h.write_json(run/'rc9-focus-developed-seed69-precondition-proof.json',result)
print(json.dumps(result,ensure_ascii=True),flush=True)
assert all(checks.values())
