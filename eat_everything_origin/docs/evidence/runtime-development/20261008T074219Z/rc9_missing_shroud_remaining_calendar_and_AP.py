import json,logging,shutil,subprocess,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime','--fixture'];import runtime as r
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();assert m['dlc_variant']=='shroud';dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(Path(__file__),dest)
base=Path('_runtime/heart-of-devouring');prefix='rc9-missing-shroud-native-Q8-'
start=prefix+'month12';a=json.loads((run/(start+'.audit.json')).read_text(encoding='utf-8'));assert a['date']=='2201.01.02' and a['countries']['0']['variables']['eep_c']==0
for date,stage,days in [('2201.08.02','month19',210),('2201.09.02','month20',30),('2201.10.02','first-notice-month',30)]:
 result=subprocess.run([sys.executable,str(base/'rc9_missing_dlc_native_calendar.py'),start,date,prefix+stage,str(days)]);assert result.returncode==0;start=prefix+stage
result=subprocess.run([sys.executable,str(base/'rc9_missing_dlc_completed_replay.py'),start]);assert result.returncode==0
result=subprocess.run([sys.executable,str(base/'rc9_missing_dlc_native_AP_open.py')]);assert result.returncode==0
result=subprocess.run([sys.executable,str(base/'rc9_browse_native_missing_dlc_AP_list_v3.py')]);assert result.returncode==0
print('Native calendar/replays/list complete, pending human visual review and final native UI stock check.',flush=True)
