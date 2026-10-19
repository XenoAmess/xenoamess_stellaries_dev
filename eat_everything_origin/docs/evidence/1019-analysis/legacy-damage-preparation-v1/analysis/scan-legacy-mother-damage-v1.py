"""Read-only native Mother damage inventory for completed old source runs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT / "tools"))
import audit_save as a
import check_1019 as c

ARTIFACTS = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts")


def root(text, key):
    match = re.search(r"(?m)^" + re.escape(key) + r"\s*=\s*\{", text)
    if not match:
        raise ValueError("native root absent: " + key)
    return a.block(text[match.start():], key)


def scan(save):
    row = {"save": str(save), "status": "UNVERIFIED"}
    try:
        manifest, proof = c.n.provenance(save)
        row["provenance"] = proof
        audit = json.loads(save.with_suffix(".audit.json").read_text(encoding="utf-8"))
        with zipfile.ZipFile(save) as archive:
            assert archive.testzip() is None
            data = archive.read("gamestate")
        assert hashlib.sha256(data).hexdigest() == audit["gamestate_sha256"]
        text = data.decode("utf-8-sig")
        targets = [target for target in audit["event_targets"] if target["name"] == "eep_mothership0"]
        if len(targets) != 1:
            raise ValueError("one native Mother fleet target required")
        fleet_id = str(targets[0]["id"])
        fleet = a.block(root(text, "fleet"), fleet_id)
        assert a.scalars(a.block(fleet, "name")).get("key") == c.MOTHER_NAME
        ship_ids = a.ids(a.block(fleet, "ships"))
        if len(ship_ids) != 1:
            raise ValueError("one native Mother ship required")
        ship_id = str(ship_ids[0])
        native = a.scalars(a.block(root(text, "ships"), ship_id))
        readings = {}
        for name, current, maximum in (("hull", "hitpoints", "max_hitpoints"),
                                        ("armor", "armor_hitpoints", "max_armor_hitpoints"),
                                        ("shield", "shield_hitpoints", "max_shield_hitpoints")):
            assert isinstance(native.get(current), (int, float))
            assert isinstance(native.get(maximum), (int, float))
            readings[name] = {"current": native[current], "maximum": native[maximum],
                              "lost_absolute": native[maximum] - native[current],
                              "fraction": native[current] / native[maximum] if native[maximum] else None}
        row.update(status="OBSERVATION_ONLY", date=audit["date"], fleet_id=fleet_id, ship_id=ship_id,
                   mother_native=native, defense=readings,
                   genuinely_damaged_layers=[key for key, value in readings.items() if value["lost_absolute"] > .001],
                   public031_source=proof["version"] == "0.3.1",
                   corresponding_paid_source=proof["production_tree_sha256"] == "83e85b96dc407396a58eceb192b5a28493053df129c272dcb28da6ee286a6fa2")
    except Exception as error:
        row.update(error_type=type(error).__name__, error=str(error))
    return row


def main():
    saves = []
    manifests = []
    for name in ("single-homeworld-20261019", "1015-implementation"):
        for path in sorted((ARTIFACTS / name / "runs").glob("*/manifest.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            descriptor = Path(manifest["copied_mod"]) / "descriptor.mod"
            version = a.scalars(descriptor.read_text(encoding="utf-8-sig"))["version"]
            if version in ("0.3.1", "0.3.0-rc.1"):
                candidates = sorted(path.parent.glob("*.sav"))
                saves.extend(candidates)
                manifests.append({"path": str(path), "sha256": c.n.digest(path), "version": version,
                                  "saves": len(candidates), "tree": manifest["repository_mod_tree_sha256"]})
    with ThreadPoolExecutor(max_workers=2) as executor:
        rows = list(executor.map(scan, saves))
    verified = [row for row in rows if row["status"] == "OBSERVATION_ONLY"]
    damaged = [row for row in verified if row["genuinely_damaged_layers"]]
    report = {"schema": "eep.1019.legacy-native-mother-damage-inventory.v1", "status": "OBSERVATION_ONLY",
              "scope": "Completed old-version native SAVs in explicit 1015 implementation and 1019 single-homeworld runs only",
              "scanner_sha256": c.n.digest(Path(__file__)), "checker_sha256": c.n.digest(Path(c.__file__)),
              "manifests": manifests, "records": rows,
              "summary": {"native_saves_examined": len(rows), "native_provenance_verified": len(verified),
                          "unverified": len(rows) - len(verified), "damaged_mother_saves": len(damaged),
                          "public031_saves": sum(row.get("public031_source", False) for row in verified),
                          "public031_damaged": sum(row.get("public031_source", False) for row in damaged),
                          "corresponding_paid_saves": sum(row.get("corresponding_paid_source", False) for row in verified),
                          "corresponding_paid_damaged": sum(row.get("corresponding_paid_source", False) for row in damaged)},
              "limitations": ["No whole-disk absence claim; old campaign saves and current 0.4 prototypes are outside this legacy-source scope.",
                              "Missing provenance is reported UNVERIFIED and never silently accepted.",
                              "No UI action, Mod mutation, original SAV mutation, or future damaged fixture is performed."]}
    output = Path(__file__).with_name("legacy-native-mother-damage-inventory-v1.json")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"output": str(output), "summary": report["summary"], "sha256": c.n.digest(output)}))


if __name__ == "__main__":
    main()
