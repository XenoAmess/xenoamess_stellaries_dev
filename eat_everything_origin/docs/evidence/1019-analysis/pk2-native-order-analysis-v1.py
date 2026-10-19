"""Read-only analysis of completed RC4 PK2 native observations and their SAVs.

This is a fixture report collector, not a Stellaris trigger interpreter.
Run from any directory; all output files are exclusively created.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT / "tools"))
import check_1019 as c


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def day(date):
    year, month, day_ = map(int, date.split("."))
    return year * 360 + (month - 1) * 30 + day_ - 1


def children(body, path=""):
    rows = []
    for key, value, obj in c.a.fields(body):
        if obj:
            node = path + "." + key if path else key
            rows.append({"path": node, "native": c.a.scalars(value), "raw": value})
            rows.extend(children(value, node))
    return rows


def load(path):
    path = Path(path)
    observation = json.loads(path.read_text(encoding="utf-8"))
    save = Path(observation["provenance_1019"]["save"])
    manifest, provenance = c.n.provenance(save)
    assert digest(save) == observation["save_sha256"] == provenance["save_sha256"]
    with zipfile.ZipFile(save) as archive:
        assert archive.testzip() is None
        data = archive.read("gamestate")
    assert hashlib.sha256(data).hexdigest() == observation["gamestate_sha256"]
    audit = json.loads(save.with_suffix(".audit.json").read_text(encoding="utf-8"))
    assert audit["gamestate_sha256"] == observation["gamestate_sha256"]
    assert audit["date"] == observation["date"]
    roots = {k: v for k, v, obj in c.a.fields(data.decode("utf-8-sig")) if obj}
    fleet = c.a.block(roots["fleet"], "159")
    assert fleet == observation["fleets_1019"]["159"]["raw"]
    for world in ("2", "17"):
        raw = c.a.block(c.a.block(roots["planets"], "planet"), world)
        assert raw == observation["worlds_1019"][world]["raw"]
    values = c.a.scalars(c.a.block(c.a.block(roots["country"], "0"), "variables"))
    assert values == observation["country_variables_all"]
    return observation, roots, {"path": str(path), "sha256": digest(path)}


def snapshot(observation, roots, reference):
    fleet = observation["fleets_1019"]["159"]
    order = c.a.block(fleet["raw"], "current_order")
    source, core = (observation["worlds_1019"][key] for key in ("17", "2"))
    armies = {key: c.a.scalars(raw) for key, raw, obj in c.a.fields(roots.get("army", ""))
              if obj and c.a.scalars(raw).get("owner") == 0}
    transports = [{"fleet": fleet_id, "ship": ship_id, "native": ship["native"]}
                  for fleet_id, f in observation["fleets_1019"].items()
                  for ship_id, ship in f["ships"].items()
                  if any(s["native"].get("ship_size") == "transport"
                         for s in ship["design"]["stages"])]
    nodes = children(order)
    return {"provenance": observation["provenance_1019"], "observation": reference,
            "date": observation["date"], "order_raw": order, "order_nodes": nodes,
            "fleet_native": fleet["native"], "all_eep_country_variables": {
                key: value for key, value in observation["country_variables_all"].items()
                if key.startswith("eep_")},
            "all_mother_variables": fleet["variables"],
            "all_mother_modifiers": fleet["timed_modifier"],
            "source_native": source["native"], "source_variables": source["variables"],
            "source_flags": source["flags"], "source_population": source["actual_pop_sum"],
            "core_native": core["native"], "core_variables": core["variables"],
            "core_population": core["actual_pop_sum"], "core_capacity": c.capacity(core),
            "crisis_objectives": observation["crisis_objectives"],
            "worlds_objective": c.objective_progress(observation, "crisobj_destroy_worlds"),
            "empires_objective": c.objective_progress(observation, "crisobj_destroy_empires"),
            "actor_armies": armies, "actor_transport_ships": transports,
            "actor_armies_on_target": {k: v for k, v in armies.items()
                if v.get("colony") == source["native"].get("colony")},
            "native_war0_raw": c.a.block(roots.get("war", ""), "0"),
            "guard_scope": {"source_colony_reference": source["native"].get("colony"),
                "source_owner": source["native"].get("owner"),
                "source_controller": source["native"].get("controller"),
                "source_designation": source["colony_native"].get("designation"),
                "source_current_order_accepted": bool(order),
                "ground_combat_engine_trigger": "UNKNOWN_NOT_EVALUATED_BY_THIS_COLLECTOR",
                "artificial_engine_trigger": "UNKNOWN_NOT_EVALUATED_BY_THIS_COLLECTOR",
                "digestible_engine_trigger": "UNKNOWN_NOT_EVALUATED_BY_THIS_COLLECTOR"}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("observations", nargs="+")
    args = parser.parse_args()
    loaded = [load(path) for path in args.observations]
    stages = [snapshot(*entry) for entry in loaded]
    comparisons = []
    for (before, _, _), (after, _, _) in zip(loaded, loaded[1:]):
        comparison = c.compare(before, after)
        comparison["date_before"] = before["date"]
        comparison["date_after"] = after["date"]
        comparisons.append(comparison)
    manifest = json.loads(Path(loaded[0][0]["manifest"]).read_text(encoding="utf-8"))
    definitions = []
    for path in sorted((Path(manifest["copied_mod"]) / "common/scripted_triggers").glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig")
        for key in ("eep_colossus_target_valid", "eep_digestible_world", "eep_qualified", "eep_core_available"):
            body = c.a.block(text, key)
            if body:
                definitions.append({"key": key, "path": str(path), "sha256": digest(path), "raw": body})
    write(args.output, {"schema": "eep.1019.native-pk-order-collector.v1",
        "status": "OBSERVATION_ONLY", "checks": None,
        "scope": "Completed native SAV order, raw guard evidence and complete strict comparisons only",
        "script_sha256": digest(__file__), "checker_sha256": digest(c.__file__),
        "inspector_sha256": digest(c.n.__file__), "stages": stages,
        "strict_comparisons": comparisons, "frozen_guard_definitions": definitions,
        "limitations": ["No complete Stellaris trigger evaluation or native UI assertion.",
            "Missing order fields remain absent; no inferred fire_time is written.",
            "Across-month population, resources and unrelated crisis objectives can change naturally."]})
    print(json.dumps({"status": "OBSERVATION_ONLY", "output": args.output, "stages": len(stages)}))


if __name__ == "__main__":
    main()
