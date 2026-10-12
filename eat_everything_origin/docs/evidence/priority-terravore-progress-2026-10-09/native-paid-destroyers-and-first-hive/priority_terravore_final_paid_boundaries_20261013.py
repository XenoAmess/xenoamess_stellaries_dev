"""Documented first paid hive, last paid pair, then native full-fleet budget. No grants."""
import json, logging, sys
from decimal import Decimal as D, ROUND_DOWN
from pathlib import Path
mode, kind, before, other, prior, execution = sys.argv[1:]
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
from priority_terravore_native_state import read_state, omit
logging.disable(logging.INFO); h = r.harness; run, user, m = h.load_run()
load = lambda n: json.loads((run/n).read_text('utf-8-sig'))
def day(s):
 y, mo, d = map(int, s.split('.')); return y*360+(mo-1)*30+d-1
def checked(x):
 return x['returncode'] == 0 and x['helper_sha256'] == h.sha256(Path(x['command'][1]))
def rq(c, k):
 raw = c['research_queues'][k]; ts = list(q.tokens(raw)); return q.scalars(raw[ts[0][2]:ts[-1][1]])
def flags(s):
 return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
b = read_state(run,before); ba=b['audit']; bc=ba['countries']['0']; p=load(prior); px=load(execution+'-execution.json')
end, days = {'hive':('2285.05.16',15), 'pair':('2285.05.24',8), 'budget':('2285.06.01',7)}[kind]
basic=p['status'].startswith('PASS') and bool(p['checks']) and all(v is True for v in p['checks'].values()) and checked(px) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav'))
package=m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7'
ids=q.ids(q.block(b['queues'].get('3',''),'items')); hives=q.ids(q.block(b['queues']['0'],'items')); eps=D('.00003')
suffix='-final-paid-'+kind
if mode=='review':
 checks={
  'prior_business_PASS_actual0_source_SAV_bound':basic,
  'exact_documented_single_boundary_date':other==end and day(end)-day(ba['date'])==days,
  'only_expected_prepaid_orders_no_pending':not b['pending'] and hives==([268435492,251658284,1191182345,117440553,1476395019,117440546] if kind=='hive' else [251658284,1191182345,117440553,1476395019,117440546]) and ids==([167772178,922746888] if kind!='budget' else []) and all(q.scalars(q.block(b['items'][str(i)],'resources'))=={'minerals':412.5} for i in ids) and q.scalars(b['items'][str(hives[0])])['progress']<480,
  'CN41_unfiltered_live_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 }
 passed=all(v is True for v in checks.values()); out=run/(before+suffix+'-review.json'); assert not out.exists()
 h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':ba['save_sha256'],'start_date':ba['date'],'end_date':end,'days':days,'maximum_days':days,'allowed_boundaries':p['boundaries'],'execution_stage':before+suffix+'-review'})
 print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True); assert passed; sys.exit(0)
assert mode=='guard'; after=other; a=read_state(run,after); aa=a['audit']; ac=aa['countries']['0']
ob=load(after+'-construction-boundary-observation-v4.json'); ox=load(after+'-boundary-observation-v4-execution.json'); cal=load(after+'-calendar-receipt.json'); cx=load(after+'-calendar-execution.json'); review=load(before+suffix+'-review.json'); rx=load(before+suffix+'-review-execution.json')
bp,ap=rq(bc,'society_queue'),rq(ac,'society_queue'); be,ae=rq(bc,'engineering_queue'),rq(ac,'engineering_queue')
income=lambda c:{k:sum((D(str(v.get(k,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bi,ai=income(bc),income(ac); tick=1 if kind=='hive' else 0; draw=min(bi['society_research'],D(str(bc['research_stockpile']['society_research'])))*tick
resources=['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']; net={k:sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0)) for k in resources}
expected={k:D(str(bc['effective_stockpile'].get(k,0)))+(v if kind=='budget' else 0) for k,v in net.items()}; expected['influence']=min(D(1000),expected['influence']); expected['trade']=min(D(50000),expected['trade']); residual={k:D(str(ac['effective_stockpile'].get(k,0)))-v for k,v in expected.items()}
new=set(a['ships'])-set(b['ships']); removed=ids if kind=='pair' else []; remaining=[] if kind=='pair' else ids
ef={k:dict(v,flag_days=v['flag_days']-days) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>days}
if kind=='pair': ef['built_artificial_ship']=63539112+24*(day(end)-day('2284.08.14'))
zones={str(z) for d in ba['colonies']['0']['districts'] for z in ba['districts'][str(d)]['zones'] if z!=4294967295}; builds={str(i) for z in zones for i in q.ids(q.block(q.block(b['roots']['zones'],z),'buildings')) if i!=4294967295}
army=q.ids(q.block(b['country'],'owned_armies')); news=ob['new_country0_messages_raw']; ex=ac['budget_categories']['current_month']['expenses']
sources=load('terravore-destroyer-first-upkeep-22840901-destroyer-first-upkeep-proof.json')['native_sources']+load('terravore-destroyer-first-pair-born-22840814-destroyer-first-pair-birth-v3-proof.json')['sources']
rels=['common/districts/00_urban_districts.txt','common/zones/00_zones.txt','common/inline_scripts/zones/shared_research_society_zone.txt','common/inline_scripts/zones/shared_research_engineering_zone.txt','common/inline_scripts/jobs/zone_biologists_add.txt','common/inline_scripts/jobs/zone_engineers_add.txt','common/scripted_variables/100_scripted_variables_zones.txt','events/focus_events_1.txt','common/on_actions/00_on_actions.txt']
for rel in rels:
 src=h.GAME_EXE.parent/rel; dest=run/('first-paid-hive-native-'+src.name)
 if dest.exists(): assert dest.read_bytes()==src.read_bytes()
 else: dest.write_bytes(src.read_bytes())
 sources.append({'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)})
fleet_ok=set(b['fleets'])<=set(a['fleets']); appended=[]
for fid,rawfleet in a['fleets'].items():
 members=q.ids(q.block(rawfleet,'ships')); old=q.ids(q.block(b['fleets'].get(fid,''),'ships')); fleet_ok=fleet_ok and members[:len(old)]==old; additions=members[len(old):]; appended.extend(additions)
 if additions:
  sizes=[]
  for sid in members:
   did=str(q.scalars(q.block(a['ships'][str(sid)],'ship_design_implementation'))['design']); raw=q.block(a['designs'][did],'growth_stages'); ts=list(q.tokens(raw)); size=q.scalars(raw[ts[0][2]:ts[-1][1]])['ship_size']; sizes.append({'crisis_corvette':4,'crisis_destroyer':8}.get(size,999))
  fleet_ok=fleet_ok and sum(sizes)<=90 and set(map(str,additions))<=new and q.scalars(q.block(q.block(q.block(rawfleet,'movement_manager'),'orbit'),'orbitable'))=={'starbase':0}
fleet_ok=fleet_ok and set(map(str,appended))==new and len(appended)==len(new)
growth={}
if kind=='budget':
 raw=q.block(q.block(q.block(a['roots']['colony'],'0'),'last_month_growth_data'),'current_month_growth_details'); fs=list(q.fields(raw)); growth={q.unquote(fs[i][1]):q.unquote(fs[i+1][1]) for i in range(0,len(fs),2)}
jobs_ok=ba['pop_jobs']['23']==aa['pop_jobs']['23']
for jid in ['24','25']:
 old,now=ba['pop_jobs'][jid],aa['pop_jobs'][jid]
 if kind=='hive': jobs_ok=jobs_ok and now['max_workforce']==now['workforce_limit']==now['automated_workforce_limit']==1080 and old['workforce']<=now['workforce']<=1080 and D(str(now['bonus_workforce']))==D(str(now['workforce']))*D('.35') and all(old[k]==now[k] for k in ['type','automated_workforce','planet','pop_group'])
 else: jobs_ok=jobs_ok and old==now
expected_districts={k:v for k,v in ba['districts'].items()}; expected_districts['1']=dict(expected_districts['1'],level=6)
newhives=hives[1:] if kind=='hive' else hives; hive_ok=q.ids(q.block(a['queues']['0'],'items'))==newhives
if kind=='hive': hive_ok=hive_ok and str(hives[0]) not in a['items'] and 0<=q.scalars(a['items'][str(newhives[0])])['progress']<=1.4 and all(a['items'][str(i)]==b['items'][str(i)] for i in newhives[1:]) and omit(b['items'][str(newhives[0])],{'progress'})==omit(a['items'][str(newhives[0])],{'progress'})
else: hive_ok=hive_ok and abs(D(str(q.scalars(a['items'][str(hives[0])])['progress']))-D(str(q.scalars(b['items'][str(hives[0])])['progress']))-D('1.4')*days)<eps and omit(b['items'][str(hives[0])],{'progress'})==omit(a['items'][str(hives[0])],{'progress'}) and all(a['items'][str(i)]==b['items'][str(i)] for i in hives[1:])
checks={
 'prior_review_calendar_observer_actual0_exactSAV_sources':basic and len(ob['checks'])==6+(kind=='budget') and all(v is True for pp in [ob,review] for v in pp['checks'].values()) and all(checked(v) for v in [ox,cx,rx]) and ob['before_sha256']==ba['save_sha256'] and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'single_documented_native_boundary':aa['date']==end and cal['days']==days and cal['date']==end and cal['start_date']==ba['date'] and day(end)-day(ba['date'])==days,
 'cash8_exact_native_ledger_no_duplicate_payment':all(abs(v)<eps for v in residual.values()) and all(ac['effective_stockpile'].get(k,0)>=0 for k in resources),
 'society_project3_only_cached_tick_truebank':bp['special_project']==ap['special_project']==9 and abs(D(str(ap['progress']))-D(str(bp['progress']))-bi['society_research']*D('1.35')*tick-draw)<eps and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+draw)<eps and ap['progress']<12000,
 'engineering_and_idle_physics_only_cached_tick':be['technology']==ae['technology']=='tech_alloys_2' and abs(D(str(ae['progress']))-D(str(be['progress']))-bi['engineering_research']*D('1.35')*tick)<eps and abs(D(str(ac['research_stockpile']['physics_research']))-D(str(bc['research_stockpile']['physics_research']))-bi['physics_research']*D('1.35')*tick)<eps and ae['progress']<2600 and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0,
 'all_other_research_projects_raw_held':dict(bp,progress=ap['progress'])==ap and dict(be,progress=ae['progress'])==ae and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'paid_ship_orders_exact_work_or_final_consumption':q.ids(q.block(a['queues'].get('3',''),'items'))==remaining and all(str(i) not in a['items'] for i in removed) and all(omit(b['items'][str(i)],{'progress'})==omit(a['items'][str(i)],{'progress'}) and abs(D(str(q.scalars(a['items'][str(i)])['progress']))-D(str(q.scalars(b['items'][str(i)])['progress']))-D('1.5')*days)<eps for i in remaining),
 'only_two_final_paid_full_hulls_birth_May24_or_none':len(new)==len(removed) and set(b['ships'])<=set(a['ships']) and all(q.scalars(q.block(a['ships'][i],'ship_design_implementation'))=={'design':83887141,'upgrade':4294967295,'growth_stage':0} and q.scalars(a['ships'][i])['construction_date']==end and q.scalars(q.block(a['ships'][i],'coordinate'))['origin']==0 and all(q.scalars(a['ships'][i])[k]==q.scalars(a['ships'][i])[mk]==val for k,mk,val in [('hitpoints','max_hitpoints',1500),('shield_hitpoints','max_shield_hitpoints',480),('armor_hitpoints','max_armor_hitpoints',765)]) for i in new),
 'all_original_ships_identity_design_name_birth_life_held':all(all(q.scalars(v).get(k)==q.scalars(a['ships'][i]).get(k) for k in ['construction_date','hitpoints','max_hitpoints','armor_hitpoints','shield_hitpoints']) and q.block(v,'ship_design_implementation')==q.block(a['ships'][i],'ship_design_implementation') and q.block(v,'name')==q.block(a['ships'][i],'name') for i,v in b['ships'].items()),
 'original_fleets_members_only_paid_append_within90':fleet_ok,
 'native_naval_capacity_exact_new_size8_hulls':q.scalars(a['country'])['used_naval_capacity']==q.scalars(a['country'])['fleet_size']==q.scalars(b['country'])['used_naval_capacity']+8*len(new),
 'EEP_government_AP_traditions_crisis_menace_no_reward':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions']) and {k:v for k,v in bc['flags'].items() if k.startswith('eep_')}=={k:v for k,v in ac['flags'].items() if k.startswith('eep_')} and q.block(b['country'],'crisis_progression')==q.block(a['country'],'crisis_progression') and ac['effective_stockpile']['menace']==2930,
 'mother_midmonth_population_held_or_only_native_month_growth':bc['owned_colonies']==ac['owned_colonies']==[0] and aa['colonies']['0']['actual_pop_sum']==ba['colonies']['0']['actual_pop_sum']+growth.get('GROWTH_CAT_GROWTH',0) and set(growth)<={'GROWTH_CAT_GROWTH','GROWTH_CAT_OTHER','GROWTH_CAT_PROMOTION'} and 0<=growth.get('GROWTH_CAT_GROWTH',0)<=10 and growth.get('GROWTH_CAT_OTHER',0)==growth.get('GROWTH_CAT_PROMOTION',0)==0 and ob['after_state']['species_population_by_colony']=={'0:73':aa['colonies']['0']['actual_pop_sum']},
 'mother39_paid28_only_hive5_to6_all_zones_labs_held':ba['planets']['7']==aa['planets']['7'] and all(expected_districts[str(i)]==aa['districts'][str(i)] for i in ba['colonies']['0']['districts']) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==28 and all(q.block(b['roots']['zones'],z)==q.block(a['roots']['zones'],z) for z in zones) and all(q.block(b['roots']['buildings'],i)==q.block(a['roots']['buildings'],i) for i in builds),
 'native_research_jobs_120_added_per_existing_specialization':jobs_ok,
 'only_first400M_hive_consumed_or_exact_tail_work':hive_ok,
 'destroyed_source_no_active_EEP_or_return':aa['planets']['1578']['planet_class']=='pc_shattered' and 'owner' not in aa['planets']['1578'] and aa['colonies'].get('30',{}).get('actual_pop_sum',0)==0 and all(v.get('killed')=='yes' for v in aa['situations'].values()),
 'all15_original_armies_raw_held':len(army)==15 and army==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in army),
 'country_flags_timers_exact_no_hive_flag_refresh':flags(a)==ef,
 'native_player_contacts_raw_held':all(q.block(q.block(b['roots']['first_contacts'],'contacts'),i)==q.block(q.block(a['roots']['first_contacts'],'contacts'),i) for i in ['63','64','65']),
 'no_unknown_messages_pending_wars_truces_combat_orders':not a['pending'] and all(q.scalars(v).get('type')=='SYSTEM_SURVEYED' and q.scalars(v).get('localization')=='MESSAGE_FLEET_SYSTEM_FULLY_SURVEYED' for v in news) and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0),
 'positive_housing_amenities_no_crime':aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['crime']==0,
 'CN41_all_native_sources_unfiltered_error_same':package and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources),
}
if kind!='budget': checks['midmonth_budget_unchanged']=bc['budget_categories']==ac['budget_categories'] and bi==ai
else:
 month_start=load('terravore-paid-destroyer-operating-22850501.audit.json'); mc=month_start['countries']['0']; bf=(D(245)/D(131)).quantize(D('.00001'),rounding=ROUND_DOWN); af=(D(261)/D(131)).quantize(D('.00001'),rounding=ROUND_DOWN); oldex=mc['budget_categories']['current_month']['expenses']['ships']; ratio=af/bf
 expected_ship={'alloys':D(str(oldex['alloys']))*ratio,'minerals':D(str(oldex['minerals']))*ratio+D(2)*2*D('.75')*af,'energy':(D(str(oldex['energy']))-3)*ratio+3+D(2)*2*D('.75')*af}
 checks['all16_paid_hulls_first_real_native_budget261_131']=q.scalars(a['country'])['used_naval_capacity']==261 and len([v for v in a['ships'].values() if q.scalars(q.block(v,'ship_design_implementation'))['design']==83887141])==16 and all(abs(D(str(ex['ships'][k]))-v)<D('.001') for k,v in expected_ship.items())
 checks['new_hive_research_income_matches_actual_job_workforce']=all(abs(D(str(ac['budget_categories']['current_month']['income'][cat][res]))-D(str(mc['budget_categories']['current_month']['income'][cat][res]))*D(str(aa['pop_jobs'][jid]['workforce']))/D(str(month_start['pop_jobs'][jid]['workforce'])))<D('.001') for cat,res,jid in [('planet_biologists','society_research','24'),('planet_engineers','engineering_research','25')])
passed=all(v is True for v in checks.values()); out=run/(after+suffix+'-proof.json'); assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_FINAL_PAID_'+kind.upper() if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'sources':sources,'new_ship_ids':sorted(new,key=int),'consumed_paid_orders':removed,'remaining_paid_orders':remaining,'hive_orders':newhives,'hive_head_work':q.scalars(a['items'][str(newhives[0])])['progress'],'project3_progress':ap['progress'],'engineering_progress':ae['progress'],'growth_details':growth,'research_jobs':{i:aa['pop_jobs'][i] for i in ['23','24','25']},'cash_residual':{k:str(v) for k,v in residual.items()},'ships_upkeep':ex.get('ships'),'component_upkeep':ex.get('ship_components'),'new_messages_raw':news,'boundaries':['next_paid_boundary_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One documented paid boundary only, not full Terravore acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'date':aa['date'],'new_paid_hulls':len(new),'orders_left':len(remaining),'project3':ap['progress'],'hive_work':q.scalars(a['items'][str(newhives[0])])['progress']}),flush=True); assert passed
