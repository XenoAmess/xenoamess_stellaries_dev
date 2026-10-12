"""Actual two-day project2 completion; original pending event295 retained."""
import json,logging,sys
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-native-project2-event-acknowledged';after='terravore-native-level3-and-project3-notice-22821007';b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
ob=load(after+'-construction-boundary-observation-v4.json');pre=load(before+'-native-level3-unlock-review.json');xs=[load(s+'-execution.json') for s in [after+'-calendar',after+'-boundary-observation-v4',before+'-native-level3-unlock-review']]
ids=q.ids(q.block(b['queues']['0'],'items'));zones={str(i) for col in bc['owned_colonies'] for d in ba['colonies'][str(col)]['districts'] for i in ba['districts'][str(d)]['zones'] if i!=4294967295}
oldbuild={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295};newbuild={str(i) for z in zones for i in q.ids(q.block(q.block(a['roots']['zones'],z),'buildings')) if i!=4294967295};added=newbuild-oldbuild
def queue(c,k):
 raw=c['research_queues'][k];ts=list(q.tokens(raw));return q.scalars(raw[ts[0][2]:ts[-1][1]])
bp={};ap={};be,ae=queue(bc,'engineering_queue'),queue(ac,'engineering_queue');income={k:sum((D(str(v.get(k,0))) for v in bc['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES};draw=min(income['physics_research'],D(str(bc['research_stockpile']['physics_research'])))
armies=q.ids(q.block(b['country'],'owned_armies'))
projects=lambda state:{q.scalars(v)['id']:v for k,v,obj in q.fields(q.block(state['country'],'events')) if obj and k=='special_project'}
bpr,apr=projects(b),projects(a);project_ok=bpr.keys()==apr.keys() and all(omit(v,{'days_left'})==omit(apr[i],{'days_left'}) and ('days_left' not in q.scalars(v) or q.scalars(apr[i])['days_left']==q.scalars(v)['days_left']-4) for i,v in bpr.items())
bflags=q.block(b['country'],'flags');aflags=q.block(a['country'],'flags');bf,af=q.scalars(bflags),q.scalars(aflags)
flag_ok=bf==af and set(k for k,v,obj in q.fields(bflags))==set(k for k,v,obj in q.fields(aflags)) and all(q.scalars(q.block(aflags,k))==dict(q.scalars(v),flag_days=q.scalars(v)['flag_days']-4) for k,v,obj in q.fields(bflags) if obj)
pre['sources']=load('terravore-remaining-labs-normal-month-22821001-project2-completion-review.json')['sources']
f=h.GAME_EXE.parent/'common/menace_perks/00_menace_perks.txt';dest=run/'terravore-level3-native-00_menace_perks.txt'
if dest.exists():assert dest.read_bytes()==f.read_bytes()
else:dest.write_bytes(f.read_bytes())
pre['sources'].append({'path':str(f),'preserved':dest.name,'sha256':h.sha256(f)})
levels=lambda state:[q.unquote(v) for k,v,obj in q.fields(q.block(state['country'],'crisis_progression')) if k=='level' and not obj]

checks={
 'review4PASS_observer6PASS_calendar_actual0_sources_bound':len(pre['checks'])==4 and len(ob['checks'])==6 and all(v is True for p in [pre,ob] for v in p['checks'].values()) and all(x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in xs),
 'original_SAV_pair_native4days_exact_dates':ba['date']=='2282.10.03' and aa['date']=='2282.10.07' and load(after+'-calendar-receipt.json')['days']==4 and pre['after_sha256']==ob['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'paid_front_lab_native_work5p6_all_other_paid_items_held':q.ids(q.block(a['queues']['0'],'items'))==ids and all(a['items'][str(i)]==b['items'][str(i)] for i in ids[1:]) and omit(a['items']['184549419'],{'progress'})==omit(b['items']['184549419'],{'progress'}) and D(str(q.scalars(a['items']['184549419'])['progress']))-D(str(q.scalars(b['items']['184549419'])['progress']))==D('5.6'),
 'no_new_buildings_owned_zones_or_free_construction':newbuild==oldbuild and not added and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones),
 'all_old_owned_buildings_other_zones_and_districts_held':all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in oldbuild) and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones if z!='16777330') and all(ba['districts'][str(i)]==aa['districts'][str(i)] for col in bc['owned_colonies'] for i in ba['colonies'][str(col)]['districts']),
 'all_original_P840_S240_E840_jobs_held':all(aa['pop_jobs'][i]==ba['pop_jobs'][i] and aa['pop_jobs'][i]['workforce']==v for i,v in [('23',840),('24',240),('25',840)]),
 'all_nonresearch_cash_exact_no_repeat_charge_or_reward':all(v==ac['effective_stockpile'][k] for k,v in bc['effective_stockpile'].items() if k not in q.RESEARCH_RESOURCES),
 'native_crisis_only_level3_added_objectives_held':levels(b)==['crisis_level_1','crisis_level_2'] and levels(a)==['crisis_level_1','crisis_level_2','crisis_level_3'] and omit(q.block(b['country'],'crisis_progression'),{'level'})==omit(q.block(a['country'],'crisis_progression'),{'level'}) and project_ok,
 'all_research_banks_tech_and_budget_held_no_repeated_tick':bc['research_stockpile']==ac['research_stockpile'] and bc['tech_status']==ac['tech_status'] and bc['budget_categories']==ac['budget_categories'],
 'both_colonies_population_species_total_no_free_population':all(ba['colonies'][c]['actual_pop_sum']==aa['colonies'][c]['actual_pop_sum'] for c in ['0','30']) and ob['before_state']['species_population_by_colony']==ob['after_state']['species_population_by_colony'],
 'EEP_all_variables_flags_government_AP_crisis_situation_held':flag_ok and all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis','owned_colonies']) and ba['situations']==aa['situations'],
 'all61_original_ships34fleets_birth_name_design_life_held':len(a['ships'])==61 and set(b['ships'])==set(a['ships']) and len(a['fleets'])==34 and set(b['fleets'])==set(a['fleets']) and all(all(q.scalars(v).get(k)==q.scalars(a['ships'][i]).get(k) for k in ['construction_date','hitpoints','max_hitpoints','armor_hitpoints','shield_hitpoints']) and q.block(v,'ship_design_implementation')==q.block(a['ships'][i],'ship_design_implementation') and q.block(v,'name')==q.block(a['ships'][i],'name') for i,v in b['ships'].items()),
 'all_original_armies_held_only_native_defense250_to475_cache':armies==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) or q.scalars(q.block(b['roots']['army'],str(i))).get('colony')==30 and omit(q.block(b['roots']['army'],str(i)),{'health','max_health'})==omit(q.block(a['roots']['army'],str(i)),{'health','max_health'}) and q.scalars(q.block(b['roots']['army'],str(i)))['health']==250 and q.scalars(q.block(a['roots']['army'],str(i)))['health']==q.scalars(q.block(a['roots']['army'],str(i)))['max_health']==475 for i in armies),
 'only_pending296_native4150_and_message_no_Queen_war_or_other_orders':len(a['pending'])==1 and q.scalars(a['pending'][0])=={'id':296,'event':'crisis.4150','date':'2285.01.07','country':0} and len(ob['new_country0_messages_raw'])==1 and q.scalars(ob['new_country0_messages_raw'][0])=={'type':'EVENT_MESSAGE_TYPE','text':'\x11H\u4ed6\u4eec\u5c06\u8dea\u670d\x11!','receiver':0,'date':'2282.10.07','event':296,'message_type':'none'} and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and all(v==a['queues'][i] for i,v in b['queues'].items() if i!='0' and q.scalars(v)['owner']==0),
 'mother35_built27_amenities_housing_positive_crime0':ba['planets']['7']==aa['planets']['7'] and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'CN41_same_package_exact_error627_and_native_sources':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and reviewed_error_pair((run/(before+'-error-after.log')).read_bytes(),(run/(after+'-error-after.log')).read_bytes(),run) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes() and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in pre['sources']),
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-level3-notice-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_LEVEL3_ORIGINAL_NOTICE_PENDING' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'added_buildings':sorted(added),'project2_completed':True,'boundaries':['native_pending296_crisis4150_confirmation'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Original project2 completed with pending295; confirm native event before continuation; no free rewards or full route claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'added_buildings':sorted(added),'project2_completed':True}),flush=True);assert passed
