"""Exact same-day normal mother report and acknowledgment, no state grants."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,mode,prior_file,prior_exec=sys.argv[1:]
assert mode in ['first','repeat','ack']
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
def vals(fs,key):return [v for k,v,o in fs if k==key]
def omit(fs,keys):return [x for x in fs if x[0] not in keys]
b,bt,bf,br=read(before);a,at,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/prior_file).read_text('utf-8'));ex=json.loads((run/(prior_exec+'-execution.json')).read_text('utf-8'))
bp,ap=vals(bf,'player_event'),vals(af,'player_event');bm,am=vals(bf,'message'),vals(af,'message')
brc,arc=q.block(br['country'],'0'),q.block(ar['country'],'0');brp,arp=q.block(br['planets'],'planet'),q.block(ar['planets'],'planet');bcore,acore=q.block(brp,'7'),q.block(arp,'7')
source=Path('eat_everything_origin/mod/events/eep_events.txt');buttons=Path('eat_everything_origin/mod/common/button_effects/eep_buttons.txt');effects=Path('eat_everything_origin/mod/common/scripted_effects/eep_effects.txt');blocker=h.GAME_EXE.parent/'common/deposits/01_blocker_deposits.txt'
ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='eep.100'];assert len(ev)==1
checks={
 'prior_PASS_all_true_actual_exit0_exact_input':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date']=='2258.10.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_effect_only_country_event100_and_report_immediate':q.scalars(q.block(q.block(q.block(buttons.read_text('utf-8-sig'),'eep_audience_button_effect'),'effect'),'from')).get('country_event') is None and q.scalars(q.block(q.block(q.block(q.block(buttons.read_text('utf-8-sig'),'eep_audience_button_effect'),'effect'),'from'),'country_event'))=={'id':'eep.100'} and q.scalars(q.block(ev[0],'immediate'))=={'eep_report':'yes'} and not q.block(ev[0],'after'),
 'report_default_option_only_name':list(q.fields(vals(list(q.fields(ev[0])),'option')[0]))==[('name','eep.100.a',False)],
 'actual_EEP_ledger_and_flags_held':all(ac['variables'][k]==bc['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()) and ac['flags']==bc['flags'],
 'all_true_stocks_research_banks_and_tech_held':all(ac[k]==bc[k] for k in ['effective_stockpile','research_stockpile','tech_status']),
 'all_actual_pop_jobs_colonies_districts_species_global_targets_held':all(a[k]==b[k] for k in ['pop_groups','pop_jobs','colonies','districts','species','event_targets']),
 'all_other_countries_ordered_raw_held':omit(list(q.fields(br['country'])),{'0'})==omit(list(q.fields(ar['country'])),{'0'}),
 'all_country0_except_variables_ordered_raw_held':omit(list(q.fields(brc)),{'variables'})==omit(list(q.fields(arc)),{'variables'}),
 'all_other_planets_and_manager_fields_held':omit(list(q.fields(brp)),{'7'})==omit(list(q.fields(arp)),{'7'}) and omit(list(q.fields(br['planets'])),{'planet'})==omit(list(q.fields(ar['planets'])),{'planet'}),
 'all_mother_except_display_variables_raw_held':omit(list(q.fields(bcore)),{'variables'})==omit(list(q.fields(acore)),{'variables'}),
 'unfiltered_errors_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
 'normal_unique_native_save_exit0':json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0,
}
if mode in ['first','repeat']:
 bs,ass=q.scalars(bt),q.scalars(at);eid=bs['last_event_id']+1
 new=[v for v in ap if v not in bp];messages=[v for v in am if v not in bm]
 checks['unique_report203_or204_no_other_pending_added']=len(new)==1 and ap==bp+new and not bp and q.scalars(new[0])=={'id':eid,'event':'eep.100','date':'2261.01.02','country':0} and eid==(203 if mode=='first' else 204)
 scope=q.block(new[0],'scope') if len(new)==1 else '';frm=q.block(scope,'from');frm2=q.block(frm,'from')
 targets=[q.scalars(v) for k,v,o in q.fields(frm2) if k=='saved_event_target']
 checks['exact_country_planet_country_scope_local_targets']=all(q.scalars(v).get('type')==ty and q.scalars(v).get('id')==i for v,ty,i in [(scope,'country',0),(frm,'planet',7),(frm2,'country',0)]) and targets==[{'type':'country','id':0,'opener_id':4294967295,'name':'eep_actor'},{'type':'planet','id':7,'opener_id':4294967295,'name':'eep_report_core'}]
 checks['only_corresponding_message_added']=len(messages)==1 and am==bm+messages and q.scalars(messages[0]).get('event')==eid and q.scalars(messages[0]).get('receiver')==0 and q.scalars(messages[0]).get('date')=='2258.10.02'
 checks['allocation_exact_plus1_random_plus2_history_held']=ass['last_event_id']==eid and ass['random_count']==bs['random_count']+2 and selected_history(bt)==selected_history(at)
 expected=dict(bc['variables'],eep_psi=1)
 checks['only_psi_display0_to1_or_repeat_whole_country_held']=ac['variables']==expected and ((mode=='first' and bc['variables']['eep_psi']==0) or (mode=='repeat' and br['country']==ar['country']))
 expected_mother=dict(b['planets']['7']['variables'],eep_actual_pop=9969,eep_free_districts=5)
 checks['only_population_and_free_slot_display_or_repeat_raw_held']=a['planets']['7']['variables']==expected_mother and (mode=='first' or br['planets']==ar['planets'])
 levels={a['districts'][str(i)]['type']:a['districts'][str(i)]['level'] for i in a['colonies']['0']['districts']}
 ds={str(i):a['deposits'][str(i)]['type'] for i in a['planets']['7']['deposits']};blocked={'272':'d_failing_infrastructure','273':'d_failing_infrastructure','33554567':'d_ruined_district'}
 checks['free5_independent_real_capacity_levels_and_three_source_blockers']=levels=={'district_hive':5,'district_mining':10,'district_generator':6} and all(ds[k]==v for k,v in blocked.items()) and all(q.scalars(q.block(q.block(blocker.read_text('utf-8-sig'),v),'planet_modifier'))['planet_max_districts_add']==-1 for v in blocked.values()) and 18+ac['variables']['eep_d']-sum(levels.values())-len(blocked)==5
 checks['exact_report_snapshot']=all(ac['variables'][k]==v for k,v in {'eep_c_remainder':1,'eep_g_remainder':0,'eep_chunks':0,'eep_tasks':0,'eep_waiting':0,'eep_core_state':0,'eep_psi':1,'eep_crisis':0}.items()) and a['colonies']['0']['actual_pop_sum']==9969
 checks['normal_button_click_exit0_exact_point']=json.loads((run/(after.replace('-pending','-button')+'-execution.json')).read_text('utf-8'))['returncode']==0 and json.loads((run/(after.replace('-pending','-button')+'.action.json')).read_text('utf-8'))['client_point']==[812,221]
 checks['all_other_ordered_top_raw_held']=omit(bf,{'country','planets','player_event','message','last_event_id','random_count'})==omit(af,{'country','planets','player_event','message','last_event_id','random_count'})
else:
 target=[v for v in bp if q.scalars(v).get('event')=='eep.100' and q.scalars(v).get('country')==0];assert len(target)==1;eid=q.scalars(target[0])['id']
 removed=[v for v in bm if q.scalars(v).get('event')==eid and q.scalars(v).get('receiver')==0]
 checks['unique_pending_removed_no_new_pending']=len(bp)==1 and ap==[]
 checks['exact_corresponding_message_removed']=len(removed)==1 and am==[v for v in bm if v not in removed]
 checks['single_human1_option0_history']=selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':0}]
 checks['all_other_ordered_top_raw_held']=omit(bf,{'player_event','message','open_player_event_selection_history'})==omit(af,{'player_event','message','open_player_event_selection_history'})
 checks['normal_default_option_click_exit0']=json.loads((run/(after+'-select-execution.json')).read_text('utf-8'))['returncode']==0 and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['client_point']==[510,582]
p={'status':'PASS_TERRAVORE_PSI_REPORT_'+mode.upper()+'_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':not ap,'mode':mode,'sources':[{'path':str(s.resolve()),'sha256':h.sha256(s)} for s in [source,buttons,effects,blocker]],'actual_display':ac['variables'],'actual_mother_display':a['planets']['7']['variables'],'scope':'Normal report display and exact native event bookkeeping only; full civic route remains incomplete.'}
out=run/(after+'-report-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original report FAIL retained'
