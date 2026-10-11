"""Bounded documented interannual native component; no game actions."""
import json, logging, re, sys, zipfile
from decimal import Decimal as D
from pathlib import Path
before, after = sys.argv[1:]
sys.path[:0] = ['eat_everything_origin/tools', '_runtime/heart-of-devouring']
sys.argv = ['runtime']
import runtime as r, audit_save as q
from formal_production_native_calendar_checked_v2 import validate_native_interval
logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
load = lambda n: json.loads((run/n).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run/(stage+'.sav')) as z:
        fs = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage+'.audit.json'), fs, {k:v for k,v,o in fs if o}
def objects(t): return {k:v for k,v,o in q.fields(t) if o}
def omit(t, ks): return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def owned(c): return list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets'))))
def construction(t):
    c=t['construction']
    return objects(q.block(q.block(c,'queue_mgr'),'queues')), objects(q.block(q.block(c,'item_mgr'),'items'))
def research_queue(t,key):
    raw=q.block(t,key)
    ts=list(q.tokens(raw))
    if not ts:return {}
    assert ts[0][0]=='{' and ts[-1][0]=='}'
    return q.scalars(raw[ts[0][2]:ts[-1][1]])
def growth(t,i):
    raw=q.block(q.block(t['colony'],i),'last_month_growth_data')
    return q.scalars(q.block(raw,'growth_and_size')), [(k,q.unquote(v),o) for k,v,o in q.fields(q.block(raw,'current_month_growth_details'))]
b,bf,br=read(before);a,af,ar=read(after)
bc,ac=b['countries']['0'],a['countries']['0']
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
bfl,afl=[objects(t['fleet']) for t in [br,ar]]
bsh,ash=[objects(t['ships']) for t in [br,ar]]
bo,ao=owned(bcr),owned(acr)
def fleetships(fl,ids,military=False):
    return {i for fid in ids if not military or q.scalars(fl[str(fid)]).get('ship_class')=='shipclass_military' for i in q.ids(q.block(fl[str(fid)],'ships'))}
bm,am=fleetships(bfl,bo,True),fleetships(afl,ao,True)
def ship_ok(i):
    old,new=bsh[str(i)],ash[str(i)]
    bs,ns=q.scalars(old),q.scalars(new)
    return (q.block(old,'ship_design_implementation')==q.block(new,'ship_design_implementation')
        and all(bs.get(k)==ns.get(k) for k in ['fleet','construction_date','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints','last_combat_activity','last_damage','experience','upgrade_progress'])
        and all(0<=D(str(bs[k]))<=D(str(ns[k]))<=D(str(ns[m])) for k,m in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
        and D(str(ns['hitpoints']))>0 and ns.get('last_combat_activity','0.01.01')<='2271.12.01' and ns.get('killed')!='yes')
cal=load(after+'-calendar-receipt.json');ce=load(after+'-calendar-execution.json')
days=cal['days'];validate_native_interval(b['date'],a['date'],days)
pre=load(cal['prior_proof_file']);pe=load(cal['prior_execution_stage']+'-execution.json')
foundation=load('terravore-rear-clearing-first-born-calibration-war1-battle-v65-proof.json')
bqs,bi=construction(br);aqs,ai=construction(ar)
pending=lambda fs:[v for k,v,o in fs if k=='player_event' and o and q.scalars(v).get('country')==0]
contacts=[q.block(q.block(t['first_contacts'],'contacts'),'16777275') for t in [br,ar]]
reports=lambda fs:[v for k,v,o in fs if k=='message' and o and q.scalars(v).get('type')=='COMBAT_STATS' and q.scalars(v).get('receiver')==0]
source_b,source_a=b['planets']['1085'],a['planets']['1085']
mother_b,mother_a=b['planets']['7'],a['planets']['7']
sf=lambda p:{k:v for k,v in p['flags'].items() if k not in ['recently_eaten_planet','superior_colonies_can_be_boosted']}
def projects_ok():
    old,new=[q.block(c,'events') for c in [bcr,acr]]
    bp,ap=[{q.scalars(v)['id']:v for k,v,o in q.fields(t) if k=='special_project' and o} for t in [old,new]]
    if bp.keys()!=ap.keys() or not {4,5}<=bp.keys() or omit(old,{'special_project'})!=omit(new,{'special_project'}):return False
    for i in bp:
        if i not in [4,5]:
            if bp[i]!=ap[i]:return False
        elif not (omit(bp[i],{'days_left'})==omit(ap[i],{'days_left'}) and q.scalars(bp[i])['debris']==q.scalars(ap[i])['debris']=={4:16777219,5:369098752}[i] and q.scalars(bp[i])['days_left']-q.scalars(ap[i])['days_left']==days and q.scalars(ap[i])['days_left']>0):return False
    return True
keys=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in keys}
delta={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in keys}
residual={k:delta[k]-net[k] for k in keys}
bt,at=bc['tech_status'],ac['tech_status']
science={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bank_delta={k:D(str(ac['research_stockpile'].get(k,0)))-D(str(bc['research_stockpile'].get(k,0))) for k in q.RESEARCH_RESOURCES}
beng,aeng=research_queue(bt,'engineering_queue'),research_queue(at,'engineering_queue')
grows={i:growth(ar,i) for i in ['0','37']}
def history_entries(t):
    raw=q.block(t['open_player_event_selection_history'],'selected');out=[];depth=0;start=0
    for token,x,y in q.tokens(raw):
        if token=='{':
            if depth==0:start=y
            depth+=1
        elif token=='}':
            depth-=1
            if depth==0:out.append(raw[start:x])
    assert depth==0
    return out
bh,ah=history_entries(br),history_entries(ar)
def completed(t):
    fs=list(q.fields(t));out=[]
    for n,(k,v,o) in enumerate(fs):
        if k=='technology':
            assert not o and fs[n+1][0]=='level' and not fs[n+1][2]
            out.append((q.unquote(v),q.unquote(fs[n+1][1])))
    return out
native_sizes=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/ship_sizes/00_ship_sizes.txt')
bcon,acon=bsh['2'],ash['2']
bcon_design,acon_design=q.block(br['ship_design'],'167773698'),q.block(ar['ship_design'],'184551252')
country_timers=['entered_war_as_defender','recent_first_contact_process_started','recent_cara_3010','discovered_site','was_recently_targeted_by_voidworms']
def country_timers_ok():
    old,new=[q.block(v,'flags') for v in [bcr,acr]]
    return omit(old,set(country_timers))==omit(new,set(country_timers)) and all(omit(q.block(old,k),{'flag_days'})==omit(q.block(new,k),{'flag_days'}) and q.scalars(q.block(old,k))['flag_days']-q.scalars(q.block(new,k))['flag_days']==days and q.scalars(q.block(new,k))['flag_days']>0 for k in country_timers)
def modules_ok():
    old,new=[q.block(v,'modules') for v in [bcr,acr]]
    bs,ns=[q.block(v,'standard_event_module') for v in [old,new]]
    be,ne=[q.block(v,'delayed_event') for v in [bs,ns]]
    return omit(old,{'standard_event_module','standard_economy_module'})==omit(new,{'standard_event_module','standard_economy_module'}) and omit(q.block(old,'standard_economy_module'),{'resources'})==omit(q.block(new,'standard_economy_module'),{'resources'}) and omit(bs,{'delayed_event'})==omit(ns,{'delayed_event'}) and omit(be,{'days'})==omit(ne,{'days'}) and q.scalars(be)['event']==q.scalars(ne)['event']=='paragon.999' and q.scalars(be)['days']-q.scalars(ne)['days']==days and q.scalars(ne)['days']>0
def ordinal(s):
    y,m,d=map(int,s.split('.'));return y*360+(m-1)*30+d-1
ob,oa=ordinal(b['date']),ordinal(a['date'])
month_ticks=sum(i%30==0 for i in range(ob+1,oa+1))
research_ticks=sum(i%30==1 for i in range(ob+1,oa+1))
remaining=ordinal('2272.06.30')-oa
first=before=='terravore-second-annual-research-day'
first_loss=before=='terravore-interannual-first-check' and after=='terravore-interannual-months1-step1'
post_loss=b['date']>='2272.03.23'
def prior_ok():
    return (before=='terravore-third-pre-final' and after=='terravore-third-threshold29' and days==1
        and b['date']=='2272.06.30' and a['date']=='2272.07.01'
        and pre['status']=='PASS_NATIVE_TERRAVORE_PRE_FINAL_SEVEN_DAYS_COMPONENT' and len(pre['checks'])==32 and all(v is True for v in pre['checks'].values())
        and pe['returncode']==0 and pre['after_sha256']==b['save_sha256']=='c78b1e56e022ab06050ec50b256218a05f727c6ef730d371ba4b5f79a5237192'
        and pe['helper_sha256']==h.sha256(run/'priority_terravore_pre_final_seven_days_observer.py')=='c344b780cde8208a9b7d92eb0434d738c47e76b9b3fa8a3b65917f6e52da5243')

def finance_ok():
    if not month_ticks:return bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile']
    return (all(abs(residual[k])<=D('0.00005') for k in keys if k not in ['trade','influence'])
        and all(bc['effective_stockpile'][k]==ac['effective_stockpile'][k]==cap for k,cap in [('trade',50000),('influence',1000)])
        and {k:v for k,v in bc['effective_stockpile'].items() if k not in keys+list(q.RESEARCH_RESOURCES)}=={k:v for k,v in ac['effective_stockpile'].items() if k not in keys+list(q.RESEARCH_RESOURCES)}
        and ac['budget_categories']['last_month']==bc['budget_categories']['current_month'])
def population_ok():
    if not month_ticks:return all(b['colonies'][i]['actual_pop_sum']==a['colonies'][i]['actual_pop_sum'] for i in ['0','37'])
    return all(v[0]['month_start_size']==b['colonies'][i]['actual_pop_sum'] and v[0]['growth']>=0 and a['colonies'][i]['actual_pop_sum']==v[0]['month_start_size']+v[0]['growth'] and v[1]==([('key','GROWTH_CAT_GROWTH',False),('value',v[0]['growth'],False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)] if v[0]['growth'] else []) for i,v in grows.items())
def tech_ok():
    return (completed(bt)==completed(at) and omit(bt,{'stored_techpoints','engineering_queue'})==omit(at,{'stored_techpoints','engineering_queue'})
        and {k:v for k,v in beng.items() if k!='progress'}=={k:v for k,v in aeng.items() if k!='progress'}
        and beng['technology']==aeng['technology']=='tech_mass_drivers_3' and D(str(aeng.get('progress',0)))<1500
        and abs(D(str(aeng.get('progress',0)))-D(str(beng.get('progress',0)))-science['engineering_research']*D('1.33')*research_ticks)<=D('0.00005')
        and all(abs(bank_delta[k]-science[k]*D('1.33')*research_ticks)<=D('0.00005') for k in ['physics_research','society_research']) and bank_delta['engineering_research']==0)

original_fail=load('terravore-interannual-first-check-interannual-build-proof.json')
original_exec=load('terravore-interannual-first-check-observer-execution.json')
station_investigation_path=run/'terravore-interannual-first-check-science-station-full-sections-investigation.json'
station_investigation=load(station_investigation_path.name)

def original_fail_ok():
    return (original_fail['status']=='FAIL' and len(original_fail['checks'])==29
        and [k for k,v in original_fail['checks'].items() if v is not True]==['all_other_civilian_and_station_ships_held_only_science_rotation']
        and original_exec['returncode']==1 and original_exec['helper_sha256']==h.sha256(run/'priority_terravore_interannual_build_observer.py')=='99e128cc109b62b1c49f74ec289839cf6e0828402e0a6bf1dbd3003d4031ff55'
        and original_fail['before_sha256']==h.sha256(run/'terravore-second-annual-research-day.sav')=='0f6750bad9d2bc033e7a29398b30394aac1cf6bd9d58931d71af68aec11de837'
        and original_fail['after_sha256']==h.sha256(run/'terravore-interannual-first-check.sav')=='57ade9e32e50f00a6ea07c4eddda2f5fa366a5a21709bcb316180512aa0680a1'
        and h.sha256(station_investigation_path)=='ce1b0f8a8684486855011ae19db6d1ded389a504c96c5ff949f288c7de8a8248')

def sections_and_indexes(raw):
    sections=[];indexes=[]
    for k,v,o in q.fields(raw):
        if k!='section':continue
        if not o:return None,None
        weapons=[]
        for wk,wv,wo in q.fields(v):
            if wk!='weapon':continue
            if not wo:return None,None
            ws=q.scalars(wv)
            if not isinstance(ws.get('index'),int) or not isinstance(ws.get('component_slot'),str):return None,None
            indexes.append(ws['index'])
            weapons.append((ws['component_slot'],omit(wv,{'index'})))
        if len({x[0] for x in weapons})!=len(weapons):return None,None
        sections.append((omit(v,{'weapon'}),sorted(weapons)))
    return sections,indexes

def station_ok(i):
    old,new=bsh[str(i)],ash[str(i)]
    if omit(old,{'section','next_weapon_index'})!=omit(new,{'section','next_weapon_index'}):return False
    bs,ns=q.scalars(old),q.scalars(new)
    if not isinstance(bs.get('next_weapon_index'),int) or not isinstance(ns.get('next_weapon_index'),int) or not bs['next_weapon_index']<=ns['next_weapon_index']:return False
    bsections,bind=sections_and_indexes(old);asections,aind=sections_and_indexes(new)
    if bind is None or aind is None or not bind or not aind:return False
    if not all(len(ids)==len(set(ids)) and all(0<=idx<limit for idx in ids) for ids,limit in [(bind,bs['next_weapon_index']),(aind,ns['next_weapon_index'])]):return False
    if first and i==0:
        return (after=='terravore-interannual-first-check' and original_fail_ok()
            and old==station_investigation['terravore-second-annual-research-day']['station_raw']['0']
            and new==station_investigation['terravore-interannual-first-check']['station_raw']['0'])
    return bsections==asections

def civilian_station_ok():
    spatial={'coordinate','target_coordinate','post_move_angle','rotation','forward_x','forward_y','speed','shield_hitpoints'}
    old,new=bfl['1'],afl['1']
    bcur,acur=[q.block(v,'current_order') for v in [old,new]]
    baut,aaut=[q.block(v,'automate_fleet_order') for v in [bcur,acur]]
    return (omit(bsh['1'],spatial)==omit(ash['1'],spatial)
        and omit(old,{'movement_manager','current_order'})==omit(new,{'movement_manager','current_order'})
        and q.scalars(old)['order_id']==q.scalars(new)['order_id']==64
        and omit(bcur,{'automate_fleet_order'})==omit(acur,{'automate_fleet_order'})
        and omit(baut,{'sub_order'})==omit(aaut,{'sub_order'}) and q.scalars(aaut)['order_id']==61
        and q.scalars(aaut)['settings_explore']==q.scalars(aaut)['settings_survey']=='yes'
        and q.scalars(bsh['1'])['shield_hitpoints']==192 and q.scalars(ash['1'])['shield_hitpoints']==200 and q.scalars(ash['1'])['max_shield_hitpoints']==320
        and all(station_ok(i) for i in [0,1931,67109591])
        and all(bsh[str(i)]==ash[str(i)] for i in fleetships(bfl,bo)-bm-{1,2,0,1931,67109591,16779140}))


loss_stage='terravore-interannual-months1-step1'
loss_inv=load(loss_stage+'-missing-original-colonizer-investigation.json')
attack_inv=load(loss_stage+'-colonizer-native-attack-investigation.json')
loss_exec=load(loss_stage+'-observer-v2-execution.json')
def original_loss_exception_ok():
    return (loss_exec['returncode']==1 and loss_exec['helper_sha256']==h.sha256(run/'priority_terravore_interannual_build_observer_v2.py')=='0a69dbf9b60852782356db4a01df3572c88d7bad3e64307003bf1b3cbfcf5978'
        and h.sha256(run/(loss_stage+'-observer-v2-stderr.txt'))=='bd50478eed2efd3b063294ecc7d0d1085d25e98d79e8cdf8be904e5e0629e319'
        and not (run/(loss_stage+'-interannual-build-v2-proof.json')).exists()
        and loss_inv['before_sha256']==h.sha256(run/'terravore-interannual-first-check.sav')=='57ade9e32e50f00a6ea07c4eddda2f5fa366a5a21709bcb316180512aa0680a1'
        and loss_inv['after_sha256']==h.sha256(run/(loss_stage+'.sav'))=='36f22230ee0a24aa7c8ea4f7c39c40788d0037a233a0024eb62573dd20ee562a'
        and h.sha256(run/(loss_stage+'-missing-original-colonizer-investigation.json'))=='e6d86c83c77f5fd25ec51a4f51eb1824fe938dfebf5a2538f2d4fc3631330378'
        and h.sha256(run/(loss_stage+'-colonizer-native-attack-investigation.json'))=='5ae461fe1bc54d7a2d774a564e1d1558eee2264476a91cf4d44281e2076b0632')
def attack_evidence_ok():
    old=attack_inv['terravore-interannual-first-check'];new=attack_inv[loss_stage]
    targets=new['targeting_original_colonizer']
    expected={'67109342','117441693','16778802','16778809','16778851','16778905','50333407','1808','33556283'}
    if old['targeting_original_colonizer'] or set(targets)!=expected or new['ship16779140_entry']!=[['none',False]] or new['fleet16778062_entry']!=[['none',False]]:return False
    if not all(t['owner']==1 and q.scalars(t['ship'])['fleet']==825 and q.scalars(t['ship'])['last_combat_activity']=='2272.02.30' and t['targeting_weapons'] and all(q.scalars(q.block(q.block(w,'targeting_module'),'target'))=={'type':0,'id':16779140} for w in t['targeting_weapons']) for t in targets.values()):return False
    msg=[q.scalars(v) for v in loss_inv['new_country0_messages']]
    if msg!=[{'type':'FLEET_EVADE_HOSTILE_MESSAGE_TYPE','localization':'MESSAGE_FLEET_EVADE_HOSTILE','receiver':0,'target_fleet':16778062,'end':'2272.04.30','date':'2272.02.30','notification':250,'message_type':'none'}]:return False
    if first_loss:return all(ash[sid]==t['ship'] and afl['825']==t['fleet'] for sid,t in targets.items())
    return post_loss

def original_colonizer_loss_or_absent_ok():
    oldraw=[(v,o) for k,v,o in q.fields(br['ships']) if k=='16779140']
    newraw=[(v,o) for k,v,o in q.fields(ar['ships']) if k=='16779140']
    newfleet=[(v,o) for k,v,o in q.fields(ar['fleet']) if k=='16778062']
    if newraw!=[('none',False)] or newfleet!=[('none',False)] or 16778062 in ao:return False
    if first_loss:
        return (oldraw==[(loss_inv['all_changed_owned_ships_full']['16779140']['before'],True)] and bfl['16778062']==loss_inv['before_original_colony_fleet'] and 16778062 in bo)
    return post_loss and oldraw==[('none',False)] and [(v,o) for k,v,o in q.fields(br['fleet']) if k=='16778062']==[('none',False)] and 16778062 not in bo

def known_war_boundary_ok():
    old=q.block(q.block(br['war'],'1'),'battles');new=q.block(q.block(ar['war'],'1'),'battles')
    if first_loss:return old==loss_inv['before_war1_battles'] and new==loss_inv['after_war1_battles']
    return post_loss and old==new


threshold_observation=load(after+'-third-boundary-observation.json')
threshold_observation_exec=load(after+'-boundary-observation-execution.json')
def threshold_observation_ok():
    return (threshold_observation['status']=='OBSERVED_NATIVE_TERRAVORE_THIRD_BOUNDARY' and len(threshold_observation['checks'])==6 and all(v is True for v in threshold_observation['checks'].values())
        and threshold_observation_exec['returncode']==0 and threshold_observation_exec['helper_sha256']==h.sha256(run/'priority_terravore_third_boundary_observation.py')=='a11ed89e421e5fc177130377cb322dcf4d96fb9b7c900bca24af411f750ec801'
        and threshold_observation['before_sha256']==b['save_sha256'] and threshold_observation['after_sha256']==a['save_sha256']=='1c51e8c1e95e497273029fad8f3a30f2672e9d43e983ec252b4ff8b3f8601087'
        and h.sha256(run/(after+'-third-boundary-observation.json'))=='e6377cb102c165747147c3c91da95bd87da4a94bdcf58e6f482e446171570a52')

checks={
 'original_threshold_observation6_actual0_source_and_SHA':threshold_observation_ok(),
 'no_new_native_bites_or_country_messages_at_threshold':not threshold_observation['new_native_bite_messages_raw'] and not threshold_observation['new_country0_messages_raw'],
 'original_V2_KeyError_actual1_traceback_and_SAV_anchor':original_loss_exception_ok(),
 'fixed_native_enemy825_attack_and_original_colonizer_removal_evidence':attack_evidence_ok(),
 'original29_single_FAIL_actual1_source_original_SAV_anchor':original_fail_ok(),
 'global_history_old_raw_prefix_no_new_manual_choices':ah[:len(bh)]==bh and all(q.scalars(v).get('human')==-1 and isinstance(q.scalars(v).get('player_event'),int) and q.scalars(v)['player_event']>0 and isinstance(q.scalars(v).get('option'),int) and len(list(q.fields(v)))==3 and all(not o for k,x,o in q.fields(v)) for v in ah[len(bh):]) and omit(br['open_player_event_selection_history'],{'selected'})==omit(ar['open_player_event_selection_history'],{'selected'}),
 'prior_component_PASS_actual0_source_and_SHA':prior_ok(),
 'bounded_native_interval_before_final_original_SAV_pair':b['date']=='2272.06.30' and a['date']=='2272.07.01' and days==1 and month_ticks==1 and research_ticks==0 and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and cal['start_date']==b['date'] and cal['date']==a['date'] and cal['status']=='CALENDAR_CONFIRMED' and all(x['save_sha256']==h.sha256(run/(st+'.sav')) for st,x in [(before,b),(after,a)]),
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'only_original_inactive264_pending_contact_history_held':pending(bf)==pending(af) and len(pending(af))==1 and q.scalars(pending(af)[0])=={'id':264,'event':'grand_archive.2800','date':'2273.12.20','country':0} and contacts[0]==contacts[1] and not q.block(contacts[1],'event'),
 'same28_military_and_all_owned_ships_fleets_naval140':ao==([i for i in bo if i!=16778062] if first_loss else bo) and fleetships(afl,ao)==(fleetships(bfl,bo)-{16779140} if first_loss else fleetships(bfl,bo)) and bm==am==set(foundation['actual_alive_military_ship_ids']) and len(am)==28 and q.scalars(acr)['fleet_size']==140,
 'all28_design_dates_max_only_native_repair_no_new_combat_activity':all(ship_ok(i) for i in am),
 'no_current_owned_combat_only_fixed151_loss_battle_or_held_history':not any(q.ids(q.block(q.block(afl[str(i)],'combat'),'in_combat_with')) for i in ao) and known_war_boundary_ok() and all(v in reports(bf) for v in reports(af)),
 'original_colonizer_fixed_loss_or_held_absence_target523_uncolonized':original_colonizer_loss_or_absent_ok() and q.block(q.block(br['planets'],'planet'),'523')==q.block(q.block(ar['planets'],'planet'),'523'),
 'EEP_C37_D11_G0_worlds2_PSI1_no_new_reward_or_species':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'].get(k)==v for k,v in {'eep_c':37,'eep_d':11,'eep_g':0,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()) and b['species']==a['species'] and b['event_targets']==a['event_targets'],
 'nemesis_level1_projects_only_two_known_debris_timers':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and projects_ok() and all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions','owned_colonies']),
 'mother_capacity11_modifier_no_bombardment_same_districts_buildings':mother_a['owner']==mother_a['controller']==0 and mother_a['colony']==0 and mother_a['variables']['eep_capacity_value']==11 and mother_b['modifiers']==mother_a['modifiers'] and mother_a['bombardment_damage']==0 and sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and all(b['districts'][i]==a['districts'][i] for i in ['1','2','3']) and all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','104']) and all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for zid in ['0','2','104'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))),
 'full_technician1400_and_all_other_mother_job_caps_held':len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['workforce']==j['max_workforce']==j['workforce_limit']==1400])==1 and {i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in b['pop_jobs'].items() if j['planet']==0}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in a['pop_jobs'].items() if j['planet']==0},
 'month1_housing14100_exact_native_growth7_cache_lag':a['colonies']['0']['total_housing']==14100 and a['colonies']['0']['housing_usage']==b['colonies']['0']['actual_pop_sum']==10827 and a['colonies']['0']['free_housing']==3273 and a['colonies']['0']['actual_pop_sum']==a['colonies']['0']['employable_pops']==a['colonies']['0']['num_sapient_pops']==10834 and a['colonies']['0']['actual_pop_sum']-a['colonies']['0']['housing_usage']==grows['0'][0]['growth']==7 and a['colonies']['0']['free_amenities']>0 and a['colonies']['0']['crime']==0,
 'two_colonies_only_native_zero_or_one_month_growth':population_ok(),
 'third_Q12_T29_seed103_need_minus3_deposits_held':source_b['variables']==source_a['variables']=={'eep_q':12,'eep_old_damage':0,'eep_months':29,'eep_seed_existing':103,'eep_seed_need':-3} and sf(source_b)==sf(source_a) and source_a['owner']==0 and source_a['colony']==37 and source_b['deposits']==source_a['deposits'] and source_b['modifiers']==source_a['modifiers'],
 'third_expected_progress24_to28_no_native_duplicate':omit(q.block(br['situations'],'100663299'),{'progress'})==omit(q.block(ar['situations'],'100663299'),{'progress'}) and b['situations']['100663299']['progress']==24+(ob-ordinal('2272.02.01'))//30 and a['situations']['100663299']['progress']==24+(oa-ordinal('2272.02.01'))//30 and a['situations']['100663299']['progress']==29 and len([v for v in a['situations'].values() if v.get('type')=='situation_eep_devouring'])==1 and not any(v.get('type')=='situation_terravore_consume_planet' for v in a['situations'].values()),
 'two_known_source_flags_exact_days_and_recovery':all(source_b['flags'][k]['flag_date']==source_a['flags'][k]['flag_date'] and source_b['flags'][k]['flag_days']-source_a['flags'][k]['flag_days']==days and source_a['flags'][k]['flag_days']>0 for k in ['recently_eaten_planet','superior_colonies_can_be_boosted']) and 0<=source_a['bombardment_damage']<=source_b['bombardment_damage'],
 'physics_zone_original_order_exact_total_native_work':q.ids(q.block(bqs['0'],'items'))==q.ids(q.block(aqs['0'],'items'))==[1258291211] and omit(bi['1258291211'],{'progress'})==omit(ai['1258291211'],{'progress'}) and all(D(str(q.scalars(items['1258291211'])['progress']))==D('1.4')*(ord_value-ordinal('2271.12.23'))<360 for items,ord_value in [(bi,ob),(ai,oa)]),
 'rear_colonizer_original_order_exact_total_native_work':q.ids(q.block(bqs['2287'],'items'))==q.ids(q.block(aqs['2287'],'items'))==[83886124] and omit(bi['83886124'],{'progress'})==omit(ai['83886124'],{'progress'}) and all(D(str(q.scalars(items['83886124'])['progress']))==D('1.33')*(ord_value-ordinal('2271.12.12'))<360 for items,ord_value in [(bi,ob),(ai,oa)]),
 'all_other_player_queues_held_no_new_orders':{k:v for k,v in bqs.items() if q.scalars(v).get('owner')==0}=={k:v for k,v in aqs.items() if q.scalars(v).get('owner')==0},
 'native_zero_or_one_month_resource_ledger_positive_E_M_A_U':finance_ok() and all(net[k]>0 for k in ['energy','minerals','alloys','unity']),
 'same_mass_drivers3_native_science_progress_and_banks_no_completion':tech_ok(),
 'known_five_country_native_timers_exact_days_EEP_flags_held':country_timers_ok(),
 'only_native_paragon999_timer_and_economy_mirror_module_changes':modules_ok(),
 'current_constructor184551252_armor125_held':omit(bcon,{'rotation','forward_x','forward_y'})==omit(acon,{'rotation','forward_x','forward_y'}) and q.scalars(q.block(acon,'ship_design_implementation'))=={'design':184551252,'upgrade':4294967295,'growth_stage':0} and q.scalars(acon)['armor_hitpoints']==q.scalars(acon)['max_armor_hitpoints']==125,
 'existing_science_auto_explore_and_fixed_station_instances_only':civilian_station_ok(),
 'source_native_caps_and_all_population_employed':all(len([j for j in a['pop_jobs'].values() if j['planet']==37 and j['type']==kind and j['max_workforce']==cap and 0<=j['workforce']<=cap])==1 for kind,cap in [('coordinator',200),('patrol_drone',100),('logistics_drone',200)]) and sum(j['workforce'] for j in a['pop_jobs'].values() if j['planet']==37 and j['max_workforce']>=0)==a['colonies']['37']['actual_pop_sum']<=500,
}
passed=all(v is True for v in checks.values())
p={'status':'PASS_NATIVE_TERRAVORE_THIRD_THRESHOLD29_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'days':days,'actual_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'ledger_residuals':{k:str(v) for k,v in residual.items()},'science_income':{k:str(v) for k,v in science.items()},'research_bank_delta':{k:str(v) for k,v in bank_delta.items()},'actual_engineering_queue_before':beng,'actual_engineering_queue_after':aeng,'native_population_growth':grows,'actual_alive_military_ship_ids':sorted(am),'calendar_ready':False,'interannual_build_calendar_ready':False,'maximum_days_to_final_boundary':0,'third_settlement_day_ready':passed,'housing_cache_refresh_pending':a['colonies']['0']['housing_usage']!=a['colonies']['0']['actual_pop_sum'],'actual_engineering_technology':'tech_mass_drivers_3','actual_third_progress':a['situations']['100663299']['progress'],'actual_physics_zone_work':q.scalars(ai['1258291211'])['progress'],'actual_colonizer_work':q.scalars(ai['83886124'])['progress'],'native_month_ticks':month_ticks,'new_global_nonmanual_history':[q.scalars(v) for v in ah[len(bh):]],'scope':'Only native third progress29 threshold still active/uncredited, housing monthly cache lag7 still pending. Bounded native interannual construction/economy/science/population component after explicitly recorded original colonizer loss, not original route recovery, with original28 military, unchanged EEP and no final consumption yet. Housing cache must actually match population at these aligned endpoints. Not physics specialization completion, new colonizer birth/recovery, mineral fleet or full route acceptance.'}
out=run/(after+'-third-threshold29-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'net':p['actual_net'],'research_bank_delta':p['research_bank_delta']}),flush=True)
assert passed,'Original month FAIL retained; no calendar replay'
