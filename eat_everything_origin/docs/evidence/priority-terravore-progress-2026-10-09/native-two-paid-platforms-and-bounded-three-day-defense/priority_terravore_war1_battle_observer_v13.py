"""Native battle loss accounting with preserved failed no-loss observer; read-only."""
import json, logging, re, shutil, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r, audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, metadata = h.load_run()
assert metadata['version'] == '0.2.0' and metadata['language'] == 'l_simp_chinese'
dest = run / Path(__file__).name
if dest.exists():
    assert dest.read_bytes() == Path(__file__).read_bytes()
else:
    shutil.copyfile(__file__, dest)
def load(name):
    return json.loads((run / name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        fields = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage + '.audit.json'), fields, {k: v for k, v, o in fields if o}
def objects(text):
    return {k: v for k, v, o in q.fields(text) if o}
def omit(text, keys):
    return [(k, v, o) for k, v, o in q.fields(text) if k not in keys]
def owned(country):
    return list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(country, 'fleets_manager'), 'owned_fleets'))))
def combat(fleet):
    return list(map(int, re.findall(r'\bfleet\s*=\s*(\d+)', q.block(q.block(fleet, 'combat'), 'in_combat_with'))))
b, bf, br = read(before)
a, af, ar = read(after)
bc, ac = b['countries']['0'], a['countries']['0']
bcr, acr = [q.block(top['country'], '0') for top in [br, ar]]
bfl, afl = objects(br['fleet']), objects(ar['fleet'])
bsh, ash = objects(br['ships']), objects(ar['ships'])
bo, ao = owned(bcr), owned(acr)
enemy_owned = owned(q.block(ar['country'], '1'))
military = lambda fleets, own: {i: q.ids(q.block(fleets[str(i)], 'ships')) for i in own
                               if q.scalars(fleets[str(i)]).get('ship_class') == 'shipclass_military'}
bm, am = military(bfl, bo), military(afl, ao)
old_ships = [i for ids in bm.values() for i in ids]
current_ships = [i for ids in am.values() for i in ids]
added_ships = [i for i in current_ships if i not in old_ships]
lost_ships = [i for i in old_ships if i not in current_ships]
original8 = {1816, 1817, 33555519, 33556208, 33556207, 50332878, 1807, 1810}
paid_ships = [i for i in current_ships if i not in original8]
receipt = load(after + '-calendar-receipt.json')
days = receipt['days']
validate_native_interval(b['date'], a['date'], days)
pre = load(receipt['prior_proof_file'])
execution = load(receipt['prior_execution_stage'] + '-execution.json')
paid_stage = 'terravore-war1-reinforce-paid'
paid = load(paid_stage + '-war1-reinforcement-payment-proof.json')
paid_execution = load(paid_stage + '-guard-execution.json')
queue = lambda top: q.block(q.block(q.block(top['construction'], 'queue_mgr'), 'queues'), '3')
bq, aq = queue(br), queue(ar)
bids, aids = [q.ids(q.block(v, 'items')) for v in [bq, aq]]
items = lambda top: objects(q.block(q.block(top['construction'], 'item_mgr'), 'items'))
bi, ai = items(br), items(ar)
completed = len(bids) - len(aids)
base_b, base_a = [q.block(q.block(top['starbase_mgr'], 'starbases'), '0') for top in [br, ar]]
pending = [q.scalars(v) for k, v, o in af if k == 'player_event' and o and q.scalars(v).get('country') == 0]
active = {i: combat(afl[str(i)]) for i in ao if combat(afl[str(i)])}
target = a['planets']['1085']
mother = a['planets']['7']
colony = a['colonies']['37']
nets = {k: sum(D(str(v.get(k, 0))) for v in ac['budget_categories']['current_month']['balance'].values())
        for k in ['energy', 'minerals', 'alloys', 'unity', 'trade']}
project2 = lambda country: [v for k, v, o in q.fields(q.block(country, 'events'))
                          if k == 'special_project' and o and q.scalars(v).get('id') == 2]
war = q.block(ar['war'], '1')
cumulative_original_lost = set(pre.get('cumulative_original_lost', [])) | (set(lost_ships) & original8)
cumulative_paid_lost = set(pre.get('cumulative_paid_lost', [])) | (set(lost_ships) - original8)
observed_paid = set(pre.get('all_observed_paid_ship_ids', set(old_ships) - original8)) | set(added_ships)
all_current_references = {i for raw in afl.values() for i in q.ids(q.block(raw, 'ships'))}
lost_by_fleet = {fid: [i for i in ids if i in lost_ships] for fid,ids in bm.items()}
def loss_stats(raw):
    stats = q.block(q.block(raw, 'fleet_stats'), 'combat_stats')
    own_stats = q.block(stats, 'fleet')
    return q.scalars(stats).get('date'), sum(q.ids(q.block(own_stats, 'ship_size_count_lost')))
def anonymous_objects(text):
    depth=0; start=None
    for token,beg,end in q.tokens(text):
        if token=='{':
            if depth==0: start=end
            depth+=1
        elif token=='}':
            depth-=1
            if depth==0: yield text[start:beg]
weapon_aggregate_evidence=[]
weapon_fields={
    'damage_outgoing':{'damage_hitpoints','damage_shields','damage_armor','base_damage_hitpoints','base_damage_shields','base_damage_armor'},
    'damage_incoming':{'damage_hitpoints','damage_shields','damage_armor','base_damage_hitpoints','base_damage_shields','base_damage_armor'},
    'hit_ratio_outgoing':{'hits','misses','evades'},
    'hit_ratio_incoming':{'hits','misses','evades'},
    'targetables_killed_outgoing':{'missile','strike_craft'},
}
def weapon_groups(stats,field):
    blocks=[v for k,v,o in q.fields(stats) if k==field and o]
    assert len(blocks)==1
    identities=set();totals={}
    for row in anonymous_objects(blocks[0]):
        fields=list(q.fields(row)); values=q.scalars(row)
        assert len({k for k,v,o in fields})==len(fields)
        assert all(k in weapon_fields[field]|{'template','fleet_index','ship_design_implementation'} for k,v,o in fields)
        assert all(k=='ship_design_implementation' and field.startswith('hit_ratio_') for k,v,o in fields if o)
        assert type(values.get('fleet_index')) is int and values['fleet_index']==0
        if field.startswith('targetables_'):
            assert 'template' not in values
        else:
            assert isinstance(values.get('template'),str) and values['template']
        identity=(values.get('template'),tuple(t for t,b,e in q.tokens(q.block(row,'ship_design_implementation'))))
        identities.add(identity)
        for key in weapon_fields[field]:
            value=D(str(values.get(key,0)))
            assert value.is_finite() and value>=0
            assert field.startswith('damage_') or value==value.to_integral_value()
            totals[(identity,key)]=totals.get((identity,key),D(0))+value
    assert identities
    return identities,totals

def cumulative_weapons(oldstats,live,newstats,fid):
    evidence=[]
    try:
        for field in weapon_fields:
            oldids,old=weapon_groups(oldstats,field)
            liveids,before_live=weapon_groups(live,field)
            newids,new=weapon_groups(newstats,field)
            assert newids==oldids|liveids
            assert all(new.get(key,D(0))+D('.0001')>=old.get(key,D(0))+before_live.get(key,D(0)) for key in set(old)|set(before_live))
            evidence.append({'field':field,'identity_counts':[len(oldids),len(liveids),len(newids)],
                'old_totals':{k:str(sum(v for (i,key),v in old.items() if key==k)) for k in sorted(weapon_fields[field])},
                'live_before_totals':{k:str(sum(v for (i,key),v in before_live.items() if key==k)) for k in sorted(weapon_fields[field])},
                'new_totals':{k:str(sum(v for (i,key),v in new.items() if key==k)) for k in sorted(weapon_fields[field])}})
    except (AssertionError,ValueError,TypeError):
        return False
    weapon_aggregate_evidence.append({'fleet':fid,'fields':evidence})
    return True

coherent_appended_reports=[]
def tokvalues(raw):return [token for token,beg,end in q.tokens(raw)]
def coherent_existing_report(message,fid):
    now=q.scalars(message)
    prior=[v for k,v,o in bf if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('notification')==now.get('notification') and q.scalars(v).get('date')==now.get('date')]
    if len(prior)!=1 or now.get('receiver')!=0:return False
    previous=prior[0];old=q.scalars(previous)
    oldstats,newstats=[q.block(v,'combat_stats') for v in [previous,message]]
    oldown,newown=[list(anonymous_objects(q.block(v,'fleets'))) for v in [oldstats,newstats]]
    target=[v for v in newown if q.scalars(v).get('fleet')==fid and q.scalars(v).get('country')==0]
    others=[v for v in newown if v not in target]
    oldmsg=[(k,v) for k,v in old.items() if k!='end'];newmsg=[(k,v) for k,v in now.items() if k!='end']
    global_dates=[q.scalars(q.block(fleets['825'],'combat')).get('start_date') for fleets in [bfl,afl]]
    enemy=[q.scalars(v) for v in anonymous_objects(q.block(newstats,'enemy'))]
    valid=oldmsg==newmsg and old.get('end','')<=now.get('end','') and q.scalars(oldstats).get('date')==q.scalars(newstats).get('date') and q.scalars(oldstats).get('reason') in {'we_escaped','we_destroyed'} and q.scalars(newstats).get('reason') in {'we_escaped','we_destroyed'} and [(k,tokvalues(v),o) for k,v,o in q.fields(oldstats) if k not in {'reason','fleets'}|set(weapon_fields)]==[(k,tokvalues(v),o) for k,v,o in q.fields(newstats) if k not in {'reason','fleets'}|set(weapon_fields)] and bool(oldown) and len(newown)==len(oldown)+1 and len(target)==1 and target[0]==newown[-1] and [tokvalues(v) for v in oldown]==[tokvalues(v) for v in others]
    # Compare original counts from their proper native blocks, never inferred fleet size.
    original=q.block(q.block(q.block(bfl[str(fid)],'fleet_stats'),'combat_stats'),'fleet')
    valid=valid and q.ids(q.block(target[0],'ship_size_count'))==q.ids(q.block(original,'ship_size_count')) and global_dates[0]==global_dates[1]=='2268.06.14' and combat(bfl['0'])==combat(afl['0'])==[825] and any(v.get('fleet')==825 and v.get('country')==1 for v in enemy)
    valid=valid and cumulative_weapons(oldstats,q.block(q.block(bfl[str(fid)],'fleet_stats'),'combat_stats'),newstats,fid)
    if valid:coherent_appended_reports.append({'notification':now['notification'],'message_date':now['date'],'report_start':q.scalars(newstats)['date'],'previous_end':old['end'],'new_end':now['end'],'previous_fleet_ids':[q.scalars(v)['fleet'] for v in oldown],'appended_fleet':fid})
    return valid

def observed_after_loss(fid,date):
    if str(fid) in afl and loss_stats(afl[str(fid)])[0]==date:
        return loss_stats(afl[str(fid)])[1]
    records=[]
    for key,value,obj in af:
        if key!='message' or not obj or q.scalars(value).get('type')!='COMBAT_STATS': continue
        stats=q.block(value,'combat_stats')
        enemy_start=q.scalars(q.block(afl['825'],'combat')).get('start_date')
        enemy_records=[q.scalars(x) for x in anonymous_objects(q.block(stats,'enemy'))]
        if q.scalars(stats).get('reason') not in {'we_escaped','we_destroyed'}: continue
        if q.scalars(stats).get('date') not in {date,enemy_start} and not coherent_existing_report(value,fid): continue
        if not any(x.get('fleet')==825 and x.get('country')==1 for x in enemy_records): continue
        for own_stats in anonymous_objects(q.block(stats,'fleets')):
            fields=q.scalars(own_stats)
            if fields.get('fleet')==fid and fields.get('country')==0:
                records.append(sum(q.ids(q.block(own_stats,'ship_size_count_lost'))))
    return records[0] if len(records)==1 else None
prior_pending_dead=set(pre.get('actual_pending_destroyed_ship_ids',[]))
raw_prior_pending={i for i in old_ships if q.scalars(bsh[str(i)]).get('killed')=='yes' or q.scalars(bsh[str(i)]).get('hitpoints',0)<=0}
current_pending_dead={i for i in current_ships if q.scalars(ash[str(i)]).get('killed')=='yes' or q.scalars(ash[str(i)]).get('hitpoints',0)<=0}
new_pending_by_fleet={fid:[i for i in ids if i in current_pending_dead] for fid,ids in bm.items()}
def exact_loss_explained(fid,ids):
    new_pending=new_pending_by_fleet[fid]
    if not ids and not new_pending: return True
    date=q.scalars(q.block(bfl[str(fid)],'combat')).get('start_date')
    final=observed_after_loss(fid,date)
    expected=len(ids)-len(set(ids)&prior_pending_dead)+len(new_pending)
    return combat(bfl[str(fid)])==[825] and loss_stats(bfl[str(fid)])[0]==date and final is not None and final-loss_stats(bfl[str(fid)])[1]==expected
explained_losses=all(exact_loss_explained(fid,ids) for fid,ids in lost_by_fleet.items())

bprogress, aprogress = [q.block(c,'crisis_progression') for c in [bcr,acr]]
bobjectives, aobjectives = [[v for k,v,o in q.fields(c) if k=='objective' and o] for c in [bprogress,aprogress]]
menace_delta = D(str(ac['effective_stockpile']['menace']))-D(str(bc['effective_stockpile']['menace']))
objective_changes=[]
progression_held = omit(bprogress,{'objective'})==omit(aprogress,{'objective'}) and len(bobjectives)==len(aobjectives)
for old,new in zip(bobjectives,aobjectives):
    os,ns=q.scalars(old),q.scalars(new)
    if os.get('objective')=='crisobj_destroy_enemy_ships':
        delta=D(str(ns.get('progress',0)))-D(str(os.get('progress',0)))
        objective_changes.append(delta)
        progression_held &= omit(old,{'progress'})==omit(new,{'progress'}) and delta==menace_delta
    else:
        progression_held &= old==new
progression_held &= len(objective_changes)==1 and q.scalars(aprogress)=={'path':'nemesis_path','level':'crisis_level_1'}
before_enemy=set(q.ids(q.block(bfl['825'],'ships')))
after_enemy=set(q.ids(q.block(afl['825'],'ships')))
missing_enemy=sorted(before_enemy-after_enemy)
battle_losses_before=loss_stats(bfl['825'])
battle_losses_after=loss_stats(afl['825'])
native_enemy_loss_bound = after_enemy<=before_enemy and battle_losses_before[0]==battle_losses_after[0]=='2268.06.14' and battle_losses_after[1]-battle_losses_before[1]==len(missing_enemy) and all(str(i) not in ash and i not in all_current_references for i in missing_enemy)
menace_eligible_bound = menace_delta>=0 and menace_delta%15==0 and menace_delta<=15*len(missing_enemy)
game=Path('C:/SteamLibrary/steamapps/common/Stellaris')
source_bindings={
    'common/crisis_objectives/00_crisis_objectives.txt':'e5caaa3be22664c20ea341c2dac33d2d93b099abb4a2b4b361feb2e54915851b',
    'events/nemesis_crisis_menace_objective_events.txt':'f38d1c9291767ea4b1845214198fd2d84686db9e3a89d3e49180d6a6d2f2b261'}
native_menace_source_bound=all(h.sha256(game/name)==sha for name,sha in source_bindings.items()) and q.scalars(ar['galaxy']).get('template')=='tiny' and q.scalars(q.block((game/'map/setup_scenarios/tiny.txt').read_text('utf-8-sig'),'setup_scenario')).get('num_stars')==200
for name in [*source_bindings,'map/setup_scenarios/tiny.txt']:
    dest=run/('native-war1-menace-'+Path(name).name)
    if dest.exists(): assert dest.read_bytes()==(game/name).read_bytes()
    else: shutil.copyfile(game/name,dest)
prior_naval_death_credit=D(str(pre.get('actual_naval_death_cache_credit',0)))
actual_naval_cache=D(str(q.scalars(acr)['fleet_size']))
naval_death_credit=actual_naval_cache-D(5*len(current_ships))
checks = {
    'prior_all_PASS_actual0_original_helper_bound': pre['status'].startswith('PASS_')
        and bool(pre['checks']) and all(v is True for v in pre['checks'].values())
        and pre['after_sha256'] == b['save_sha256'] and execution['returncode'] == 0
        and h.sha256(run / Path(execution['command'][1]).name) == execution['helper_sha256'],
    'actual_SHA_pair_unique_native_calendar1_to30_actual0':
        all(h.sha256(run / (st + '.sav')) == au['save_sha256'] for st, au in [(before, b), (after, a)])
        and 1 <= days <= 30 and receipt['status'] == 'CALENDAR_CONFIRMED'
        and receipt['start_date'] == b['date'] and receipt['date'] == a['date']
        and load(after + '-calendar-execution.json')['returncode'] == 0,
    'fixed_original45_paid30_orders_SHA_actual0_bound':
        paid['status'] == 'PASS_TERRAVORE_WAR1_REINFORCEMENT_PAYMENT_COMPONENT'
        and len(paid['checks']) == 45 and all(v is True for v in paid['checks'].values())
        and paid['after_sha256'] == h.sha256(run / (paid_stage + '.sav'))
        == 'b4344cd46f423531c3a23607248276c9b963cfa66be6d6572fb0ad08637ca36c'
        and paid_execution['returncode'] == 0
        and paid_execution['helper_sha256'] == 'ffe533def5fd2da48252413df05b336729a7935fc59428929a1a576943cd51e1',
    'paid_orders_contiguous_completion_and_original_nonprogress_raw_held':
        completed >= 0 and aids == bids[completed:]
        and aids == paid['native_queue_ids'][30-len(aids):]
        and all(omit(bi[str(i)], {'progress'}) == omit(ai[str(i)], {'progress'})
                and 0 <= q.scalars(ai[str(i)])['progress'] < 60 for i in aids),
    'actual_paid_ship_count_and_order_conservation_explained_combat_losses':
        len(added_ships) == completed and len(paid_ships) + len(aids) + len(cumulative_paid_lost) == 30
        and len(original8 & set(current_ships)) + len(cumulative_original_lost) == 8
        and set(observed_paid) == set(paid_ships) | cumulative_paid_lost,
    'all_military_relations_unique_positive_or_proven_killed_pending_hull':
        len(current_ships) == len(set(current_ships))
        and all(q.scalars(ash[str(i)])['fleet'] == fid
                and ((i not in current_pending_dead and 0 < q.scalars(ash[str(i)])['hitpoints'] <= q.scalars(ash[str(i)])['max_hitpoints']) or i in current_pending_dead)
                for fid, ids in am.items() for i in ids),
    'surviving_original8_actual_design_dates_max_HP270_held': all(
        0 < q.scalars(ash[str(i)])['hitpoints'] <= q.scalars(ash[str(i)])['max_hitpoints'] == 270
        and q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))['design'] == 167772797
        and q.scalars(bsh[str(i)])['construction_date'] == q.scalars(ash[str(i)])['construction_date']
        for i in original8 & set(current_ships)),
    'paid_built_ships_actual_design_dates_and_no_actual_free_upgrade': all(
        q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))['design'] == 385877628
        and q.scalars(q.block(ash[str(i)], 'ship_design_implementation'))['growth_stage'] == 0
        and q.scalars(ash[str(i)])['upgrade_progress'] == 0
        and '2268.03.17' <= q.scalars(ash[str(i)])['construction_date'] <= a['date'] for i in paid_ships)
        and all(b['date'] <= q.scalars(ash[str(i)])['construction_date'] <= a['date'] for i in added_ships)
        and all(q.scalars(bsh[str(i)])['construction_date'] == q.scalars(ash[str(i)])['construction_date']
                for i in set(old_ships) & set(paid_ships)),
    'native_naval_size5_per_object_plus_proven_unconsumed_death_cache_credit': prior_naval_death_credit.is_finite() and prior_naval_death_credit>=0 and prior_naval_death_credit%5==0 and D(str(q.scalars(bcr)['fleet_size']))==D(5*len(old_ships))+prior_naval_death_credit and naval_death_credit.is_finite() and 0<=naval_death_credit<=prior_naval_death_credit+D(5*len(lost_ships)) and naval_death_credit%5==0 and explained_losses,
    'original_two_shipyards_base0_queue3_nonitem_fields_held':
        omit(bq, {'items'}) == omit(aq, {'items'})
        and q.scalars(q.block(base_b, 'modules')) == q.scalars(q.block(base_a, 'modules'))
        == {'0': 'shipyard', '1': 'shipyard'}
        and all(q.scalars(base_b)[k] == q.scalars(base_a)[k]
                for k in ['level', 'type', 'build_queue', 'shipyard_build_queue', 'station'])
        and q.block(base_b, 'buildings') == q.block(base_a, 'buildings'),
    'EEP_ledger_flags_species_targets_and_no_active_task_held':
        bc['variables'] == ac['variables'] and bc['flags'] == ac['flags']
        and all(ac['variables'][k] == v for k, v in {'eep_c': 37, 'eep_g': 0, 'eep_d': 11, 'eep_made': 0, 'eep_worlds': 2, 'eep_psi': 1}.items())
        and b['species'] == a['species'] and b['event_targets'] == a['event_targets'] and not a['situations'],
    'unique_mother_owned_core_capacity11_no_new_bombardment':
        mother['owner'] == mother['controller'] == 0 and mother['colony'] == 0
        and mother['planet_size'] == 18 and mother['variables']['eep_capacity_value'] == 11
        and sum('eep_core' in v['flags'] for v in a['planets'].values()) == 1
        and mother['modifiers'] == b['planets']['7']['modifiers']
        and mother['bombardment_damage'] == 0 and mother['last_bombardment'] == '2261.07.03',
    'all_mother_zones_buildings_districts_raw_held':
        all(q.block(br['zones'], i) == q.block(ar['zones'], i) for i in ['0', '2', '61'])
        and all(q.block(br['districts'], i) == q.block(ar['districts'], i) for i in ['1', '2', '3'])
        and all(q.block(br['buildings'], str(i)) == q.block(ar['buildings'], str(i))
                for zid in ['0', '2', '61'] for i in q.ids(q.block(q.block(ar['zones'], zid), 'buildings'))),
    'original_full_mother_jobs_housing_amenities_stability80_held':
        all(len([j for j in a['pop_jobs'].values() if j['planet'] == 0 and j['type'] == kind
                 and j['workforce'] == j['max_workforce'] == n]) == 1
            for kind, n in [('fabricator', 200), ('coordinator', 2000), ('logistics_drone', 500),
                            ('telepath_drone', 200), ('calculator_physicist', 300), ('calculator_biologist', 300),
                            ('calculator_engineer', 300), ('mining_drone', 2400), ('technician_drone', 1200)])
        and a['colonies']['0']['free_housing'] > 0 and a['colonies']['0']['free_amenities'] > 0
        and a['colonies']['0']['stability'] == 80 and a['colonies']['0']['crime'] == 0,
    'same_native_colony37_1085_owned_species73_still_colonizing':
        bc['owned_colonies'] == ac['owned_colonies'] == [0, 37]
        and target['owner'] == target['controller'] == 0 and target['colony'] == 37
        and target['planet_size'] == 12 and target['planet_class'] == 'pc_alpine'
        and target['bombardment_damage'] == 0 and target['last_bombardment'] == '0.01.01'
        and colony.get('colonizing_species') == 73
        and colony['actual_pop_sum'] >= b['colonies']['37']['actual_pop_sum']
        and all(a['pop_groups'][str(i)]['key']['species'] == 73 for i in colony['pop_groups']),
    'native_finished_PSIONIC1_full_breach_level1_menace90_held':
        len(project2(bcr)) == len(project2(acr)) == 1 and project2(bcr) == project2(acr)
        and q.scalars(project2(acr)[0]).get('status') == 'completed'
        and progression_held
        and ac['effective_stockpile']['menace'] >= bc['effective_stockpile']['menace'] >= 90
        and all(q.scalars(q.block(acr, 'flags')).get(k) == value for k, value in [
            ('breached_shroud', 63314904), ('psionic_traditions_unlocked', 63314904),
            ('crisis_special_project_1_complete', 63355224)]),
    'actual_war1_participants_objectives_start_held': q.scalars(war)['start_date'] == '2265.12.30'
        and re.findall(r'\bcountry\s*=\s*(\d+)', q.block(war, 'attackers')) == ['1']
        and re.findall(r'\bcountry\s*=\s*(\d+)', q.block(war, 'defenders')) == ['0']
        and q.scalars(q.block(war, 'attacker_war_goal'))['type'] == 'wg_end_threat_swarm'
        and q.scalars(q.block(war, 'defender_war_goal'))['type'] == 'wg_absorption',
    'current_owned_combat_only_actual_war1_enemy_fleets':
        all(i in enemy_owned for enemies in active.values() for i in enemies),
    'all_actual_primary_stocks_positive_report_actual_nets':
        all(ac['effective_stockpile'][k] > 0 for k in ['energy', 'minerals', 'alloys', 'unity']),
    'unfiltered_error2670_exact_held': (run / (before + '-error-after.log')).read_bytes()
        == (run / (after + '-error-before.log')).read_bytes() == (run / (after + '-error-after.log')).read_bytes()
        and (run / (after + '-error-after.log')).stat().st_size == 2670,
}
if before == paid_stage:
    checks['first_month_exact_477_captured_disabled_no_original_military_loss'] = (
        a['date'] == '2268.04.17' and days == 30
        and 477 in bo and 477 not in ao and 477 in enemy_owned
        and q.ids(q.block(afl['477'], 'ships')) == [1415]
        and q.scalars(ash['1415'])['original_owner'] == 0
        and q.scalars(ash['1415'])['disabled'] == 'yes' and q.scalars(ash['1415'])['hitpoints'] == 1
        and q.scalars(ash['1415'])['last_damage'] == q.scalars(ash['1415'])['last_combat_activity'] == '2268.03.22'
        and q.scalars(ash['1415'])['construction_date'] == q.scalars(bsh['1415'])['construction_date'] == '2223.11.21'
        and q.block(ash['1415'], 'ship_design_implementation') == q.block(bsh['1415'], 'ship_design_implementation')
        and combat(bfl['477']) == [825] and combat(bfl['825']) == [477]
        and q.scalars(q.block(bfl['477'], 'combat'))['start_date'] == '2268.03.12'
        and q.ids(q.block(afl['825'], 'ships')) == q.ids(q.block(bfl['825'], 'ships'))
        and len(aids) == 30 and not added_ships and not lost_ships
        and [q.scalars(ai[str(i)])['progress'] for i in aids] == [37.5, 37.5] + [0] * 28)
checks['all_missing_ships_exact_native_same_battle_loss_counts'] = explained_losses \
    and all(str(i) not in ash and i not in all_current_references for i in lost_ships) \
    and all(i not in current_ships for i in cumulative_original_lost | cumulative_paid_lost)
checks['actual_surviving_hull_damage_has_native_battle_date'] = all(
    '2268.06.14' <= q.scalars(ash[str(i)]).get('last_damage','0.01.01') <= a['date']
    for i in current_ships if q.scalars(ash[str(i)])['hitpoints'] < q.scalars(ash[str(i)])['max_hitpoints'])
base_ship = q.scalars(ash['0'])
checks['paid_defensive_tree_and_vigilance_base0_hull18300_same_design_owned'] = 0 in ao \
    and base_ship['fleet'] == base_ship['original_owner'] == 0 \
    and base_ship['max_hitpoints'] == 18300 and 0 < base_ship['hitpoints'] <= 18300 \
    and all(0 <= base_ship.get(k,0) <= base_ship[maxk] for k,maxk in
        [('shield_hitpoints','max_shield_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]) \
    and q.block(ash['0'],'ship_design_implementation') == q.block(bsh['0'],'ship_design_implementation') \
    and 'tr_unyielding_defensive_zeal' in ac['traditions'] and 'tr_unyielding_finish' in ac['traditions'] and 'ap_eternal_vigilance' in ac['ascension_perks']
if after == 'terravore-war1-defense-sixdays1':
    original_failure = load(after + '-guard-execution.json')
    checks['first6days_exact_original_failure_and_actual3loss2build_bound'] = \
        original_failure['returncode'] == 1 \
        and original_failure['helper_sha256'] == '085a7db14a6a9ea094d292a1948eba806409b9dd9e0a54bb7ce8e4f3e939f394' \
        and "KeyError: '50332878'" in (run/(after+'-guard-stderr.txt')).read_text('utf-8') \
        and not (run/(after+'-war1-combat-colonization-proof.json')).exists() \
        and set(lost_ships) == {50332878,33556208,33556207} \
        and set(added_ships) == {67110094,50333423} and len(aids) == 26 \
        and days == 6 and a['date'] == '2268.06.23' and base_ship['hitpoints'] == 15800
if after=='terravore-war1-defense-fortnight1':
    old=load(after+'-war1-battle-v2-proof.json'); oldex=load(after+'-battle-v2-execution.json')
    checks['first14days_original23_only_loss_stats_FAIL_and_exact_two_losses_bound'] = old['status']=='FAIL' and len(old['checks'])==23 and [k for k,v in old['checks'].items() if not v]==['all_missing_ships_exact_native_same_battle_loss_counts'] and oldex['returncode']==1 and oldex['helper_sha256']=='3f843f1ed420de5bc496fe7f1ba9e296c0e26ebcd373b9a26c3ba6d7cfe6a271' and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'] and set(lost_ships)=={1817,67110094} and len(current_ships)==7 and len(aids)==26 and q.scalars(afl['788']).get('mia_type')=='mia_emergency_ftl' and q.scalars(afl['788']).get('return_date')=='2270.01.07' and q.scalars(afl['33555013']).get('mia_type')=='mia_emergency_ftl' and q.scalars(afl['33555013']).get('return_date')=='2270.01.10'
ap_stage='terravore-war1-vigilance-selected2'
ap_proof=load(ap_stage+'-vigilance-ap-proof.json'); ap_ex=load(ap_stage+'-guard-execution.json')
checks['actual_paid_full_tree_vigilance_AP12_PASS_SHA_actual0_bound'] = ap_proof['status']=='PASS_TERRAVORE_NATIVE_PAID_TREE_VIGILANCE_AP_COMPONENT' and len(ap_proof['checks'])==12 and all(v is True for v in ap_proof['checks'].values()) and ap_ex['returncode']==0 and ap_ex['helper_sha256']=='0c40a2cff326a2422e03a60a9982e0602d35f222f3a647f0ec785d94c5122c29' and ap_proof['after_sha256']==h.sha256(run/(ap_stage+'.sav'))=='7a9e7d08a39265359a253ce26774d928b4bf18de976c31b651fb5fc1263f4798'
if after=='terravore-war1-defense-fortnight2':
    old=load(after+'-war1-battle-v4-proof.json'); oldex=load(after+'-battle-v4-execution.json')
    checks['first_updated_aggregate_report_original24_one_FAIL_exact_last_paid_loss_bound'] = old['status']=='FAIL' and len(old['checks'])==24 and [k for k,v in old['checks'].items() if not v]==['all_missing_ships_exact_native_same_battle_loss_counts'] and oldex['returncode']==1 and oldex['helper_sha256']=='19e4801213bab14c9a3149fafd5df5562917662ad633bdc7563d00585f53485e' and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'] and lost_ships==[50333423] and len(current_ships)==6 and len(aids)==26 and [q.scalars(ai[str(i)])['progress'] for i in aids[:2]]==[44.24,44.24]
checks['native_enemy825_loss_real_objects_and_15_menace_progression_source_bound'] = native_enemy_loss_bound and menace_eligible_bound and native_menace_source_bound
if after=='terravore-war1-defense-three-days2':
    old=load(after+'-war1-battle-v5-proof.json'); oldex=load(after+'-battle-v5-execution.json')
    checks['first_menace_gain_original24_single_FAIL_exact_real_enemy_loss_bound'] = old['status']=='FAIL' and len(old['checks'])==24 and [k for k,v in old['checks'].items() if not v]==['native_finished_PSIONIC1_full_breach_level1_menace90_held'] and oldex['returncode']==1 and oldex['helper_sha256']=='47d2f746067431ed6c51f14f8301ed6f68cd4d9f79d86dc2d513f28f653c448e' and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'] and missing_enemy==[16779066] and menace_delta==15 and bc['effective_stockpile']['menace']==90 and ac['effective_stockpile']['menace']==105
rear_paid_stage='terravore-war1-rear-starport-paid'
rear_paid=load(rear_paid_stage+'-rear-starport-payment-proof.json')
rear_execution=load(rear_paid_stage+'-guard-execution.json')
rear_bbase,rear_abase=[q.block(q.block(t['starbase_mgr'],'starbases'),'153') for t in [br,ar]]
rear_bqueue,rear_aqueue=[q.block(q.block(q.block(t['construction'],'queue_mgr'),'queues'),'2278') for t in [br,ar]]
rear_bitem,rear_aitem=[q.block(items_raw,'234881044') for items_raw in [q.block(q.block(br['construction'],'item_mgr'),'items'),q.block(q.block(ar['construction'],'item_mgr'),'items')]]
rear_expected_progress=D(str(q.scalars(rear_bitem)['progress']))+D('1.5')*days
checks['rear125_payment20_PASS_actual0_exact_native_order_source_bound']=rear_paid['status']=='PASS_TERRAVORE_NATIVE_REAR_STARPORT_PAYMENT_COMPONENT' and len(rear_paid['checks'])==20 and all(v is True for v in rear_paid['checks'].values()) and rear_execution['returncode']==0 and rear_execution['helper_sha256']=='a8a52e34638492a7fe0c1a317c54cd9d5238a1192c2d2abf119fe785ec5aa8cf' and h.sha256(run/Path(rear_execution['command'][1]).name)==rear_execution['helper_sha256'] and rear_paid['after_sha256']==h.sha256(run/(rear_paid_stage+'.sav'))=='2a3381a6d47c8105714fe2379c6d0a859f35ae5f90f74ce1e0ec3218a3aebee3' and rear_paid['paid_alloys']==125 and rear_paid['rear_order_id']==234881044
checks['rear153_owned_outpost_same_station_no_shipyard_and_exact_1point5_work_daily']=rear_bbase==rear_abase and q.scalars(rear_abase)=={'level':'starbase_level_outpost','build_queue':2278,'shipyard_build_queue':4294967295,'station':67109591} and 804 in ao and q.scalars(ash['67109591'])['fleet']==804 and q.scalars(ash['67109591'])['hitpoints']>0 and rear_bqueue==rear_aqueue and q.ids(q.block(rear_aqueue,'items'))==[234881044] and omit(rear_bitem,{'progress'})==omit(rear_aitem,{'progress'}) and omit(rear_aitem,{'progress'})==omit(rear_paid['rear_order_raw'],{'progress'}) and D(str(q.scalars(rear_aitem)['progress']))==rear_expected_progress<360
if after=='terravore-war1-defense-sixdays4':
    failed=load(after+'-war1-battle-v7-proof.json');failed_ex=load(after+'-battle-v7-execution.json')
    checks['first_continuous_report210_original27_single_FAIL_exact_last_paid_loss_bound']=failed['status']=='FAIL' and len(failed['checks'])==27 and [k for k,v in failed['checks'].items() if not v]==['all_missing_ships_exact_native_same_battle_loss_counts'] and failed_ex['returncode']==1 and failed_ex['helper_sha256']=='f51472626d0ec58f5a6fea2225df96fff6a63ba4abf7543a94c861d366919841' and failed['before_sha256']==b['save_sha256'] and failed['after_sha256']==a['save_sha256'] and lost_ships==[67110636] and base_ship['hitpoints']==959.2447 and coherent_appended_reports==[{'notification':210,'message_date':'2268.08.26','report_start':'2268.08.01','previous_end':'2268.10.11','new_end':'2268.11.15','previous_fleet_ids':[100664127],'appended_fleet':67109687}]
if after=='terravore-war1-defense-sixdays4':
    failed8=load(after+'-war1-battle-v8-proof.json');failed8_ex=load(after+'-battle-v8-execution.json')
    checks['first_weapon_aggregate_original28_exact_two_FAIL_and_same_SAV_bound']=failed8['status']=='FAIL' and len(failed8['checks'])==28 and {k for k,v in failed8['checks'].items() if not v}=={'all_missing_ships_exact_native_same_battle_loss_counts','first_continuous_report210_original27_single_FAIL_exact_last_paid_loss_bound'} and failed8_ex['returncode']==1 and failed8_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v8.py')=='f1b46665b12557b9fc363c80e07115704cee9f1becd38a949d76ba6f2ed529c5' and failed8['before_sha256']==b['save_sha256'] and failed8['after_sha256']==a['save_sha256'] and len(weapon_aggregate_evidence)==1 and weapon_aggregate_evidence[0]['fleet']==67109687 and len(weapon_aggregate_evidence[0]['fields'])==5
mine_paid_stage='terravore-war1-three-mines-paid'
mine_paid=load(mine_paid_stage+'-three-mines-payment-proof.json');mine_ex=load(mine_paid_stage+'-guard-execution.json')
mine_ids=[1006632966,1207959563,905969668]
mbq,maq=[q.block(q.block(q.block(top['construction'],'queue_mgr'),'queues'),'0') for top in [br,ar]]
checks['three_mines720_payment29_PASS_actual0_exact_SHA_source_bound']=mine_paid['status']=='PASS_TERRAVORE_THREE_NATIVE_MINES_PAYMENT_COMPONENT' and len(mine_paid['checks'])==29 and all(v is True for v in mine_paid['checks'].values()) and mine_ex['returncode']==0 and mine_ex['helper_sha256']==h.sha256(run/'priority_terravore_three_mines_payment_guard.py')=='b70baab22a2dc3728c5b450e369e0dec4dce8f53e6743523dd112f796b4edfb6' and mine_paid['after_sha256']==h.sha256(run/(mine_paid_stage+'.sav'))=='e7e169e2a49f06ee8a4cf134367f21dd80d299af2250953542ba4a87f03b52a8' and mine_paid['actual_paid_minerals']==720 and mine_paid['actual_order_ids']==mine_ids
checks['three_mines_queue0_original_paid_raw_incomplete_exact_1point4_work_daily']=q.ids(q.block(mbq,'items'))==q.ids(q.block(maq,'items'))==mine_ids and omit(mbq,{'items'})==omit(maq,{'items'}) and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'})==omit(original,{'progress'}) for i,original in zip(mine_ids,mine_paid['actual_order_raw'])) and D(str(q.scalars(ai[str(mine_ids[0])])['progress']))==D(str(q.scalars(bi[str(mine_ids[0])])['progress']))+D('1.4')*days<240 and all(q.scalars(bi[str(i)])['progress']==q.scalars(ai[str(i)])['progress']==0 for i in mine_ids[1:])
if after=='terravore-war1-postmines-paid-day1':
    original9=load(after+'-war1-battle-v9-proof.json');original9_ex=load(after+'-battle-v9-execution.json')
    checks['first_mine_day_independent_original27PASS_actual0_same_SHA_bound']=original9['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' and len(original9['checks'])==27 and all(v is True for v in original9['checks'].values()) and original9_ex['returncode']==0 and original9_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v9.py')=='a39f884b439203a964353ed00c8111f732aa1fcd34ab7b71f9bd0be3d52a0717' and original9['before_sha256']==b['save_sha256'] and original9['after_sha256']==a['save_sha256'] and days==1 and a['date']=='2268.11.10'
pending_state_valid=prior_pending_dead==raw_prior_pending and not (prior_pending_dead&current_pending_dead)
if prior_pending_dead:
    pending_state_valid &= days==1 and prior_pending_dead<=set(lost_ships) and all(str(i) not in ash and i not in all_current_references for i in prior_pending_dead)
for i in current_pending_dead:
    state=q.scalars(ash[str(i)]);old=q.scalars(bsh[str(i)]) if str(i) in bsh else {}
    hull=D(str(state.get('hitpoints','NaN')));fid=state.get('fleet')
    pending_state_valid &= i in observed_paid and i in old_ships and i not in original8 and i not in added_ships and old.get('killed')!='yes' and 0<old.get('hitpoints',0)<=270 and state.get('killed')=='yes' and hull.is_finite() and hull<=0 and state.get('max_hitpoints')==old.get('max_hitpoints')==270 and state.get('fleet')==old.get('fleet') and b['date']<=state.get('last_damage','0.01.01')<=a['date'] and state.get('last_combat_activity')==state.get('last_damage') and q.block(ash[str(i)],'ship_design_implementation')==q.block(bsh[str(i)],'ship_design_implementation') and sum(i in q.ids(q.block(raw,'ships')) for raw in afl.values())==1
for fid,ids in new_pending_by_fleet.items():
    if ids:
        pending_state_valid &= str(fid) in afl and combat(afl[str(fid)])==[825] and q.scalars(afl[str(fid)]).get('cached_killed_ships',0)-q.scalars(bfl[str(fid)]).get('cached_killed_ships',0)==len(ids)
checks['native_paid_killed_pending_exact_state_loss_counters_and_one_day_cleanup']=bool(pending_state_valid)
if after=='terravore-war1-postmines-recovery3d1':
    failed10=load(after+'-war1-battle-v10-proof.json');failed10_ex=load(after+'-battle-v10-execution.json')
    checks['first_killed_state_original29_single_FAIL_actual1_same_exact_SHA_pair_bound']=failed10['status']=='FAIL' and len(failed10['checks'])==29 and [k for k,v in failed10['checks'].items() if not v]==['all_military_relations_unique_positive_actual_hull'] and failed10_ex['returncode']==1 and failed10_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v10.py')=='9d0a6c99bd775d699bf319b9f8092fb2209fb60971187afe6f7fc63677ba9f1b' and failed10['before_sha256']==b['save_sha256']=='1223198aecbccc78455f299957c3d23a99b19f3afca8e31d4e4f9fe0ef044d97' and failed10['after_sha256']==a['save_sha256']=='fca88c6fcaa19543eea963db7391be657eb595505de324aa71277c8a2932babd' and current_pending_dead=={50332132} and not prior_pending_dead and q.scalars(ash['50332132'])['hitpoints']==-134.6792 and not lost_ships and a['date']=='2268.11.16' and days==3
if after=='terravore-war1-postmines-killed-cleanup1':
    failed11=load(after+'-war1-battle-v11-proof.json');failed11_ex=load(after+'-battle-v11-execution.json')
    checks['first_naval_cache_original30_single_FAIL_actual1_same_SHA_exact_one_dead_cleanup_bound']=failed11['status']=='FAIL' and len(failed11['checks'])==30 and [k for k,v in failed11['checks'].items() if not v]==['actual_naval_size5_per_owned_corvette'] and failed11_ex['returncode']==1 and failed11_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v11.py')=='5599657d68afbf0359e355f6e3737d068f32142ab247e2c7d85b3f85abf01357' and failed11['before_sha256']==b['save_sha256']=='fca88c6fcaa19543eea963db7391be657eb595505de324aa71277c8a2932babd' and failed11['after_sha256']==a['save_sha256']=='7ed26f1798bdda8a525dfa882ebf2e32507c22386d576fa2eecca8a40baac53f' and prior_pending_dead=={50332132} and not current_pending_dead and lost_ships==[50332132] and actual_naval_cache==45 and naval_death_credit==5 and days==1 and a['date']=='2268.11.17'
platform_paid_stage='terravore-war1-two-platforms-paid'
platform_paid=load(platform_paid_stage+'-two-platforms-payment-proof.json');platform_ex=load(platform_paid_stage+'-guard-execution.json')
platform_ids=[201326606,117440537]
pbq,paq=[q.block(q.block(q.block(top['construction'],'queue_mgr'),'queues'),'2') for top in [br,ar]]
owned_platform_refs=[]
for fleets,ships,own in [(bfl,bsh,bo),(afl,ash,ao)]:
    owned_platform_refs.append([sid for fid in own for sid in q.ids(q.block(fleets[str(fid)],'ships')) if q.scalars(q.block(ships[str(sid)],'ship_design_implementation')).get('design')==150995587])
checks['two_platforms1086_payment27_PASS_actual0_exact_source_SHA_bound']=platform_paid['status']=='PASS_TERRAVORE_TWO_NATIVE_DEFENSE_PLATFORMS_PAYMENT_COMPONENT' and len(platform_paid['checks'])==27 and all(v is True for v in platform_paid['checks'].values()) and platform_ex['returncode']==0 and platform_ex['helper_sha256']==h.sha256(run/'priority_terravore_two_platforms_payment_guard.py')=='ebea5b71484512f6ccd6e4e90859857488eb6ade731038a9c59106e19f4e9c5b' and platform_paid['after_sha256']==h.sha256(run/(platform_paid_stage+'.sav'))=='189878161ed9d6d67fad2dcc0e343cec2e894e0c3c827fca500ad1a781ce6cef' and platform_paid['actual_paid_alloys']==1086 and platform_paid['actual_order_ids']==platform_ids and platform_paid['actual_design_id']==150995587
checks['two_platforms_queue2_original_paid_raw_incomplete_exact_1_work_daily_no_built_platform']=q.ids(q.block(pbq,'items'))==q.ids(q.block(paq,'items'))==platform_ids and omit(pbq,{'items'})==omit(paq,{'items'}) and all(omit(bi[str(i)],{'progress'})==omit(ai[str(i)],{'progress'})==omit(original,{'progress'}) for i,original in zip(platform_ids,platform_paid['actual_order_raw'])) and D(str(q.scalars(ai[str(platform_ids[0])])['progress']))==D(str(q.scalars(bi[str(platform_ids[0])])['progress']))+days<60 and q.scalars(bi[str(platform_ids[1])])['progress']==q.scalars(ai[str(platform_ids[1])])['progress']==0 and owned_platform_refs==[[],[]]
if after=='terravore-war1-postplatforms-paid-day1':
    original12=load(after+'-war1-battle-v12-proof.json');original12_ex=load(after+'-battle-v12-execution.json')
    checks['first_platform_day_independent_original30PASS_actual0_same_SHA_bound']=original12['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' and len(original12['checks'])==30 and all(v is True for v in original12['checks'].values()) and original12_ex['returncode']==0 and original12_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v12.py')=='2a40809a741812caabbf28f40532f5105dbf351db048ea904253f45d579b7a5f' and original12['before_sha256']==b['save_sha256'] and original12['after_sha256']==a['save_sha256']=='6f2446146bddb04af4f0acfab225eedc8674b979c9976e6bc9e4b8f09c489104' and days==1 and a['date']=='2268.11.26'
passed = all(checks.values())
details = {i: {'owned_by_player': i in ao, 'owned_by_country1': i in enemy_owned,
               'position': q.scalars(q.block(q.block(afl[str(i)], 'movement_manager'), 'coordinate')),
               'ships': q.ids(q.block(afl[str(i)], 'ships')), 'combat_with': combat(afl[str(i)]),
               'ship_states': {sid: q.scalars(ash[str(sid)]) for sid in q.ids(q.block(afl[str(i)], 'ships'))}}
           for i in set(ao) | {477, 825} if str(i) in afl and (i in am or i in {477, 825})}
proof = {'status': 'PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'], 'date': a['date'],
         'days': days, 'actual_naval_cache':str(actual_naval_cache), 'actual_military_object_naval_size':5*len(current_ships), 'actual_naval_death_cache_credit':str(naval_death_credit), 'actual_pending_destroyed_ship_ids':sorted(current_pending_dead), 'actual_prior_pending_destroyed_ship_ids':sorted(prior_pending_dead), 'actual_alive_military_ship_ids':sorted(set(current_ships)-current_pending_dead), 'actual_confirmed_paid_dead_ids':sorted(cumulative_paid_lost|current_pending_dead), 'pending_death_cleanup_max_days':1 if current_pending_dead else None, 'actual_owned_military': am, 'cumulative_original_lost': sorted(cumulative_original_lost),
         'cumulative_paid_lost': sorted(cumulative_paid_lost), 'all_observed_paid_ship_ids': sorted(observed_paid),
         'actual_base0_ship_state': q.scalars(ash['0']), 'actual_new_paid_ships': added_ships,
         'actual_lost_military_requires_separate_combat_evidence': lost_ships, 'remaining_paid_orders': aids,
         'front_order_progress': [q.scalars(ai[str(i)])['progress'] for i in aids[:2]],
         'actual_fleet_details': details, 'actual_active_owned_combat': active, 'actual_pending': pending,
         'actual_mother_population': a['colonies']['0']['actual_pop_sum'], 'actual_colonization_population': colony['actual_pop_sum'],
         'actual_endpoint_nets': {k: str(v) for k, v in nets.items()}, 'actual_stockpiles': ac['effective_stockpile'],
         'actual_war1': q.scalars(war), 'actual_platform_order_ids':platform_ids, 'actual_platform_order_progress':[q.scalars(ai[str(i)])['progress'] for i in platform_ids], 'actual_built_paid_platform_ids':owned_platform_refs[-1], 'actual_mine_order_ids':mine_ids, 'actual_mine_order_progress':[q.scalars(ai[str(i)])['progress'] for i in mine_ids], 'actual_coherent_appended_reports':coherent_appended_reports, 'actual_cumulative_weapon_aggregate_evidence':weapon_aggregate_evidence, 'actual_rear_upgrade_progress':str(q.scalars(rear_aitem)['progress']), 'actual_missing_enemy825':missing_enemy, 'actual_menace_delta':str(menace_delta), 'native_menace_sources':source_bindings, 'calendar_ready': False, 'short_combat_calendar_ready': passed and not pending,
         'scope': 'Only bounded native war1/paid reinforcement/ongoing colonization/three documented paid mining and two paid platform orders before completion, with exact native naval cache credit from proven removed deaths and killed-pending-object versus alive and removed-loss accounting; any killed pending objects require one next native day and complete cleanup. Remote capture is retained, no annual safety, victory, completed colonization, monthly ledger or full-route claim.'}
out = run / (after + '-war1-battle-v13-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True],
                  'pending': pending, 'killed_pending_cleanup':sorted(current_pending_dead), 'alive_military':len(set(current_ships)-current_pending_dead), 'naval_death_cache_credit':str(naval_death_credit), 'new_paid_ships': added_ships, 'remaining_orders': len(aids),
                  'short_combat_calendar_ready': proof['short_combat_calendar_ready']}), flush=True)
assert passed, 'Original war1 observation FAIL retained; no repeated calendar'
