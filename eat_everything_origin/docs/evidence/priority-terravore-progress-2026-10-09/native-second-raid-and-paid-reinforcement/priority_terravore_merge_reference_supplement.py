"""Exact same-tick inactive fleet references; original merge strict FAIL retained."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
old=json.loads((run/(after+'-merge-recall-proof.json')).read_text('utf-8'));ts=[]
for st in [before,after]:
 with zipfile.ZipFile(run/(st+'.sav')) as z:ts.append(z.read('gamestate').decode('utf-8-sig'))
own=lambda t:q.block(q.block(q.block(q.block(t,'country'),'0'),'fleets_manager'),'owned_fleets')
checks={
 'original30_unique_FAIL_other29_PASS_retained':old['status']=='FAIL' and len(old['checks'])==30 and [k for k,v in old['checks'].items() if not v]==['only_original593_598_owned_references_removed'] and sum(v is True for v in old['checks'].values())==29 and json.loads((run/'terravore-defense-merged-return-guard-execution.json').read_text('utf-8'))['returncode']==1,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==old['before_sha256'] and h.sha256(run/(after+'.sav'))==old['after_sha256'],
 'same_tick_entire_owned_reference_list_raw_held':own(ts[0])==own(ts[1]),
 'two_references_only_inactive_none_zero_ships_power':all(q.scalars(f:=q.block(q.block(ts[1],'fleet'),str(i)))['ship_class']=='none' and not q.ids(q.block(f,'ships')) and q.scalars(f)['military_power']==0 for i in [593,598]),
 'all12_actual_ships_unique_and_in_main_fleet':len(old['actual12_ships'])==len(set(old['actual12_ships']))==12 and all(q.scalars(q.block(q.block(ts[1],'ships'),str(i)))['fleet']==16777797 for i in old['actual12_ships']),
}
p={'status':'PASS_NATIVE_MERGE_INACTIVE_REFERENCE_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':old['before_sha256'],'after_sha256':old['after_sha256'],'scope':'Original29 PASS plus exact inactive reference persistence, original30 FAIL retained. Actual12 ships merged and normal recall order bound; no next-month repair/victory claim.'}
out=run/(after+'-merge-reference-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original reference supplement FAIL retained'
