"""Read-only native Theory research wait after exact mature agenda launch; no annual closure claim."""
import json,logging,re,shutil,sys,zipfile
from decimal import Decimal as D
from pathlib import Path
before,after,end,days,pre_name=sys.argv[1:];days=int(days);assert 1<=days<=360 and Path(pre_name).name==pre_name
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run();dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)

b=json.loads((run/(before+'.audit.json')).read_text(encoding='utf-8'));a=json.loads((run/(after+'.audit.json')).read_text(encoding='utf-8'));bc,ac=b['countries']['0'],a['countries']['0']
def extra(stem):
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o};col=q.block(roots['colony'],'0')
 return [q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0],[v for k,v,o in fs if k=='message' and q.scalars(v).get('receiver')==0 and q.scalars(v).get('type')=='MESSAGE_TERRAVORE_CONSUME_WORLD'],q.block(col,'last_month_growth_data')
bp,bm,bg=extra(before);ap,am,ag=extra(after);growth=q.scalars(q.block(ag,'growth_and_size'))
resources=['energy','minerals','food','consumer_goods','alloys','unity','trade','influence'];net={}
for k in resources:
 net[k]=sum((D(str(v.get(k,0))) for v in ac['budget_categories']['current_month']['balance'].values()),D(0))
receipt=json.loads((run/(after+'-calendar-receipt.json')).read_text(encoding='utf-8'));core=a['planets']['7'];source=a['planets']['90']
pre=json.loads((run/pre_name).read_text('utf-8'))
bgov,agov=q.scalars(bc['government']),q.scalars(ac['government'])
checks={'actual_days_date_and_receipt':a['date']==end and receipt['status']=='CALENDAR_CONFIRMED' and receipt['days']==days and receipt['start_date']==b['date'] and receipt['date']==a['date'],
 'original_SHA_pair':h.sha256(run/(before+'.sav'))==b['save_sha256'] and h.sha256(run/(after+'.sav'))==a['save_sha256'],
 'no_pending_or_repeat_Queen_notice':not bp and not ap,
 'all_EEP_ledger_and_flags_held':bc['variables']==ac['variables'] and bc['flags']==ac['flags'],
 'C37_G0_D11_made0_worlds2':all(ac['variables'][k]==v for k,v in {'eep_c':37,'eep_g':0,'eep_d':11,'eep_made':0,'eep_worlds':2}.items()),
 'no_new_bite_message':all(am.count(x)<=bm.count(x) for x in am) and all(am.count(x)==bm.count(x) or q.scalars(x).get('end','9999.12.30')<=a['date'] for x in bm),
 'no_new_active_task':not any(s.get('type')=='situation_eep_devouring' and s.get('killed')!='yes' for s in a['situations'].values()),
 'source_still_unowned_shattered':all(a['planets'][pid].get('owner') is None and a['planets'][pid].get('controller') is None and a['planets'][pid]['planet_class']=='pc_shattered' and not a['planets'][pid]['deposits'] for pid in ['90','124']),
 'source_no_actual_population':not any(p['planet'] in [15,24] and p['size']>0 for p in a['pop_groups'].values()),
 'only_mother_owned':bc['owned_colonies']==ac['owned_colonies']==[0],
 'population_nondecreasing_founder_only':a['colonies']['0']['actual_pop_sum']>=b['colonies']['0']['actual_pop_sum'] and all(g['key']['species']==3321888769 for g in a['pop_groups'].values() if g['planet']==0 and g['size']>0),
 'all_actual_stocks_nonnegative':all(D(str(v))>=0 for v in ac['effective_stockpile'].values()),
 'last_month_minerals_energy_unity_net_nonnegative':all(net[k]>=0 for k in ['energy','minerals','unity']),
 'original_AP_and_traditions_held':bc['ascension_perks']==ac['ascension_perks'] and bc['traditions']==ac['traditions'],
 'unique_core_owned_capacity11_size18':sum('eep_core' in p['flags'] for p in a['planets'].values())==1 and core['owner']==core['controller']==0 and core['colony']==0 and core['planet_size']==18 and core['variables']['eep_capacity_value']==11,
 'one_permanent_capacity11':core['modifiers'].count('modifier="eep_capacity"')==1 and bool(re.search(r'multiplier\s*=\s*11\s+modifier\s*=\s*"eep_capacity"\s+days\s*=\s*-1',core['modifiers'])),
 'court_and_original_deposit_held':core['modifiers'].count('modifier="eep_court"')==1 and [(i,v) for i,v in b['deposits'].items() if v.get('type')=='d_eep_core']==[(i,v) for i,v in a['deposits'].items() if v.get('type')=='d_eep_core'],
 'mother_actual_districts_held':a['colonies']['0']['districts']==b['colonies']['0']['districts'] and all(a['districts'][str(i)]==b['districts'][str(i)] for i in b['colonies']['0']['districts']),
 'source_species_and_binding_held':a['species']==b['species'] and a['event_targets']==b['event_targets'],
 'no_new_error':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()}
checks.update({
 'bound_actual_prior_PASS_and_SHA':pre['status'].startswith('PASS_') and bool(pre['checks']) and all(v is True for v in pre['checks'].values()) and pre['after_sha256']==b['save_sha256'],
 'same_native_government_MOM_launched_no_current_agenda':all(bgov.get(k)==agov.get(k) for k in ['type','authority','origin']) and all(k not in g for g in [bgov,agov] for k in ['council_agenda','council_agenda_progress']),
 'Theory_not_completed_still_selected_and_progress_growing':all('tech_psionic_theory' not in c['completed_technologies'] and q.scalars(q.block(c['tech_status'],'society_queue').strip()[1:-1]).get('technology')=='tech_psionic_theory' for c in [bc,ac]) and D(str(q.scalars(q.block(ac['tech_status'],'society_queue').strip()[1:-1]).get('progress',0)))>D(str(q.scalars(q.block(bc['tech_status'],'society_queue').strip()[1:-1]).get('progress',0))),
 'specialized_Theory650_and_old607_25288_held':bc['research_progress_by_tech']==ac['research_progress_by_tech']=={'tech_psionic_theory':650,'tech_colonization_2':607.25288},
 'completed_technologies_not_lost':set(bc['completed_technologies'])<=set(ac['completed_technologies']),
 'true_research_banks_held':q.block(bc['tech_status'],'stored_techpoints')==q.block(ac['tech_status'],'stored_techpoints'),
 'mother_mining2000_generator800_fully_staffed':all(len(js:=[j for j in a['pop_jobs'].values() if j['planet']==0 and j['type']==kind])==1 and js[0]['workforce']==js[0]['max_workforce']==value for kind,value in [('mining_drone',2000),('technician_drone',800)]),
})
p={'status':'PASS_NATIVE_TERRAVORE_THEORY_WAIT_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'last_native_month_growth_only':growth,'agenda_before_after':[bgov,agov],'bound_prior_proof':pre_name,'true_bank_before_after':[q.block(bc['tech_status'],'stored_techpoints'),q.block(ac['tech_status'],'stored_techpoints')],'research_queues':ac['research_queues'],'actual_current_month_net':{k:str(v) for k,v in net.items()},'stockpile':ac['effective_stockpile'],'newly_completed_technologies':sorted(set(ac['completed_technologies'])-set(bc['completed_technologies'])),'scope':'Native Theory research wait with two settled sources and an already launched agenda. Exact selected Theory queue grows; specialized650 and former607.25288 retained. Last monthly net and nonnegative stocks only; no annual cumulative closure, Theory completion, Shroud, reload or full route claim.'}
out=run/(after+'-theory-wait-proof.json');assert not out.exists();h.write_json(out,p);print(json.dumps(p),flush=True);assert all(checks.values()),'Original Theory wait FAIL retained; no next calendar'
