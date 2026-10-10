"""Read-only exact two paid defensive traditions during the paused mother battle."""
import json, logging, shutil, sys, zipfile
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO)
h = r.harness; run, user, metadata = h.load_run()
dest = run / Path(__file__).name
assert not dest.exists()
shutil.copyfile(__file__, dest)
before = 'terravore-war1-defense-month3'
middle = 'terravore-war1-defensive-traditions-paid'
after = 'terravore-war1-defensive-traditions-paid2'
def load(name): return json.loads((run / name).read_text('utf-8'))
def read(stage):
    audit = load(stage + '.audit.json')
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        fields = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return audit, fields, {k:v for k,v,o in fields if o}
def omit(raw, keys): return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b, bf, br = read(before); m, mf, mr = read(middle); a, af, ar = read(after)
bc, mc, ac = [x['countries']['0'] for x in [b,m,a]]
paid = [D(str(x['effective_stockpile']['unity'])) - D(str(y['effective_stockpile']['unity']))
        for x,y in [(bc,mc),(mc,ac)]]
prior = load(before + '-war1-combat-colonization-proof.json')
prior_execution = load(before + '-guard-execution.json')
source = Path('C:/SteamLibrary/steamapps/common/Stellaris/common/traditions/00_unyielding.txt')
checks = {
    'prior20_PASS_actual0_SHA_bound': prior['status'].startswith('PASS_')
        and len(prior['checks']) == 20 and all(v is True for v in prior['checks'].values())
        and prior['after_sha256'] == b['save_sha256'] and prior_execution['returncode'] == 0
        and prior_execution['helper_sha256'] == '085a7db14a6a9ea094d292a1948eba806409b9dd9e0a54bb7ce8e4f3e939f394',
    'native_source_SHA_bound': h.sha256(source) == 'b1a5e8da4514622a0302940953c0e63b66dff3af266e956cd00aa664552367e6',
    'same_actual_paused_date_three_original_SHA': b['date'] == m['date'] == a['date'] == '2268.06.17'
        and all(h.sha256(run/(st+'.sav')) == au['save_sha256'] for st,au in [(before,b),(middle,m),(after,a)]),
    'exact_two_decimal_UI_ceiling_payments': all(0 < p <= price and p.to_integral_value(rounding=ROUND_CEILING) == price
        for p,price in zip(paid,[D(4330),D(4608)])),
    'exact_intermediate_and_final_traditions': mc['traditions'] == bc['traditions'] + ['tr_unyielding_adopt']
        and ac['traditions'] == mc['traditions'] + ['tr_unyielding_defensive_zeal'],
    'other_real_stocks_and_banks_held': all({k:v for k,v in c['effective_stockpile'].items() if k!='unity'}
        == {k:v for k,v in bc['effective_stockpile'].items() if k!='unity'} for c in [mc,ac]),
    'EEP_flags_variables_AP_tech_gov_and_colonies_held': all(bc[k] == ac[k] for k in
        ['variables','flags','ascension_perks','tech_status','government','owned_colonies'])
        and bc['owned_colonies'] == [0,37],
    'all_population_jobs_planets_buildings_districts_species_held': all(b[k] == a[k] for k in
        ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','event_targets','situations']),
    'construction_zones_buildings_and_all_ships_raw_held': all(br[k] == ar[k] for k in
        ['construction','zones','buildings','ships']),
    'no_pending_country0': not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
    'save_click_confirm_executions_actual0': all(load(st+'-execution.json')['returncode']==0 for st in
        [middle,after,'terravore-war1-unyielding-adopt-click','terravore-war1-unyielding-adopt-confirm',
         'terravore-war1-defensive-zeal-click','terravore-war1-defensive-zeal-reopen','terravore-war1-defensive-zeal-confirm']),
    'full_error_bytes_held': (run/(before+'-error-after.log')).read_bytes()
        == (run/(after+'-error-before.log')).read_bytes() == (run/(after+'-error-after.log')).read_bytes(),
}
bfleets = {k:v for k,v,o in q.fields(br['fleet']) if o}
afleets = {k:v for k,v,o in q.fields(ar['fleet']) if o}
changed_fleets = [k for k in bfleets if bfleets[k] != afleets.get(k)]
checks['exact20_fleet_cache_changes_only'] = set(bfleets) == set(afleets) and set(changed_fleets) == {
    '0','1','2','136','137','138','139','140','161','166','167','172','178','183','198',
    '33555013','33555034','788','804','16778043'} and all(
    omit(bfleets[k], {'properties'}) == omit(afleets[k], {'properties'})
    and q.fields(q.block(bfleets[k],'properties')) is not None
    and list(q.fields(q.block(afleets[k],'properties'))) == list(q.fields(q.block(bfleets[k],'properties')))
        + [('dirty_cloaking_strength','yes',False)] for k in changed_fleets)
bs, ass = [q.block(q.block(top['starbase_mgr'],'starbases'),'0') for top in [br,ar]]
checks['only_base0_update_flag2048_added'] = omit(bs,{'update_flag'}) == omit(ass,{'update_flag'}) \
    and 'update_flag' not in q.scalars(bs) and q.scalars(ass).get('update_flag') == 2048 \
    and br['starbase_mgr'].replace(bs,ass,1) == ar['starbase_mgr']
bcr, acr = [q.block(top['country'],'0') for top in [br,ar]]
checks['country_only_exact_tradition_fields_and_economic_flush'] = \
    omit(bcr, {'tradition_categories','traditions','modules','last_picked_tradition'}) == \
    omit(acr, {'tradition_categories','traditions','modules','last_picked_tradition'}) \
    and q.scalars(acr)['last_picked_tradition'] == 'tr_unyielding_defensive_zeal' \
    and list(q.tokens(q.block(acr,'tradition_categories'))) == list(q.tokens(q.block(bcr,'tradition_categories'))) + ['"tradition_unyielding"']
bm, am = [q.block(c,'modules') for c in [bcr,acr]]
be, ae = [q.block(c,'standard_economy_module') for c in [bm,am]]
checks['only_economy_resources_flush_other_modules_raw_held'] = omit(bm,{'standard_economy_module'}) == omit(am,{'standard_economy_module'}) \
    and omit(be,{'resources'}) == omit(ae,{'resources'}) and q.scalars(q.block(ae,'resources')) == ac['effective_stockpile']
checks['all_other_countries_raw_held'] = br['country'].replace(bcr,acr,1) == ar['country']
bmessages = [v for k,v,o in bf if k=='message']; amessages = [v for k,v,o in af if k=='message']
checks['original_combat_message_held_one_adoption_agenda_notice'] = amessages[:-1] == bmessages \
    and len(amessages) == len(bmessages)+1 \
    and q.scalars(amessages[-1]).get('type') == 'COUNCIL_AGENDA_AVAILABLE' \
    and q.scalars(amessages[-1]).get('receiver') == 0 \
    and q.scalars(amessages[-1]).get('date') == '2268.06.17'
top_allow = {'country','fleet','starbase_mgr','message','random_count','last_notification_id'}
checks['all_other_top_fields_raw_held_random2_notice1_only'] = [(k,v,o) for k,v,o in bf if k not in top_allow] \
    == [(k,v,o) for k,v,o in af if k not in top_allow] \
    and int(next(v for k,v,o in af if k=='random_count')) == int(next(v for k,v,o in bf if k=='random_count'))+2 \
    and int(next(v for k,v,o in af if k=='last_notification_id')) == int(next(v for k,v,o in bf if k=='last_notification_id'))+1
out = {'status':'PASS_NATIVE_DEFENSIVE_TRADITIONS_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL',
       'checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],
       'intermediate_sha256':m['save_sha256'],'actual_unity_payments':list(map(str,paid)),
       'actual_unity_remaining':ac['effective_stockpile']['unity'],'source_sha256':h.sha256(source),
       'changed_fleet_cache_ids':changed_fleets,'calendar_ready':False,
       'short_combat_calendar_ready':all(checks.values()),
       'scope':'Exactly two normal paid native defensive traditions; paused base hull remains cached12500. No battle outcome or complete route claim.'}
p = run/(after+'-defensive-traditions-payment-proof.json'); assert not p.exists()
h.write_json(p,out); print(json.dumps(out),flush=True)
assert all(checks.values()), 'Preserve original FAIL; do not repeat purchases'
