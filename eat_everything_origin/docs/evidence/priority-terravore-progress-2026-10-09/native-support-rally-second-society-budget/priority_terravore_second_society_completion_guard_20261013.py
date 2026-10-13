"""Validate native completion of the second paid society zone and its original labs."""
import json, logging, sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
from priority_terravore_native_state import read_state, omit
logging.disable(logging.INFO)
h = r.harness; run, user, meta = h.load_run()
load = lambda name: json.loads((run/name).read_text('utf-8-sig'))
before = 'terravore-second-society-precomplete-22870101'
after = 'terravore-second-society-completed-22870119'
b, a = [read_state(run, stage) for stage in [before, after]]
ba, aa = b['audit'], a['audit']; bc, ac = ba['countries']['0'], aa['countries']['0']
pre = load(before+'-support-zone-v5-proof.json')
rev = load(before+'-second-society-zone-completion-review.json')
ob = load(after+'-construction-boundary-observation-v4.json')
cal = load(after+'-calendar-receipt.json')
stages = [before+'-support-zone-v5-guard',before+'-second-society-zone-completion-review',after+'-calendar',after+'-boundary-observation-v4']
executions = [load(stage+'-execution.json') for stage in stages]
queue_before = q.ids(q.block(b['queues']['0'],'items'))
queue_after = q.ids(q.block(a['queues']['0'],'items'))
zones_before = {str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295}
zones_after = {str(z) for d in aa['colonies']['0']['districts'] for z in aa['districts'][str(d)]['zones'] if z!=4294967295}
builds_before = {str(i) for z in zones_before for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
builds_after = {str(i) for z in zones_after for i in q.ids(q.block(q.block(a['roots']['zones'],z),'buildings')) if i!=4294967295}

def research_queue(country,key):
    raw=country['research_queues'].get(key,''); ts=list(q.tokens(raw))
    return q.scalars(raw[ts[0][2]:ts[-1][1]]) if ts else {}

def income(country,key):
    return sum((D(str(v.get(key,0))) for v in country['budget_categories']['current_month']['income'].values()),D(0))

def flags(state):
    return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(state['country'],'flags'))}

bp,ap=[research_queue(c,'society_queue') for c in [bc,ac]]
draw=min(income(bc,'society_research'),D(str(bc['research_stockpile']['society_research'])))
cash_keys=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']
cash={k:str(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))) for k in cash_keys}
oldjobs,newjobs=ba['pop_jobs'],aa['pop_jobs']
jobs_ok=oldjobs['23']==newjobs['23'] and [oldjobs[i]['max_workforce'] for i in ['24','25']]==[1200,1200] and [newjobs[i]['max_workforce'] for i in ['24','25']]==[2040,360]
for i in ['24','25']:
    old,now=oldjobs[i],newjobs[i]
    jobs_ok=jobs_ok and all(now[k]==now['max_workforce'] for k in ['workforce','workforce_limit','automated_workforce_limit']) and D(str(now['bonus_workforce']))==D(str(now['workforce']))*D('.35') and all(old[k]==now[k] for k in ['type','automated_workforce','planet','pop_group'])
jobs_ok=jobs_ok and sum(oldjobs[i]['max_workforce'] for i in ['23','24','25'])==sum(newjobs[i]['max_workforce'] for i in ['23','24','25'])
orbitals=q.scalars(q.block(q.block(q.block(a['roots']['planets'],'planet'),'1732'),'planet_orbitals'))
support_ok=True
for fid,index in [('917',1),('50332250',2)]:
    fleet=a['fleets'][fid];mm=q.block(fleet,'movement_manager')
    support_ok=support_ok and not q.block(fleet,'current_order') and q.scalars(q.block(mm,'coordinate'))['origin']==164 and q.scalars(q.block(mm,'orbit'))=={'index':index} and q.scalars(q.block(q.block(mm,'orbit'),'orbitable'))=={'planet':1732} and orbitals.get(str(index))==int(fid) and q.block(fleet,'movement_manager')==q.block(b['fleets'][fid],'movement_manager') and q.ids(q.block(fleet,'ships'))==q.ids(q.block(b['fleets'][fid],'ships'))
main={str(i) for i in q.ids(q.block(b['fleets']['83886903'],'ships'))}
support_ships={str(i) for fid in ['917','50332250'] for i in q.ids(q.block(b['fleets'][fid],'ships'))}
life=True; healing={}
for i,v in b['ships'].items():
    av=a['ships'].get(i,''); old,now=q.scalars(v),q.scalars(av)
    life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and all(old.get(k)==now.get(k) for k in ['construction_date','killed','max_hitpoints','max_armor_hitpoints','max_shield_hitpoints'])
    if i in main:
        healing[i]={}
        for key,cap in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints')]:
            expected=min(D(str(old[cap])),D(str(old.get(key,0)))+D(str(old[cap]))*D('.0025')*18)
            actual=D(str(now.get(key,0)))
            healing[i][key]={'expected':str(expected),'actual':str(actual)}
            life=life and abs(actual-expected)<D('.0001')
        life=life and now.get('shield_hitpoints',0)==0 and now.get('hitpoints',0)>0
    else:
        life=life and all(old.get(k)==now.get(k) for k in ['hitpoints','armor_hitpoints'])
        if i in support_ships:life=life and now.get('shield_hitpoints',0)==0
        else:life=life and old.get('shield_hitpoints')==now.get('shield_hitpoints')
army=q.ids(q.block(b['country'],'owned_armies'))
expected_flags={k:dict(v,flag_days=v['flag_days']-18) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>18}
checks={
    'review5PASS_calendar_observer6PASS_all_actual0_sources_originalSAV': len(rev['checks'])==5 and len(ob['checks'])==6 and all(v is True for proof in [pre,rev,ob] for v in proof['checks'].values()) and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in executions) and pre['after_sha256']==rev['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
    'native18day_exact_boundary_and_one_research_tick_no_month_cash': ba['date']=='2287.01.01' and aa['date']=='2287.01.19' and cal['days']==18 and cal['date']==aa['date'] and cal['review_file']==Path(before+'-second-society-zone-completion-review.json').name and rev['end_date']==aa['date'],
    'paid800_order_consumed_four_original_hives_exact_held': queue_before==[201326629,1191182345,117440553,1476395019,117440546] and queue_after==queue_before[1:] and '201326629' not in a['items'] and all(a['items'][str(i)]==b['items'][str(i)] for i in queue_after),
    'only_engineering_zone_replaced_by_society_zone119_three_original_labs': zones_after-zones_before=={'119'} and zones_before-zones_after=={'16777330'} and not q.block(a['roots']['zones'],'16777330') and q.scalars(q.block(a['roots']['zones'],'119'))=={'type':'zone_research_society'} and q.ids(q.block(q.block(a['roots']['zones'],'119'),'buildings'))==[33554447,50331690,16777354] and builds_before==builds_after and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in builds_before),
    'other_zones_districts_and_mother_capacity_held': all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones_before if z!='16777330') and aa['districts']['1']==dict(ba['districts']['1'],zones=[0,67108970,119]) and all(ba['districts'][str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts'] if i!=1) and ba['planets']['7']==aa['planets']['7'] and bc['owned_colonies']==ac['owned_colonies']==[0],
    'original_2760_research_jobs_only_840_transfer_to_society': jobs_ok,
    'all_eight_nonresearch_cash_balances_exact_no_second_payment': all(D(value)==0 for value in cash.values()) and all(D(str(ac['effective_stockpile'][k]))>=0 for k in cash_keys),
    'project3_exact_one_old_month_tick_and_society_bank_draw': bp['special_project']==ap['special_project']==9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-income(bc,'society_research')*D('1.35')-draw)<D('.00005') and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+draw)<D('.00005') and ap['progress']<12000,
    'physics_engineering_idle_true_banks_old_month_tick': not research_queue(ac,'engineering_queue') and all(abs(D(str(ac['research_stockpile'][k]))-D(str(bc['research_stockpile'][k]))-income(bc,k)*D('1.35'))<D('.00005') for k in ['physics_research','engineering_research']),
    'cached_month_budget_and_other_technology_shapes_held': bc['budget_categories']==ac['budget_categories'] and dict(bp,progress=ap['progress'])==ap and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue'}),
    'both_supports_original_registered_orbit1732_no_move': support_ok,
    'all75_original_ships_identity_native_main_regeneration': len(b['ships'])==len(a['ships'])==75 and set(b['ships'])==set(a['ships']) and life,
    'all35_original_fleets_same_members_no_new_ship_orders': len(b['fleets'])==len(a['fleets'])==35 and set(b['fleets'])==set(a['fleets']) and all(q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships')) for i,v in b['fleets'].items()) and not q.ids(q.block(a['queues'].get('3',''),'items')),
    'all15_original_armies_raw_held': len(army)==15 and army==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in army),
    'mother_only_same_population_housing_amenities_crime0': aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']==12947 and ob['before_state']['species_population_by_colony']==ob['after_state']['species_population_by_colony']=={'0:73':12947} and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0,
    'EEP_queen_crisis3_menace3065_government_AP_held': all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==3065,
    'native_flags_18days_contacts_and_other_owned_queues_held': flags(a)==expected_flags and all(q.block(q.block(a['roots']['first_contacts'],'contacts'),i)==q.block(q.block(b['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']) and all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0),
    'no_new_messages_pending_war_truce_combat': not ob['new_country0_messages_raw'] and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()),
    'CN41_same_production_tree_unfiltered_error_held': meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values())
out=run/(after+'-second-society-zone-completion-proof.json'); assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_SECOND_PAID_SOCIETY_ZONE' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'new_zone':119,'old_zone':16777330,'retained_labs':[33554447,50331690,16777354],'jobs':{i:aa['pop_jobs'][i] for i in ['23','24','25']},'project3_progress':ap['progress'],'cash_delta':cash,'healing':healing,'boundaries':['post_second_society_conversion_month_budget_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Paid second zone conversion only; not project3/C200/Queen3 or full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'project3':ap['progress'],'new_zone':119}),flush=True)
assert passed
