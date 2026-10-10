"""Read-only exact native meditate selection and observed cache changes."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:];sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime'];import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));return a,t,fs,{k:v for k,v,o in fs if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def objs(t):return {k:v for k,v,o in q.fields(t) if o}
b,bt,bf,br=read(before);a,at,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
pre=json.loads((run/(before+'-psi-corps-month-proof.json')).read_text('utf-8'));ex=json.loads((run/'terravore-native-psi-corps-month-ledger-execution.json').read_text('utf-8'))
checks={'same_actual_date':b['date']==a['date']=='2244.08.02','original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],'prior17_month_PASS_exit0':pre['status']=='PASS_TERRAVORE_PAID_ECONOMY_MONTH_COMPONENT' and len(pre['checks'])==17 and all(pre['checks'].values()) and pre['after_sha256']==b['save_sha256'] and ex['returncode']==0}
click=json.loads((run/'terravore-native-meditate-select.action.json').read_text('utf-8'));clickex=json.loads((run/'terravore-native-meditate-select-execution.json').read_text('utf-8'))
checks['normal_exact_UI_select_exit0']=click['action']=='left-click' and click['client_point']==[444,235] and clickex['returncode']==0
skip={'country','fleet','starbase_mgr','situations','random_count'}
checks['all_other_ordered_top_level_raw_held']=[x for x in bf if x[0] not in skip]==[x for x in af if x[0] not in skip]
checks['same_ordered_top_level_field_names']=[(k,o) for k,v,o in bf]==[(k,o) for k,v,o in af]
checks['random_count_exact_observed_one']=q.scalars(bt)['random_count']==72047020 and q.scalars(at)['random_count']==72047021
bs,ass=[q.block(rt['situations'],'situations') for rt in [br,ar]];bsi,asi=[q.block(s,'16777221') for s in [bs,ass]]
checks['all_other_situations_raw_held']=omit(bs,{'16777221'})==omit(ass,{'16777221'}) and omit(br['situations'],{'situations'})==omit(ar['situations'],{'situations'})
checks['only_exact_breach_approach_and_flag']=omit(bsi,{'approach','flags'})==omit(asi,{'approach','flags'}) and q.scalars(bsi)['approach']=='approach_situation_breach_shroud_nothing' and q.scalars(asi)['approach']=='approach_situation_breach_shroud_meditate' and q.scalars(q.block(bsi,'flags'))=={'breach_shroud_stage_1_started':63173784} and q.scalars(q.block(asi,'flags'))=={'breach_shroud_stage_1_started':63173784,'beneficial_approach':63193224}
bcr,acr=[q.block(rt['country'],'0') for rt in [br,ar]];bm,am=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(v,'standard_economy_module') for v in [bm,am]];bres,ares=[q.scalars(q.block(v,'resources')) for v in [be,ae]]
checks['all_country_raw_except_exact_economic_resources_held']=omit(br['country'],{'0'})==omit(ar['country'],{'0'}) and omit(bcr,{'modules'})==omit(acr,{'modules'}) and omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'})
checks['only_exact_research_mirror_refresh']=bres.get('physics_research')==43.4368 and bres.get('engineering_research')==46.5368 and bres.get('society_research')==632.32212 and ares=={**{k:v for k,v in bres.items() if k not in ['physics_research','engineering_research','society_research']},'society_research':643.86552} and ac['research_stockpile']==bc['research_stockpile']=={'physics_research':0,'society_research':643.86552,'engineering_research':0}
bss,asss=[q.block(rt['starbase_mgr'],'starbases') for rt in [br,ar]];bs0,as0=[q.block(v,'0') for v in [bss,asss]]
checks['only_starbase0_update_flag2048']=omit(br['starbase_mgr'],{'starbases'})==omit(ar['starbase_mgr'],{'starbases'}) and omit(bss,{'0'})==omit(asss,{'0'}) and omit(bs0,{'update_flag'})==omit(as0,{'update_flag'}) and 'update_flag' not in q.scalars(bs0) and q.scalars(as0).get('update_flag')==2048
bfl,afl=objs(br['fleet']),objs(ar['fleet']);changed=[i for i,v in bfl.items() if afl.get(i)!=v]
expected=['0','1','2','136','137','138','139','140','161','166','167','171','172','178','183','196','198','477','490','16777797','602']
checks['exact21_fleet_dirty_properties_only']=set(bfl)==set(afl) and set(changed)==set(expected) and all(omit(bfl[i],{'properties'})==omit(afl[i],{'properties'}) and omit(q.block(bfl[i],'properties'),{'dirty_cloaking_strength'})==omit(q.block(afl[i],'properties'),{'dirty_cloaking_strength'}) and 'dirty_cloaking_strength' not in q.scalars(q.block(bfl[i],'properties')) and q.scalars(q.block(afl[i],'properties')).get('dirty_cloaking_strength')=='yes' for i in changed) and [(k,v,o) for k,v,o in q.fields(br['fleet']) if not o]==[(k,v,o) for k,v,o in q.fields(ar['fleet']) if not o]
for k in ['effective_stockpile','research_stockpile','tech_status','budget_categories','variables','flags','government','traditions','ascension_perks','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','species','event_targets']:checks[k+'_held']=b[k]==a[k]
checks['all_ships_construction_zones_buildings_raw_held']=all(br[k]==ar[k] for k in ['ships','construction','zones','buildings'])
checks['no_country0_pending']=not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0]
checks['unfiltered_errors_held']=(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()
source=h.GAME_EXE.parent/'common/situations/13_shroud_situations.txt';sit=q.block(source.read_text('utf-8-sig'),'situation_breach_shroud');approaches=[v for k,v,o in q.fields(sit) if k=='approach' and o and q.scalars(v).get('name')=='approach_situation_breach_shroud_meditate'];assert len(approaches)==1
sel=q.block(approaches[0],'on_select');checks['native_selected_approach_has_only_flag_and_tooltips']=set(k for k,v,o in q.fields(sel))=={'set_situation_flag','custom_tooltip'} and q.scalars(sel)['set_situation_flag']=='beneficial_approach' and q.scalars(q.block(approaches[0],'modifier'))=={'country_unity_produces_mult':-0.25}
p={'status':'PASS_NATIVE_TERRAVORE_MEDITATE_SELECTION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'actual_breach':a['situations']['16777221'],'actual_true_bank':ac['research_stockpile'],'exact_dirty_fleets':changed,'native_source':{'path':str(source),'sha256':h.sha256(source)},'scope':'One same-date native meditate selection, exact observed cache changes only. Future actual5/month and reduced unity need calendar evidence; no full route claim.'}
out=run/(after+'-meditate-selection-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original meditate selection FAIL retained'
