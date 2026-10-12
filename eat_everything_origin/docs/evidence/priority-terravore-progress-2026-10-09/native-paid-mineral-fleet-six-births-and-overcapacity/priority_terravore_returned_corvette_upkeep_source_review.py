"""Independently resolve official ordinary corvette component upkeep sources."""
import json,logging,re,shutil,sys,zipfile
from collections import Counter
from decimal import Decimal as D
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools');sys.argv=['runtime']
import runtime as r,audit_save as q
logging.disable(logging.INFO);h=r.harness;run,user,m=h.load_run()
load=lambda n:json.loads((run/n).read_text(encoding='utf-8-sig'))
stage='terravore-returned-corvette-upkeep-source-review';after='terravore-six-mineral-build-22800201'
o=load(after+'-construction-boundary-observation-v4.json');b,a=o['before_state'],o['after_state'];base=Path('C:/SteamLibrary/steamapps/common/Stellaris/common')
globalvars={};sources={};templates={};texts={}
def preserve(p):
 key=str(p)
 if key in sources:return
 dest=run/('terravore-ordinary-upkeep-native-'+p.name);assert not dest.exists();shutil.copyfile(p,dest);sources[key]={'path':key,'preserved':dest.name,'sha256':h.sha256(p)}
for p in (base/'scripted_variables').glob('*.txt'):
 text=p.read_text(encoding='utf-8-sig');local=q.scalars(text)
 for key,val in local.items():
  if key.startswith('@'):globalvars[key]=(val,p)
targets=Counter(['FLAK_BATTERY_1','SMALL_MASS_DRIVER_2','MISSILE_1','SMALL_ARMOR_2','SMALL_ARMOR_2','SMALL_SHIELD_3','REACTOR_BOOSTER_1','CORVETTE_FUSION_REACTOR','HYPER_DRIVE_2','SHIP_THRUSTER_1','SENSOR_2','COMBAT_COMPUTER_DEFAULT'])
for p in (base/'component_templates').glob('00_*.txt'):
 text=p.read_text(encoding='utf-8-sig')
 if not any(key in text for key in targets):continue
 for k,v,x in q.fields(text):
  if x and q.scalars(v).get('key') in targets:
   key=q.scalars(v)['key'];assert key not in templates;templates[key]=(v,p,q.scalars(text));texts[p]=text;preserve(p)
def resolve(value,local,seen=()):
 if isinstance(value,str) and value.startswith('@'):
  assert value not in seen
  if value in local:return resolve(local[value],local,seen+(value,))
  val,p=globalvars[value];preserve(p);return resolve(val,local,seen+(value,))
 return D(str(value))
components=[];total={'energy':D(0),'alloys':D(0)}
for key,count in targets.items():
 raw,p,local=templates[key];up=q.scalars(q.block(q.block(raw,'resources'),'upkeep'));fees={k:resolve(v,local) for k,v in up.items()};components.append({'key':key,'count':count,'template_original':raw,'source':str(p),'upkeep':{k:str(v) for k,v in fees.items()}})
 for k,v in fees.items():total[k]=total.get(k,D(0))+v*count
shipvars=base/'scripted_variables/03_scripted_variables_ships.txt';preserve(shipvars);sv=q.scalars(shipvars.read_text(encoding='utf-8-sig'));preserve(base/'ship_sizes/00_ship_sizes.txt');preserve(base/'ship_sizes/20_nemesis.txt')
messages=Path('C:/SteamLibrary/steamapps/common/Stellaris/localisation/simp_chinese/messages_l_simp_chinese.yml');preserve(messages)
with zipfile.ZipFile(run/(after+'.sav')) as z:roots={k:v for k,v,x in q.fields(z.read('gamestate').decode('utf-8-sig')) if x}
enemyowned=set(map(int,re.findall(r'\bfleet\s*=\s*(\d+)',q.block(q.block(q.block(roots['country'],'1'),'fleets_manager'),'owned_fleets'))));enemy=q.block(roots['fleet'],'825')
checks={
 'all_original_design_component_templates_resolved':set(templates)==set(targets) and all(key in q.block(a['raw_roots']['ship_design'],'167772797') for key in targets),
 'official_component_fees_exact074E0124A':total=={'energy':D('.74'),'alloys':D('.124')},
 'official_ordinary_corvette_base1E05A':sv['@corvette_upkeep_energy']==1 and sv['@corvette_upkeep_alloys']==.5,
 'actual_first_post_return_month_fee_change_reconciled':a['audit']['countries']['0']['budget_categories']['current_month']['expenses']['ships']=={'energy':25.25,'minerals':2.25,'trade':10.5,'alloys':10.5} and a['audit']['countries']['0']['budget_categories']['current_month']['expenses']['ship_components']=={'energy':19.14,'alloys':3.255},
 'known_fleet825_detection_only_original_country1_five':825 in enemyowned and set(q.ids(q.block(enemy,'ships')))=={16779110,33556025,67109342,16779083,33556209} and len(o['new_country0_messages_raw'])==1 and q.scalars(o['new_country0_messages_raw'][0])['target_fleet']==825 and q.scalars(o['new_country0_messages_raw'][0])['type']=='FLEET_DETECTED_MESSAGE_TYPE' and 'MESSAGE_FLEET_DETECTED_WE:' in messages.read_text(encoding='utf-8-sig'),
 'original_source_copies_and_ui_preserved':all(h.sha256(Path(v['path']))==h.sha256(run/v['preserved'])==v['sha256'] for v in sources.values()) and (run/'terravore-returned-ordinary-corvette-actual-row-upkeep-ui.jpg').is_file(),
}
passed=all(v is True for v in checks.values());out=run/(stage+'.json');assert not out.exists()
h.write_json(out,{'status':'PASS_NATIVE_RETURNED_ORDINARY_CORVETTE_FEES' if passed else 'FAIL','checks':checks,'before_sha256':b['audit']['save_sha256'],'after_sha256':a['audit']['save_sha256'],'components':components,'component_upkeep_total':{k:str(v) for k,v in total.items()},'sources':list(sources.values()),'detected_enemy_fleet_raw':enemy,'detection_message_original':o['new_country0_messages_raw'],'native_ui_file':'terravore-returned-ordinary-corvette-actual-row-upkeep-ui.jpg','native_ui_sha256':h.sha256(run/'terravore-returned-ordinary-corvette-actual-row-upkeep-ui.jpg'),'scope':'Exact ordinary returned ship fees source resolution and known fleet detection; added mineral ships have separate paid orders and native hull sources.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'fees':{k:str(v) for k,v in total.items()},'failed':[k for k,v in checks.items() if v is not True]}),flush=True);assert passed
