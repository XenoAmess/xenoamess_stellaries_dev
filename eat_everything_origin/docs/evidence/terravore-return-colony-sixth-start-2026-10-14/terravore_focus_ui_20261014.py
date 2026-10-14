import json,logging,sys
stage,date=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run()
assert not list(run.glob(stage+'*'))
error=(user/'logs/error.log').read_bytes()
h.press_scan_code(0x10,stage+'-Q-focus',1)
frame=r.gpu_capture(stage+'-after')
assert date in [x['text'] for x in frame['rows']] and '暂停' in [x['text'] for x in frame['rows']]
assert (user/'logs/error.log').read_bytes()==error
print(json.dumps({'labels':[x['text'] for x in frame['rows']],'image_sha256':frame['image_sha256']},ensure_ascii=False),flush=True)
