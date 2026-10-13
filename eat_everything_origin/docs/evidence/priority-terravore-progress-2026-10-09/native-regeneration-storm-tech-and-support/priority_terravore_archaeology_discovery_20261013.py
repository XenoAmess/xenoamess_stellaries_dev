"""Exact existing site visibility discovery supplement; no calendar or UI."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-recovery-22860301';after='terravore-border-22860330'
b,a=read_state(run,before),read_state(run,after)
p=load(after+'-postcombat-v3-proof.json');ex=load(after+'-postcombat-v3-guard-execution.json')
failure='no_pending_unknown_news_wars_truces_or_combat'
checks={k:v for k,v in p['checks'].items() if k!=failure}
checks['original24_only_news_FAIL_actual1_source_originalSAV']=len(p['checks'])==24 and [k for k,v in p['checks'].items() if v is not True]==[failure] and ex['returncode']==1 and ex['helper_sha256']==h.sha256(Path(ex['command'][1]))=='8b06efe213320aef3654efa170863508b53882949c764d179548dc6ce4bf6dd4' and p['before_sha256']==b['audit']['save_sha256']==h.sha256(run/(before+'.sav')) and p['after_sha256']==a['audit']['save_sha256']==h.sha256(run/(after+'.sav'))
news=p['new_messages_raw']
checks['unique_exact_native_site5_discovery_notice']=len(news)==1 and q.scalars(news[0])=={'type':'MESSAGE_ARCHAEOLOGY_SITE_DISCOVERED','localization':'MESSAGE_ARCHAEOLOGY_SITE_DISCOVERED_DESC','receiver':0,'target_site':5,'end':'2286.06.23','date':'2286.03.23','notification':314,'message_type':'archaeology'}
bs=q.block(b['roots']['archaeological_sites'],'sites');ass=q.block(a['roots']['archaeological_sites'],'sites');old=q.block(bs,'5');new=q.block(ass,'5')
checks['preexisting_site5_only_visibility0_added_no_excavation_or_reward']=q.scalars(old)==q.scalars(new)=={'last_excavator_country':4294967295,'excavator_fleet':4294967295,'type':'site_abandoned_bio_lab','index':0,'clues':0,'last_roll':0,'days_left':90,'difficulty':1} and q.scalars(q.block(old,'location'))==q.scalars(q.block(new,'location'))=={'type':2,'id':1917} and q.ids(q.block(old,'visible_to'))==[1] and q.ids(q.block(new,'visible_to'))==[0,1] and omit(old,{'visible_to'})==omit(new,{'visible_to'}) and omit(bs,{'5'})==omit(ass,{'5'})
planet=q.block(q.block(a['roots']['planets'],'planet'),'1917')
checks['original_autoexplorer1_order64_legitimate_system57_discovery']=q.scalars(b['fleets']['1'])['order_id']==q.scalars(a['fleets']['1'])['order_id']==64 and q.scalars(q.block(q.block(a['fleets']['1'],'movement_manager'),'coordinate'))['origin']==q.scalars(q.block(planet,'coordinate'))['origin']==57
checks['no_pending_other_war_combat_or_new_unfiltered_error']=not a['pending'] and all(b['roots'][k]==a['roots'][k] for k in ['war','truce']) and all(not q.block(q.block(v,'combat'),'in_combat_with') for v in a['fleets'].values()) and (user/'logs/error.log').read_bytes()==(run/(after+'-error-after.log')).read_bytes()
passed=all(v is True for v in checks.values());out=run/(after+'-archaeology-discovery-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_EXISTING_ARCHAEOLOGY_DISCOVERY' if passed else 'FAIL','checks':checks,'before_sha256':p['before_sha256'],'after_sha256':p['after_sha256'],'date':a['audit']['date'],'native_site_before':old,'native_site_after':new,'native_message_raw':news,'boundaries':['native_border_expiry_next_day_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Existing site discovery only; no excavation, rewards or full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
