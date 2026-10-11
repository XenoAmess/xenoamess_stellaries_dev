"""Exact paused native Supremacy adoption payment and unchanged physical state."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D,ROUND_CEILING
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');sys.path[:0]=['eat_everything_origin/tools','_runtime/heart-of-devouring'];sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,meta=h.load_run()
assert meta['version']=='0.2.0' and meta['language']=='l_simp_chinese'
dest=run/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
load=lambda n:json.loads((run/n).read_text('utf-8'))
def read(st):
 a=load(st+'.audit.json')
 with zipfile.ZipFile(run/(st+'.sav')) as z:f=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 return a,f,{k:v for k,v,o in f if o}
def omit(raw,keys):return [(k,v,o) for k,v,o in q.fields(raw) if k not in keys]
def objects(raw):return {k:v for k,v,o in q.fields(raw) if o}
before='terravore-second-battle-critical3-step1';after='terravore-supremacy-adopt-paid'
b,bf,br=read(before);a,af,ar=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bcr,acr=[q.block(t['country'],'0') for t in [br,ar]]
prior=load(before+'-war1-battle-v53-proof.json');prior_ex=load(before+'-battle-v53-execution.json')
cost=D(str(bc['effective_stockpile']['unity']))-D(str(ac['effective_stockpile']['unity']))
source=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/traditions/00_supremacy.txt')
checks={
 'prior85_PASS_actual0_same_original_capture_SHA':len(prior['checks'])==85 and all(v is True for v in prior['checks'].values()) and prior['status'].startswith('PASS_') and prior_ex['returncode']==0 and prior_ex['helper_sha256']==h.sha256(run/'priority_terravore_war1_battle_observer_v53.py')=='4d1bfd03965c3dbd25e9d46469c0ba81cc29cadbf823d44a4104eb2a2579341f' and prior['after_sha256']==b['save_sha256'],
 'same_paused_date_and_both_exact_native_SHA':b['date']==a['date']=='2271.08.11' and b['save_sha256']==h.sha256(run/(before+'.sav'))=='3c809d393532e3bf4342db343502acf613dfecc698e8f29fe8677694bf284dbe' and a['save_sha256']==h.sha256(run/(after+'.sav'))=='ff8dfe7781f94b767cd9eda9ab49e2abe16a3e6b6d30c42dfb40725492aec015',
 'native_full_sources_and_unchanged_production_package':h.sha256(source)==h.sha256(run/'native-postcapture-supremacy-00_supremacy.txt')=='e27f8d40e752a0a03ad0883031812b7c5c5384c12e0c2c918290006667e27ee6' and h.sha256(run/'native-postcapture-supremacy-02_gestalt_civics.txt')=='5678e1d1fa16682662d3ac4ef9bef54c37d5e62e388b7f3915732b2c779b7a82' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7',
 'original_prequote_and_confirmation_images_bound':all(load(st+'.ocr.json')['image_sha256']==h.sha256(run/(st+'.jpg'))==sha for st,sha in [('terravore-postcapture-supremacy-quote-visible','d761d0ee2a5fca21337eabca35fe6dafac1083f4628b4e78e7d1b489a6956040'),('terravore-supremacy-confirm-visible','c5bef7f2cc617749d59dd9d198e4d106ddc480aef0ad9f5c98f74d3ea64f7eb4')]),
 'normal_quote_click_confirm_save_actual0':all(load(st+'-execution.json')['returncode']==0 for st in ['terravore-postcapture-supremacy-quote-capture','terravore-supremacy-adopt-click','terravore-supremacy-confirm-capture','terravore-supremacy-adopt-confirm',after+'-native-save']),
 'exact_decimal6466point21278_ceiling6467_remaining2772point00264':cost==D('6466.21278') and cost.to_integral_value(rounding=ROUND_CEILING)==6467 and D(str(ac['effective_stockpile']['unity']))==D('2772.00264'),
 'other_true_stocks_and_all_research_banks_held':{k:v for k,v in bc['effective_stockpile'].items() if k!='unity'}=={k:v for k,v in ac['effective_stockpile'].items() if k!='unity'} and bc['research_stockpile']==ac['research_stockpile'],
 'one_original_adoption_and_category_appended':ac['traditions']==bc['traditions']+['tr_supremacy_adopt'] and [t for t,beg,end in q.tokens(q.block(acr,'tradition_categories'))]==[t for t,beg,end in q.tokens(q.block(bcr,'tradition_categories'))]+['"tradition_supremacy"'] and q.scalars(acr)['last_picked_tradition']=='tr_supremacy_adopt',
 'EEP_PSI_AP_tech_government_owned_colonies_held':all(bc[k]==ac[k] for k in ['variables','flags','ascension_perks','tech_status','government','owned_colonies']) and bc['owned_colonies']==[0,37],
 'all_population_jobs_planets_colonies_districts_deposits_species_situations_held':all(b[k]==a[k] for k in ['pop_groups','pop_jobs','planets','colonies','districts','deposits','species','event_targets','situations']),
 'all_physical_ships_armies_war_construction_zones_buildings_raw_held':all(br[k]==ar[k] for k in ['ships','army','war','construction','zones','buildings']),
 'no_pending_country0_events':not [v for k,v,o in af if k=='player_event' and o and q.scalars(v).get('country')==0],
 'full_error2814_bytes_SHA_held':(run/(before+'-error-after.log')).read_bytes()==(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes() and h.sha256(run/(after+'-error-after.log'))=='df43a78778ff981c9add0382adb3fd127128adbc6006d6bfd7db6a194c6056eb'
}
bfl,afl=[objects(t['fleet']) for t in [br,ar]]
changed=[k for k in bfl if bfl[k]!=afl.get(k)]
expected=['0','1','2','136','137','138','139','140','161','166','167','172','178','183','33555013','33555034','67109603','788','804','83886903','33555259','100664127','16778062','849']
owned=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(bcr,'fleets_manager'),'owned_fleets'))))
checks['exact24_owned_fleet_only_one_dirty_cloaking_flag_no_physical_order_change']=(set(bfl)==set(afl) and set(changed)==set(expected) and all(int(k) in owned and omit(bfl[k],{'properties'})==omit(afl[k],{'properties'}) and omit(q.block(bfl[k],'properties'),{'dirty_cloaking_strength'})==omit(q.block(afl[k],'properties'),{'dirty_cloaking_strength'}) and [row for row in q.fields(q.block(afl[k],'properties')) if row[0]=='dirty_cloaking_strength']==[('dirty_cloaking_strength','yes',False)] and 'dirty_cloaking_strength' not in q.scalars(q.block(bfl[k],'properties')) for k in changed))
bs,ass=[q.block(q.block(t['starbase_mgr'],'starbases'),'0') for t in [br,ar]]
checks['only_base0_update_flag2048_added_other_bases_held']=omit(bs,{'update_flag'})==omit(ass,{'update_flag'}) and 'update_flag' not in q.scalars(bs) and q.scalars(ass).get('update_flag')==2048 and br['starbase_mgr'].replace(bs,ass,1)==ar['starbase_mgr']
checks['country_only_tradition_fields_modules_other_countries_held']=omit(bcr,{'tradition_categories','traditions','modules','last_picked_tradition'})==omit(acr,{'tradition_categories','traditions','modules','last_picked_tradition'}) and br['country'].replace(bcr,acr,1)==ar['country']
bm,am=[q.block(c,'modules') for c in [bcr,acr]];be,ae=[q.block(m,'standard_economy_module') for m in [bm,am]]
resources=q.scalars(q.block(ae,'resources'))
checks['only_economy_resources_true_bank_flush_zero_omission_other_modules_held']=omit(bm,{'standard_economy_module'})==omit(am,{'standard_economy_module'}) and omit(be,{'resources'})==omit(ae,{'resources'}) and all(D(str(resources.get(k,0)))==D(str(ac['effective_stockpile'].get(k,0))) for k in set(resources)|set(ac['effective_stockpile']))
bmsg,amsg=[[v for k,v,o in f if k=='message' and o] for f in [bf,af]]
checks['original_report238_and_all_messages_held_only_native_agenda239_added']=amsg[:-1]==bmsg and len(amsg)==len(bmsg)+1 and q.scalars(amsg[-1])=={'type':'COUNCIL_AGENDA_AVAILABLE','localization':'MESSAGE_COUNCIL_AGENDA_AVAILABLE_UNLOCKED_DESC','receiver':0,'end':'2271.11.11','date':'2271.08.11','notification':239,'message_type':'council_agenda_ready'}
allow={'country','fleet','starbase_mgr','message','random_count','last_notification_id'}
checks['all_other_ordered_top_fields_held_exact_random1_notification1']=[row for row in bf if row[0] not in allow]==[row for row in af if row[0] not in allow] and int(next(v for k,v,o in af if k=='random_count'))==int(next(v for k,v,o in bf if k=='random_count'))+1 and int(next(v for k,v,o in af if k=='last_notification_id'))==int(next(v for k,v,o in bf if k=='last_notification_id'))+1
passed=all(checks.values())
proof={'status':'PASS_NATIVE_TERRAVORE_SUPREMACY_ADOPT_PAYMENT_COMPONENT' if passed else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'date':a['date'],'actual_unity_cost':str(cost),'actual_unity_remaining':ac['effective_stockpile']['unity'],'displayed_UI_price':6467,'changed_fleet_cache_ids':changed,'calendar_ready':False,'supremacy_paid_next_one_day_ready':passed,'scope':'One normal paid native adoption, exact physical state held and native caches flushed. No final displayed capacity or maintenance-cycle acceptance.'}
for k in ['cumulative_original_lost','cumulative_paid_lost','all_observed_paid_ship_ids','actual_pending_destroyed_ship_ids','actual_naval_death_cache_credit','actual_alive_military_ship_ids']:proof[k]=prior[k]
out=run/(after+'-supremacy-payment-proof.json');assert not out.exists();h.write_json(out,proof)
print(json.dumps({'status':proof['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'cost':str(cost)}),flush=True);assert passed,'Original payment failure retained; no repeated purchase'
