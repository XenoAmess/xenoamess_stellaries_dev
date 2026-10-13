"""Documented paid second society zone and normal support travel, before completion."""
import json, logging, re, sys
from decimal import Decimal as D
from itertools import groupby
from pathlib import Path

mode, before, other, prior, execution = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
from priority_terravore_native_state import read_state, omit
logging.disable(logging.INFO); h = r.harness; run, user, meta = h.load_run()
load = lambda name: json.loads((run/name).read_text('utf-8-sig'))
suffix = '-support-zone-v2'; eps = D('.00005')

def day(value):
    y, m, d = map(int, value.split('.')); return y*360+(m-1)*30+d-1

def checked(stage):
    x = load(stage+'-execution.json')
    return x['returncode'] == 0 and x['helper_sha256'] == h.sha256(Path(x['command'][1]))

def rq(c, key):
    raw = c['research_queues'].get(key, ''); ts = list(q.tokens(raw))
    if not ts: return {}
    out = q.scalars(raw[ts[0][2]:ts[-1][1]]); out.setdefault('progress', 0)
    return out

def flags(s):
    return {k: q.scalars(v) if obj else q.unquote(v) for k, v, obj in q.fields(q.block(s['country'], 'flags'))}

def income(c):
    return {key: sum((D(str(v.get(key, 0))) for v in c['budget_categories']['current_month']['income'].values()), D(0)) for key in q.RESEARCH_RESOURCES}

b = read_state(run, before); ba = b['audit']; bc = ba['countries']['0']; p = load(prior)
end = other if mode == 'review' else load(other+'.audit.json')['date']
days = day(end)-day(ba['date'])
ticks = sum((day(ba['date'])+i)%30 == 1 for i in range(1, days+1))
months = sum((day(ba['date'])+i)%30 == 0 for i in range(1, days+1))
bi = income(bc); bp = rq(bc, 'society_queue')
ids = q.ids(q.block(b['queues']['0'], 'items')); headid = str(ids[0])
head = D(str(q.scalars(b['items'][headid])['progress']))
complete = head+D(days)*D('1.4') >= 360
basic = p['status'].startswith('PASS') and bool(p['checks']) and all(v is True for v in p['checks'].values()) and checked(execution) and p['after_sha256'] == ba['save_sha256'] == h.sha256(run/(before+'.sav'))
package = meta['language'] == 'l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1] == 'ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
if mode == 'review':
    checks = {
        'prior_PASS_actual0_source_original_SAV': basic,
        'documented_bounded_window_at_or_before_Jan1': 1 <= days <= 30 and day('2286.05.01') <= day(ba['date']) < day(end) <= day('2287.01.01') and months <= 1 and ticks <= 1,
        'only_paid800_zone_and_frozen_four_hives': ids == [201326629,1191182345,117440553,1476395019,117440546] and all(q.scalars(q.block(b['items'][str(i)],'resources')) == {'minerals':800 if i==201326629 else 400} for i in ids) and not q.ids(q.block(b['queues'].get('3',''),'items')) and not complete and q.scalars(b['items']['1191182345'])['progress']==2.8,
        'no_pending_combat_or_project_completion_empty_engineering': not b['pending'] and not rq(bc,'engineering_queue') and q.scalars(bc['tech_status']).get('auto_researching_engineering','no') == 'no' and bp['special_project'] == 9 and D(str(bp['progress']))+D(ticks)*bi['society_research']*D('2.35') < 12000 and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in b['fleets'].values()),
        'CN41_unfiltered_live_error_same': package and (user/'logs/error.log').read_bytes() == (run/(before+'-error-after.log')).read_bytes(),
    }
    passed = all(v is True for v in checks.values()); out = run/(before+suffix+'-review.json'); assert not out.exists()
    h.write_json(out, {'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':ba['save_sha256'],'start_date':ba['date'],'end_date':end,'days':days,'maximum_days':days,'allowed_boundaries':p['boundaries'],'execution_stage':before+suffix+'-review'})
    print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
    assert passed; sys.exit(0)

assert mode == 'guard'; after = other; a = read_state(run,after); aa = a['audit']; ac = aa['countries']['0']; ap = rq(ac,'society_queue')
ob = load(after+'-construction-boundary-observation-v4.json'); cal = load(after+'-calendar-receipt.json'); review = load(before+('-support-zone-v1-review.json' if after=='terravore-second-society-month-22860901' else suffix+'-review.json'))
resources = ['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']
net = {k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
expected = {k:D(str(bc['effective_stockpile'].get(k,0)))+D(months)*v for k,v in net.items()}
expected['influence'] = min(D(1000),expected['influence']); expected['trade'] = min(D(50000),expected['trade'])
residual = {k:D(str(ac['effective_stockpile'].get(k,0)))-v for k,v in expected.items()}
draw = min(bi['society_research'],D(str(bc['research_stockpile']['society_research'])))
ef = {k:dict(v,flag_days=v['flag_days']-days) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>days}
growth_raw = q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details'); fs = list(q.fields(growth_raw))
growth = {q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
zones = {str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z != 4294967295}
builds = {str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i != 4294967295}
army = q.ids(q.block(b['country'],'owned_armies')); news = ob['new_country0_messages_raw']
routes = {}; route_ok = True; full = [188,139,171,70,30,71,164]
for fid in ['83886903','50332250','917']:
    am = q.block(a['fleets'][fid],'movement_manager'); bm = q.block(b['fleets'][fid],'movement_manager'); path = q.block(am,'path')
    nodes = [q.scalars(q.block(v,'coordinate'))['origin'] for k,v,obj in q.fields(path) if obj and k == 'node']; remaining = [i for i,_ in groupby(nodes)]
    current = q.scalars(q.block(am,'coordinate'))['origin']; previous = q.scalars(q.block(bm,'coordinate'))['origin']
    order = q.block(q.block(a['fleets'][fid],'current_order'),'orbit_planet_order'); target = q.scalars(q.block(am,'target_coordinate'))
    routes[fid] = {'current':current,'remaining':remaining,'eta':q.scalars(path).get('date'),'state':q.scalars(am).get('state'),'target':target}
    route_ok = route_ok and q.scalars(a['fleets'][fid])['order_id'] == q.scalars(b['fleets'][fid])['order_id']
    if fid == '83886903':
        route_ok = route_ok and current == previous == 164 and not q.block(a['fleets'][fid],'current_order') and not remaining and q.scalars(am)['state'] == 'move_idle' and q.block(am,'orbit') == q.block(bm,'orbit') and target == {'x':0,'y':0,'origin':4294967295}
    else:
        route_ok = route_ok and current in full and previous in full and full.index(current) >= full.index(previous) and (remaining == full[full.index(current):] or (q.scalars(am).get('state')=='move_wind_up' and current==30 and remaining==[30,71] and nodes==[30,71,71] and q.scalars(am).get('ftl_total_windup')==112 and 0<q.scalars(am).get('ftl_windup',0)<=112 and q.block(a['fleets'][fid],'current_order')==q.block(b['fleets'][fid],'current_order') and all(abs(q.scalars(q.block(am,'coordinate'))[key]-value)<1 for key,value in [('x',156.83193),('y',-14.49142)]) and q.scalars(q.block(am,'last_ftl_jump')).get('to')==30 and q.scalars(q.block(q.block(am,'last_ftl_jump'),'from')).get('origin')==70 and all(q.scalars(v).get('ftl')=='jump_hyperlane' for k,v,obj in q.fields(path) if obj and k=='node') and all(dst in list(map(int,re.findall(r'\bto\s*=\s*(\d+)',q.block(q.block(a['roots']['galactic_object'],str(src)),'hyperlane')))) for src,dst in [(30,71),(71,164)]))) and q.scalars(order).get('can_reach') == 'yes' and q.scalars(q.block(order,'orbitable')) == {'planet':1732} and target['origin'] == 164 and not q.block(am,'orbit').strip()
mainids = set(q.ids(q.block(b['fleets']['83886903'],'ships'))); life = len(mainids) == 16; health = {}
for i,v in b['ships'].items():
    av = a['ships'].get(i,''); bs, ass = q.scalars(v),q.scalars(av)
    life = life and q.block(v,'ship_design_implementation') == q.block(av,'ship_design_implementation') and q.block(v,'name') == q.block(av,'name') and all(bs.get(k) == ass.get(k) for k in ['construction_date','killed','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
    if int(i) not in mainids:
        life = life and all(bs.get(k) == ass.get(k) for k in ['hitpoints','armor_hitpoints','shield_hitpoints'])
    else:
        record = {}
        for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
            wanted = min(D(str(bs[cap])),D(str(bs.get(key,0)))+D(str(bs[cap]))*D('.0025')*D(days)); actual = D(str(ass.get(key,0)))
            record[key] = {'before':bs.get(key,0),'after':str(actual),'expected':str(wanted),'residual':str(actual-wanted)}
            life = life and abs(actual-wanted) < D('.0001')
        life = life and ass.get('shield_hitpoints',0) == 0 and ass.get('hitpoints',0) > 0; health[i] = record
expected_districts = {str(i):dict(ba['districts'][str(i)]) for i in ba['colonies']['0']['districts']}
if complete: expected_districts['1']['level'] += 1
newids = ids[1:] if complete else ids
hive_ok = q.ids(q.block(a['queues']['0'],'items')) == newids
if complete:
    hive_ok = hive_ok and headid not in a['items'] and 0 <= q.scalars(a['items'][str(newids[0])])['progress'] <= 1.4 and omit(b['items'][str(newids[0])],{'progress'}) == omit(a['items'][str(newids[0])],{'progress'}) and all(a['items'][str(i)] == b['items'][str(i)] for i in newids[1:])
else:
    hive_ok = hive_ok and abs(D(str(q.scalars(a['items'][headid])['progress']))-head-D(days)*D('1.4')) < eps and omit(b['items'][headid],{'progress'}) == omit(a['items'][headid],{'progress'}) and all(a['items'][str(i)] == b['items'][str(i)] for i in ids[1:])
jobs_ok = ba['pop_jobs']['23'] == aa['pop_jobs']['23']
for jid in ['24','25']:
    old,now = ba['pop_jobs'][jid],aa['pop_jobs'][jid]
    if complete:
        maximum = old['max_workforce']+120
        jobs_ok = jobs_ok and now['max_workforce'] == now['workforce_limit'] == now['automated_workforce_limit'] == maximum and old['workforce'] <= now['workforce'] <= maximum and D(str(now['bonus_workforce'])) == D(str(now['workforce']))*D('.35') and all(old[k] == now[k] for k in ['type','automated_workforce','planet','pop_group'])
    else: jobs_ok = jobs_ok and old == now
budget_base = load('terravore-support164-orders-22860402.audit.json'); budget_country = budget_base['countries']['0']
delays = [q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k == 'delayed_event']
checks = {
    'prior_review_calendar_observer_actual0_originalSAV': basic and len(ob['checks']) in [6,7] and all(v is True for pp in [ob,review] for v in pp['checks'].values()) and all(checked(s) for s in [after+'-boundary-observation-v4',after+'-calendar',review['execution_stage']]) and ob['before_sha256'] == ba['save_sha256'] and ob['after_sha256'] == aa['save_sha256'] == h.sha256(run/(after+'.sav')),
    'single_bounded_documented_native_interval': cal['days'] == days and cal['start_date'] == ba['date'] and cal['date'] == aa['date'] == end and 1 <= days <= 30 and day(end) <= day('2287.01.01'),
    'cash8_exact_native_budget_no_payments_or_rewards': all(abs(v) < eps for v in residual.values()) and all(ac['effective_stockpile'].get(k,0) >= 0 for k in resources),
    'project3_tick_true_society_bank_exact': bp['special_project'] == ap['special_project'] == 9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-D(ticks)*(bi['society_research']*D('1.35')+draw)) < eps and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+D(ticks)*draw) < eps and ap['progress'] < 12000,
    'idle_engineering_and_physics_true_banks_exact_no_auto': not rq(ac,'engineering_queue') and q.scalars(ac['tech_status']).get('auto_researching_engineering','no') == 'no' and all(abs(D(str(ac['research_stockpile'][key]))-D(str(bc['research_stockpile'][key]))-D(ticks)*bi[key]*D('1.35')) < eps for key in ['physics_research','engineering_research']),
    'all_other_technology_and_project_shapes_raw_held': dict(bp,progress=ap['progress']) == ap and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue'}) == omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue'}) and q.block(b['country'],'events') == q.block(a['country'],'events'),
    'all75_original_ships_identity_exact_native_regeneration': len(b['ships']) == len(a['ships']) == 75 and set(b['ships']) == set(a['ships']) and life,
    'all35_original_fleets_same_members': len(b['fleets']) == len(a['fleets']) == 35 and set(b['fleets']) == set(a['fleets']) and all(q.ids(q.block(v,'ships')) == q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()),
    'main164_orbit_and_two_supports_native_legal_suffix': route_ok,
    'no_new_shiporders_naval251': not q.ids(q.block(a['queues'].get('3',''),'items')) and q.scalars(a['country'])['used_naval_capacity'] == q.scalars(a['country'])['fleet_size'] == 251,
    'EEP_government_AP_traditions_crisis_menace_held': all(bc[k] == ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')} == {k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression') == q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace'] == 3065,
    'mother_only_species73_natural_growth_OTHER0': bc['owned_colonies'] == ac['owned_colonies'] == [0] and aa['colonies']['0']['actual_pop_sum'] == ba['colonies']['0']['actual_pop_sum']+months*growth.get('GROWTH_CAT_GROWTH',0) and set(growth) <= {'GROWTH_CAT_GROWTH','GROWTH_CAT_OTHER','GROWTH_CAT_PROMOTION'} and 0 <= growth.get('GROWTH_CAT_GROWTH',0) <= 10 and growth.get('GROWTH_CAT_OTHER',0) == growth.get('GROWTH_CAT_PROMOTION',0) == 0 and ob['after_state']['species_population_by_colony'] == {'0:73':aa['colonies']['0']['actual_pop_sum']},
    'mother39_only_paid_hive_level_added_original_zones_labs': ba['planets']['7'] == aa['planets']['7'] and all(v == aa['districts'][i] for i,v in expected_districts.items()) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts']) == sum(ba['districts'][str(i)]['level'] for i in ba['colonies']['0']['districts'])+int(complete) and all(q.block(b['roots']['zones'],z) == q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i) == q.block(a['roots']['buildings'],i) for i in builds),
    'research_jobs_only_native120_per_specialization': jobs_ok,
    'only_paid800_zone_daily_work_four_original_hives_held': hive_ok,
    'all15_original_armies_raw_held': len(army) == 15 and army == q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i)) == q.block(a['roots']['army'],str(i)) for i in army),
    'native_flags_only_normal_timers_no_reward_refresh': flags(a) == ef,
    'native_player_contacts63_64_65_held': all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i) == q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
    'only_reviewed_lowtrade_pirate6_delay': len(delays) <= 1 and all(v['event'] == 'pirate.6' and 1 <= v['days'] <= 30 for v in delays) and sum(D(str(v.get('trade',0))) for v in ac['budget_categories']['current_month']['income'].values()) < 300 and 'birth_of_piracy' not in ac['flags'],
    'no_pending_unknown_news_wars_truces_or_combat': not a['pending'] and all(q.scalars(v).get('type') == 'SYSTEM_SURVEYED' and q.scalars(v).get('localization') == 'MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED' for v in news) and all(b['roots'][k] == a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
    'all_other_owned_queues_held': all(a['queues'].get(i) == v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner'] == 0),
    'native23_mineral_hulls_away_M_upkeep_held': abs(D(str(ac['budget_categories']['current_month']['expenses']['ships']['minerals']))-D('74.72517')) < D('.001'),
    'destroyed_source_no_active_EEP_no_return': aa['planets']['1578']['planet_class'] == 'pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0) == 0 and all(v.get('killed') == 'yes' for v in aa['situations'].values()),
    'positive_housing_amenities_no_crime': aa['colonies']['0']['free_amenities'] > 0 and aa['colonies']['0']['free_housing'] > 0 and aa['colonies']['0']['crime'] == 0,
    'midmonth_budget_held_or_new_month_research_job_income': (bc['budget_categories'] == ac['budget_categories'] and income(bc) == income(ac)) if not months else all(abs(D(str(ac['budget_categories']['current_month']['income'][cat][res]))-D(str(budget_country['budget_categories']['current_month']['income'][cat][res]))*D(str(aa['pop_jobs'][jid]['workforce']))/D(str(budget_base['pop_jobs'][jid]['workforce']))) < D('.001') for cat,res,jid in [('planet_biologists','society_research','24'),('planet_engineers','engineering_research','25')]),
    'CN41_unfiltered_live_error_same': package and (user/'logs/error.log').read_bytes() == (run/(before+'-error-after.log')).read_bytes() == (run/(after+'-error-after.log')).read_bytes(),
}
if after=='terravore-second-society-month-22860901':
    original=load(after+'-support-zone-v1-proof.json'); original_exec=load(after+'-support-zone-v1-guard-execution.json')
    checks['original26_only_routeFAIL_actual1_source_SAV_retained']=len(original['checks'])==26 and [k for k,v in original['checks'].items() if v is not True]==['main164_orbit_and_two_supports_native_legal_suffix'] and original_exec['returncode']==1 and original_exec['helper_sha256']=='d0eb9bbe7e51df0d9894b0030bc8c32f50121e8186e9be37f3417cbedf434cce' and original['before_sha256']==ba['save_sha256'] and original['after_sha256']==aa['save_sha256']
    checks['two_exact_native_windup_prefixes_target_orders_preserved']=all(routes[fid]['current']==30 and routes[fid]['remaining']==[30,71] and routes[fid]['state']=='move_wind_up' and q.block(a['fleets'][fid],'current_order')==q.block(b['fleets'][fid],'current_order') for fid in ['917','50332250'])
passed = all(v is True for v in checks.values()); out = run/(after+suffix+'-proof.json'); assert not out.exists()
h.write_json(out, {'status':'PASS_NATIVE_SUPPORT_ZONE' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'days':days,'research_ticks':ticks,'budget_settlements':months,'zone_completed':complete,'construction_orders':newids,'paid_zone_head_work':q.scalars(a['items'][str(newids[0])])['progress'],'project3_progress':ap['progress'],'research_jobs':{i:aa['pop_jobs'][i] for i in ['23','24','25']},'routes':routes,'regeneration':health,'cash_residual':{k:str(v) for k,v in residual.items()},'new_messages_raw':news,'boundaries':['native_paid_second_society_next_boundary_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One documented native support/hive interval only; not full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'project3':ap['progress'],'zone_completed':complete,'zone_work':q.scalars(a['items'][str(newids[0])])['progress'],'routes':routes}),flush=True)
assert passed
