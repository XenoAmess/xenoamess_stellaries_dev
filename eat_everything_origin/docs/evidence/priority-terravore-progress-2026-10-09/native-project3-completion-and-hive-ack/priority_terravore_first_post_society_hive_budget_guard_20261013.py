"""Validate native new-month ledger after the first hive added to two society zones."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-first-post-conversion-hive-completed-22871230';after='terravore-first-post-hive-budget-22880101-v2'
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
p=load(before+'-first-post-society-hive-completion-proof.json');rev=load(before+'-first-hive-budget-review-v2.json');ob=load(after+'-construction-boundary-observation-v4.json');cal=load(after+'-calendar-receipt.json')
xs=[load(s+'-execution.json') for s in [before+'-first-post-society-hive-completion-guard',before+'-first-hive-budget-review-v2',after+'-calendar',after+'-boundary-observation-v4']]
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
expected={k:D(str(bc['effective_stockpile'].get(k,0)))+net[k] for k in resources};expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade'])
residual={k:D(str(ac['effective_stockpile'].get(k,0)))-expected[k] for k in resources}
ids=q.ids(q.block(b['queues']['0'],'items'));zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295}
buildings={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
growthraw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(growthraw));growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
def flags(s):return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
old_income,new_income=[c['budget_categories']['current_month']['income'] for c in [bc,ac]]
old_exp,new_exp=[c['budget_categories']['current_month']['expenses'] for c in [bc,ac]]
orbitals=q.scalars(q.block(q.block(q.block(a['roots']['planets'],'planet'),'1732'),'planet_orbitals'));support=True
for fid,index in [('917',1),('50332250',2)]:
    fleet=a['fleets'][fid];mm=q.block(fleet,'movement_manager')
    support=support and not q.block(fleet,'current_order') and q.scalars(q.block(mm,'orbit'))=={'index':index} and q.scalars(q.block(q.block(mm,'orbit'),'orbitable'))=={'planet':1732} and orbitals.get(str(index))==int(fid) and mm==q.block(b['fleets'][fid],'movement_manager')
main={str(i) for i in q.ids(q.block(b['fleets']['83886903'],'ships'))};support_ships={str(i) for fid in ['917','50332250'] for i in q.ids(q.block(b['fleets'][fid],'ships'))};life=True
for i,v in b['ships'].items():
    av=a['ships'].get(i,'');old,now=q.scalars(v),q.scalars(av)
    life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and all(old.get(k)==now.get(k) for k in ['construction_date','killed','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
    if i in main:
        for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
            wanted=min(D(str(old[cap])),D(str(old.get(key,0)))+D(str(old[cap]))*D('.0025'))
            life=life and abs(D(str(now.get(key,0)))-wanted)<D('.0001')
        life=life and now.get('shield_hitpoints',0)==0 and now.get('hitpoints',0)>0
    else:
        life=life and all(old.get(k)==now.get(k) for k in ['hitpoints','armor_hitpoints'])
        life=life and (now.get('shield_hitpoints',0)==0 if i in support_ships else old.get('shield_hitpoints')==now.get('shield_hitpoints'))
armies=q.ids(q.block(b['country'],'owned_armies'))
checks={
 'prior18PASS_corrected_review6PASS_calendar_observer6PASS_actual0_originalSAV':len(p['checks'])==18 and len(rev['checks'])==6 and len(ob['checks'])==6 and all(v is True for pp in [p,rev,ob] for v in pp['checks'].values()) and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs) and p['after_sha256']==rev['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'native_one_day_to_Jan1_no_day2_tick':ba['date']=='2287.12.30' and aa['date']=='2288.01.01' and cal['days']==1 and cal['start_date']==ba['date'] and cal['date']==aa['date'] and rev['days']==1,
 'all_eight_cash_new_month_native_net_caps_exact':all(abs(v)<D('.00005') for v in residual.values()) and all(ac['effective_stockpile'][k]>=0 for k in resources),
 'society2280_job_income_and_mineral_cost_exact_original_ratio':D(str(new_income['planet_biologists']['society_research']))==D(str(old_income['planet_biologists']['society_research']))*D(2280)/D(2040) and D(str(new_exp['planet_biologists']['minerals']))==D(str(old_exp['planet_biologists']['minerals']))*D(2280)/D(2040) and new_income['planet_engineers']==old_income['planet_engineers'] and new_income['planet_physicists']==old_income['planet_physicists'] and new_exp['planet_engineers']==old_exp['planet_engineers'] and new_exp['planet_physicists']==old_exp['planet_physicists'],
 'native_hive_energy_maintenance_and_trade_deltas_exact':D(str(new_exp['planet_districts_cities']['energy']))-D(str(old_exp['planet_districts_cities']['energy']))==D('1.8') and old_income['planet_maintenance_drones']['trade']==63.79212 and new_income['planet_maintenance_drones']['trade']==60.05748 and old_income['trade_policy']['trade']==90.43181 and new_income['trade_policy']['trade']==86.69042 and new_exp['planet_pops_traits']['minerals']==117.135 and new_exp['ships']==old_exp['ships'] and new_exp['ship_components']==old_exp['ship_components'] and new_exp['ships']['minerals']==74.72517,
 'project3_all_research_banks_queues_native_tech_held_before_Jan2':bc['research_stockpile']==ac['research_stockpile'] and bc['research_queues']==ac['research_queues'] and q.block(b['country'],'tech_status')==q.block(a['country'],'tech_status'),
 'three_paid_hives_only_first_one_day_1point4_work':ids==[117440553,1476395019,117440546] and q.ids(q.block(a['queues']['0'],'items'))==ids and q.scalars(b['items'][str(ids[0])])['progress']==0 and q.scalars(a['items'][str(ids[0])])['progress']==1.4 and omit(b['items'][str(ids[0])],{'progress'})==omit(a['items'][str(ids[0])],{'progress'}) and all(b['items'][str(i)]==a['items'][str(i)] for i in ids[1:]),
 'original_hive8_zones_buildings_jobs_held':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in buildings) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']) and [aa['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2280,360],
 'mother_only_native_species73_growth6_OTHER0':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+growth.get('GROWTH_CAT_GROWTH',0) and growth.get('GROWTH_CAT_GROWTH',0)==6 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'EEP_queen_crisis3_menace3065_government_AP_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==3065,
 'all75_original_ships_identity_native_main_regeneration':len(a['ships'])==len(b['ships'])==75 and set(a['ships'])==set(b['ships']) and life,
 'all35_fleets_same_members_two_support_orbits':len(a['fleets'])==len(b['fleets'])==35 and set(a['fleets'])==set(b['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()) and support,
 'all15_original_armies_raw_held_no_new_ship_order':len(armies)==15 and armies==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in armies) and not q.ids(q.block(a['queues'].get('3',''),'items')),
 'native_flags_only_one_day_contacts_held':flags(a)=={k:dict(v,flag_days=v['flag_days']-1) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>1} and all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'no_new_messages_pending_war_truce_combat':not ob['new_country0_messages_raw'] and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'positive_housing_amenities_crime0_destroyed_source_still_shattered':aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0 and aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0,
 'CN41_same_production_tree_unfiltered_error_held':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-first-post-society-hive-budget-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_FIRST_HIVE_TWO_SOCIETY_BUDGET' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'cash_residual':{k:str(v) for k,v in residual.items()},'growth_details':growth,'project3_progress':9317.78873,'next_hive_work':q.scalars(a['items'][str(ids[0])])['progress'],'boundaries':['project3_completion_bounded_months_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'First native full monthly ledger after hive8; not project3/C200/Queen3 or full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'next_hive_work':q.scalars(a['items'][str(ids[0])])['progress']}),flush=True);assert passed
