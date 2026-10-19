"""Read-only native evidence extraction; observations never imply acceptance."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import audit_save as a


def objects(text):
    return {key: value for key, value, obj in a.fields(text) if obj}


def observe(save, manifest):
    data = a.audit(save, (0,))
    with zipfile.ZipFile(save) as archive:
        text = archive.read("gamestate").decode("utf-8-sig")
    provenance = json.loads(manifest.read_text(encoding="utf-8"))
    result = {
        "status": "OBSERVATION_ONLY",
        "save_sha256": data["save_sha256"], "date": data["date"],
        "manifest": str(manifest.resolve()),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "production_tree_sha256": provenance["repository_mod_tree_sha256"],
        "language": provenance["language"], "enabled_mods": provenance["enabled_mods"],
        "country": data["countries"]["0"],
        "worlds": data["planets"], "colonies": data["colonies"],
        "districts": data["districts"], "pop_groups": data["pop_groups"],
        "pop_jobs": data["pop_jobs"], "situations": data["situations"],
        "event_targets": data["event_targets"],
        "zones": {}, "queues": {}, "construction_items": {}, "fleets": {}, "starbases": {},
    }
    zones = objects(a.block(text, "zones"))
    for district in data["districts"].values():
        for identity in district["zones"]:
            if str(identity) in zones:
                result["zones"][str(identity)] = a.scalars(zones[str(identity)])
    ships = objects(a.block(text, "ships"))
    all_fleets = objects(a.block(text, "fleet"))
    country = a.block(a.block(text, "country"), "0")
    progression = a.block(country, "crisis_progression")
    result["crisis_progression"] = {
        "native": a.scalars(progression), "raw": progression,
    }
    owned = a.block(a.block(country, "fleets_manager"), "owned_fleets")
    owned_fleets = {int(value) for value in re.findall(r"\bfleet\s*=\s*(\d+)", owned)}
    starbase_queue_ids = set()
    for identity, value in objects(a.block(a.block(text, "starbase_mgr"), "starbases")).items():
        record = a.scalars(value)
        station = ships[str(record["station"])]
        station_record = a.scalars(station)
        if station_record["fleet"] not in owned_fleets:
            continue
        record["station_native"] = station_record
        record["modules"] = a.scalars(a.block(value, "modules"))
        record["buildings"] = a.scalars(a.block(value, "buildings"))
        result["starbases"][identity] = record
        starbase_queue_ids.update(str(record[k]) for k in ("build_queue", "shipyard_build_queue"))
    construction = a.block(text, "construction")
    queue_data = a.block(a.block(construction, "queue_mgr"), "queues")
    world_ids = {int(key) for key in data["planets"]}
    item_ids = set()
    for identity, value in objects(queue_data).items():
        record = a.scalars(value)
        location = a.scalars(a.block(value, "location"))
        is_world_queue = record.get("type") == "planet" and location.get("id") in world_ids
        if record.get("owner") == 0 and (is_world_queue or identity in starbase_queue_ids):
            record["location"] = location
            record["items"] = a.ids(a.block(value, "items"))
            item_ids.update(str(i) for i in record["items"])
            result["queues"][identity] = record
    for identity, value in objects(a.block(a.block(construction, "item_mgr"), "items")).items():
        if identity in item_ids:
            result["construction_items"][identity] = {
                "native": a.scalars(value), "resources": a.scalars(a.block(value, "resources")),
                "district": a.scalars(a.block(value, "buildable_district")),
                "building": a.scalars(a.block(value, "buildable_building")),
                "ship": a.scalars(a.block(value, "buildable_ship")),
                "raw": value,
            }
    designs = objects(a.block(text, "ship_design"))
    for identity, value in all_fleets.items():
        name = a.scalars(a.block(value, "name")).get("key")
        if name not in ("NAME_EEP_Baiqi_Mothership", "1015 Gray Control"):
            continue
        record = {"name": name, "native": a.scalars(value), "settings": a.scalars(a.block(value, "settings")), "ships": {}}
        for ship_id in a.ids(a.block(value, "ships")):
            ship = ships[str(ship_id)]
            design = a.scalars(a.block(ship, "ship_design_implementation"))["design"]
            design_text = designs[str(design)]
            record["ships"][str(ship_id)] = {
                "native": a.scalars(ship), "modifiers": a.block(ship, "timed_modifier"),
                "design_id": design, "design": a.scalars(design_text),
                "design_name": a.scalars(a.block(design_text, "name")).get("key"),
            }
        result["fleets"][identity] = record
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = observe(args.save, args.manifest or args.save.parent / "manifest.json")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": report["status"], "date": report["date"], "worlds": len(report["worlds"]), "fleets": len(report["fleets"]), "queues": report["queues"]}))
