"""Exact legal fifth AP after a fully paid native defensive tradition tree."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
before='terravore-war1-fortress-paid';after='terravore-war1-vigilance-selected2'
def load(n):return json.loads((run/n).read_text('utf-8'))
def read(st):
 a=load(st+'.audit.json')
 with zipfile.ZipFile(run/(st+'.sav')) as z:f=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,f,{k:v for k,v,o in f if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
pre=load(before+'-war1-tradition-payment-v4-proof.json');ex=load(before+'-guard-v4-execution.json')
checks={
 'prior_paid_full_tree18_PASS_actual0_original_source_SHA':pre['status'].startswith('PASS_') and len(pre['checks'])==18
  and all(v is True for v in pre['checks'].values()) and ex['returncode']==0
  and ex['helper_sha256']=='4aaa6e6665494b6bd1ec9e5e50fb3a3c97bd6b9d5862cf1ac92facefaadb2593'
  and pre['after_sha256']==b['save_sha256'] and h.sha256(run/Path(ex['command'][1]).name)==ex['helper_sha256'],
 'native_AP_and_unyielding_source_SHA_bound':h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/common/ascension_perks/00_ascension_perks.txt'))=='0992582948a3ca199b30ab646720091e0207e2e58b688171d9cc501f266a720c'
  and h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/common/traditions/00_unyielding.txt'))=='b1a5e8da4514622a0302940953c0e63b66dff3af266e956cd00aa664552367e6',
 'same_actual_paused_date_original_SHA_pair':b['date']==a['date']=='2268.07.07'
  and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'exact_legal_fifth_AP_after_full_tree_original_four_held':len(bc['ascension_perks'])==4
  and ac['ascension_perks']==bc['ascension_perks']+['ap_eternal_vigilance']
  and 'tr_unyielding_finish' in bc['traditions'] and bc['traditions']==ac['traditions'],
 'country0_only_exact_AP_field_changed':omit(bcr,{'ascension_perks'})==omit(acr,{'ascension_perks'}),
 'all_other_countries_raw_held':br['country'].replace(bcr,acr,1)==ar['country'],
 'every_other_top_field_raw_held_except_random1':[(k,v,o) for k,v,o in bf if k not in {'country','random_count'}]
  ==[(k,v,o) for k,v,o in af if k not in {'country','random_count'}]
  and int(next(v for k,v,o in af if k=='random_count'))==int(next(v for k,v,o in bf if k=='random_count'))+1,
 'all_true_inventory_banks_EEP_population_jobs_colonies_held':all(bc[k]==ac[k] for k in bc if k!='ascension_perks')
  and all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','event_targets','situations']),
 'actual_native_slot_reopen_choice_confirm2_save_actual0':all(load(st+'-execution.json')['returncode']==0 for st in
  ['terravore-war1-fifth-ap-slot-reopen','terravore-war1-vigilance-reopen','terravore-war1-vigilance-confirm2',after])
  and load('terravore-war1-vigilance-confirm2-execution.json')['command'][-2:]==['588','433'],
 'original_failed_save_actual1_no_SAV_or_audit_retained':load('terravore-war1-vigilance-selected-execution.json')['returncode']==1
  and not (run/'terravore-war1-vigilance-selected.sav').exists() and not (run/'terravore-war1-vigilance-selected.audit.json').exists(),
 'no_pending_country0':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'full_unfiltered_error2670_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()
  ==(run/(after+'-error-after.log')).read_bytes() and (run/(after+'-error-after.log')).stat().st_size==2670,
}
out={'status':'PASS_TERRAVORE_NATIVE_PAID_TREE_VIGILANCE_AP_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,
 'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,
 'short_combat_calendar_ready':all(checks.values()),'scope':'Only legal fifth AP after paid defensive tree; ship hull still cached15800 while paused. No battle outcome or full route claim.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids']:out[key]=pre[key]
p=run/(after+'-vigilance-ap-proof.json');assert not p.exists();h.write_json(p,out)
print(json.dumps(out),flush=True);assert all(checks.values())
