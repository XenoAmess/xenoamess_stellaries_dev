"""Validate first native month ledger after the second paid society-zone conversion."""
import json, logging, sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO)
h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-second-society-completed-22870119';after='terravore-second-society-first-budget-22870201-v2'
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
p=load(before+'-second-society-zone-completion-proof.json');rev=load(before+'-second-society-first-budget-review-v2.json');ob=load(after+'-construction-boundary-observation-v4.json');cal=load(after+'-calendar-receipt.json')
xs=[load(s+'-execution.json') for s in [before+'-second-society-zone-completion-guard',before+'-second-society-first-budget-review-v2',after+'-calendar',after+'-boundary-observation-v4']]
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']
net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
expected={k:D(str(bc['effective_stockpile'].get(k,0)))+net[k] for k in resources};expected['influence']=min(D(1000),expected['influence']);expected['trade']=min(D(50000),expected['trade'])
residual={k:D(str(ac['effective_stockpile'].get(k,0)))-expected[k] for k in resources}
ids=q.ids(q.block(b['queues']['0'],'items'));front=str(ids[0]);zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295}
buildings={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
growthraw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details');fs=list(q.fields(growthraw));growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
flags=lambda s:{k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
old_income=bc['budget_categories']['current_month']['income'];new_income=ac['budget_categories']['current_month']['income'];old_exp=bc['budget_categories']['current_month']['expenses'];new_exp=ac['budget_categories']['current_month']['expenses']
support_ok=True;orbitals=q.scalars(q.block(q.block(q.block(a['roots']['planets'],'planet'),'1732'),'planet_orbitals'))
for fid,index in [('917',1),('50332250',2)]:
    fm=a['fleets'][fid];mm=q.block(fm,'movement_manager')
    support_ok=support_ok and not q.block(fm,'current_order') and q.scalars(q.block(mm,'orbit'))=={'index':index} and q.scalars(q.block(q.block(mm,'orbit'),'orbitable'))=={'planet':1732} and orbitals.get(str(index))==int(fid) and mm==q.block(b['fleets'][fid],'movement_manager')
main={str(i) for i in q.ids(q.block(b['fleets']['83886903'],'ships'))};support_ships={str(i) for fid in ['917','50332250'] for i in q.ids(q.block(b['fleets'][fid],'ships'))};life=True
for i,v in b['ships'].items():
    av=a['ships'].get(i,'');bs,now=q.scalars(v),q.scalars(av)
    life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and all(bs.get(k)==now.get(k) for k in ['construction_date','killed','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
    if i in main:
        for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
            wanted=min(D(str(bs[cap])),D(str(bs.get(key,0)))+D(str(bs[cap]))*D('.0025')*12)
            life=life and abs(D(str(now.get(key,0)))-wanted)<D('.0001')
        life=life and now.get('shield_hitpoints',0)==0 and now.get('hitpoints',0)>0
    else:
        life=life and all(bs.get(k)==now.get(k) for k in ['hitpoints','armor_hitpoints'])
        life=life and (now.get('shield_hitpoints',0)==0 if i in support_ships else bs.get('shield_hitpoints')==now.get('shield_hitpoints'))
armies=q.ids(q.block(b['country'],'owned_armies'))
checks={
 'prior19PASS_review5PASS_calendar_observer6PASS_all_actual0_originalSAV':len(p['checks'])==19 and len(rev['checks'])==5 and len(ob['checks'])==6 and all(v is True for pp in [p,rev,ob] for v in pp['checks'].values()) and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs) and p['after_sha256']==rev['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact12day_native_one_month_no_research_tick':ba['date']=='2287.01.19' and aa['date']=='2287.02.01' and cal['days']==12 and cal['start_date']==ba['date'] and cal['date']==aa['date'] and cal['review_file']==before+'-second-society-first-budget-review-v2.json',
 'all_eight_cash_native_new_month_balance_exact_no_repeat_payment':all(abs(v)<D('.00005') for v in residual.values()) and all(ac['effective_stockpile'][k]>=0 for k in resources),
 'society_engineering_income_exact_original_job_transfer':D(str(new_income['planet_biologists']['society_research']))==D(str(old_income['planet_biologists']['society_research']))*D('1.7') and D(str(new_income['planet_engineers']['engineering_research']))==D(str(old_income['planet_engineers']['engineering_research']))*D('.3') and new_income['planet_physicists']==old_income['planet_physicists'] and [aa['pop_jobs'][i]['workforce'] for i in ['23','24','25']]==[360,2040,360],
 'research_job_mineral_upkeep_exact_transfer_ship_cost_held':D(str(new_exp['planet_biologists']['minerals']))==D(str(old_exp['planet_biologists']['minerals']))*D('1.7') and D(str(new_exp['planet_engineers']['minerals']))==D(str(old_exp['planet_engineers']['minerals']))*D('.3') and new_exp['planet_physicists']==old_exp['planet_physicists'] and new_exp['ships']==old_exp['ships'] and new_exp['ship_components']==old_exp['ship_components'] and D(str(new_exp['ships']['minerals']))==D('74.72517'),
 'project3_and_all_research_banks_queues_held_before_Feb2':bc['research_stockpile']==ac['research_stockpile'] and bc['research_queues']==ac['research_queues'] and q.block(b['country'],'tech_status')==q.block(a['country'],'tech_status'),
 'four_paid_hives_only_front_plus16point8_tail_raw_held':ids==[1191182345,117440553,1476395019,117440546] and q.ids(q.block(a['queues']['0'],'items'))==ids and abs(D(str(q.scalars(a['items'][front])['progress']))-D(str(q.scalars(b['items'][front])['progress']))-D('16.8'))<D('.00005') and omit(b['items'][front],{'progress'})==omit(a['items'][front],{'progress'}) and all(b['items'][str(i)]==a['items'][str(i)] for i in ids[1:]),
 'all_original_zones_buildings_districts_research_jobs_held':ba['planets']['7']==aa['planets']['7'] and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in buildings) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']),
 'mother_only_natural_growth6_OTHER0_species73':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+growth.get('GROWTH_CAT_GROWTH',0) and growth.get('GROWTH_CAT_GROWTH',0)==6 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'EEP_queen_crisis3_menace3065_government_AP_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==3065,
 'all75_ships_original_identity_native_main_regeneration':len(a['ships'])==len(b['ships'])==75 and set(a['ships'])==set(b['ships']) and life,
 'all35_fleets_same_members_two_support_orbits_held':len(a['fleets'])==len(b['fleets'])==35 and set(a['fleets'])==set(b['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()) and support_ok,
 'all15_original_armies_raw_held_no_new_ship_orders':len(armies)==15 and armies==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in armies) and not q.ids(q.block(a['queues'].get('3',''),'items')),
 'timed_flags_only_minus12_contacts_held':flags(a)=={k:dict(v,flag_days=v['flag_days']-12) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>12} and all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'no_new_messages_pending_war_truce_combat':not ob['new_country0_messages_raw'] and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
 'positive_housing_amenities_crime0_destroyed_source_still_shattered':aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0 and aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0,
 'CN41_same_production_tree_unfiltered_error_held':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-second-society-first-budget-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_SECOND_SOCIETY_FIRST_BUDGET' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'cash_residual':{k:str(v) for k,v in residual.items()},'growth_details':growth,'project3_progress':6218.77182,'hive_front_work':q.scalars(a['items'][front])['progress'],'boundaries':['project3_normal_months_and_next_paid_hive_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'First month budget after second paid society-zone conversion, not full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'hive_work':q.scalars(a['items'][front])['progress']}),flush=True);assert passed
