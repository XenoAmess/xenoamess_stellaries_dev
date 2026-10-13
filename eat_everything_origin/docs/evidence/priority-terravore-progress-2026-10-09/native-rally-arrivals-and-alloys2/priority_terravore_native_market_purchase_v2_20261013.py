"""Read-only, same-date native market purchase guard; never buys or advances time."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
before,after,quote,display,action,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def checked(st):
 x=load(st+'-execution.json');return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
b=read_state(run,before);a=read_state(run,after);ba=b['audit'];aa=a['audit'];bc=ba['countries']['0'];ac=aa['countries']['0'];p=load(prior)
bm=q.block(b['country'],'modules');am=q.block(a['country'],'modules');be=q.block(bm,'standard_economy_module');ae=q.block(am,'standard_economy_module');br=q.scalars(q.block(be,'resources'));ar=q.scalars(q.block(ae,'resources'));cost=D(str(br['trade']))-D(str(ar['trade']));quotej=load(quote+'.ocr.json');rows=[x['text'] for x in quotej['rows']];inputj=load(action+'.action.json')
checks={
 'prior_component_PASS_actual0_originalSAV':p['status'].startswith('PASS') and p['checks'] and all(v is True for v in p['checks'].values()) and checked(execution) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')),
 'same_paused_October2_normal_save_actual0_original_pair':ba['date']==aa['date']=='2285.10.02' and checked(after+'-native-save') and aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'one_normal_click_exact1000_quote_original_F12_actual0':checked(action) and inputj['action']=='left-click' and inputj['client_point']==[190,340] and checked(quote) and quotej['image_sha256']==h.sha256(run/(quote+'.jpg')) and any('1000.00' in x for x in rows) and any(str(display) in x for x in rows) and 0<D(display)<=2000,
 'native_cash_debit_quote_integer_precision_mineral_gain1000':abs(cost-D(display))<1 and 0<cost<=2000 and D(str(ar['minerals']))-D(str(br['minerals']))==1000 and all(ar.get(k)==v for k,v in br.items() if k not in ['trade','minerals']) and set(ar)==set(br),
 'all_other_effective_cash_research_banks_and_technology_held':all(ac['effective_stockpile'].get(k)==v for k,v in bc['effective_stockpile'].items() if k not in ['trade','minerals']) and ac['research_stockpile']==bc['research_stockpile'] and ac['tech_status']==bc['tech_status'],
 'country_raw_only_economy_resource_block_changes':omit(a['country'],{'modules'})==omit(b['country'],{'modules'}) and omit(am,{'standard_economy_module'})==omit(bm,{'standard_economy_module'}) and omit(ae,{'resources'})==omit(be,{'resources'}),
 'all77_owned_ships_full_raw_held':len(a['ships'])==len(b['ships'])==77 and a['ships']==b['ships'],
 'all35_owned_fleets_full_raw_held':len(a['fleets'])==len(b['fleets'])==35 and a['fleets']==b['fleets'],
 'all_construction_queues_and_items_raw_held':a['queues']==b['queues'] and a['items']==b['items'] and a['roots']['construction']==b['roots']['construction'],
 'population_planets_districts_zones_buildings_army_war_truce_held':all(a['roots'][k]==b['roots'][k] for k in ['planets','colony','pop_groups','districts','zones','buildings','army','war','truce']),
 'EEP_government_AP_traditions_crisis_menace_held':all(ac[k]==bc[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis']) and ac['effective_stockpile']['menace']==bc['effective_stockpile']['menace']==2930,
 'messages_held_no_pending':a['messages']==b['messages'] and not a['pending'] and not b['pending'],
 'no_native_automatic_monthly_trade_added':q.block(a['country'],'market_trades')==q.block(b['country'],'market_trades'),
 'CN41_unfiltered_error_original_bytes_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
checks['energy_and_other_resources_held_payment_exact_native_integer']=ar['energy']==br['energy'] and cost==D(display)
if after=='terravore-native-market-purchase01-22851002':
 original=load(after+'-market-purchase-proof.json');ox=load(after+'-market-purchase-guard-execution.json')
 checks['original14_two_currencyFAIL_actual1_sameSAV_retained']=len(original['checks'])==14 and [k for k,v in original['checks'].items() if v is not True]==['native_cash_debit_quote_integer_precision_mineral_gain1000','all_other_effective_cash_research_banks_and_technology_held'] and ox['returncode']==1 and ox['helper_sha256']==h.sha256(Path(ox['command'][1]))=='21235d3a9c9e6e284058c00d1c37edf87eadbe0e939355da5aec78b3d648b47c' and original['before_sha256']==ba['save_sha256'] and original['after_sha256']==aa['save_sha256']
passed=all(v is True for v in checks.values());out=run/(after+'-market-purchase-v2-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_MARKET_PURCHASE_V2' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'actual_trade_debit':str(cost),'mineral_gain':str(D(str(ar['minerals']))-D(str(br['minerals']))),'quote_integer':display,'quote_image_sha256':h.sha256(run/(quote+'.jpg')),'after_trade':ar['trade'],'after_energy':ar['energy'],'after_minerals':ar['minerals'],'boundaries':['native_market_next_quote_or_rally_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Single same-date paid market purchase only; not full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'trade_debit':str(cost),'minerals':ar['minerals']}),flush=True);assert passed
