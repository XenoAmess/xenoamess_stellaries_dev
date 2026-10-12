"""Actual native daily army modifier and research tick; targeted business checks."""
import json,logging,re,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-first-assault-army-native-birth-date';after='terravore-first-assault-army-daily-refreshed'
o=load(after+'-construction-boundary-observation-v2.json');b,a=o['before_state'],o['after_state'];ba,aa=b['audit'],a['audit'];bc,ac=[v['countries']['0'] for v in [ba,aa]]
pre=load(before+'-first-paid-army-birth-v3-proof.json');px=load(before+'-first-paid-army-birth-guard-v3-execution.json');ox=load(after+'-boundary-observation-v2-execution.json');cx=load(after+'-calendar-execution.json')
def roots(st):
 with zipfile.ZipFile(run/(st+'.sav')) as z:return {k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
br,ar=roots(before),roots(after)
omit=lambda raw,keys:[(k,v,x) for k,v,x in q.fields(raw) if k not in keys]
def items(st):return {i:v for i,v,x in q.fields(q.block(q.block(st['raw_roots']['construction'],'item_mgr'),'items')) if x and q.scalars(v).get('paying_country')==0}
bi,ai=items(b),items(a)
def progress(raw,name):
 values=re.findall(r'progress=([0-9.]+)',q.block(raw,name));assert len(values)==1;return D(values[0])
bt,at=bc['tech_status'],ac['tech_status'];bb,ab=bc['research_stockpile'],ac['research_stockpile']
ids=q.ids(q.block(b['country0_raw'],'owned_armies'));army_b=q.block(br['army'],'50331728');army_a=q.block(ar['army'],'50331728')
bp,ap=[{q.scalars(v)['id']:v for k,v,x in q.fields(q.block(st['country0_raw'],'events')) if k=='special_project' and x} for st in [b,a]]
checks={
 'prior_birth_PASS21_actual0_source_SAV':len(pre['checks'])==21 and all(pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and pre['after_sha256']==ba['save_sha256'],
 'native_one_day_six_observations_actual0_original_SAVs':all(o['checks'].values()) and ox['returncode']==cx['returncode']==0 and (ba['date'],aa['date'])==('2279.06.01','2279.06.02') and all(au['save_sha256']==h.sha256(run/(st+'.sav')) for st,au in [(before,ba),(after,aa)]),
 'paid_next_army_only_one_work_no_new_orders':bi.keys()==ai.keys() and all(omit(v,{'progress'})==omit(ai[i],{'progress'}) and q.scalars(ai[i])['progress']==q.scalars(v)['progress']+(1 if i=='1124073481' else 0) for i,v in bi.items()),
 'same13_armies_only_first_native_health200_to330':ids==q.ids(q.block(a['country0_raw'],'owned_armies')) and len(ids)==13 and all(q.block(br['army'],str(i))==q.block(ar['army'],str(i)) for i in ids if i!=50331728) and omit(army_b,{'health','max_health'})==omit(army_a,{'health','max_health'}) and all(q.scalars(army_b)[k]==200 and q.scalars(army_a)[k]==330 for k in ['health','max_health']),
 'original_ship_fleet_sets_all_designs_alive_transport_link':set(b['owned_ship_ids'])==set(a['owned_ship_ids']) and set(b['owned_fleets'])==set(a['owned_fleets']) and all(q.block(v,'ship_design_implementation')==q.block(a['owned_ships_raw'][i],'ship_design_implementation') and q.scalars(a['owned_ships_raw'][i]).get('hitpoints',0)>0 for i,v in b['owned_ships_raw'].items()) and q.scalars(army_a)['ship']==100664961 and q.scalars(a['owned_ships_raw']['100664961'])['army']==50331728,
 'physics_native_project_tick_and_bank':abs(progress(at,'physics_queue')-progress(bt,'physics_queue')-D('129.98954'))<=D('.00001') and D(str(ab['physics_research']))-D(str(bb['physics_research']))==D('-55.31470') and q.block(bt,'physics_queue').replace('649.9477','779.93724')==q.block(at,'physics_queue'),
 'society_bank_and_original_engineering_tick':D(str(ab['society_research']))-D(str(bb['society_research']))==D('26.58919') and ab['engineering_research']==bb['engineering_research']==0 and abs(progress(at,'engineering_queue')-progress(bt,'engineering_queue')-D('37.72669'))<=D('.00001') and omit(bt,{'physics_queue','engineering_queue','stored_techpoints'})==omit(at,{'physics_queue','engineering_queue','stored_techpoints'}),
 'special_projects_only_native_one_day_timers':bp.keys()==ap.keys() and all(omit(v,{'days_left'})==omit(ap[i],{'days_left'}) and (q.scalars(ap[i]).get('days_left')==q.scalars(v)['days_left']-1 if 'days_left' in q.scalars(v) else 'days_left' not in q.scalars(ap[i])) for i,v in bp.items()),
 'all_cash_and_nonresearch_stock_held':all(ac['effective_stockpile'].get(k,0)==bc['effective_stockpile'].get(k,0) for k in set(ac['effective_stockpile'])|set(bc['effective_stockpile']) if k not in ['physics_research','society_research','engineering_research']),
 'EEP_government_AP_crisis_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions','crisis']),
 'mother_capacity_district_levels_population_held_positive':aa['planets']['7']['variables']==ba['planets']['7']['variables'] and a['species_population_by_colony']==b['species_population_by_colony']=={'0:73':11972} and aa['colonies']['0']['districts']==ba['colonies']['0']['districts'] and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27 and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0,
 'no_new_messages_pending_combat':not o['new_country0_messages_raw'] and not a['pending_country0_raw'] and not any(re.search(r'\bfleet\s*=',q.block(q.block(v,'combat'),'in_combat_with')) for v in a['owned_fleets_raw'].values()),
 'production_CN_and_original_unfiltered_error_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
}
passed=all(v is True for v in checks.values());out=run/(after+'-daily-refresh-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_TERRAVORE_NATIVE_ARMY_DAILY_REFRESH' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'boundaries':[],'native_devour_calendar_ready':passed,'maximum_days_to_native_bite_boundary':29 if passed else 0,'scope':'Paid army native next-day modifier and research tick only; later campaign checks separate.'});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
