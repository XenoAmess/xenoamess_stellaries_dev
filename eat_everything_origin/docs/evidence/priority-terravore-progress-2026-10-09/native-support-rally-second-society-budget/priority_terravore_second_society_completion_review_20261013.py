"""Read-only, documented 18-day preflight for the second paid society zone."""
import json, logging, sys
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, 'eat_everything_origin/tools'); sys.argv = ['runtime']
import runtime as r, audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h = r.harness; run, user, meta = h.load_run()
load = lambda name: json.loads((run/name).read_text('utf-8-sig'))
before = 'terravore-second-society-precomplete-22870101'
after = 'terravore-second-society-completed-22870119'
a = read_state(run, before); audit = a['audit']; country = audit['countries']['0']
p = load(before+'-support-zone-v5-proof.json')
x = load(before+'-support-zone-v5-guard-execution.json')
ids = q.ids(q.block(a['queues']['0'], 'items'))
head = q.scalars(a['items']['201326629'])
zone = q.block(a['roots']['zones'], '16777330')
project_raw = country['research_queues']['society_queue']; ts = list(q.tokens(project_raw))
project = q.scalars(project_raw[ts[0][2]:ts[-1][1]])
income = sum((D(str(v.get('society_research', 0))) for v in country['budget_categories']['current_month']['income'].values()), D(0))
ships = q.ids(q.block(a['queues'].get('3', ''), 'items'))
orbitals = q.scalars(q.block(q.block(q.block(a['roots']['planets'], 'planet'), '1732'), 'planet_orbitals'))
support = {}
for fid, index in [('917', 1), ('50332250', 2)]:
    fleet = a['fleets'][fid]; mm = q.block(fleet, 'movement_manager')
    support[fid] = not q.block(fleet, 'current_order') and q.scalars(q.block(mm, 'coordinate'))['origin'] == 164 and q.scalars(q.block(mm, 'orbit')) == {'index':index} and q.scalars(q.block(q.block(mm, 'orbit'), 'orbitable')) == {'planet':1732} and orbitals.get(str(index)) == int(fid)
checks = {
    'V5_27PASS_actual0_source_original_SAV': p['status']=='PASS_NATIVE_SUPPORT_ZONE' and len(p['checks'])==27 and all(v is True for v in p['checks'].values()) and x['returncode']==0 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='e459d2756c7b107cf2351bf7851c61a281ea9cdde3a5de42e943ec03ba983f4b' and p['after_sha256']==audit['save_sha256']==h.sha256(run/(before+'.sav')),
    'paid800_front_336_of360_four_paid_hives_held': ids==[201326629,1191182345,117440553,1476395019,117440546] and head=={'queue':0,'paying_country':0,'progress':336,'progress_needed':360} and q.scalars(q.block(a['items']['201326629'],'resources'))=={'minerals':800} and [q.scalars(a['items'][str(i)])['progress'] for i in ids[1:]]==[2.8,0,0,0] and all(q.scalars(q.block(a['items'][str(i)],'resources'))=={'minerals':400} for i in ids[1:]),
    'engineering_zone_three_original_labs_1200to360_expected': audit['districts']['1']=={'type':'district_hive','level':7,'zones':[0,67108970,16777330]} and q.scalars(zone)=={'type':'zone_research_engineering'} and q.ids(q.block(zone,'buildings'))==[33554447,50331690,16777354] and [audit['pop_jobs'][i]['max_workforce'] for i in ['23','24','25']]==[360,1200,1200],
    'native_orbit_both_supports_no_pending_combat_ships_and_one_tick_project_safe': all(support.values()) and not a['pending'] and not ships and not any(q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for v in a['fleets'].values()) and project['special_project']==9 and D(str(project['progress']))+income*D('2.35')<12000,
    'CN41_live_error_same_18days_no_month_boundary': audit['date']=='2287.01.01' and p['boundaries']==['native_paid_second_society_next_boundary_review'] and meta['language']=='l_simp_chinese' and h.tree_manifest(h.MOD_ROOT)[1]=='ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7' and (user/'logs/error.log').read_bytes()==(run/(before+'-error-after.log')).read_bytes(),
}
passed = all(v is True for v in checks.values())
stage = before+'-second-society-zone-completion-review'
out = run/(stage+'.json'); assert not out.exists()
h.write_json(out, {'status':'PASS_REVIEWED_NATIVE_BOUNDARY' if passed else 'FAIL','checks':checks,'before_sha256':audit['save_sha256'],'after_sha256':audit['save_sha256'],'start_date':audit['date'],'end_date':'2287.01.19','days':18,'maximum_days':18,'allowed_boundaries':p['boundaries'],'execution_stage':stage,'scope':'One paid second society zone completion, one old-month research tick; no monthly cash settlement.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'support_orbit_registered':support}),flush=True)
assert passed
