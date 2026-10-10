"""Read-only exact native mature MOM launch; immutable bounded component proof."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(s):
 a=json.loads((run/(s+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(s+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 roots={k:v for k,v,o in fs if o};return a,fs,roots
def omit(t,keys):return [(k,v,o) for k,v,o in q.fields(t) if k not in keys]
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
def vals(t):return [q.unquote(v) for v,_,_ in q.tokens(t)]
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bcs,acs=objs(br['country']),objs(ar['country']);bg,ag=bc['government'],ac['government']
bt,at=bc['tech_status'],ac['tech_status'];ba,aa=q.block(bt,'alternatives'),q.block(at,'alternatives')
oldcd=[v for k,v,o in q.fields(bg) if k=='council_agenda_cooldowns']
newcd=[v for k,v,o in q.fields(ag) if k=='council_agenda_cooldowns']
bv,av=q.block(bcs['0'],'variables'),q.block(acs['0'],'variables')
pre=json.loads((run/(before+'-second-psionic-wait-proof.json')).read_text('utf-8'))
click=json.loads((run/'terravore-MOM-normal-launch-click.action.json').read_text('utf-8'))
execution=json.loads((run/'terravore-MOM-normal-launch-click-execution.json').read_text('utf-8'))
ui=json.loads((run/'terravore-theory-choice-bar-capture.ocr.json').read_text('utf-8'))
native=Path('C:/SteamLibrary/steamapps/common/Stellaris')
paths=[native/'common/council_agendas/02_council_agendas_ascensions.txt',native/'common/scripted_variables/05_scripted_variables_paragon.txt',native/'events/focus_events_1.txt']
agenda,variables,focus=[p.read_text('utf-8-sig') for p in paths]
fleets=['0','1','2','3','136','137','138','139','140','161','166','167','171','172','174','178','183','196','198','477','490']
fb,fa=objs(br['fleet']),objs(ar['fleet']);changed_fleets=[k for k in fb if fb[k]!=fa.get(k)]
sb,sa=q.block(br['starbase_mgr'],'starbases'),q.block(ar['starbase_mgr'],'starbases')
sbo,sao=objs(sb),objs(sa)
checks={
 'bound_original_wait_25_PASS':pre['status'].startswith('PASS_') and len(pre['checks'])==25 and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'same_date_original_SHA_pair':b['date']==a['date']=='2235.04.01' and b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'single_recorded_normal_launch_click':click['action']=='left-click' and click['client_point']==[502,410] and click['foreground_after']==click['expected_hwnd'] and execution['returncode']==0 and execution['command'][-2:]==['502','410'],
 'mature_MOM3528_to_empty':q.scalars(bg).get('council_agenda')=='agenda_mind_over_matter' and q.scalars(bg).get('council_agenda_progress')==3528 and not any(k in q.scalars(ag) for k in ['council_agenda','council_agenda_progress']),
 'only_append_exact_native_cooldown':len(oldcd)==1 and len(newcd)==2 and newcd[:-1]==oldcd and q.scalars(newcd[-1])=={'council_agenda':'agenda_mind_over_matter','start_date':'2238.04.01'} and '@ascension_agenda_cooldown = 1080' in agenda,
 'other_government_raw_held':omit(bg,['council_agenda','council_agenda_progress','council_agenda_cooldowns'])==omit(ag,['council_agenda','council_agenda_progress','council_agenda_cooldowns']),
 'native_focus_counter_only_1_to2':q.scalars(bv)['focus_agendas_completed']==1 and q.scalars(av)['focus_agendas_completed']==2 and omit(bv,['focus_agendas_completed'])==omit(av,['focus_agendas_completed']) and 'id = focus.105' in focus and bool(re.search(r'which\s*=\s*focus_agendas_completed\s+value\s*=\s*1',focus)),
 'only_new_Theory650_specialized_progress':not q.block(bt,'stored_techpoints_for_tech') and q.scalars(q.block(at,'stored_techpoints_for_tech'))=={'tech_psionic_theory':650},
 'actual_UI650_of2600_matches_native25percent':h.sha256(run/'terravore-theory-choice-bar-capture.jpg')=='1f389fe46db5b2415829e0914923e63840897d8b7c06890206bc26fe8d5a18ed' and any(x['text']=='650/2600' for x in ui['rows']) and D(2600)*D('.25')==D(650) and bool(re.search(r'@agenda_award_tech_progress\s*=\s*0\.25',variables)) and 'tech = tech_psionic_theory' in agenda and 'progress = @agenda_award_tech_progress' in agenda,
 'Theory_not_completed_before_or_after':all('tech_psionic_theory' not in c['completed_technologies'] for c in [bc,ac]),
 'only_append_Theory_society_candidate':vals(q.block(aa,'society'))==vals(q.block(ba,'society'))+['tech_psionic_theory'] and omit(ba,['society'])==omit(aa,['society']),
 'only_append_Theory_always_available':[(k,v,o) for k,v,o in q.fields(at) if k=='always_available_tech']==[(k,v,o) for k,v,o in q.fields(bt) if k=='always_available_tech']+[('always_available_tech','"tech_psionic_theory"',False)],
 'all_other_tech_fields_raw_held':omit(bt,['stored_techpoints_for_tech','alternatives','always_available_tech'])==omit(at,['stored_techpoints_for_tech','alternatives','always_available_tech']),
 'true_three_banks_zero_held':q.research_stocks(bt)==q.research_stocks(at)==dict.fromkeys(q.RESEARCH_RESOURCES,0),
 'only_three_country0_fields_changed':omit(bcs['0'],['tech_status','government','variables'])==omit(acs['0'],['tech_status','government','variables']),
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(v==acs[k] for k,v in bcs.items() if k!='0'),
 'exact21_fleets_only_add_cloaking_dirty_flag':set(fb)==set(fa) and set(changed_fleets)==set(fleets) and all(omit(fb[k],['properties'])==omit(fa[k],['properties']) and omit(q.block(fb[k],'properties'),['dirty_cloaking_strength'])==omit(q.block(fa[k],'properties'),['dirty_cloaking_strength']) and 'dirty_cloaking_strength' not in q.scalars(q.block(fb[k],'properties')) and q.scalars(q.block(fa[k],'properties'))['dirty_cloaking_strength']=='yes' for k in fleets),
 'starbase0_only_add_update2048':omit(br['starbase_mgr'],['starbases'])==omit(ar['starbase_mgr'],['starbases']) and set(sbo)==set(sao) and all(sbo[k]==sao[k] for k in sbo if k!='0') and omit(sbo['0'],['update_flag'])==omit(sao['0'],['update_flag']) and 'update_flag' not in q.scalars(sbo['0']) and q.scalars(sao['0'])['update_flag']==2048,
 'all_other_top_level_raw_held':[(k,v,o) for k,v,o in bf if k not in ['country','fleet','starbase_mgr','random_count']]==[(k,v,o) for k,v,o in af if k not in ['country','fleet','starbase_mgr','random_count']],
 'this_pair_random_counter_exact_plus3':[(k,q.unquote(v),o) for k,v,o in bf if k=='random_count']==[('random_count',6770866,False)] and [(k,q.unquote(v),o) for k,v,o in af if k=='random_count']==[('random_count',6770869,False)],
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
for k in ['effective_stockpile','research_queues','completed_technologies','variables','flags','traditions','ascension_perks','budget_categories','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
p={'status':'PASS_NATIVE_TERRAVORE_MOM_LAUNCH_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_sources':[{'path':str(x),'sha256':h.sha256(x)} for x in paths],'actual_UI_cost':2600,'native_fraction':'0.25','actual_Theory_progress':650,'changed_fleets':changed_fleets,'scope':'Same-day mature native agenda launch only; Theory is not completed, no research wait, Shroud, reload or full civic completion claim. Exact observed cache flags and RNG pair only.'}
out=run/(after+'-mom-launch-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original launch FAIL retained; no replay or calendar'
