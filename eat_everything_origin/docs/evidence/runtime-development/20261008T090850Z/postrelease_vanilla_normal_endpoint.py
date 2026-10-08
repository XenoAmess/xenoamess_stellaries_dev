"""Original month-117 branch with ordinary native unpause across the endpoint."""
import json,logging,re,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--vanilla']
import runtime as r
from postrelease_vanilla_raw_source import inspect
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['enabled_mods']==[]
shutil.copyfile(Path(__file__),run/Path(__file__).name)
src=run/'postvanilla-q20-m117.sav';alias=user/'save games/acceptance-fixtures/vanilla-ui.sav';assert not alias.exists();shutil.copyfile(src,alias);assert h.sha256(src)==h.sha256(alias)
r.native_load('vanilla-ui','postvanilla-normal-original117-load');b=r.native_save('postvanilla-normal-before','2209.10.02',(0,));assert b['situations']['11']['progress']==994.5
eb=(user/'logs/error.log').read_bytes();(run/'postvanilla-normal-error-before.log').write_bytes(eb)
f=r.gpu_capture('postvanilla-normal-paused-start');assert any(x['text']=='\u6682\u505c' for x in f['rows'])
width=f['resolution'][0]
for i in range(3):h.click_point(width-31,12,'postvanilla-normal-speed-plus-'+str(i))
h.press_scan_code(0x39,'postvanilla-normal-ordinary-unpause',1)
frames=[];seen=False
for i in range(30):
 if i:time.sleep(2)
 f=r.gpu_capture('postvanilla-normal-calendar-'+str(i));labels=[x['text'] for x in f['rows']];dates=[t for t in labels if re.fullmatch(r'2209\.\d\d\.\d\d',t)];seen=any('\u661f\u7403\u5df2\u541e\u566c' in t or '\u6211\u4eec\u8fd8\u662f\u5f88\u997f' in t for t in labels)
 frames.append({'image_sha256':f['image_sha256'],'dates':dates,'completion_option_seen':seen,'paused_label_seen':'\u6682\u505c' in labels});print(json.dumps(frames[-1]),flush=True)
 if seen or any(t>='2209.11.01' for t in dates):
  if '\u6682\u505c' not in labels:h.press_scan_code(0x39,'postvanilla-normal-ordinary-pause',1)
  break
else:
 h.press_scan_code(0x39,'postvanilla-normal-timeout-pause',1);raise RuntimeError('Normal native endpoint was not observed')
f=r.gpu_capture('postvanilla-normal-paused-end');dates=[x['text'] for x in f['rows'] if re.fullmatch(r'2209\.\d\d\.\d\d',x['text'])];assert len(dates)==1 and any(x['text']=='\u6682\u505c' for x in f['rows'])
a=r.native_save('postvanilla-normal-end',dates[0],(0,));raw=inspect(run/'postvanilla-normal-end.sav');ea=(user/'logs/error.log').read_bytes();(run/'postvanilla-normal-error-after.log').write_bytes(ea)
checks={'original117_bytes_loaded':h.sha256(alias)==h.sha256(src),'ordinary_endpoint_shattered':raw['source']['planet_class']=='pc_shattered','source_unowned':'owner' not in raw['source'],'no_live_native_task':not any(s.get('type')=='situation_terravore_consume_planet' and s.get('killed')!='yes' for s in a['situations'].values()),'no_EEP_variables':a['countries']['0']['variables']=={},'no_EEP_flags':a['countries']['0']['flags']=={},'AP_empty':a['countries']['0']['ascension_perks']==[],'no_new_errors':ea==eb}
proof={'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'actual_date':a['date'],'save_sha256':a['save_sha256'],'normal_completion_UI':'OBSERVED_PENDING_ACK' if seen else 'NOT_OBSERVED','frames':frames,'raw_final':raw,'scope':'Independent native ordinary-calendar month-117 branch; no injected progress, event or reward, not same continuous branch as fast-forward checkpoints.'};h.write_json(run/'postvanilla-normal-endpoint-proof.json',proof);print(json.dumps({k:v for k,v in proof.items() if k not in ['frames','raw_final']}),flush=True);assert all(checks.values())
