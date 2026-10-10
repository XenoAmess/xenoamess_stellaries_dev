"""Exact token-value and omitted-zero corrections; retain original payment FAIL."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
before='terravore-war1-defense-month3';after='terravore-war1-defensive-traditions-paid2'
def load(n):return json.loads((run/n).read_text('utf-8'))
def country(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return q.block(q.block(t,'country'),'0')
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,a=[load(st+'.audit.json') for st in [before,after]];bc,ac=country(before),country(after)
p=load(after+'-defensive-traditions-payment-proof.json');e=load(after+'-guard-execution.json')
bm,am=[q.block(c,'modules') for c in [bc,ac]];be,ae=[q.block(c,'standard_economy_module') for c in [bm,am]]
resources=q.scalars(q.block(ae,'resources'));actual=a['countries']['0']['effective_stockpile']
checks={
 'original19_exact_two_private_assertion_FAILs_actual1':p['status']=='FAIL' and len(p['checks'])==19
  and [k for k,v in p['checks'].items() if not v]==['country_only_exact_tradition_fields_and_economic_flush','only_economy_resources_flush_other_modules_raw_held']
  and e['returncode']==1 and e['helper_sha256']=='fd6f97230d955118462aeaf800f2f92416941a02abe0736a88c16c6e0053845a'
  and h.sha256(run/Path(e['command'][1]).name)==e['helper_sha256'],
 'original_SHA_pair_bound':p['before_sha256']==b['save_sha256']==h.sha256(run/(before+'.sav'))
  and p['after_sha256']==a['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact_ordered_category_token_values_and_other_country_raw':
  [t for t,_,_ in q.tokens(q.block(ac,'tradition_categories'))]==[t for t,_,_ in q.tokens(q.block(bc,'tradition_categories'))]+['"tradition_unyielding"']
  and q.scalars(ac)['last_picked_tradition']=='tr_unyielding_defensive_zeal'
  and omit(bc,{'tradition_categories','traditions','modules','last_picked_tradition'})==omit(ac,{'tradition_categories','traditions','modules','last_picked_tradition'}),
 'exact_omitted_zero_resources_decimal_and_all_other_modules_raw':set(resources)<=set(actual)
  and all(D(str(resources.get(k,0)))==D(str(v)) for k,v in actual.items())
  and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}),
 'original_intermediate_SHA_and_save_actual0_bound':p['intermediate_sha256']==h.sha256(run/'terravore-war1-defensive-traditions-paid.sav')
  and load(after+'-execution.json')['returncode']==0,
}
out={'status':'PASS_NATIVE_DEFENSIVE_TRADITIONS_EXACT_PAYMENT_SUPPLEMENT' if all(checks.values()) else 'FAIL','checks':checks,
 'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,
 'short_combat_calendar_ready':all(checks.values()),'scope':'Two exact private assertion corrections; original17 true retained. No native free resources, battle victory or full route claim.'}
path=run/(after+'-defensive-payment-supplement.json');assert not path.exists();h.write_json(path,out)
print(json.dumps(out),flush=True);assert all(checks.values())
