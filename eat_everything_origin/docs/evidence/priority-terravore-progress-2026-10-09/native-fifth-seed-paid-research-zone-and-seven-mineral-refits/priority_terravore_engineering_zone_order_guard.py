"""Read-only exact native paid800 empty foundry zone replacement order."""
import json,logging,re,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-balthasar-native-devour-started';after='terravore-engineering-zone-paid-order'
ba,aa=[load(st+'.audit.json') for st in [before,after]];bc,ac=[v['countries']['0'] for v in [ba,aa]]
states=[]
for st in [before,after]:
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 rr={k:v for k,v,x in fs if x};country=q.block(rr['country'],'0')
 fleets=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(country,'fleets_manager'),'owned_fleets'))))
 fraw={k:v for k,v,x in q.fields(rr['fleet']) if x and int(k) in fleets}
 ships={i for v in fraw.values() for i in q.ids(q.block(v,'ships'))}
 sraw={k:v for k,v,x in q.fields(rr['ships']) if x and int(k) in ships}
 states.append({'roots':rr,'fleets':fraw,'ships':sraw,'army':rr['army'],'messages':[v for k,v,x in fs if x and k=='message' and q.scalars(v).get('receiver')==0],'pending':[v for k,v,x in fs if x and k=='player_event' and q.scalars(v).get('country')==0]})
b,a=states;br,ar=[v['roots'] for v in states]
queues=lambda rr:{k:v for k,v,x in q.fields(q.block(q.block(rr['construction'],'queue_mgr'),'queues')) if x}
items=lambda rr:{k:v for k,v,x in q.fields(q.block(q.block(rr['construction'],'item_mgr'),'items')) if x}
bq,aq=queues(br),queues(ar);bi,ai=items(br),items(ar);item=ai['1627389955'];isv=q.scalars(item);build=q.scalars(q.block(item,'buildable_zone'))
pre=load(before+'-fifth-devour-start-proof.json');px=load('terravore-balthasar-fifth-devour-start-guard-execution.json');obs=load(after+'-observation.json');sx=load('terravore-engineering-zone-paid-order-save-execution.json');ux=load('terravore-engineering-zone-normal-order-execution.json')
checks={
 'prior15_PASS_actual0_exact_seed_start_SAV_source':len(pre['checks'])==15 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(run/'priority_terravore_fifth_devour_start_guard.py')=='afd6baac963ee3f1901e99fa2997a527600f4fb405dae32a8ef356c20e2ce286' and pre['after_sha256']==ba['save_sha256']=='03d0aefc831de09f6547fc5f7c1c618bdd13ff860e291390ec856e6e5ee605ee',
 'normal_UI_and_save_actual0_original_sources_dependencies':ux['returncode']==sx['returncode']==0 and ux['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and sx['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and all(h.sha256(Path(v['path']))==v['sha256'] for v in obs['dependency_bindings']),
 'same_paused_date_original_SAV_SHA':ba['date']==aa['date']==obs['date']=='2280.11.03' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,ba),(after,aa)]) and aa['save_sha256']==obs['save_sha256']=='249748727d83ae2f7cf590f10d0396a40a2f398459d3720a838b44db345aff20',
 'exact800_minerals_paid_all_other_resources_held':all(D(str(ac['effective_stockpile'].get(k,0)))-D(str(bc['effective_stockpile'].get(k,0)))==(-D(800) if k=='minerals' else D(0)) for k in set(bc['effective_stockpile'])|set(ac['effective_stockpile'])) and q.scalars(q.block(item,'resources'))=={'minerals':800},
 'true_research_banks_and_full_queues_all_non_resource_country_fields_held':all(bc[k]==ac[k] for k in bc if k not in ['stockpile','effective_stockpile','modules']),
 'all_audited_population_jobs_planets_colonies_districts_situations_held':all(ba[k]==aa[k] for k in ba if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes','countries']),
 'only_one_new_order_paid800_360work_empty_slot2':set(ai)-set(bi)=={'1627389955'} and all(ai.get(k)==v for k,v in bi.items()) and isv=={'queue':0,'paying_country':0,'progress':0,'progress_needed':360} and build=={'zone':'zone_research_engineering','planet':0,'district':1,'zone_slot':2},
 'only_mother_planet_queue0_changed_normal_single_construction':set(bq)==set(aq) and all(v==aq[k] for k,v in bq.items() if k!='0') and not q.ids(q.block(bq['0'],'items')) and q.ids(q.block(aq['0'],'items'))==[1627389955] and q.scalars(aq['0'])=={'owner':0,'simultaneous':1,'type':'planet'} and q.scalars(q.block(aq['0'],'location'))=={'type':2,'id':7},
 'old_foundry104_and_all_buildings_zones_held_no_early_output':br['zones']==ar['zones'] and br['buildings']==ar['buildings'] and q.scalars(q.block(ar['zones'],'104'))=={'type':'zone_foundry'},
 'all_owned_fleets_ships_and_armies_raw_held':all(b[k]==a[k] for k in ['fleets','ships','army']),
 'messages_held_and_pending_empty':b['messages']==a['messages'] and not b['pending'] and not a['pending'],
 'production41_CN_unfiltered_error_exact_held':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and obs['new_error_bytes']==0 and obs['error_prefix_held'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(after+'-paid-zone-order-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NORMAL_PAID800_ENGINEERING_ZONE_ORDER' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'original_order_raw':item,'old_zone104_raw':q.block(ar['zones'],'104'),'original_queue_raw':aq['0'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Paid order only. No completed research zone or labs, no swallowed source, no Queen or full route acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
