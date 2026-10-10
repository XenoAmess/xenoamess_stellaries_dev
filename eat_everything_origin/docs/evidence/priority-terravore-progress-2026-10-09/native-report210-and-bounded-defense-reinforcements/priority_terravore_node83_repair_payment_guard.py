"""Read-only exact native node83 repair order and paid160 minerals."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]]
bmod,amod=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(c,'standard_economy_module') for c in [bmod,amod]];bres,ares=[q.block(c,'resources') for c in [be,ae]]
conb,cona=[rt['construction'] for rt in [br,ar]];bqm,aqm=[q.block(c,'queue_mgr') for c in [conb,cona]];bqs,aqs=[q.block(c,'queues') for c in [bqm,aqm]];bq,aq=[q.block(c,'0') for c in [bqs,aqs]]
bim,aim=[q.block(c,'item_mgr') for c in [conb,cona]];bi,ai=[q.block(c,'items') for c in [bim,aim]];item=q.block(ai,'620757018');sc=q.scalars(item)
pre=json.loads((run/(before+'-raid-ended-proof.json')).read_text('utf-8'));ex=json.loads((run/(before+'-guard-execution.json')).read_text('utf-8'))
checks={
 'exact_same_date_input_pair':before=='terravore-raid-defense-day15' and after=='terravore-raid-node83-repair-paid' and b['date']==a['date']=='2261.11.17',
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'prior37_raid_ended_PASS_actual_exit0':pre['status']=='PASS_TERRAVORE_SECOND_RAID_ENDED_COMPONENT' and len(pre['checks'])==37 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'exact160_actual_minerals_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==160,
 'all_other_actual_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'other_top_ordered_raw_held':[x for x in bf if x[0] not in {'country','construction'}]==[x for x in af if x[0] not in {'country','construction'}],
 'other_countries_ordered_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'country0_except_modules_raw_held':omit(bcr,{'modules'})==omit(acr,{'modules'}),
 'other_country_modules_raw_held':omit(bmod,{'standard_economy_module'})==omit(amod,{'standard_economy_module'}),
 'economy_except_resources_raw_held':omit(be,{'resources'})==omit(ae,{'resources'}),
 'only_economy_mineral_field_changed':omit(bres,{'minerals'})==omit(ares,{'minerals'}) and q.scalars(bres)['minerals']==10700.62188 and q.scalars(ares)['minerals']==10540.62188,
 'one_mother_order_only':q.ids(q.block(bq,'items'))==[] and q.ids(q.block(aq,'items'))==[620757018] and omit(bq,{'items'})==omit(aq,{'items'}),
 'all_other_queues_including16_paid_ships_raw_held':omit(bqs,{'0'})==omit(aqs,{'0'}),
 'only_original_none_handle_recycled':q.scalars(bi).get('603979802')=='none' and 620757018==603979802+16777216 and not any(k=='620757018' for k,v,o in q.fields(bi)) and not any(k=='603979802' for k,v,o in q.fields(ai)) and omit(bi,{'603979802'})==omit(ai,{'620757018'}),
 'other_construction_managers_raw_held':omit(conb,{'queue_mgr','item_mgr'})==omit(cona,{'queue_mgr','item_mgr'}) and omit(bqm,{'queues'})==omit(aqm,{'queues'}) and omit(bim,{'items'})==omit(aim,{'items'}),
 'native_order_exact_payer0_work180':sc=={'queue':0,'paying_country':0,'progress':0,'progress_needed':180},
 'native_order_exact_paid_resources160':q.scalars(q.block(item,'resources'))=={'minerals':160},
 'native_repair83_mother0_zone61_type':q.scalars(q.block(item,'buildable_planet_repair_building'))=={'type':'building_hive_node','building':83,'planet':0,'zone':61},
 'native_order_no_extra_fields':set(k for k,v,o in q.fields(item))=={'queue','paying_country','progress','progress_needed','resources','buildable_planet_repair_building'},
 'actual_node83_still_ruined_pending_real_completion':q.scalars(q.block(ar['buildings'],'83'))=={'type':'building_hive_node','ruined':'yes','position':0} and q.ids(q.block(q.block(ar['zones'],'61'),'buildings'))==[83,16777258,86],
 'tech_status_and_real_banks_raw_held':bc['tech_status']==ac['tech_status'] and bc['research_stockpile']==ac['research_stockpile'],
 'no_pending_and_errors_exact2670':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0] and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and len((run/(after+'-error-after.log')).read_bytes())==2670,
 'save_actual_exit0':json.loads((run/(after+'-save-execution.json')).read_text('utf-8'))['returncode']==0,
}
click=json.loads((run/'terravore-raid-node83-repair-click.action.json').read_text('utf-8'))
checks['unique_normal_repair_click_actual_exit0']=click['action']=='left-click' and click['client_point']==[878,168] and json.loads((run/'terravore-raid-node83-repair-click-execution.json').read_text('utf-8'))['returncode']==0
checks['UI_repair_quote_image_bound']=h.sha256(run/'terravore-raid-node83-repair-price-visible.jpg')==json.loads((run/'terravore-raid-node83-repair-price-visible.ocr.json').read_text('utf-8'))['image_sha256']
sources=[h.GAME_EXE.parent/p for p in ['common/defines/00_defines.txt','common/buildings/08_unity_buildings.txt','common/scripted_variables/00_scripted_variables.txt']]
defines=q.scalars(q.block(sources[0].read_text('utf-8-sig'),'NGameplay'));values=q.scalars(sources[2].read_text('utf-8-sig'));node=q.scalars(q.block(sources[1].read_text('utf-8-sig'),'building_hive_node'))
checks['native_repair_half_base400_and360']=defines.get('REPAIR_BUILDING_COST')==defines.get('REPAIR_BUILDING_TIME')==0.5 and node.get('base_buildtime')=='@b1_time' and values.get('@b1_time')==360 and values.get('@b1_minerals')==400
p={'status':'PASS_TERRAVORE_NATIVE_NODE83_REPAIR_PAYMENT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_item_raw':item,'actual_paid_minerals':160,'native_base_work':180,'UI_estimated_days':129,'native_sources':[{'path':str(p),'sha256':h.sha256(p)} for p in sources],'calendar_ready':all(checks.values()),'scope':'One normal paid repair order only;83 still ruined. No construction completion, restored jobs or recovered stable economy claim.'}
out=run/(after+'-node83-repair-payment-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps({'status':p['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'after_sha256':p['after_sha256']}),flush=True);assert all(checks.values()),'Original repair payment FAIL retained; do not replay payment'
