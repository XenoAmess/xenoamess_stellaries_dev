"""Documented seven-day preannual component; no game actions."""
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
checks={
 'global_history_old_raw_prefix_no_new_manual_choices':ah[:len(bh)]==bh and all(q.scalars(v).get('human')==-1 and isinstance(q.scalars(v).get('player_event'),int) and q.scalars(v)['player_event']>0 and isinstance(q.scalars(v).get('option'),int) and len(list(q.fields(v)))==3 and all(not o for k,x,o in q.fields(v)) for v in ah[len(bh):]) and omit(br['open_player_event_selection_history'],{'selected'})==omit(ar['open_player_event_selection_history'],{'selected'}),
 'original_month28_PASS_actual0_source_and_SHA':len(pre['checks'])==28 and pre['status'].startswith('PASS_') and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(run/'priority_terravore_post_generator_month_observer_v2.py')=='900e994fa2ea31c320cd3ec529aae0284e557457e4aaaffc6700c403d25ba47c' and pre['after_sha256']==b['save_sha256']=='fc01ed3a3a679f6173fdc6f9db699d11eb032b30cbb5d1da730d0d339ca40a7f',
 'actual_unique7day_preannual_calendar_and_original_SAV_pair':b['date']=='2272.01.23' and a['date']=='2272.01.30' and days==7 and ce['returncode']==0 and ce['helper_sha256']==h.sha256(run/'formal_production_native_calendar_checked_v2.py')=='66382265586f27567ad5ab5395a4505b45b9a6cb4f55be5e928febd4b68667dc' and cal['start_date']==b['date'] and cal['date']==a['date'] and cal['status']=='CALENDAR_CONFIRMED' and all(x['save_sha256']==h.sha256(run/(st+'.sav')) for st,x in [(before,b),(after,a)]),
 'production41_same_tree_simp_chinese':meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'unfiltered2814_error_exact_original_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'only_original_inactive264_pending_contact_history_held':pending(bf)==pending(af) and len(pending(af))==1 and q.scalars(pending(af)[0])=={'id':264,'event':'grand_archive.2800','date':'2273.12.20','country':0} and contacts[0]==contacts[1] and not q.block(contacts[1],'event'),
 'same28_military_and_all_owned_ships_fleets_naval140':bo==ao and fleetships(bfl,bo)==fleetships(afl,ao) and bm==am==set(foundation['actual_alive_military_ship_ids']) and len(am)==28 and q.scalars(acr)['fleet_size']==140,
 'all28_design_dates_max_only_native_repair_no_new_combat_activity':all(ship_ok(i) for i in am),
 'no_owned_combat_or_war1_new_battle_only_old_reports_may_expire':not any(q.ids(q.block(q.block(afl[str(i)],'combat'),'in_combat_with')) for i in ao) and q.block(q.block(br['war'],'1'),'battles')==q.block(q.block(ar['war'],'1'),'battles') and all(v in reports(bf) for v in reports(af)),
 'original_colonizer_idle151_retained_and_target523_still_uncolonized':bsh['16779140']==ash['16779140'] and bfl['16778062']==afl['16778062'] and q.block(q.block(br['planets'],'planet'),'523')==q.block(q.block(ar['planets'],'planet'),'523'),
 'EEP_C37_D11_G0_worlds2_PSI1_no_new_reward_or_species':bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and all(ac['variables'].get(k)==v for k,v in {'eep_c':37,'eep_d':11,'eep_g':0,'eep_made':0,'eep_worlds':2,'eep_psi':1}.items()) and b['species']==a['species'] and b['event_targets']==a['event_targets'],
 'nemesis_level1_projects_only_two_known_debris_timers':q.block(bcr,'crisis_progression')==q.block(acr,'crisis_progression') and q.scalars(q.block(acr,'crisis_progression'))=={'path':'nemesis_path','level':'crisis_level_1'} and projects_ok() and all(bc[k]==ac[k] for k in ['government','ascension_perks','traditions','owned_colonies']),
 'mother_capacity11_modifier_no_bombardment_same_districts_buildings':mother_a['owner']==mother_a['controller']==0 and mother_a['colony']==0 and mother_a['variables']['eep_capacity_value']==11 and mother_b['modifiers']==mother_a['modifiers'] and mother_a['bombardment_damage']==0 and sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and all(b['districts'][i]==a['districts'][i] for i in ['1','2','3']) and all(q.block(br['zones'],i)==q.block(ar['zones'],i) for i in ['0','2','104']) and all(q.block(br['buildings'],str(i))==q.block(ar['buildings'],str(i)) for zid in ['0','2','104'] for i in q.ids(q.block(q.block(ar['zones'],zid),'buildings'))),
 'full_technician1400_and_all_other_mother_job_caps_held':len([j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']=='technician_drone' and j['workforce']==j['max_workforce']==j['workforce_limit']==1400])==1 and {i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in b['pop_jobs'].items() if j['planet']==0}=={i:(j['type'],j['max_workforce'],j['workforce_limit']) for i,j in a['pop_jobs'].items() if j['planet']==0},
 'housing14100_positive_amenities_no_crime':a['colonies']['0']['total_housing']==14100 and a['colonies']['0']['free_housing']==14100-a['colonies']['0']['actual_pop_sum'] and a['colonies']['0']['free_amenities']>0 and a['colonies']['0']['crime']==0,
 'no_month_tick_both_colony_actual_population_held':all(b['colonies'][i]['actual_pop_sum']==a['colonies'][i]['actual_pop_sum'] for i in ['0','37']),
 'third_Q12_T29_seed103_need_minus3_deposits_held':source_b['variables']==source_a['variables']=={'eep_q':12,'eep_old_damage':0,'eep_months':29,'eep_seed_existing':103,'eep_seed_need':-3} and sf(source_b)==sf(source_a) and source_a['owner']==0 and source_a['colony']==37 and source_b['deposits']==source_a['deposits'] and source_b['modifiers']==source_a['modifiers'],
 'third23_held_no_native_duplicate':q.block(br['situations'],'100663299')==q.block(ar['situations'],'100663299') and a['situations']['100663299']['progress']==23 and len([v for v in a['situations'].values() if v.get('type')=='situation_eep_devouring'])==1 and not any(v.get('type')=='situation_terravore_consume_planet' for v in a['situations'].values()),
 'two_known_source_flags_exact7_days_positive_and_devastation_recovery':all(source_b['flags'][k]['flag_date']==source_a['flags'][k]['flag_date'] and source_b['flags'][k]['flag_days']-source_a['flags'][k]['flag_days']==days and source_a['flags'][k]['flag_days']>0 for k in ['recently_eaten_planet','superior_colonies_can_be_boosted']) and 0<=source_a['bombardment_damage']<=source_b['bombardment_damage'],
 'physics_zone_only_paid_order_work42_to51_8':q.ids(q.block(bqs['0'],'items'))==q.ids(q.block(aqs['0'],'items'))==[1258291211] and omit(bi['1258291211'],{'progress'})==omit(ai['1258291211'],{'progress'}) and D(str(q.scalars(bi['1258291211'])['progress']))==D(42) and D(str(q.scalars(ai['1258291211'])['progress']))==D('51.8'),
 'rear_colonizer_only_paid_order_work54_53_to63_84':q.ids(q.block(bqs['2287'],'items'))==q.ids(q.block(aqs['2287'],'items'))==[83886124] and omit(bi['83886124'],{'progress'})==omit(ai['83886124'],{'progress'}) and D(str(q.scalars(bi['83886124'])['progress']))==D('54.53') and D(str(q.scalars(ai['83886124'])['progress']))==D('63.84'),
 'all_other_player_queues_held_no_new_orders':{k:v for k,v in bqs.items() if q.scalars(v).get('owner')==0}=={k:v for k,v in aqs.items() if q.scalars(v).get('owner')==0},
 'all_actual_stocks_banks_technology_held_no_month_tick':bc['effective_stockpile']==ac['effective_stockpile'] and bc['research_stockpile']==ac['research_stockpile'] and bc['tech_status']==ac['tech_status'],
}
passed=all(v is True for v in checks.values())
p={'status':'PASS_NATIVE_TERRAVORE_THIRD_PRE_SECOND_ANNUAL_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'days':days,'actual_net':{k:str(v) for k,v in net.items()},'actual_stock_deltas':{k:str(v) for k,v in delta.items()},'ledger_residuals':{k:str(v) for k,v in residual.items()},'science_income':{k:str(v) for k,v in science.items()},'research_bank_delta':{k:str(v) for k,v in bank_delta.items()},'actual_engineering_queue_before':beng,'actual_engineering_queue_after':aeng,'native_population_growth':grows,'actual_alive_military_ship_ids':sorted(am),'calendar_ready':False,'pre_second_annual_ready':passed,'new_global_nonmanual_history':[q.scalars(v) for v in ah[len(bh):]],'scope':'Exactly7 native days before second annual bite; unchanged stocks/science/population/EEP, paid construction51.8 and63.84,28 ordinary military. Not physics specialization completion, new colonizer birth/recovery, mineral fleet or full route acceptance.'}
out=run/(after+'-pre-second-annual-proof.json');assert not out.exists();h.write_json(out,p)
print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'net':p['actual_net'],'research_bank_delta':p['research_bank_delta']}),flush=True)
assert passed,'Original month FAIL retained; no calendar replay'
