"""Read-only actual-design component fee inventory, with native per-component precision."""
from pathlib import Path
import json,sys,re,hashlib,shutil,zipfile
from decimal import Decimal as D,ROUND_DOWN,ROUND_UP
from collections import Counter
sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z');o=json.loads((run/'terravore-first-overcap-month-22800401-construction-boundary-observation-v4.json').read_text(encoding='utf-8'));a=o['after_state'];base=Path('C:/SteamLibrary/steamapps/common/Stellaris/common');g={}
sources={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def preserve(p):
 key=str(p)
 if key not in sources:
  dest=run/('terravore-overcap-fees-native-'+p.parent.name+'-'+p.name);assert not dest.exists();shutil.copyfile(p,dest);sources[key]={'path':key,'preserved':dest.name,'sha256':sha(p)}
for p in (base/'scripted_variables').glob('*.txt'):
 g.update(q.scalars(p.read_text(encoding='utf-8-sig')));preserve(p)
for p in [base/'ascension_perks/00_ascension_perks.txt',base/'starbase_buildings/00_starbase_buildings.txt',Path('C:/SteamLibrary/steamapps/common/Stellaris/localisation/simp_chinese/concepts_l_simp_chinese.yml')]:preserve(p)
sizes={}
for fn in ['00_ship_sizes.txt','00_starbases.txt','20_nemesis.txt']:
 p=base/'ship_sizes'/fn;preserve(p);t=p.read_text(encoding='utf-8-sig');local=q.scalars(t)
 for k,v,x in q.fields(t):
  if x:sizes[k]=(v,local)
designs={k:v for k,v,x in q.fields(a['raw_roots']['ship_design']) if x};ts={};shipkeys={};targets=set()
for i,s in a['owned_ships_raw'].items():
 fid=str(q.scalars(s)['fleet']);f=a['owned_fleets_raw'][fid]
 if q.scalars(q.block(f,'properties')).get('mia')=='yes':continue
 did=str(q.scalars(q.block(s,'ship_design_implementation'))['design']);dr=designs[did];size=re.findall(r'ship_size="([^"]+)"',dr);assert len(size)==1
 sr,sl=sizes[size[0]];ss=q.scalars(sr)
 if ss.get('components_add_to_cost')=='no':continue
 keys=Counter(re.findall(r'\bcomponent\s*=\s*\{[^{}]*\btemplate="([^"]+)"',dr)+re.findall(r'required_component="([^"]+)"',dr));shipkeys[i]=(size[0],ss.get('class'),keys);targets.update(keys)
for p in (base/'component_templates').glob('00_*.txt'):
 t=p.read_text(encoding='utf-8-sig')
 if not any(k in t for k in targets):continue
 preserve(p);l=q.scalars(t)
 for k,v,x in q.fields(t):
  key=re.search(r'^\s*key\s*=\s*"([^"]+)"',v,re.M) if x else None
  if key and key[1] in targets:assert key[1] not in ts;ts[key[1]]=(v,l)
def val(v,l):return val(l.get(v,g.get(v)),l) if isinstance(v,str) and v.startswith('@') else D(str(v))
quant=lambda v:v.quantize(D('.00001'),rounding=ROUND_DOWN)
total_low=Counter();total_high=Counter();details=[]
for i,(size,cls,keys) in shipkeys.items():
 lo=Counter();hi=Counter();factor=quant(D(133)/131) if cls=='shipclass_military' else D('.5');upper=factor+D('.00001') if cls=='shipclass_military' else factor
 for k,n in keys.items():
  tr,l=ts[k]
  for res,v in q.scalars(q.block(q.block(tr,'resources'),'upkeep')).items():
   lo[res]+=quant(val(v,l)*factor)*n;hi[res]+=(val(v,l)*upper).quantize(D('.00001'),rounding=ROUND_UP)*n
 total_low.update(lo);total_high.update(hi);details.append({'ship':i,'size':size,'class':cls,'factor_lower':str(factor),'factor_upper':str(upper),'fees_lower':{k:str(v) for k,v in lo.items()},'fees_upper':{k:str(v) for k,v in hi.items()}})
def savroots(stage):
 with zipfile.ZipFile(run/(stage+'.sav')) as z:return {k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
br,ar=[savroots(st) for st in ['terravore-constructor-return-22800317','terravore-first-overcap-month-22800401']];b=o['before_state'];c=a['audit']['countries']['0'];exp=c['budget_categories']['current_month']['expenses'];factor=quant(D(133)/131)
basefee={'energy':D(21)*quant(D(1)*factor)+D(7)*quant(D('.75')*factor)+3,'minerals':D(7)*quant(D('.75')*factor),'alloys':D(21)*quant(D('.5')*factor)}
owned=lambda raw:set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(raw,'fleets_manager'),'owned_fleets'))))
be=owned(q.block(br['country'],'1'));ae=owned(q.block(ar['country'],'1'));bs={k:v for k,v,x in q.fields(br['ships']) if x};ass={k:v for k,v,x in q.fields(ar['ships']) if x}
transfers=[]
for i in [1882,1887,1897]:
 old,new=bs[str(i)],ass[str(i)];os,ns=q.scalars(old),q.scalars(new);fid=os['fleet'];transfers.append({'ship':i,'before_ship_raw':old,'after_ship_raw':new,'valid':fid in be and fid not in ae and fid in a['owned_fleets'] and ns['fleet']==fid and os['construction_date']==ns['construction_date'] and ns['hitpoints']>0 and q.scalars(q.block(new,'coordinate'))['origin']==146})
def objects(raw):
 depth=0;start=0
 for token,x,y in q.tokens(raw):
  if token=='{':
   if depth==0:start=y
   depth+=1
  elif token=='}':
   depth-=1
   if depth==0:yield raw[start:x]
 assert depth==0
reports=o['new_country0_messages_raw'];report=reports[0] if len(reports)==1 else '';rs=q.scalars(report);cs=q.block(report,'combat_stats');ours=list(objects(q.block(cs,'fleets')));enemies=list(objects(q.block(cs,'enemy')))
b0=q.block(q.block(ar['starbase_mgr'],'starbases'),'0');platformmod=q.scalars(q.block(q.block((base/'ascension_perks/00_ascension_perks.txt').read_text(encoding='utf-8-sig'),'ap_eternal_vigilance'),'modifier'))
checks={
 'original_SAVs_prior25_and_calendar_observer_actual0':all(v is True for v in o['checks'].values()) and all(st['audit']['save_sha256']==sha(run/(name+'.sav')) for st,name in [(b,'terravore-constructor-return-22800317'),(a,'terravore-first-overcap-month-22800401')]) and all(json.loads((run/(name+'-execution.json')).read_text(encoding='utf-8'))['returncode']==0 for name in ['terravore-first-overcap-month-22800401-calendar','terravore-first-overcap-month-22800401-boundary-observation-v4','terravore-constructor-return-22800317-campaign-guard-v9']),
 'same_original_146_three_stations_recaptured_only':set(a['owned_ship_ids'])-set(b['owned_ship_ids'])=={1882,1887,1897} and set(b['owned_ship_ids'])<=set(a['owned_ship_ids']) and all(v['valid'] for v in transfers),
 'exact_native290_main18_enemyfive_zero_kills':rs.get('type')=='COMBAT_STATS' and rs.get('notification')==290 and rs.get('date')=='2280.03.25' and q.scalars(cs).get('reason')=='no_more_enemies' and len(ours)==len(enemies)==1 and q.scalars(ours[0])['fleet']==83886903 and q.ids(q.block(ours[0],'ship_size_count'))==[18] and q.ids(q.block(ours[0],'ship_size_count_lost'))==[0] and q.scalars(enemies[0])['fleet']==825 and q.ids(q.block(enemies[0],'ship_size_count'))==[1,1,3] and q.ids(q.block(enemies[0],'ship_size_count_lost'))==[0,0,0],
 'original_enemy_five_survive_and_no_Menace':all(q.scalars(ass[str(i)])['hitpoints']>0 and q.scalars(bs[str(i)])['construction_date']==q.scalars(ass[str(i)])['construction_date'] for i in [16779110,33556025,67109342,16779083,33556209]) and c['effective_stockpile']['menace']==b['audit']['countries']['0']['effective_stockpile']['menace']==1635,
 'source21_corvettes_two_platforms_only_component_fees':sum(v['size']=='corvette' for v in details)==21 and {v['ship'] for v in details if v['size']!='corvette'}=={'1900','83887310'} and 'ap_eternal_vigilance' in c['ascension_perks'] and platformmod['ship_military_station_small_upkeep_mult']==-.5,
 'seven_original_mineral_ships_no_component_fees_docked_discount':len(q.ids(q.block(a['owned_fleets_raw']['50332250'],'ships')))==7 and 50332250 in q.scalars(q.block(b0,'orbitals')).values() and 'crew_quarters' in q.scalars(q.block(b0,'buildings')).values() and q.scalars(sizes['crisis_corvette'][0])['components_add_to_cost']=='no' and q.scalars(q.block(q.block((base/'starbase_buildings/00_starbase_buildings.txt').read_text(encoding='utf-8-sig'),'crew_quarters'),'orbit_modifier'))=={'ship_orbit_upkeep_mult':-.25},
 'naval133_and_base_fees_exact':c['native']['used_naval_capacity']==133 and all(D(str(exp['ships'][k]))==v for k,v in basefee.items()),
 'components_within_per_component_quantization_bounds':all(total_low[k]<=D(str(exp['ship_components'][k]))<=total_high[k] for k in ['energy','alloys']),
 'all_original_source_bytes_preserved':all(sha(Path(v['path']))==sha(run/v['preserved'])==v['sha256'] for v in sources.values()),
}
passed=all(v is True for v in checks.values());out=run/'terravore-first-overcap-native-source-review.json';assert not out.exists();out.write_text(json.dumps({'status':'PASS_NATIVE_OVERCAPACITY_SOURCE' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'components':details,'components_lower':{k:str(v) for k,v in total_low.items()},'components_upper':{k:str(v) for k,v in total_high.items()},'base_fees_exact':{k:str(v) for k,v in basefee.items()},'observed_component_fees':exp['ship_components'],'native_report_original':reports,'transfers':transfers,'sources':list(sources.values()),'scope':'Exact native base fees and source attribution. Component intermediate rounding is bounded, not claimed as an exact closed-engine formula. Full subsequent month must hold these observed fees exactly.'},indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True],'components_lower':{k:str(v) for k,v in total_low.items()},'components_upper':{k:str(v) for k,v in total_high.items()}}),flush=True);assert passed
