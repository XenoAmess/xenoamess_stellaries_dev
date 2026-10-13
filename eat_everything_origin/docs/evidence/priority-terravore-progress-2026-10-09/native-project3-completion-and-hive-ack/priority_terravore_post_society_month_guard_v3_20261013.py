"""Validate each 30-day native post-conversion research, hive, fleet and ledger interval."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
before,after,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
p=load(prior);review=load(before+'-post-second-society-month-review-v3.json');ob=load(after+'-construction-boundary-observation-v4.json');cal=load(after+'-calendar-receipt.json')
xs=[load(s+'-execution.json') for s in [execution,review['execution_stage'],after+'-calendar',after+'-boundary-observation-v4']]
def queue(c,key):
    raw=c['research_queues'].get(key,'');ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]]) if ts else {}
def income(c,key):return sum((D(str(v.get(key,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0))
def flags(s):return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
bp,ap=queue(bc,'society_queue'),queue(ac,'society_queue')
draw=min(income(bc,'society_research'),D(str(bc['research_stockpile']['society_research'])))
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
expected={k:D(str(bc['effective_stockpile'].get(k,0)))+net[k] for k in resources};expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade'])
residual={k:D(str(ac['effective_stockpile'].get(k,0)))-expected[k] for k in resources}
ids=q.ids(q.block(b['queues']['0'],'items'));front=str(ids[0]);zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295}
buildings={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
growthraw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(growthraw));growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
armies=q.ids(q.block(b['country'],'owned_armies'))
orbitals=q.scalars(q.block(q.block(q.block(a['roots']['planets'],'planet'),'1732'),'planet_orbitals'))
support=True
for fid,index in [('917',1),('50332250',2)]:
    fleet=a['fleets'][fid];mm=q.block(fleet,'movement_manager')
    support=support and not q.block(fleet,'current_order') and q.scalars(q.block(mm,'coordinate'))['origin']==164 and q.scalars(q.block(mm,'orbit'))=={'index':index} and q.scalars(q.block(q.block(mm,'orbit'),'orbitable'))=={'planet':1732} and orbitals.get(str(index))==int(fid) and mm==q.block(b['fleets'][fid],'movement_manager')
main={str(i) for i in q.ids(q.block(b['fleets']['83886903'],'ships'))};support_ships={str(i) for fid in ['917','50332250'] for i in q.ids(q.block(b['fleets'][fid],'ships'))};life=True
for i,v in b['ships'].items():
    av=a['ships'].get(i,'');old,now=q.scalars(v),q.scalars(av)
    life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and all(old.get(k)==now.get(k) for k in ['construction_date','killed','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
    if i in main:
        for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
            wanted=min(D(str(old[cap])),D(str(old.get(key,0)))+D(str(old[cap]))*D('.0025')*30)
            life=life and abs(D(str(now.get(key,0)))-wanted)<D('.0001')
        life=life and now.get('shield_hitpoints',0)==0 and now.get('hitpoints',0)>0
    else:
        life=life and all(old.get(k)==now.get(k) for k in ['hitpoints','armor_hitpoints'])
        life=life and (now.get('shield_hitpoints',0)==0 if i in support_ships else old.get('shield_hitpoints')==now.get('shield_hitpoints'))
news=ob['new_country0_messages_raw']
native_news=all(q.scalars(v).get('type')=='SYSTEM_SURVEYED' and q.scalars(v).get('localization')=='MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED' and q.scalars(v).get('receiver')==0 for v in news)
delays=[q.scalars(v) for k,v,obj in q.fields(q.block(q.block(a['country'],'modules'),'standard_event_module')) if obj and k=='delayed_event']
expected_flags={k:dict(v,flag_days=v['flag_days']-30) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>30}
checks={
 'prior_review6or7PASS_calendar_observer7PASS_actual0_originalSAV':p['status'].startswith('PASS') and review['status']=='PASS_REVIEWED_NATIVE_BOUNDARY' and len(review['checks']) in [6,7] and len(ob['checks'])==7 and all(v is True for pp in [p,review,ob] for v in pp['checks'].values()) and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs) and p['after_sha256']==review['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'one_native30day_autosave_month_bounded':cal['days']==30 and cal['start_date']==ba['date'] and cal['date']==aa['date']==review['end_date'] and ba['date'].endswith('.01') and aa['date'].endswith('.01') and aa['date']<='2287.12.01',
 'all_eight_cash_new_month_native_net_caps_exact':all(abs(v)<D('.00005') for v in residual.values()) and all(ac['effective_stockpile'][k]>=0 for k in resources),
 'project3_one_cached_research_tick_true_society_bank_draw':bp['special_project']==ap['special_project']==9 and ap['progress']<12000 and abs(D(str(ap['progress']))-D(str(bp['progress']))-income(bc,'society_research')*D('1.35')-draw)<D('.00005') and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+draw)<D('.00005'),
 'physics_engineering_idle_true_banks_one_tick':not queue(bc,'engineering_queue') and not queue(ac,'engineering_queue') and all(abs(D(str(ac['research_stockpile'][k]))-D(str(bc['research_stockpile'][k]))-income(bc,k)*D('1.35'))<D('.00005') for k in ['physics_research','engineering_research']),
 'all_other_native_tech_fields_and_project_shapes_held':dict(bp,progress=ap['progress'])==ap and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'four_paid400_hives_only_front_plus42_work_tail_held':ids==[1191182345,117440553,1476395019,117440546] and q.ids(q.block(a['queues']['0'],'items'))==ids and q.scalars(q.block(a['items'][front],'resources'))=={'minerals':400} and abs(D(str(q.scalars(a['items'][front])['progress']))-D(str(q.scalars(b['items'][front])['progress']))-D('42'))<D('.00005') and q.scalars(a['items'][front])['progress']<480 and omit(b['items'][front],{'progress'})==omit(a['items'][front],{'progress'}) and all(b['items'][str(i)]==a['items'][str(i)] for i in ids[1:]),
 'mother39_two_society_zones_six_old_labs_all_jobs_held':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in buildings) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']) and [aa['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2040,360],
 'society_engineering_job_income_and_costs_stable_23mineralship_upkeep':all(ac['budget_categories']['current_month'][kind][cat]==bc['budget_categories']['current_month'][kind][cat] for kind in ['income','expenses'] for cat in ['planet_biologists','planet_engineers','planet_physicists']) and ac['budget_categories']['current_month']['expenses']['ships']['minerals']==bc['budget_categories']['current_month']['expenses']['ships']['minerals']==74.72517,
 'mother_only_native_species73_growth_OTHER0':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+growth.get('GROWTH_CAT_GROWTH',0) and 0<=growth.get('GROWTH_CAT_GROWTH',0)<=10 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'EEP_queen_crisis3_menace3065_government_AP_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==3065,
 'all75_original_ship_identity_native_main_regeneration':len(a['ships'])==len(b['ships'])==75 and set(a['ships'])==set(b['ships']) and life,
 'all35_original_fleets_same_members_both_support_orbits':len(a['fleets'])==len(b['fleets'])==35 and set(a['fleets'])==set(b['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()) and support,
 'all15_original_armies_raw_held_no_new_ship_order':len(armies)==15 and armies==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in armies) and not q.ids(q.block(a['queues'].get('3',''),'items')),
 'native_flags_only_timer_change_contacts_held':flags(a)==expected_flags and all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'no_unknown_news_pending_delayed_event_war_truce_combat':native_news and not a['pending'] and not delays and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'destroyed_source_still_shattered_mother_housing_amenities_crime0':aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'CN41_same_production_unfiltered_error':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-post-second-society-month-v3-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_SECOND_SOCIETY_NORMAL_MONTH' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'cash_residual':{k:str(v) for k,v in residual.items()},'growth_details':growth,'project3_progress':ap['progress'],'hive_front_work':q.scalars(a['items'][front])['progress'],'new_messages_raw':news,'boundaries':['project3_normal_months_and_next_paid_hive_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One native paid-hive and project3 month, before first hive or project completion; not full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'project3':ap['progress'],'hive_work':q.scalars(a['items'][front])['progress'],'new_messages':[q.scalars(v) for v in news]}),flush=True);assert passed
