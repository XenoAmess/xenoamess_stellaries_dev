import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
names=['production-only-preflight.json','formal-prod-initial-clean-identity.json','formal-prod-native-DLC-proof.json','formal-prod-intro-ack-proof.json','formal-prod-native-report-readonly-proof.json','formal-prod-report-repeat-readonly-proof.json','formal-prod-first-month-invariants-proof.json','formal-prod-native-month-stable-reloaded-proof.json']
sources={name:json.loads((run/name).read_text(encoding='utf-8')) for name in names}
assert all(v['status'] in ['PASS','PASS_SCOPED'] for v in sources.values())
copy_files,tree=h.tree_manifest(Path(m['copied_mod']));root_files,root_tree=h.tree_manifest(Path('eat_everything_origin/mod'));assert copy_files==root_files==sources['production-only-preflight.json']['production_files'];assert tree==root_tree==m['repository_mod_tree_sha256']
stop=h.stop(30);assert stop['forced'] is False and stop['running_after'] is False
error=(user/'logs/error.log').read_bytes();(run/'formal-prod-final-unfiltered-error.log').write_bytes(error);lines=[x for x in error.decode('utf-8-sig').splitlines() if x.strip()]
allowed=lambda x:('Could not find files for mod: C:\\SteamLibrary\\steamapps\\workshop\\content\\281990\\' in x) or ('Object with key: decision_lithoid_swarm_consume_world already exists' in x and 'common/decisions/zz_eep_native_decision.txt line: 2' in x)
checks={'all_eight_actual_components_pass':all(v['status'] in ['PASS','PASS_SCOPED'] for v in sources.values()),'all41_production_files_exact':len(root_files)==41 and copy_files==root_files,'no_testing_module':not any('eep_probe' in k or k.startswith('testing/') for k in root_files),
 'normal_stop':not stop['forced'] and not stop['running_after'],'entire_unfiltered_error_log_known_only':all(allowed(x) for x in lines),'no_wrong_scope':'Wrong scope for trigger' not in error.decode('utf-8-sig'),'no_invalid_scripted_effect':'Invalid scripted effect' not in error.decode('utf-8-sig')}
v={'status':'PASS' if all(checks.values()) else 'FAIL','version':'0.2.0','run_id':run.name,'language':'l_simp_chinese','scope':'Final production-only Scorched Hive smoke. Original-byte clean initial seed, actual DLC query, native Queen intro and report, actual month and stable native reload. Not a new random world or all-government acceptance.',
 'checks':checks,'production_files':root_files,'production_tree_sha256':tree,'game_exe_sha256':m['game_exe_sha256'],'normal_stop':stop,'source_proofs':[{'path':n,'sha256':h.sha256(run/n),'status':sources[n]['status']} for n in names],
 'component_boolean_checks':sum(len(x.get('checks',{})) for x in sources.values()),'initial_date':'2200.01.01','last_date':'2200.02.04','initial_population':5300,'last_population':5307,
 'full_error_sha256':h.sha256(user/'logs/error.log'),'full_error_bytes':len(error),'known_missing_workshop_lines':sum('Could not find files for mod:' in x for x in lines),'known_decision_override_lines':sum('Object with key:' in x for x in lines),
 'global_zero_error_claimed':False,'first_reload_full_object_failure_retained':'formal-prod-native-month-reloaded-v3-proof.json','failure_difference_record':'formal-prod-first-reload-differences.json'}
h.write_json(run/'formal-production-smoke-proof.json',v);print(json.dumps({k:v[k] for k in ['status','checks','component_boolean_checks','full_error_bytes','known_missing_workshop_lines','known_decision_override_lines']}),flush=True);assert all(checks.values())
