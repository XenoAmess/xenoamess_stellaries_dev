"""Final native combat report supplements the active-combat boundary guard."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
before='terravore-crystal164-22860215';after='terravore-crystal164-22860222';initial='terravore-travel164-22860201'
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
b,a,i=read_state(run,before),read_state(run,after),read_state(run,initial)
ba,aa,ia=b['audit'],a['audit'],i['audit']
p=load(after+'-crystal-window-v4-proof.json');ex=load(after+'-crystal-window-v4-guard-execution.json')
failures=['no_other_combat_no_pending_newmessage_war_or_truce','native_own_losses_exact_main_tombstones_stats_naval5_each','enemy_native_loss_stats_exact_removed_count']
checks={k:v for k,v in p['checks'].items() if k not in failures}
checks['original21_only_three_boundaryFAIL_actual1_source_pair']=len(p['checks'])==21 and [k for k,v in p['checks'].items() if v is not True]==failures and ex['returncode']==1 and ex['helper_sha256']==h.sha256(Path(ex['command'][1]))=='2d1106694b9dfd1a5d27776d8a47dd18e1239633e9f633ab7fe901534ef725b9' and p['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and p['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav'))
news=load(after+'-construction-boundary-observation-v4.json')['new_country0_messages_raw']
assert len(news)==1
message=news[0];ms=q.scalars(message);cs=q.block(message,'combat_stats')
def single_array(raw):
 ts=list(q.tokens(raw));return raw[ts[0][2]:ts[-1][1]] if ts else ''
own=single_array(q.block(cs,'fleets'));enemy=single_array(q.block(cs,'enemy'))
checks['unique_native_report164_January26_to_February20_no_more_enemies']=ms=={'type':'COMBAT_STATS','receiver':0,'end':'2286.04.05','date':'2286.02.20','notification':312,'message_type':'combat_stats'} and q.scalars(q.block(message,'coordinate'))['origin']==164 and q.scalars(cs)=={'date':'2286.01.26','reason':'no_more_enemies'}
checks['report_own83886903_country0_original18_lost2']=q.scalars(own)['fleet']==83886903 and q.scalars(own)['country']==0 and q.ids(q.block(own,'ship_size_count'))==[18] and q.ids(q.block(own,'ship_size_count_lost'))==[2]
checks['report_enemy16777660_country25_original9_lost9']=q.scalars(enemy)['fleet']==16777660 and q.scalars(enemy)['country']==25 and q.ids(q.block(enemy,'ship_size_count'))==[9] and q.ids(q.block(enemy,'ship_size_count_lost'))==[9]
main=a['fleets']['83886903'];initial_ids=set(q.ids(q.block(i['fleets']['83886903'],'ships')));remaining=set(q.ids(q.block(main,'ships')))
rawships={k:(v,obj) for k,v,obj in q.fields(a['roots']['ships'])};rawfleets={k:(v,obj) for k,v,obj in q.fields(a['roots']['fleet'])}
checks['only_two_original_own_deaths_16_survivors_naval251']=initial_ids-remaining=={16779033,16779128} and len(remaining)==16 and all(rawships[str(k)]==('none',False) for k in [16779033,16779128]) and all(q.scalars(a['country'])[k]==251 for k in ['fleet_size','used_naval_capacity']) and b['ships'].keys()==a['ships'].keys()
enemyids=q.ids(q.block(q.block(i['roots']['fleet'],'16777660'),'ships'))
checks['all9_enemy_removed_exact7none2absent_fleet_none']=len(enemyids)==9 and rawfleets['16777660']==('none',False) and {str(k) for k in enemyids if str(k) not in rawships}=={'83887250','67110053'} and all(rawships[str(k)]==('none',False) for k in enemyids if str(k) in rawships)
initial_obj={q.scalars(v)['objective']:q.scalars(v)['progress'] for k,v,obj in q.fields(q.block(i['country'],'crisis_progression')) if obj and k=='objective'}
final_obj={q.scalars(v)['objective']:q.scalars(v)['progress'] for k,v,obj in q.fields(q.block(a['country'],'crisis_progression')) if obj and k=='objective'}
checks['whole_battle9_times15_menace_and_objective_last2_times15']=ia['save_sha256']==h.sha256(run/(initial+'.sav')) and aa['countries']['0']['effective_stockpile']['menace']-ia['countries']['0']['effective_stockpile']['menace']==135 and final_obj['crisobj_destroy_enemy_ships']-initial_obj['crisobj_destroy_enemy_ships']==135 and p['enemy_removed_or_dead']==[50332761,67110053] and p['menace_reward']=='30'
live=q.block(q.block(main,'fleet_stats'),'combat_stats')
checks['postcombat_live_stats_cleared_no_pending_war_or_active_opponent']=not list(q.fields(q.block(live,'fleet'))) and q.scalars(live)=={'date':'0.01.01'} and all(not q.block(q.block(v,'combat'),'in_combat_with') for v in a['fleets'].values()) and not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['war','truce'])
vx=load(after+'-crystal-victory-guard-execution.json')
checks['V1_missing_tombstone_KeyError_actual1_source_retained']=vx['returncode']==1 and vx['helper_sha256']=='f605bac30a950c3c1774555d72bf0850f7cfa8f08baddec9b202b306c5f28d91'
passed=all(v is True for v in checks.values());out=run/(after+'-crystal-victory-v2-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_CRYSTAL_VICTORY_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'initial_sha256':ia['save_sha256'],'date':aa['date'],'battle_end_date':ms['date'],'own_losses':[16779033,16779128],'enemy_losses':enemyids,'total_menace_reward':135,'native_report_raw':message,'boundaries':['native_postcombat_travel_or_colonization_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Native crystal battle victory with two ordinary corvette losses; not full civic acceptance or arrival at target orbit.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
