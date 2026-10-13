"""Only normal engineering automatic research setting changes on the same day."""
import json,logging,re,sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state,omit
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-border-22860401';after='terravore-engineering-off-22860401'
b,a=read_state(run,before),read_state(run,after);ba,aa=b['audit'],a['audit']
p=load(before+'-postcombat-v4-proof.json');px=load(before+'-postcombat-v4-guard-execution.json')
bt=q.block(b['country'],'tech_status');at=q.block(a['country'],'tech_status')
cx=load('terravore-engineering-auto-off-click-22860401-execution.json');sx=load(after+'-save-execution.json')
checks={
 'prior24PASS_actual0_source_originalSAV':len(p['checks'])==24 and all(v is True for v in p['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(Path(px['command'][1])) and p['after_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')),
 'same_day_CN_original_native_save_SHA':ba['date']==aa['date']=='2286.04.01' and aa['save_sha256']==h.sha256(run/(after+'.sav')) and m['language']=='l_simp_chinese',
 'normal_single_click_and_native_save_actual0_source':cx['returncode']==sx['returncode']==0 and all(x['helper_sha256']==h.sha256(Path(x['command'][1])) for x in [cx,sx]),
 'only_engineering_auto_yes_to_no_or_omitted':q.scalars(bt)['auto_researching_engineering']=='yes' and q.scalars(at).get('auto_researching_engineering','no')=='no' and omit(bt,{'auto_researching_engineering'})==omit(at,{'auto_researching_engineering'}),
 'all_other_country0_raw_held':omit(b['country'],{'tech_status'})==omit(a['country'],{'tech_status'}),
 'all_other_countries_raw_held':omit(b['roots']['country'],{'0'})==omit(a['roots']['country'],{'0'}),
 'all_other_named_world_roots_raw_held':set(b['roots'])==set(a['roots']) and all(v==a['roots'][k] for k,v in b['roots'].items() if k not in ['country','fleet']),
 'all75_original_ships_and35_fleets_raw_held':len(a['ships'])==75 and len(a['fleets'])==35 and b['ships']==a['ships'] and b['fleets']==a['fleets'],
 'all_research_queue_banks_cash_EEP_population_held':all(ba['countries']['0'][k]==aa['countries']['0'][k] for k in ['research_queues','research_stockpile','effective_stockpile','variables','owned_colonies']) and ba['colonies']==aa['colonies'],
 'messages_and_pending_held':b['messages']==a['messages'] and b['pending']==a['pending']==[],
 'production41_and_live_unfiltered_error_held':h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}

bf=q.block(b['roots']['fleet'],'922');af=q.block(a['roots']['fleet'],'922')
checks['only_foreign16777218_fleet922_ship33555439_dirty_cloaking_cache_added']=q.ids(q.block(bf,'ships'))==q.ids(q.block(af,'ships'))==[33555439] and q.scalars(q.block(bf,'properties'))=={'mobile':'yes','valid_for_combat':'yes'} and q.scalars(q.block(af,'properties'))=={'mobile':'yes','valid_for_combat':'yes','dirty_cloaking_strength':'yes'} and omit(bf,{'properties'})==omit(af,{'properties'}) and omit(b['roots']['fleet'],{'922'})==omit(a['roots']['fleet'],{'922'}) and re.search(r'\bfleet\s*=\s*922\b',q.block(q.block(q.block(a['roots']['country'],'16777218'),'fleets_manager'),'owned_fleets')) is not None
op=load(after+'-engineering-auto-off-proof.json');ox=load(after+'-guard-execution.json')
checks['original11_only_world_cacheFAIL_actual1_source_originalSAV']=len(op['checks'])==11 and [k for k,v in op['checks'].items() if v is not True]==['all_other_named_world_roots_raw_held'] and ox['returncode']==1 and ox['helper_sha256']=='274b2a1bb1cd40563fb739d32f67c99b4220a755d615afa0fd169add66615de0' and op['before_sha256']==ba['save_sha256'] and op['after_sha256']==aa['save_sha256']

passed=all(v is True for v in checks.values());out=run/(after+'-engineering-auto-off-v2-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_ENGINEERING_AUTO_OFF' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'auto_after':q.scalars(at).get('auto_researching_engineering','omitted'),'boundaries':['native_engineering_storm_550_completion_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Normal auto research setting only; current research, resources and assets unchanged.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
