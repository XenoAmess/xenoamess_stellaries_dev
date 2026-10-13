"""Read-only supplement for a native crystal encounter, not peaceful travel."""
import json, logging, re, sys
from pathlib import Path
sys.path.insert(0,'eat_everything_origin/tools')
sys.argv=['runtime']
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state
logging.disable(logging.INFO)
h=r.harness
run,user,meta=h.load_run()
before='terravore-travel164-22860101'
after='terravore-travel164-22860201'
load=lambda name:json.loads((run/name).read_text('utf-8-sig'))
b,a=read_state(run,before),read_state(run,after)
ba,aa=b['audit'],a['audit']
p=load(after+'-travel164-month-proof.json')
x=load(after+'-travel164-month-guard-execution.json')
failures=['all77_original_ships_identity_design_birth_name_life_held','no_pending_unknown_news_wars_truces_or_combat']
checks={k:v for k,v in p['checks'].items() if k not in failures}
checks['original24_only_two_expectedFAIL_actual1_source_pair_retained']=len(p['checks'])==24 and [k for k,v in p['checks'].items() if v is not True]==failures and x['returncode']==1 and x['helper_sha256']==h.sha256(Path(x['command'][1]))=='69fe57ce40e9a06dc9d60046b3f5f44c7131adeb81770918bf1ba4763fc87324' and p['before_sha256']==ba['save_sha256']==h.sha256(run/(before+'.sav')) and p['after_sha256']==aa['save_sha256']==h.sha256(run/(after+'.sav'))
mainids=set(q.ids(q.block(b['fleets']['83886903'],'ships')))
life=True
for i,bs in b['ships'].items():
    ass=a['ships'].get(i,'')
    bv,av=q.scalars(bs),q.scalars(ass)
    life=life and all(bv.get(k)==av.get(k) for k in ['construction_date','hitpoints','max_hitpoints','max_shield_hitpoints','max_armor_hitpoints']) and q.block(bs,'ship_design_implementation')==q.block(ass,'ship_design_implementation') and q.block(bs,'name')==q.block(ass,'name')
    if int(i) in mainids:
        life=life and bv.get('shield_hitpoints')==160 and av.get('shield_hitpoints',0)==0 and av.get('armor_hitpoints',0)==(151.865 if i=='16779033' else bv.get('armor_hitpoints',0))
    else:
        life=life and all(bv.get(k)==av.get(k) for k in ['shield_hitpoints','armor_hitpoints'])
checks['all77_ships_held_only18_nebula_shields_and_exact_one_armor_damage']=len(mainids)==18 and len(a['ships'])==77 and set(a['ships'])==set(b['ships']) and life
enemy=q.block(a['roots']['fleet'],'16777660')
country25=q.block(a['roots']['country'],'25')
main=a['fleets']['83886903']
combat=q.block(main,'combat')
checks['only_main_native_crystal_combat164_startJanuary26']=q.scalars(combat)['start_date']=='2286.01.26' and q.scalars(q.block(combat,'coordinate'))['origin']==164 and q.ids(q.block(combat,'in_combat_with'))==[16777660] and all(not q.ids(q.block(q.block(v,'combat'),'in_combat_with')) for i,v in a['fleets'].items() if i!='83886903')
checks['enemy_original_country25_crystal9_hulls_power783']=q.scalars(country25)['type']=='crystal' and re.search(r'\bfleet\s*=\s*16777660\b',q.block(q.block(country25,'fleets_manager'),'owned_fleets')) is not None and len(q.ids(q.block(enemy,'ships')))==9 and q.scalars(enemy)['military_power']==783.77343 and q.scalars(q.block(enemy,'name'))['key']=='NAME_Shardlings' and q.scalars(q.block(q.block(enemy,'movement_manager'),'coordinate'))['origin']==164
native=Path('C:/SteamLibrary/steamapps/common/Stellaris/common/static_modifiers/02_static_modifiers.txt')
source=native.read_text('utf-8-sig')
nebula=q.scalars(q.block(source,'turbulent_nebula'))
checks['native_turbulent_nebula_full_shield_reduction_exact_source']=nebula=={'ship_shield_reduction':1.0,'ship_speed_reduction':0.5,'ship_evasion_mult':0.3} and 'turbulent_nebula' in q.block(a['roots']['galactic_object'],'164')
checks['no_pending_messages_war_truce_or_extra_rewards']=not a['pending'] and not load(after+'-construction-boundary-observation-v4.json')['new_country0_messages_raw'] and b['roots']['war']==a['roots']['war'] and b['roots']['truce']==a['roots']['truce'] and aa['countries']['0']['effective_stockpile']['menace']==2930 and aa['countries']['0']['variables']==ba['countries']['0']['variables']
original=run/'terravore-crystal-turbulent-nebula-native-source.txt'
assert not original.exists()
original.write_bytes(native.read_bytes())
passed=all(v is True for v in checks.values())
out=run/(after+'-crystal-encounter-proof.json')
assert not out.exists()
h.write_json(out,{'status':'PASS_OBSERVED_NATIVE_CRYSTAL_ENCOUNTER' if passed else 'FAIL','checks':checks,'before_sha256':ba['save_sha256'],'after_sha256':aa['save_sha256'],'date':aa['date'],'native_source':{'file':original.name,'sha256':h.sha256(original)},'boundaries':['native_crystal_combat_7day_review'],'native_devour_calendar_ready':False,'maximum_days_to_native_bite_boundary':0,'scope':'Encounter boundary explicitly includes native combat and nebula shield suppression; not peaceful travel or full civic acceptance.'})
print(json.dumps({'status':'PASS' if passed else 'FAIL','checks':len(checks),'failed':[k for k,v in checks.items() if v is not True]}),flush=True)
assert passed
