"""Validate the first later prepaid hive completion with two society zones."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-post-second-society-month-22871201';after='terravore-first-post-conversion-hive-completed-22871230'
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
p=load(before+'-post-second-society-month-v3-proof.json');rev=load(before+'-first-hive-completion-review.json');ob=load(after+'-construction-boundary-observation-v4.json');cal=load(after+'-calendar-receipt.json')
xs=[load(s+'-execution.json') for s in [before+'-post-second-society-month-guard-v3',before+'-first-hive-completion-review',after+'-calendar',after+'-boundary-observation-v4']]
ids=q.ids(q.block(b['queues']['0'],'items'));newids=q.ids(q.block(a['queues']['0'],'items'))
zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295}
buildings={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
def research_queue(c,key):
    raw=c['research_queues'].get(key,'');ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]]) if ts else {}
def income(c,key):return sum((D(str(v.get(key,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0))
def flags(s):return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
bp,ap=[research_queue(c,'society_queue') for c in [bc,ac]];draw=min(income(bc,'society_research'),D(str(bc['research_stockpile']['society_research'])))
cash_keys=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']
cash={k:D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0))) for k in cash_keys}
job24_before=ba['pop_jobs']['24'];job24_after=aa['pop_jobs']['24'];job7_before=ba['pop_jobs']['7'];job7_after=aa['pop_jobs']['7']
jobs_ok=set(ba['pop_jobs'])==set(aa['pop_jobs']) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ba['pop_jobs'] if i not in ['24','7'])
jobs_ok=jobs_ok and job24_after==dict(job24_before,workforce=2280,max_workforce=2280,bonus_workforce=798,workforce_limit=2280,automated_workforce_limit=2280)
jobs_ok=jobs_ok and job7_after==dict(job7_before,workforce=3762,bonus_workforce=753.6)
orbitals=q.scalars(q.block(q.block(q.block(a['roots']['planets'],'planet'),'1732'),'planet_orbitals'))
support_ok=True
for fid,index in [('917',1),('50332250',2)]:
    fleet=a['fleets'][fid];mm=q.block(fleet,'movement_manager')
    support_ok=support_ok and not q.block(fleet,'current_order') and q.scalars(q.block(mm,'orbit'))=={'index':index} and q.scalars(q.block(q.block(mm,'orbit'),'orbitable'))=={'planet':1732} and orbitals.get(str(index))==int(fid) and mm==q.block(b['fleets'][fid],'movement_manager')
main={str(i) for i in q.ids(q.block(b['fleets']['83886903'],'ships'))};support_ships={str(i) for fid in ['917','50332250'] for i in q.ids(q.block(b['fleets'][fid],'ships'))};life=True
for i,v in b['ships'].items():
    av=a['ships'].get(i,'');old,now=q.scalars(v),q.scalars(av)
    life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and all(old.get(k)==now.get(k) for k in ['construction_date','killed','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
    if i in main:
        for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
            wanted=min(D(str(old[cap])),D(str(old.get(key,0)))+D(str(old[cap]))*D('.0025')*29)
            life=life and abs(D(str(now.get(key,0)))-wanted)<D('.0001')
        life=life and now.get('shield_hitpoints',0)==0 and now.get('hitpoints',0)>0
    else:
        life=life and all(old.get(k)==now.get(k) for k in ['hitpoints','armor_hitpoints'])
        life=life and (now.get('shield_hitpoints',0)==0 if i in support_ships else old.get('shield_hitpoints')==now.get('shield_hitpoints'))
armies=q.ids(q.block(b['country'],'owned_armies'))
expected_flags={k:dict(v,flag_days=v['flag_days']-29) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>29}
news=ob['new_country0_messages_raw'];expected_news={'type':'SYSTEM_SURVEYED','localization':'MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED','receiver':0,'target_system':168,'end':'2288.03.21','date':'2287.12.21','notification':318,'message_type':'none'}
checks={
 'prior18PASS_review5PASS_calendar_observer6PASS_actual0_originalSAV':len(p['checks'])==18 and len(rev['checks'])==5 and len(ob['checks'])==6 and all(v is True for pp in [p,rev,ob] for v in pp['checks'].values()) and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs) and p['after_sha256']==rev['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact29day_first_threshold_native_calendar':ba['date']=='2287.12.01' and aa['date']=='2287.12.30' and cal['days']==29 and cal['start_date']==ba['date'] and cal['date']==aa['date']==rev['end_date'],
 'paid400_first_hive_consumed_three_original_orders_held':ids==[1191182345,117440553,1476395019,117440546] and newids==ids[1:] and '1191182345' not in a['items'] and all(a['items'][str(i)]==b['items'][str(i)] for i in newids) and all(q.scalars(q.block(a['items'][str(i)],'resources'))=={'minerals':400} for i in newids),
 'mother_hive7_to8_built29_to30_capacity39_other_districts_held':aa['districts']['1']==dict(ba['districts']['1'],level=8) and ba['districts']['1']['level']==7 and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==30 and sum(ba['districts'][str(i)]['level'] for i in ba['colonies']['0']['districts'])==29 and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts'] if i!=1) and ba['planets']['7']==aa['planets']['7'],
 'six_old_labs_two_society_zones_all_original_buildings_raw_held':all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in buildings) and q.ids(q.block(q.block(a['roots']['zones'],'67108970'),'buildings'))==[16777251,83886120,16777323] and q.ids(q.block(q.block(a['roots']['zones'],'119'),'buildings'))==[33554447,50331690,16777354],
 'two_society_zones_plus240_jobs_maintenance_minus240_only':jobs_ok and [aa['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2280,360],
 'housing_plus894_amenities_native_crime0_population_same':aa['colonies']['0']['free_housing']-ba['colonies']['0']['free_housing']==894 and D(str(aa['colonies']['0']['free_amenities']))-D(str(ba['colonies']['0']['free_amenities']))==D('-565.2') and aa['colonies']['0']['crime']==0 and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']==13015,
 'all_eight_nonresearch_cash_held_no_repeat_payment_or_reward':all(v==0 for v in cash.values()) and all(ac['effective_stockpile'][k]>=0 for k in cash_keys),
 'project3_one_old_month_tick_society_bank_exact':bp['special_project']==ap['special_project']==9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-income(bc,'society_research')*D('1.35')-draw)<D('.00005') and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+draw)<D('.00005') and ap['progress']==9317.78873,
 'physics_engineering_idle_banks_exact_one_tick':not research_queue(bc,'engineering_queue') and not research_queue(ac,'engineering_queue') and all(abs(D(str(ac['research_stockpile'][k]))-D(str(bc['research_stockpile'][k]))-income(bc,k)*D('1.35'))<D('.00005') for k in ['physics_research','engineering_research']),
 'cached_month_budget_and_other_tech_shapes_held':bc['budget_categories']==ac['budget_categories'] and dict(bp,progress=ap['progress'])==ap and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'all75_original_ships_identity_native_main_regeneration':len(a['ships'])==len(b['ships'])==75 and set(a['ships'])==set(b['ships']) and life,
 'all35_fleets_same_members_two_support_orbits':len(a['fleets'])==len(b['fleets'])==35 and set(a['fleets'])==set(b['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()) and support_ok,
 'all15_original_armies_raw_held_no_new_ship_order':len(armies)==15 and armies==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in armies) and not q.ids(q.block(a['queues'].get('3',''),'items')),
 'EEP_queen_crisis3_menace3065_government_AP_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==3065,
 'native_flags_only29day_timers_contacts_held':flags(a)==expected_flags and all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'only_one_exact_native_system_survey_no_pending_war_truce_combat':len(news)==1 and q.scalars(news[0])==expected_news and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'CN41_same_production_unfiltered_error':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-first-post-society-hive-completion-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_FIRST_HIVE_AFTER_TWO_SOCIETY_ZONES' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'project3_progress':ap['progress'],'new_hive_level':8,'research_jobs':{i:aa['pop_jobs'][i] for i in ['23','24','25']},'cash_deltas':{k:str(v) for k,v in cash.items()},'new_messages_raw':news,'boundaries':['first_hive_new_month_budget_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Paid first hive completion after two society zones; not project3/C200/Queen3/full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'project3':ap['progress'],'hive_level':aa['districts']['1']['level']}),flush=True);assert passed
