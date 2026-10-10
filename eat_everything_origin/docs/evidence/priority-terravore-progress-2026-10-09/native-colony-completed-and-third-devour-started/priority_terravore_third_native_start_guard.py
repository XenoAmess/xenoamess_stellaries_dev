"""Exact read-only third native consume start; actual state and immutable evidence."""
import json, logging, re, shutil, sys, zipfile
from pathlib import Path
before, after = sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
logging.disable(logging.INFO); h = r.harness; run, user, meta = h.load_run()
assert meta['version'] == '0.2.0' and meta['language'] == 'l_simp_chinese'
dest = run / Path(__file__).name
if dest.exists(): assert dest.read_bytes() == Path(__file__).read_bytes()
else: shutil.copyfile(__file__, dest)
load = lambda name: json.loads((run / name).read_text('utf-8'))
def read(stage):
    with zipfile.ZipFile(run / (stage + '.sav')) as z:
        fs = list(q.fields(z.read('gamestate').decode('utf-8-sig')))
    return load(stage + '.audit.json'), fs, {k:v for k,v,o in fs if o}
def omit(raw, keys): return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
def objs(raw): return {k:v for k,v,o in q.fields(raw) if o}
b,bf,br=read(before);a,af,ar=read(after)
bc,ac=b['countries']['0'],a['countries']['0'];bp,ap=b['planets']['1085'],a['planets']['1085']
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
source_b,source_a=[q.block(q.block(t['planets'],'planet'),'1085') for t in [br,ar]]
pre=load(before+'-war1-battle-v29-proof.json');ex=load(before+'-battle-v29-execution.json')
click=load('terravore-colony1085-devour-entry-click-execution.json')
action=load('terravore-colony1085-devour-entry-click.action.json')
save_ex=load(after+'-native-save-execution.json')
sits={i:v for i,v in a['situations'].items() if v.get('type')=='situation_eep_devouring'}
pending=[q.scalars(v) for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks={
 'exact_original_same_date_SHA_pair':before=='terravore-colony1085-completion-boundary2' and after=='terravore-colony1085-devour-started' and a['date']==b['date']=='2270.02.01' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='ae5c07eb6112d217a7e9163c4b1ed8f4610083a8700ede82b73527c9b357202f' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='e030634f1d921a002869cff7a5a3639e0aae56fb9b5a93455d4158572b10281a',
 'prior_actual_colony_complete_V29_46PASS_actual0_bound':pre['status'].startswith('PASS') and len(pre['checks'])==46 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0 and ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v29.py')=='7643c09fc6e6b1cce4dbb04c4ec1a4ce9ac6b3a8aaa6b2d052bf6c3d3014e35d',
 'actual_normal_UI_click_and_save_actual0':click['returncode']==save_ex['returncode']==0 and click['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and save_ex['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and action['action']=='left-click' and action['client_point']==[790,170],
 'actual_Q12_T29_seed103_need_minus3':bp['variables']=={} and ap['variables']=={'eep_q':12,'eep_old_damage':0,'eep_months':29,'eep_seed_existing':103,'eep_seed_need':-3},
 'source_complete_owned_alpine12_not_core':all(ap.get(k)==v for k,v in {'owner':0,'controller':0,'colony':37,'planet_size':12,'planet_class':'pc_alpine','colonize_date':'2270.02.01'}.items()) and 'colonizing_species' not in a['colonies']['37'] and a['planets']['7']['colony']==0,
 'all_real_economy_and_three_research_banks_held':bc['effective_stockpile']==ac['effective_stockpile'] and ac['effective_stockpile']['society_research']==6458.22177 and ac['effective_stockpile']['physics_research']==ac['effective_stockpile']['engineering_research']==0,
 'source103_founder_population_and_mother10826_no_resettle':a['colonies']['37']['actual_pop_sum']==b['colonies']['37']['actual_pop_sum']==103 and a['colonies']['0']['actual_pop_sum']==b['colonies']['0']['actual_pop_sum']==10826 and all(g['key']['species']==73 for g in a['pop_groups'].values() if g['planet']==37 and g['size']>0),
 'exact_six_flags_native360_cooldown':set(ap['flags'])-set(bp['flags'])=={'eep_active','eep_owned_colony_event','colony_event','eep_native','being_devoured','recently_eaten_planet'} and all(ap['flags'][k]==v for k,v in bp['flags'].items()) and all(ap['flags'][k]==63413520 for k in ['eep_active','eep_owned_colony_event','colony_event','eep_native','being_devoured']) and ap['flags']['recently_eaten_planet']=={'flag_date':63413520,'flag_days':360},
 'exact_native_permanent_modifier':not bp['modifiers'] and [v for v,_,_ in q.tokens(ap['modifiers'])]==[v for v,_,_ in q.tokens('items={ { modifier="being_devoured_modifier" days=-1 } }')],
 'source_other_physical_raw_held':omit(source_b,{'variables','flags','modifiers'})==omit(source_a,{'variables','flags','modifiers'}),
 'exact_unique_EEP_task100663299_progress0':sits=={'100663299':{'country':0,'type':'situation_eep_devouring','progress':0,'last_month_progress':0,'approach':'eep_devour_approach','stage':0,'target':{'type':'planet','id':1085,'opener_id':4294967295},'variables':{}}},
 'no_native_duplicate_and_other_situations_held':not any(v.get('type')=='situation_terravore_consume_planet' for v in a['situations'].values()) and all(a['situations'].get(i)==v for i,v in b['situations'].items()),
 'exact_task_actor_added':a['event_targets']==b['event_targets']+[{'type':'country','id':0,'opener_id':4294967295,'name':'eep_task_actor1085'}],
 'all_other_physical_planets_raw_held':omit(q.block(br['planets'],'planet'),{'1085'})==omit(q.block(ar['planets'],'planet'),{'1085'}),
 'all_other_countries_raw_held':omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'country0_other_raw_fields_held':omit(bcr,{'events','modules'})==omit(acr,{'events','modules'}),
 'country0_events_only_new_situation_reference':omit(q.block(bcr,'events'),{'situations'})==omit(q.block(acr,'events'),{'situations'}) and not q.block(q.block(bcr,'events'),'situations') and q.ids(q.block(q.block(acr,'events'),'situations'))==[100663299],
 'no_pending_and_strict2814_error_bytes':not pending and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb',
 'all_other_top_level_full_fields_held':[(k,v,o) for k,v,o in bf if k not in {'planets','country','saved_event_target','random_count','situations'}]==[(k,v,o) for k,v,o in af if k not in {'planets','country','saved_event_target','random_count','situations'}],
}
bm,am=[q.block(cr,'modules') for cr in [bcr,acr]]
be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
checks['modules_only_exact_research_display_refresh']=omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}) and q.scalars(q.block(ae,'resources'))=={k:v for k,v in ac['effective_stockpile'].items() if k not in {'physics_research','engineering_research'}} and q.scalars(q.block(be,'resources'))=={**bc['effective_stockpile'],'physics_research':87.7785,'society_research':6467.11601,'engineering_research':92.4285}
for k in ['variables','flags','government','traditions','ascension_perks','tech_status','owned_colonies']:
    checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','districts','deposits','species']:
    checks[k+'_held']=b[k]==a[k]
checks['exact_current_production_start_definition_sources_bound']=all(h.sha256(Path(path))==sha for path,sha in {'eat_everything_origin/mod/common/decisions/zz_eep_native_decision.txt': '155adeb0ad4a0f4e3c1a81f6d14840e3d9a2f70883a10e7ed637c786407b2f72', 'eat_everything_origin/mod/common/scripted_effects/eep_effects.txt': '03fd2ba55bd33f7b61cd2fdc1c5bbd1e6548ae967a1b464915812531ecb63df8', 'eat_everything_origin/mod/common/situations/eep_situation.txt': '64c9fc80f7d8b316b4948fb000fa45886b30be1ba4237589ac0676c6648d6d3e'}.items())
proof={'status':'PASS_TERRAVORE_THIRD_NATIVE_START_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'actual_situations':sits,'source_variables':ap['variables'],'source_flags':ap['flags'],'actual_stockpiles':ac['effective_stockpile'],'calendar_ready':all(checks.values()),'scope':'Third legal native consume on completed colony1085; no population creation, relocation or reward, no monthly bite/completion/full route acceptance yet.'}
out=run/(after+'-third-start-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps(proof),flush=True);assert all(checks.values()),'Original start differences retained; no repeated UI input'
