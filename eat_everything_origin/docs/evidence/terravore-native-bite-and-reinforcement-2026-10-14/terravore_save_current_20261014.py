import json,logging,re,sys
stage,date=sys.argv[1:]
assert re.fullmatch(r'hope-route-[a-z0-9-]+-native-\d{8}',stage)
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
assert not list(run.glob(stage+'*'))
frame=r.gpu_capture(stage+'-pre')
assert date in [x['text'] for x in frame['rows']] and '暂停' in [x['text'] for x in frame['rows']]
assert meta['language']=='l_simp_chinese' and h.tree_manifest(r.ROOT/'mod')[1]==meta['repository_mod_tree_sha256']
error=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(error)
saved=r.native_save(stage,date,(0,1,15))
after=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(after)
assert after==error
print(json.dumps({'date':saved['date'],'save_sha256':saved['save_sha256']}),flush=True)
