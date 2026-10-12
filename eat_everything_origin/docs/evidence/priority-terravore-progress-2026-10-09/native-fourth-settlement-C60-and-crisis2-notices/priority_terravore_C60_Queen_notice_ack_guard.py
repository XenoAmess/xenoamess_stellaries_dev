"""Strict same-day C60 growth/fleet Queen narration ACK with zero effects."""
import json,logging,sys,zipfile
from pathlib import Path
before,after,eid,event,pre_name,pre_stage,click_stage=sys.argv[1:];eid=int(eid)
assert event in {'eep.13','eep.31'}
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def read(st):
    au=load(st+'.audit.json')
    with zipfile.ZipFile(run/(st+'.sav')) as z:raw=z.read('gamestate').decode('utf-8-sig')
    return au,raw,list(q.fields(raw))
b,bt,bfs=read(before);a,at,afs=read(after);pre,pe=load(pre_name),load(pre_stage+'-execution.json')
vals=lambda fs,key:[v for k,v,o in fs if k==key]
bp,ap=[vals(fs,'player_event') for fs in [bfs,afs]];bm,am=[vals(fs,'message') for fs in [bfs,afs]]
target=[v for v in bp if q.scalars(v).get('id')==eid and q.scalars(v).get('event')==event and q.scalars(v).get('country')==0]
removed=[v for v in bm if q.scalars(v).get('event')==eid and q.scalars(v).get('receiver')==0]
source=h.MOD_ROOT/'events/eep_events.txt';definition=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')==event];option=q.block(definition[0],'option') if len(definition)==1 else ''
checks={
 'latest_nonempty_PASS_actual0_fixed_allowed_source_and_current_SAV':pre['status'].startswith('PASS_') and pre['checks'] and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and pe['returncode']==0 and pe['helper_sha256']==h.sha256(Path(pe['command'][1])) and pe['helper_sha256'] in {'33a77916ea6b1e071f7acc0211c9a7aa679dfdacf91c8d7bad74bbdbe8168f31',h.sha256(Path(__file__))},
 'same_native_date_original_two_SAVs':b['date']==a['date']=='2278.11.01' and all(au['save_sha256']==h.sha256(run/(st+'.sav')) for au,st in [(b,before),(a,after)]),
 'only_target_pending_removed_all_others_raw_held':len(target)==1 and ap==[v for v in bp if v not in target],
 'only_matching_message_removed':len(removed)==1 and q.scalars(removed[0]).get('type')=='EVENT_MESSAGE_TYPE' and am==[v for v in bm if v not in removed],
 'exact_single_human1_option0_selected_history':selected_history(at)==selected_history(bt)+[{'player_event':eid,'human':1,'option':0}],
 'every_other_world_top_raw_held':[(k,v,o) for k,v,o in bfs if k not in {'player_event','message','open_player_event_selection_history'}]==[(k,v,o) for k,v,o in afs if k not in {'player_event','message','open_player_event_selection_history'}],
 'native_Queen_single_option_source_zero_effects':len(definition)==1 and q.scalars(option)=={'name':event+'.a'} and len(list(q.fields(option)))==1 and len([v for k,v,o in q.fields(definition[0]) if k=='option'])==1,
 'normal_click_source_and_unique_save_actual0':load(click_stage+'-execution.json')['returncode']==0 and load(click_stage+'-execution.json')['helper_sha256']==h.sha256(Path(load(click_stage+'-execution.json')['command'][1]))=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and load(after+'-native-save-execution.json')['returncode']==0 and load(after+'-native-save-execution.json')['helper_sha256']==h.sha256(Path(load(after+'-native-save-execution.json')['command'][1]))=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e',
 'unfiltered_error_original41_020_simp_chinese':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb' and meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed=all(v is True for v in checks.values());out=run/(after+'-Queen-notice-ack-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_QUEEN_NOTICE_ACK_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'paid_births':pre['paid_births'],'event':event,'event_id':eid,'remaining_country0_pending':[q.scalars(v) for v in ap if q.scalars(v).get('country')==0],'native_source_sha256':h.sha256(source),'boundaries':['remaining_Queen_notice'] if ap else ['next_native_acceptance_plan_required'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Exactly one narrative option0 ACK; every other world field unchanged. Actual ship production and full route remain unaccepted.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'event':event,'remaining':[q.scalars(v).get('event') for v in ap]}),flush=True);assert passed
