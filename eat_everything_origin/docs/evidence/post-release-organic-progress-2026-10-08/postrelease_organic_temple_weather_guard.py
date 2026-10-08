import json,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,date,progress,weather_days,source_progress,shroud_delta=sys.argv[1:];done=progress=='done';source_progress=int(source_progress)
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261008T103147Z');dest=run/Path(__file__).name
if not dest.exists():shutil.copyfile(__file__,dest)
assert dest.read_bytes()==Path(__file__).read_bytes()
def state(stem):
    a=json.loads((run/(stem+'.audit.json')).read_text(encoding='utf-8'))
    with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
    root=list(q.fields(t));return a,{k:v for k,v,o in root if o},[q.scalars(v) for k,v,o in root if k=='player_event' and o and q.scalars(v).get('country')==0]
def queue(root):
    c=root['construction'];sq=q.block(q.block(q.block(c,'queue_mgr'),'queues'),'0');it=q.block(q.block(c,'item_mgr'),'items');ids=q.ids(q.block(sq,'items'));return ids,{str(i):q.block(it,str(i)) for i in ids}
def anonymous(text):
    rows=[];depth=0;start=None
    for token,l,r in q.tokens(text):
        if token=='{':
            if depth==0:start=r
            depth+=1
        elif token=='}':
            assert depth>0;depth-=1
            if depth==0:rows.append(q.scalars(text[start:l]))
        elif depth==0:raise ValueError('Expected anonymous native modifier object')
    assert depth==0;return rows
b,br,bp=state(before);a,ar,ap=state(after);bc,ac=b['countries']['0'],a['countries']['0'];bid,bi=queue(br);aid,ai=queue(ar);source=a['planets']['711'];active=[(k,v) for k,v in a['situations'].items() if v.get('type')=='situation_eep_devouring' and v.get('killed')!='yes'];weather=[v for v in anonymous(q.block(a['planets']['7']['modifiers'],'items')) if v.get('modifier')=='electric_storm_aftermath_modifier_severity_3'];jobs={v['type']:v for v in a['pop_jobs'].values() if v['planet']==0}
checks={'actual_date':a['date']==date,'no_new_errors':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes(),'no_pending_native_events':not ap,'all_EEP_variables_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],'AP_traditions_government_owned_colonies_held':all(bc[k]==ac[k] for k in ['ascension_perks','traditions','government','owned_colonies']),'latent_family_definitions_held':all(b['species'][k]==a['species'][k] for k in ['102','103']),'mother_unique_core_owned_and_D12':sum('eep_core' in v['flags'] for v in a['planets'].values())==1 and a['planets']['7']['owner']==a['planets']['7']['controller']==0 and a['planets']['7']['variables']['eep_capacity_value']==12,'native_same_stage2_shroud_exact_delta':a['situations']['33554438']['stage']==b['situations']['33554438']['stage']==1 and D(str(a['situations']['33554438']['progress']))-D(str(b['situations']['33554438']['progress']))==D(shroud_delta),'weather_expired_or_exact_days':not weather if weather_days=='none' else len(weather)==1 and weather[0]['days']==int(weather_days),'source_Q22_T53_seed2516_frozen':source['variables']['eep_q']==22 and source['variables']['eep_months']==53 and source['variables']['eep_seed_existing']==2516,'source_owned_active_and_alive':source['owner']==source['controller']==0 and 'eep_active' in source['flags'] and a['colonies']['29']['actual_pop_sum']>0,'exact_source_situation_progress':len(active)==1 and active[0][0]=='50331651' and active[0][1]['target']['id']==711 and active[0][1]['progress']==source_progress,'raw_default_zone_held':q.block(ar['zones'],'0')==q.block(br['zones'],'0'),'all_eight_original_mother_buildings_raw_held':all(q.block(ar['buildings'],str(i))==q.block(br['buildings'],str(i))!='' for i in [0,280,3,16777262,50331657,248,2,237]),'native_telepath200_miner1000_farmer1800_active':all(jobs[k]['workforce']==jobs[k]['max_workforce']==v for k,v in [('telepath',200),('miner',1000),('farmer',1800)]),'native_all_mother_district_levels_held':all(a['districts'][k]['level']==b['districts'][k]['level'] for k in ['0','1','2','3']),'native_priest_expected':jobs['bureaucrat']['max_workforce']==jobs['bureaucrat']['workforce']==(1240 if done else 1040),'all_primary_actual_stocks_positive':all(ac['effective_stockpile'][k]>0 for k in ['energy','minerals','food','consumer_goods','alloys','unity']),'housing_amenities_positive':a['colonies']['0']['free_housing']>0 and a['colonies']['0']['free_amenities']>0}
newbuilding=None
if done:
    bz,az=q.block(br['zones'],'1'),q.block(ar['zones'],'1');old_ids=q.ids(q.block(bz,'buildings'));new_ids=q.ids(q.block(az,'buildings'));added=[v for v in new_ids if v not in old_ids];newbuilding=added[0] if len(added)==1 else None
    checks.update(native_only_temple_order_removed=bid==[218103840] and aid==[],native_archive_exact_temple_added=new_ids==old_ids+added and len(added)==1 and q.scalars(q.block(ar['buildings'],str(newbuilding))).get('type')=='building_temple')
else:
    old=q.scalars(bi['218103840'])['progress'];expected=bi['218103840'].replace('progress='+str(old)+'\n','progress='+str(progress)+'\n',1)
    checks.update(native_only_exact_temple_progress_changed=bid==aid==[218103840] and ai['218103840']==expected,native_raw_archive_zone_held=q.block(ar['zones'],'1')==q.block(br['zones'],'1'))
period=ac['budget_categories']['current_month'];net={k:str(sum((D(str(v.get(k,0))) for v in period['balance'].values()),D(0))) for k in ['energy','minerals','food','consumer_goods','alloys','unity']}
p={'status':'PASS_NATIVE_TEMPLE_WEATHER_CHECKPOINT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'native_pending':ap,'native_queue_before':bid,'native_queue_after':aid,'native_temple_raw':ai.get('218103840'),'native_added_temple_id':newbuilding,'native_storm_modifier':weather,'actual_primary_net':net,'actual_stocks':ac['effective_stockpile'],'mother_actual_pop':a['colonies']['0']['actual_pop_sum'],'source_actual_pop':a['colonies']['29']['actual_pop_sum'],'scope':'Existing paid serial temple under real native weather, concurrent natural Q22 source. No production patch, speed/resource grant or full route claim.'}
out=run/(after+'-temple-weather-proof.json');assert not out.exists();out.write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8');print(json.dumps(p),flush=True);assert all(checks.values()),'Original temple weather checkpoint failure retained; stop next calendar'
