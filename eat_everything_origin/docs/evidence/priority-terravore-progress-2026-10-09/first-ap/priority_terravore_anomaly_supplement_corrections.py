"""Exact independent correction of two original read-only assumptions."""
import hashlib,json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
old=json.loads((run/'terravore-anomaly-month-supplement-proof.json').read_text(encoding='utf-8'))
b=json.loads((run/'terravore-clock-pause-recovered.audit.json').read_text(encoding='utf-8'))['countries']['0']
a=json.loads((run/'terravore-native-physics-deposit-ack.audit.json').read_text(encoding='utf-8'))['countries']['0']
eb=(run/'terravore-colonization-clock-probe-error-before.log').read_bytes();ea=(user/'logs/error.log').read_bytes()
checks={
 'original_14_true_and_only_two_expected_failures':old['status']=='FAIL' and sum(v is True for v in old['checks'].values())==14 and {k for k,v in old['checks'].items() if not v}=={'same_legal_government_AP_traditions','no_new_errors'},
 'only_exact_agenda_progress_changed':b['government'].replace('council_agenda_progress=2011.05','council_agenda_progress=2077.05')==a['government'] and b['government'].count('council_agenda_progress=2011.05')==1,
 'native_AP_and_traditions_held':a['ascension_perks']==b['ascension_perks'] and a['traditions']==b['traditions'],
 'actual_2842_log_held_byte_for_byte':eb==ea and len(ea)==2842 and hashlib.sha256(ea).hexdigest()=='3ce09316fe6b09950153d044616cafe4a12fcbc7d7241c0dda92548bfb978671',
 'stable_native_save_exact_original_ACK_bytes':(run/'terravore-anomaly-stable.sav').read_bytes()==(run/'terravore-native-physics-deposit-ack.sav').read_bytes(),
 'original_one_day_scope_retained':old['checks']['actual_one_day_month_boundary'] is True and old['before_sha256']=='b2ad3aa2f9ee9cb1e81fb9b7f7a494dfe5494d890a7314b59e056dbf1fd41cbd' and old['after_sha256']=='8f20eb361b7eaebe6a177c290d7a1b6e4bd7f6c58605d9e3a4351da36b4cc274'}
proof={'status':'PASS_STRICT_ANOMALY_MONTH_CORRECTIONS' if all(checks.values()) else 'FAIL','checks':checks,
       'scope':'Independent exact correction of agenda progress and actual log baseline; original FAIL retained. Not same-date ACK, clock or full route acceptance.'}
out=run/'terravore-anomaly-month-corrections-proof.json';assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True)
assert all(checks.values())
