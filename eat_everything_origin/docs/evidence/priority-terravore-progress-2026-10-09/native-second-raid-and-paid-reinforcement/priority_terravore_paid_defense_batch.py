"""One recorded normal UI batch of twenty paid corvettes; no calendar or grants."""
import json,logging,shutil,subprocess,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
before='terravore-theory-year1-native-event-ack';after='terravore-defense-corvettes20-paid'
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
pre=json.loads((run/(before+'-native-voidworm-ack-proof.json')).read_text('utf-8'))
b=json.loads((run/(before+'.audit.json')).read_text('utf-8'))
assert pre['status']=='PASS_NATIVE_TERRAVORE_VOIDWORM_ACK_COMPONENT' and len(pre['checks'])==26 and all(v is True for v in pre['checks'].values())
assert pre['after_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and b['date']=='2236.04.01'
assert m['version']=='0.2.0' and m['language']=='l_simp_chinese'
frame=r.gpu_capture(after+'-before-order-UI');labels=[x['text'] for x in frame['rows']]
assert '\u62a4\u536b\u8230' in labels and any('90' in x for x in labels) and b['countries']['0']['effective_stockpile']['alloys']>=1800
eb=(user/'logs/error.log').read_bytes();(run/(after+'-error-before.log')).write_bytes(eb)
receipts=[]
for n in range(1,21):
 stage=after+'-click-'+str(n).zfill(2)
 result=subprocess.run([sys.executable,'_runtime/heart-of-devouring/record_current_helper.py',stage,'_runtime/heart-of-devouring/priority_native_ui_input_v3.py','left-click',stage,'565','403'],capture_output=True)
 print(result.stdout.decode('utf-8',errors='replace'),end='',flush=True);print(result.stderr.decode('utf-8',errors='replace'),end='',flush=True)
 assert result.returncode==0,'Original partial batch retained; do not rerun or issue remaining clicks blindly'
 receipts.append(stage)
r.gpu_capture(after+'-after-orders-UI')
a=r.native_save(after,b['date'],(0,));ea=(user/'logs/error.log').read_bytes();(run/(after+'-error-after.log')).write_bytes(ea)
proof={'status':'OBSERVED_NORMAL_UI_CORVETTE_BATCH','before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'click_stages':receipts,'observed_alloy_before_after':[b['countries']['0']['effective_stockpile']['alloys'],a['countries']['0']['effective_stockpile']['alloys']],'scope':'One normal twenty-click batch. Independent native payment/queue validation and later completion/warfare proof required; no full defense or crisis claim.'}
h.write_json(run/(after+'-observation.json'),proof);print(json.dumps(proof),flush=True)
