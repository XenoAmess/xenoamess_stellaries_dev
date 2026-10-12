"""Review one native first shroud tunnel discovery while retaining21 business checks."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-paid-destroyer-operating-22841101';after='terravore-paid-destroyer-operating-22841201';b,a=[read_state(run,s) for s in [before,after]];p=load(after+'-operating-month-proof.json');px=load(after+'-operating-month-guard-execution.json');ob=load(after+'-construction-boundary-observation-v4.json')
failed={'country_timers_exact_expiry_only_native_birth_flag_refresh','no_unknown_messages_pending_combat_wars_truces_or_orders'}
flags=lambda s:{k:q.scalars(v) if obj else q.unquote(v) for k,v,obj in q.fields(q.block(s['country'],'flags'))}
ef={k:dict(v,flag_days=v['flag_days']-30) if isinstance(v,dict) and 'flag_days' in v else v for k,v in flags(b).items()};ef.update(built_artificial_ship=63541032,encountered_first_shroud_tunnel=63541584)
src=h.GAME_EXE.parent/'events/overlord_enclaves_events.txt';dest=run/'native-tunnel303-overlord_enclaves_events.txt';assert not dest.exists();dest.write_bytes(src.read_bytes());sources=[{'path':str(src),'preserved':dest.name,'sha256':h.sha256(src)}]
ev=next(v for k,v,obj in q.fields(src.read_text('utf-8-sig')) if obj and q.scalars(v).get('id')=='enclave.100');opts=[v for k,v,obj in q.fields(ev) if obj and k=='option'];news=ob['new_country0_messages_raw']
checks={k:v for k,v in p['checks'].items() if k not in failed};checks.update({
 'original_unknown_boundary_FAIL_actual1_original_SAV_source':p['status']=='FAIL' and len(p['checks'])==23 and {k for k,v in p['checks'].items() if v is False}==failed and px['returncode']==1 and px['helper_sha256']==h.sha256(Path(px['command'][1]))=='2e5ca8ce78ec97a28f7e9ce0300da7946cdfb9d6005216f957d3b1ada97e2924' and p['before_sha256']==b['audit']['save_sha256']==h.sha256(run/(before+'.sav')) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact_only_pending303_ship1_system14_and_native_message':len(a['pending'])==1 and q.scalars(a['pending'][0])=={'id':303,'event':'enclave.100','date':'2287.02.27','country':0} and q.scalars(q.block(a['pending'][0],'scope'))['id']==1 and q.scalars(q.block(q.block(a['pending'][0],'scope'),'from'))['id']==14 and len(news)==1 and q.scalars(news[0])['event']==303 and q.scalars(news[0])['type']=='EVENT_MESSAGE_TYPE' and q.scalars(news[0])['date']=='2284.11.27',
 'all_flags_exact_only_new_tunnel_and_known_paid_birth_refresh':flags(a)==ef,
 'native_tunnel_source_empty_option_starflag_and_bypass_bound':len(opts)==1 and list(q.fields(opts[0]))==[('name','enclave.100.a',False)] and q.scalars(q.block(q.block(ev,'immediate'),'owner'))=={'set_country_flag':'encountered_first_shroud_tunnel','add_seen_bypass_type':'shroud_tunnel'} and bool({'shroud_tunnel_nexus','shroud_tunnel_node'}&set(q.scalars(q.block(q.block(a['roots']['galactic_object'],'14'),'flags')))) and '"shroud_tunnel"' in q.block(a['country'],'seen_bypass_types') and h.sha256(src)==h.sha256(dest),
 'other_original_boundary_terms_no_combat_war_truce_or_orders':all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and all(a['queues'].get(i)==v for i,v in b['queues'].items() if i not in ['0','3'] and q.scalars(v)['owner']==0) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
})
passed=all(v is True for v in checks.values());out=run/(after+'-native-tunnel303-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_REVIEWED_NATIVE_TUNNEL_DISCOVERY' if passed else 'FAIL','checks':checks,'before_sha256':p['before_sha256'],'after_sha256':p['after_sha256'],'date':a['audit']['date'],'sources':sources,'native_pending_raw':a['pending'],'native_messages_raw':news,'boundaries':['native_tunnel303_ack_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Only native discovery303 supplement;21 original business checks retained. No calendar until normal empty-effect acknowledgement verified.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
