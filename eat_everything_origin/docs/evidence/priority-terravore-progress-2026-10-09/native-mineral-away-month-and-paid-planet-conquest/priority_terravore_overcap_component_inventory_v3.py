"""Read-only actual-design component fee inventory, with native per-component precision."""
from pathlib import Path
import json,sys,re
from decimal import Decimal as D,ROUND_DOWN
from collections import Counter
sys.path.insert(0,'eat_everything_origin/tools');import audit_save as q
run=Path('_runtime/heart-of-devouring/runs/20261009T044016Z');o=json.loads((run/'terravore-first-overcap-month-22800401-construction-boundary-observation-v4.json').read_text(encoding='utf-8'));a=o['after_state'];base=Path('C:/SteamLibrary/steamapps/common/Stellaris/common');g={}
for p in (base/'scripted_variables').glob('*.txt'):g.update(q.scalars(p.read_text(encoding='utf-8-sig')))
sizes={}
for fn in ['00_ship_sizes.txt','00_starbases.txt','20_nemesis.txt']:
 p=base/'ship_sizes'/fn;t=p.read_text(encoding='utf-8-sig');local=q.scalars(t)
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
 l=q.scalars(t)
 for k,v,x in q.fields(t):
  key=re.search(r'^\s*key\s*=\s*"([^"]+)"',v,re.M) if x else None
  if key and key[1] in targets:assert key[1] not in ts;ts[key[1]]=(v,l)
def val(v,l):return val(l.get(v,g.get(v)),l) if isinstance(v,str) and v.startswith('@') else D(str(v))
quant=lambda v:v.quantize(D('.00001'),rounding=ROUND_DOWN)
total=Counter();details=[]
for i,(size,cls,keys) in shipkeys.items():
 fees=Counter();factor=D(133)/131 if cls=='shipclass_military' else D('.5')
 for k,n in keys.items():
  tr,l=ts[k]
  for res,v in q.scalars(q.block(q.block(tr,'resources'),'upkeep')).items():fees[res]+=quant(val(v,l)*factor)*n
 total.update(fees);details.append({'ship':i,'size':size,'class':cls,'factor':str(factor),'fees':{k:str(v) for k,v in fees.items()}})
out=run/'terravore-overcap-component-readonly-inventory-v3.json';assert not out.exists();out.write_text(json.dumps({'details':details,'total':{k:str(v) for k,v in total.items()},'original_expenses':a['audit']['countries']['0']['budget_categories']['current_month']['expenses'],'before_sha256':o['before_state']['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256']},indent=2),encoding='utf-8')
print('TOTAL',total);print('NONCORV',json.dumps([v for v in details if v['size']!='corvette']));print('CORV',Counter(tuple(sorted(v['fees'].items())) for v in details if v['size']=='corvette'))
