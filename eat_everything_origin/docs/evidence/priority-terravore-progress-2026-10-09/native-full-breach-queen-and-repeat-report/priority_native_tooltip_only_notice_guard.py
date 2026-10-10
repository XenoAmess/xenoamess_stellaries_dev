"""Read-only same-date tooltip-only native notice acknowledgement."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after,eid,event,pre_file,pre_stage=sys.argv[1:];eid=int(eid);assert event in ['shroud.2760']
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t
def vals(t,key):return [v for k,v,o in q.fields(t) if k==key]
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bt=read(before);a,at=read(after);pre=json.loads((run/pre_file).read_text('utf-8'));bp,ap=vals(bt,'player_event'),vals(at,'player_event');target=[v for v in bp if q.scalars(v).get('id')==eid and q.scalars(v).get('event')==event and q.scalars(v).get('country')==0]
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')==event];assert len(ev)==1;opts=vals(ev[0],'option');assert len(opts)==1;opt=opts[0]
bm,am=vals(bt,'message'),vals(at,'message');removed=[v for v in bm if q.scalars(v).get('event')==eid and q.scalars(v).get('receiver')==0]
checks={
 'prior_PASS_actual_exit0_SHA_bound':pre['status'].startswith('PASS') and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/(pre_stage+'-execution.json')).read_text('utf-8'))['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date'] and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'exact_native_situation_pending_removed':len(target)==1 and q.scalars(q.block(target[0],'scope')).get('type')=='situation' and q.scalars(q.block(target[0],'scope')).get('id')==16777221 and ap==[v for v in bp if v not in target],
 'exact_once_human_option0_history':selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':0}],
 'only_corresponding_message_removed':len(removed)<=1 and am==[v for v in bm if v not in removed],
 'all_other_ordered_top_level_raw_held':omit(bt,{'player_event','message','open_player_event_selection_history'})==omit(at,{'player_event','message','open_player_event_selection_history'}),
 'native_source_tooltip_only_no_immediate_after':not q.block(ev[0],'immediate') and not q.block(ev[0],'after') and [(k,o) for k,v,o in q.fields(opt)]==[('name',True),('if',True),('else',True)] and [(k,o) for k,v,o in q.fields(q.block(opt,'if'))]==[('limit',True),('custom_tooltip',False)] and q.scalars(q.block(opt,'if'))=={'custom_tooltip':'shroud.2760.a_tt_no_psi_corps'} and q.scalars(q.block(opt,'else'))=={'custom_tooltip':'shroud.2760.a_tt'},
 'unfiltered_error_zero_increment':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
 'normal_click_and_save_actual_exit0':all(json.loads((run/(after+s+'-execution.json')).read_text('utf-8'))['returncode']==0 for s in ['-select','-save']) and json.loads((run/(after+'-select.action.json')).read_text('utf-8'))['action']=='left-click',
}
for k in ['effective_stockpile','research_stockpile','tech_status','variables','flags','traditions','ascension_perks','government','owned_colonies','budget_categories']:checks[k+'_held']=b['countries']['0'][k]==a['countries']['0'][k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TOOLTIP_ONLY_NOTICE_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'event_id':eid,'event':event,'pending_after':[q.scalars(v) for v in ap if q.scalars(v).get('country')==0],'calendar_ready':not [v for v in ap if q.scalars(v).get('country')==0],'native_source':{'path':str(source),'sha256':h.sha256(source)},'scope':'One native situation tooltip-only option0 acknowledgement, all other ordered raw state held. No psionic completion or Mod reward claimed.'}
out=run/(after+'-tooltip-notice-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original tooltip-only notice FAIL retained; no replay'
