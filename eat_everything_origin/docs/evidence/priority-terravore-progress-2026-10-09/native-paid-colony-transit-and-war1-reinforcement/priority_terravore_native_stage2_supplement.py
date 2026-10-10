"""Exact native first stage2 entry; original stage1-only FAIL remains intact."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-before-stage2';after='terravore-native-stage2-pending'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt,br=read(before);a,at,ar=read(after);orig=json.loads((run/(after+'-meditate-year-proof.json')).read_text('utf-8'));ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
bs,ass=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]]
pending=[v for k,v,o in q.fields(at) if k=='player_event' and o and q.scalars(v).get('country')==0]
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';stagesource=h.GAME_EXE.parent/'common/situations/13_shroud_situations.txt';ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2760'];assert len(ev)==1
stage2=q.block(q.block(q.block(stagesource.read_text('utf-8-sig'),'situation_breach_shroud'),'stages'),'stage_2');hook=q.block(stage2,'on_first_enter')
bf,af=q.scalars(q.block(bs,'flags')),q.scalars(q.block(ass,'flags'));expected=dict(bf);expected.pop('breach_shroud_approach_selected',None);expected['breach_shroud_stage_2_started']=63250800
failed={'no_country0_pending','one_native_breach_stage1_progress_only','all_native_breach_raw_except_progress_held'}
checks={
 'original40_exact_three_stage_boundary_FAIL_exit1':orig['status']=='FAIL' and len(orig['checks'])==40 and {k for k,v in orig['checks'].items() if not v}==failed and ex['returncode']==1,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256']==orig['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==orig['after_sha256'],
 'unique_calendar_actual_exit0':json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0 and json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))['days']==30,
 'exact_30_days_cross500_with_meditation5':b['date']=='2251.03.02' and a['date']=='2251.04.02' and orig['days']==30 and b['situations']['16777221']['progress']==496.25 and a['situations']['16777221']['progress']==501.25 and a['situations']['16777221']['last_month_progress']==5,
 'only_stage0_to1_and_exact_native_stage2_flag':q.scalars(bs)['stage']==0 and q.scalars(ass)['stage']==1 and af==expected and omit(bs,{'progress','last_month_progress','stage','flags'})==omit(ass,{'progress','last_month_progress','stage','flags'}),
 'unique_actual_stage2_notice_for_actual_situation':not [v for k,v,o in q.fields(bt) if k=='player_event' and o and q.scalars(v).get('country')==0] and len(pending)==1 and q.scalars(pending[0]).get('event')=='shroud.2760' and q.scalars(q.block(pending[0],'scope')).get('type')=='situation' and q.scalars(q.block(pending[0],'scope')).get('id')==16777221,
 'native_stage2_source_exact_hook':q.scalars(hook)=={'set_situation_flag':'breach_shroud_stage_2_started','remove_situation_flag':'breach_shroud_approach_selected'} and q.scalars(q.block(hook,'situation_event'))=={'id':'shroud.2760'} and [(k,o) for k,v,o in q.fields(hook)]==[('set_situation_flag',False),('remove_situation_flag',False),('situation_event',True)],
 'native_notice_no_immediate_one_tooltip_option':not q.block(ev[0],'immediate') and len([v for k,v,o in q.fields(ev[0]) if k=='option'])==1 and [(k,o) for k,v,o in q.fields(q.block(ev[0],'option'))]==[('name',True),('if',True),('else',True)] and q.scalars(q.block(q.block(ev[0],'option'),'else'))=={'custom_tooltip':'shroud.2760.a_tt'},
 'all_other37_original_boundary_checks_true':all(v is True for k,v in orig['checks'].items() if k not in failed),
 'no_early_EEP_psionic_reward':a['countries']['0']['variables']['eep_psi']==0 and 'eep_psi_notice' not in a['countries']['0']['flags'],
 'actual_native_psi_building_remains':len([v for k,v,o in q.fields(ar['buildings']) if o and q.scalars(v).get('type')=='building_psi_corps'])==1,
}
p={'status':'PASS_NATIVE_TERRAVORE_STAGE2_PENDING_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'pending':[{'scalars':q.scalars(v),'raw':v} for v in pending],'native_breach_raw_before_after':[bs,ass],'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,stagesource]],'scope':'Only exact native phase2 entry and shroud2760 pending; remaining37 original checks mandatory. Original first-stage-only FAIL retained; no calendar clearance.'}
out=run/(after+'-stage2-pending-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original stage2 pending supplement FAIL retained'
