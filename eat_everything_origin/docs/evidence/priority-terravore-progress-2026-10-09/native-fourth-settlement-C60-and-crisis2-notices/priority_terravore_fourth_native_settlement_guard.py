"""Independent exact native Terravore settlement and population conservation."""
import json
import logging
import re
import sys
import zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools')
sys.argv = ['runtime']
import runtime as r
import audit_save as q
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run / n).read_text('utf-8-sig'))
sha = h.sha256
obs = load(after + '-construction-boundary-observation-v2.json')
oe = load(after + '-boundary-observation-v2-execution.json')
b, a = obs['before_state'], obs['after_state']
ba, aa = b['audit'], a['audit']
bc, ac = ba['countries']['0'], aa['countries']['0']
bv, av = bc['variables'], ac['variables']
p, core = aa['planets']['523'], aa['planets']['7']
cal, ce = load(after + '-calendar-receipt.json'), load(after + '-calendar-execution.json')
pre, pe = load(cal['prior_proof_file']), load(cal['prior_execution_stage'] + '-execution.json')
review = load(cal['review_file'])
review_ex = load(review['execution_stage'] + '-execution.json')
anchor_name = 'terravore-fourth-devour-post-capture-wait-01-native-source37-battle-v2-proof.json'
anchor, anchor_ex = load(anchor_name), load('terravore-fourth-devour-post-capture-wait-01-native-source37-battle-guard-v2-execution.json')
roots = {}
for label in [before, after]:
    with zipfile.ZipFile(run / (label + '.sav')) as z:
        roots[label] = {k:v for k,v,opened in q.fields(z.read('gamestate').decode('utf-8-sig')) if opened}
omit = lambda raw, keys: [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
def structure(st):
    au = st['audit']
    ids = au['colonies']['0']['districts']
    zones = sorted({z for i in ids for z in au['districts'][str(i)]['zones'] if z != 4294967295})
    buildings = sorted({i for z in zones for i in q.ids(q.block(q.block(st['raw_roots']['zones'], str(z)), 'buildings'))})
    return {root:{str(i):q.block(st['raw_roots'][root],str(i)) for i in items}
        for root,items in {'districts':ids,'zones':zones,'buildings':buildings,'deposit':au['planets']['7']['deposits']}.items()}
def eng(st):
    raw = q.block(st['tech_status'], 'engineering_queue')
    t = list(q.tokens(raw))
    return q.scalars(raw[t[0][2]:t[-1][1]])
def objective(raw, name):
    return [q.scalars(v)['progress'] for k,v,o in q.fields(raw) if k == 'objective' and o and q.scalars(v).get('objective') == name]
crisis_b, crisis_a = [q.block(st['country0_raw'], 'crisis_progression') for st in [b,a]]
country_delays = [v for k,v,o in q.fields(q.block(q.block(a['country0_raw'], 'modules'), 'standard_event_module')) if k == 'delayed_event' and o]
sit = aa['situations']['50331660']
new = obs['new_country0_messages_raw']
ms = [q.scalars(v) for v in new]
stock = {k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in ['energy','minerals','alloys','unity','menace']}
military = {sid for raw in a['owned_fleets_raw'].values() if q.scalars(raw).get('ship_class') == 'shipclass_military'
    for sid in q.ids(q.block(raw, 'ships')) if q.scalars(a['owned_ships_raw'][str(sid)]).get('hitpoints',0)>0
    and q.scalars(a['owned_ships_raw'][str(sid)]).get('killed') != 'yes'}
typed = lambda raw: set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(raw,'combat'),'in_combat_with'))))
changes = {'eep_c':62,'eep_d':17,'eep_worlds':4,'eep_previous_capacity':14,'eep_last_return':491}
capacity_items = core['modifiers']
checks = {
    'original27_pending_actual0_fixed_source_and_last_SAV': len(pre['checks']) == 27 and all(v is True for v in pre['checks'].values())
        and pe['returncode'] == 0 and pe['helper_sha256'] == sha(Path(pe['command'][1]))
        == '87a7530927a93c52d5859aab5afe981d75706507b42161cf74b9e835d4425b95'
        and pre['after_sha256'] == ba['save_sha256'],
    'six_observations_actual0_fixed_source_and_exact_two_SAVs': len(obs['checks']) == 6 and all(v is True for v in obs['checks'].values())
        and oe['returncode'] == 0 and oe['helper_sha256'] == sha(Path(oe['command'][1]))
        == '44c27824de3486709c69acfb8ccc2b8ecff9cf356374bfd5fdc584db6a198a9b'
        and ba['save_sha256'] == sha(run / (before+'.sav')) == '09a444d71a7a3d59e24cf1c90678647ad89bfc8071ba73a9364a1af8d7d6e673'
        and aa['save_sha256'] == sha(run / (after+'.sav')) == '7e13a140ff372bb916ac3e06f97c6dfe2bdc32a7439fe76e669f2360a2c9f939',
    'exact_one_day_calendarV3_and_review11_actual0_before_GUI': cal['start_date'] == ba['date'] == '2278.10.01'
        and cal['date'] == aa['date'] == '2278.10.02' and cal['days'] == 1 and cal['business_preflight'] is True
        and ce['returncode'] == 0 and ce['helper_sha256'] == sha(Path(ce['command'][1]))
        == 'c0bd2c1b44adc36b746cc8e13d87754c7bad970cee870d4e87eb63ccbb176589'
        and len(review['checks']) == 11 and all(v is True for v in review['checks'].values())
        and review_ex['returncode'] == 0 and review_ex['helper_sha256'] == sha(Path(review_ex['command'][1]))
        == 'b0e58048f8996a3b86efe4a80c72fb337d079456a7d3ff3d0eca0b77555c8b91'
        and review['after_sha256'] == ba['save_sha256'] and cal['review_sha256'] == sha(run / cal['review_file']),
    'Q13_exact_credit49_to62_capacity14_to17_worlds3_to4_other_variables_held':
        bv['eep_c'] == 49 and av['eep_c']-bv['eep_c'] == ba['planets']['523']['variables']['eep_q'] == 13
        and bv['eep_d'] == 14 and bv['eep_worlds'] == 3 and all(av.get(k)==v for k,v in changes.items())
        and {k:v for k,v in bv.items() if k not in changes} == {k:v for k,v in av.items() if k not in changes}
        and av['eep_last_capacity'] == 3,
    'native_no_generic_generated_POP_G_made_delta_entitled_manufactured_zero':
        all(av.get(k) == bv.get(k) == 0 for k in ['eep_g','eep_made','eep_delta','eep_entitled','eep_last_manufactured']),
    'all_source391_plus_native100_return491_mother11920_conservation':
        ba['colonies']['38']['actual_pop_sum'] == 391 and ba['colonies']['0']['actual_pop_sum'] == 11429
        and av['eep_last_return'] == p['variables']['eep_return_amount'] == 491
        and aa['colonies']['0']['actual_pop_sum'] == 11920 == 11429+491
        and sum(v['size'] for v in aa['pop_groups'].values())-sum(v['size'] for v in ba['pop_groups'].values()) == 100
        and all(v['key']['species']==73 for au in [ba,aa] for v in au['pop_groups'].values()),
    'source_shattered_unowned_empty_actual_groups_and_cleared_task_deposits':
        set(bc['owned_colonies']) == {0,38} and ac['owned_colonies'] == [0]
        and p['planet_class'] == 'pc_shattered' and p['planet_size'] == 13 and p['colony'] == 38
        and 'owner' not in p and 'controller' not in p and p['deposits'] == []
        and aa['colonies']['38']['actual_pop_sum'] == 0 and not aa['colonies']['38']['pop_groups']
        and all(v['planet']==0 for v in aa['pop_groups'].values())
        and not any(k in p['flags'] for k in ['eep_active','eep_native','eep_pending','being_devoured','eep_owned_colony_event','colony_event'])
        and not p['modifiers'],
    'original_situation32_killed_tombstone_and_exact_all_settlement_step_flags':
        sit['killed'] == 'yes' and sit['progress'] == 32 and sit['target'] == ba['situations']['50331660']['target']
        and all(p['flags'].get(k)==63488424 for k in ['eep_bites_done','eep_population_done','eep_crisis_done','eep_destroy_done','eep_credit_done','eep_return_done'])
        and not any(k=='delayed_event' for k,v,o in q.fields(q.block(q.block(a['raw_roots']['situations'],'situations'),'50331660'))),
    'two_final_native_messages_alloy279_POP280_and_damage_plus40': len(ms)==2
        and [m['localization'] for m in ms] == ['MESSAGE_TERRAVORE_CONSUME_WORLD_ALLOYS_TEXT','MESSAGE_TERRAVORE_CONSUME_WORLD_POP_TEXT']
        and [m['notification'] for m in ms] == [279,280]
        and all(m['type']=='MESSAGE_TERRAVORE_CONSUME_WORLD' and m['receiver']==0 and m['target_planet']==523 and m['date']=='2278.10.02' for m in ms)
        and D(str(p['bombardment_damage']))-D(str(ba['planets']['523']['bombardment_damage'])) == 40,
    'native_alloy130_one_day_reward_and_no_energy_mineral_unity_change': stock == {'energy':D(0),'minerals':D(0),'alloys':D(130),'unity':D(0),'menace':D(750)},
    'single_destroy_world_objective750_and_native_level2_threshold':
        bc['effective_stockpile']['menace'] == 885 and ac['effective_stockpile']['menace'] == 1635
        and objective(crisis_b,'crisobj_destroy_worlds') == [750] and objective(crisis_a,'crisobj_destroy_worlds') == [1500]
        and [(v,o) for k,v,o in q.fields(crisis_b) if k=='level'] == [('crisis_level_1',False)]
        and [(v,o) for k,v,o in q.fields(crisis_a) if k=='level'] == [('crisis_level_1',False),('crisis_level_2',False)]
        and omit(crisis_b,{'level','objective'}) == omit(crisis_a,{'level','objective'}),
    'only_native_crisis4145_country0_delay3_and_Queen_notice_pending_no_player_event':
        len(country_delays)==1 and q.scalars(country_delays[0]) == {'event':'crisis.4145','days':3}
        and all(q.scalars(q.block(country_delays[0],'scope')).get(k)==v for k,v in {'type':'country','id':0,'opener_id':4294967295,'random_allowed':'yes'}.items())
        and 'eep_notice_pending' in ac['flags'] and 'eep_notice_pending' not in bc['flags']
        and {k:v for k,v in ac['flags'].items() if k!='eep_notice_pending'} == bc['flags'] and not a['pending_country0_raw'],
    'mother_capacity35_structure27_levels_and_original_jobs_held': core['planet_size'] == 18
        and core['variables']['eep_capacity_value'] == 17 and re.search(r'multiplier\s*=\s*17\s+modifier\s*=\s*"eep_capacity"',capacity_items) is not None
        and structure(b)==structure(a) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27
        and {i:v for i,v in ba['pop_jobs'].items() if v['planet']==0} == {i:v for i,v in aa['pop_jobs'].items() if v['planet']==0},
    'mother_10K_housing_amenities_crime_and_control_good': aa['colonies']['0']['actual_pop_sum']>=10000
        and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0
        and aa['colonies']['0']['crime']==0 and core['owner']==core['controller']==0,
    'original_four_native_deaths_anchor12_actual0_and_all21_owned_actual_designs_alive':
        sha(run/anchor_name)=='c8f6f43d08e3a737079fece93f8b30e66035374aba66d997d071ea51e1f88a31'
        and len(anchor['checks'])==12 and all(v is True for v in anchor['checks'].values()) and anchor_ex['returncode']==0
        and anchor_ex['helper_sha256']==sha(Path(anchor_ex['command'][1]))=='fa51dd4f8fcec3d01c24d9ada472f9973b7cd5a53541703a98eb634781d15bec'
        and b['owned_ship_ids']==a['owned_ship_ids'] and military==set(anchor['military_ids']) and len(military)==21
        and all(q.block(raw,'ship_design_implementation')==q.block(b['owned_ships_raw'][sid],'ship_design_implementation') for sid,raw in a['owned_ships_raw'].items()),
    'only_original_three_MIA_dates_and_no_owned_active_combat':
        not any(typed(raw) for raw in a['owned_fleets_raw'].values())
        and {i for i,raw in a['owned_fleets_raw'].items() if q.scalars(q.block(raw,'properties')).get('mia')=='yes'}==set(anchor['known_MIA'])
        and all(q.scalars(a['owned_fleets_raw'][i]).get('return_date')==date and q.ids(q.block(a['owned_fleets_raw'][i],'ships'))==[sid] for i,(date,sid) in anchor['known_MIA'].items()),
    'both_wars_all_fields_except_natural_fatigue_held': all(omit(q.block(roots[before]['war'],i),{'attacker_war_exhaustion','defender_war_exhaustion'})
        ==omit(q.block(roots[after]['war'],i),{'attacker_war_exhaustion','defender_war_exhaustion'}) for i in ['1','16777216']),
    'government_AP_traditions_held_real_PS_banks_increase_Eng_starbase4':
        all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions'])
        and all(ac['research_stockpile'][k]>=bc['research_stockpile'][k] for k in ['physics_research','society_research'])
        and ac['research_stockpile']['engineering_research']==bc['research_stockpile']['engineering_research']==0
        and omit(bc['tech_status'],{'stored_techpoints','engineering_queue'})==omit(ac['tech_status'],{'stored_techpoints','engineering_queue'})
        and {k:v for k,v in eng(bc).items() if k!='progress'}=={k:v for k,v in eng(ac).items() if k!='progress'}
        and eng(ac).get('technology')=='tech_starbase_4' and eng(ac).get('progress',0)>=eng(bc).get('progress',0),
    'original_unfiltered_error_production41_020_simp_chinese':
        (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()
        and sha(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41
        and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed=all(v is True for v in checks.values())
proof={'status':'PASS_NATIVE_TERRAVORE_FINAL_SETTLEMENT_COMPONENT' if passed else 'FAIL','checks':checks,
    'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],
    'before_state':b,'after_state':a,'native_final_messages_raw':new,'before_crisis_raw':crisis_b,'after_crisis_raw':crisis_a,
    'country_delayed_events_raw':country_delays,'paid_births':pre['paid_births'],
    'boundaries':['native_crisis4145_day3','queen_monthly_notice'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,
    'mother_capacity':35,'paid_district_levels':27,'returned_population':491,'native_created_population':100,
    'scope':'Exact fourth native world destruction and population conservation only. Queen notice, Nemesis research, mineral ships, reload and full route not yet accepted.'}
out=run/(after+'-native-final-settlement-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'returned':491,'capacity':35}),flush=True)
assert passed,'Original settlement failure preserved; no continuation'
