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
bids, aids = [[i for i in q.ids(q.block(v, 'items')) if i in paid['native_queue_ids']] for v in [bq, aq]]
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
mine_ids=[1006632966,1207959563,905969668]
mbq,maq=[q.block(q.block(q.block(top['construction'],'queue_mgr'),'queues'),'0') for top in [br,ar]]
mine_before_ids,mine_after_ids=[[i for i in q.ids(q.block(raw,'items')) if i in mine_ids] for raw in [mbq,maq]]
mine_completed_before,mine_completed_after=[3-len(ids) for ids in [mine_before_ids,mine_after_ids]]
mother_growth=q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'current_month_growth_data'),'growth_and_size'))
third_start_stage='terravore-colony1085-devour-started'
third_start=load(third_start_stage+'.audit.json');third_start_proof=load(third_start_stage+'-third-start-v2-proof.json');third_start_ex=load(third_start_stage+'-guard-v2-execution.json')
third_source_start=third_start['planets']['1085'];third_sits={i:v for i,v in a['situations'].items() if v.get('type')=='situation_eep_devouring'}
ordinal=lambda date:sum(x*y for x,y in zip(map(int,date.split('.')),[360,30,1]))
third_elapsed=ordinal(a['date'])-ordinal(third_start['date'])
third_expected_progress=(int(a['date'][:4])-2270)*12+int(a['date'][5:7])-2
active_third_valid=360<=third_elapsed<720 and 12<=third_expected_progress<24 and third_sits=={'100663299':{'country':0,'type':'situation_eep_devouring','progress':third_expected_progress,'last_month_progress':0 if third_expected_progress==0 else 1,'approach':'eep_devour_approach','stage':0,'target':{'type':'planet','id':1085,'opener_id':4294967295},'variables':{}}} and not any(v.get('type')=='situation_terravore_consume_planet' for v in a['situations'].values()) and target['variables']==third_source_start['variables']=={'eep_q':12,'eep_old_damage':0,'eep_months':29,'eep_seed_existing':103,'eep_seed_need':-3} and all(target['flags'].get(k)==third_source_start['flags'][k] for k in ['eep_active','eep_native','being_devoured','eep_owned_colony_event','colony_event']) and target['flags'].get('recently_eaten_planet')=={'flag_date':63422160,'flag_days':720-third_elapsed} and not any(k in target['flags'] for k in ['eep_pending','eep_credit_done','eep_return_done','eep_destroy_done','eep_bites_done']) and target['modifiers']==third_source_start['modifiers'] and target['deposits']==b['planets']['1085']['deposits']==[961,962,963,965,967,968,969,970,33554915,16777700] and all(a['deposits'][i]=={'type':'d_lithoid_devastation','deposit_holder':{'type':0,'id':1085}} for i in ['33554915','16777700'])
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
    'EEP_ledger_flags_species_targets_and_exact_active_third_task_held':
        bc['variables'] == ac['variables'] and bc['flags'] == ac['flags']
        and all(ac['variables'][k] == v for k, v in {'eep_c': 37, 'eep_g': 0, 'eep_d': 11, 'eep_made': 0, 'eep_worlds': 2, 'eep_psi': 1}.items())
        and b['species'] == a['species'] and b['event_targets'] == a['event_targets'] and active_third_valid,
    'unique_mother_owned_core_capacity11_no_new_bombardment':
        mother['owner'] == mother['controller'] == 0 and mother['colony'] == 0
        and mother['planet_size'] == 18 and mother['variables']['eep_capacity_value'] == 11
        and sum('eep_core' in v['flags'] for v in a['planets'].values()) == 1
        and mother['modifiers'] == b['planets']['7']['modifiers']
        and mother['bombardment_damage'] == 0 and mother['last_bombardment'] == '2261.07.03',
    'mother_only_paid_completed_mining_levels_changed_other_structure_raw_held':
        all(q.block(br['zones'], i) == q.block(ar['zones'], i) for i in ['0', '2', '61'])
        and all(q.block(br['districts'], i) == q.block(ar['districts'], i) for i in ['1', '2'])
        and omit(q.block(br['districts'],'3'),{'level'})==omit(q.block(ar['districts'],'3'),{'level'})
        and q.scalars(q.block(br['districts'],'3'))['level']==12+mine_completed_before
        and q.scalars(q.block(ar['districts'],'3'))['level']==12+mine_completed_after
        and all(q.block(br['buildings'], str(i)) == q.block(ar['buildings'], str(i))
                for zid in ['0', '2', '61'] for i in q.ids(q.block(q.block(ar['zones'], zid), 'buildings'))),
    'mother_paid_mining_full_jobs_capacity_housing_and_native_population_records':
        all(len([j for j in a['pop_jobs'].values() if j['planet'] == 0 and j['type'] == kind
                 and j['workforce'] == j['max_workforce'] == n]) == 1
            for kind, n in [('fabricator', 200), ('coordinator', 2000), ('logistics_drone', 500),
                            ('telepath_drone', 200), ('calculator_physicist', 300), ('calculator_biologist', 300),
                            ('calculator_engineer', 300), ('mining_drone', 2400+200*mine_completed_after), ('technician_drone', 1200)])
        and a['colonies']['0']['free_housing'] > 0 and a['colonies']['0']['free_amenities'] > 0
        and a['colonies']['0']['stability'] == 80 and a['colonies']['0']['crime'] == 0
        and a['colonies']['0']['total_housing']==12900+300*mine_completed_after
        and a['colonies']['0']['total_housing']-a['colonies']['0']['housing_usage']==a['colonies']['0']['free_housing']
        and a['colonies']['0']['actual_pop_sum']==a['colonies']['0']['employable_pops']==a['colonies']['0']['num_sapient_pops']==mother_growth['month_start_size']+mother_growth['growth']
        and all(a['pop_jobs']['29'][k]==v for k,v in {'bonus_workforce':600+50*mine_completed_after,'workforce_limit':2400+200*mine_completed_after,'automated_workforce':0,'automated_workforce_limit':2399+200*mine_completed_after}.items()),
    'same_native_colony37_1085_completed_owned_founder73_original_hive_structure':
        bc['owned_colonies']==ac['owned_colonies']==[0,37]
        and target['owner']==target['controller']==0 and target['colony']==37
        and target['planet_size']==12 and target['planet_class']=='pc_alpine'
        and target.get('colonize_date')=='2270.02.01' and 0<=target['bombardment_damage']<=b['planets']['1085']['bombardment_damage']<=20 and target['last_bombardment']=='0.01.01'
        and 'colonizing_species' not in colony and 100<=colony['actual_pop_sum']<=500
        and all(a['pop_groups'][str(i)]['key']['species']==73 for i in colony['pop_groups'])
        and colony['actual_pop_sum']==colony['employable_pops']==colony['num_sapient_pops']
        and q.scalars(q.block(ar['districts'],'68'))=={'type':'district_hive','level':1}
        and q.ids(q.block(q.block(ar['districts'],'68'),'zones'))==[16777291,4294967295,4294967295]
        and q.scalars(q.block(ar['zones'],'16777291'))=={'type':'zone_default'}
        and q.ids(q.block(q.block(ar['zones'],'16777291'),'buildings'))==[33554455]
        and q.scalars(q.block(ar['buildings'],'33554455'))=={'type':'building_hive_capital','position':0}
        and all(a['pop_jobs'][i]['planet']==37 and a['pop_jobs'][i]['type']==kind and a['pop_jobs'][i]['max_workforce']==cap and a['pop_jobs'][i]['automated_workforce']==0 and 0<=a['pop_jobs'][i]['workforce']<=cap for i,kind,cap in [('812','coordinator',200),('813','patrol_drone',100),('814','logistics_drone',200)]),
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
    'unfiltered_error_exact_documented_native2814_baseline_no_unknown_increment':
        (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()
        and (run/(after+'-error-after.log')).read_bytes()==(run/'terravore-war1-idle11-step1-error-after.log').read_bytes()
        and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
        and (run/(after+'-error-after.log')).stat().st_size==2814
        and (after=='terravore-war1-idle11-step1' or (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()),
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
end_stage='terravore-war1-bounded18-step1'
end_sha='f18b14c90dec452c4a5d36b1f6b6de98c71ff88e60a3b80f1cc3c97554dbcb98'
if after==end_stage:
    old_stage='terravore-war1-defense-sixdays4'
    old9=load(old_stage+'-war1-battle-v9-proof.json');old9_ex=load(old_stage+'-battle-v9-execution.json')
    oldaudit,oldfields,oldtop=read(old_stage)
    old_messages=[v for k,v,o in oldfields if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('notification')==210]
    final_messages=[v for k,v,o in af if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('notification')==211]
    report_valid=len(old_messages)==len(final_messages)==1
    final_message=final_messages[0] if final_messages else ''
    final_stats=q.block(final_message,'combat_stats')
    final_own=list(anonymous_objects(q.block(final_stats,'fleets')))
    final_enemy=list(anonymous_objects(q.block(final_stats,'enemy')))
    old_enemy=list(anonymous_objects(q.block(q.block(old_messages[0],'combat_stats'),'enemy'))) if old_messages else []
    old_enemy825=[v for v in old_enemy if q.scalars(v).get('fleet')==825 and q.scalars(v).get('country')==1]
    previous_enemy=q.block(q.block(q.block(bfl['825'],'fleet_stats'),'combat_stats'),'fleet')
    report_valid &= q.scalars(final_message)=={'type':'COMBAT_STATS','receiver':0,'end':'2269.01.29','date':'2268.12.14','notification':211,'message_type':'combat_stats'} and q.scalars(final_stats)=={'date':'2268.06.14','reason':'no_more_enemies'}
    report_valid &= [q.scalars(v).get('fleet') for v in final_own]==[0,67109603,33555259] and all(q.scalars(v).get('country')==0 for v in final_own)
    for row,fid,count,lost in zip(final_own,[0,67109603,33555259],[[1],[2],[2]],[[0],[1],[1]]):
        previous=q.block(q.block(q.block(bfl[str(fid)],'fleet_stats'),'combat_stats'),'fleet')
        report_valid &= q.ids(q.block(row,'ship_size_count'))==q.ids(q.block(previous,'ship_size_count'))==count and q.ids(q.block(row,'ship_size_count_lost'))==q.ids(q.block(previous,'ship_size_count_lost'))==lost
    report_valid &= len(final_enemy)==len(old_enemy825)==1
    if final_enemy and old_enemy825:
        row=final_enemy[0];oldrow=old_enemy825[0]
        report_valid &= q.scalars(row).get('fleet')==825 and q.scalars(row).get('country')==1 and q.ids(q.block(row,'ship_size_count'))==q.ids(q.block(previous_enemy,'ship_size_count'))==[2,9,4,1] and q.ids(q.block(row,'ship_size_count_lost'))==[0,3,0,0] and q.ids(q.block(oldrow,'ship_size_count_lost'))==[0,1,0,0] and q.ids(q.block(previous_enemy,'ship_size_count_lost'))==[x+y for x,y in zip(q.ids(q.block(row,'ship_size_count_lost')),q.ids(q.block(oldrow,'ship_size_count_lost')))]==[0,4,0,0]
    report_valid &= old9['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' and len(old9['checks'])==29 and all(v is True for v in old9['checks'].values()) and old9_ex['returncode']==0 and old9_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v9.py')=='a39f884b439203a964353ed00c8111f732aa1fcd34ab7b71f9bd0be3d52a0717' and old9['after_sha256']==oldaudit['save_sha256']==h.sha256(run/(old_stage+'.sav'))=='e9419175617ac77fcc9335655ab5a4951746e21053b2e75dc0f33d7c1f214cd6'
    failed13=load(after+'-war1-battle-v13-proof.json');failed13_ex=load(after+'-battle-v13-execution.json')
    checks['first_battle_end_original32_single_FAIL_actual1_same_exact_SHA_pair_bound']=failed13['status']=='FAIL' and len(failed13['checks'])==32 and [k for k,v in failed13['checks'].items() if not v]==['native_enemy825_loss_real_objects_and_15_menace_progression_source_bound'] and failed13_ex['returncode']==1 and failed13_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v13.py')=='8c627b5ffe51d8531cef1c9e625c19bd47c8946879eb1c7c67bafb4ce9798dcb' and failed13['before_sha256']==b['save_sha256']=='577035aa79b9e5430e69216bcbddfaf1a87f848c5a2d50b649f9f2035ee16f06' and failed13['after_sha256']==a['save_sha256']==end_sha and days==1 and a['date']=='2268.12.15' and loss_stats(bfl['825'])==('2268.06.14',4) and loss_stats(afl['825'])==('0.01.01',0)
    end_evidence={'enemy_ship_ids':sorted(before_enemy),'final_message_raw':final_message,'old210_message_raw':old_messages[0] if old_messages else '', 'old210_save_sha256':oldaudit['save_sha256'],'live_enemy_losses':[0,4,0,0],'final_report_enemy_losses':[0,3,0,0],'old210_enemy_losses':[0,1,0,0],'return_date':'2270.07.07','scope':'Emergency FTL retreat; no new enemy death or menace, war1 remains active.'}
else:
    anchor=load(end_stage+'-war1-battle-v14-proof.json');anchor_ex=load(end_stage+'-battle-v14-execution.json')
    report_valid=anchor['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(anchor['checks'])==34 and all(v is True for v in anchor['checks'].values()) and anchor_ex['returncode']==0 and anchor_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v14.py')=='b3607852c6ab934eee94d0d0988cae90e3dbef4ffbfa37c92da94cd63e70ea13' and anchor['after_sha256']==h.sha256(run/(end_stage+'.sav'))==end_sha
    end_evidence=anchor['native_finished_battle_evidence']
checks['native_final_report211_old210_exact_counter_split_and_immutable_end_anchor']=bool(report_valid)
checks['native_enemy825_actually_returned_same_positive12_no_new_kills_or_menace']=before_enemy==after_enemy==set(end_evidence['enemy_ship_ids']) and len(after_enemy)==12 and not active and not combat(afl['825']) and 825 in enemy_owned and 'return_date' not in q.scalars(afl['825']) and q.scalars(q.block(afl['825'],'properties')).get('mia') is None and a['date']>='2270.07.08' and str(q.scalars(q.block(q.block(afl['825'],'movement_manager'),'coordinate')).get('origin')) in objects(ar['galactic_object']) and all(q.scalars(ash[str(i)]).get('fleet')==825 and q.scalars(ash[str(i)]).get('killed')!='yes' and 0<q.scalars(ash[str(i)])['hitpoints']<=q.scalars(ash[str(i)])['max_hitpoints'] for i in after_enemy) and not lost_ships and not current_pending_dead and menace_delta==0 and native_menace_source_bound
if after=='terravore-war1-defense-three-days2':
    old=load(after+'-war1-battle-v5-proof.json'); oldex=load(after+'-battle-v5-execution.json')
    checks['first_menace_gain_original24_single_FAIL_exact_real_enemy_loss_bound'] = old['status']=='FAIL' and len(old['checks'])==24 and [k for k,v in old['checks'].items() if not v]==['native_finished_PSIONIC1_full_breach_level1_menace90_held'] and oldex['returncode']==1 and oldex['helper_sha256']=='47d2f746067431ed6c51f14f8301ed6f68cd4d9f79d86dc2d513f28f653c448e' and old['before_sha256']==b['save_sha256'] and old['after_sha256']==a['save_sha256'] and missing_enemy==[16779066] and menace_delta==15 and bc['effective_stockpile']['menace']==90 and ac['effective_stockpile']['menace']==105
rear_paid_stage='terravore-war1-rear-starport-paid'
rear_paid=load(rear_paid_stage+'-rear-starport-payment-proof.json')
rear_execution=load(rear_paid_stage+'-guard-execution.json')
rear_bbase,rear_abase=[q.block(q.block(t['starbase_mgr'],'starbases'),'153') for t in [br,ar]]
rear_bqueue,rear_aqueue=[q.block(q.block(q.block(t['construction'],'queue_mgr'),'queues'),'2278') for t in [br,ar]]
rear_bitem,rear_aitem=[q.block(items_raw,'234881044') for items_raw in [q.block(q.block(br['construction'],'item_mgr'),'items'),q.block(q.block(ar['construction'],'item_mgr'),'items')]]
rear_before_done=q.scalars(rear_bbase).get('level')=='starbase_level_starport'
rear_after_done=q.scalars(rear_abase).get('level')=='starbase_level_starport'
rear_before_work=D(360) if rear_before_done else D(str(q.scalars(rear_bitem)['progress']))
rear_after_work=D(360) if rear_after_done else D(str(q.scalars(rear_aitem)['progress']))
checks['rear125_payment20_PASS_actual0_exact_native_order_source_bound']=rear_paid['status']=='PASS_TERRAVORE_NATIVE_REAR_STARPORT_PAYMENT_COMPONENT' and len(rear_paid['checks'])==20 and all(v is True for v in rear_paid['checks'].values()) and rear_execution['returncode']==0 and rear_execution['helper_sha256']=='a8a52e34638492a7fe0c1a317c54cd9d5238a1192c2d2abf119fe785ec5aa8cf' and h.sha256(run/Path(rear_execution['command'][1]).name)==rear_execution['helper_sha256'] and rear_paid['after_sha256']==h.sha256(run/(rear_paid_stage+'.sav'))=='2a3381a6d47c8105714fe2379c6d0a859f35ae5f90f74ce1e0ec3218a3aebee3' and rear_paid['paid_alloys']==125 and rear_paid['rear_order_id']==234881044
rear_complete_stage='terravore-war1-rear-starport-complete'
rear_source_bindings={'native-rear-completion-00_starbase_levels.txt':'495d5c5d13b80502c8cd121cd8817dc76e1690e8bd584a6a1d91845af006f94d','native-rear-completion-00_starbases.txt':'bf3719e954596118f046f49f4b672b0e1f88d11c192bd179170a651d12c1f1ce'}
rear_design=q.block(ar['ship_design'],'201328266')
if after==rear_complete_stage:
    rear_end_evidence={'stage':after,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'design_raw':rear_design,'station':67109591,'fleet':804,'system':97,'paid_order':234881044,'source_bindings':rear_source_bindings}
    rear_anchor_valid=a['save_sha256']=='3f0eb62159dd9bf0c0bfb519baa349fb6f219d7c1f3a41bb0a9fddf230e2d26e'
else:
    rear_anchor=load(rear_complete_stage+'-war1-battle-v19-proof.json');rear_anchor_ex=load(rear_complete_stage+'-battle-v19-execution.json')
    rear_end_evidence=rear_anchor['native_rear_completion_evidence']
    rear_anchor_valid=rear_anchor['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(rear_anchor['checks'])==40 and all(v is True for v in rear_anchor['checks'].values()) and rear_anchor_ex['returncode']==0 and rear_anchor_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v19.py')=='b057f107d87a752030f58c0157e85ab2e3f3d7739f996bc57aec8e1e06744f90' and rear_anchor_ex['wrapper_sha256']=='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3' and rear_anchor['after_sha256']==h.sha256(run/(rear_complete_stage+'.sav'))=='3f0eb62159dd9bf0c0bfb519baa349fb6f219d7c1f3a41bb0a9fddf230e2d26e'
rear_queue_refs={sid for key,raw,obj in q.fields(q.block(q.block(ar['construction'],'queue_mgr'),'queues')) if obj for sid in q.ids(q.block(raw,'items'))}
rear_item_records={key:(raw,obj) for key,raw,obj in q.fields(q.block(q.block(ar['construction'],'item_mgr'),'items'))}
rear_same_slot=[int(k) for k in rear_item_records if k.isdigit() and int(k)%16777216==234881044%16777216]
rear_old_record=rear_item_records.get('234881044')
rear_removed_valid=234881044 not in rear_queue_refs and ((rear_old_record==('none',False) and rear_same_slot==[234881044]) or (rear_old_record is None and len(rear_same_slot)==1 and rear_same_slot[0]>234881044 and (rear_same_slot[0]-234881044)%16777216==0))
rear_state_valid=True
for base_raw,queue_raw,item_raw,done,own,fleets,ships in [(rear_bbase,rear_bqueue,rear_bitem,rear_before_done,bo,bfl,bsh),(rear_abase,rear_aqueue,rear_aitem,rear_after_done,ao,afl,ash)]:
    level='starbase_level_starport' if done else 'starbase_level_outpost'
    rear_state_valid=rear_state_valid and q.scalars(base_raw)=={'level':level,'build_queue':2278,'shipyard_build_queue':4294967295,'station':67109591} and q.ids(q.block(queue_raw,'items'))==([] if done else [234881044])
    if not done:
        rear_state_valid=rear_state_valid and omit(item_raw,{'progress'})==omit(rear_paid['rear_order_raw'],{'progress'}) and 0<=D(str(q.scalars(item_raw)['progress']))<360
    state=q.scalars(ships['67109591']);expected=(18300,5125,4320) if done else (9150,3125,1440)
    rear_state_valid=rear_state_valid and 804 in own and q.ids(q.block(fleets['804'],'ships'))==[67109591] and q.scalars(fleets['804']).get('ship_class')=='shipclass_starbase' and q.scalars(q.block(q.block(fleets['804'],'movement_manager'),'coordinate')).get('origin')==97 and state.get('fleet')==804 and state.get('killed')!='yes' and state.get('construction_date')=='2264.07.24' and tokvalues(q.block(ships['67109591'],'ship_design_implementation'))==tokvalues(q.block(base_raw,'ship_design_implementation'))==['design','=','201328266','upgrade','=','4294967295','growth_stage','=','0'] and q.scalars(q.block(base_raw,'ship_design_implementation'))=={'design':201328266,'upgrade':4294967295,'growth_stage':0} and state.get('upgrade_progress')==0 and tuple(state.get(k) for k in ['max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])==expected and state.get('hitpoints',0)>0 and all(D(str(state.get(k,0))).is_finite() and 0<=D(str(state.get(k,0)))<=D(str(state[maxk])) for k,maxk in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
checks['rear153_paid_upgrade_exact_serial_work_same_station_and_order_completion']=bool(rear_state_valid) and rear_before_done<=rear_after_done and omit(rear_bbase,{'level'})==omit(rear_abase,{'level'}) and omit(rear_bqueue,{'items'})==omit(rear_aqueue,{'items'}) and rear_after_work==min(D(360),rear_before_work+D('1.5')*days) and (not rear_after_done or rear_removed_valid)
checks['rear153_native_completed_starport_design_stats_owned_system97_and_fixed_anchor']=bool(rear_anchor_valid) and rear_after_done and rear_design==rear_end_evidence['design_raw'] and 'ship_size="starbase_starport"' in rear_design and 'template="STARPORT_STARBASE_SECTION"' in rear_design and (rear_before_done or all(q.scalars(ash['67109591'])[k]==q.scalars(ash['67109591'])[maxk] for k,maxk in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]))
checks['native_rear_starport_level_and_ship_size_source_raw_exact_SHA_bound']=all(h.sha256(run/name)==sha for name,sha in rear_source_bindings.items())
if after==rear_complete_stage:
    checks['first_rear_completion_priorV17_36PASS_actual0_exact_pair_one_day358point5_to360']=before=='terravore-war1-idle7-step2' and pre['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(pre['checks'])==36 and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v17.py')=='d24a25a4b3e1a8cc39260edd5c45d259d914b0af2011cb053be9456eeac1343f' and b['save_sha256']=='cacc0aa82564e7f95eddacef3e766d5fb07a3b590346f2c31de9432d3725d1ab' and b['date']=='2269.04.12' and a['date']=='2269.04.13' and days==1 and not rear_before_done and rear_after_done and rear_before_work==D('358.5') and rear_after_work==360 and rear_old_record==('none',False)
if after==rear_complete_stage:
    failed18=load(after+'-war1-battle-v18-proof.json');failed18_ex=load(after+'-battle-v18-execution.json')
    checks['first_rear_implementation_whitespace_original39_single_FAIL_actual1_same_exact_SHA_pair']=failed18['status']=='FAIL' and len(failed18['checks'])==39 and [k for k,v in failed18['checks'].items() if v is not True]==['rear153_paid_upgrade_exact_serial_work_same_station_and_order_completion'] and failed18_ex['returncode']==1 and failed18_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v18.py')=='c9eb6aa204d63ea71c5f40315dee8f697622901253c0cc283b7fbe58f24d4c8b' and failed18['before_sha256']==b['save_sha256']=='cacc0aa82564e7f95eddacef3e766d5fb07a3b590346f2c31de9432d3725d1ab' and failed18['after_sha256']==a['save_sha256']=='3f0eb62159dd9bf0c0bfb519baa349fb6f219d7c1f3a41bb0a9fddf230e2d26e' and days==1 and q.block(bsh['67109591'],'ship_design_implementation')!=q.block(rear_bbase,'ship_design_implementation') and q.block(ash['67109591'],'ship_design_implementation')!=q.block(rear_abase,'ship_design_implementation') and tokvalues(q.block(bsh['67109591'],'ship_design_implementation'))==tokvalues(q.block(rear_bbase,'ship_design_implementation'))==tokvalues(q.block(ash['67109591'],'ship_design_implementation'))==tokvalues(q.block(rear_abase,'ship_design_implementation'))==['design','=','201328266','upgrade','=','4294967295','growth_stage','=','0']
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
mine_expected_ids=list(mine_before_ids)
mine_expected_progress=D(str(q.scalars(bi[str(mine_expected_ids[0])])['progress'])) if mine_expected_ids else D(0)
for day in range(days):
    if mine_expected_ids:
        mine_expected_progress+=D('1.4')
        if mine_expected_progress>=240:
            mine_expected_ids.pop(0);mine_expected_progress=D(0)
mine_handle_evidence=[]
item_table=q.block(q.block(ar['construction'],'item_mgr'),'items')
item_records={k for k,v,o in q.fields(item_table)}
all_queue_references={i for k,v,o in q.fields(q.block(q.block(ar['construction'],'queue_mgr'),'queues')) if o for i in q.ids(q.block(v,'items'))}
for oldid in mine_ids[:mine_completed_after]:
    replacements=[int(k) for k in item_records if k.isdigit() and int(k)!=oldid and (int(k)&0xffffff)==(oldid&0xffffff)]
    valid=(q.scalars(item_table).get(str(oldid))=='none' or (str(oldid) not in item_records and replacements and all(i>oldid for i in replacements))) and oldid not in all_queue_references
    mine_handle_evidence.append({'original_handle':oldid,'old_scalar_none':q.scalars(item_table).get(str(oldid))=='none','same_slot_handles':replacements,'old_in_any_queue':oldid in all_queue_references,'valid':bool(valid)})
checks['three_paid_mines_exact_serial_1point4_daily_discarded_overflow_and_completed_handles']=mine_before_ids==mine_ids[mine_completed_before:] and mine_after_ids==mine_ids[mine_completed_after:]==mine_expected_ids and 0<=mine_completed_before<=mine_completed_after<=3 and omit(mbq,{'items'})==omit(maq,{'items'}) and all(omit(rawitems[str(i)],{'progress'})==omit(mine_paid['actual_order_raw'][mine_ids.index(i)],{'progress'}) and 0<=D(str(q.scalars(rawitems[str(i)])['progress']))<240 for ids,rawitems in [(mine_before_ids,bi),(mine_after_ids,ai)] for i in ids) and all(q.scalars(rawitems[str(i)])['progress']==0 for ids,rawitems in [(mine_before_ids,bi),(mine_after_ids,ai)] for i in ids[1:]) and (not mine_after_ids or D(str(q.scalars(ai[str(mine_after_ids[0])])['progress']))==mine_expected_progress) and all(v['valid'] for v in mine_handle_evidence)
mine_first_stage='terravore-war1-first-mine-complete'
if after==mine_first_stage:
    mine_completion_evidence={'date':a['date'],'save_sha256':a['save_sha256'],'before_sha256':b['save_sha256'],'prior_progress':str(D(str(q.scalars(bi['1006632966'])['progress']))),'first_completed_id':1006632966,'remaining_ids':mine_after_ids,'remaining_progress':[q.scalars(ai[str(i)])['progress'] for i in mine_after_ids],'mining_job':a['pop_jobs']['29'],'housing':{k:a['colonies']['0'][k] for k in ['total_housing','housing_usage','free_housing','civilian','actual_pop_sum','employable_pops','num_sapient_pops']},'last_month_growth':q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))}
    mine_anchor_valid=before=='terravore-war1-idle9-step1' and days==1 and a['date']=='2269.05.01' and b['save_sha256']=='444fbef7b8efe8157c59d2be7ede30e6b9f33c229d11166a8beb32b4a9e1fee0' and a['save_sha256']=='f27135be8da8d895a474d4db9d5be4252db370f87e79d305f275d22613c1c62b' and pre['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(pre['checks'])==38 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v19.py')=='b057f107d87a752030f58c0157e85ab2e3f3d7739f996bc57aec8e1e06744f90' and mine_completed_before==0 and mine_completed_after==1 and mine_completion_evidence['prior_progress']=='239.4' and mine_after_ids==[1207959563,905969668] and mine_completion_evidence['remaining_progress']==[0,0] and mine_completion_evidence['last_month_growth']=={'month_start_size':10762,'growth':7} and a['colonies']['0']['actual_pop_sum']==10769 and a['colonies']['0']['housing_usage']==10762 and a['colonies']['0']['civilian']==b['colonies']['0']['civilian']-200==2910
else:
    mine_anchor=load(mine_first_stage+'-war1-battle-v21-proof.json');mine_anchor_ex=load(mine_first_stage+'-battle-v21-execution.json')
    mine_completion_evidence=mine_anchor['native_mine_completion_evidence']
    mine_anchor_valid=mine_anchor['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(mine_anchor['checks'])==40 and all(v is True for v in mine_anchor['checks'].values()) and mine_anchor_ex['returncode']==0 and mine_anchor_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v21.py') and mine_anchor_ex['wrapper_sha256']=='7058a037c55931c3d69f6139eff7096bd7ff15b3715e5f081a26b73b5c35a7d3' and mine_anchor['after_sha256']==h.sha256(run/(mine_first_stage+'.sav'))=='f27135be8da8d895a474d4db9d5be4252db370f87e79d305f275d22613c1c62b'
checks['native_first_paid_mine_completion_fixed_SAV_prior_source_growth_cache_and_order_anchor']=bool(mine_anchor_valid)
if after==mine_first_stage:
    failed20=load(after+'-war1-battle-v20-proof.json');failed20_ex=load(after+'-battle-v20-execution.json')
    checks['first_mine_original_V20_39_single_refresh_flag_FAIL_actual1_same_SAV_bound']=failed20['status']=='FAIL' and len(failed20['checks'])==39 and [k for k,v in failed20['checks'].items() if v is not True]==['actual_paid_platforms_same_design_full_newborn_HP4740_armor1125_shield1440_owned_base0_references'] and failed20_ex['returncode']==1 and failed20_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v20.py')=='8e15a5df446dad53d98080c23ddacec3ca9632ea09005f91d72037ac523d25ec' and failed20['before_sha256']==b['save_sha256'] and failed20['after_sha256']==a['save_sha256'] and q.scalars(base_b).get('update_flag') is None and q.scalars(base_a).get('update_flag')==2048 and omit(base_b,{'update_flag'})==omit(base_a,{'update_flag'})

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
platform_before_ids=q.ids(q.block(pbq,'items'));platform_after_ids=q.ids(q.block(paq,'items'))
platform_completed_before=2-len(platform_before_ids);platform_completed_after=2-len(platform_after_ids)
platform_original=dict(zip(platform_ids,platform_paid['actual_order_raw']))
def platform_work(order_ids,raw_items):
    return D(60)*(2-len(order_ids))+sum((D(str(q.scalars(raw_items[str(i)])['progress'])) for i in order_ids),D(0))
platform_before_work=platform_work(platform_before_ids,bi);platform_after_work=platform_work(platform_after_ids,ai)
new_platforms=sorted(set(owned_platform_refs[1])-set(owned_platform_refs[0]))
all_native_queue_refs={sid for key,raw,obj in q.fields(q.block(q.block(ar['construction'],'queue_mgr'),'queues')) if obj for sid in q.ids(q.block(raw,'items'))}
platform_item_fields=list(q.fields(q.block(q.block(ar['construction'],'item_mgr'),'items')))
platform_item_records={key:(raw,obj) for key,raw,obj in platform_item_fields}
platform_completed_handle_evidence=[]
def completed_platform_handle_valid(sid):
    key=str(sid);same_slot=[int(k) for k in platform_item_records if k.isdigit() and int(k)%16777216==sid%16777216]
    record=platform_item_records.get(key)
    valid=sid not in all_native_queue_refs and len(platform_item_records)==len(platform_item_fields)
    if record is not None:
        valid=valid and record==('none',False) and same_slot==[sid]
    else:
        valid=valid and len(same_slot)==1 and same_slot[0]>sid and (same_slot[0]-sid)%16777216==0
    platform_completed_handle_evidence.append({'original_handle':sid,'old_scalar_none':record==('none',False),'old_absent':record is None,'same_slot_handles':same_slot,'old_in_any_queue':sid in all_native_queue_refs,'valid':bool(valid)})
    return bool(valid)
checks['two_platforms_paid_queue2_serial_exact_work_conservation_and_actual_instance_count']=platform_before_ids==platform_ids[platform_completed_before:] and platform_after_ids==platform_ids[platform_completed_after:] and 0<=platform_completed_before<=platform_completed_after<=2 and omit(pbq,{'items'})==omit(paq,{'items'}) and platform_after_work-platform_before_work==min(D(days),D(120)-platform_before_work) and all(omit(raw_items[str(i)],{'progress'})==omit(platform_original[i],{'progress'}) and 0<=D(str(q.scalars(raw_items[str(i)])['progress']))<60 for ids,raw_items in [(platform_before_ids,bi),(platform_after_ids,ai)] for i in ids) and all(q.scalars(raw_items[str(i)])['progress']==0 for ids,raw_items in [(platform_before_ids,bi),(platform_after_ids,ai)] for i in ids[1:]) and len(owned_platform_refs[0])==len(set(owned_platform_refs[0]))==platform_completed_before and len(owned_platform_refs[1])==len(set(owned_platform_refs[1]))==platform_completed_after and set(owned_platform_refs[0])<=set(owned_platform_refs[1]) and len(new_platforms)==platform_completed_after-platform_completed_before and all(completed_platform_handle_valid(i) for i in platform_ids[:platform_completed_after])
platform_actual=[];platform_valid=True
for fleets,ships,own,refs in [(bfl,bsh,bo,owned_platform_refs[0]),(afl,ash,ao,owned_platform_refs[1])]:
    global_refs={int(sid) for sid,raw in ships.items() if q.scalars(q.block(raw,'ship_design_implementation')).get('design')==150995587}
    platform_valid=platform_valid and global_refs==set(refs) and 0 in own and q.scalars(fleets['0']).get('ship_class')=='shipclass_starbase' and set(q.ids(q.block(fleets['0'],'ships')))=={0}|set(refs)
    for sid in refs:
        raw=ships[str(sid)];state=q.scalars(raw)
        platform_valid=platform_valid and state.get('fleet')==0 and ('original_owner' not in state or state['original_owner']==0) and state.get('killed')!='yes' and q.scalars(q.block(raw,'ship_design_implementation'))=={'design':150995587,'upgrade':4294967295,'growth_stage':0} and state.get('upgrade_progress')==0 and state.get('max_hitpoints')==4740 and state.get('max_armor_hitpoints')==1125 and state.get('max_shield_hitpoints')==1440 and all(D(str(state.get(key,0))).is_finite() and 0<=D(str(state.get(key,0)))<=D(str(state[maxkey])) for key,maxkey in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')]) and state.get('hitpoints',0)>0 and '2269.01.25'<=state.get('construction_date','')<=a['date']
        if ships is ash:
            platform_actual.append({'id':sid,'state':state,'implementation':q.scalars(q.block(raw,'ship_design_implementation'))})
            if sid in new_platforms:
                platform_valid=platform_valid and b['date']<state['construction_date']<=a['date'] and all(state[key]==state[maxkey] for key,maxkey in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
            else:
                platform_valid=platform_valid and q.scalars(bsh[str(sid)])['construction_date']==state['construction_date']
checks['actual_paid_platforms_same_design_full_newborn_HP4740_armor1125_shield1440_owned_base0_references']=bool(platform_valid) and omit(base_b,{'update_flag'})==omit(base_a,{'update_flag'}) and all(q.scalars(raw).get('update_flag') in [None,2048] for raw in [base_b,base_a]) and q.scalars(base_a)['station']==0 and q.scalars(base_a)['build_queue']==2 and q.block(br['ship_design'],'150995587')==q.block(ar['ship_design'],'150995587') and 'ship_size="military_station_small"' in q.block(ar['ship_design'],'150995587')
platform_sources={'native-platform-completion-00_ascension_perks.txt':'0992582948a3ca199b30ab646720091e0207e2e58b688171d9cc501f266a720c','native-platform-completion-00_unyielding.txt':'b1a5e8da4514622a0302940953c0e63b66dff3af266e956cd00aa664552367e6'}
checks['native_platform_completed_hull_source_raw_AP_and_unyielding_exact_SHA_bound']=all(h.sha256(run/name)==sha for name,sha in platform_sources.items())
if after=='terravore-war1-first-platform-complete':
    checks['first_platform_completion_prior_V15_34PASS_actual0_exact_pair_single_day_and_first_paid_instance']=before=='terravore-war1-idle2-step2' and pre['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(pre['checks'])==34 and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v15.py')=='78e8ff0769a635473fd728a7b71f40ffe0dbf2cbe2ebc591db5b6ffc65696f54' and b['save_sha256']=='e9ca67abcf938292c890c99ca9b4068a864062d63a93382cb8c38aed72a539ae' and a['save_sha256']=='4c69d97e62a483af655639b43a34e8e1aed7fa2f267c9652d65e9db0c003d09e' and b['date']=='2269.01.24' and a['date']=='2269.01.25' and days==1 and platform_before_work==59 and platform_after_work==60 and platform_before_ids==platform_ids and platform_after_ids==[117440537] and new_platforms==[83887310]
if after=='terravore-war1-idle3-step1':
    failed16=load(after+'-war1-battle-v16-proof.json');failed16_ex=load(after+'-battle-v16-execution.json');failed9_ex=load('terravore-war1-idle3-driver-execution.json')
    replacement_raw=ai.get('218103822','')
    checks['first_completed_order_generation_reuse_original36_single_FAIL_actual1_same_exact_pair_bound']=failed16['status']=='FAIL' and len(failed16['checks'])==36 and [k for k,v in failed16['checks'].items() if v is not True]==['two_platforms_paid_queue2_serial_exact_work_conservation_and_actual_instance_count'] and failed16_ex['returncode']==failed9_ex['returncode']==1 and failed16_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v16.py')=='8bb468621217f56671d43594d5646f573045e0140a471a7e9cb086ab269c2396' and failed9_ex['helper_sha256']==h.sha256(run/'priority_terravore_idle_war_driver_v9.py')=='e56d195930019641cb522679a196044d429814559ca3c60c65d1ff84ece3647f' and failed16['before_sha256']==b['save_sha256']=='4c69d97e62a483af655639b43a34e8e1aed7fa2f267c9652d65e9db0c003d09e' and failed16['after_sha256']==a['save_sha256']=='0f35bdd5d44a0ed7bde87819d3b34b02010799120ffa92375ca21f0731b16f42' and days==14 and b['date']=='2269.01.25' and a['date']=='2269.02.09' and q.scalars(q.block(q.block(br['construction'],'item_mgr'),'items')).get('201326606')=='none' and '201326606' not in platform_item_records and platform_completed_handle_evidence==[{'original_handle':201326606,'old_scalar_none':False,'old_absent':True,'same_slot_handles':[218103822],'old_in_any_queue':False,'valid':True}] and q.scalars(replacement_raw).get('queue')==50 and q.scalars(replacement_raw).get('paying_country')==1 and q.scalars(replacement_raw).get('progress')==7 and q.scalars(replacement_raw).get('progress_needed')==90 and q.scalars(q.block(replacement_raw,'buildable_army')).get('army_type')=='assault_army'
if after=='terravore-war1-postplatforms-paid-day1':
    original12=load(after+'-war1-battle-v12-proof.json');original12_ex=load(after+'-battle-v12-execution.json')
    checks['first_platform_day_independent_original30PASS_actual0_same_SHA_bound']=original12['status']=='PASS_TERRAVORE_NATIVE_WAR1_BATTLE_OBSERVATION_COMPONENT' and len(original12['checks'])==30 and all(v is True for v in original12['checks'].values()) and original12_ex['returncode']==0 and original12_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v12.py')=='2a40809a741812caabbf28f40532f5105dbf351db048ea904253f45d579b7a5f' and original12['before_sha256']==b['save_sha256'] and original12['after_sha256']==a['save_sha256']=='6f2446146bddb04af4f0acfab225eedc8674b979c9976e6bc9e4b8f09c489104' and days==1 and a['date']=='2268.11.26'
owned_ship_states=[q.scalars(ash[str(sid)]) for fid in ao for sid in q.ids(q.block(afl[str(fid)],'ships'))]
checks['all_owned_ship_activity_damage_and_native_reports_no_new_battle_after_end_anchor']=all(v.get('last_combat_activity','0.01.01')<='2268.12.14' and v.get('last_damage','0.01.01')<='2268.12.14' for v in owned_ship_states) and all(q.scalars(v).get('date','0.01.01')<='2268.12.14' for k,v,o in af if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0)
if after==end_stage:
    original14=load(after+'-war1-battle-v14-proof.json');original14_ex=load(after+'-battle-v14-execution.json')
    checks['first_idle_strict_activity_independent_original34PASS_actual0_same_SHA_bound']=original14['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(original14['checks'])==34 and all(v is True for v in original14['checks'].values()) and original14_ex['returncode']==0 and original14_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v14.py')=='b3607852c6ab934eee94d0d0988cae90e3dbef4ffbfa37c92da94cd63e70ea13' and original14['before_sha256']==b['save_sha256'] and original14['after_sha256']==a['save_sha256']==end_sha
leader_control=Path('eat_everything_origin/docs/evidence/priority-terravore-progress-2026-10-09/native-leader-trait-error-control')
control_proof_path=leader_control/'leader13-control-fleet-error-reproduction-proof.json'
control_proof=json.loads(control_proof_path.read_text('utf-8'));control_ex=json.loads((leader_control/'leader13-control-fleet-error-guard-execution.json').read_text('utf-8'))
leader_sources={entry['path']:entry['sha256'] for entry in control_proof['native_sources']}
for path,sha in leader_sources.items():
    source=Path(path);target=run/('native-leader1-'+source.name)
    assert h.sha256(source)==sha
    if target.exists():assert h.sha256(target)==sha
    else:shutil.copyfile(source,target)
checks['native_leader_trait_sources_prior_no_mod14_control_and_unchanged_package_bound']=h.sha256(control_proof_path)=='696015f50a82abc3ce82a78eada44362d376329286067e744dc25bdb4ed43dbd' and control_proof['status']=='PASS_SCOPED_NO_MOD_LEADER13_ERROR_REPRODUCTION' and len(control_proof['checks'])==14 and all(v is True for v in control_proof['checks'].values()) and control_ex['returncode']==0 and control_ex['helper_sha256']==h.sha256(leader_control/'priority_leader13_fleet_effect_error_guard.py')=='a19ca68d3bbc2b49b11fb9c3cfd9e94822421eee60f5e51c891803d2f1cfcfc5' and json.loads((leader_control/'userdir-config/dlc_load.json').read_text('utf-8'))=={'enabled_mods':[],'disabled_dlcs':[]} and h.sha256(leader_control/'leader13-control-event.sav')==control_proof['before_sha256'] and h.sha256(leader_control/'leader13-control-fleet-effect.sav')==control_proof['after_sha256'] and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
leader_error_evidence={'stage':'terravore-war1-idle11-step1','log_sha256':'df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb','log_size':2814,'native_event':'leader.1','native_line':110,'new_foreign_leader':16777279,'foreign_country':16777219,'sources':leader_sources,'existing_no_mod_control':'leader.13 fleet scope only; new leader.1 creation branch not independently reproduced without mods'}
if after=='terravore-war1-idle11-step1':
    failed21=load(after+'-war1-battle-v21-proof.json');failed21_ex=load(after+'-battle-v21-execution.json');failed_driver=load('terravore-war1-idle11-driver-execution.json')
    error_before=(run/(after+'-error-before.log')).read_bytes();error_after=(run/(after+'-error-after.log')).read_bytes();increment=error_after[len(error_before):]
    expected_error=b'[TIME][effect_utils.cpp:96]: Unable to add trait for [reason] councilor_trait_not_allowed [at]  file: events/leader_events_1.txt line: 110\r\n'
    leader=q.block(ar['leaders'],'16777279');leader_state=q.scalars(leader);leader_traits=[v.strip('"') for k,v,o in q.fields(leader) if k=='traits']
    checks['first_native_leader1_exact144_original_V21_single_error_FAIL_driver1_and_foreign_created_leader_bound']=before=='terravore-war1-idle10-step3' and b['date']=='2269.06.05' and a['date']=='2269.06.19' and days==14 and b['save_sha256']=='15a97e2ab03112419c72557fb081205cfa9f95fd16741006d415ab18318e063b' and a['save_sha256']=='667fb7568b8d0d04c04a5c2b708dfadd518bad254481e91fb990006efaebb310' and failed21['status']=='FAIL' and len(failed21['checks'])==39 and [k for k,v in failed21['checks'].items() if v is not True]==['unfiltered_error2670_exact_held'] and failed21['before_sha256']==b['save_sha256'] and failed21['after_sha256']==a['save_sha256'] and failed21_ex['returncode']==failed_driver['returncode']==1 and failed21_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v21.py')=='25a72330367ddb31328665dd068d47c0e8e05b2f8c1fb4d46388be44a894b173' and failed_driver['helper_sha256']==h.sha256(run/'priority_terravore_idle_war_driver_v12.py')=='c02a68f9110aeb24ae0a289803db1389b2b19bae9e50a6be63ba17532d7cf581' and len(error_before)==2670 and error_after.startswith(error_before) and len(increment)==144 and re.sub(rb'\[\d{2}:\d{2}:\d{2}\]',b'[TIME]',increment)==expected_error and not q.block(br['leaders'],'16777279') and all(leader_state[k]==v for k,v in {'country':16777219,'creator':16777219,'class':'commander','level':2,'date':'2269.06.12','recruitment_date':'2269.06.12'}.items()) and leader_traits==['leader_trait_aggressive','leader_trait_eager']
if after=='terravore-war1-idle11-step1':
    failed22=load(after+'-war1-battle-v22-proof.json');failed22_ex=load(after+'-battle-v22-execution.json')
    checks['first_native_error_V22_41_single_CRCRLF_constant_FAIL_actual1_same_SAV_bound']=failed22['status']=='FAIL' and len(failed22['checks'])==41 and [k for k,v in failed22['checks'].items() if v is not True]==['first_native_leader1_exact144_original_V21_single_error_FAIL_driver1_and_foreign_created_leader_bound'] and failed22_ex['returncode']==1 and failed22_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v22.py')=='e03be7b268a37932585c025b47bb874a47a86033a8321b95cbe1b71745a8654d' and failed22['before_sha256']==b['save_sha256'] and failed22['after_sha256']==a['save_sha256'] and increment.endswith(b'\r\n') and not increment.endswith(b'\r\r\n')
yomon_paid_stage='terravore-yomon-outpost-paid';yomon_paid=load(yomon_paid_stage+'-payment-v3-proof.json');yomon_ex=load(yomon_paid_stage+'-guard-v3-execution.json')
yomon_orders=[q.block(q.block(fleets['2'],'current_order'),'build_orbital_station_order') for fleets in [bfl,afl]]
checks['yomon_outpost_native100A37I_payment22_PASS_actual0_exact_source_SHA_bound']=yomon_paid['status']=='PASS_TERRAVORE_YOMON_NATIVE_OUTPOST_PAYMENT_COMPONENT' and len(yomon_paid['checks'])==22 and all(v is True for v in yomon_paid['checks'].values()) and yomon_ex['returncode']==0 and yomon_ex['helper_sha256']==h.sha256(run/'priority_terravore_yomon_outpost_payment_guard_v3.py')=='4b10c2d68e938a3d42ff98261a856e4fb800a26b60a6463d06efc5f87e6189fa' and yomon_paid['after_sha256']==h.sha256(run/(yomon_paid_stage+'.sav'))=='d753ea1c9faacd7d289653b5facc6d3a4593734ca575581c1b303d57e2402e57' and yomon_paid['actual_paid']=={'influence':37,'alloys':100}
yomon_end_stage='terravore-yomon-outpost-completion-boundary1';yomon_end_sha='dd7ce883c259430e85028f4431155e9a2454cd02d1a905f5baa259df80314c08'
yomon_base=q.block(q.block(ar['starbase_mgr'],'starbases'),'158');yomon_station=ash.get('1931','');yomon_station_state=q.scalars(yomon_station)
yomon_design=q.block(ar['ship_design'],'117442392');yomon_template=q.block(ar['ship_design'],'201326648')
yomon_queue=q.block(q.block(q.block(ar['construction'],'queue_mgr'),'queues'),'2285')
yomon_normalized=lambda raw:[(k,tokvalues(v),o) for k,v,o in q.fields(raw) if k!='auto_gen_design']
checks['yomon_paid_outpost_actual_base158_fleet849_ship1931_full_owned_empty_queues_constructor_idle']=(
    {k:v for k,v in q.scalars(yomon_base).items() if k!='update_flag'}=={'level':'starbase_level_outpost','build_queue':2285,'shipyard_build_queue':4294967295,'station':1931}
    and q.scalars(yomon_base).get('update_flag') in [None,2048]
    and [(k,o) for k,v,o in q.fields(yomon_base) if k!='update_flag']==[('level',False),('build_queue',False),('shipyard_build_queue',False),('ship_design_implementation',True),('station',False),('orbitals',True)]
    and not list(q.fields(q.block(yomon_base,'orbitals')))
) and q.ids(q.block(q.block(ar['galactic_object'],'37'),'starbases'))==[158] and 849 in ao and q.scalars(afl['849'])['ship_class']=='shipclass_starbase' and q.ids(q.block(afl['849'],'ships'))==[1931] and q.scalars(q.block(q.block(afl['849'],'movement_manager'),'coordinate'))['origin']==37 and all(yomon_station_state.get(k)==v for k,v in {'fleet':849,'hitpoints':9150,'max_hitpoints':9150,'armor_hitpoints':3125,'max_armor_hitpoints':3125,'shield_hitpoints':1440,'max_shield_hitpoints':1440,'construction_date':'2270.01.13','upgrade_progress':0}.items()) and q.scalars(q.block(yomon_station,'ship_design_implementation'))==q.scalars(q.block(yomon_base,'ship_design_implementation'))=={'design':117442392,'upgrade':4294967295,'growth_stage':0} and yomon_normalized(yomon_design)==yomon_normalized(yomon_template) and q.scalars(yomon_template).get('auto_gen_design')=='yes' and 'auto_gen_design' not in q.scalars(yomon_design) and tokvalues(q.block(br['ship_design'],'201326648'))==tokvalues(yomon_template) and q.scalars(yomon_queue)=={'owner':0,'simultaneous':1,'type':'starbase'} and q.scalars(q.block(yomon_queue,'location'))=={'type':0,'id':1931} and not q.ids(q.block(yomon_queue,'items')) and not q.block(yomon_base,'modules') and not q.block(yomon_base,'buildings') and q.scalars(q.block(q.block(ar['planets'],'planet'),'518')).get('controller')==0 and q.scalars(q.block(q.block(ar['planets'],'planet'),'518')).get('orbital_defence')==849 and 2 in ao and q.ids(q.block(afl['2'],'ships'))==[2] and q.scalars(ash['2'])['fleet']==2 and q.scalars(ash['2'])['hitpoints']==q.scalars(ash['2'])['max_hitpoints']==375 and q.scalars(afl['2'])['ship_class']=='shipclass_constructor' and q.scalars(afl['2'])['order_id']==13 and not q.block(afl['2'],'current_order') and q.scalars(q.block(afl['2'],'movement_manager'))['state']=='move_idle' and q.scalars(q.block(q.block(afl['2'],'movement_manager'),'coordinate'))=={'x':18.27902,'y':-24.18672,'origin':37} and all(all(q.scalars(q.block(q.block(top['planets'],'planet'),'523')).get(k)==v for k,v in {'planet_class':'pc_tropical','planet_size':13}.items()) and all(k not in q.scalars(q.block(q.block(top['planets'],'planet'),'523')) for k in ['owner','controller','colony']) for top in [br,ar])
if after==yomon_end_stage:
    yomon_end_ok=before=='terravore-yomon-outpost-precompletion-boundary1' and days==1 and b['date']=='2270.01.12' and a['date']=='2270.01.13' and b['save_sha256']=='a16cb3bfbb5dc0860023517b5e0271368f64bc1ef45fdb657bd4edff86bfa7ab' and a['save_sha256']==yomon_end_sha and len(pre['checks'])==43 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v26.py')=='316aec54c6f0a00ad07166ecfa636af7d122f450f16bc311f87d3d17adaff9bf' and q.scalars(yomon_orders[0]).get('progress')==99 and not yomon_orders[1] and not q.block(q.block(br['starbase_mgr'],'starbases'),'158') and '849' not in bfl and '1931' not in bsh and not q.block(q.block(q.block(br['construction'],'queue_mgr'),'queues'),'2285') and set(objects(q.block(ar['starbase_mgr'],'starbases')))==set(objects(q.block(br['starbase_mgr'],'starbases')))|{'158'} and ao==sorted(bo+[849]) and q.ids(q.block(q.block(br['galactic_object'],'37'),'starbases'))==[4294967295] and all(k not in q.scalars(q.block(q.block(br['planets'],'planet'),'518')) for k in ['controller','orbital_defence'])
    yomon_end_evidence={'save_sha256':yomon_end_sha,'date':'2270.01.13','base_id':158,'fleet_id':849,'ship_id':1931,'queue_id':2285,'actual_base_raw':yomon_base,'actual_design_raw':yomon_design,'paid_template_raw':yomon_template,'scope':'Original paid outpost completed with a native materialized design clone; planet523 remains uncolonized.'}
else:
    yomon_end_proof=load(yomon_end_stage+'-war1-battle-v27-proof.json');yomon_end_ex=load(yomon_end_stage+'-battle-v27-execution.json');yomon_end_evidence=yomon_end_proof['native_yomon_completion_evidence']
    yomon_end_ok=yomon_end_proof['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(yomon_end_proof['checks'])==44 and all(v is True for v in yomon_end_proof['checks'].values()) and yomon_end_proof['after_sha256']==h.sha256(run/(yomon_end_stage+'.sav'))==yomon_end_sha and yomon_end_ex['returncode']==0 and yomon_end_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v27.py') and all(q.ids(q.block(q.block(top['galactic_object'],'37'),'starbases'))==[158] and 849 in own and not q.block(fleets['2'],'current_order') and q.scalars(q.block(q.block(fleets['2'],'movement_manager'),'coordinate'))=={'x':18.27902,'y':-24.18672,'origin':37} and [(k,tokvalues(v),o) for k,v,o in omit(q.block(q.block(top['starbase_mgr'],'starbases'),'158'),{'update_flag'})]==[(k,tokvalues(v),o) for k,v,o in omit(yomon_end_evidence['actual_base_raw'],{'update_flag'})] and q.scalars(q.block(q.block(top['starbase_mgr'],'starbases'),'158')).get('update_flag') in [None,2048] and tokvalues(q.block(top['ship_design'],'117442392'))==tokvalues(yomon_end_evidence['actual_design_raw']) for top,fleets,own in [(br,bfl,bo),(ar,afl,ao)])
checks['yomon_exact_first_completion_one_day_prior43_actual0_or_immutable_V27_44PASS_anchor_bound']=bool(yomon_end_ok)
yomon_arrival_stage='terravore-yomon-outpost-start-boundary1';yomon_start_stage='terravore-yomon-outpost-start-daily1'
yomon_arrival=load(yomon_arrival_stage+'-war1-battle-v25-proof.json');yomon_arrival_ex=load(yomon_arrival_stage+'-battle-v25-execution.json')
yomon_ui_name='terravore-yomon-constructor-progress2-tooltip-visible';yomon_ui=load(yomon_ui_name+'.ocr.json')
yomon_start_sha='fca1e0dbb55521337e0e340e7ca2c560f3375b23c85ab0a523e5d2631a601b2d'
yomon_anchor_ok=yomon_arrival['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(yomon_arrival['checks'])==43 and all(v is True for v in yomon_arrival['checks'].values()) and yomon_arrival_ex['returncode']==0 and yomon_arrival_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v25.py')=='f4b4a5a403552c0e49f427f5b0671637a6752763901f924d6b7757bd1cb14830' and yomon_arrival['after_sha256']==h.sha256(run/(yomon_arrival_stage+'.sav'))=='5dc8b4d68c5c08becd6151d8bfef2caf5ae7677b26841ad788bcb9dede7fc8e3' and h.sha256(run/(yomon_start_stage+'.sav'))==yomon_start_sha and h.sha256(run/(yomon_ui_name+'.jpg'))==yomon_ui['image_sha256']=='8cf665747deba0c942abf281d1f920cf5419ecc0bf2c1a5520c5d24109d02d90' and '正在建造亚蒙恒星基地：2%' in [row['text'] for row in yomon_ui['rows']]
if after==yomon_start_stage:
    yomon_anchor_ok &= before==yomon_arrival_stage and days==1 and b['date']=='2269.10.04' and a['date']=='2269.10.05' and b['save_sha256']==yomon_arrival['after_sha256'] and a['save_sha256']==yomon_start_sha and [q.scalars(raw)['progress'] for raw in yomon_orders]==[1,2]
else:
    yomon_start_proof=load(yomon_start_stage+'-war1-battle-v26-proof.json');yomon_start_ex=load(yomon_start_stage+'-battle-v26-execution.json')
    yomon_anchor_ok &= yomon_start_proof['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(yomon_start_proof['checks'])==43 and all(v is True for v in yomon_start_proof['checks'].values()) and yomon_start_proof['after_sha256']==yomon_start_sha and yomon_start_ex['returncode']==0 and yomon_start_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v26.py')
checks['yomon_native_first_daily_percent1_to2_V25_43PASS_actual0_UI2percent_exact_SHA_bound']=bool(yomon_anchor_ok)
colony_end_stage='terravore-colony1085-completion-boundary2';colony_end_sha='ae5c07eb6112d217a7e9163c4b1ed8f4610083a8700ede82b73527c9b357202f'
colony_ui_name='terravore-colony1085-completed-planet-visible';colony_ui=load(colony_ui_name+'.ocr.json');colony_ui_ex=load('terravore-colony1085-completed-open-execution.json');colony_ui_action=load('terravore-colony1085-completed-open.action.json')
colony_source_growth=q.scalars(q.block(q.block(q.block(ar['colony'],'37'),'last_month_growth_data'),'growth_and_size'))
colony_mother_last_growth=q.scalars(q.block(q.block(q.block(ar['colony'],'0'),'last_month_growth_data'),'growth_and_size'))
if after==colony_end_stage:
    colony_end_ok=before=='terravore-war1-idle19-step2' and days==1 and b['date']=='2270.01.30' and a['date']=='2270.02.01' and b['save_sha256']=='2b9bac27bd0fe02ceeba67997143100999badc1c481146ed68c974cf8830bde3' and a['save_sha256']==colony_end_sha and len(pre['checks'])==44 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v27.py')=='10f5f86929511f8ea3180df1e38cd34515029dc2d4123460a2ef92fe1b188753' and b['colonies']['37'].get('colonizing_species')==73 and b['colonies']['37']['actual_pop_sum']==99 and colony['actual_pop_sum']==103 and colony_source_growth=={'month_start_size':99,'growth':4} and b['colonies']['0']['actual_pop_sum']==10820 and a['colonies']['0']['actual_pop_sum']==10826 and colony_mother_last_growth=={'month_start_size':10820,'growth':6} and sum(a['colonies'][str(i)]['actual_pop_sum']-b['colonies'][str(i)]['actual_pop_sum'] for i in ac['owned_colonies'])==10 and colony['pop_groups']==[402653219] and a['pop_groups']['402653219']['key']=={'species':73,'category':'complex_drone'} and all(335544348 not in co['pop_groups'] for co in a['colonies'].values()) and tokvalues(q.block(br['districts'],'68'))==tokvalues(q.block(ar['districts'],'68')) and q.ids(q.block(q.block(br['zones'],'16777291'),'buildings'))==[130] and tokvalues(q.block(br['buildings'],'130'))==tokvalues(q.block(ar['buildings'],'33554455')) and [(k,q.scalars(q.block(ar['buildings'],'130'))[k],o) for k,v,o in q.fields(q.block(ar['buildings'],'130'))]==[('type','building_hive_capital',False),('killed','yes',False),('position',0,False)] and all(130 not in q.ids(q.block(raw,'buildings')) for raw in objects(ar['zones']).values()) and all(b['pop_jobs'][old]['planet']==a['pop_jobs'][new]['planet']==37 and b['pop_jobs'][old]['type']==a['pop_jobs'][new]['type']==kind and b['pop_jobs'][old]['max_workforce']==a['pop_jobs'][new]['max_workforce']==cap for old,new,kind,cap in [('16777369','812','coordinator',200),('16777394','814','logistics_drone',200),('16777395','813','patrol_drone',100)]) and h.sha256(run/(colony_ui_name+'.jpg'))==colony_ui['image_sha256']=='a87f16c2c9060051c0bfa1a764e6c4f347ea3a65d761f8ed97d9fd617b645b19' and any('2270.02.01' in row['text'] for row in colony_ui['rows']) and colony_ui_ex['returncode']==0 and colony_ui_ex['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and colony_ui_action['action']=='left-click' and colony_ui_action['client_point']==[901,278]
    colony_end_evidence={'save_sha256':colony_end_sha,'date':'2270.02.01','physical_planet':1085,'colony_id':37,'native_source_growth':colony_source_growth,'native_mother_growth':colony_mother_last_growth,'population_delta':10,'new_source_group':a['pop_groups']['402653219'],'old_building':130,'new_building':33554455,'source_UI_sha256':colony_ui['image_sha256'],'scope':'Actual native colony completion; existing district and logical capital/jobs preserved with native instance replacement, no EEP reward. Negative E/A monthly nets recorded; full operating recovery remains pending.'}
else:
    colony_end_proof=load(colony_end_stage+'-war1-battle-v29-proof.json');colony_end_ex=load(colony_end_stage+'-battle-v29-execution.json');colony_end_evidence=colony_end_proof['native_colony1085_completion_evidence']
    colony_end_ok=colony_end_proof['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(colony_end_proof['checks'])==46 and all(v is True for v in colony_end_proof['checks'].values()) and colony_end_proof['after_sha256']==h.sha256(run/(colony_end_stage+'.sav'))==colony_end_sha and colony_end_ex['returncode']==0 and colony_end_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v29.py') and 'colonizing_species' not in b['colonies']['37']
checks['colony1085_exact_completed_one_day_native_growth10_UI_and_prior44_or_immutable_V29_46PASS_anchor']=bool(colony_end_ok)
failed28=load(colony_end_stage+'-war1-battle-v28-proof.json');failed28_ex=load(colony_end_stage+'-battle-v28-execution.json')
checks['original_V28_exact45_single_FAIL_actual1_same_completed_SHA_pair_preserved']=(failed28['status']=='FAIL' and len(failed28['checks'])==45 and [k for k,v in failed28['checks'].items() if v is not True]==['colony1085_exact_completed_one_day_native_growth10_UI_and_prior44_or_immutable_V28_45PASS_anchor'] and failed28_ex['returncode']==1 and failed28_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v28.py')=='fc8e6e6e1b92aacfbeaf34af479c78594c6dce7fcc3a24c271eb0bcf6f7ea790' and failed28['before_sha256']=='2b9bac27bd0fe02ceeba67997143100999badc1c481146ed68c974cf8830bde3' and failed28['after_sha256']==h.sha256(run/(colony_end_stage+'.sav'))==colony_end_sha)
checks['third_native_start35_PASS_actual0_source_SAV_and_held_initial_ledger_bound']=third_start_proof['status']=='PASS_TERRAVORE_THIRD_NATIVE_START_COMPONENT' and len(third_start_proof['checks'])==35 and all(v is True for v in third_start_proof['checks'].values()) and third_start_proof['after_sha256']==h.sha256(run/(third_start_stage+'.sav'))=='e030634f1d921a002869cff7a5a3639e0aae56fb9b5a93455d4158572b10281a' and third_start_ex['returncode']==0 and third_start_ex['helper_sha256']==h.sha256(run/'priority_terravore_third_native_start_guard_v2.py')=='801ddc424c827482d5b3f2bdf5c0f312da784d1215ecb501b74c1ab1bc8fe4b6' and bc['variables']==ac['variables']==third_start['countries']['0']['variables']
clear_stage='terravore-mother-blocker-clear-paid';clear_proof=load(clear_stage+'-blocker-payment-v2-proof.json');clear_ex=load(clear_stage+'-guard-v2-execution.json')
clear_b,clear_a=[raw.get('1224736779','') for raw in [bi,ai]]

clear_done_pair=[audit['date']>='2270.08.15' for audit in [b,a]]
clear_states=[]
for top,audit,raw,rawq,done in zip([br,ar],[b,a],[clear_b,clear_a],[mbq,maq],clear_done_pair):
 dep=q.block(top['deposit'],'272');expected_fields=[('type','"d_fertile_lands"',False),('deposit_holder',q.block(dep,'deposit_holder'),True)] if done else [('type','"d_failing_infrastructure"',False),('swap_type','"d_fertile_lands"',False),('deposit_holder',q.block(dep,'deposit_holder'),True)]
 valid=list(q.fields(dep))==expected_fields and q.scalars(q.block(dep,'deposit_holder'))=={'type':0,'id':7} and 272 in audit['planets']['7']['deposits'] and q.ids(q.block(rawq,'items'))==([16777257] if done else [1224736779,16777257])
 if done:
  records={k:(v,o) for k,v,o in q.fields(q.block(q.block(top['construction'],'item_mgr'),'items'))};slots=[int(k) for k in records if k.isdigit() and int(k)%16777216==1224736779%16777216];original=records.get('1224736779');refs=[i for k,v,o in q.fields(q.block(q.block(top['construction'],'queue_mgr'),'queues')) if o for i in q.ids(q.block(v,'items'))]
  valid=valid and 1224736779 not in refs and ((original==('none',False) and slots==[1224736779]) or (original is None and len(slots)==1 and slots[0]>1224736779 and (slots[0]-1224736779)%16777216==0))
 else:
  valid=valid and omit(raw,{'progress'})==omit(clear_proof['actual_order_raw'],{'progress'}) and 0<=D(str(q.scalars(raw)['progress']))<120 and D(str(q.scalars(raw)['progress']))==ordinal(audit['date'])-ordinal('2270.04.15')
 clear_states.append(bool(valid))
checks['paid_clear272_300E17_PASS_actual0_exact_completion_and_fertile_same_ID']=clear_proof['status']=='PASS_TERRAVORE_NATIVE_BLOCKER_PAYMENT_COMPONENT' and len(clear_proof['checks'])==17 and all(v is True for v in clear_proof['checks'].values()) and clear_proof['after_sha256']==h.sha256(run/(clear_stage+'.sav'))=='14c59f182e97cbfff4d46a4cb7d444b027c6cbc2a8009a812b1d19f68c5be4e1' and clear_ex['returncode']==0 and clear_ex['helper_sha256']==h.sha256(run/'priority_terravore_blocker_payment_guard_v2.py')=='7d2be883d7fbd84a7dcde746bf970f4582da8c2c5b924fc23d6595cb556b63d6' and all(clear_states) and clear_done_pair[1] and mine_completed_before==mine_completed_after==3

failed30_stage='terravore-third-devour-calibration14-battle-v30';failed30_ex=load(failed30_stage+'-execution.json');failed30_err=(run/(failed30_stage+'-stderr.txt')).read_text('utf-8')
checks['original_V30_dict_raw_type_exception_actual1_exact_source_and_pair_preserved']=failed30_ex['returncode']==1 and failed30_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v30.py')=='466d67f0eca96f1204f8aad1e6b67e5ae1436325596abe7d52b9e21b7fc242d2' and failed30_ex['command'][2:]==['terravore-mother-blocker-clear-paid','terravore-third-devour-calibration14'] and failed30_err.rstrip().endswith("TypeError: expected string or bytes-like object, got 'dict'") and not (run/'terravore-third-devour-calibration14-war1-battle-v30-proof.json').exists()
clear_first_stage='terravore-mother-clear-first-work';clear_first_sha='c27de545eacc1081ae36533f7f2d3928054ad705662b422e6755b7a79a5cca7d'
if after==clear_first_stage:
 clear_first_valid=before=='terravore-war1-idle21-step2' and days==1 and b['date']=='2270.04.15' and a['date']=='2270.04.16' and b['save_sha256']=='77b4165921b01ebe079d0dc9013dd97054e8eeac42a0ab9780481f221ca721f3' and a['save_sha256']==clear_first_sha and len(pre['checks'])==49 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v31.py')=='32e76bbf006df276ba5e01958ec653ee491e89182343d268a20eecac89399338' and q.scalars(clear_b)['progress']==0 and q.scalars(clear_a)['progress']==1
else:
 clear_first=load(clear_first_stage+'-war1-battle-v32-proof.json');clear_first_ex=load(clear_first_stage+'-battle-v32-execution.json')
 clear_first_valid=clear_first['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(clear_first['checks'])==50 and all(v is True for v in clear_first['checks'].values()) and clear_first_ex['returncode']==0 and clear_first_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v32.py') and clear_first['after_sha256']==h.sha256(run/(clear_first_stage+'.sav'))==clear_first_sha and clear_first['actual_clear_progress']==1
checks['clear_first_exact_native_one_day_work1_from0_prior49_or_immutable_V32_50PASS_anchor']=bool(clear_first_valid)

colony523_stage='terravore-yomon-colony-paid';colony523_paid=load(colony523_stage+'-colony-payment-proof.json');colony523_ex=load(colony523_stage+'-guard-execution.json')
heavy_stage='terravore-mother-heavy-conversion-paid';heavy_paid=load(heavy_stage+'-heavy-payment-proof.json');heavy_ex=load(heavy_stage+'-guard-execution.json')
checks['colony523_original17_PAYMENT_PASS_actual0_source_and_SHA_bound']=colony523_paid['status']=='PASS_TERRAVORE_YOMON_COLONY_PAYMENT_COMPONENT' and len(colony523_paid['checks'])==17 and all(v is True for v in colony523_paid['checks'].values()) and colony523_ex['returncode']==0 and colony523_ex['helper_sha256']==h.sha256(run/'priority_terravore_yomon_colony_payment_guard.py')=='1d8279c62e72e4033cbb1b32332ffac84db0b3bd8c164b1b12c516facaefe24a' and colony523_paid['after_sha256']==h.sha256(run/(colony523_stage+'.sav'))=='a416d360d40d28b24e2a8fc9d01b0c279bf03fd1bd24dd52c77b5c136415c9b0'
checks['heavy_original14_PAYMENT_PASS_actual0_source_and_SHA_bound']=heavy_paid['status']=='PASS_TERRAVORE_HEAVY_CONVERSION_PAYMENT_COMPONENT' and len(heavy_paid['checks'])==14 and all(v is True for v in heavy_paid['checks'].values()) and heavy_ex['returncode']==0 and heavy_ex['helper_sha256']==h.sha256(run/'priority_terravore_heavy_conversion_payment_guard.py')=='5e44523f27ccd53a4c32338039e1ca0743fee37e5e3b1763b9f0ae3be30bdd53' and heavy_paid['after_sha256']==h.sha256(run/(heavy_stage+'.sav'))=='d7ecdd864e0b97bbca18f6d2ad6cd1c7af871191770e558dc6fe3abc5495a732'
colony523_raw=[rawitems.get('16777256','') for rawitems in [bi,ai]]
colony523_done=[not raw for raw in colony523_raw];colony523_work=[D(360) if done else D(str(q.scalars(raw)['progress'])) for raw,done in zip(colony523_raw,colony523_done)]
colony523_build_ok=True;colony523_expansion=[];colony523_targets=[];colony523_ship_states=[];colony523_fleet_states=[]
for top,audit,rawitems,rawqueue,raw,done,work,fleets,ships,own in zip([br,ar],[b,a],[bi,ai],[bq,aq],colony523_raw,colony523_done,colony523_work,[bfl,afl],[bsh,ash],[bo,ao]):
 expansion=q.block(q.block(q.block(q.block(top['country'],'0'),'modules'),'standard_expansion_module'),'expansion_list');xs=list(anonymous_objects(expansion));colony523_expansion.append(xs);colony523_targets.append(q.block(q.block(top['planets'],'planet'),'523'))
 if not done:
  valid=q.ids(q.block(rawqueue,'items'))==[16777256] and omit(raw,{'progress'})==omit(colony523_paid['actual_colony523_order_raw'],{'progress'}) and 0<=work<360 and work==D('1.33')*(ordinal(audit['date'])-ordinal('2270.05.15')) and len(xs)==1 and tokvalues(xs[0])==tokvalues(colony523_paid['actual_colony523_expansion_raw']) and '16779140' not in ships and '16778062' not in fleets
  colony523_ship_states.append(None);colony523_fleet_states.append(None)
 else:
  allqueues=objects(q.block(q.block(top['construction'],'queue_mgr'),'queues'));raw_items=q.block(q.block(top['construction'],'item_mgr'),'items');handles=[(int(k),v,o) for k,v,o in q.fields(raw_items) if int(k)%16777216==40]
  ship=ships.get('16779140','');fleet=fleets.get('16778062','');sv=q.scalars(ship);fv=q.scalars(fleet);order=q.block(q.block(fleet,'current_order'),'colonize_planet_order');ov=q.scalars(order);position=q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate'))
  design=q.scalars(q.block(ship,'ship_design_implementation'))
  duplicates=[int(k) for k,v in ships.items() if q.scalars(q.block(v,'ship_design_implementation')).get('design')==150995039 and q.scalars(q.block(v,'colonization_data')).get('species')==73]
  valid=q.ids(q.block(rawqueue,'items'))==[] and not any(16777256 in q.ids(q.block(v,'items')) for v in allqueues.values()) and len(handles)==1 and (handles[0]==(16777256,'none',False) or handles[0][0]>16777256) and xs==[] and 16778062 in own and q.ids(q.block(fleet,'ships'))==duplicates==[16779140] and sv.get('fleet')==16778062 and sv.get('construction_date')=='2271.02.16' and sv.get('killed')!='yes' and all(sv.get(k)==sv.get('max_'+k)>0 for k in ['hitpoints','armor_hitpoints','shield_hitpoints']) and design=={'design':150995039,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(ship,'colonization_data'))=={'species':73} and fv.get('ship_class')=='shipclass_colonizer' and not combat(fleet) and 'return_date' not in fv and q.scalars(q.block(fleet,'properties')).get('mia') is None and ov.get('planet')==523 and ov.get('progress')==0 and ov.get('can_reach')=='yes' and tokvalues(q.block(order,'name'))==tokvalues(q.block(colony523_paid['actual_colony523_expansion_raw'],'name')) and str(position.get('origin')) in objects(top['galactic_object'])
  colony523_ship_states.append(sv);colony523_fleet_states.append({'native':fv,'order':ov,'position':position,'path_prediction':q.scalars(q.block(q.block(fleet,'movement_manager'),'path')).get('date')})
 colony523_build_ok=colony523_build_ok and valid
checks['colony523_unique_paid_order_build_or_one_native_born_colonizer_no_duplicate']=bool(colony523_build_ok and bids==aids==[] and not (colony523_done[0] and not colony523_done[1]) and (colony523_work[1]-colony523_work[0]==D('1.33')*days if not colony523_done[1] else True))
checks['colony523_original_expansion_consumed_to_native_order_target_still_uncolonized13tropical']=all(q.scalars(raw).get('planet_class')=='pc_tropical' and q.scalars(raw).get('planet_size')==13 and not any(k in {'owner','controller','colony','colonize_date'} for k,v,o in q.fields(raw)) for raw in colony523_targets)
heavy_raw=[rawitems.get('16777257','') for rawitems in [bi,ai]]

heavy_work=[D(str(q.scalars(raw)['progress'])) for raw in heavy_raw]
checks['heavy_exact_original_order1point4_daily_work_after_paid_clear']=all(omit(raw,{'progress'})==omit(heavy_paid['actual_heavy_order_raw'],{'progress'}) for raw in heavy_raw) and all(0<=work<360 and work==D('1.4')*(ordinal(audit['date'])-ordinal('2270.08.15')) for work,audit in zip(heavy_work,[b,a])) and heavy_work[1]-heavy_work[0]==D('1.4')*days and all(q.ids(q.block(raw,'items'))==[16777257] for raw in [mbq,maq]) and clear_done_pair==[True,True]

civilian_first_stage='terravore-dual-civilian-first-work';civilian_first_sha='39ae981c14cec416797ea224f7e4e1b4f9314ed04af3f64873990ec6c4ef4c88'
if after==civilian_first_stage:
 civilian_first_ok=before==heavy_stage and days==1 and b['date']=='2270.05.15' and a['date']=='2270.05.16' and b['save_sha256']==heavy_paid['after_sha256'] and a['save_sha256']==civilian_first_sha and len(pre['checks'])==14 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==heavy_ex['helper_sha256'] and colony523_work==[D(0),D('1.33')] and [q.scalars(raw)['progress'] for raw in [clear_b,clear_a]]==[30,31]
else:
 civilian_first=load(civilian_first_stage+'-war1-battle-v33-proof.json');civilian_first_ex=load(civilian_first_stage+'-battle-v33-execution.json')
 civilian_first_ok=civilian_first['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(civilian_first['checks'])==56 and all(v is True for v in civilian_first['checks'].values()) and civilian_first_ex['returncode']==0 and civilian_first_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v33.py') and civilian_first['after_sha256']==h.sha256(run/(civilian_first_stage+'.sav'))==civilian_first_sha and civilian_first['actual_colony523_order_progress']=='1.33' and civilian_first['actual_clear_progress']==31
checks['civilian_first_exact_one_day1point33_prior14_or_immutable_V33_56PASS_anchor']=bool(civilian_first_ok)


enemy_return_stage='terravore-enemy825-return-boundary2';enemy_return_sha='d6e27afa98f77a2b61a2e4a7af5e222c4e6a8a7afce38ca7a1ff8b89fe836b63'
if after==enemy_return_stage:
 enemy_return_ok=before=='terravore-enemy825-return-boundary1' and days==1 and b['date']=='2270.07.07' and a['date']=='2270.07.08' and b['save_sha256']=='67217b3110b6e3d58e69a826c89dc6ab9f3f503b88d16ad38309c0b679683bdd' and a['save_sha256']==enemy_return_sha and len(pre['checks'])==57 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v34.py')=='a0f008b40d25ad8bb33d12dc89638962fe877b4201caf8cc298167082b0ee00b' and q.scalars(bfl['825'])['return_date']=='2270.07.07' and q.scalars(q.block(bfl['825'],'properties'))['mia']=='yes' and q.scalars(q.block(q.block(bfl['825'],'movement_manager'),'coordinate'))['origin']==4294967295 and q.scalars(q.block(q.block(afl['825'],'movement_manager'),'coordinate'))=={'x':203.22038,'y':-111.43812,'origin':99} and q.scalars(q.block(afl['825'],'properties'))=={'weapon':'yes','mobile':'yes','valid_for_combat':'yes'} and q.scalars(afl['825'])['mia_type']=='mia_emergency_ftl' and before_enemy==after_enemy
else:
 enemy_return=load(enemy_return_stage+'-war1-battle-v35-proof.json');enemy_return_ex=load(enemy_return_stage+'-battle-v35-execution.json')
 enemy_return_ok=enemy_return['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(enemy_return['checks'])==57 and all(v is True for v in enemy_return['checks'].values()) and enemy_return_ex['returncode']==0 and enemy_return_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v35.py') and enemy_return['after_sha256']==h.sha256(run/(enemy_return_stage+'.sav'))==enemy_return_sha and enemy_return['actual_enemy825_returned'] is True
checks['enemy825_exact_native_first_return_one_day_prior57_or_immutable_V35_57PASS_anchor']=bool(enemy_return_ok)


clear_end_stage='terravore-mother-clear-completed';clear_end_sha='a01e644c43e6a5124c8caebfc8f4d76573e289038c9f2a81c0a83732a88c181b'
if after==clear_end_stage:
 clear_end_ok=before=='terravore-war1-idle25-step1' and days==1 and b['date']=='2270.08.14' and a['date']=='2270.08.15' and b['save_sha256']=='14386cc37408a93ebb99f0ac4c4cc6a38d31a78a7d52e4d2b11d5e23fb03e92b' and a['save_sha256']==clear_end_sha and len(pre['checks'])==57 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v35.py')=='02e650682fb918fa9ffa572493d6d3bece834655d4a2e56e7c148b9ced59b9e6' and clear_done_pair==[False,True] and q.scalars(clear_b)['progress']==119 and bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'] and b['planets']['7']['deposits']==a['planets']['7']['deposits'] and h.sha256(run/'native-blocker-clear-01_blocker_deposits.txt')=='df9665890f54567b5988857e73baf752f690ad2fc8beb1ab7f543e184e43b11a'
else:
 clear_end=load(clear_end_stage+'-war1-battle-v36-proof.json');clear_end_ex=load(clear_end_stage+'-battle-v36-execution.json')
 clear_end_ok=clear_end['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(clear_end['checks'])==58 and all(v is True for v in clear_end['checks'].values()) and clear_end_ex['returncode']==0 and clear_end_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v36.py') and clear_end['after_sha256']==h.sha256(run/(clear_end_stage+'.sav'))==clear_end_sha and clear_end['actual_clear_complete'] is True
checks['clear272_exact_native119_to_complete_one_day_prior57_or_immutable_V36_58PASS_anchor']=bool(clear_end_ok)


heavy_first_stage='terravore-heavy-first-work';heavy_first_sha='e390ea18fafcc5e913db5795e261c71ea445a82d203b916e69c37b4cb67c7b48'
if after==heavy_first_stage:
 heavy_first_ok=before=='terravore-mother-clear-completed' and days==1 and b['date']=='2270.08.15' and a['date']=='2270.08.16' and b['save_sha256']=='a01e644c43e6a5124c8caebfc8f4d76573e289038c9f2a81c0a83732a88c181b' and a['save_sha256']==heavy_first_sha and len(pre['checks'])==58 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v36.py')=='01d294c5566a20771d71fb95072640d4ef64062fbeadb665f891af2e1f09d589' and heavy_work==[D(0),D('1.4')] and bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile']
else:
 heavy_first=load(heavy_first_stage+'-war1-battle-v37-proof.json');heavy_first_ex=load(heavy_first_stage+'-battle-v37-execution.json')
 heavy_first_ok=heavy_first['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(heavy_first['checks'])==60 and all(v is True for v in heavy_first['checks'].values()) and heavy_first_ex['returncode']==0 and heavy_first_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v37.py') and heavy_first['after_sha256']==h.sha256(run/(heavy_first_stage+'.sav'))==heavy_first_sha and heavy_first['actual_heavy_order_progress']=='1.4'
checks['heavy_first_exact_native_one_day1point4_prior58_or_immutable_V37_60PASS_anchor']=bool(heavy_first_ok)
heavy_source_bindings={'common/zones/00_zones.txt': 'ce48f6aea3b5a5a30dabe15b46b5a32ac9149389b3d412d7f0cccf7f1562dcaa', 'common/inline_scripts/zones/shared_industrial_foundry_zone.txt': '355351b6e6b151e1ff1f6bbf22b72977acc850870f907abe0231362b74137d95', 'common/inline_scripts/jobs/zone_foundry_add.txt': '76a0376e41fa879774ada460893a3dafe1ea349166d076143e08f2b72a516d88', 'common/inline_scripts/zones/shared_city_non_urban_zone_modifiers.txt': 'fe613595b2109be9f38738b225ef0d57a8c8e1cbd2928363c4e4c5cb2001b397', 'common/scripted_variables/100_scripted_variables_zones.txt': 'f67b8c2d1d53c5b392ae60d0b89d069b581e59dee52f8102a2a47c430b216155'}
checks['five_native_heavy_zone_jobs_housing_scaling_sources_exact_bound']=all(h.sha256(game/rel)==h.sha256(run/('native-heavy-completion-'+Path(rel).name))==sha for rel,sha in heavy_source_bindings.items())


source_over_stage='terravore-source-over200-boundary';source_over_sha='b811c3477ac907300970b93320ee93a487bfc5f5bdec0914ce6f838cb7610e74'
source_jobs_valid=True
for audit in [b,a]:
 co=audit['colonies']['37'];n=co['actual_pop_sum'];jobs=audit['pop_jobs'];source_jobs_valid=source_jobs_valid and 100<=n<=500 and jobs['812']['workforce']==min(n,200) and all(0<=jobs[i]['workforce']<=cap and jobs[i]['automated_workforce']==0 and jobs[i]['max_workforce']==cap and jobs[i]['planet']==37 for i,cap in [('812',200),('813',100),('814',200)]) and sum(jobs[i]['workforce'] for i in ['812','813','814'])==n
if after==source_over_stage:
 source_over_ok=before=='terravore-war1-idle26-step1' and days==1 and b['date']=='2270.08.30' and a['date']=='2270.09.01' and b['save_sha256']=='f90bd9499254ad2dbc498f4029992123e643cb84a2c75a6dc13431c949abffa1' and a['save_sha256']==source_over_sha and len(pre['checks'])==60 and all(v is True for v in pre['checks'].values()) and execution['returncode']==0 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v37.py')=='f5da19eab1bba265e094c6c0e5ada73d1dc3d60264f4ce9d73a8ca783675a1d1' and b['colonies']['37']['actual_pop_sum']==200 and colony['actual_pop_sum']==216 and b['colonies']['37']['pop_groups']==colony['pop_groups']==[402653219] and a['pop_groups']['402653219']['key']=={'species':73,'category':'complex_drone'} and q.scalars(q.block(q.block(q.block(ar['colony'],'37'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':200,'growth':16} and list(q.fields(q.block(q.block(q.block(ar['colony'],'37'),'last_month_growth_data'),'current_month_growth_details')))==[('key','"GROWTH_CAT_IMMIGRATION"',False),('value','16',False),('key','"GROWTH_CAT_PROMOTION"',False),('value','0',False)] and b['pop_jobs']['813']['workforce']==0 and a['pop_jobs']['813']['workforce']==16 and sum(a['colonies'][i]['actual_pop_sum']-b['colonies'][i]['actual_pop_sum'] for i in ['0','37'])==7
else:
 source_over=load(source_over_stage+'-war1-battle-v38-proof.json');source_over_ex=load(source_over_stage+'-battle-v38-execution.json')
 source_over_ok=source_over['status']=='PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' and len(source_over['checks'])==61 and all(v is True for v in source_over['checks'].values()) and source_over_ex['returncode']==0 and source_over_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v38.py') and source_over['after_sha256']==h.sha256(run/(source_over_stage+'.sav'))==source_over_sha and source_over['actual_colonization_population']==216
checks['source_native_cross200_exact_coordinator_patrol_assignment_prior60_or_V38_61PASS_anchor']=bool(source_over_ok and source_jobs_valid)

annual_stage='terravore-third-first-year-boundary';annual_proof=load(annual_stage+'-war1-battle-v40-proof.json');annual_ex=load(annual_stage+'-battle-v40-execution.json')
checks['first_native_annual65_PASS_actual0_100alloys_two_deposits_original_V39_failure_bound']=annual_proof['status'].startswith('PASS_') and len(annual_proof['checks'])==65 and all(v is True for v in annual_proof['checks'].values()) and annual_ex['returncode']==0 and annual_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v40.py')=='fe9ed008335f172dcd3be811e32759232ae99a18edcef10a27ecc910ba08a371' and annual_proof['after_sha256']==h.sha256(run/(annual_stage+'.sav'))=='7f422e7373b4c49772fbc313e963540474f34e9fb4c9b1349a5800f1235e7caa' and annual_proof['actual_annual_resource_deltas']['alloys']=='96.88931' and annual_proof['actual_annual_current_month_nets']['alloys']=='-3.11069'
next_day_stage='terravore-third-first-year-next-day';next_day_sha='9416c13c83987127a0fdc2fc0e108c71a4d7eb6ce7d548d98dc0f2a1736e9acc'
def research_queue_value(country,key):
 return q.scalars(next(anonymous_objects(q.block(q.block(country,'tech_status'),key))))
if after==next_day_stage:
 next_day_ok=before==annual_stage and days==1 and b['date']=='2271.02.01' and a['date']=='2271.02.02' and a['save_sha256']==next_day_sha and pre==annual_proof and execution==annual_ex and all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k] for k in ['energy','minerals','alloys','unity','trade','influence','menace']) and bc['research_stockpile']=={'physics_research':0,'society_research':6875.72733,'engineering_research':0} and ac['research_stockpile']=={'physics_research':0,'society_research':6910.51946,'engineering_research':0} and {k:v for k,v in ac['stockpile'].items() if 'research' in k}=={'society_research':6875.72733} and [(research_queue_value(cr,'physics_queue')['progress'],research_queue_value(cr,'engineering_queue')['progress']) for cr in [bcr,acr]]==[(661.55721,983.43912),(700.47234,1024.41575)] and b['colonies']['37']['actual_pop_sum']==a['colonies']['37']['actual_pop_sum']==282 and b['colonies']['0']['actual_pop_sum']==a['colonies']['0']['actual_pop_sum']==10725 and b['situations']==a['situations'] and b['planets']['1085']['bombardment_damage']==20 and a['planets']['1085']['bombardment_damage']==19.97449
else:
 next_day=load(next_day_stage+'-war1-battle-v41-proof.json');next_day_ex=load(next_day_stage+'-battle-v41-execution.json')
 next_day_ok=next_day['status'].startswith('PASS_') and len(next_day['checks'])==63 and all(v is True for v in next_day['checks'].values()) and next_day_ex['returncode']==0 and next_day_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v41.py') and next_day['after_sha256']==h.sha256(run/(next_day_stage+'.sav'))==next_day_sha
checks['first_postannual_one_day_actual_recovery_and_research_monthly_tick_prior65_or_V41_63PASS_anchor']=bool(next_day_ok)

colony_birth_stage='terravore-colony523-birth-boundary';colony_birth_sha='dae6dbdf1ff8337c2b8114b5b7812adc3adb5195fe651f102f57025cae842a0a'
if after==colony_birth_stage:
 colony_birth_ok=before=='terravore-colony523-prebirth-boundary' and days==1 and b['date']=='2271.02.15' and a['date']=='2271.02.16' and b['save_sha256']=='d17b2f2ee3f4a4f411fad7944ddd47255e47332ebd7915edadcd70ce54e40f07' and a['save_sha256']==colony_birth_sha and len(pre['checks'])==63 and execution['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v41.py')=='c055611bd54502d81eb065b3ba69d874397e5cc7748cbf0246bc1ae05786d89c' and colony523_work==[D('359.1'),D(360)] and colony523_done==[False,True] and set(ash)-set(bsh)=={'16779140'} and set(afl)-set(bfl)=={'16778062'} and set(ao)-set(bo)=={16778062} and bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'] and all(b['colonies'][i]['actual_pop_sum']==a['colonies'][i]['actual_pop_sum'] for i in ['0','37'])
else:
 colony_birth=load(colony_birth_stage+'-war1-battle-v43-proof.json');colony_birth_ex=load(colony_birth_stage+'-battle-v43-execution.json')
 colony_birth_ok=colony_birth['status'].startswith('PASS_') and len(colony_birth['checks'])==65 and all(v is True for v in colony_birth['checks'].values()) and colony_birth_ex['returncode']==0 and colony_birth_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v43.py') and colony_birth['after_sha256']==h.sha256(run/(colony_birth_stage+'.sav'))==colony_birth_sha and colony_birth['actual_colony523_ship_complete'] is True
checks['colony523_first_paid_birth_exact_single_day_prior63_or_V43_65PASS_anchor']=bool(colony_birth_ok)

original42=load(colony_birth_stage+'-war1-battle-v42-proof.json');original42_ex=load(colony_birth_stage+'-battle-v42-execution.json')
checks['original_V42_name_raw_indent_only_singleFAIL_actual1_retained']=original42['status']=='FAIL' and len(original42['checks'])==64 and [k for k,v in original42['checks'].items() if v is not True]==['colony523_unique_paid_order_build_or_one_native_born_colonizer_no_duplicate'] and original42_ex['returncode']==1 and original42_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v42.py')=='5cfce3e6fc4875c516f538f090fb242c162b2bbc8054ae37c504f8a17e679aea' and original42['after_sha256']==colony_birth_sha and h.sha256(run/(colony_birth_stage+'-battle-v42-stderr.txt'))=='17bb78ffc11a47283cdcfbcf03f396a5d8ae084231df942c1941ed8beb856c22'
reassign_stage='terravore-war1-idle29-step1';reassign_sha='9d8368cd6a35c2f50daefb6432c314bb875b8f1b39363f562bafd29f724d274f'
old43=load(reassign_stage+'-war1-battle-v43-proof.json');old43_ex=load(reassign_stage+'-battle-v43-execution.json');old25_ex=load('terravore-war1-idle29-driver-execution.json')
checks['original_postannual_V43_exact65_two_fixed_priority_FAIL_driver1_no_step2_retained']=old43['status']=='FAIL' and len(old43['checks'])==65 and [k for k,v in old43['checks'].items() if v is not True]==['same_native_colony37_1085_completed_owned_founder73_original_hive_structure','source_native_cross200_exact_coordinator_patrol_assignment_prior60_or_V38_61PASS_anchor'] and old43_ex['returncode']==old25_ex['returncode']==1 and old43_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v43.py')=='f25c2994ce812b2402fcb4bc8fc7e80edc6a772c2e16550835417ecdbf3a2789' and old25_ex['helper_sha256']==h.sha256(run/'priority_terravore_idle_war_driver_v25.py')=='3b25c06f97f4b3da8cda8f96208fa491248f8196a9b9ff8cfeabd71d2cf3539a' and old43['after_sha256']==reassign_sha and h.sha256(run/(reassign_stage+'-battle-v43-stderr.txt'))=='c89d461a2e60cfc6e746ca522e805dac81d93cf51ab5c3aeb16e92857288ac64' and not (run/'terravore-war1-idle29-step2-calendar-execution.json').exists()
if after==reassign_stage:
 reassign_ok=before=='terravore-colony523-birth-boundary' and days==30 and b['date']=='2271.02.16' and a['date']=='2271.03.16' and b['save_sha256']==colony_birth_sha and a['save_sha256']==reassign_sha and len(pre['checks'])==65 and execution['helper_sha256']=='f25c2994ce812b2402fcb4bc8fc7e80edc6a772c2e16550835417ecdbf3a2789' and b['colonies']['37']['actual_pop_sum']==a['colonies']['37']['actual_pop_sum']==282 and b['colonies']['37']['pop_groups']==a['colonies']['37']['pop_groups']==[402653219] and [b['pop_jobs'][i]['workforce'] for i in ['812','813','814']]==[200,82,0] and [a['pop_jobs'][i]['workforce'] for i in ['812','813','814']]==[200,0,82] and b['colonies']['37']['free_amenities']==-110.936 and a['colonies']['37']['free_amenities']==331.72714 and q.scalars(q.block(q.block(q.block(ar['colony'],'37'),'last_month_growth_data'),'growth_and_size'))=={'month_start_size':282,'growth':0}
else:
 reassigned=load(reassign_stage+'-war1-battle-v44-proof.json');reassigned_ex=load(reassign_stage+'-battle-v44-execution.json')
 reassign_ok=reassigned['status'].startswith('PASS_') and len(reassigned['checks'])==67 and all(v is True for v in reassigned['checks'].values()) and reassigned_ex['returncode']==0 and reassigned_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v44.py') and reassigned['after_sha256']==h.sha256(run/(reassign_stage+'.sav'))==reassign_sha
checks['native_amenities_negative_factor10_job_reassignment_same282_first_or_V44_67PASS_anchor']=bool(reassign_ok and h.sha256(game/'common/pop_jobs/04_gestalt_jobs.txt')==h.sha256(run/'native-third-postannual-04_gestalt_jobs.txt')=='9469c178efbaa2d8e5bce43545ee6d5a184ee0e764336e85170795d0cc6820ad')

passed = all(checks.values())
details = {i: {'owned_by_player': i in ao, 'owned_by_country1': i in enemy_owned,
               'position': q.scalars(q.block(q.block(afl[str(i)], 'movement_manager'), 'coordinate')),
               'ships': q.ids(q.block(afl[str(i)], 'ships')), 'combat_with': combat(afl[str(i)]),
               'ship_states': {sid: q.scalars(ash[str(sid)]) for sid in q.ids(q.block(afl[str(i)], 'ships'))}}
           for i in set(ao) | {477, 825} if str(i) in afl and (i in am or i in {477, 825})}
proof = {'status': 'PASS_TERRAVORE_NATIVE_WAR1_POSTBATTLE_MIA_OBSERVATION_COMPONENT' if passed else 'FAIL',
         'checks': checks, 'before_sha256': b['save_sha256'], 'after_sha256': a['save_sha256'], 'date': a['date'],
         'days': days, 'actual_naval_cache':str(actual_naval_cache), 'actual_military_object_naval_size':5*len(current_ships), 'actual_naval_death_cache_credit':str(naval_death_credit), 'actual_pending_destroyed_ship_ids':sorted(current_pending_dead), 'actual_prior_pending_destroyed_ship_ids':sorted(prior_pending_dead), 'actual_alive_military_ship_ids':sorted(set(current_ships)-current_pending_dead), 'actual_confirmed_paid_dead_ids':sorted(cumulative_paid_lost|current_pending_dead), 'pending_death_cleanup_max_days':1 if current_pending_dead else None, 'actual_owned_military': am, 'cumulative_original_lost': sorted(cumulative_original_lost),
         'cumulative_paid_lost': sorted(cumulative_paid_lost), 'all_observed_paid_ship_ids': sorted(observed_paid),
         'actual_base0_ship_state': q.scalars(ash['0']), 'actual_new_paid_ships': added_ships,
         'actual_lost_military_requires_separate_combat_evidence': lost_ships, 'remaining_paid_orders': aids,
         'front_order_progress': [q.scalars(ai[str(i)])['progress'] for i in aids[:2]],
         'actual_fleet_details': details, 'actual_active_owned_combat': active, 'actual_pending': pending,
         'actual_mother_population': a['colonies']['0']['actual_pop_sum'], 'actual_colonization_population': colony['actual_pop_sum'], 'actual_colony1085_complete':checks['same_native_colony37_1085_completed_owned_founder73_original_hive_structure'], 'native_colony1085_completion_evidence':colony_end_evidence,
         'actual_third_situations':third_sits,'actual_third_expected_progress':third_expected_progress,'actual_third_elapsed_days':third_elapsed,'actual_clear_order_id':1224736779,'actual_clear_progress':120,'actual_endpoint_nets': {k: str(v) for k, v in nets.items()}, 'actual_stockpiles': ac['effective_stockpile'],
         'actual_war1': q.scalars(war), 'native_finished_battle_evidence':end_evidence, 'short_idle_war_calendar_ready':passed and not pending, 'actual_platform_order_ids':platform_after_ids, 'actual_platform_order_progress':[q.scalars(ai[str(i)])['progress'] for i in platform_after_ids], 'actual_built_paid_platform_ids':owned_platform_refs[-1], 'actual_new_paid_platform_ids':new_platforms, 'actual_platform_states':platform_actual, 'actual_platform_consumed_work':str(platform_after_work), 'native_platform_completion_sources':platform_sources, 'actual_completed_platform_handle_states':platform_completed_handle_evidence, 'actual_mine_order_ids':mine_after_ids, 'actual_mine_order_progress':[q.scalars(ai[str(i)])['progress'] for i in mine_after_ids], 'actual_paid_mines_completed':mine_completed_after, 'actual_completed_mine_handle_states':mine_handle_evidence, 'native_mine_completion_evidence':mine_completion_evidence, 'actual_coherent_appended_reports':coherent_appended_reports, 'actual_cumulative_weapon_aggregate_evidence':weapon_aggregate_evidence, 'actual_rear_upgrade_progress':str(rear_after_work), 'actual_rear_starport_complete':rear_after_done, 'actual_rear_station_state':q.scalars(ash['67109591']), 'native_rear_completion_evidence':rear_end_evidence, 'actual_missing_enemy825':missing_enemy, 'actual_menace_delta':str(menace_delta), 'native_menace_sources':source_bindings, 'calendar_ready': False, 'short_combat_calendar_ready': passed and not pending,
         'actual_yomon_constructor_order_raw':yomon_orders[-1], 'actual_yomon_constructor_order':q.scalars(yomon_orders[-1]), 'actual_yomon_constructor_position':q.scalars(q.block(q.block(afl['2'],'movement_manager'),'coordinate')), 'actual_yomon_outpost_complete':checks['yomon_paid_outpost_actual_base158_fleet849_ship1931_full_owned_empty_queues_constructor_idle'], 'native_yomon_completion_evidence':yomon_end_evidence, 'actual_yomon_station_state':yomon_station_state, 'native_leader_error_evidence':leader_error_evidence, 'scope': 'Yomon original paid outpost physically completed, with exact base158/fleet849/ship1931 ownership chain and materialized design clone; planet523 remains uncolonized. Exact documented native leader.1 trait rejection baseline retained; only leader.13 has prior no-Mod runtime reproduction. Only bounded native postbattle observation while war1 remains active and enemy825 is in emergency FTL, with paid reinforcements/colonization/three paid mining orders with exact native completion accounting, one paid rear starport completed and two paid native platforms with exact completion accounting, with exact native naval cache credit from proven removed deaths and killed-pending-object versus alive and removed-loss accounting; any killed pending objects require one next native day and complete cleanup. Remote capture is retained, Native colony1085 completed and third native consume active before its first annual bite, with one paid clearing order still queued behind the remaining mines and temporary negative E/A monthly nets explicitly recorded; no annual safety, victory, monthly-ledger recovery or full-route claim.'}
proof.update(actual_colony523_order_id=16777256,actual_colony523_order_progress=str(colony523_work[1]),actual_heavy_order_id=16777257,actual_heavy_order_progress=0)
proof['scope']='Bounded native pre-first-bite Terravore observation: original military losses, paid mines/platforms/rear/outpost, colony1085 third devour, clear272 working, colony523 ship1.33/day still building and heavy conversion0 queued. No victory, economic recovery, colony523 completion or full-route claim.'
proof['actual_enemy825_returned']=checks['native_enemy825_actually_returned_same_positive12_no_new_kills_or_menace']
proof['scope']='Bounded native observation after actual enemy825 return, original12 alive and war1 ongoing. Three paid mines, active third devour, clear272 working, colony523 still building1.33/day and heavy conversion0 queued; no victory, economy recovery or full-route claim.'
proof['actual_clear_complete']=clear_done_pair[-1]
proof['scope']='Bounded native observation after clear272 completion and actual enemy return; heavy conversion still0 and original buildings/jobs held, colony523 still1.33/day. No heavy completion, economic recovery, victory or full-route claim.'
proof['actual_heavy_order_progress']=str(heavy_work[-1])
proof['scope']='Bounded native observation: clear272 completed, heavy conversion1.4/day still building with original buildings/jobs held, colony5231.33/day, third devour before first annual bite, enemy825 returned and war1 ongoing. No heavy completion, economic recovery, victory or full-route claim.'
proof['actual_source_job_states']={i:a['pop_jobs'][i] for i in ['812','813','814']}
proof['scope']='Bounded pre-first-annual-bite native observation with source population100..300: coordinator fills first200, patrol fills next100, logistics0. Clear272 complete, heavy1.4/day and colony5231.33/day still building; original military/EEP checks retained. No completed economy, victory or full-route claim.'
proof['actual_source_devastation']=a['planets']['1085']['bombardment_damage']
proof['scope']='Bounded after-first-annual-consume before-second-annual native observation: exact original two devastation deposits/cooldown date, monotone recovery<=20,source100..300 original hive/capital/jobs; original military/EEP/PSI/clear complete and both paid civilian orders strictly before completion. Research monthly tick first-next-day anchored; no full route or economic recovery claim.'
proof['actual_colony523_ship_complete']=colony523_done[-1]
proof['actual_colony523_ship_state']=colony523_ship_states[-1]
proof['actual_colony523_fleet_state']=colony523_fleet_states[-1]
proof['scope']='Bounded native after-first-annual before-second-annual observation: paid colony523 ship born once and normal reachable colonize order in transit, target still uncolonized. Heavy conversion strictly before completion; original military/EEP/PSI/source/clear bounds retained. No arrival, economic recovery or full-route claim.'
proof['scope']='Bounded first-annual native observation with source100..500 original three jobs capacity and actual employment conservation; patrol/logistics allocation remains native and original negative-amenities factor10 reallocation anchored. One paid colony523 ship in transit, heavy before completion; original military/EEP/PSI/error retained. Capacity bound is not evidence of a500-pop test; no full route or economic recovery.'
out = run / (after + '-war1-battle-v44-proof.json')
assert not out.exists()
h.write_json(out, proof)
print(json.dumps({'status': proof['status'], 'checks': len(checks), 'failed': [k for k, v in checks.items() if v is not True],
                  'pending': pending, 'killed_pending_cleanup':sorted(current_pending_dead), 'alive_military':len(set(current_ships)-current_pending_dead), 'naval_death_cache_credit':str(naval_death_credit), 'new_paid_ships': added_ships, 'remaining_orders': len(aids),
                  'short_combat_calendar_ready': proof['short_combat_calendar_ready']}), flush=True)
assert passed, 'Original war1 observation FAIL retained; no repeated calendar'
