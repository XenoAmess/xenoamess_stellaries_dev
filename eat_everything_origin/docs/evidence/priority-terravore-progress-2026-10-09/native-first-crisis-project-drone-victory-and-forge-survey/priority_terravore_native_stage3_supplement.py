"""Source-bound native stage3 conversion; original42 phase2 FAIL retained."""
import json,logging,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-before-stage3';after='terravore-native-stage3-pending'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t,{k:v for k,v,o in q.fields(t) if o}
def obj(t):return {k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def traits(t):return [q.unquote(v) for k,v,o in q.fields(q.block(t,'traits')) if k=='trait' and not o]
def leadertraits(t):return [q.unquote(v) for k,v,o in q.fields(t) if k=='traits' and not o]
def anonymous(t):
 out=[];depth=0;start=None
 for token,beg,end in q.tokens(t):
  if token=='{':
   if depth==0:start=end
   depth+=1
  elif token=='}':
   depth-=1;assert depth>=0
   if depth==0:out.append(t[start:beg])
  elif depth==0:raise ValueError('Expected native anonymous object')
 assert depth==0;return out
b,bt,br=read(before);a,at,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0'];orig=json.loads((run/(after+'-meditate-stage2-proof.json')).read_text('utf-8'));ex=json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))
failed={'no_country0_pending','species_held','one_native_breach_stage2_progress_only','one_latent_lithoid_hive_species','all_native_breach_raw_except_progress_held'}
bs,ass=[q.block(q.block(rt['situations'],'situations'),'16777221') for rt in [br,ar]];flags=q.scalars(q.block(bs,'flags'));pending=[v for k,v,o in q.fields(at) if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={
 'original42_exact_five_FAIL_exit1':orig['status']=='FAIL' and len(orig['checks'])==42 and {k for k,v in orig['checks'].items() if not v}==failed and ex['returncode']==1,
 'remaining37_original_checks_all_true':all(v is True for k,v in orig['checks'].items() if k not in failed),
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256']==orig['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==orig['after_sha256'],
 'unique_calendar_30_days_exit0':b['date']=='2254.10.02' and a['date']=='2254.11.02' and orig['days']==30 and json.loads((run/(after+'-observe-execution.json')).read_text('utf-8'))['returncode']==0,
 'exact750_crossing_observed_rate':b['situations']['16777221']['progress']==744.35104 and a['situations']['16777221']['progress']==750.13916 and a['situations']['16777221']['last_month_progress']==5.78812,
 'only_exact_native_stage3_fields':q.scalars(bs)['stage']==1 and q.scalars(ass)['stage']==2 and q.block(bs,'stage_flags').split()==['yes','yes','no'] and q.block(ass,'stage_flags').split()==['yes','yes','yes'] and q.scalars(q.block(ass,'flags'))=={**flags,'breach_shroud_stage_3_started':63281760} and omit(bs,{'progress','last_month_progress','stage','stage_flags','flags'})==omit(ass,{'progress','last_month_progress','stage','stage_flags','flags'}),
 'unique189_native2780_situation_pending':len(pending)==1 and q.scalars(pending[0])=={'id':189,'event':'shroud.2780','date':'2257.02.01','country':0} and q.scalars(q.block(pending[0],'scope')).get('type')=='situation' and q.scalars(q.block(pending[0],'scope')).get('id')==16777221,
 'no_early_EEP_reward_or_notice':bc['variables']==ac['variables'] and ac['variables']['eep_psi']==0 and 'eep_psi_notice' not in ac['flags'],
 'original_ruler_preserved_founder66_to73':bc['native']['ruler']==ac['native']['ruler']==167772189 and bc['native']['founder_species_ref']==66 and ac['native']['founder_species_ref']==73,
}
bsd,asd=obj(br['species_db']),obj(ar['species_db']);old,new=bsd['66'],asd['73']
checks['only_one_new73_all_old_species_raw_held']=set(asd)==set(bsd)|{'73'} and all(asd[i]==v for i,v in bsd.items())
checks['exact_full_psionic_same_lithoid_hive_template']=set(b['species'])=={'66'} and set(a['species'])=={'73'} and omit(old,{'traits'})==omit(new,{'traits'}) and traits(new)==[v for v in traits(old) if v!='trait_latent_psionic']+['trait_psionic'] and q.scalars(new)['base_ref']==3321888769 and q.scalars(new)['class']=='LITHOID' and q.scalars(new)['portrait']=='lith11'
bg,ag=b['pop_groups'],a['pop_groups'];groups_ok=set(bg)==set(ag)=={'1','14','15'}
for i,v in bg.items():
 expected={**v,'key':{**v['key'],'species':73}}
 if i=='1':expected.update(size=2574,last_month_growth=7,month_start_size=2574,power=25.74,crime=25.74,housing_usage=2574)
 groups_ok &= ag[i]==expected and v['key']['species']==66
checks['three_actual_groups_only_template_and_native_birth7']=groups_ok
growth=q.block(q.block(ar['colony'],'0'),'last_month_growth_data');gd=q.scalars(q.block(growth,'growth_and_size'))
checks['actual_total_population_conserved_plus_native_birth7']=b['colonies']['0']['actual_pop_sum']==9659 and a['colonies']['0']['actual_pop_sum']==9666 and gd=={'month_start_size':9659,'growth':7} and [(k,q.unquote(v),o) for k,v,o in q.fields(q.block(growth,'current_month_growth_details'))]==[('key','GROWTH_CAT_GROWTH',False),('value',7,False),('key','GROWTH_CAT_PROMOTION',False),('value',0,False)]
jobs_ok=set(b['pop_jobs'])==set(a['pop_jobs']);jobchanges={}
for i,v in b['pop_jobs'].items():
 expected=dict(v)
 if i=='7':expected.update(workforce=2573,bonus_workforce=515.8)
 if i=='22':expected['bonus_workforce']=720
 if i in ['23','24','25']:expected['bonus_workforce']=54
 if i=='567':expected['bonus_workforce']=60
 jobs_ok &= a['pop_jobs'][i]==expected
 if v!=a['pop_jobs'][i]:jobchanges[i]=[v,a['pop_jobs'][i]]
checks['all_actual_jobs_exact_only_native_bonus_and_birth']=jobs_ok
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];bm,am=[q.block(c,'modules') for c in [bcr,acr]];bri,ari=[q.block(md,'standard_species_rights_module') for md in [bm,am]];bp,ap=[q.scalars(q.block(v,'primary')) for v in [bri,ari]]
bl,al=[anonymous(q.block(v,'species_rights')) for v in [bri,ari]]
checks['primary_rights_only66_to73']=ap=={**bp,'species_index':73} and bp['species_index']==66 and omit(bri,{'primary','species_rights'})==omit(ari,{'primary','species_rights'})
checks['old_rights_raw_held_one_exact73_rights_copy']=len(bl)==2 and len(al)==3 and {q.scalars(v)['species_index'] for v in al}=={66,73,3321888769} and all(v in al for v in bl) and [q.scalars(v) for v in al if q.scalars(v)['species_index']==73]==[{**bp,'species_index':73}]
checks['default_species_only_base_mapping66_to73']=q.scalars(q.block(bcr,'default_species'))=={'3321888769':66} and q.scalars(q.block(acr,'default_species'))=={'3321888769':73}
bflags,aflags=[q.block(c,'flags') for c in [bcr,acr]];oldtimed={k:q.scalars(v) for k,v,o in q.fields(bflags) if o};newtimed={k:q.scalars(v) for k,v,o in q.fields(aflags) if o}
checks['only_native_toast_flag_and_exact_old_timers']=q.scalars(bflags)==q.scalars(aflags) and newtimed=={**{k:{**v,'flag_days':v['flag_days']-30} for k,v in oldtimed.items()},'psionic_leader_toast':{'flag_date':63281760,'flag_days':29}}
leaders_b,leaders_a=obj(br['leaders']),obj(ar['leaders']);own={i:v for i,v in leaders_b.items() if q.scalars(v).get('country')==0};actualown={i:v for i,v in leaders_a.items() if q.scalars(v).get('country')==0}
xp={'150994969':'6.75','167772189':'13.8','74':'6.75','76':'6.75','77':'14','78':'13.5','79':'14','80':'11.5','81':'5.75'}
prepend={'184549381','150994969','33554467','16777275','16777283','74','76','81','16777403','33554620','33554662'};leaders_ok=set(own)==set(actualown) and len(own)==20
for i,v in own.items():
 nv=actualown[i];sc,nsc=q.scalars(v),q.scalars(nv);expected_traits=leadertraits(v)
 if i in prepend:expected_traits=['leader_trait_psionic']+expected_traits
 if i=='167772189':expected_traits+=['leader_trait_psionic']
 leaders_ok &= sc['species']==66 and nsc['species']==73 and omit(v,{'species','traits','experience'})==omit(nv,{'species','traits','experience'}) and leadertraits(nv)==expected_traits
 if i in xp:leaders_ok &= D(str(nsc['experience']))-D(str(sc['experience']))==D(xp[i])
 else:leaders_ok &= nsc.get('experience')==sc.get('experience')
checks['twenty_owned_leaders_exact_species_traits_experience_portraits']=leaders_ok
checks['foreign_existing_leader_species_and_traits_held']=all(q.scalars(leaders_a[i]).get('species')==q.scalars(v).get('species') and leadertraits(leaders_a[i])==leadertraits(v) for i,v in leaders_b.items() if q.scalars(v).get('country')!=0)
armyb,armya=obj(br['army']),obj(ar['army']);ownarmy={i:v for i,v in armyb.items() if q.scalars(v).get('owner')==0}
checks['twelve_owned_armies_only_species_changed']=len(ownarmy)==12 and set(ownarmy)=={i for i,v in armya.items() if q.scalars(v).get('owner')==0} and all(q.scalars(v).get('species')==66 and q.scalars(armya[i]).get('species')==73 and omit(v,{'species'})==omit(armya[i],{'species'}) for i,v in ownarmy.items())
checks['foreign_existing_army_species_held']=all(q.scalars(armya[i]).get('species')==q.scalars(v).get('species') for i,v in armyb.items() if q.scalars(v).get('owner')!=0)
source=h.GAME_EXE.parent/'events/shroud_situation_events.txt';stage_source=h.GAME_EXE.parent/'common/situations/13_shroud_situations.txt';effects=h.GAME_EXE.parent/'common/scripted_effects/shroud_shadows_scripted_effects.txt';nodes=h.GAME_EXE.parent/'common/scripted_effects/paragon_effects.txt';latent=h.GAME_EXE.parent/'common/inline_scripts/traits/latent_psionic_effects.txt';full=h.GAME_EXE.parent/'common/inline_scripts/traits/psionic_effects.txt'
ev=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='shroud.2780'];assert len(ev)==1;imm=q.block(q.block(q.block(ev[0],'immediate'),'owner'),'if');hook=q.block(q.block(q.block(q.block(stage_source.read_text('utf-8-sig'),'situation_breach_shroud'),'stages'),'stage_3'),'on_first_enter')
checks['native_stage3_exact_hook_and_great_awakening_immediate']=q.scalars(hook)=={'set_situation_flag':'breach_shroud_stage_3_started','remove_situation_flag':'breach_shroud_approach_selected'} and q.scalars(q.block(hook,'situation_event'))=={'id':'shroud.2780'} and q.scalars(q.block(imm,'limit'))=={'has_tradition':'tr_psionics_shroud_great_awakening'} and q.scalars(imm)=={'turn_main_species_to_psionic':'yes','update_node_portraits_if_gestalt_effect':'yes','update_every_leader_from_psionic_countries':'yes','refresh_portraits':'character'}
eff=q.block(effects.read_text('utf-8-sig'),'turn_main_species_to_psionic');add=q.block(effects.read_text('utf-8-sig'),'add_psionic_trait')
checks['native_conversion_source_targets_actual_groups_leaders_armies']=all(key in eff for key in ['change_dominant_species','every_owned_pop_group','every_owned_leader','every_pool_leader','every_envoy','every_owned_army','every_controlled_ship']) and q.scalars(q.block(q.block(add,'else_if'),'modify_species'))=={'species':'this','remove_trait':'trait_latent_psionic','add_trait':'trait_psionic'}
checks['native_trait_bonus_source_exact5_to10percent']=q.scalars(q.block(latent.read_text('utf-8-sig'),'modifier'))=={'researcher_jobs_bonus_workforce_mult':0.05,'bureaucrat_jobs_bonus_workforce_mult':0.05,'telepath_jobs_bonus_workforce_mult':0.05} and q.scalars(q.block(full.read_text('utf-8-sig'),'modifier'))=={'researcher_jobs_bonus_workforce_mult':0.1,'bureaucrat_jobs_bonus_workforce_mult':0.1,'telepath_jobs_bonus_workforce_mult':0.1}
p={'status':'PASS_NATIVE_TERRAVORE_STAGE3_CONVERSION_PENDING_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':False,'pending':[q.scalars(v) for v in pending],'new_species':a['species'],'actual_population_before_after':[9659,a['colonies']['0']['actual_pop_sum']],'native_growth_raw':growth,'job_changes':jobchanges,'owned_leader_ids':list(own),'owned_army_ids':list(ownarmy),'actual_native_experience_increments':xp,'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,stage_source,effects,nodes,latent,full]],'scope':'Exact native stage3 immediate conversion with original37 checks mandatory and42 FAIL retained. No calendar clearance, full breach, Queen notice or Mod payout claim.'}
out=run/(after+'-stage3-conversion-supplement.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Native stage3 original supplement FAIL retained; no replay'
