"""Documented bounded native construction/economy checks before September completion."""
import json, logging, re, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path[:0] = ['eat_everything_origin/tools','_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r, audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run/n).read_text('utf-8'))
omit = lambda t,ks: [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
objects = lambda t: {k:v for k,v,o in q.fields(t) if o}

def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:
        fields=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'), fields, {k:v for k,v,o in fields if o}
def ordinal(s):
    y,m,d=map(int,s.split('.'));return y*360+(m-1)*30+d-1
def owned(c):
    return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets'))))
def fleetships(fleets,ids,military=False):
    return {i for fid in ids if not military or q.scalars(fleets[str(fid)]).get('ship_class')=='shipclass_military' for i in q.ids(q.block(fleets[str(fid)],'ships'))}
def construction(t):
    c=t['construction']
    return objects(q.block(q.block(c,'queue_mgr'),'queues')),objects(q.block(q.block(c,'item_mgr'),'items'))
def research_queue(t,key):
    raw=q.block(t,key);ts=list(q.tokens(raw))
    if not ts:return {}
    assert ts[0][0]=='{' and ts[-1][0]=='}'
    return q.scalars(raw[ts[0][2]:ts[-1][1]])
b,bf,br=read(before);a,af,ar=read(after)
bc,ac=b['countries']['0'],a['countries']['0']
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bfl,afl=[objects(t['fleet']) for t in [br,ar]]
bsh,ash=[objects(t['ships']) for t in [br,ar]]
bo,ao=owned(bcr),owned(acr)
bm,am=fleetships(bfl,bo,True),fleetships(afl,ao,True)
ob,oa=ordinal(b['date']),ordinal(a['date']);days=oa-ob
validate_native_interval(b['date'],a['date'],days)
mt=sum(i%30==0 for i in range(ob+1,oa+1))
rt=sum(i%30==1 for i in range(ob+1,oa+1))
first=before=='terravore-third-settlement-native'
v2_transition=before=='terravore-post-settlement-research-day' and after=='terravore-post-settlement-month-end'
original='terravore-third-post-settlement-month'
cal=load(after+'-calendar-receipt.json') if not first else None
ce=load(after+'-calendar-execution.json') if not first else None
pre=load(cal['prior_proof_file']) if cal else load('terravore-third-settlement-native-third-settlement-proof.json')
pe=load(cal['prior_execution_stage']+'-execution.json') if cal else load('terravore-third-settlement-native-observer-fullpath-execution.json')
observation=load(after+'-post-settlement-observation.json') if first else None
oe=load(after+'-observation-execution.json') if first else None

def chain_ok():
    return (before=='terravore-rear-colonizer-prebirth' and after=='terravore-rear-colonizer-born' and days==1
        and pre['status']=='PASS_NATIVE_TERRAVORE_REAR_COLONIZER_PREBIRTH_COMPONENT' and len(pre['checks'])==43 and pre['rear_colonizer_birth_single_day_ready'] is True and pre['maximum_days_to_birth_boundary']==1
        and pe['helper_sha256']==h.sha256(run/'priority_terravore_rear_colonizer_prebirth_observer.py')=='dde54966736f25b1f47afb0d10489aeb5d9506c4ad6bcb8c4f3bb94e5c01aac5'
        and cal['status']=='CALENDAR_CONFIRMED' and cal['days']==1 and cal['start_date']==b['date']=='2272.09.12' and cal['date']==a['date']=='2272.09.13'
        and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc')

cb,ca=b['colonies']['0'],a['colonies']['0']
mb,ma=b['planets']['7'],a['planets']['7']
sp,sa=b['planets']['1085'],a['planets']['1085']
growth_raw=q.block(q.block(ar['colony'],'0'),'last_month_growth_data')
growth=q.scalars(q.block(growth_raw,'growth_and_size'))
growth_details=[(k,q.unquote(v),o) for k,v,o in q.fields(q.block(growth_raw,'current_month_growth_details'))]
new_growth=ca['actual_pop_sum']-cb['actual_pop_sum']
def population_ok():
    if first:
        return (new_growth==7 and cb['actual_pop_sum']==11123 and ca['actual_pop_sum']==11130
            and growth=={'month_start_size':10834,'growth':296}
            and growth_details==[('key','GROWTH_CAT_GROWTH',False),('value',7,False),('key','GROWTH_CAT_OTHER',False),('value',289,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)]
            and growth['month_start_size']+growth['growth']==ca['actual_pop_sum'])
    if not mt:return new_growth==0
    return (growth=={'month_start_size':cb['actual_pop_sum'],'growth':new_growth} and new_growth==7
        and growth_details==[('key','GROWTH_CAT_GROWTH',False),('value',7,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)])
keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in keys}
stocks=set(bc['effective_stockpile'])|set(ac['effective_stockpile'])
delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in stocks}
residual={k:delta.get(k,D(0))-net[k]*mt for k in keys}
bt,at=bc['tech_status'],ac['tech_status']
beng,aeng=[research_queue(t,'engineering_queue') for t in [bt,at]]
science={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bank_delta={k:D(str(ac['research_stockpile'].get(k,0)))-D(str(bc['research_stockpile'].get(k,0))) for k in q.RESEARCH_RESOURCES}
bqs,bi=construction(br);aqs,ai=construction(ar)
country_timers=['entered_war_as_defender','recent_first_contact_process_started','recent_cara_3010','discovered_site','was_recently_targeted_by_voidworms']
def timers_ok():
    old,new=[q.block(c,'flags') for c in [bcr,acr]]
    return (omit(old,set(country_timers+(['eep_notice_pending'] if first else [])))==omit(new,set(country_timers))
        and all(omit(q.block(old,k),{'flag_days'})==omit(q.block(new,k),{'flag_days'}) and q.scalars(q.block(old,k))['flag_days']-q.scalars(q.block(new,k))['flag_days']==days and q.scalars(q.block(new,k))['flag_days']>0 for k in country_timers))
def modules_ok():
    old,new=[q.block(c,'modules') for c in [bcr,acr]]
    ev=[q.block(v,'standard_event_module') for v in [old,new]];de=[q.block(v,'delayed_event') for v in ev]
    return (omit(old,{'standard_event_module','standard_economy_module'})==omit(new,{'standard_event_module','standard_economy_module'})
        and omit(q.block(old,'standard_economy_module'),{'resources'})==omit(q.block(new,'standard_economy_module'),{'resources'})
        and omit(ev[0],{'delayed_event'})==omit(ev[1],{'delayed_event'}) and omit(de[0],{'days'})==omit(de[1],{'days'})
        and q.scalars(de[0])['event']==q.scalars(de[1])['event']=='paragon.999' and q.scalars(de[0])['days']-q.scalars(de[1])['days']==days)
def projects_ok():
    old,new=[q.block(c,'events') for c in [bcr,acr]]
    ps=[{q.scalars(v)['id']:v for k,v,o in q.fields(t) if k=='special_project' and o} for t in [old,new]]
    return (ps[0].keys()==ps[1].keys() and {4,5}<=ps[1].keys()
        and omit(old,{'special_project','situations'})==omit(new,{'special_project','situations'})
        and not q.ids(q.block(new,'situations'))
        and all(ps[0][i]==ps[1][i] if i not in [4,5] else omit(ps[0][i],{'days_left'})==omit(ps[1][i],{'days_left'}) and q.scalars(ps[0][i])['days_left']-q.scalars(ps[1][i])['days_left']==days and q.scalars(ps[1][i])['days_left']>0 for i in ps[0]))
pending=lambda fs:[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
messages=lambda fs:[v for k,v,o in fs if k=='message' and o and q.scalars(v).get('receiver')==0]
foundation=load('terravore-rear-clearing-first-born-calibration-war1-battle-v65-proof.json')
expected_vars=dict(bc['variables'],eep_crisis=1) if first else bc['variables']
expected_flags={k:v for k,v in bc['flags'].items() if k!='eep_notice_pending'} if first else bc['flags']
expected_mvars=dict(mb['variables'],eep_actual_pop=11123,eep_free_districts=3) if first else mb['variables']
def military_ok():
    for i in bm:
        old,new=bsh[str(i)],ash[str(i)];os,ns=q.scalars(old),q.scalars(new)
        if i!=1916:
            if old!=new:return False
        elif not (omit(old,{'hitpoints','armor_hitpoints'})==omit(new,{'hitpoints','armor_hitpoints'})
            and all(0<D(str(os[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')])):return False
    return True
def fleets_ok():
    return all(bfl[str(i)]==afl[str(i)] if i!=83886903 else omit(bfl[str(i)],{'diplomacy_weight','hit_points','military_power'})==omit(afl[str(i)],{'diplomacy_weight','hit_points','military_power'}) for i in bo)
blocker_file=run/'native-blocker-clear-01_blocker_deposits.txt'
blockers=blocker_file.read_text('utf-8-sig')
planet_deps=[a['deposits'][str(i)]['type'] for i in ma['deposits']]
blocked=sum(q.scalars(q.block(q.block(blockers,t),'planet_modifier')).get('planet_max_districts_add',0) for t in planet_deps)

def original_dead_entry_fail_ok():
    if not first:return len(pre['checks'])==(42 if v2_transition else 43)
    proof=load(after+'-post-settlement-build-proof.json');execution=load(after+'-build-observer-execution.json')
    inv_path=run/(after+'-original-colonizer-target-investigation.json');inv=load(inv_path.name)
    return (proof['status']=='FAIL' and len(proof['checks'])==41 and [k for k,v in proof['checks'].items() if v is not True]==['original_colonizer_death_and_target523_held']
        and execution['returncode']==1 and execution['helper_sha256']==h.sha256(run/'priority_terravore_post_settlement_build_observer.py')=='9e3d6d6c6a631319a0ac2977f60a8d9dac80ccb060d0501687027f162d42896e'
        and proof['before_sha256']==inv['before_sha256']==b['save_sha256'] and proof['after_sha256']==inv['after_sha256']==a['save_sha256']
        and h.sha256(inv_path)=='f17c37fb575bcc0a8651606e78b8061dee8c76389f2233274444135b1f1893f9'
        and inv['before_ship_entry']==[['none',False]] and inv['after_ship_entry']==[] and inv['before_fleet_entry']==inv['after_fleet_entry']==[['none',False]]
        and inv['target523_before']==inv['target523_after']==q.block(q.block(ar['planets'],'planet'),'523'))

def history_entries(raw):
    out=[];depth=0;start=0;selected=q.block(raw,'selected')
    for token,x,y in q.tokens(selected):
        if token=='{':
            if depth==0:start=y
            depth+=1
        elif token=='}':
            depth-=1
            if depth==0:out.append(selected[start:x])
    assert depth==0;return out
bh,ah=[history_entries(t['open_player_event_selection_history']) for t in [br,ar]]
def history_ok():
    return (ah[:len(bh)]==bh and omit(br['open_player_event_selection_history'],{'selected'})==omit(ar['open_player_event_selection_history'],{'selected'})
        and all(q.scalars(v).get('human')==-1 and isinstance(q.scalars(v).get('player_event'),int) and q.scalars(v)['player_event']>0 and isinstance(q.scalars(v).get('option'),int) and q.scalars(v)['option']>=0 and len(list(q.fields(v)))==3 and all(not obj for k,x,obj in q.fields(v)) for v in ah[len(bh):]))
def original_history_fail_ok():
    if not v2_transition:return len(pre['checks'])==43
    proof=load(after+'-post-settlement-build-v2-proof.json');execution=load(after+'-build-observer-v2-execution.json')
    inv_path=run/(after+'-global-nonmanual-history-investigation.json');inv=load(inv_path.name)
    old,new=[inv[st] for st in [before,after]]
    return (proof['status']=='FAIL' and len(proof['checks'])==42 and [k for k,v in proof['checks'].items() if v is not True]==['government_traditions_AP_and_manual_history_held']
        and execution['returncode']==1 and execution['helper_sha256']==h.sha256(run/'priority_terravore_post_settlement_build_observer_v2.py')=='18f7285afd6945f918bc558914b57f174ee845d4bb63a5c80f828a2d737eae29'
        and old['save_sha256']==proof['before_sha256']==b['save_sha256'] and new['save_sha256']==proof['after_sha256']==a['save_sha256']
        and h.sha256(inv_path)=='07f811343f99a22c4d360ed6dbb71e6e3c1530565e842677af1198fa16e64f13'
        and old['history_raw']==br['open_player_event_selection_history'] and new['history_raw']==ar['open_player_event_selection_history']
        and len(bh)==247 and len(ah)==248 and [q.scalars(v) for v in ah[len(bh):]]==[{'player_event':269,'human':-1,'option':0}])


completion_observation=load(after+'-construction-boundary-observation.json');completion_execution=load(after+'-boundary-observation-execution.json')
inv_path=run/(after+'-rear97-native-inventory.json');inv=load(inv_path.name);inventory_execution=load(after+'-rear97-native-inventory-execution.json')
co,cn=completion_observation['before_state'],completion_observation['after_state'];ei,ej=inv[before],inv[after]

def enemy_health_ok(i):
    expected={'33556209':{'hitpoints':(522.64241,472.49126)},'67109342':{'armor_hitpoints':(625,65.69158)}}
    old,new=q.scalars(ei['enemy825_ships_raw'][i]),q.scalars(ej['enemy825_ships_raw'][i])
    return all((old.get(k,0),new.get(k,0))==expected[i][k] if k in expected.get(i,{}) else old.get(k,0)==new.get(k,0) for k in ['hitpoints','armor_hitpoints','shield_hitpoints'])

def observation_ok():
    return (completion_observation['status']=='OBSERVED_NATIVE_TERRAVORE_CONSTRUCTION_BOUNDARY' and len(completion_observation['checks'])==6 and all(v is True for v in completion_observation['checks'].values())
        and completion_execution['returncode']==0 and completion_execution['helper_sha256']==h.sha256(run/'priority_terravore_construction_boundary_observation.py')=='e72511912b5a1a1e363384e3aca20b44d329a80c2b0c6f8e5bcbff2758549678'
        and h.sha256(run/(after+'-construction-boundary-observation.json'))=='72355e3299ed41093d6c447dd803872e6c566d2ace171edc8ae715f33b46e9ed'
        and completion_observation['before_sha256']==ei['save_sha256']==b['save_sha256'] and completion_observation['after_sha256']==ej['save_sha256']==a['save_sha256']
        and h.sha256(inv_path)=='066450968b93e34b99d836080b3bf7343848c5b24ad153a9c8220e205292a55d'
        and all(v['audit']==audit and v['country0_raw']==raw for v,audit,raw in [(co,b,bcr),(cn,a,acr)]))

def combat_military_ok():
    for i in bm:
        old,new=bsh[str(i)],ash[str(i)];os,ns=q.scalars(old),q.scalars(new)
        if i==117441817:
            if not(old==co['owned_ships_raw'][str(i)] and new==cn['owned_ships_raw'][str(i)] and q.block(old,'ship_design_implementation')==q.block(new,'ship_design_implementation')
                and ns['fleet']==16778073 and os['hitpoints']==ns['max_hitpoints']==270 and ns['hitpoints']==263.7738 and ns['max_armor_hitpoints']==250 and os['armor_hitpoints']==246.8308 and ns.get('armor_hitpoints',0)==0 and os.get('shield_hitpoints',0)==ns.get('shield_hitpoints',0)==0 and ns['last_combat_activity']=='2272.09.13'):return False
        elif i==1916:
            if not(omit(old,{'hitpoints','armor_hitpoints'})==omit(new,{'hitpoints','armor_hitpoints'}) and all(0<D(str(os[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')])):return False
        elif old!=new:return False
    return True

def combat_station_ok():
    i='67109591';old,new=bsh[i],ash[i];os,ns=q.scalars(old),q.scalars(new)
    return (old==co['owned_ships_raw'][i] and new==cn['owned_ships_raw'][i] and q.block(old,'ship_design_implementation')==q.block(new,'ship_design_implementation')
        and ns['fleet']==804 and 804 in ao and 67109591 in q.ids(q.block(afl['804'],'ships')) and q.scalars(ej['rear153_raw'])['station']==67109591
        and ns['hitpoints']==ns['max_hitpoints']==18300 and ns['armor_hitpoints']==ns['max_armor_hitpoints']==5125 and os['shield_hitpoints']==4257.8562 and ns['shield_hitpoints']==4187.4972
        and all(bsh[str(j)]==ash[str(j)] for j in fleetships(bfl,bo)-bm-{1,67109591}))

def combat_fleets_ok():
    return all(bfl[str(i)]==co['owned_fleets_raw'][str(i)] and afl[str(i)]==cn['owned_fleets_raw'][str(i)] if i in [804,16778073] else bfl[str(i)]==afl[str(i)] if i!=83886903 else omit(bfl[str(i)],{'diplomacy_weight','hit_points','military_power'})==omit(afl[str(i)],{'diplomacy_weight','hit_points','military_power'}) for i in bo)

def combat_enemy_ok():
    ids=ei['enemy825_ship_ids']
    return (ids==ej['enemy825_ship_ids'] and len(ids)==12 and ei['enemy825_country1_owned'] is ej['enemy825_country1_owned'] is True
        and all(q.block(t['fleet'],'825')==e['enemy825_raw'] and all(q.block(t['ships'],str(i))==e['enemy825_ships_raw'][str(i)] for i in ids) and q.block(q.block(t['starbase_mgr'],'starbases'),'153')==e['rear153_raw'] for t,e in [(br,ei),(ar,ej)])
        and omit(ei['rear153_raw'],{'orbitals'})==omit(ej['rear153_raw'],{'orbitals'}) and q.scalars(q.block(ei['rear153_raw'],'orbitals'))=={'0':4294967295} and q.scalars(q.block(ej['rear153_raw'],'orbitals'))=={'0':33555278} and q.scalars(ej['rear153_raw'])['shipyard_build_queue']==2287
        and all(q.block(ei['enemy825_ships_raw'][str(i)],'ship_design_implementation')==q.block(ej['enemy825_ships_raw'][str(i)],'ship_design_implementation') and enemy_health_ok(str(i)) for i in ids)
        and all(q.scalars(q.block(q.block(e['enemy825_raw'],'movement_manager'),'coordinate'))['origin']==97 for e in [ei,ej])
        and all({int(i):q.ids(q.block(q.block(fs[str(i)],'combat'),'in_combat_with')) for i in own if q.ids(q.block(q.block(fs[str(i)],'combat'),'in_combat_with'))}==expect for fs,own,expect in [(bfl,bo,{804:[825],16778073:[825]}),(afl,ao,{804:[825],16778073:[825],33555278:[825]})])
        and set(q.ids(q.block(q.block(ei['enemy825_raw'],'combat'),'in_combat_with')))=={804,16778073} and set(q.ids(q.block(q.block(ej['enemy825_raw'],'combat'),'in_combat_with')))=={804,16778073,33555278}
        and q.block(q.block(br['war'],'1'),'battles')==q.block(q.block(ar['war'],'1'),'battles'))


payment_path=run/'terravore-rear-colonizer2-paid-rear-colonizer2-payment-v2-proof.json';payment=load(payment_path.name);payment_execution=load('terravore-rear-colonizer2-paid-payment-guard-v2-execution.json')
def new_paid_colonizer_ok():
    i='50333369';fid='33555278';new=ash[i];ns=q.scalars(new);fleet=afl[fid];build=q.block(bi['83886124'],'buildable_colony_ship')
    return (i not in bsh and fid not in bfl and new==cn['owned_ships_raw'][i] and fleet==cn['owned_fleets_raw'][fid] and ns['fleet']==33555278 and q.ids(q.block(fleet,'ships'))==[50333369]
        and list(q.fields(q.block(new,'ship_design_implementation')))==list(q.fields(q.block(build,'ship_design_implementation'))) and q.scalars(q.block(new,'ship_design_implementation'))=={'design':150995039,'upgrade':4294967295,'growth_stage':0}
        and q.scalars(q.block(new,'colonization_data'))==q.scalars(q.block(build,'colonization_data'))=={'species':73} and q.scalars(q.block(build,'orbitable'))=={'starbase':153}
        and q.block(br['ship_design'],'150995039')==q.block(ar['ship_design'],'150995039') and 'ship_size="colonizer"' in q.block(ar['ship_design'],'150995039')
        and ns['hitpoints']==ns['max_hitpoints']==625 and ns['armor_hitpoints']==ns['max_armor_hitpoints']==125 and ns['shield_hitpoints']==ns['max_shield_hitpoints']==320 and ns['construction_date']==a['date']=='2272.09.13'
        and q.scalars(q.block(new,'coordinate'))=={'x':18.95,'y':-20.95,'origin':97} and q.scalars(q.block(q.block(fleet,'movement_manager'),'coordinate'))=={'x':18.95,'y':-20.95,'origin':97}
        and q.scalars(q.block(q.block(q.block(fleet,'movement_manager'),'orbit'),'orbitable'))=={'starbase':153}
        and q.scalars(fleet)['ship_class']=='shipclass_colonizer' and q.scalars(fleet)['fleet_stance']=='evasive' and not q.block(fleet,'current_order')
        and q.scalars(q.block(fleet,'combat'))['start_date']=='2272.09.13' and q.ids(q.block(q.block(fleet,'combat'),'in_combat_with'))==[825])

def colonizer_order_retired_ok():
    return (q.ids(q.block(bqs['2287'],'items'))==[83886124] and not q.ids(q.block(aqs['2287'],'items')) and q.scalars(bi['83886124'])['progress']==359.1 and q.scalars(bi['83886124'])['progress_needed']==360
        and q.scalars(q.block(bi['83886124'],'resources'))=={'minerals':375,'alloys':150} and [(v,o) for k,v,o in q.fields(q.block(q.block(ar['construction'],'item_mgr'),'items')) if k=='83886124']==[('none',False)])

def owned_queues_birth_ok():
    old={k:v for k,v in bqs.items() if q.scalars(v).get('owner')==0};new={k:v for k,v in aqs.items() if q.scalars(v).get('owner')==0}
    return old.keys()==new.keys() and all(omit(old[k],{'items'})==omit(new[k],{'items'}) if k=='2287' else old[k]==new[k] for k in old)


original_proof=load(after+'-birth-proof.json');original_execution=load(after+'-observer-execution.json');correction_path=run/(after+'-design-indent-and-base-completion-investigation.json');correction=load(correction_path.name)
def original_two_fail_anchor_ok():
    return (original_proof['status']=='FAIL' and len(original_proof['checks'])==45 and [k for k,v in original_proof['checks'].items() if v is not True]==['unique_paid_colonizer_birth_species73_original_design_full_health_position_owner_combat','fixed_rear97_enemy12_precise_damage_new_civilian_combat_no_war_result']
        and original_execution['returncode']==1 and original_execution['helper_sha256']==h.sha256(run/'priority_terravore_rear_colonizer_birth_observer.py')=='89a7857dffe2eada9b22c5b992cca8399b7100b9d1711023db6f8436293323cd'
        and original_proof['before_sha256']==correction['before_sha256']==b['save_sha256'] and original_proof['after_sha256']==correction['after_sha256']==a['save_sha256']
        and h.sha256(correction_path)=='341f9b356ce27511c70bfa732c951c3821228565d44091fc682c37dea8d137c7' and correction['implementation_fields_equal'] is True
        and correction['base_before_raw']==ei['rear153_raw'] and correction['base_after_raw']==ej['rear153_raw'] and list(correction['base_changes'])==['orbitals'])

checks={
 'original45_two_FAIL_actual1_full_indent_and_native_orbitals_anchor':original_two_fail_anchor_ok(),
 'original375M150A_payment17_PASS_actual0_proof_source_anchor':payment['status']=='PASS_TERRAVORE_NATIVE_REAR_COLONIZER2_PAYMENT_COMPONENT' and len(payment['checks'])==17 and all(v is True for v in payment['checks'].values()) and h.sha256(payment_path)=='7766c4ebf92d38c9b9177c0a117c2e5b7b3f37dab06ef10add902b60055db994' and payment_execution['returncode']==0 and payment_execution['helper_sha256']==h.sha256(Path(payment_execution['command'][1])),
 'unique_paid_colonizer_birth_species73_original_design_full_health_position_owner_combat':new_paid_colonizer_ok(),
 'prior_prebirth43_all_PASS_actual0_source_and_ready':chain_ok(),
 'current_observation6_and_native_inventory4_actual0_original_SHA':observation_ok() and inv["status"]=="OBSERVED_NATIVE_TERRAVORE_REAR97_INVENTORY" and len(inv["checks"])==4 and all(v is True for v in inv["checks"].values()) and inventory_execution["returncode"]==0 and inventory_execution["helper_sha256"]==h.sha256(run/"priority_terravore_rear97_native_inventory.py")=="ac2936be649be907434072d4c72be139cf81d6faf801361345af95b5678a8df6",
 'original_interval_chain_or_precise_failed_OCR_recovery':chain_ok(),
 'prior_all_PASS_actual0_original_SHA_and_source':all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(Path(pe['command'][1])) and pre['after_sha256']==b['save_sha256'],
 'single_birth_day_no_month_or_research_tick':days==1 and mt==rt==0 and b['date']=='2272.09.12' and a['date']=='2272.09.13',
 'original_SAV_SHA_pair':all(x['save_sha256']==h.sha256(run/(st+'.sav')) for st,x in [(before,b),(after,a)]),
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'true_resources_only_native_month_net_no_repeat_rewards':all(abs(residual[k])<=D('0.00005') for k in keys if k not in ['trade','influence']) and all(delta[k]==0 for k in stocks-set(keys)-set(q.RESEARCH_RESOURCES)) and all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap for k,cap in [('trade',50000),('influence',1000)]),
 'native_budget_month_roll_or_held_between_months':ac['budget_categories']['last_month']==bc['budget_categories']['current_month'] if mt else bc['budget_categories']==ac['budget_categories'],
 'positive_native_energy_minerals_alloys_unity_net':all(net[k]>0 for k in ['energy','minerals','alloys','unity']),
 'research_true_P_S_banks_only_native_tick_Eng_bank0':all(abs(bank_delta[k]-science[k]*D('1.33')*rt)<=D('0.00005') for k in ['physics_research','society_research']) and bank_delta['engineering_research']==0,
 'only_original_mass_drivers3_progress_no_new_completed_tech':omit(bt,{'stored_techpoints','engineering_queue'})==omit(at,{'stored_techpoints','engineering_queue'}) and {k:v for k,v in beng.items() if k!='progress'}=={k:v for k,v in aeng.items() if k!='progress'} and beng['technology']==aeng['technology']=='tech_mass_drivers_3' and abs(D(str(aeng['progress']))-D(str(beng['progress']))-science['engineering_research']*D('1.33')*rt)<=D('0.00005'),
 'population_only_growth7_with_historic_migration289_once':population_ok(),
 'one_owned_colony_only_species73_source_empty':bc['owned_colonies']==ac['owned_colonies']==[0] and b['species']==a['species'] and sum(g['size'] for g in a['pop_groups'].values() if g['planet']==0 and g['key']['species']==73)==ca['actual_pop_sum'] and not any(g['planet']==37 and g['size']>0 for g in a['pop_groups'].values()),
 'housing_return_cache_refreshed_only_current_month_growth_lag':ca['total_housing']==14100 and ca['free_housing']==14100-ca['housing_usage'] and 0<=ca['actual_pop_sum']-ca['housing_usage']<=7 and ca['housing_usage']>=cb['housing_usage'] and (not mt or ca['housing_usage']==cb['actual_pop_sum']) and ca['actual_pop_sum']==ca['employable_pops']==ca['num_sapient_pops'] and ca['free_amenities']>0 and ca['crime']==0,
 'aligned_month_end_or_final_prebuild_housing_fully_refreshed':not (a['date'].endswith('.30') or a['date']=='2272.09.10') or ca['housing_usage']==ca['actual_pop_sum'],
 'report_only_expected_snapshot_C49_D14_worlds3_held':ac['variables']==expected_vars and all(ac['variables'][k]==v for k,v in {'eep_c':49,'eep_d':14,'eep_worlds':3,'eep_psi':1,'eep_g':0,'eep_made':0,'eep_delta':0,'eep_stage':1,'eep_fleet_stage':0}.items()),
 'monthly_pending_notice_cleared_no_new_Queen_flags':ac['flags']==expected_flags and 'eep_notice_pending' not in ac['flags'],
 'unique_owned_core18_capacity14_original_deposit_and_modifier':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and ma['owner']==ma['controller']==ma['colony']==0 and ma['planet_size']==18 and ma['modifiers']==mb['modifiers'] and ma['deposits']==mb['deposits'] and ma['flags']==mb['flags'] and ma['variables']==expected_mvars and a['deposits']['1573']==b['deposits']['1573'],
 'report_free3_independent_two_native_capacity_blockers':blocked==-2 and all(planet_deps.count(t)==1 and q.scalars(q.block(q.block(blockers,t),'planet_modifier'))['planet_max_districts_add']==-1 for t in ['d_failing_infrastructure','d_ruined_district']) and ma['variables']['eep_free_districts']==18+14-27+blocked==3,
 'paid_districts7_15_5_completed_physics_zone_and_all_buildings_held':br['districts']==ar['districts'] and br['zones']==ar['zones'] and br['buildings']==ar['buildings'] and q.scalars(q.block(ar['zones'],'16777323'))['type']=='zone_research_physics',
 'mother_all_job_caps_held_technician1400':{i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in b['pop_jobs'].items() if j['planet']==0}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in a['pop_jobs'].items() if j['planet']==0} and len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['max_workforce']==j['workforce_limit']==1400])==1,
 'source_shattered_unowned_cleaned_no_new_progress':sa['planet_class']=='pc_shattered' and 'owner' not in sa and 'controller' not in sa and sa['deposits']==[] and sa['modifiers']=='' and sa['variables']==sp['variables'] and sa['bombardment_damage']==sp['bombardment_damage'],
 'source_done_flags_held_only_two_cooldowns_minus_days':{k:v for k,v in sa['flags'].items() if k not in ['recently_eaten_planet','superior_colonies_can_be_boosted']}=={k:v for k,v in sp['flags'].items() if k not in ['recently_eaten_planet','superior_colonies_can_be_boosted']} and all(sp['flags'][k]['flag_date']==sa['flags'][k]['flag_date'] and sp['flags'][k]['flag_days']-sa['flags'][k]['flag_days']==days and sa['flags'][k]['flag_days']>0 for k in ['recently_eaten_planet','superior_colonies_can_be_boosted']),
 'dead_situation_removed_no_live_EEP_or_native_duplicate':not any(v.get('type') in ['situation_eep_devouring','situation_terravore_consume_planet'] for v in a['situations'].values()),
 'same_nemesis1_objectives_and_true_Menace885':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and ac['effective_stockpile']['menace']==885,
 'only_original_inactive264_pending_no_new_country_messages':pending(bf)==pending(af) and len(pending(af))==1 and q.scalars(pending(af)[0])=={'id':264,'event':'grand_archive.2800','date':'2273.12.20','country':0} and all(v in messages(bf) for v in messages(af)),
 'owned_collection_exactly_one_new_colonizer_fleet_original28_military_naval140':bo==[i for i in ao if i!=33555278] and set(ao)-set(bo)=={33555278} and fleetships(afl,ao)==fleetships(bfl,bo)|{50333369} and bm==am==set(foundation['actual_alive_military_ship_ids']) and len(am)==28 and q.scalars(acr)['fleet_size']==140,
 'all28_military_held_only_fixed_rear_damage_and1916_repair':combat_military_ok(),
 'all_fleets_held_except_fixed_rear97_combat_raw':combat_fleets_ok(),
 'science_only_orientation_and_bounded_native_shield_regen':omit(bsh['1'],{'rotation','forward_x','forward_y','shield_hitpoints'})==omit(ash['1'],{'rotation','forward_x','forward_y','shield_hitpoints'}) and D(str(q.scalars(ash['1'])['shield_hitpoints']))==min(D(320),D(str(q.scalars(bsh['1'])['shield_hitpoints']))+8*days),
 'rear_station_only_native_shield_damage_other_civilian_stations_held':combat_station_ok(),
 'fixed_rear97_enemy12_precise_damage_new_civilian_combat_no_war_result':combat_enemy_ok(),
 'original_colonizer_death_and_target523_held':all([(v,o) for k,v,o in q.fields(t[root]) if k==sid] in [[],[('none',False)]] for t in [br,ar] for root,sid in [('ships','16779140'),('fleet','16778062')]) and 16778062 not in ao and 16779140 not in fleetships(afl,ao) and q.block(q.block(br['planets'],'planet'),'523')==q.block(q.block(ar['planets'],'planet'),'523'),
 'same12_owned_defense_armies_no_free_transports':q.ids(q.block(bcr,'owned_armies'))==q.ids(q.block(acr,'owned_armies')) and len(q.ids(q.block(acr,'owned_armies')))==12,
 'completed_physics_order_remains_none_mother_queue_empty':all([(v,o) for k,v,o in q.fields(q.block(q.block(t['construction'],'item_mgr'),'items')) if k=='1258291211']==[('none',False)] for t in [br,ar]) and not q.ids(q.block(aqs['0'],'items')) and all(a['pop_jobs'][i]['max_workforce']==n for i,n in [('22',700),('23',780),('24',180),('25',180)]),
 'original_paid375M150A_colonizer_order_retired_none_queue_empty':colonizer_order_retired_ok(),
 'all_owned_queue_structures_held_only_colonizer_order_completed':owned_queues_birth_ok(),
 'five_country_native_timers_exact_days_only_notice_removed':timers_ok(),
 'only_native_paragon999_timer_and_economy_mirror_modules':modules_ok(),
 'only_known_debris_timers_and_removed_dead_situation':projects_ok(),
 'government_traditions_AP_and_manual_history_held':all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions']) and history_ok(),
}
passed=all(v is True for v in checks.values())
p={'status':'PASS_NATIVE_TERRAVORE_REAR_COLONIZER_BIRTH_IN_COMBAT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'days':days,'actual_alive_military_ship_ids':sorted(am),'actual_core_population':ca['actual_pop_sum'],'new_colonizer_ship':50333369,'new_colonizer_fleet':33555278,'colonizer_in_combat':True,'normal_colonization_route_ready':False,'scope':'Actual paid colonizer birth into native rear97 combat, full health and original design. No safe route, retreat availability, colonization, war victory or full acceptance.'}
out=run/(after+'-birth-v2-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':a['date'],'new_colonizer':50333369,'in_combat':True}),flush=True)
assert passed,'Original birth result retained; no calendar replay'
