"""One documented native branch, never edit a .sav or repeat a mutation on timeout."""
import argparse
import json
import logging
from pathlib import Path
import sys
import time

logging.disable(logging.INFO)
REPO = next(p for p in Path(__file__).resolve().parents
            if (p/'shishan_code_origin/tools/runtime_feedback.py').is_file())
sys.path.insert(0, str(REPO / 'shishan_code_origin/tools'))
sys.path.insert(0, str(REPO / 'tools'))
import runtime_feedback as r
import audit_additive_runtime_matrix as audit

p = argparse.ArgumentParser()
p.add_argument('--run', required=True)
p.add_argument('--common', required=True)
p.add_argument('--date', required=True, help='common native date YYYY.MM.DD, day 1-3')
p.add_argument('--attempt',type=int,default=1)
p.add_argument('--branch', choices=['F00','F10','F01','F11','FP','FN','FH'], required=True)
args = p.parse_args()
year, month, day = map(int,args.date.split('.'))
assert 1 <= month <= 12 and 1 <= day <= 3
def plus_months(amount):
    total=year*12+month-1+amount
    return f'{total//12:04d}.{total%12+1:02d}.{day:02d}'
warm_date,measured_date=plus_months(1),plus_months(2)
a,u,m = r.harness.load_run()
assert m['run_id'] == args.run, 'different active run'
prefix = 'econstable_' + args.branch + (('_attempt'+str(args.attempt)) if args.attempt>1 else '')
assert not any((a/(prefix+'_'+phase+'.sav')).exists() for phase in ['input','warm','measured']), 'refuse branch replay'
r.harness.write_json(a/(prefix+'-driver-input.json'), vars(args))

def labels(frame):
    return [x['text'] for x in frame['rows']]

def exact(frame, text):
    q=[x for x in frame['rows'] if x['text']==text and x['score']>.75]
    assert len(q)==1, ('missing/ambiguous exact row',text,len(q))
    b=q[0]['box']
    return round(sum(t[0] for t in b)/4),round(sum(t[1] for t in b)/4)

for i in range(5):
    f=r.capture(prefix+'-open-menu-'+str(i))
    if '载入游戏' in labels(f):
        break
    r.harness.press_scan_code(1,prefix+'-menu-esc-'+str(i),1)
else:
    raise RuntimeError('native load menu unavailable')
if '读取存档' not in labels(f):
    r.click_text('载入游戏',prefix+'-open-load')
for i in range(8):
    f=r.capture(prefix+'-load-list-'+str(i))
    if args.common in labels(f):
        break
    r.harness.scroll(-1,1000,560,prefix+'-load-scroll-'+str(i),64)
else:
    raise RuntimeError('common native save row not found by bounded scrolling')
r.click_point(*exact(f,args.common),prefix+'-select-common')
r.click_text('读取存档',prefix+'-read-common')
for i in range(15):
    time.sleep(2)
    f=r.capture(prefix+'-load-wait-'+str(i))
    if args.date in labels(f) and '暂停' in labels(f):
        break
else:
    raise RuntimeError('common date/pause not observed')

events={'F00':[10],'F10':[10,20],'F01':[],'F11':[20],'FP':[20,30],'FN':[20,31],'FH':[20,32]}
for event in events[args.branch]:
    log=u/'logs/game.log'
    offset=log.stat().st_size
    r.console('event shishan_econ_probe.'+str(event),prefix+'-event-'+str(event))
    text=log.read_bytes()[offset:].decode('utf-8-sig')
    ready='SHISHAN_ECON_PROBE_'+str(event)+'_READY_' in text
    r.harness.write_json(a/(prefix+'-event-'+str(event)+'-native-log.json'),{'new_game_log':text,'offset':offset,'fresh_ready':ready,'status':'OBSERVED' if ready else 'PENDING_NATIVE_INPUT_AUDIT'})
    assert '_BLOCKED_' not in text, text[-1500:]

saved=r.native_save(prefix+'_input')
assert 'date="'+args.date+'"' in saved['meta']
snap=audit.extract_snapshot(Path(saved['archived']))
common=audit.extract_snapshot(a/(args.common+'.sav'))
checks=audit.core_guards(args.branch,'input',snap)
setup_same=audit.equivalent(audit.employment_signature(snap),audit.employment_signature(common))
r.harness.write_json(a/(prefix+'-actual-native-input-check.json'),{'snapshot':snap,'core_checks':checks,'setup_all_jobs_match_common':setup_same})
assert audit.status_of(checks)=='PASS' and setup_same, 'actual native input audit failed; do not advance'
print(json.dumps({'branch':args.branch,'phase':'input','sha256':saved['sha256']}),flush=True)
for phase,target in [('warm',warm_date),('measured',measured_date)]:
    stage=prefix+'_'+phase
    r.console('fast_forward 30',stage+'-advance')
    for i in range(15):
        time.sleep(2)
        f=r.capture(stage+'-wait-'+str(i))
        if target in labels(f) and '暂停' in labels(f):
            break
    else:
        raise RuntimeError('native target/pause not observed '+target)
    if any('使用任何调试命令' in x or 'Fast Forwarded' in x for x in labels(f)):
        r.harness.press_scan_code(0x29,stage+'-close-observed-console',1)
    saved=r.native_save(stage)
    assert 'date="'+target+'"' in saved['meta']
    print(json.dumps({'branch':args.branch,'phase':phase,'sha256':saved['sha256'],'date':target}),flush=True)
