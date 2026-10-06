"""Create a fresh, traceable test package without modifying production files."""
from pathlib import Path
import argparse
import json
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

PRESETS = [
    ("01-terravore", "EEP 01 石质噬岩者", "LITHOID", "lith11", "trait_lithoid", "auth_hive_mind", "gov_devouring_swarm", ["ethic_gestalt_consciousness"], ["civic_hive_devouring_swarm", "civic_hive_ascetic"], "pc_continental"),
    ("02-hive", "EEP 02 有机吞噬蜂群", "HUM", "human", "trait_organic", "auth_hive_mind", "gov_devouring_swarm", ["ethic_gestalt_consciousness"], ["civic_hive_devouring_swarm", "civic_hive_ascetic"], "pc_continental"),
    ("03-machine", "EEP 03 铁心灭绝者", "MACHINE", "sd_hum_robot", "trait_machine_unit", "auth_machine_intelligence", "gov_machine_terminator", ["ethic_gestalt_consciousness"], ["civic_machine_terminator", "civic_machine_replication"], "pc_continental"),
    ("04-purifier", "EEP 04 种族洁癖", "HUM", "human", "trait_organic", "auth_dictatorial", "gov_purity_order", ["ethic_fanatic_xenophobe", "ethic_spiritualist"], ["civic_fanatic_purifiers", "civic_efficient_bureaucracy"], "pc_continental"),
    ("05-scorched", "EEP 05 焦土帝国", "INF", "inf9", "trait_infernal", "auth_dictatorial", "gov_despotic_hegemony", ["ethic_fanatic_xenophobe", "ethic_materialist"], ["civic_scorched_earth", "civic_efficient_bureaucracy"], "pc_volcanic"),
    ("06-scorched-hive", "EEP 06 焦土蜂巢", "INF", "inf9", "trait_infernal", "auth_hive_mind", "gov_hive_mind", ["ethic_gestalt_consciousness"], ["civic_hive_scorched_earth", "civic_hive_ascetic"], "pc_volcanic"),
    ("07-control", "EEP 07 普通帝国拒绝对照", "HUM", "human", "trait_organic", "auth_dictatorial", "gov_despotic_hegemony", ["ethic_fanatic_xenophobe", "ethic_materialist"], ["civic_efficient_bureaucracy", "civic_mining_guilds"], "pc_continental"),
    ("08-native-terravore", "EEP 08 原版噬岩对照", "LITHOID", "lith11", "trait_lithoid", "auth_hive_mind", "gov_devouring_swarm", ["ethic_gestalt_consciousness"], ["civic_hive_devouring_swarm", "civic_hive_ascetic"], "pc_continental"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = args.output or REPO / f"_runtime/heart-of-devouring/fixtures/{stamp}"
    if target.exists():
        raise FileExistsError(target)
    shutil.copytree(ROOT / "mod", target / "mod")
    shutil.copytree(ROOT / "testing/mod", target / "mod", dirs_exist_ok=True)
    shutil.copy2(ROOT / "VERSION", target / "VERSION")
    preset_file = target / "mod/prescripted_countries/eep_probe_presets.txt"
    preset_file.parent.mkdir(parents=True)
    blocks = []
    for key, name, klass, portrait, trait, authority, government, ethics, civics, planet in PRESETS:
        origin = "origin_default" if key.startswith(("07", "08")) else "origin_heart_of_devouring"
        block = f'''eep_probe_{key.replace('-', '_')} = {{
    name = "{name}"
    adjective = "EEP"
    ship_prefix = "EEP"
    spawn_enabled = no
    ignore_portrait_duplication = yes
    species = {{ class = "{klass}" portrait = "{portrait}" name = "EEP" plural = "EEP" adjective = "EEP" name_list = "HUMAN1" trait = "{trait}" }}
    room = "personality_purifier_room"
    authority = "{authority}"
    government = "{government}"
    origin = "{origin}"
    civics = {{ {' '.join('"'+c+'"' for c in civics)} }}
    planet_name = "EEP-Core"
    planet_class = "{planet}"
    system_name = "EEP-Throne"
    initializer = ""
    graphical_culture = "mammalian_01"
    city_graphical_culture = "mammalian_01"
    empire_flag = {{ icon = {{ category = "blocky" file = "flag_blocky_7.dds" }} background = {{ category = "backgrounds" file = "double_hemispheres.dds" }} colors = {{ "dark_grey" "purple" "null" "null" }} }}
    ruler = {{ name = "EEP" gender = female portrait = "{portrait}" texture = 0 attachment = 0 clothes = 0 leader_class = official }}
'''
        if authority == "auth_hive_mind":
            block = block.replace(f'trait = "{trait}"', f'trait = "{trait}" trait = "trait_hive_mind"')
        block += "\n".join(f'    ethic = "{ethic}"' for ethic in ethics) + "\n}\n"
        blocks.append(block)
    preset_file.write_text("\n".join(blocks), encoding="utf-8", newline="\n")
    (target / "fixture.json").write_text(json.dumps({"production": str(ROOT / "mod"), "fixture": str(ROOT / "testing/mod"), "created_at": stamp, "presets": [p[0] for p in PRESETS]}, indent=2) + "\n", encoding="utf-8")
    pointer = REPO / "_runtime/heart-of-devouring/current-fixture.json"
    pointer.write_text(json.dumps({"root": str(target)}) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
