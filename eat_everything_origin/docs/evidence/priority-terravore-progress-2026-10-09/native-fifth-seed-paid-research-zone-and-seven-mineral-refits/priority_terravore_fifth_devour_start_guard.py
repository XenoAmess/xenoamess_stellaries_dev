"""Read-only real founder relocation and native fifth devour start."""
import collections,json,logging,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text('utf-8-sig'))
before='terravore-balthasar-conquest-day-22801103';after='terravore-balthasar-native-devour-started'
ba,aa=[load(st+'.audit.json') for st in [before,after]];bc,ac=[v['countries']['0'] for v in [ba,aa]]
roots=[]
for st in [before,after]:
 with zipfile.ZipFile(run/(st+'.sav')) as z:fs=list(q.fields(z.read('gamestate').decode('utf-8-sig')))
 rr={k:v for k,v,x in fs if x}
 rr['_messages']=[v for k,v,x in fs if x and k=='message' and q.scalars(v).get('receiver')==0]
 rr['_pending']=[v for k,v,x in fs if x and k=='player_event' and q.scalars(v).get('country')==0]
 roots.append(rr)
br,ar=roots
def owned(rr):
 c=q.block(rr['country'],'0');fs=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(c,'fleets_manager'),'owned_fleets'))))
 ships={i for fid in fs for i in q.ids(q.block(q.block(rr['fleet'],str(fid)),'ships'))}
 return fs,ships
def pops(rr,colony):
 result=collections.Counter();rows=[]
 for i in q.ids(q.block(q.block(rr['colony'],str(colony)),'pop_groups')):
  raw=q.block(rr['pop_groups'],str(i));key=q.scalars(q.block(raw,'key'));size=q.scalars(raw)['size']
  result[key['species']]+=size;rows.append({'id':i,'species':key['species'],'category':key['category'],'size':size})
 return dict(result),rows
bm,bmr=pops(br,0);am,amr=pops(ar,0);bs,bsr=pops(br,30);aps,asr=pops(ar,30)
pre=load(before+'-conquest-proof.json');px=load(before+'-conquest-guard-execution.json')
obs=load(after+'-observation.json');sx=load('terravore-balthasar-devour-start-save-execution.json');ux=load('terravore-balthasar-native-devour-select-execution.json')
p=aa['planets']['1578'];oldp=ba['planets']['1578'];sit={k:v for k,v in aa['situations'].items() if v.get('type')=='situation_eep_devouring'}
jobs=lambda au:{k:v for k,v in au['pop_jobs'].items() if v['planet']==0}
messages=lambda rr:rr['_messages']
pending=lambda rr:rr['_pending']
checks={
 'original_conquest16_PASS_actual0_exact_source_and_SAV':len(pre['checks'])==16 and all(v is True for v in pre['checks'].values()) and px['returncode']==0 and px['helper_sha256']==h.sha256(run/'priority_terravore_balthasar_conquest_guard.py')=='6f945e6e14b75d6f427e177c2aedeca761fe321ef317f91d726b8208913ea83b' and pre['after_sha256']==ba['save_sha256']=='8e10a5a711d7cca62b9342754ca4c5795a9dabc48b2947a495f5a6306fa1d8b5',
 'normal_UI_decision_and_save_actual0_bound_sources':ux['returncode']==sx['returncode']==0 and ux['helper_sha256']==h.sha256(run/'priority_native_ui_input_v3.py')=='801941d04cb3b4434483d22f3418187438142d66c9740367794ae75f2ac41a9f' and sx['helper_sha256']==h.sha256(run/'priority_native_save.py')=='19fea261969af27e547860acead4fa010e90612d8b6d2904b1b6b11ba49ee82e' and all(h.sha256(Path(v['path']))==v['sha256'] for v in obs['dependency_bindings']),
 'same_paused_date_exact_original_SAVs':ba['date']==aa['date']==obs['date']=='2280.11.03' and all(h.sha256(run/(st+'.sav'))==au['save_sha256'] for st,au in [(before,ba),(after,aa)]) and aa['save_sha256']==obs['save_sha256']=='03d0aefc831de09f6547fc5f7c1c618bdd13ff860e291390ec856e6e5ee605ee',
 'actual100_founder_transfer_no_manufacture':bm=={73:12075} and am=={73:11975} and bs=={61:27,2:366} and aps=={61:27,2:366,73:100} and sum(bm.values())+sum(bs.values())==sum(am.values())+sum(aps.values())==12468,
 'all_foreign_stays_source_purge_and_none_on_mother':all(v['species']==73 for v in amr) and all(v['category']=='purge' for v in asr if v['species']!=73),
 'mother35_capacity27_paid_levels_and_structure_held':aa['planets']['7']==ba['planets']['7'] and aa['colonies']['0']['districts']==ba['colonies']['0']['districts'] and all(aa['districts'][str(i)]==ba['districts'][str(i)] for i in aa['colonies']['0']['districts']) and sum(aa['districts'][str(i)]['level'] for i in aa['colonies']['0']['districts'])==27,
 'same_day_only_mother_job_cache_held_not_future_workforce_claim':jobs(ba)==jobs(aa) and aa['colonies']['0']['free_housing']>0 and aa['colonies']['0']['free_amenities']>0 and aa['colonies']['0']['crime']==0,
 'EEP_government_AP_traditions_crisis_no_early_rewards':all(bc[k]==ac[k] for k in ['variables','flags','government','ascension_perks','traditions','crisis','owned_colonies']) and ac['variables']['eep_c']==62 and ac['variables']['eep_d']==17 and ac['variables']['eep_worlds']==4,
 'all_real_resources_and_three_research_banks_full_queue_held':all(bc[k]==ac[k] for k in ['effective_stockpile','research_stockpile','tech_status']) and ac['effective_stockpile']['menace']==2135,
 'source14_exact34_months_real_seed_no_old_damage':all(p.get(k)==v for k,v in {'owner':0,'controller':0,'colony':30,'planet_size':14,'planet_class':'pc_ocean'}.items()) and p['variables']=={'eep_months':34,'eep_old_damage':0,'eep_q':14,'eep_seed_existing':100,'eep_seed_move':100,'eep_seed_need':0},
 'native_flags360_modifier_no_immediate_bite':all(k in p['flags'] for k in ['eep_active','eep_native','eep_owned_colony_event','colony_event','being_devoured']) and p['flags']['recently_eaten_planet']['flag_days']==360 and 'being_devoured_modifier' in p['modifiers'] and p['deposits']==oldp['deposits'],
 'unique_new_devour_situation_original_other_situations_held':set(sit)=={'167772163'} and sit['167772163']['country']==0 and sit['167772163']['progress']==0 and sit['167772163']['target']['id']==1578 and sit['167772163']['approach']=='eep_devour_approach' and set(aa['situations'])-set(ba['situations'])==set(sit) and all(aa['situations'].get(k)==v for k,v in ba['situations'].items()),
 'all_owned_ship_fleet_and_army_identity_design_health_held':owned(br)==owned(ar) and all(q.block(br['ships'],str(i))==q.block(ar['ships'],str(i)) for i in owned(br)[1]) and q.block(q.block(br['country'],'0'),'owned_armies')==q.block(q.block(ar['country'],'0'),'owned_armies') and all(q.block(br['army'],str(i))==q.block(ar['army'],str(i)) for i in q.ids(q.block(q.block(br['country'],'0'),'owned_armies'))),
 'original_messages_held_no_new_pending':messages(br)==messages(ar) and pending(br)==pending(ar),
 'production41_CN_and_unfiltered_error_held':m['language']=='l_simp_chinese' and m['version']=='0.2.0' and len(h.tree_manifest(h.MOD_ROOT)[0])==41 and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and obs['new_error_bytes']==0 and obs['error_prefix_held'] and h.sha256(user/'logs/error.log')==h.sha256(run/(before+'-error-after.log'))==h.sha256(run/(after+'-error-after.log'))=='4f3b0e6b9ac64daf9c3daf0346f8f61180f9e87486035a2f1a8298833becd850',
}
passed=all(v is True for v in checks.values());out=run/(after+'-fifth-devour-start-proof.json');assert not out.exists()
h.write_json(out,{'status':'PASS_FIFTH_NATIVE_DEVOUR_REAL_SEED_START' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'mother_before':bmr,'mother_after':amr,'source_before':bsr,'source_after':asr,'source':p,'situation':sit,'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Same-day start and true seed relocation only; not completion, Queen C200, high crisis or full route acceptance. Jobs are same-day native cache only.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
