"""Same-date single native late-route preview and cancellation; read-only guard."""
import json,logging,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
before='terravore-native-market-purchase02-22851002';after='terravore-mineral-forward-canceled-22851002'
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
def checked(st):
 x=load(st+'-execution.json');return x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))
b=read_state(run,before);a=read_state(run,after);ba=b['audit'];aa=a['audit'];p=load(before+'-market-purchase-v3-proof.json');bf=b['fleets']['917'];af=a['fleets']['917'];bm=q.block(bf,'movement_manager');am=q.block(af,'movement_manager')
bs=q.block(b['roots']['starbase_mgr'],'starbases');ass=q.block(a['roots']['starbase_mgr'],'starbases');bb=q.block(bs,'160');ab=q.block(ass,'160');image='terravore-mineral-forward-order917-eta';ocr=load(image+'.ocr.json')
checks={
 'prior16_marketPASS_actual0_source_originalSAV':len(p['checks'])==16 and p['status']=='PASS_NATIVE_MARKET_PURCHASE_V3' and all(v is True for v in p['checks'].values()) and checked(before+'-market-purchase-v3-guard') and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')),
 'same_paused_October2_normal_save_actual0_original_pair':ba['date']==aa['date']=='2285.10.02' and checked(after+'-native-save') and aa['save_sha256']==h.sha256(run/(after+'.sav')),
 'all_country0_raw_cash_research_EEP_flags_held':a['country']==b['country'],
 'all_audit_business_population_buildings_jobs_assets_held':{k:v for k,v in ba.items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']}=={k:v for k,v in aa.items() if k not in ['save','save_sha256','gamestate_sha256','gamestate_bytes']},
 'all77_owned_ships_full_raw_held':len(b['ships'])==77 and b['ships']==a['ships'],
 'only917_of35_owned_fleets_changes_three_exact_fields':len(b['fleets'])==len(a['fleets'])==35 and set(b['fleets'])==set(a['fleets']) and {k for k in b['fleets'] if b['fleets'][k]!=a['fleets'][k]}=={'917'} and omit(bf,{'movement_manager','order_id','properties'})==omit(af,{'movement_manager','order_id','properties'}),
 'native_order_id2_to3_only_dirty_cloaking_cache_added':q.scalars(bf)['order_id']==2 and q.scalars(af)['order_id']==3 and q.scalars(q.block(af,'properties'))==dict(q.scalars(q.block(bf,'properties')),dirty_cloaking_strength='yes'),
 'canceled_no_active_order_original188_position_target_jump_held':not q.block(af,'current_order') and omit(bm,{'path','orbit','time_since_last_path_update'})==omit(am,{'path','orbit','time_since_last_path_update'}) and q.scalars(am)=={'state':'move_idle'} and q.scalars(q.block(am,'coordinate'))['origin']==188 and q.scalars(q.block(am,'target_coordinate'))['origin']==4294967295,
 'canceled_empty_orbit_path_only_obsolete_ETA_no_active_arrival':list(q.fields(q.block(am,'path')))==[('date','"2286.07.12"',False)] and not list(q.fields(q.block(am,'orbit'))),
 'only_station160_slot0_cleared_other_slot_old_fleet_held':q.scalars(q.block(bb,'orbitals'))=={'0':917,'1':50332250} and q.scalars(q.block(ab,'orbitals'))=={'0':4294967295,'1':50332250} and omit(bb,{'orbitals'})==omit(ab,{'orbitals'}) and omit(bs,{'160'})==omit(ass,{'160'}) and omit(b['roots']['starbase_mgr'],{'starbases'})==omit(a['roots']['starbase_mgr'],{'starbases'}),
 'all_other_roots_and_all_other_fleets_held':set(a['roots'])==set(b['roots']) and all(a['roots'][k]==v for k,v in b['roots'].items() if k not in ['fleet','starbase_mgr']) and omit(a['roots']['fleet'],{'917'})==omit(b['roots']['fleet'],{'917'}),
 'native_select_rightclick_cancel_H_actual0_bound':all(checked(s) for s in ['terravore-mineral-forward-select917','terravore-mineral-forward-order917-nishpan','terravore-mineral-forward917-cancel-late']) and load('terravore-mineral-forward-order917-nishpan.action.json')['client_point']==[635,394] and load('terravore-mineral-forward917-cancel-late.action.json')['scan_code']==35,
 'actual_late_UI_ETA_original_F12_source_actual0':checked(image) and ocr['image_sha256']==h.sha256(run/(image+'.jpg'))=='f4c5f13da6b2608203dfaaa5da89b412632dbff562bbd8b9f73786311b9d3a8b' and any('2286.07.12' in x['text'] for x in ocr['rows']),
 'messages_held_no_pending':a['messages']==b['messages'] and not a['pending'] and not b['pending'],
 'CN41_unfiltered_error_original_bytes_held':m['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
passed=all(v is True for v in checks.values());out=run/(after+'-forward-cancel-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_LATE_FORWARD_CANCELED' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'boundaries':['native_main_arrival_or_science_forward_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Same-date late native ETA preview safely canceled; no forward-arrival or full-civic claim.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
