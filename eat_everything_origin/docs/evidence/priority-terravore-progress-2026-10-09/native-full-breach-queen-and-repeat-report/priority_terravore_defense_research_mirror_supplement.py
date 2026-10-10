"""Exact non-bank research mirror deletion during a normal paid ship batch."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:rt={k:v for k,v,o in q.fields(z.read('gamestate').decode('utf-8-sig')) if o}
 mods=q.block(q.block(rt['country'],'0'),'modules');econ=q.block(mods,'standard_economy_module')
 return a,mods,econ,q.block(econ,'resources')
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bm,be,br=read(before);a,am,ae,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(after+'-defense-payment-proof.json')).read_text('utf-8'));mirror={'physics_research':690.63101,'society_research':588.33101,'engineering_research':741.78101}
checks={
 'original41_exact_one_mirror_raw_FAIL_and40_valid':pre['status']=='FAIL' and len(pre['checks'])==41 and [k for k,v in pre['checks'].items() if v is not True]==['only_economy_actual_alloy_field_changed'],
 'original_SHA_pair_bound':pre['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav')) and pre['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'only_three_exact_economy_research_mirrors_removed':{k:q.scalars(br)[k] for k in mirror}==mirror and not any(k in q.scalars(ar) for k in mirror) and omit(br,['alloys',*mirror])==omit(ar,['alloys',*mirror]),
 'all_other_modules_and_economy_raw_held':omit(bm,['standard_economy_module'])==omit(am,['standard_economy_module']) and omit(be,['resources'])==omit(ae,['resources']),
 'all_actual_banks_zero_and_full_tech_status_held':q.research_stocks(bc['tech_status'])==q.research_stocks(ac['tech_status'])==dict.fromkeys(q.RESEARCH_RESOURCES,0) and bc['tech_status']==ac['tech_status'] and bc['research_queues']==ac['research_queues'] and bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'actual_native_alloy1792_paid_not_research':D(str(q.scalars(br)['alloys']))-D(str(q.scalars(ar)['alloys']))==D(1792) and bc['effective_stockpile']['alloys']==8736.73315 and ac['effective_stockpile']['alloys']==6944.73315,
 'complete_unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_SCOPED_TERRAVORE_DEFENSE_PAYMENT_MIRROR_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'original_valid_checks':{k:v for k,v in pre['checks'].items() if v is True},'removed_economy_mirrors':mirror,'actual_true_bank':q.research_stocks(ac['tech_status']),'scope':'Original41-check FAIL retained; exact three stale economy mirrors removed, true research state unchanged,20 paid native orders validated by original40 checks. No ship completion or defense success claim.'}
out=run/(after+'-defense-mirror-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original mirror supplement FAIL retained; no calendar'
