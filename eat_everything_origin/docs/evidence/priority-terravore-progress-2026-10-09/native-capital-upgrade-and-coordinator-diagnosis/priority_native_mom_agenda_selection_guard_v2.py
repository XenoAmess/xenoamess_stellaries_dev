"""Read-only exact native Mind over Matter agenda selection; no calendar or grants."""
import json,logging,shutil,sys,zipfile
from pathlib import Path
before,after=sys.argv[1:]
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
dest=run/Path(__file__).name
if dest.exists():assert dest.read_bytes()==Path(__file__).read_bytes()
else:shutil.copyfile(__file__,dest)
def read(stem):
 a=json.loads((run/(stem+'.audit.json')).read_text('utf-8'))
 with zipfile.ZipFile(run/(stem+'.sav')) as z:t=z.read('gamestate').decode('utf-8-sig')
 fs=list(q.fields(t));roots={k:v for k,v,o in fs if o}
 pending=[q.scalars(v) for k,v,o in fs if k=='player_event' and q.scalars(v).get('country')==0]
 return a,fs,roots,pending
b,bf,br,bp=read(before);a,af,ar,ap=read(after);bc,ac=b['countries']['0'],a['countries']['0']
bcs,acs={k:v for k,v,o in q.fields(br['country']) if o},{k:v for k,v,o in q.fields(ar['country']) if o}
bg,ag=bc['government'],ac['government'];bgs,ags=q.scalars(bg),q.scalars(ag)
checks={
 'same_actual_date':b['date']==a['date']=='2231.03.02',
 'original_SHA_pair':b['save_sha256']==h.sha256(run/(before+'.sav')) and a['save_sha256']==h.sha256(run/(after+'.sav')),
 'original_no_agenda_and_no_progress':not any(k in bgs for k in ['council_agenda','council_agenda_progress']),
 'native_MOM_agenda_zero_progress':ags['council_agenda']=='agenda_mind_over_matter' and ags['council_agenda_progress']==0,
 'all_other_government_direct_fields_raw_held':[(k,v,o) for k,v,o in q.fields(bg) if k not in ['council_agenda','council_agenda_progress']]==[(k,v,o) for k,v,o in q.fields(ag) if k not in ['council_agenda','council_agenda_progress']],
 'all_other_country0_direct_fields_raw_held':[(k,v,o) for k,v,o in q.fields(bcs['0']) if k!='government']==[(k,v,o) for k,v,o in q.fields(acs['0']) if k!='government'],
 'all_other_countries_raw_held':set(bcs)==set(acs) and all(acs[k]==v for k,v in bcs.items() if k!='0'),
 'all_other_top_level_fields_raw_held':[(k,v,o) for k,v,o in bf if k not in ['country','random_count']]==[(k,v,o) for k,v,o in af if k not in ['country','random_count']],
 'original_random_counter_only_plus1':int(next(v for k,v,o in af if k=='random_count'))==int(next(v for k,v,o in bf if k=='random_count'))+1,
 'no_country_pending':not bp and not ap,
 'unfiltered_error_bytes_held':(run/(after+'-error-before.log')).read_bytes()==(run/(after+'-error-after.log')).read_bytes()==(run/(before+'-error-after.log')).read_bytes()
}
for k in ['effective_stockpile','variables','flags','traditions','ascension_perks','tech_status','research_queues','completed_technologies','budget_categories','owned_colonies']:checks[k+'_held']=bc[k]==ac[k]
for k in ['pop_groups','pop_jobs','colonies','planets','districts','deposits','situations','species','event_targets']:checks[k+'_held']=b[k]==a[k]
proof={'status':'PASS_NATIVE_MOM_AGENDA_SELECTION_COMPONENT' if all(checks.values()) else 'FAIL','checks':checks,'before_sha256':b['save_sha256'],'after_sha256':a['save_sha256'],'government_before':bg,'government_after':ag,'scope':'Actual normal agenda selection from an empty native agenda only. No mature agenda launch, free research, Shroud or full civic acceptance claim.'}
out=run/(after+'-mom-agenda-selection-v2-proof.json');assert not out.exists();h.write_json(out,proof);print(json.dumps(proof),flush=True);assert all(checks.values()),'Original agenda selection FAIL retained; do not replay'
