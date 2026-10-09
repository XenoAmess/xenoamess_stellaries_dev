import json,logging,shutil,sys,zipfile
from pathlib import Path
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();shutil.copyfile(Path(__file__),run/Path(__file__).name)
src=run/'organic-purifier-growth-normal-pending.sav';alias=user/'save games/acceptance-fixtures/org-growth-ui.sav'
if not alias.exists():shutil.copyfile(src,alias)
assert h.sha256(src)==h.sha256(alias);b=json.loads((run/'organic-purifier-growth-normal-pending.audit.json').read_text(encoding='utf-8'));eb=(user/'logs/error.log').read_bytes()
r.native_load('org-growth-ui','organic-growth-pending-restore');a=r.native_save('organic-growth-restored-before',b['date'],(0,));cb,ca=b['countries']['0'],a['countries']['0'];ea=(user/'logs/error.log').read_bytes();(run/'organic-growth-restored-before-error-final.log').write_bytes(ea)
def species_amount(data):
 out=defaultdict(int)
 for col in data['countries']['0']['owned_colonies']:
  for i in data['colonies'][str(col)]['pop_groups']:
   g=data['pop_groups'][str(i)];out[str(g['key']['species'])]+=g['size']
 return dict(out)
with zipfile.ZipFile(run/'organic-growth-restored-before.sav') as z:t=z.read('gamestate').decode('utf-8-sig')
events=[q.scalars(v) for k,v,obj in q.fields(t) if k=='player_event' and obj]
checks={'source_alias_original_bytes':h.sha256(src)==h.sha256(alias),'restored_same_date':a['date']==b['date'],'all_stock_same':ca['stockpile']==cb['stockpile'],'EEP_ledger_same':ca['variables']==cb['variables'],'EEP_flags_same':ca['flags']==cb['flags'],'actual_species_population_same':species_amount(a)==species_amount(b),'pending_same_growth_identity':any(e.get('id')==368 and e.get('event')=='eep.13' and e.get('country')==0 for e in events),'AP_same':ca['ascension_perks']==cb['ascension_perks'],'tech_queue_same':ca['completed_technologies']==cb['completed_technologies'] and ca['research_queues']==cb['research_queues'],'no_new_errors':ea==eb}
h.write_json(run/'organic-growth-restored-before-proof.json',{'status':'PASS_SCOPED' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'raw_collection_same':{k:a[k]==b[k] for k in ('pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species')},'scope':'Original pending growth event recovery/native load; does not replace old full raw reload FAIL or failed May ACK branch.'});print(json.dumps(checks),flush=True);assert all(checks.values()),'Original recovery FAIL retained'
