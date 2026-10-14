import hashlib,json,shutil
from pathlib import Path
repo=Path.cwd().resolve()
pointer=json.loads((repo/'_runtime/heart-of-devouring/runs/current-run.json').read_text('utf-8'))
run=Path(pointer['artifact_dir'])
dest=repo/'eat_everything_origin/docs/evidence/terravore-paid-armies-and-repair-2026-10-14'
assert not dest.exists()
stems=['hope-route-mar22-recruit8-native-22940322','hope-route-aug01-salietto-orders-native-22940801','hope-route-aug01-salietto-confirm-native-22940801','hope-route-fauna-sep08-native-22940908']+[f'hope-route-wait-native-2294{month:02d}01' for month in range(4,10)]
names=set()
for stem in stems:
 for suffix in ['.sav','.audit.json','.native-save.json','-error-before.log','-error-after.log','-preflight.json','-calendar-receipt.json']:
  if (run/(stem+suffix)).is_file():names.add(stem+suffix)
 names.update(p.name for p in run.glob(stem+'*-proof.json'))
names.update(['hope-route-mar22-recruit8-guard-proof.json','hope-route-jul01-birth-reviewed-proof.json','hope-route-aug01-salietto-order-guard-proof.json','hope-route-aug01-salietto-order-guard-v2-proof.json','hope-route-aug01-order-raw-inspection.json','hope-route-jul01-repair-inventory.json','hope-route-sep01-ship-delta-inspection.json','hope-route-sep01-battle-reviewed-proof.json','hope-route-fauna-sep08-loss-reviewed-proof.json','hope-route-jun01-nearest-source-planning.json','hope-route-aug01-path-fleet-planning.json'])
frames=['hope-route-mar22-assault-tooltip-after','hope-route-jul01-select-transport-after','hope-route-aug01-dwell-right3-ui-after','hope-route-aug01-salietto-confirm-native-22940801-pre','hope-route-aug01-salietto-orders-native-22940801-ordered-3','hope-route-sep08-retreat-tooltip']
for stem in frames:names.update(stem+ext for ext in ['.jpg','.ocr.json'])
executions=['hope-route-mar22-recruit8-20261014','hope-route-mar22-recruit8-guard-20261014','hope-route-mar22-assault-tooltip-20261014','hope-route-jul01-select-transport-20261014','hope-route-jul01-birth-review-20261014','hope-route-aug01-salietto-orders-20261014','hope-route-aug01-salietto-confirm-save-20261014','hope-route-aug01-salietto-order-guard-20261014','hope-route-aug01-salietto-order-guard-v2-20261014','hope-route-aug01-dwell-right3-ui-20261014','hope-route-sep01-battle-review-20261014','hope-route-fauna-sep08-calendar-20261014','hope-route-fauna-sep08-guard-20261014','hope-route-fauna-sep08-loss-review-20261014','hope-route-sep08-retreat-tooltip-20261014']
executions += [f'hope-route-wait-batch{i}-20261014' for i in range(1,5)]
for month in range(4,10):
 for v in ['', '-v2']:
  stem=f'hope-route-wait-native-2294{month:02d}01-guard'+v
  if (run/(stem+'-execution.json')).is_file():executions.append(stem)
for stem in ['hope-route-aug01-reselect2','hope-route-aug01-reselect3','hope-route-aug01-dwell-right2','hope-route-aug01-dwell-right3']:
 executions.append(stem+'-20261014')
for stem in executions:
 names.update(stem+'-'+ext for ext in ['execution.json','stdout.txt','stderr.txt'])
 execution=json.loads((run/(stem+'-execution.json')).read_text('utf-8'))
 helper=Path(execution['command'][1]).name
 assert hashlib.sha256((run/helper).read_bytes()).hexdigest()==execution['helper_sha256']
 names.add(helper)
names.add('record_current_helper.py')
sources={name:run/name for name in names}
sources.update({'support-runtime.py':repo/'eat_everything_origin/tools/runtime.py','support-audit_save.py':repo/'eat_everything_origin/tools/audit_save.py','priority_terravore_native_state.py':repo/'_runtime/heart-of-devouring/priority_terravore_native_state.py','archive-helper.py':Path(__file__).resolve()})
assert all(p.is_file() for p in sources.values())
size=sum(p.stat().st_size for p in sources.values());assert shutil.disk_usage(repo).free>size*3+220_000_000
dest.mkdir();(dest/'.gitattributes').write_bytes(b'* binary\n');rows=[]
for name,source in sorted(sources.items()):
 data=source.read_bytes();sha=hashlib.sha256(data).hexdigest();target=dest/name
 target.write_bytes(data);assert hashlib.sha256(target.read_bytes()).hexdigest()==sha
 rows.append({'file':name,'bytes':len(data),'sha256':sha,'source':str(source)})
(dest/'source-snapshot.json').write_text(json.dumps({'files':len(rows),'bytes':size,'source_run':pointer,'manifest':rows,'scope':'Paid armies, monthly economy, repair and normal orders through08.01;09.01/08 combat observations preserved. Native09.11 still active and excluded. Not full-route acceptance.'},indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':'PASS_RAW_CHECKPOINT','files':len(rows),'bytes':size,'dest':str(dest)}),flush=True)
