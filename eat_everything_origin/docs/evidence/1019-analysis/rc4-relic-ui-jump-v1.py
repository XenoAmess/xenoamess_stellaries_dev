"""Read native archived SAVs and bind already captured GPU/OCR; never operates UI."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

PROJECT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(PROJECT / "tools"), str(PROJECT / "testing")]
import audit_save as a
import inspect_1015 as old
import inspect_1019 as n

RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z")
OUTPUT = Path(__file__).with_suffix(".json")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source(path):
    return {"path": str(path), "sha256": digest(path)}


def roots(path):
    with zipfile.ZipFile(path) as archive:
        text = archive.read("gamestate").decode("utf-8-sig")
    return {k: v for k, v, block in a.fields(text) if block}


def frame(stage):
    image, ocr = RUN / (stage + ".jpg"), RUN / (stage + ".ocr.json")
    data = json.loads(ocr.read_text(encoding="utf-8"))
    assert data["image_sha256"] == digest(image)
    return {"image": source(image), "ocr": source(ocr),
            "capture": data["capture"], "captured_at_utc": data["captured_at_utc"],
            "pid": data["pid"], "rows": data["rows"]}


def snapshot(stem):
    path = RUN / (stem + ".sav")
    observation = n.observe(path)
    raw = roots(path)
    fleets, systems = old.objects(raw["fleet"]), old.objects(raw["galactic_object"])
    country = a.block(raw["country"], "0")
    owned = set(re.findall(r"\bfleet\s*=\s*(\d+)", a.block(a.block(country, "fleets_manager"), "owned_fleets")))
    records = {}
    for role, fleet_id, ship_id in [("mother", "159", "997"), ("relic", "16777221", "16777223")]:
        f = observation["fleets_1019"][fleet_id]
        assert list(f["ships"]) == [ship_id]
        s = f["ships"][ship_id]
        order = a.block(fleets[fleet_id], "current_order")
        jump = a.block(order, "jumpdrive_order")
        windup = a.block(a.block(jump, "sub_order"), "jumpdrive_windup")
        records[role] = {"fleet_id": fleet_id, "ship_id": ship_id, "owned_by_country0": fleet_id in owned,
                         "design_name": s["design"]["name"], "design_body_sha256": s["design"]["body_sha256"],
                         "design_stages": s["design"]["stages"], "native": s["native"],
                         "coordinate": s["coordinate"], "movement_coordinate": f["movement"]["coordinate"],
                         "movement_native": f["movement"]["native"], "current_order_raw": order,
                         "jumpdrive_order_native": a.scalars(jump), "jumpdrive_windup_native": a.scalars(windup),
                         "last_ftl_jump_raw": a.block(f["movement"]["raw"], "last_ftl_jump"),
                         "fleet_variables": f["variables"], "ship_variables": s["variables"],
                         "fleet_modifiers": f["timed_modifier"]["items"], "ship_modifiers": s["timed_modifier"]["items"]}
    queue_bodies = old.objects(a.block(a.block(raw["construction"], "queue_mgr"), "queues"))
    queues = {identity: {"native": a.scalars(body), "location": a.scalars(a.block(body, "location")),
                         "items": a.ids(a.block(body, "items")), "body_sha256": hashlib.sha256(body.encode()).hexdigest()}
              for identity, body in queue_bodies.items() if a.scalars(body).get("owner") == 0}
    return {"date": observation["date"], "source": observation["provenance_1019"],
            "gamestate_sha256": observation["gamestate_sha256"], "country_native": observation["country"]["native"],
            "country_variables": observation["country_variables_all"], "records": records,
            "country0_queues": queues, "event_targets": observation["event_targets"],
            "systems": {identity: {"coordinate": a.scalars(a.block(systems[identity], "coordinate")),
                                   "name": a.scalars(a.block(systems[identity], "name")),
                                   "flags": a.scalars(a.block(systems[identity], "flags"))} for identity in ["8", "196"]},
            "legendary_flag_systems": [identity for identity, body in systems.items()
                                       if "legendary_leader_1st_system" in a.scalars(a.block(body, "flags"))]}


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    stages = {name: snapshot(name) for name in ["r4relic6", "r4jumpwind1", "r4jumpedge14"]}
    before, wind, arrived = (stages[k] for k in ["r4relic6", "r4jumpwind1", "r4jumpedge14"])
    wf, af = wind["records"]["mother"], arrived["records"]["mother"]
    checks = {
        "same_frozen_RC4": all(x["source"]["production_tree_sha256"] == "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468" for x in stages.values()),
        "native_dates_Mar13_Mar14_Mar27": [x["date"] for x in stages.values()] == ["2200.03.13", "2200.03.14", "2200.03.27"],
        "country_C0_preserved": all(x["country_variables"]["eep_c"] == 0 for x in stages.values()),
        "country_component_and_growth_ledger_preserved": all(x["country_variables"] == before["country_variables"] for x in stages.values()),
        "all_country0_queues_byte_equal": all(x["country0_queues"] == before["country0_queues"] for x in stages.values()),
        "all_country0_queues_empty": all(not q["items"] for x in stages.values() for q in x["country0_queues"].values()),
        "unique_original_destination_flag": all(x["legendary_flag_systems"] == ["196"] for x in stages.values()),
        "galactic_coordinates_unchanged": all(x["systems"][i]["coordinate"] == before["systems"][i]["coordinate"] for x in stages.values() for i in ["8", "196"]),
        "alias_targets_same_system196": all(x["systems"]["196"]["name"]["key"] == "EEP_JUMP_196" and
            len([t for t in x["event_targets"] if t["name"] == "eep_jump_destination_1019" and t["type"] == "galactic_object" and t["id"] == 196]) == 1
            for x in [wind, arrived]),
        "real_windup_from_system8_to196": wf["movement_coordinate"]["origin"] == 8 and wf["jumpdrive_order_native"].get("system") == 196 and
            wf["jumpdrive_windup_native"].get("can_reach") == "yes",
        "real_windup_dates_and_duration": wf["jumpdrive_windup_native"].get("windup_time") == 14 and
            wf["jumpdrive_windup_native"].get("start_date") == "2200.03.13" and wf["jumpdrive_windup_native"].get("end_date") == "2200.03.27",
        "same_mother_arrives_at196": af["coordinate"]["origin"] == 196 and af["movement_coordinate"]["origin"] == 196,
        "arrival_jump_order_completed": not af["current_order_raw"].strip(),
        "new_native_jump_cooldown_at_arrival": "jump_drive_cooldown" not in wf["native"] and af["native"].get("jump_drive_cooldown") == "yes" and
            af["native"].get("last_jump_date") == "2200.03.27",
        "relic_stays_at_origin8": all(x["records"]["relic"]["movement_coordinate"]["origin"] == 8 for x in stages.values()),
    }
    for role in ["mother", "relic"]:
        initial = before["records"][role]
        checks[role + "_owned_identity_preserved"] = all(x["records"][role]["owned_by_country0"] and
            all(x["records"][role][k] == initial[k] for k in ["fleet_id", "ship_id", "design_name", "design_body_sha256", "design_stages"]) for x in stages.values())
        checks[role + "_health_and_ledgers_preserved"] = all(all(x["records"][role]["native"][k] == initial["native"][k]
            for k in ["hitpoints", "armor_hitpoints", "shield_hitpoints", "max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints"]) and
            all(x["records"][role][k] == initial[k] for k in ["fleet_variables", "ship_variables", "fleet_modifiers", "ship_modifiers"]) for x in stages.values())
    frames = {stage: frame(stage) for stage in ["r4mother13-verified-details", "r4ref13-details", "r4mother13-details",
              "r4jump-vapob-search-result", "r4jump-vapob-pasted-result", "r4jump-edge-native-tooltip"]}
    report = {"schema": "eep.rc4_relic_ui_and_native_jump.v1", "status": "PASS_SCOPED" if all(checks.values()) else "FAIL",
              "scope": "same-country Mar13 visible ship configuration statistics and actual Mother jump8to196 with native cooldown; excludes maintenance, power, in-flight transient and cooldown expiry",
              "checks": checks, "stages": stages, "frames": frames,
              "manual_gpu_observations": {"mother": {"stage": "r4mother13-verified-details", "name": "白绮的裁决", "class": "白绮的裁决级主宰", "date": "2200.03.13", "hull": 93960, "armor": 44787, "shield": 167310, "speed": 417, "evasion_percent": 22.1, "damage_display": 5598.57},
                  "relic": {"stage": "r4ref13-details", "name": "EEP遗迹", "class": "遗迹级无畏战舰", "date": "2200.03.13", "hull": 20000, "armor": 30740, "shield": 138352, "speed": 225, "evasion_percent": 22.0, "damage_display": 2373.28},
                  "damage_unit": "native resource_time icon after slash; SHIP_STAT_DAMAGE_VALUE, main_2_l_simp_chinese.yml:1684",
                  "naval_capacity_HUD": "365/69", "maintenance_visible": False, "power_visible": False,
                  "failures": {"r4mother13-details": "system panorama; actual ship details never opened", "r4jump-vapob-search-result": "empty search edit after attempted Chinese typing", "r4jump-vapob-pasted-result": "empty search edit after attempted Unicode Ctrl+V"},
                  "arrival_tooltip": {"stage": "r4jump-edge-native-tooltip", "date": "2200.03.27", "cooldown_days_remaining": 200, "weapon_damage_penalty_percent": -50, "sublight_speed_penalty_percent": -50, "native_shortcut_display": "J"}},
              "tools": {name: source(PROJECT / subdir / name) for subdir, name in [("tools", "audit_save.py"), ("testing", "inspect_1015.py"), ("testing", "inspect_1019.py")]},
              "collector": source(Path(__file__)),
              "limitations": ["UI statistics are manual readings checked against original GPU frames and OCR, not newly executed UI.",
                  "Country capacity365 includes native Relic250; fixture economy is not a fresh-game budget.",
                  "Native last_ftl_jump still has old to13/jump_count sentinel. It is explicitly excluded from this jump proof.",
                  "No in_ftl field or independent transient in-flight sample was captured. Native windup, actual arrival and cooldown are verified.",
                  "No maintenance amount or power is visible in these configuration frames; both remain unverified.",
                  "No cooldown200-day expiry or long-range jump boundary was tested. No broad Mod acceptance claim."]}
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": report["status"], "checks": len(checks), "failures": [k for k, v in checks.items() if not v], "output": str(OUTPUT), "sha256": digest(OUTPUT)}))


if __name__ == "__main__":
    main()
