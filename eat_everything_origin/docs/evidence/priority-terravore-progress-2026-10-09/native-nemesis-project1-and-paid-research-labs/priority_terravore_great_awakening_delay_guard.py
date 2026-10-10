"""Native stage2 Great Awakening exact delayed event and untouched latent species."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
before='terravore-native-stage2-ack';after='terravore-native-awakening-paid'
def read(st):
 a=json.loads((run/(st+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(st+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 return a,t
def obj(t):return {k:v for k,v,o in q.fields(t) if o}
def omit(t,ks):return [(k,v,o) for k,v,o in q.fields(t) if k not in ks]
def vals(t,k):return [v for kk,v,o in q.fields(t) if kk==k]
b,bt=read(before);a,at=read(after);bc,ac=[obj(q.block(t,'country')) for t in [bt,at]];bm,am=[q.block(c['0'],'modules') for c in [bc,ac]];be,ae=[q.block(t,'standard_event_module') for t in [bm,am]];bd,ad=[vals(t,'delayed_event') for t in [be,ae]];new=ad[len(bd):]
pre=json.loads((run/(after+'-paid-tradition-v4-proof.json')).read_text('utf-8'));source=h.GAME_EXE.parent/'common/traditions/01_psionics_shroud.txt';src=source.read_text('utf-8-sig');trad=q.block(src,'tr_psionics_shroud_great_awakening');sw=q.block(trad,'tradition_swap');hidden=q.block(q.block(sw,'on_enabled'),'hidden_effect');condition=q.block(q.block(hidden,'if'),'limit')
ber,aer=[q.block(q.block(t,'standard_economy_module'),'resources') for t in [bm,am]];resources=q.scalars(ber);resources.pop('physics_research');resources.pop('engineering_research');resources['society_research']=2659.65517;resources['unity']=14147.47413
checks={
 'bound15_paid_checks_PASS_actual_exit0':pre['status']=='PASS_NATIVE_PAID_TRADITION_COMPONENT' and len(pre['checks'])==15 and all(v is True for v in pre['checks'].values()) and json.loads((run/(after+'-guard-execution.json')).read_text('utf-8'))['returncode']==0,
 'same_date_original_SHA_pair':b['date']==a['date']=='2251.04.02' and h.sha256(run/(before+'.sav'))==b['save_sha256']==pre['before_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256']==pre['after_sha256'],
 'all_other_ordered_top_raw_held':omit(bt,{'country','random_count'})==omit(at,{'country','random_count'}),
 'actual_random_count_exact_one':q.scalars(bt)['random_count']==156552955 and q.scalars(at)['random_count']==156552956,
 'all_other_countries_raw_held':set(bc)==set(ac) and all(ac[k]==v for k,v in bc.items() if k!='0'),
 'country0_only_declared_tradition_and_modules':omit(bc['0'],{'modules','traditions','last_picked_tradition'})==omit(ac['0'],{'modules','traditions','last_picked_tradition'}) and q.scalars(ac['0'])['last_picked_tradition']=='tr_psionics_shroud_great_awakening',
 'all_other_modules_raw_held':omit(bm,{'standard_event_module','standard_economy_module'})==omit(am,{'standard_event_module','standard_economy_module'}),
 'only_one_delayed_event_append_other_event_fields_held':ad[:len(bd)]==bd and len(new)==1 and omit(be,{'delayed_event'})==omit(ae,{'delayed_event'}),
 'exact_native_enclave_event649_scope_from_country0':len(new)==1 and q.scalars(new[0])=={'event':'enclave.7000','days':649} and all(q.scalars(s).get('type')=='country' and q.scalars(s).get('id')==0 for s in [q.block(new[0],'scope'),q.block(q.block(new[0],'scope'),'from')]),
 'previous_paragon_event599_raw_held':len(bd)==1 and q.scalars(bd[0])=={'event':'paragon.999','days':599} and bd[0]==ad[0],
 'native_swap_only_stage3_conversion_delay360random720':q.scalars(sw)['name']=='tr_psionics_shroud_great_awakening_situation' and q.scalars(q.block(sw,'trigger'))=={'has_breached_shroud':'no'} and q.scalars(q.block(condition,'any_situation')).get('current_stage')=='stage_3' and q.scalars(q.block(hidden,'country_event'))=={'id':'enclave.7000','days':360,'random':720} and q.scalars(hidden).get('refresh_portraits')=='character' and 'turn_main_species_to_psionic = yes' in q.block(hidden,'if'),
 'actual_stage2_unchanged_latent_not_fullPsi':b['situations']==a['situations'] and a['situations']['16777221']['stage']==1 and a['situations']['16777221']['progress']==501.25 and b['species']==a['species'] and a['species']['66']['traits']==['trait_lithoid','trait_hive_mind','trait_pc_continental_preference','trait_latent_psionic'],
 'only_exact_economy_mirror_and_paid_unity_change':q.scalars(aer)==resources and q.scalars(ber)['physics_research']==772.7125 and q.scalars(ber)['engineering_research']==826.9625 and q.scalars(ber)['society_research']==2440.46522 and omit(q.block(bm,'standard_economy_module'),{'resources'})==omit(q.block(am,'standard_economy_module'),{'resources'}),
 'true_research_bank_and_full_tech_status_held':b['countries']['0']['tech_status']==a['countries']['0']['tech_status'] and a['countries']['0']['research_stockpile']['society_research']==2659.65517,
 'EEP_psi_reward_and_notice_still_absent':a['countries']['0']['variables']['eep_psi']==0 and 'eep_psi_notice' not in a['countries']['0']['flags'],
 'no_pending_and_no_error_increment':not [v for k,v,o in q.fields(at) if k=='player_event' and q.scalars(v).get('country')==0] and (run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),
}
p={'status':'PASS_NATIVE_STAGE2_GREAT_AWAKENING_DELAY_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'calendar_ready':True,'new_delayed_event_raw':new,'actual_decimal_unity_paid':pre['actual_decimal_unity_paid'],'native_source':{'path':str(source),'sha256':h.sha256(source)},'scope':'Actual normal Great Awakening payment in native phase2, exactly one enclave7000 delayed event, latent species remains. No full psionic or route completion claim.'}
out=run/(after+'-great-awakening-delay-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original Great Awakening delay FAIL retained'
