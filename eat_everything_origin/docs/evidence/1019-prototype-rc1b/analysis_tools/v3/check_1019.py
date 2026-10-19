"""Independent, read-only 1019 SAV checks; never a whole-Mod acceptance gate."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys
import zipfile

import audit_save as a
import check_single_homeworld as old

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "testing"))
import inspect_1019 as n

MOTHER_NAME = "NAME_EEP_Baiqi_Mothership"
DESIGN_NAME = "NAME_EEP_Baiqi_Mothership_1019"
EVOLUTION = "eep_mothership_evolution"
RECEIPT_FLAGS = ("eep_credit_done", "eep_return_done", "eep_population_done",
                 "eep_crisis_done", "eep_destroy_done")
ECONOMIC_VARIABLES = ("eep_c", "eep_g", "eep_d", "eep_made", "eep_worlds")


def result(checks, scope, **details):
    return {"status": "PASS_SCOPED" if all(checks.values()) else "FAIL",
            "scope": scope, "checks": checks, **details}


def mother_records(observation):
    return {identity: fleet for identity, fleet in observation["fleets_1019"].items()
            if fleet["name"] == MOTHER_NAME}


def design_shape(record):
    # Slot identity and required-component multiplicity matter. Serialization
    # ordering remains visible in the observations and strict raw differences.
    return [{"ship_size": stage["native"].get("ship_size"),
             "sections": sorted([
                 {"template": s["native"].get("template"), "slot": s["native"].get("slot"),
                  "components": sorted(s["components"], key=lambda c: json.dumps(c, sort_keys=True))}
                 for s in stage["sections"]], key=lambda s: json.dumps(s, sort_keys=True)),
             "required_components": sorted(stage["required_components"])} for stage in record["stages"]]


def mod_definition(observation, relative, key):
    manifest = json.loads(Path(observation["manifest"]).read_text(encoding="utf-8"))
    path = Path(manifest["copied_mod"]) / relative
    raw = path.read_text(encoding="utf-8-sig")
    body = a.block(raw, key)
    return {"path": str(path), "sha256": n.digest(path), "body": body}


def growth(observation, expected_c=None):
    values = observation["country"]["variables"]
    c = values.get("eep_c")
    if not isinstance(c, (int, float)) or not math.isfinite(c) or c < 0:
        raise ValueError("missing/invalid native settled matter eep_c")
    level = math.floor(c / 10)
    checks = {"candidate_0_4": str(observation["provenance_1019"]["version"]).startswith("0.4."),
              "native_country_level": values.get("eep_mothership_level") == level,
              "native_next_level_remainder": values.get("eep_mothership_next") == (level + 1) * 10 - c}
    if expected_c is not None:
        checks["expected_c"] = c == expected_c
    mothers = mother_records(observation)
    checks["unique_mothership"] = len(mothers) == 1
    multiplier_records = []
    for fleet in mothers.values():
        modifiers = [item for item in fleet["timed_modifier"]["items"] if item.get("modifier") == EVOLUTION]
        multiplier_records.extend(modifiers)
        checks["fleet_applied_level"] = fleet["variables"].get("eep_applied_level") == level
        checks["single_scaled_evolution_modifier"] = (
            len(modifiers) == (1 if level else 0) and
            (not level or modifiers[0].get("multiplier", 1) == level))
        checks["permanent_evolution_modifier"] = all(item.get("days") == -1 for item in modifiers)
        checks["no_ship_evolution_stacking"] = all(
            not any(item.get("modifier") == EVOLUTION for item in ship["timed_modifier"]["items"])
            for ship in fleet["ships"].values())
    definition = mod_definition(observation, "common/static_modifiers/eep_modifiers.txt", EVOLUTION)
    expected = {"ship_weapon_damage": .05, "ship_hull_mult": .05,
                "ship_armor_mult": .05, "ship_shield_mult": .05,
                "ship_hull_regen_add_static": .1, "ship_armor_regen_add_static": .1}
    checks["frozen_per_level_definition"] = a.scalars(definition["body"]) == expected
    return result(checks, "native country level, one fleet modifier and frozen per-level definition only",
                  c=c, level=level, next_level_remainder=(level + 1) * 10 - c,
                  multiplier_records=multiplier_records, frozen_definition=definition,
                  provenance=observation["provenance_1019"],
                  limitations=["Panel growth also depends on country modifiers.",
                               "Five-level real-component rewards are not certified by this check."])


def mother(observation):
    mothers = mother_records(observation)
    checks = {"candidate_0_4": str(observation["provenance_1019"]["version"]).startswith("0.4."),
              "unique_mothership_fleet": len(mothers) == 1,
              "one_mothership_ship": sum(len(f["ships"]) for f in mothers.values()) == 1}
    targets = [t for t in observation["event_targets"] if t["name"] == "eep_mothership0"]
    checks["unique_bound_native_fleet_target"] = len(targets) == 1 and str(targets[0]["id"]) in mothers
    definition = mod_definition(observation, "common/global_ship_designs/eep_mothership.txt", "ship_design")
    expected = n.design(definition["body"])
    readings = []
    for fleet_id, fleet in mothers.items():
        for ship_id, ship in fleet["ships"].items():
            native, actual = ship["native"], ship["design"]
            checks["new_native_design_name"] = actual["name"] == DESIGN_NAME
            checks["complete_native_loadout_matches_frozen_design"] = design_shape(actual) == design_shape(expected)
            components = [c for stage in actual["stages"] for section in stage["sections"]
                          for c in section["components"]]
            counts = Counter(c.get("template") for c in components)
            checks["relic_weapons_and_defenses"] = all(counts[key] == amount for key, amount in {
                "TITAN_LASER": 1, "LARGE_PLASMA_3": 7, "SMALL_DISRUPTOR_3": 2,
                "SMALL_PLASMA_3": 3, "POINT_DEFENCE_3": 3, "LARGE_ARMOR_5": 11,
                "LARGE_DARK_MATTER_DEFLECTOR": 11, "SHIELD_BOOSTER": 3, "AUTO_REPAIR": 2}.items())
            checks["native_planet_killer_component"] = counts["EEP_PLANET_KILLER_DEVOURER"] == 1
            required = [c for stage in actual["stages"] for c in stage["required_components"]]
            checks["native_jump_sensor_computer_and_dark_matter_propulsion"] = set((
                "JUMP_DRIVE_1", "SENSOR_4", "COMBAT_COMPUTER_LINE_SAPIENT",
                "JUGGERNAUT_DARK_MATTER_REACTOR", "COLOSSUS_SHIP_THRUSTER_5",
                "SHIP_AURA_INSPIRING_PRESENCE")).issubset(required)
            checks["retained_hull_minimum"] = native.get("max_hitpoints", 0) >= 93960
            checks["retained_armor_minimum"] = native.get("max_armor_hitpoints", 0) >= 24429.6
            checks["retained_shield_minimum"] = native.get("max_shield_hitpoints", 0) >= 48370.608
            yards = [b for b in observation["starbases_1019"].values()
                     if str(b["native"].get("station")) == ship_id]
            checks["one_mobile_starbase"] = len(yards) == 1
            checks["ten_mobile_shipyard_queue"] = len(yards) == 1 and observation["queues"].get(
                str(yards[0]["native"].get("shipyard_build_queue")), {}).get("simultaneous") == 10
            readings.append({"fleet_id": fleet_id, "ship_id": ship_id,
                             "native": native, "components": dict(counts), "required_components": required,
                             "design": actual, "starbases": yards})
    references = {k: v for k, v in observation["fleets_1019"].items() if v["name"] == "NAME_Relic"}
    return result(checks, "native Mother loadout, hull/armor/shield and ten-shipyard queue only",
                  provenance=observation["provenance_1019"], frozen_design=definition,
                  readings=readings, same_save_relic_fleets=references,
                  limitations=["Native jump action, power surplus, damage and speed need UI/runtime evidence.",
                               "A missing same-country Relic comparison remains outside this scoped result."])


def gameplay(observation):
    # Preserve the old strict gate's exact fields, then extend them. No ignored paths.
    result = old.gameplay_fields(observation)
    for key in ("fleets_1019", "starbases_1019", "worlds_1019", "crisis_progression_raw",
                "country_variables_all", "country_timed_modifier", "crisis_objectives", "crisis_levels"):
        result[key] = observation[key]
    for key in ("queues_1019", "construction_items_1019"):
        if key in observation:
            result[key] = observation[key]
    return result


def compare(before, after, require_same_date=True):
    differences = old.differences(gameplay(before), gameplay(after))
    checks = {"no_gameplay_differences": not differences}
    if require_same_date:
        checks["same_native_date"] = before["date"] == after["date"]
    return result(checks, "strict comparison of all old gameplay fields plus all 1019 observations; no ignored paths",
                  before=before["provenance_1019"], after=after["provenance_1019"],
                  before_date=before["date"], after_date=after["date"], differences=differences)


def value_delta(before, after, key):
    if key not in before or key not in after:
        raise ValueError("required native variable missing: " + key)
    return after[key] - before[key]


def capacity(world):
    items = [item for item in world["timed_modifier"]["items"] if item.get("modifier") == "eep_capacity"]
    if len(items) != 1:
        raise ValueError("expected exactly one native core capacity modifier")
    return items[0].get("multiplier", 1)


def settlement(case, before, after, reload_observation=None):
    if case.get("schema") != "eep.1019.settlement-case.v1" or case.get("path") not in ("normal", "colossus"):
        raise ValueError("explicit valid settlement schema and normal/colossus path required")
    core_id, source_id = str(case["core_world"]), str(case["source_world"])
    if core_id == source_id:
        raise ValueError("source cannot equal core")
    cb, ca = before["country"]["variables"], after["country"]["variables"]
    wb, wa = before["worlds_1019"][source_id], after["worlds_1019"][source_id]
    kb, ka = before["worlds_1019"][core_id], after["worlds_1019"][core_id]
    q = case["expected_q"]
    if not isinstance(q, (int, float)) or not math.isfinite(q) or q <= 0:
        raise ValueError("expected_q must be a finite positive number")
    native = case["native"]
    if not isinstance(native, bool):
        raise ValueError("native must be an explicit boolean")
    expected_return = case["expected_return"]
    other_pop_delta = case["expected_other_core_pop_delta"]
    c_delta, g_delta = value_delta(cb, ca, "eep_c"), value_delta(cb, ca, "eep_g")
    made_delta = value_delta(cb, ca, "eep_made")
    expected_g = 0 if native else q
    expected_made = math.floor((cb["eep_g"] + expected_g) / 6) * 100
    district_delta = capacity(ka) - capacity(kb)
    pop_delta = ka["actual_pop_sum"] - kb["actual_pop_sum"]
    damage = sum(deposit.get("type") == "d_lithoid_devastation" for deposit in wb["deposits"].values())
    checks = {"same_candidate_tree": before["production_tree_sha256"] == after["production_tree_sha256"],
              "candidate_0_4": str(after["provenance_1019"]["version"]).startswith("0.4."),
              "c_effective_matter_delta": c_delta == q,
              "g_ordinary_material_delta": g_delta == expected_g,
              "d_formula": ca["eep_d"] == 2 + math.floor(ca["eep_c"] / 4),
              "one_world_credit": value_delta(cb, ca, "eep_worlds") == 1,
              "manufactured_population_formula": ca["eep_made"] == expected_made,
              "manufactured_population_receipt": ca.get("eep_last_manufactured") == made_delta,
              "return_population_receipt": ca.get("eep_last_return") == expected_return,
              "core_population_delta": pop_delta == made_delta + expected_return + other_pop_delta,
              "core_capacity_matches_d": capacity(ka) == ca["eep_d"],
              "capacity_delta_matches_d_delta": district_delta == value_delta(cb, ca, "eep_d"),
              "capacity_receipt": ca.get("eep_last_capacity") == district_delta,
              "source_was_colonized": "colony" in wb["native"],
              "source_colony_destroyed": "colony" not in wa["native"],
              "real_shattered_planet_class": wa["native"].get("planet_class") == "pc_shattered",
              "no_previous_destroy_receipt": "eep_destroy_done" not in wb["flags"],
              "all_once_only_receipts": all(flag in wa["flags"] for flag in RECEIPT_FLAGS),
              "bound_core_keeps_owner": kb["native"].get("owner") == ka["native"].get("owner") == 0,
              "source_is_not_core": "eep_core" not in wb["flags"]}
    checks["source_q_receipt"] = wa["variables"].get("eep_q") == q
    if case["path"] == "normal":
        # q is frozen at task start. Native bites during its duration add damage
        # deposits, so subtracting current damage a second time would be wrong.
        checks["persisted_normal_task_q"] = wb["variables"].get("eep_q") == q
        checks["normal_source_owned_by_beneficiary"] = wb["native"].get("owner") == 0
        checks["normal_task_evidence"] = any(str(s.get("target", {}).get("id")) == source_id
                                             for s in before["situations"].values())
    else:
        checks["fresh_colossus_q_matches_live_size_less_damage"] = wb["native"].get("planet_size", 0) - damage == q
        checks["no_enemy_population_return"] = expected_return == 0 if wb["native"].get("owner") != 0 else True
    expected_crisis = case["expected_crisis_progress_delta"]
    if not isinstance(expected_crisis, (int, float)) or not math.isfinite(expected_crisis) or expected_crisis <= 0:
        raise ValueError("expected_crisis_progress_delta must be a finite positive calibrated reward")
    calibration = case.get("crisis_calibration_evidence")
    if not calibration or n.digest(Path(calibration["path"])) != calibration["sha256"]:
        raise ValueError("independent crisis reward calibration evidence missing or SHA changed")
    crisis_values = []
    for observation in (before, after):
        if observation["crisis_progression_native"].get("path") != "nemesis_path":
            raise ValueError("expected native Nemesis crisis progression path")
        objectives = [item for item in observation["crisis_objectives"]
                      if item.get("objective") == "crisobj_destroy_worlds"]
        if len(objectives) > 1:
            raise ValueError("duplicate native destroy-worlds objective records require investigation")
        crisis_values.append(objectives[0]["progress"] if objectives else 0)
    crisis_delta = crisis_values[1] - crisis_values[0]
    checks["one_calibrated_crisis_objective_reward"] = crisis_delta == expected_crisis
    strict_differences = old.differences(gameplay(before), gameplay(after))
    reload_check = no_settlement(case, after, reload_observation) if reload_observation else None
    if reload_check:
        checks["reload_does_not_pay_again"] = reload_check["status"] == "PASS_SCOPED"
    return result(checks, "explicit normal/colossus settlement math and persistent native result only; firing is separate",
                  path=case["path"], case=case, before=before["provenance_1019"], after=after["provenance_1019"],
                  actual={"q": c_delta, "g_delta": g_delta, "made_delta": made_delta,
                          "core_pop_delta": pop_delta, "capacity_delta": district_delta,
                          "crisis_progress_before_after": crisis_values, "crisis_progress_delta": crisis_delta,
                          "galaxy_system_count": before["galaxy_system_count"],
                          "native_habitability_setting": before["galaxy_native"].get("habitability")},
                  all_differences=strict_differences, reload_check=reload_check,
                  limitations=["This report alone does not prove native charge/fire, war targeting or absence of army."])


def no_settlement(case, before, after):
    core_id, source_id = str(case["core_world"]), str(case["source_world"])
    cb, ca = before["country"]["variables"], after["country"]["variables"]
    kb, ka = before["worlds_1019"][core_id], after["worlds_1019"][core_id]
    wb, wa = before["worlds_1019"][source_id], after["worlds_1019"][source_id]
    checks = {"same_native_date": before["date"] == after["date"],
              "same_candidate_tree": before["production_tree_sha256"] == after["production_tree_sha256"],
              "reward_variables_unchanged": all(key in cb and key in ca and cb[key] == ca[key] for key in ECONOMIC_VARIABLES),
              "core_population_unchanged": kb["actual_pop_sum"] == ka["actual_pop_sum"],
              "core_capacity_unchanged": capacity(kb) == capacity(ka),
              "source_class_unchanged": wb["native"].get("planet_class") == wa["native"].get("planet_class"),
              "source_colony_unchanged": wb["native"].get("colony") == wa["native"].get("colony"),
              "settlement_receipts_unchanged": all((flag in wb["flags"]) == (flag in wa["flags"]) for flag in RECEIPT_FLAGS),
              "crisis_progression_unchanged": before["crisis_progression_raw"] == after["crisis_progression_raw"]}
    return result(checks, "same-day no second settlement only; strict differences separately retained",
                  before=before["provenance_1019"], after=after["provenance_1019"],
                  strict_comparison=compare(before, after))


def damage_readings(ship):
    native = ship["native"]
    readings = {}
    for name, current, maximum in (("hull", "hitpoints", "max_hitpoints"),
                                    ("armor", "armor_hitpoints", "max_armor_hitpoints"),
                                    ("shield", "shield_hitpoints", "max_shield_hitpoints")):
        now, limit = native.get(current), native.get(maximum)
        if not isinstance(now, (int, float)) or not isinstance(limit, (int, float)):
            raise ValueError("native current/maximum defense missing: " + name)
        readings[name] = {"current_absolute": now, "maximum": limit, "lost_absolute": limit - now,
                          "fraction": now / limit if limit else None}
    return readings


def migration_snapshot(observation):
    mothers = mother_records(observation)
    if len(mothers) != 1:
        raise ValueError("migration requires one native Mother fleet")
    fleet_id, fleet = next(iter(mothers.items()))
    if len(fleet["ships"]) != 1:
        raise ValueError("migration requires one native Mother ship")
    ship_id, ship = next(iter(fleet["ships"].items()))
    yards = [(identity, base) for identity, base in observation["starbases_1019"].items()
             if str(base["native"].get("station")) == ship_id]
    if len(yards) != 1:
        raise ValueError("migration requires one attached native starbase")
    base_id, base = yards[0]
    queues = {identity: {k: v for k, v in queue.items() if k != "raw"}
              for identity, queue in observation["queues_1019"].items()}
    items = {}
    for identity, item in observation["construction_items_1019"].items():
        implementation = {k: v for k, v in item["ship_implementation"].items() if k != "design"}
        items[identity] = {"native": item["native"], "resources": item["resources"],
                           "orbitable": item["orbitable"], "implementation_except_design_index": implementation,
                           "queued_design": design_shape(item["queued_ship_design"]) if item["queued_ship_design"] else None,
                           "district": item["district"], "building": item["building"]}
    shipyard_queue_id = str(base["native"].get("shipyard_build_queue"))
    if shipyard_queue_id not in queues:
        raise ValueError("attached Mother shipyard queue absent from native observation")
    layout = {}
    for identity, world in observation["worlds"].items():
        colony = observation["colonies"].get(str(world.get("colony")), {})
        layout[identity] = {"planet": {k: world.get(k) for k in ("planet_class", "planet_size", "colony", "owner")},
                            "districts": {str(i): observation["districts"].get(str(i)) for i in colony.get("districts", [])},
                            "buildings": colony.get("buildings")}
    return {"fleet_id": fleet_id, "ship_id": ship_id, "starbase_id": base_id,
            "ship_name": ship["name"], "fleet_name": fleet["name"],
            "ship_coordinate": ship["coordinate"], "ship_target_coordinate": ship["target_coordinate"],
            "movement_coordinate": fleet["movement"]["coordinate"],
            "movement_target_coordinate": fleet["movement"]["target_coordinate"],
            "orbit_raw": fleet["movement"]["orbit_raw"], "design_name": ship["design"]["name"],
            "design_id": ship["design_id"], "design_body_sha256": ship["design"]["body_sha256"],
            "design_shape": design_shape(ship["design"]), "damage": damage_readings(ship),
            "build_queue_id": str(base["native"].get("build_queue")), "shipyard_queue_id": shipyard_queue_id,
            "all_owned_queues": queues, "all_owned_queue_items": items, "world_layout": layout,
            "owned_ship_inventory": sorted(key for f in observation["fleets_1019"].values() for key in f["ships"])}


def migration(case, before, after, reload_observation=None, fixture_observation=None):
    if case.get("schema") != "eep.1019.migration-case.v1":
        raise ValueError("explicit migration-case.v1 schema required")
    if case.get("require_damaged_before") is not True:
        raise ValueError("this migration check requires a genuinely damaged native before-save")
    mode = case["damage_mode"]
    metrics = case["damage_metrics"]
    tolerance = case.get("damage_tolerance", .001)
    if mode not in ("lost_absolute", "fraction", "current_absolute") or not metrics or any(
            key not in ("hull", "armor", "shield") for key in metrics):
        raise ValueError("explicit valid damage mode and metrics required")
    if not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("finite nonnegative damage tolerance required")
    b, a_ = migration_snapshot(before), migration_snapshot(after)
    if fixture_observation is None or fixture_observation["save_sha256"] != case["fixture_sha256"]:
        raise ValueError("verified original native fixture is required for migration")
    fixture = migration_snapshot(fixture_observation)
    mother_items = b["all_owned_queues"][b["shipyard_queue_id"]]["items"]
    cb, ca = before["country"], after["country"]
    checks = {"same_native_date": before["date"] == after["date"],
              "after_candidate_0_4": str(after["provenance_1019"]["version"]).startswith("0.4."),
              "expected_old_ship": b["ship_id"] == str(case["expected_ship_id"]),
              "expected_old_fleet": b["fleet_id"] == str(case["expected_fleet_id"]),
              "expected_old_starbase": b["starbase_id"] == str(case["expected_starbase_id"]),
              "expected_old_shipyard_queue": b["shipyard_queue_id"] == str(case["expected_shipyard_queue_id"]),
              "original_fixture_identity_binding": all(fixture[key] == b[key] for key in (
                  "fleet_id", "ship_id", "starbase_id", "ship_name", "shipyard_queue_id", "build_queue_id", "owned_ship_inventory")),
              "original_fixture_queue_members_binding": fixture["all_owned_queues"][fixture["shipyard_queue_id"]]["items"] == mother_items,
              "ship_identity_preserved": b["ship_id"] == a_["ship_id"],
              "fleet_identity_preserved": b["fleet_id"] == a_["fleet_id"],
              "starbase_identity_preserved": b["starbase_id"] == a_["starbase_id"],
              "all_owned_ships_preserved_without_duplication": b["owned_ship_inventory"] == a_["owned_ship_inventory"],
              "names_preserved": b["ship_name"] == a_["ship_name"] and b["fleet_name"] == a_["fleet_name"],
              "position_and_orbit_preserved": all(b[key] == a_[key] for key in (
                  "ship_coordinate", "ship_target_coordinate", "movement_coordinate", "movement_target_coordinate", "orbit_raw")),
              "new_native_design": a_["design_name"] == DESIGN_NAME,
              "real_design_transition": b["design_shape"] != a_["design_shape"],
              "genuinely_damaged_before": any(b["damage"][key]["lost_absolute"] > tolerance for key in metrics),
              "damaged_layers_remain_damaged": all(b["damage"][key]["lost_absolute"] <= tolerance or
                                                     a_["damage"][key]["lost_absolute"] > tolerance for key in metrics),
              "damage_preserved_in_declared_mode": all(b["damage"][key][mode] is not None and a_["damage"][key][mode] is not None
                  and math.isclose(b["damage"][key][mode], a_["damage"][key][mode], rel_tol=0, abs_tol=tolerance) for key in metrics),
              "queue_identifiers_preserved": b["build_queue_id"] == a_["build_queue_id"] and b["shipyard_queue_id"] == a_["shipyard_queue_id"],
              "all_owned_queues_preserved": b["all_owned_queues"] == a_["all_owned_queues"],
              "all_queue_costs_progress_designs_orbitables_preserved": b["all_owned_queue_items"] == a_["all_owned_queue_items"],
              "expected_mother_queue_count": len(mother_items) == case["expected_queued_items"],
              "nonempty_recorded_queue_costs_and_payer_before": bool(mother_items) and all(
                  b["all_owned_queue_items"][str(i)]["resources"] and
                  b["all_owned_queue_items"][str(i)]["native"].get("paying_country") == 0 for i in mother_items),
              "real_queue_progress_before": any(b["all_owned_queue_items"][str(i)]["native"].get("progress", 0) > 0 for i in mother_items),
              "no_additional_charge_or_refund": cb["stockpile"] == ca["stockpile"],
              "existing_layout_preserved": b["world_layout"] == a_["world_layout"],
              "existing_colonies_preserved": sorted(cb["owned_colonies"]) == sorted(ca["owned_colonies"]),
              "ledger_not_awarded_again": all(key in cb["variables"] and key in ca["variables"] and
                                             cb["variables"][key] == ca["variables"][key] for key in ECONOMIC_VARIABLES),
              "startup_flags_preserved": all((key in cb["flags"]) == (key in ca["flags"]) for key in (
                  "eep_initialized", "eep_startup_granted", "eep_mothership_granted", "eep_extra_world_granted", "eep_parallel_construction_granted"))}
    reload_report = None
    if reload_observation is not None:
        r = migration_snapshot(reload_observation)
        reload_checks = {"same_native_date": after["date"] == reload_observation["date"],
                         "same_candidate_tree": after["production_tree_sha256"] == reload_observation["production_tree_sha256"],
                         "migration_snapshot_preserved": a_ == r,
                         "ledger_preserved": all(ca["variables"].get(key) == reload_observation["country"]["variables"].get(key)
                                                 for key in ECONOMIC_VARIABLES),
                         "stockpile_preserved": ca["stockpile"] == reload_observation["country"]["stockpile"]}
        reload_report = result(reload_checks, "same-day native migration snapshot and ledger only",
                               snapshot=r, strict_comparison=compare(after, reload_observation))
        checks["reload_migration_snapshot_preserved"] = reload_report["status"] == "PASS_SCOPED"
    return result(checks, "damaged Mother identity, declared damage, layout and native paid-queue records only",
                  case=case, before=before["provenance_1019"], after=after["provenance_1019"],
                  original_fixture=fixture_observation["provenance_1019"], original_fixture_snapshot=fixture,
                  before_snapshot=b, after_snapshot=a_, damage_mode=mode, damage_metrics=metrics,
                  damage_tolerance=tolerance, all_differences=old.differences(gameplay(before), gameplay(after)),
                  reload_check=reload_report, limitations=[
                      "Stored resource costs/payer and preserved stockpile show no migration charge; original enqueue payment needs its original actions/audits.",
                      "An old 0.3.0-rc.1 queue fixture does not certify released 0.3.1 migration.",
                      "Scoped snapshot equality does not replace or overwrite strict raw comparison results."])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("observe", "mother", "growth"):
        command_parser = sub.add_parser(command)
        command_parser.add_argument("save", type=Path)
        command_parser.add_argument("--world", type=int, action="append", default=[])
        if command == "growth":
            command_parser.add_argument("--expected-c", type=float)
    comparison = sub.add_parser("compare")
    comparison.add_argument("before", type=Path)
    comparison.add_argument("after", type=Path)
    comparison.add_argument("--world", type=int, action="append", default=[])
    for command in ("settlement", "no-settlement", "migration"):
        sub.add_parser(command).add_argument("case", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("refusing to overwrite existing evidence: " + str(args.output))
    try:
        if args.command == "migration":
            case = json.loads(args.case.read_text(encoding="utf-8"))
            fixture = n.observe(Path(case["fixture_source"]))
            before, after = n.observe(Path(case["before"])), n.observe(Path(case["after"]))
            reload_obs = n.observe(Path(case["reload"])) if case.get("reload") else None
            report = migration(case, before, after, reload_obs, fixture)
            report["case_sha256"] = n.digest(args.case)
        elif args.command in ("settlement", "no-settlement"):
            case = json.loads(args.case.read_text(encoding="utf-8"))
            world_ids = (case["source_world"], case["core_world"])
            before = n.observe(Path(case["before"]), world_ids)
            after = n.observe(Path(case["after"]), world_ids)
            if args.command == "no-settlement":
                report = no_settlement(case, before, after)
            else:
                reload_obs = n.observe(Path(case["reload"]), world_ids) if case.get("reload") else None
                report = settlement(case, before, after, reload_obs)
            report["case_sha256"] = n.digest(args.case)
        elif args.command == "compare":
            before, after = n.observe(args.before, args.world), n.observe(args.after, args.world)
            report = compare(before, after)
        else:
            observation = n.observe(args.save, args.world)
            if args.command == "observe":
                report = observation
            elif args.command == "growth":
                report = growth(observation, args.expected_c)
            else:
                report = mother(observation)
    except (ValueError, KeyError, OSError, TypeError, zipfile.BadZipFile) as error:
        report = {"status": "FAIL", "scope": "native evidence/checker prerequisite",
                  "error_type": type(error).__name__, "error": str(error)}
    report["checker_sha256"] = n.digest(Path(__file__))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "output": str(args.output),
                      "checks": report.get("checks"), "error": report.get("error")}, ensure_ascii=False))
    return 0 if report["status"] in ("PASS_SCOPED", "OBSERVATION_ONLY") else 1


if __name__ == "__main__":
    raise SystemExit(main())
