"""Documented recovery: event10 already verified in native save; never replay it."""
from pathlib import Path
import logging, sys, time, json
logging.disable(logging.INFO)
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'shishan_code_origin/tools/runtime_feedback.py').is_file())
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'shishan_code_origin/tools')]
import runtime_feedback as r
import audit_additive_runtime_matrix as audit
a,u,m=r.harness.load_run()
assert m['run_id']=='20261015T113522Z'
assert not (a/'econstable_F10_input.sav').exists()
prior=audit.extract_snapshot(a/'econstable_F10_after10_log_missing.sav')
assert audit.status_of(audit.core_guards('F00','input',prior))=='PASS'
log=u/'logs/game.log';offset=log.stat().st_size
r.console('event shishan_econ_probe.20','econstable_F10-recovery-event-20')
new=log.read_bytes()[offset:].decode('utf-8-sig')
r.harness.write_json(a/'econstable_F10-recovery-event-20-log.json',{'offset':offset,'new_game_log':new})
assert '_BLOCKED_' not in new
saved=r.native_save('econstable_F10_input')
assert 'date="2210.03.02"' in saved['meta']
snap=audit.extract_snapshot(Path(saved['archived']))
common=audit.extract_snapshot(a/'econstable_common_0302.sav')
checks=audit.core_guards('F10','input',snap)
setup_same=audit.equivalent(audit.employment_signature(snap),audit.employment_signature(common))
r.harness.write_json(a/'econstable_F10-actual-native-input-check.json',{'snapshot':snap,'core_checks':checks,'setup_all_jobs_match_common':setup_same})
assert audit.status_of(checks)=='PASS' and setup_same
print(json.dumps({'branch':'F10','phase':'input','sha256':saved['sha256']}),flush=True)
for phase,target in [('warm','2210.04.02'),('measured','2210.05.02')]:
    stage='econstable_F10_'+phase
    r.console('fast_forward 30',stage+'-advance')
    for i in range(15):
        time.sleep(2);f=r.capture(stage+'-wait-'+str(i));labels=[x['text'] for x in f['rows']]
        if target in labels and '暂停' in labels:break
    else:raise RuntimeError('date/pause not observed')
    if any('使用任何调试命令' in x or 'Fast Forwarded' in x for x in labels):
        r.harness.press_scan_code(0x29,stage+'-close-observed-console',1)
    saved=r.native_save(stage)
    assert 'date="'+target+'"' in saved['meta']
    print(json.dumps({'branch':'F10','phase':phase,'sha256':saved['sha256'],'date':target}),flush=True)
