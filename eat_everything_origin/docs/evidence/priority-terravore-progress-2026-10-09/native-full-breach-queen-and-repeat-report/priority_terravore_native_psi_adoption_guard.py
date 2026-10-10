"""Actual paid native hive psi adoption and exact species transformation boundary."""
import json, logging, shutil, sys, zipfile
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path
before, after, prefile, prestage, quote = sys.argv[1:]
quote=int(quote)
sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def obj(t):return {k:v for k,v,o in q.fields(t) if o}
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,obj(t)
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/prefile).read_text('utf-8'));ex=json.loads((run/(prestage+'-execution.json')).read_text('utf-8'))
paid=D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']))
old,new=bc['native']['founder_species_ref'],ac['native']['founder_species_ref']
bs,ass=obj(br['species_db']),obj(ar['species_db']);oldraw,newraw=bs[str(old)],ass[str(new)]
traits=lambda t:[q.unquote(v) for k,v,o in q.fields(q.block(t,'traits')) if k=='trait' and not o]
pending=lambda t:[q.scalars(v) for k,v,o in q.fields(t) if k=='player_event' and o and q.scalars(v).get('country')==0]
bp,ap=pending(bt),pending(at)
ns={k:v for k,v in a['situations'].items() if k not in b['situations']}
bcr,acr=q.block(br['country'],'0'),q.block(ar['country'],'0')
checks={
 'actual_prior_Theory_PASS_exit0':pre['status']=='PASS_NATIVE_TERRAVORE_UNITY_NODES_THEORY_COMPLETE_COMPONENT' and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0,
 'same_date_original_SHA':a['date']==b['date']=='2242.05.02' and h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'normal_confirmation_quote_affordable_exact_payment':0<paid<=D(str(bc['effective_stockpile']['unity'])) and int(paid.to_integral_value(rounding=ROUND_CEILING))==quote==2607 and paid==D('2606.73943'),
 'other_effective_stocks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='unity'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='unity'},
 'complete_native_tech_and_true_banks_held':bc['tech_status']==ac['tech_status'] and bc['research_stockpile']==ac['research_stockpile']=={'physics_research':0,'society_research':0,'engineering_research':0},
 'only_native_adoption_added':ac['traditions']==bc['traditions']+['tr_psionics_shroud_adopt'] and ac['ascension_perks']==bc['ascension_perks'],
 'government_and_EEP_state_held_no_early_award':bc['government']==ac['government'] and bc['variables']==ac['variables'] and bc['flags']==ac['flags'] and ac['variables']['eep_psi']==0 and 'eep_psi_notice' not in ac['flags'],
 'only_native_access_flag_added':omit(q.block(bcr,'flags'),{'can_access_shroud'})==omit(q.block(acr,'flags'),{'can_access_shroud'}) and q.scalars(q.block(acr,'flags')).get('can_access_shroud')==63173784 and 'can_access_shroud' not in q.scalars(q.block(bcr,'flags')),
 'one_native_intro_pending':not bp and len(ap)==1 and ap[0]['id']==153 and ap[0]['event']=='shroud.2750',
 'one_native_breach_situation_zero':len(ns)==1 and next(iter(ns.values()))=={'country':0,'type':'situation_breach_shroud','progress':0,'last_month_progress':0,'approach':'approach_situation_breach_shroud_nothing','stage':0,'target':{'type':'country','id':0,'opener_id':4294967295},'variables':{}},
 'old_situations_held':all(a['situations'].get(k)==v for k,v in b['situations'].items()),
 'old_species_db_raw_held_one_new_template':old==3321888769 and new==66 and set(ass)==set(bs)|{str(new)} and all(ass[k]==v for k,v in bs.items()),
 'exact_latent_template_copy':q.scalars(newraw).get('base_ref')==old and omit(newraw,{'base_ref','traits'})==omit(oldraw,{'traits'}) and traits(newraw)==traits(oldraw)+['trait_latent_psionic'],
 'country_founder_only_native_field_change':{k:v for k,v in bc['native'].items() if k!='founder_species_ref'}=={k:v for k,v in ac['native'].items() if k!='founder_species_ref'},
 'all_original_ships_raw_held':br['ships']==ar['ships'],
 'all_construction_zones_buildings_districts_held':all(br[k]==ar[k] for k in ['construction','zones','buildings','districts']),
 'all_jobs_and_planets_deposits_EEP_binding_held':all(b[k]==a[k] for k in ['pop_jobs','planets','deposits','event_targets']),
 'actual_owned_population_held':bc['owned_colonies']==ac['owned_colonies']==[0] and b['colonies']['0']['actual_pop_sum']==a['colonies']['0']['actual_pop_sum']==8899,
 'unfiltered_error_original_bytes_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
bg,ag=obj(br['pop_groups']),obj(ar['pop_groups']);changed_groups=[];groups_ok=set(bg)==set(ag)
for i,v in bg.items():
 key=q.scalars(q.block(v,'key'));own=key.get('species')==old and q.scalars(v).get('planet')==0
 if own:
  changed_groups.append(i);groups_ok &= omit(v,{'key'})==omit(ag[i],{'key'}) and q.scalars(q.block(ag[i],'key'))=={**key,'species':new}
 else:groups_ok &= v==ag[i]
checks['exact_three_owned_groups_only_species_change']=groups_ok and len(changed_groups)==3
changes={}
for root,expected in [('leaders',20),('army',9)]:
 x,y=obj(br[root]),obj(ar[root]);ok=set(x)==set(y);changed=[]
 for i,v in x.items():
  if q.scalars(v).get('species')==old and q.scalars(v).get('country',q.scalars(v).get('owner'))==0:
   changed.append(i);ok &= omit(v,{'species'})==omit(y[i],{'species'}) and q.scalars(y[i]).get('species')==new
  else:ok &= v==y[i]
 changes[root]=changed;checks[root+'_exact_owned_species_only']=ok and len(changed)==expected
bf,af=obj(br['fleet']),obj(ar['fleet']);fleet_ok=set(bf)==set(af);dirty=[]
for i,v in bf.items():
 if v==af[i]:continue
 dirty.append(i);x,y=q.block(v,'properties'),q.block(af[i],'properties')
 fleet_ok &= omit(v,{'properties'})==omit(af[i],{'properties'}) and omit(x,{'dirty_cloaking_strength'})==omit(y,{'dirty_cloaking_strength'}) and q.scalars(y).get('dirty_cloaking_strength')=='yes'
checks['fleets_only_recorded_dirty_cloaking_cache']=fleet_ok and len(dirty)==21
bco,aco=obj(br['colony']),obj(ar['colony']);skip={'housing_usage','free_housing','amenities','free_amenities'}
checks['colony_only_precise_four_cache_fields']=set(bco)==set(aco) and all(v==aco[i] for i,v in bco.items() if i!='0') and omit(bco['0'],skip)==omit(aco['0'],skip) and all(a['colonies']['0'][k]==v for k,v in {'housing_usage':8899,'free_housing':4901,'amenities':20673.8,'free_amenities':14485.6}.items()) and a['colonies']['0']['total_housing']-a['colonies']['0']['housing_usage']==a['colonies']['0']['free_housing'] and abs(a['colonies']['0']['amenities']-a['colonies']['0']['amenities_usage']-a['colonies']['0']['free_amenities'])<.00001
foreign_b,foreign_a=obj(br['country']),obj(ar['country']);checks['all_foreign_country_raw_held']=set(foreign_b)==set(foreign_a) and all(foreign_a[i]==v for i,v in foreign_b.items() if i!='0')
sources=[h.GAME_EXE.parent/'common/traditions/01_psionics_shroud.txt',h.GAME_EXE.parent/'events/shroud_situation_events.txt',h.GAME_EXE.parent/'common/scripted_effects/shroud_shadows_scripted_effects.txt']
p={'status':'PASS_NATIVE_TERRAVORE_PSI_ADOPTION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_unity_paid':str(paid),'old_new_founder':[old,new],'transformed_group_ids':changed_groups,'transformed_objects':changes,'fleet_dirty_cache_ids':dirty,'pending':ap,'native_situations':ns,'native_sources':[{'path':str(s),'sha256':h.sha256(s)} for s in sources],'raw_research_mirror_before_after':[{k:v for k,v in c['stockpile'].items() if k.endswith('_research')} for c in [bc,ac]],'scope':'Real normal paid hive native adoption and precise transformation only; native intro ACK, comprehensive rights verification, full month and Shroud endpoint pending.'}
out=run/(after+'-psi-adoption-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original native adoption FAIL retained; no repayment'
