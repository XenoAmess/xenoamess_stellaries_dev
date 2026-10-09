import json,logging,re,shutil,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['version']=='0.2.0';shutil.copyfile(Path(__file__),run/Path(__file__).name)
stage='organic-purifier-growth-normal';b=json.loads((run/'organic-purifier-real-devour-terminal-day02.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes();(run/(stage+'-error-before.log')).write_bytes(eb)
f=r.gpu_capture(stage+'-actual-paused-start');labels=[x['text'] for x in f['rows']];assert b['date'] in labels and '\u6682\u505c' in labels
for i in range(3):h.click_point(f['resolution'][0]-31,12,stage+'-native-speed-plus-'+str(i))
h.press_scan_code(0x39,stage+'-ordinary-unpause',1);frames=[];seen=False
for i in range(30):
 if i:time.sleep(2)
 f=r.gpu_capture(stage+'-ordinary-observe-'+str(i));labels=[x['text'] for x in f['rows']];dates=[x for x in labels if re.fullmatch(r'2290\.\d\d\.\d\d',x)];seen='\u788e\u661f\u4e4b\u51a0' in labels and '\u8ba9\u4ed6\u4eec\u6210\u4e3a\u5730\u57fa\u3002' in labels
 row={'dates':dates,'queen_growth_seen':seen,'paused':'\u6682\u505c' in labels,'image_sha256':f['image_sha256']};frames.append(row);print(json.dumps(row),flush=True)
 if seen or any(x>='2290.02.01' for x in dates):
  if '\u6682\u505c' not in labels:h.press_scan_code(0x39,stage+'-ordinary-pause',1)
  break
else:
 h.press_scan_code(0x39,stage+'-timeout-pause',1);raise RuntimeError('Queen ordinary observation timeout')
f=r.gpu_capture(stage+'-actual-pending-UI');dates=[x['text'] for x in f['rows'] if re.fullmatch(r'2290\.\d\d\.\d\d',x['text'])];assert len(dates)==1 and '\u6682\u505c' in [x['text'] for x in f['rows']]
a=r.native_save(stage+'-pending',dates[0],(0,));c=a['countries']['0'];v=c['variables'];ea=(user/'logs/error.log').read_bytes();(run/(stage+'-error-after.log')).write_bytes(ea)
checks={'queen_native_UI_seen':seen,'actual_february_first':a['date']=='2290.02.01','no_second_economic_reward':all(v[k]==x for k,x in {'eep_c':27,'eep_g':27,'eep_d':8,'eep_made':400,'eep_worlds':2}.items()),'growth_stage_one':v['eep_stage']==1,'notice_pending_cleared':'eep_notice_pending' not in c['flags'],'AP_same':c['ascension_perks']==b['countries']['0']['ascension_perks'],'no_new_errors':eb==ea}
h.write_json(run/(stage+'-proof.json'),{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'save_sha256':a['save_sha256'],'actual_date':a['date'],'frames':frames,'scope':'Continuous ordinary native calendar/Queen growth pending UI only, ACK/reload still pending.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original ordinary observation FAIL retained'
