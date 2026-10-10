"""One normal native defensive tradition payment; preserve cumulative battle losses."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D,ROUND_CEILING
from pathlib import Path
before,after,price,addition,priorfile,priorexec,clickstem=sys.argv[1:]
price=D(price);sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def load(n):return json.loads((run/n).read_text('utf-8'))
def read(st):
 a=load(st+'.audit.json')
 with zipfile.ZipFile(run/(st+'.sav')) as z:f=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,f,{k:v for k,v,o in f if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=load(priorfile);ex=load(priorexec+'-execution.json')
cost=D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']))
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bm,am=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(c,'standard_economy_module') for c in [bm,am]]
resources=q.scalars(q.block(ae,'resources'));actual=ac['effective_stockpile']
fl=[{k:v for k,v,o in q.fields(t['fleet']) if o} for t in [br,ar]]
changed=[k for k,v in fl[0].items() if v!=fl[1].get(k)]
bs,ass=[q.block(q.block(t['starbase_mgr'],'starbases'),'0') for t in [br,ar]]
checks={
 'prior_PASS_all_true_actual0_original_helper_SHA':pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values())
  and ex['returncode']==0 and pre['after_sha256']==b['save_sha256'] and h.sha256(run/Path(ex['command'][1]).name)==ex['helper_sha256'],
 'same_actual_date_original_SHA_pair':b['date']==a['date']=='2268.06.23'
  and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'native_unyielding_source_SHA':h.sha256(Path('C:/SteamLibrary/steamapps/common/Stellaris/common/traditions/00_unyielding.txt'))=='b1a5e8da4514622a0302940953c0e63b66dff3af266e956cd00aa664552367e6',
 'exact_decimal_payment_UI_ceiling':0<cost<=price and cost.to_integral_value(rounding=ROUND_CEILING)==price,
 'exact_one_tradition_AP_categories_held':ac['traditions']==bc['traditions']+[addition]
  and ac['ascension_perks']==bc['ascension_perks'] and q.block(bcr,'tradition_categories')==q.block(acr,'tradition_categories')
  and q.scalars(acr)['last_picked_tradition']==addition,
 'all_other_real_stocks_and_banks_held':{k:v for k,v in actual.items() if k!='unity'}=={k:v for k,v in bc['effective_stockpile'].items() if k!='unity'},
 'EEP_flags_government_technology_owned_colonies_held':all(bc[k]==ac[k] for k in ['flags','variables','government','tech_status','owned_colonies']),
 'population_jobs_all_planets_buildings_districts_species_tasks_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','event_targets','situations'])
  and all(br[k]==ar[k] for k in ['ships','construction','zones','buildings','war','army']),
 'only_country_tradition_and_economy_flush_fields':omit(bcr,{'traditions','modules','last_picked_tradition'})==omit(acr,{'traditions','modules','last_picked_tradition'})
  and br['country'].replace(bcr,acr,1)==ar['country'],
 'all_other_modules_raw_held_and_true_resources_decimal':omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'})
  and omit(be,{'resources'})==omit(ae,{'resources'}) and set(resources)<=set(actual)
  and all(D(str(resources.get(k,0)))==D(str(v)) for k,v in actual.items()),
 'only_fleet_dirty_cloaking_and_exact_actual_hull_sum_cache_allowed':set(fl[0])==set(fl[1]) and all(omit(fl[0][k],{'properties','hit_points'})==omit(fl[1][k],{'properties','hit_points'})
  and (q.scalars(fl[0][k]).get('hit_points')==q.scalars(fl[1][k]).get('hit_points') or abs(D(str(q.scalars(fl[1][k])['hit_points']))-sum(D(str(q.scalars(q.block(ar['ships'],str(i)))['hitpoints'])) for i in q.ids(q.block(fl[1][k],'ships'))))<=D('0.00005'))
  and omit(q.block(fl[0][k],'properties'),{'dirty_cloaking_strength'})==omit(q.block(fl[1][k],'properties'),{'dirty_cloaking_strength'})
  and q.scalars(q.block(fl[1][k],'properties')).get('dirty_cloaking_strength')=='yes' for k in changed),
 'only_base0_update2048_allowed':omit(bs,{'update_flag'})==omit(ass,{'update_flag'})
  and q.scalars(ass).get('update_flag')==2048 and br['starbase_mgr'].replace(bs,ass,1)==ar['starbase_mgr'],
 'all_other_top_fields_raw_held':[(k,v,o) for k,v,o in bf if k not in {'country','fleet','starbase_mgr','random_count'}]
  ==[(k,v,o) for k,v,o in af if k not in {'country','fleet','starbase_mgr','random_count'}],
 'native_one_selection_random_increment1':int(next(v for k,v,o in af if k=='random_count'))==int(next(v for k,v,o in bf if k=='random_count'))+1,
 'click_confirm_save_actual0':all(load(st+'-execution.json')['returncode']==0 for st in [clickstem+'-click',clickstem+'-confirm',after]),
 'no_pending_country0':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'full_unfiltered_error_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
 'prior_exact_cumulative_battle_ledger_retained':pre.get('cumulative_original_lost')==[33556207,33556208,50332878]
  and pre.get('cumulative_paid_lost')==[] and pre.get('all_observed_paid_ship_ids')==[1895,1896,50333423,67110094],
}
if after=='terravore-war1-resistance-paid':
 old=load(after+'-guard-execution.json')
 checks['first_purchase_original_armies_KeyError_actual1_bound']=old['returncode']==1 and old['helper_sha256']=='7139d532929c019fd34d4d25123821d02fcba3197df03ee342aeccf1755275b2' and "KeyError: 'armies'" in (run/(after+'-guard-stderr.txt')).read_text('utf-8') and not (run/(after+'-war1-tradition-payment-proof.json')).exists()
if after=='terravore-war1-resistance-paid':
 v2=load(after+'-war1-tradition-payment-v2-proof.json');v2e=load(after+'-guard-v2-execution.json')
 checks['first_payment_original19_exact_one_cached_hull_FAIL_bound']=v2['status']=='FAIL' and len(v2['checks'])==19 and [k for k,v in v2['checks'].items() if not v]==['only_fleet_dirty_cloaking_cache_allowed'] and v2e['returncode']==1 and v2e['helper_sha256']=='fdf0fce75b84bd268e70b2ae13e84b318b60ce6bdee03cf4e4b93afd92d2a8ed' and v2['before_sha256']==b['save_sha256'] and v2['after_sha256']==a['save_sha256']
out={'status':'PASS_NATIVE_WAR1_SINGLE_TRADITION_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,
 'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_unity_paid':str(cost),'UI_price':str(price),
 'addition':addition,'changed_fleet_cache_ids':changed,'calendar_ready':False,'short_combat_calendar_ready':all(checks.values()),
 'scope':'One normal native defensive tradition purchase while paused; no battle outcome or full route claim.'}
for key in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids']:out[key]=pre.get(key)
p=run/(after+'-war1-tradition-payment-v3-proof.json');assert not p.exists();h.write_json(p,out)
print(json.dumps(out),flush=True);assert all(checks.values()),'Preserve original FAIL and do not repeat payment'
