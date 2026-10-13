"""Bounded native crystal battle review and ledger guard; no GUI writes."""
import json, logging, re, sys
from decimal import Decimal as D
from pathlib import Path
mode,before,other,prior,execution=sys.argv[1:]
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def checked(stage):
 x=load(stage+'-execution.json');return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
def day(value):
 y,m,d=map(int,value.split('.'));return y*360+(m-1)*30+d-1
def rq(c,k):
 raw=c['research_queues'][k];ts=list(q.tokens(raw));v=q.scalars(raw[ts[0][2]:ts[-1][1]]);v.setdefault('progress',0);return v
def flags(s):
 return {k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
def objectives(s):
 return {q.scalars(v)['objective']:D(str(q.scalars(v).get('progress',0))) for k,v,obj in q.fields(q.block(s['country'],'crisis_progression')) if obj and k=='objective'}
def alive(raw):
 v=q.scalars(raw);return v.get('killed')!='yes' and v.get('hitpoints',0)>0
b=read_state(run,before);ba=b['audit'];bc=ba['countries']['0'];p=load(prior);eps=D('.00003')
basic=p['status'].startswith('PASS') and bool(p['checks']) and all(v is True for v in p['checks'].values()) and checked(execution) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav'))
bp,be=rq(bc,'society_queue'),rq(bc,'engineering_queue');ids=q.ids(q.block(b['queues']['0'],'items'));head=D(str(q.scalars(b['items']['251658284'])['progress']))
if mode=='review':
 days=day(other)-day(ba['date']);combat=q.block(b['fleets']['83886903'],'combat')
 checks={
  'prior_PASS_actual0_source_originalSAV':basic,
  'one_to7_days_same_February_before_month_budget_border_and_completion':1<=days<=7 and ba['date'][:8]==other[:8]=='2286.02.' and day(other)<=day('2286.02.30') and head+D(days)*D('1.4')<480 and bp['progress']+161<12000 and be['progress']+104<550,
  'only_original_main18_against_known_crystal164':list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(combat,'in_combat_with'))))==[16777660] and q.scalars(q.block(combat,'coordinate'))['origin']==164 and 12<=len(q.ids(q.block(b['fleets']['83886903'],'ships')))<=18 and all(alive(b['ships'][str(i)]) for i in q.ids(q.block(b['fleets']['83886903'],'ships'))),
  'no_pending_and_live_CN41_error_held':not b['pending'] and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
 }
 passed=all(v is True for v in checks.values());out=run/(before+'-crystal-window-v4-review.json');assert not out.exists()
 h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':ba['save_sha256'],'start_date':ba['date'],'end_date':other,'days':days,'maximum_days':days,'allowed_boundaries':p['boundaries'],'execution_stage':before+'-crystal-window-v4-review'})
 print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed;sys.exit(0)
assert mode=='guard';after=other;a=read_state(run,after);aa=a['audit'];ac=aa['countries']['0'];ap,ae=rq(ac,'society_queue'),rq(ac,'engineering_queue')
cal=load(after+'-calendar-receipt.json');days=cal['days'];ob=load(after+'-construction-boundary-observation-v4.json');rev=load(before+('-crystal-window-v2-review.json' if before=='terravore-travel164-22860201' else '-crystal-window-v4-review.json'))
ticks=int(int(ba['date'].split('.')[2])<2<=int(aa['date'].split('.')[2]))
income=lambda c:{k:sum((D(str(v.get(k,0))) for v in c['budget_categories']['current_month']['income'].values()),D(0)) for k in q.RESEARCH_RESOURCES}
bi=income(bc);draw=min(bi['society_research'],D(str(bc['research_stockpile']['society_research'])))
mainids=set(q.ids(q.block(b['fleets']['83886903'],'ships')));life=True
for i,v in b['ships'].items():
 if i not in a['ships']:continue
 av=a['ships'].get(i,'');bs,ass=q.scalars(v),q.scalars(av)
 life=life and q.block(v,'ship_design_implementation')==q.block(av,'ship_design_implementation') and q.block(v,'name')==q.block(av,'name') and bs.get('construction_date')==ass.get('construction_date')
 if int(i) not in mainids:life=life and all(bs.get(k)==ass.get(k) for k in ['hitpoints','max_hitpoints','armor_hitpoints','shield_hitpoints'])
 else:life=life and alive(av) and all(0<=ass.get(k,0)<=ass.get(m,0) for k,m in [('hitpoints','max_hitpoints'),('armor_hitpoints','max_armor_hitpoints'),('shield_hitpoints','max_shield_hitpoints')])
bf=q.block(b['roots']['fleet'],'16777660');af=q.block(a['roots']['fleet'],'16777660');enb=set(q.ids(q.block(bf,'ships')));ena=set(q.ids(q.block(af,'ships')))
dead=enb-ena
for i in ena:
 if not alive(q.block(a['roots']['ships'],str(i))):dead.add(i)
bo,ao=objectives(b),objectives(a);reward=ao.get('crisobj_destroy_enemy_ships',D(0))-bo.get('crisobj_destroy_enemy_ships',D(0))
ef={k:dict(v,flag_days=v['flag_days']-days) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items() if not isinstance(v,dict) or 'flag_days' not in v or v['flag_days']>days}
news=ob['new_country0_messages_raw'];combat=q.block(a['fleets']['83886903'],'combat');active=list(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(combat,'in_combat_with'))))
checks={
 'prior_review_calendar_observer_actual0_originalSAV':basic and all(all(v is True for v in pp['checks'].values()) for pp in [rev,ob]) and all(checked(st) for st in [rev['execution_stage'],after+'-calendar',after+'-boundary-observation-v4']) and ob['before_sha256']==ba['save_sha256'] and ob['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'single1_to7_native_days_same_month':1<=days<=7 and day(aa['date'])-day(ba['date'])==days and ba['date'][:8]==aa['date'][:8]=='2286.02.',
 'cash8_no_month_budget_or_payments':all(bc['effective_stockpile'].get(k,0)==ac['effective_stockpile'].get(k,0) for k in ['energy','minerals','food','alloys','unity','rare_crystals','influence','trade']),
 'one_known_day2_tick_or_no_tick_true_research_banks':bi==income(ac) and abs(D(str(ap['progress']))-D(str(bp['progress']))-D(ticks)*(bi['society_research']*D('1.35')+draw))<eps and abs(D(str(ac['research_stockpile']['society_research']))-D(str(bc['research_stockpile']['society_research']))+D(ticks)*draw)<eps and abs(D(str(ae['progress']))-D(str(be['progress']))-D(ticks)*bi['engineering_research']*D('1.35'))<eps and abs(D(str(ac['research_stockpile']['physics_research']))-D(str(bc['research_stockpile']['physics_research']))-D(ticks)*bi['physics_research']*D('1.35'))<eps and bc['research_stockpile']['engineering_research']==ac['research_stockpile']['engineering_research']==0,
 'all_other_technology_projects_held':dict(bp,progress=ap['progress'])==ap and dict(be,progress=ae['progress'])==ae and omit(q.block(b['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'})==omit(q.block(a['country'],'tech_status'),{'stored_techpoints','society_queue','engineering_queue'}) and q.block(b['country'],'events')==q.block(a['country'],'events'),
 'all77_original_ship_identity_no_new_no_unexplained_loss_legal_health':len(a['ships'])<=len(b['ships'])<=77 and set(a['ships'])<=set(b['ships']) and life,
 '35_fleets_original_members_no_new_order':set(a['fleets'])==set(b['fleets']) and all((set(q.ids(q.block(a['fleets'][i],'ships')))<=set(q.ids(q.block(v,'ships'))) if i=='83886903' else q.ids(q.block(v,'ships'))==q.ids(q.block(a['fleets'][i],'ships'))) and q.scalars(v).get('order_id')==q.scalars(a['fleets'][i]).get('order_id') for i,v in b['fleets'].items()),
 'only_original_enemy_crystal_ships_no_reinforcement':ena<=enb and all(q.block(q.block(b['roots']['ships'],str(i)),'ship_design_implementation')==q.block(q.block(a['roots']['ships'],str(i)),'ship_design_implementation') for i in ena),
 'native_kills15_each_exact_objective_and_menace_no_other_reward':reward==D(15)*len(dead) and D(str(ac['effective_stockpile']['menace']))-D(str(bc['effective_stockpile']['menace']))==reward and {k:v for k,v in bo.items() if k!='crisobj_destroy_enemy_ships'}=={k:v for k,v in ao.items() if k!='crisobj_destroy_enemy_ships'} and omit(q.block(b['country'],'crisis_progression'),{'objective'})==omit(q.block(a['country'],'crisis_progression'),{'objective'}),
 'EEP_government_AP_traditions_population_held':all(bc[k]==ac[k] for k in ['variables','government','ascension_perks','traditions','owned_colonies']) and ba['colonies']['0']['actual_pop_sum']==aa['colonies']['0']['actual_pop_sum'] and ba['species']==aa['species'] and ba['planets']['7']==aa['planets']['7'],
 'mother_districts_zones_buildings_research_jobs_held':all(b['roots'][k]==a['roots'][k] for k in ['districts','zones','buildings']) and all(ba['pop_jobs'][i]==aa['pop_jobs'][i] for i in ['23','24','25']),
 'five_paid_hives_only_head_native_daily_work':q.ids(q.block(a['queues']['0'],'items'))==ids and omit(b['items']['251658284'],{'progress'})==omit(a['items']['251658284'],{'progress'}) and abs(D(str(q.scalars(a['items']['251658284'])['progress']))-head-D(days)*D('1.4'))<eps and all(a['items'][str(i)]==b['items'][str(i)] for i in ids[1:]),
 'all15_armies_held':q.ids(q.block(b['country'],'owned_armies'))==q.ids(q.block(a['country'],'owned_armies')) and all(q.block(b['roots']['army'],str(i))==q.block(a['roots']['army'],str(i)) for i in q.ids(q.block(b['country'],'owned_armies'))),
 'flags_only_native_daily_timers':flags(a)==ef,
 'no_other_combat_no_pending_newmessage_war_or_truce':active in [[],[16777660]] and all(not q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for i,v in a['fleets'].items() if i!='83886903') and not a['pending'] and not news and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']),
 'only_main_crystal_combat164_or_normal_order164':q.scalars(q.block(q.block(a['fleets']['83886903'],'movement_manager'),'coordinate'))['origin']==164,
 'other_player_queues_held':all(a['queues'].get(i)==v for i,v in b['queues'].items() if i!='0' and q.scalars(v).get('owner')==0),
 'CN41_unfiltered_live_error_held':meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
checks['enemy_original_country25_owner_chain_held_until_destroyed']=re.search(r'\bfleet\s*=\s*16777660\b',q.block(q.block(q.block(b['roots']['country'],'25'),'fleets_manager'),'owned_fleets')) is not None and (not ena or re.search(r'\bfleet\s*=\s*16777660\b',q.block(q.block(q.block(a['roots']['country'],'25'),'fleets_manager'),'owned_fleets')) is not None)
lost=set(b['ships'])-set(a['ships']);tombstones={k:v for k,v,obj in q.fields(a['roots']['ships']) if not obj and k in lost}
def combat_counts(state):
 cs=q.block(q.block(state['fleets']['83886903'],'fleet_stats'),'combat_stats')
 own=q.block(cs,'fleet');raw=q.block(cs,'enemy');ts=list(q.tokens(raw))
 enemy=raw[ts[0][2]:ts[-1][1]] if ts else ''
 esc=q.scalars(enemy)
 assert not esc or esc.get('fleet')==16777660
 return sum(q.ids(q.block(own,'ship_size_count_lost'))),sum(q.ids(q.block(enemy,'ship_size_count_lost')))
bl,al=combat_counts(b),combat_counts(a)
checks['native_own_losses_exact_main_tombstones_stats_naval5_each']=lost<=set(map(str,mainids)) and tombstones=={i:'none' for i in lost} and al[0]-bl[0]==len(lost) and al[0]==18-len(q.ids(q.block(a['fleets']['83886903'],'ships'))) and all(q.scalars(a['country'])[k]==q.scalars(b['country'])[k]-5*len(lost) for k in ['fleet_size','used_naval_capacity'])
checks['enemy_native_loss_stats_exact_removed_count']=al[1]-bl[1]==len(dead)
if after=='terravore-crystal164-22860208':
 original=load(after+'-crystal-window-v2-proof.json');ox=load(after+'-crystal-window-v2-guard-execution.json')
 checks['original19_threeFAIL_actual1_source_pair_retained']=len(original['checks'])==19 and sum(v is not True for v in original['checks'].values())==3 and ox['returncode']==1 and ox['helper_sha256']=='e492981ea8d9a80c6b7b505b01b76c9bcce83635c7b0b5acf7320bba549d26ae' and original['before_sha256']==ba['save_sha256'] and original['after_sha256']==aa['save_sha256']
if after=='terravore-crystal164-22860208':
 vx=load(after+'-crystal-window-v3-guard-execution.json')
 checks['originalV3_anonymous_stats_error_actual1_source_retained']=vx['returncode']==1 and vx['helper_sha256']=='16888297139d116749d54d0729fa8e28f73e2449bbcc6072e235adb6484907a6'
passed=all(v is True for v in checks.values());out=run/(after+'-crystal-window-v4-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_CRYSTAL_WINDOW' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'own_native_lost':sorted(lost),'native_loss_stats_before':bl,'native_loss_stats_after':al,'enemy_removed_or_dead':sorted(dead),'enemy_remaining':sorted(ena),'menace_reward':str(reward),'main_combat_with':active,'new_messages_raw':news,'boundaries':['native_crystal_combat_7day_review' if active else 'native_crystal_victory_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'One bounded native crystal battle window; any unknown loss, event or reward stops continuation.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'enemy_dead':sorted(dead),'active':active,'menace_reward':str(reward)}),flush=True);assert passed
