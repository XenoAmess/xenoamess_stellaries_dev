"""Exact string-token civic check supplement; original numeric-parser failure retained."""
import json,logging,shutil,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
old=json.loads((run/'terravore-legal-initial-proof.json').read_text(encoding='utf-8'))
a=json.loads((run/'terravore-legal-initial-pending.audit.json').read_text(encoding='utf-8'))
government=a['countries']['0']['government'];tokens=[q.unquote(t) for t,_,_ in q.tokens(q.block(government,'civics'))]
gov=q.scalars(government)
f=json.loads((run/'priority-terravore-empire-selection.ocr.json').read_text(encoding='utf-8'));labels=[v['text'] for v in f['rows']]
checks={
'original_FAIL_and_other25_true':old['status']=='FAIL' and old['checks']['legal_civics'] is False and len(old['checks'])==26 and all(v for k,v in old['checks'].items() if k!='legal_civics'),
'same_original_SHA':old['save_sha256']==a['save_sha256']==h.sha256(run/'terravore-legal-initial-pending.sav'),
'exact_two_string_civic_tokens':tokens==['civic_hive_devouring_swarm','civic_hive_ascetic'],
'native_government_authority_origin':gov['type']=='gov_devouring_swarm' and gov['authority']=='auth_hive_mind' and gov['origin']=='origin_heart_of_devouring',
'official_native_selection_UI_bound':'噬岩者' in labels and '禁欲主义' in labels and '石质' in labels and h.sha256(Path(f['image']))==f['image_sha256']}
proof={'status':'PASS_LEGAL_INITIAL_CIVIC_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,
       'save_sha256':a['save_sha256'],'actual_civic_tokens':tokens,'original_status':old['status'],
       'scope':'Read-only exact token supplement to initial component. Original FAIL remains; no game replay or full-route claim.'}
h.write_json(run/'terravore-legal-initial-civic-supplement-proof.json',proof);print(json.dumps(proof),flush=True)
assert all(checks.values()),'Original supplement failure retained'
