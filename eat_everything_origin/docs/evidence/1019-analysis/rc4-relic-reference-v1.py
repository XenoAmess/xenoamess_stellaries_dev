"""Read-only r4relic0 reference analysis; no UI or production acceptance claim."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

PROJECT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(PROJECT / "tools"), str(PROJECT / "testing")]
import audit_save as a
import inspect_1015
import inspect_1019 as n
import check_single_homeworld

RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z")
OUTPUT = Path(__file__).with_suffix(".json")


def raw_database(save):
    with zipfile.ZipFile(save) as archive:
        data = archive.read("gamestate")
    roots = {key: value for key, value, block in a.fields(data.decode("utf-8-sig")) if block}
    fleets, ships = inspect_1015.objects(roots["fleet"]), inspect_1015.objects(roots["ships"])
    country = a.block(roots["country"], "0")
    owned = set(re.findall(r"\bfleet\s*=\s*(\d+)", a.block(a.block(country, "fleets_manager"), "owned_fleets")))
    membership = {identity: [str(i) for i in a.ids(a.block(fleets[identity], "ships"))] for identity in owned}
    return {"gamestate_sha256": hashlib.sha256(data).hexdigest(), "fleets": fleets, "ships": ships,
            "owned": owned, "membership": membership, "owned_ships": {i for members in membership.values() for i in members}}


def shape(design):
    return [{"ship_size": stage["native"].get("ship_size"), "sections": [{
        "template": section["native"].get("template"), "slot": section["native"].get("slot"),
        "components": sorted(section["components"], key=lambda c: c["slot"])} for section in stage["sections"]],
        "required": sorted(stage["required_components"])} for stage in design["stages"]]


def slots(design):
    return {component["slot"]: component["template"] for stage in design["stages"]
            for section in stage["sections"] for component in section["components"]}


def main():
    if OUTPUT.exists():
        raise FileExistsError("refusing to overwrite independent evidence: " + str(OUTPUT))
    before_path, after_path = RUN / "pk2base.sav", RUN / "r4relic0.sav"
    before, after = n.observe(before_path), n.observe(after_path)
    braw, araw = raw_database(before_path), raw_database(after_path)
    manifest = json.loads((RUN / "manifest.json").read_text(encoding="utf-8"))
    mod, game = Path(manifest["copied_mod"]), Path(manifest["game_exe"]).parent
    source_paths = {"mother_design": mod / "common/global_ship_designs/eep_mothership.txt",
                    "relic_design": game / "common/global_ship_designs/leviathans_designs.txt",
                    "mother_modifiers": mod / "common/static_modifiers/eep_modifiers.txt",
                    "relic_chassis": game / "common/ship_sizes/11_leviathans.txt",
                    "mother_names": mod / "localisation/simp_chinese/eep_l_simp_chinese.yml",
                    "relic_names": game / "localisation/simp_chinese/name_lists/ship_design_names_l_simp_chinese.yml",
                    "name_format": game / "localisation/simp_chinese/name_system_l_simp_chinese.yml"}
    source_text = {key: path.read_text(encoding="utf-8-sig") for key, path in source_paths.items()}
    locale = {}
    for key in ("mother_names", "relic_names", "name_format"):
        for match in re.finditer(r'^\s+([^:\s]+):\d*\s+"((?:[^"\\]|\\.)*)"', source_text[key], re.MULTILINE):
            locale[match[1]] = match[2]
    def name_record(body):
        key = a.scalars(body).get("key")
        variables = {a.scalars(v)["key"]: name_record(a.block(v, "value"))
                     for v in n.anonymous_blocks(a.block(body, "variables"))}
        rendered = locale.get(key, key)
        if isinstance(rendered, str):
            for name, value in variables.items():
                rendered = rendered.replace("$" + name + "$", value["source_resolved_name"])
        return {"key": key, "variables": variables, "source_resolved_name": rendered, "ui_verified": False}
    def design_definition(text, name):
        body = next(body for key, body, block in a.fields(text)
                    if key == "ship_design" and block and a.scalars(body).get("name") == name)
        return n.design(body)
    expected_mother = design_definition(source_text["mother_design"], "NAME_EEP_Baiqi_Mothership_1019")
    expected_relic = design_definition(source_text["relic_design"], "NAME_Relic")
    def target(observation, name):
        matches = [t for t in observation["event_targets"] if t["name"] == name]
        if len(matches) != 1 or matches[0]["type"] != "fleet":
            raise ValueError("requires one actual fleet target: " + name)
        return str(matches[0]["id"])
    mother_id, relic_id = target(after, "eep_mothership0"), target(after, "eep_relic_reference_1019")
    def snapshot(fleet_id):
        fleet = after["fleets_1019"][fleet_id]
        if len(fleet["ships"]) != 1:
            raise ValueError("one actual ship per reference fleet required")
        ship_id, ship = next(iter(fleet["ships"].items()))
        return {"fleet_id": fleet_id, "ship_id": ship_id, "owned_by_country0": fleet_id in araw["owned"],
                "fleet_name": name_record(a.block(araw["fleets"][fleet_id], "name")),
                "ship_name": name_record(a.block(ship["raw"], "name")), "ship_native": ship["native"],
                "fleet_native": fleet["native"], "design_name": ship["design"]["name"], "design_id": ship["design_id"],
                "design_body_sha256": ship["design"]["body_sha256"], "design_shape": shape(ship["design"]),
                "slots": slots(ship["design"]), "component_count": sum(len(s["components"]) for t in ship["design"]["stages"] for s in t["sections"]),
                "required": [c for t in ship["design"]["stages"] for c in t["required_components"]],
                "fleet_variables": fleet["variables"], "ship_variables": ship["variables"],
                "fleet_timed_modifiers": fleet["timed_modifier"]["items"], "ship_timed_modifiers": ship["timed_modifier"]["items"],
                "ship_aura_modifier": a.scalars(a.block(ship["raw"], "aura_modifier")),
                "ship_auras": [{"id": a.scalars(a.block(v, "id")), "source": a.scalars(a.block(v, "source"))}
                               for v in n.anonymous_blocks(a.block(ship["raw"], "auras"))],
                "fleet_movement": {"native": fleet["movement"]["native"], "coordinate": fleet["movement"]["coordinate"]},
                "ship_coordinate": ship["coordinate"],
                "direct_native_damage_or_upkeep_fields": {k: v for k, v in ship["native"].items() if re.search("damage|dps|upkeep|fire_rate", k)}}
    mother, relic = snapshot(mother_id), snapshot(relic_id)
    added_fleets = sorted(araw["fleets"].keys() - braw["fleets"].keys())
    added_ships = sorted(araw["ships"].keys() - braw["ships"].keys())
    removed_fleets = sorted(braw["fleets"].keys() - araw["fleets"].keys())
    removed_ships = sorted(braw["ships"].keys() - araw["ships"].keys())
    shared_slot_differences = {slot: {"mother": mother["slots"].get(slot), "relic": component}
                               for slot, component in relic["slots"].items() if mother["slots"].get(slot) != component}
    defense = {layer: {"mother_current": mother["ship_native"][current], "mother_maximum": mother["ship_native"][maximum],
                       "relic_current": relic["ship_native"][current], "relic_maximum": relic["ship_native"][maximum]}
               for layer, current, maximum in (("hull", "hitpoints", "max_hitpoints"),
                   ("armor", "armor_hitpoints", "max_armor_hitpoints"), ("shield", "shield_hitpoints", "max_shield_hitpoints"))}
    checks = {"original_before_sha": before["save_sha256"] == "be5a344439dafe105d4959b4afa31143331b1daaaf915dba28bc70ee23f6f2e2",
              "same_native_date": before["date"] == after["date"] == "2200.03.07",
              "same_frozen_candidate": before["production_tree_sha256"] == after["production_tree_sha256"] == "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468",
              "matter_C0_before_and_after": before["country"]["variables"]["eep_c"] == after["country"]["variables"]["eep_c"] == 0,
              "mother_identity_preserved": target(before, "eep_mothership0") == mother_id == "159" and mother["ship_id"] == "997",
              "one_new_global_fleet_only": added_fleets == [relic_id] and not removed_fleets,
              "one_new_global_ship_only": added_ships == [relic["ship_id"]] and not removed_ships,
              "one_new_country0_fleet_only": araw["owned"] - braw["owned"] == {relic_id} and not braw["owned"] - araw["owned"],
              "one_new_country0_ship_only": araw["owned_ships"] - braw["owned_ships"] == {relic["ship_id"]} and not braw["owned_ships"] - araw["owned_ships"],
              "all_existing_country0_fleet_members_preserved": all(araw["membership"][fid] == members for fid, members in braw["membership"].items()),
              "relic_reference_owned_by_country0": relic["owned_by_country0"],
              "mother_50_components_six_required": mother["component_count"] == len(mother["slots"]) == 50 and len(mother["required"]) == 6,
              "relic_43_components_six_required": relic["component_count"] == len(relic["slots"]) == 43 and len(relic["required"]) == 6,
              "actual_mother_design_matches_frozen_source": mother["design_shape"] == shape(expected_mother),
              "actual_relic_design_matches_native_source": relic["design_shape"] == shape(expected_relic),
              "all_43_relic_slots_retained_on_mother": not shared_slot_differences,
              "mother_native_maxima_at_least_relic": all(d["mother_maximum"] >= d["relic_maximum"] for d in defense.values())}
    report = {"schema": "eep.1019.native-relic-reference.v1", "status": "PASS_SCOPED" if all(checks.values()) else "FAIL",
        "scope": "same-day country0 entity/design/defense reference only; not UI DPS, maintenance or whole-Mod acceptance",
        "checks": checks, "before": before["provenance_1019"], "after": after["provenance_1019"],
        "before_gamestate_sha256": braw["gamestate_sha256"], "after_gamestate_sha256": araw["gamestate_sha256"],
        "mother": mother, "relic": relic, "defenses": defense,
        "extra_mother_slots": {key: value for key, value in mother["slots"].items() if key not in relic["slots"]},
        "shared_slot_differences": shared_slot_differences,
        "required_common": sorted(set(mother["required"]) & set(relic["required"])),
        "mother_only_required": sorted(set(mother["required"]) - set(relic["required"])),
        "relic_only_required": sorted(set(relic["required"]) - set(mother["required"])),
        "entity_delta": {"added_fleets": added_fleets, "added_ships": added_ships, "removed_fleets": removed_fleets, "removed_ships": removed_ships},
        "existing_raw_changed_fleets": sorted(i for i in braw["fleets"].keys() & araw["fleets"].keys() if braw["fleets"][i] != araw["fleets"][i]),
        "existing_raw_changed_ships": sorted(i for i in braw["ships"].keys() & araw["ships"].keys() if braw["ships"][i] != araw["ships"][i]),
        "country_before": {key: before["country"][key] for key in ("native", "stockpile", "variables")},
        "country_after": {key: after["country"][key] for key in ("native", "stockpile", "variables")},
        "source_chassis_modifiers_not_runtime_exports": a.scalars(a.block(a.block(source_text["relic_chassis"], "npc_warship_01"), "modifier")),
        "source_mother_fleet_modifier_not_runtime_export": a.scalars(a.block(source_text["mother_modifiers"], "eep_mothership")),
        "sources": {key: {"path": str(path), "sha256": n.digest(path)} for key, path in source_paths.items()},
        "tools": {Path(module.__file__).name: {"path": str(Path(module.__file__).resolve()), "sha256": n.digest(module.__file__)}
                  for module in (a, inspect_1015, n, check_single_homeworld)},
        "analysis_source_sha256": n.digest(Path(__file__)),
        "limitations": ["Name rendering is reconstructed from native name records and exact Chinese localization; UI was not inspected.",
            "No direct native ship DPS/damage/upkeep amount fields were synthesized from military power or design values.",
            "Stored native used_naval_capacity is reported as cached at this same-day save; no refresh or final monthly maintenance claim.",
            "The reference was console-created for a separate feature fixture and cannot certify natural construction costs or startup economy.",
            "Source modifier definitions are separated from actual stored timed/aura state and are not aggregate runtime modifier exports."]}
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "output": str(OUTPUT), "checks": checks,
                      "mother_name": mother["ship_name"]["source_resolved_name"], "relic_name": relic["ship_name"]["source_resolved_name"],
                      "entity_delta": report["entity_delta"]}, ensure_ascii=True))


if __name__ == "__main__":
    main()
