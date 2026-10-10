"""Read-only actual two paid shipyard work slots over one native day."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,list(q.fields(t)),{k:v for k,v,o in q.fields(t) if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def queue(rt,i):return q.block(q.block(q.block(rt['construction'],'queue_mgr'),'queues'),str(i))
def items(rt):return {k:v for k,v,o in q.fields(q.block(q.block(rt['construction'],'item_mgr'),'items')) if o}
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-first-contact118-ack-proof.json')).read_text('utf-8'));receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text('utf-8'))
bq,aq=queue(br,3),queue(ar,3);ids=q.ids(q.block(bq,'items'));bi,ai=items(br),items(ar)
shipids=[16777221,16778303,16778412,1564]
checks={
 'bound_original_ACK_PASS':pre['status']=='PASS_NATIVE_FIRST_CONTACT118_ACK_COMPONENT' and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and json.loads((run/'terravore-defense-contact118-ack-guard-execution.json').read_text('utf-8'))['returncode']==0,
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'actual_one_day_receipt':b['date']=='2236.11.19' and a['date']=='2236.11.20' and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==1 and receipt['start_date']==b['date'] and receipt['date']==a['date'] and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'same16_original_orders_queue_capacity2':len(ids)==16 and q.ids(q.block(aq,'items'))==ids and q.scalars(bq)['simultaneous']==q.scalars(aq)['simultaneous']==2 and bq==aq,
 'first_original_paid_order_45_to46_25':ids[0]==671088646 and q.scalars(bi[str(ids[0])])['progress']==45 and q.scalars(ai[str(ids[0])])['progress']==46.25 and omit(bi[str(ids[0])],['progress'])==omit(ai[str(ids[0])],['progress']),
 'second_original_paid_order_0_to1_25':ids[1]==335544337 and q.scalars(bi[str(ids[1])])['progress']==0 and q.scalars(ai[str(ids[1])])['progress']==1.25 and omit(bi[str(ids[1])],['progress'])==omit(ai[str(ids[1])],['progress']),
 'other14_orders_complete_raw_held':all(bi[str(i)]==ai[str(i)] for i in ids[2:]),
 'actual_starbase_complete_raw_held':q.block(q.block(br['starbase_mgr'],'starbases'),'0')==q.block(q.block(ar['starbase_mgr'],'starbases'),'0'),
 'same_four_actual_paid_corvettes':q.ids(q.block(q.block(br['fleet'],'16777797'),'ships'))==q.ids(q.block(q.block(ar['fleet'],'16777797'),'ships'))==shipids,
 'same_four_ship_design_dates_hull_fleet':all(q.scalars(q.block(br['ships'],str(i)))==q.scalars(q.block(ar['ships'],str(i))) and q.block(q.block(br['ships'],str(i)),'ship_design_implementation')==q.block(q.block(ar['ships'],str(i)),'ship_design_implementation') for i in shipids),
 'true_population8930_held':b['colonies']['0']['actual_pop_sum']==a['colonies']['0']['actual_pop_sum']==8930,
 'core_capacity11_modifiers_held':b['planets']['7']['variables']==a['planets']['7']['variables'] and a['planets']['7']['variables']['eep_capacity_value']==11 and b['planets']['7']['modifiers']==a['planets']['7']['modifiers'],
 'core_bombardment_still_native':a['planets']['7']['ground_support_stance']=='voidworm_invasion' and a['planets']['7']['last_bombardment']==a['date'] and a['planets']['7']['bombardment_damage']>=b['planets']['7']['bombardment_damage'],
 'no_country0_pending':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TWO_SHIPYARDS_ACTUALLY_WORKING_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_front_progress':[q.scalars(ai[str(i)])['progress'] for i in ids[:2]],'scope':'One native day, two original paid orders independently advance. Four actual ships, no monthly boundary or defense victory/full-route claim.'}
out=run/(after+'-parallel-shipyards-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original parallel work FAIL retained; no next calendar'
