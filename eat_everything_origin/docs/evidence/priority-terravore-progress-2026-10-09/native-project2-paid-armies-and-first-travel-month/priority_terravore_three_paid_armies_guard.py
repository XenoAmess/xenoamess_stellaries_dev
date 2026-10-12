"""Exact same-day three legitimate paid armies; includes corrected quote interpretation."""
import json,logging,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'));sha=h.sha256
before='terravore-project2-full-month-calibration-01';after='terravore-three-assault-armies-paid'
def read(s):
 a=load(s+'.audit.json')
 with zipfile.ZipFile(run/(s+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,list(q.fields(t)),{k:v for k,v,o in q.fields(t) if o}
omit=lambda raw,keys:[(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=[u['countries']['0'] for u in [b,a]];b0,a0=[q.block(u['country'],'0') for u in [br,ar]];bm,am=[q.block(c,'modules') for c in [b0,a0]];be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
def construction(u,manager,key):return q.block(q.block(u['construction'],manager),key)
bq,aq=[construction(u,'queue_mgr','queues') for u in [br,ar]];bi,ai=[construction(u,'item_mgr','items') for u in [br,ar]]
oldslots={'1107296265','1358954507','100663339'};newids={'1124073481','1375731723','117440555'};ordered=q.ids(q.block(q.block(aq,'1'),'items'));items={i:q.block(ai,i) for i in newids};pre=load(before+'-project2-month-v2-proof.json');px=load(before+'-month-guard-v2-execution.json');invname=after+'-native-diff-detail.json';iv=load(invname)
checks={
 'prior27_PASS_actual0_source_current_SAV':len(pre['checks'])==27 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==sha(Path(px['command'][1]))=='69c904954d2fa1af84f7bd533842a3be4fffb9efc17d7523501ef38070e58e50' and pre['after_sha256']==b['save_sha256'],
 'same_date_exact_original_SAVs':a['date']==b['date']=='2279.03.01' and all(sha(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,b),(after,a)]),
 'corrected_quote_three100M_total300_only':D(str(bc['effective_stockpile']['minerals']))-D(str(ac['effective_stockpile']['minerals']))==300 and {k:v for k,v in bc['effective_stockpile'].items() if k!='minerals'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='minerals'},
 'true_research_banks_and_all_research_raw_held':bc['research_stockpile']==ac['research_stockpile'] and bc['tech_status']==ac['tech_status'],
 'economy_mirrors_native_refresh_to_true_PS_banks_E0_omitted':all(q.scalars(q.block(ae,'resources')).get(k,0)==v for k,v in ac['research_stockpile'].items()),
 'other_economy_resources_exact_held':{k:v for k,v in q.scalars(q.block(be,'resources')).items() if k not in {'minerals',*q.RESEARCH_RESOURCES}}=={k:v for k,v in q.scalars(q.block(ae,'resources')).items() if k not in {'minerals',*q.RESEARCH_RESOURCES}},
 'country0_other_raw_and_other_modules_held':omit(b0,{'modules'})==omit(a0,{'modules'}) and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}),
 'all_other_countries_exact_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'queue1_exact_three_new_orders_only':not q.block(q.block(bq,'1'),'items') and ordered==[1375731723,1124073481,117440555] and omit(q.block(bq,'1'),{'items'})==omit(q.block(aq,'1'),{'items'}) and omit(bq,{'1'})==omit(aq,{'1'}),
 'queue1_owner0_army_planet7_simultaneous1':q.scalars(q.block(aq,'1'))=={'owner':0,'simultaneous':1,'type':'army'} and q.scalars(q.block(q.block(aq,'1'),'location'))=={'type':2,'id':7},
 'three_actual_orders_paid100_progress0_work90':all(q.scalars(v)=={'queue':1,'paying_country':0,'progress':0,'progress_needed':90} and q.scalars(q.block(v,'resources'))=={'minerals':100} for v in items.values()),
 'three_assault_founder73_mother_colony0_only':all(q.scalars(q.block(v,'buildable_army'))=={'army_type':'assault_army','species':73,'planet':0,'starbase':4294967295} and [(k,o) for k,w,o in q.fields(v) if o]==[('resources',True),('buildable_army',True)] for v in items.values()),
 'same3_native_handle_slots_other_construction_raw_held':all(q.scalars(bi).get(i)=='none' for i in oldslots) and {int(i)&0xffffff for i in oldslots}=={int(i)&0xffffff for i in newids} and omit(bi,oldslots)==omit(ai,newids) and omit(br['construction'],{'queue_mgr','item_mgr'})==omit(ar['construction'],{'queue_mgr','item_mgr'}) and all(omit(q.block(br['construction'],mgr),{key})==omit(q.block(ar['construction'],mgr),{key}) for mgr,key in [('queue_mgr','queues'),('item_mgr','items')]),
 'only_known_fleet65_native_dirty_cloaking_cache':omit(br['fleet'],{'65'})==omit(ar['fleet'],{'65'}) and omit(q.block(br['fleet'],'65'),{'properties'})==omit(q.block(ar['fleet'],'65'),{'properties'}) and omit(q.block(q.block(br['fleet'],'65'),'properties'),{'dirty_cloaking_strength'})==omit(q.block(q.block(ar['fleet'],'65'),'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(q.block(br['fleet'],'65'),'properties')) and q.scalars(q.block(q.block(ar['fleet'],'65'),'properties')).get('dirty_cloaking_strength')=='yes',
 'all_other_world_raw_held_no_army_or_ship_birth':[(k,v,o) for k,v,o in bf if k not in {'country','construction','fleet','random_count'}]==[(k,v,o) for k,v,o in af if k not in {'country','construction','fleet','random_count'}],
 'native_random3_for_three_clicks_only':int(next(v for k,v,o in af if k=='random_count'))-int(next(v for k,v,o in bf if k=='random_count'))==3,
 'EEP_population_structure_government_budget_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','situations','event_targets']) and all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis','budget_categories']),
 'three_distinct_normal_clicks_actual0':all(load('terravore-'+n+'-assault-army-recruit-click-execution.json')['returncode']==0 and load('terravore-'+n+'-assault-army-recruit-click.action.json')['client_point']==[580,326] for n in ['first','second','third']),
 'native_save_actual0_unchanged_original_error':load(after+'-native-save-execution.json')['returncode']==0 and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
 'native_readonly_difference_INV_bound':sha(run/invname)=='c80495237ea4f2142769cdfd979e196ebad8a1b590d023e26fdd84cb5f5f26ac' and iv['stages']==[before,after],
 'production41_tree_CN_020_held':len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and meta['language']=='l_simp_chinese' and meta['version']=='0.2.0',
}
passed=all(v is True for v in checks.values());out=run/(after+'-paid-armies-proof.json');assert not out.exists();h.write_json(out,{'status':'PASS_TERRAVORE_THREE_NATIVE_PAID_ARMIES_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'ordered_ids':ordered,'items_raw':items,'actual_paid_minerals':300,'quote_interpretation_correction':'Original90M assumption wrong; actual100M per native order,90work. No compensation or repeated purchase.','boundaries':['native_army_recruitment_and_expansion_review_required'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0});print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
