"""Read-only review of one exact zero-health defense army; cause remains inferred."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-project3-partial-month-22830101';after='terravore-project3-normal-month-22830201'
b,a=[read_state(run,s) for s in [before,after]];ba,aa=b['audit'],a['audit']
pre=load(before+'-remaining-labs-month-v7-proof.json');px=load(before+'-remaining-labs-guard-v7-execution.json')
old=load(after+'-remaining-labs-month-v7-proof.json');ox=load(after+'-remaining-labs-guard-v7-execution.json');dx=load('terravore-project3-first-six-normal-months-execution.json')
obs=load(after+'-construction-boundary-observation-v4.json');cx=load(after+'-calendar-execution.json');ex=load(after+'-boundary-observation-v4-execution.json')
ids=lambda s:set(q.ids(q.block(s['country'],'owned_armies')))
arm=lambda s,i:q.block(s['roots']['army'],str(i));target=50331803
changed={i for i in ids(b)|ids(a) if arm(b,i)!=arm(a,i)}
def live_source(s):
 return {i for i in ids(s) if q.scalars(arm(s,i)).get('colony')==30 and q.scalars(arm(s,i)).get('type')=='defense_army' and q.scalars(arm(s,i)).get('health',0)>0}
sources=load('terravore-three-labs-normal-month-22811201-annual-pop-bite-review-proof.json')['sources']
capital=(run/'terravore-annual-pop-native-00_capital_buildings.txt').read_text('utf-8-sig');jobs=(run/'terravore-annual-pop-native-04_gestalt_jobs.txt').read_text('utf-8-sig')
checks={
 'prior19_PASS_actual0_original_V7_single_army_FAIL_driver_stopped':len(pre['checks'])==19 and all(pre['checks'].values()) and px['returncode']==0 and len(old['checks'])==19 and [k for k,v in old['checks'].items() if not v]==['all_twenty_original_armies_raw_held_no_new_defense_or_assault'] and ox['returncode']==dx['returncode']==1 and not(run/'terravore-project3-normal-month-22830301.sav').exists() and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in [px,ox,dx]),
 'original_SHA_pair_calendar0_observer7_PASS_actual0':ba['date']=='2283.01.01' and aa['date']=='2283.02.01' and ba['save_sha256']==h.sha256(run/(before+'.sav'))==pre['after_sha256']==old['before_sha256']==obs['before_sha256'] and aa['save_sha256']==h.sha256(run/(after+'.sav'))==old['after_sha256']==obs['after_sha256'] and cx['returncode']==ex['returncode']==0 and len(obs['checks'])==7 and all(obs['checks'].values()),
 'only50331803_health475_to0_all_other_fields_and20_IDs_held':ids(b)==ids(a) and len(ids(a))==20 and changed=={target} and q.scalars(arm(b,target))['health']==475 and q.scalars(arm(a,target))['health']==0 and omit(arm(b,target),{'health'})==omit(arm(a,target),{'health'}) and all(q.scalars(arm(a,target))[k]==v for k,v in {'type':'defense_army','max_health':475,'owner':0,'species':73,'colony':30,'spawning_colony':30,'morale':250}.items()),
 'other19_including_three_paid_assault_raw_held_source5_to4_live':all(arm(b,i)==arm(a,i) for i in ids(b)-{target}) and {50331728,33554574,33554634}<=ids(a) and len(live_source(b))==5 and len(live_source(a))==4 and live_source(b)-live_source(a)=={target},
 'original_native_sources_and_capital4_patrol1_retained':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources) and q.scalars(capital)['@tier_2_capital_defense_armies']==4 and q.scalars(q.block(q.block(capital,'building_hive_capital'),'planet_modifier'))['planet_defense_armies_add']=='@tier_2_capital_defense_armies' and q.scalars(q.block(q.block(jobs,'patrol_drone'),'planet_modifier'))['planet_defense_armies_add']==1 and q.block(b['roots']['buildings'],'16777355')==q.block(a['roots']['buildings'],'16777355') and q.scalars(q.block(a['roots']['buildings'],'16777355'))['type']=='building_hive_capital' and ba['pop_jobs']['856']==aa['pop_jobs']['856'] and aa['pop_jobs']['856']['workforce']==100 and aa['pop_jobs']['856']['bonus_workforce']==-2.5,
 'no_ground_combat_messages_pending_or_new_error':q.scalars(b['roots']['ground_combat'])==q.scalars(a['roots']['ground_combat'])=={'150994944':'none'} and not obs['new_country0_messages_raw'] and not a['pending'] and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 'all_other18_original_business_checks_PASS':sum(v is True for v in old['checks'].values())==18 and not old['boundaries'] and not old['native_devour_calendar_ready'],
 'production41_CN_held_no_explicit_army_health_manipulation':m['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and not any(__import__('re').search(r'\b(?:create_army|remove_army|kill_army|set_health|change_health)\s*=',p.read_text('utf-8-sig')) for p in h.MOD_ROOT.rglob('*.txt')),
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-defense-retirement-review-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_EXACT_OBSERVED_DEFENSE_RETIREMENT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'army':target,'sources':sources,'inference':'Consistent with deferred native capacity cleanup (4 capital plus 0.975 patrol). Engine rounding and timing not confirmed. Exact pair only; not proof of a general rule or complete route.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
