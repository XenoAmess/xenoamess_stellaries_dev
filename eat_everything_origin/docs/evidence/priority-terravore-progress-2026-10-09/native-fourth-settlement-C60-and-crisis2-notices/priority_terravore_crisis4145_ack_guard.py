"""Exact native crisis282 ACK, project8 and auto-design refresh conservation."""
import json,logging,sys,zipfile,re
from pathlib import Path
sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r
import audit_save as q
from native_selected_history import selected_history
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run();load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before,after='terravore-native-crisis4145-event-date','terravore-native-crisis4145-acked'
def read(st):
    au=load(st+'.audit.json')
    with zipfile.ZipFile(run/(st+'.sav')) as z:raw=z.read('gamestate').decode('utf-8-sig')
    fs=list(q.fields(raw));roots={k:v for k,v,o in fs if o};sc=q.scalars('\n'.join(k+'='+v for k,v,o in fs if not o))
    return au,raw,fs,roots,sc
b,bt,bfs,br,bs=read(before);a,at,afs,ar,ass=read(after)
vals=lambda fs,key:[v for k,v,o in fs if k==key]
omit=lambda raw,keys:[(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
lex=lambda raw:[v for v,x,y in q.tokens(raw)]
bc,ac=[q.block(x['country'],'0') for x in [br,ar]];be,ae=[q.block(x,'events') for x in [bc,ac]]
bp,ap=[vals(fs,'player_event') for fs in [bfs,afs]];bm,am=[vals(fs,'message') for fs in [bfs,afs]]
target=[v for v in bp if q.scalars(v).get('country')==0 and q.scalars(v).get('id')==282];removed=[v for v in bm if q.scalars(v).get('event')==282 and q.scalars(v).get('receiver')==0]
bproj,aproj=[vals(list(q.fields(x)),'special_project') for x in [be,ae]];new=[v for v in aproj if v not in bproj];project=new[0] if len(new)==1 else ''
pre_name=before+'-native-crisis4145-arrival-proof.json';pre,pe=load(pre_name),load(before+'-native-crisis4145-arrival-guard-execution.json')
inv_name=after+'-native-auto-design-refresh-investigation.json';inv=load(inv_name)
objects=lambda raw:{k:(v,o) for k,v,o in q.fields(raw)}
entities={root:[objects(x[root]) for x in [br,ar]] for root in ['ships','fleet','ship_design']}
changed={root:{k:{'before':bb.get(k),'after':aa.get(k)} for k in set(bb)|set(aa) if bb.get(k)!=aa.get(k)} for root,(bb,aa) in entities.items()}
ship_remap={'50332983':(58,8),'50333076':(58,8),'50333335':(59,9)}
fleet_remap={'875','16778097','16778103'}
new_designs={'184550902':'crisis_corvette','201328177':'military_station_medium','218105357':'military_station_large','251659768':'starbase_starport','268436983':'starbase_starhold'}
old_none={'167773686','184550961','201328141','234882552','251659767'}
source=h.GAME_EXE.parent/'events/nemesis_crisis_events.txt';proj_source=h.GAME_EXE.parent/'common/special_projects/00_projects_nemesis.txt'
event=[v for k,v,o in q.fields(source.read_text('utf-8-sig')) if o and q.scalars(v).get('id')=='crisis.4145'][0]
pdef=[v for k,v,o in q.fields(proj_source.read_text('utf-8-sig')) if o and q.scalars(v).get('key')=='CRISIS_SPECIAL_PROJECT_PSIONIC_2'][0]
checks={
 'arrival9_PASS_actual0_fixed_source_and_before_SAV':len(pre['checks'])==9 and all(v is True for v in pre['checks'].values()) and pe['returncode']==0 and pe['helper_sha256']==h.sha256(Path(pe['command'][1]))=='985bd358dcc95c9c691ff3629f8f838b2e204fba848b1dcd1c2affb79888c567' and pre['after_sha256']==b['save_sha256'],
 'same_date_original_two_SAVs':b['date']==a['date']=='2278.10.05' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='073f662405184c78ce128a6f4d891859eaca16f2f059f1eaba417c118f94ba63' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='2e272b75fc4b9f688094ff01e124e2affe00416736639ebc6526492182c6a40f',
 'exact_pending282_message_removed_human1_option0_once':len(target)==1 and q.scalars(target[0]).get('event')=='crisis.4145' and ap==[v for v in bp if v not in target] and len(removed)==1 and am==[v for v in bm if v not in removed] and selected_history(at)==selected_history(bt)+[{'player_event':282,'human':1,'option':0}],
 'only_project8_unstarted_PSIONIC2_added_allocator8_to9':aproj==bproj+new and len(new)==1 and q.scalars(project)=={'id':8,'special_project':'CRISIS_SPECIAL_PROJECT_PSIONIC_2','ai_research_date':'2278.10.11'} and q.scalars(q.block(project,'coordinate'))=={'type':2,'id':7} and q.scalars(q.block(project,'carrier'))=={'type':'planet','reference':7} and q.scalars(be)['next_special_project_id']==8 and q.scalars(ae)['next_special_project_id']==9 and omit(be,{'special_project','next_special_project_id'})==omit(ae,{'special_project','next_special_project_id'}),
 'project_scope_preserves_event_scope_with_native_root_prev':lex('\n'.join(k+'='+('{' + v + '}' if o else v) for k,v,o in q.fields(q.block(project,'scope')) if k not in {'root','prev'}))==lex(q.block(target[0],'scope')) and all(lex(q.block(q.block(project,'scope'),key))==lex(q.block(target[0],'scope')) for key in ['root','prev']),
 'native_option0_psionic_priority_project6000_physics_and_auto_refresh':q.scalars(q.block(event,'option')).get('name')=='crisis.4145.a' and q.scalars(q.block(q.block(q.block(q.block(event,'option'),'root'),'if'),'limit'))=={'is_psionic':'yes'} and q.scalars(q.block(q.block(q.block(q.block(event,'option'),'root'),'if'),'enable_special_project'))=={'name':'CRISIS_SPECIAL_PROJECT_PSIONIC_2','owner':'ROOT'} and 'is_psionic = yes' in event and 'refresh_auto_generated_ship_designs = yes' in q.block(event,'after') and q.scalars(pdef).get('cost')==6000 and q.scalars(pdef).get('tech_department')=='physics_technology',
 'original_refresh_INV_exact_raw_changed_entities_bound':h.sha256(run/inv_name)=='7f901ef47c9edcc0edac107663ce6aa0fa15dce3a44e9728b7ec95502b2f6667' and json.loads(json.dumps(changed))==inv['changed_global_entities_raw'],
 'only_three_captured_stations_same_components_no_stats_or_ship_birth_changes':set(changed['ships'])==set(ship_remap) and all(omit(entities['ships'][0][sid][0],{'ship_design_implementation','is_original_design'})==omit(entities['ships'][1][sid][0],{'ship_design_implementation','is_original_design'}) and q.scalars(q.block(entities['ships'][0][sid][0],'ship_design_implementation'))=={'design':old,'upgrade':4294967295,'growth_stage':0} and q.scalars(q.block(entities['ships'][1][sid][0],'ship_design_implementation'))=={'design':newid,'upgrade':4294967295,'growth_stage':0} and q.scalars(entities['ships'][1][sid][0]).get('is_original_design')=='no' and q.block(br['ship_design'],str(old)) and lex(q.block(q.block(br['ship_design'],str(old)),'growth_stages'))==lex(q.block(q.block(ar['ship_design'],str(newid)),'growth_stages')) for sid,(old,newid) in ship_remap.items()),
 'only_three_corresponding_fleets_add_dirty_cloaking_strength':set(changed['fleet'])==fleet_remap and all(omit(entities['fleet'][0][fid][0],{'properties'})==omit(entities['fleet'][1][fid][0],{'properties'}) and q.scalars(q.block(entities['fleet'][1][fid][0],'properties'))=={**q.scalars(q.block(entities['fleet'][0][fid][0],'properties')),'dirty_cloaking_strength':'yes'} for fid in fleet_remap),
 'exact_five_new_auto_templates_and_only_five_scalar_none_retired':set(changed['ship_design'])==set(new_designs)|old_none and all(entities['ship_design'][0].get(i)==('none',False) and i not in entities['ship_design'][1] for i in old_none) and all(i not in entities['ship_design'][0] and entities['ship_design'][1][i][1] and re.findall(r'ship_size="([^"]+)"',entities['ship_design'][1][i][0])==[size] and q.scalars(entities['ship_design'][1][i][0]).get('auto_gen_design')=='yes' for i,size in new_designs.items()),
 'country0_collection_exact_old4_removed_new5_added_other_country_raw_held':q.block(bc,'ship_design_collection')==inv['before_country_collection'] and q.block(ac,'ship_design_collection')==inv['after_country_collection'] and set(q.ids(q.block(q.block(bc,'ship_design_collection'),'ship_design')))-set(q.ids(q.block(q.block(ac,'ship_design_collection'),'ship_design')))=={251660010,369100552,385877735,402654950} and set(q.ids(q.block(q.block(ac,'ship_design_collection'),'ship_design')))-set(q.ids(q.block(q.block(bc,'ship_design_collection'),'ship_design')))==set(map(int,new_designs)) and omit(bc,{'events','ship_design_collection'})==omit(ac,{'events','ship_design_collection'}) and omit(br['country'],{'0'})==omit(ar['country'],{'0'}),
 'native_random_plus233_and_last_created_design_exact':bs['random_count']==331528808 and ass['random_count']==331529041 and bs['last_created_design']==285214259 and ass['last_created_design']==184550902,
 'all_other_ordered_world_top_raw_held':[(k,v,o) for k,v,o in bfs if k not in {'country','player_event','message','open_player_event_selection_history','ship_design','ships','fleet','random_count','last_created_design'}]==[(k,v,o) for k,v,o in afs if k not in {'country','player_event','message','open_player_event_selection_history','ship_design','ships','fleet','random_count','last_created_design'}],
 'all_EEP_stock_banks_POP_jobs_government_AP_research_held':all(b['countries']['0'][k]==a['countries']['0'][k] for k in ['effective_stockpile','research_stockpile','variables','flags','government','traditions','ascension_perks','tech_status']) and all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','situations','species','event_targets']),
 'actual_normal_click_save_and_original_error41_020_simp_chinese':all(load(after+s+'-execution.json')['returncode']==0 for s in ['-select','-native-save']) and load(after+'-select.action.json')['client_point']==[510,514] and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb' and meta['version']=='0.2.0' and meta['language']=='l_simp_chinese' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
}
passed=all(v is True for v in checks.values());out=run/(after+'-native-crisis4145-ack-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_CRISIS4145_ACK_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'paid_births':pre['paid_births'],'actual_project_raw':project,'refresh_INV_sha256':h.sha256(run/inv_name),'native_sources':[{'path':str(v),'sha256':h.sha256(v)} for v in [source,proj_source]],'boundaries':['queen_monthly_notice'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Normal native ACK and exact auto-template/captured-station mapping only; project unstarted. No mineral ship produced or paid.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
