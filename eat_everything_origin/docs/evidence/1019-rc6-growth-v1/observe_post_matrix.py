"""Read fixed post-matrix SAV fields with the frozen native parser only."""
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PARSER = ROOT / "docs/evidence/1019-rc6-migration-checkpoint-v1/source-tools/eat_everything_origin/tools/audit_save.py"
spec = importlib.util.spec_from_file_location("rc6_frozen_native_parser", PARSER)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
KINDS = ("shield", "armor", "hull", "damage", "tracking", "regen")
HEALTH = ("hitpoints", "max_hitpoints", "armor_hitpoints", "max_armor_hitpoints", "shield_hitpoints", "max_shield_hitpoints")


def digest(path): return sha256(path.read_bytes()).hexdigest()
def ref(path): return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}
def read(path): return json.loads(path.read_text(encoding="utf-8"))


def extract(prefix):
    path = OUT / "run" / (prefix + ".sav")
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        raw = archive.read("gamestate")
    roots = list(a.fields(raw.decode("utf-8-sig")))
    objects = {key: body for key, body, obj in roots if obj}
    targets = [a.scalars(body) for key, body, obj in roots if key == "saved_event_target" and obj and a.scalars(body).get("name") == "eep_mothership0"]
    assert len(targets) == 1
    fleet_id = targets[0]["id"]
    fleet = a.block(objects["fleet"], str(fleet_id))
    ships = a.ids(a.block(fleet, "ships"))
    assert fleet_id == 125 and ships == [809]
    country = a.block(objects["country"], "0")
    ship = a.block(objects["ships"], "809")
    ship_data = a.scalars(ship)
    assert ship_data["fleet"] == 125
    cvar = a.scalars(a.block(country, "variables"))
    fvar = a.scalars(a.block(fleet, "variables"))
    design_id = a.scalars(a.block(ship, "ship_design_implementation"))["design"]
    design = a.block(objects["ship_design"], str(design_id))
    tiers = {k: fvar["eep_component_" + k + "_level"] for k in KINDS}
    assert all(cvar["eep_component_" + k + "_level"] == value for k, value in tiers.items())
    return {"save": ref(path), "gamestate_sha256": sha256(raw).hexdigest(),
        "date": next(a.unquote(body) for key, body, obj in roots if key == "date" and not obj),
        "country": 0, "fleet": fleet_id, "ship": 809, "tiers": tiers,
        "country_variables": cvar, "fleet_variables": fvar,
        "ship_variables": a.scalars(a.block(ship, "variables")),
        "health": {k: ship_data.get(k) for k in HEALTH},
        "design_id": design_id, "design_body_sha256": sha256(design.encode()).hexdigest(),
        "government_raw_sha256": sha256(a.block(country, "government").encode()).hexdigest()}


def main():
    assert not (OUT / "post-matrix-observation-v1.json").exists()
    names = ("r6g-n08-c10000-final", "r6grepeat", "r6greload", "r6gexport1", "r6gbudget1")
    actual = {}
    for prefix in names:
        actual[prefix] = extract(prefix)
        print(json.dumps({"extracted": prefix, "date": actual[prefix]["date"]}), flush=True)
    repeat = actual["r6grepeat"]
    reload = actual["r6greload"]
    export = actual["r6gexport1"]
    budget = actual["r6gbudget1"]
    c0 = read(OUT / "authored/rc6-growth-pair-n00-c0-observation-v1.json")["actual_final"]["modifier_exports"]
    level = export["country_variables"]["eep_mothership_level"]
    expected = dict(c0)
    for field, tier in (("ship_hull_mult", "hull"), ("ship_armor_mult", "armor"), ("ship_shield_mult", "shield")):
        expected[field] += .05 * level + .1 * export["tiers"][tier]
    expected["ship_weapon_damage"] += .05 * level + .05 * export["tiers"]["damage"]
    expected["ship_tracking_add"] += 3 * export["tiers"]["tracking"]
    for field in ("ship_hull_regen_add_static", "ship_armor_regen_add_static"):
        expected[field] += .1 * level + .2 * export["tiers"]["regen"]
    comparisons = [{"field": field, "observed": export["ship_variables"]["eep_probe_" + field], "expected": value,
        "absolute_tolerance": .01, "relative_tolerance": 0,
        "passed": abs(export["ship_variables"]["eep_probe_" + field] - value) <= .01} for field, value in expected.items()]
    assert len(comparisons) == 10 and all(row["passed"] for row in comparisons)
    r_before = export["country_variables"]["eep_component_rewards"]
    r_after = budget["country_variables"]["eep_component_rewards"]
    entitlement = budget["country_variables"]["eep_component_entitled"]
    pending = budget["country_variables"]["eep_component_pending"]
    intended_R = r_before + min(max(entitlement - r_before, 0), 200)
    intended_P = max(entitlement - intended_R, 0)
    assert (r_before, r_after, entitlement, pending, intended_R, intended_P) == (200, 300, 410, 110, 400, 10)
    same_fields = ("date", "country_variables", "fleet_variables", "ship_variables", "health", "design_id", "design_body_sha256", "government_raw_sha256")
    repeat_reload = {field: {"equal": repeat[field] == reload[field], "before": repeat[field], "after": reload[field]}
                     for field in same_fields}
    data = {"schema": "eep.rc6.archived-post-matrix-native-observation.v1",
        "status": "OBSERVATIONS_WITH_CONFIRMED_ORIGINAL_EXPORT_AND_SINGLE_SYNC_FAILURES",
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "archive_index": ref(OUT / "index.json"),
        "parser": ref(PARSER), "extractor": ref(Path(__file__).resolve()), "raw": actual,
        "n08_original_seven_export_failures_retained": True,
        "repeat_ZIP_equals_original_n08_final": (OUT / "run/r6grepeat.sav").read_bytes() == (OUT / "run/r6g-n08-c10000-final.sav").read_bytes(),
        "repeat_reload_selected_fields": repeat_reload,
        "repeat_reload_ZIP_equal": (OUT / "run/r6grepeat.sav").read_bytes() == (OUT / "run/r6greload.sav").read_bytes(),
        "reload_receipt": ref(OUT / "run/r6gload.load.json"),
        "reload_load_helper_state_verified": read(OUT / "run/r6gload.load.json")["state_verified"],
        "later_reexport_10_channels": comparisons,
        "single_sync_budget": {"status": "FAIL", "R_before": r_before, "actual_R": r_after, "actual_gain": r_after - r_before,
            "actual_pending": pending, "entitlement": entitlement, "intended_gain": 200, "expected_R": intended_R, "expected_pending": intended_P,
            "country_C": budget["country_variables"]["eep_c"], "six_tiers_sum": sum(budget["tiers"].values())},
        "limits": ["Later reexport is a different native sample and does not replace the original failed exports.",
            "Selected-field repeat/reload observations do not certify complete gameplay invariance or load callbacks.",
            "The original helper verified native load date but explicitly left state_verified false; new-save extraction is separate.",
            "Inference R104 remains a cache hypothesis, not a recorded intermediate ledger.",
            "No RC7, final logs, GUI, production, root tools or historical files modified; no growth or Mod PASS."]}
    with (OUT / "post-matrix-observation-v1.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": data["status"], "path": str(OUT / "post-matrix-observation-v1.json"),
        "sha256": digest(OUT / "post-matrix-observation-v1.json"), "repeat_reload_ZIP_equal": data["repeat_reload_ZIP_equal"],
        "selected_differences": [k for k, v in repeat_reload.items() if not v["equal"]]}))


if __name__ == "__main__": main()
