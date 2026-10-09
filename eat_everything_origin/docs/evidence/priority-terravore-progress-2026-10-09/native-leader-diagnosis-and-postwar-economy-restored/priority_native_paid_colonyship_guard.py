"""Read-only native 375/150 colony ship purchase and sole expansion binding."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
from decimal import Decimal as D
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,fs,{k:v for k,v,o in fs if o}
def without(s,keys):return [(k,v,o) for k,v,o in q.fields(s) if k not in keys]
def single(v):
 ts=list(q.tokens(v));assert ts[0][0]=='{' and ts[-1][0]=='}';depth=0
 for i,(token,_,_) in enumerate(ts):
  depth+=(token=='{')-(token=='}');assert depth>0 or i==len(ts)-1
 assert depth==0
 return v[ts[0][2]:ts[-1][1]]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
b0,a0=q.block(br['country'],'0'),q.block(ar['country'],'0');bm,am=q.block(b0,'modules'),q.block(a0,'modules')
be,ae=q.block(bm,'standard_economy_module'),q.block(am,'standard_economy_module');bx,ax=q.block(bm,'standard_expansion_module'),q.block(am,'standard_expansion_module')
bs,ass=q.scalars(q.block(be,'resources')),q.scalars(q.block(ae,'resources'))
buildb,builda=br['construction'],ar['construction'];bqm,aqm=q.block(buildb,'queue_mgr'),q.block(builda,'queue_mgr');bqs,aqs=q.block(bqm,'queues'),q.block(aqm,'queues')
bim,aim=q.block(buildb,'item_mgr'),q.block(builda,'item_mgr');bi,ai=q.block(bim,'items'),q.block(aim,'items');item=q.block(ai,'553648131');col=q.block(item,'buildable_colony_ship')
exp=single(q.block(ax,'expansion_list'));design={'design':33554522,'upgrade':4294967295,'growth_stage':0}
checks={
 'same_native_date':b['date']==a['date']=='2225.03.02',
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'exact_real375_minerals150_alloys_paid':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==375 and D(str(bc['effective_stockpile']['alloys']))-D(str(ac['effective_stockpile']['alloys']))==150,
 'all_other_actual_stocks_and_true_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k not in ['minerals','alloys']}=={k:v for k,v in ac['effective_stockpile'].items() if k not in ['minerals','alloys']},
 'exact_removed_economy_research_mirrors':{k:bs[k] for k in q.RESEARCH_RESOURCES}=={'physics_research':249.864,'society_research':212.664,'engineering_research':268.464} and not any(k in ass for k in q.RESEARCH_RESOURCES),
 'economy_other_resources_held':{k:v for k,v in bs.items() if k not in ['minerals','alloys',*q.RESEARCH_RESOURCES]}=={k:v for k,v in ass.items() if k not in ['minerals','alloys',*q.RESEARCH_RESOURCES]},
 'economy_other_fields_raw_held':without(be,{'resources'})==without(ae,{'resources'}),
 'all_other_countries_raw_held':without(br['country'],{'0'})==without(ar['country'],{'0'}),
 'country0_other_direct_fields_raw_held':without(b0,{'modules'})==without(a0,{'modules'}),
 'all_other_country0_modules_raw_held':without(bm,{'standard_economy_module','standard_expansion_module'})==without(am,{'standard_economy_module','standard_expansion_module'}),
 'expansion_original_empty_only_one_list_added':not bx.strip() and without(ax,{'expansion_list'})==[],
 'sole_expansion_exact_target_queue_item':q.scalars(exp)=={'target_planet':124,'construction_queue':3,'construction_queue_item':553648131},
 'sole_expansion_original_species_and_design':q.scalars(q.block(exp,'colonization_data'))=={'species':3321888769} and q.scalars(q.block(exp,'ship_design_implementation'))==design,
 'expansion_default_name_Zirq':[t for t,_,_ in q.tokens(q.block(exp,'name'))]==['key','=','"NEW_COLONY_NAME_1"','variables','=','{','{','key','=','"NAME"','value','=','{','key','=','"Zirq"','}','}','}'],
 'expansion_exact_named_fields':{k for k,v,o in q.fields(exp)}=={'colonization_data','ship_design_implementation','target_planet','construction_queue','construction_queue_item','name'},
 'construction_other_direct_fields_raw_held':without(buildb,{'queue_mgr','item_mgr'})==without(builda,{'queue_mgr','item_mgr'}),
 'queue_mgr_other_fields_raw_held':without(bqm,{'queues'})==without(aqm,{'queues'}),
 'all_other_queues_raw_held':without(bqs,{'3'})==without(aqs,{'3'}),
 'queue3_only_items_appended':not q.block(q.block(bqs,'3'),'items') and q.ids(q.block(q.block(aqs,'3'),'items'))==[553648131] and without(q.block(bqs,'3'),{'items'})==without(q.block(aqs,'3'),{'items'}),
 'queue3_original_owner_starbase_and_type':q.scalars(q.block(aqs,'3'))=={'owner':0,'simultaneous':1,'type':'ships'} and q.scalars(q.block(q.block(aqs,'3'),'location'))=={'type':0,'id':0},
 'item_mgr_other_fields_raw_held':without(bim,{'items'})==without(aim,{'items'}),
 'exact_one_empty_slot_replaced_other_items_raw_held':q.scalars(bi).get('536870915')=='none' and without(bi,{'536870915'})==without(ai,{'553648131'}) and (536870915&0xffffff)==(553648131&0xffffff)==3,
 'paid_item_zero_progress_base360_paying_country0':q.scalars(item)=={'queue':3,'paying_country':0,'progress':0,'progress_needed':360},
 'paid_item_exact_resources':q.scalars(q.block(item,'resources'))=={'minerals':375,'alloys':150},
 'paid_colonyship_original_design_species_starbase':q.scalars(q.block(col,'ship_design_implementation'))==design and q.scalars(q.block(col,'orbitable'))=={'starbase':0} and q.scalars(q.block(col,'colonization_data'))=={'species':3321888769},
 'all_other_roots_raw_held_including_planets_fleets_population':[(k,v,o) for k,v,o in bf if k not in {'country','construction'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction'}],
 'no_country_pending':not any(k=='player_event' and q.scalars(v).get('country')==0 for k,v,o in bf+af),
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','budget_categories']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_PAID_COLONYSHIP_ORDER_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_stocks_before_after':[bc['effective_stockpile'],ac['effective_stockpile']],'original_native_item':item,'original_native_expansion':exp,'scope':'One real375M150A colony ship purchase only; no completion, arrival or established colony claim.'}
out=run/(after+'-paid-colonyship-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original colony ship purchase FAIL retained; no next calendar'
