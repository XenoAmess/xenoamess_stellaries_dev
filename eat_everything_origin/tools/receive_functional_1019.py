"""Offline native evidence intake; original checkers stay authoritative."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import check_1019 as original

ROOT = Path(__file__).resolve().parents[1]
EXE_SHA = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
CHECKER_SHA = "681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc"
INSPECTOR_SHA = "1ec3ad71f877be5704959134b76e59be077b756a906f7297f278613ee8bfbf92"
SCHEMA = "eep.1019.functional-intake.v1"
ROLE_GROUPS = {
    "enemy_pk": ["clean", "base", "calafter", "queued", "charge", "cancel",
                 "cancel_reload", "requeued", "windup_last", "fire_start", "prefire",
                 "immediate", "stable", "duplicate", "duplicate_reload", "restart"],
    "normal": ["ready50", "decision_start", "precomplete", "immediate", "stable",
               "duplicate", "reload"],
    "guard": ["ready", "idle", "fired"],
    "native_state_guard": ["ready", "idle", "fired"],
    "core": ["before", "after", "newcore_idle", "newcore_fired", "ownerloss_idle",
             "ownerloss_fired"],
    "death": ["before", "cleanup", "full_init", "monthly", "reload"],
    "restore": ["injured", "natural_after"],
    "lithoid_pk": ["ready", "calafter", "restored", "queued", "windup_last",
                   "fire_start", "prefire", "immediate", "stable", "duplicate", "reload"],
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def content_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reference(entry):
    require(isinstance(entry, dict), "explicit path/SHA reference required")
    require(isinstance(entry.get("path"), str) and entry["path"], "reference path missing")
    require(isinstance(entry.get("sha256"), str)
            and re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]), "reference SHA missing")
    path = Path(entry["path"]).resolve()
    require(path.is_file(), "fixed evidence file missing: " + str(path))
    require(digest(path) == entry["sha256"], "evidence SHA changed: " + str(path))
    return path


def interface_sources():
    return {name: {"path": str(ROOT / relative), "sha256": digest(ROOT / relative)}
            for name, relative in {"checker": "tools/check_1019.py",
                                   "inspector": "testing/inspect_1019.py",
                                   "publisher_interface": "tools/publish_1019.py"}.items()}


def case_contract(path=None):
    """Read the limited static CASE_CHECKS syntax without importing the gate."""
    nodes = ast.parse((Path(path) if path else ROOT / "tools/publish_1019.py")
                      .read_text(encoding="utf-8-sig")).body
    assignments = {node.targets[0].id: node.value for node in nodes
                   if isinstance(node, ast.Assign) and len(node.targets) == 1
                   and isinstance(node.targets[0], ast.Name)}
    names = {name: ast.literal_eval(assignments[name])
             for name in ("STARTUP_CHECKS", "ECONOMY_CHECKS", "COMPONENT_CHECKS")}

    def value(node):
        if isinstance(node, ast.Name) and node.id in names:
            return names[node.id]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            return value(node.left) | value(node.right)
        return ast.literal_eval(node)

    result = {}
    case_node = assignments["CASE_CHECKS"]
    require(isinstance(case_node, ast.Dict), "unknown publisher CASE_CHECKS syntax")
    for key, child in zip(case_node.keys, case_node.values):
        if key is None:
            require(isinstance(child, ast.DictComp) and len(child.generators) == 1,
                    "unknown publisher dictionary expansion")
            generator = child.generators[0]
            require(isinstance(generator.target, ast.Name) and generator.target.id == "branch"
                    and not generator.ifs and not generator.is_async,
                    "unknown publisher branch generator")
            require(isinstance(child.key, ast.JoinedStr) and len(child.key.values) == 2
                    and isinstance(child.key.values[0], ast.FormattedValue)
                    and isinstance(child.key.values[0].value, ast.Name)
                    and child.key.values[0].value.id == "branch"
                    and isinstance(child.key.values[1], ast.Constant),
                    "unknown publisher case name expression")
            suffix = child.key.values[1].value
            for branch in ast.literal_eval(generator.iter):
                result[branch + suffix] = sorted(value(child.value))
        else:
            result[ast.literal_eval(key)] = sorted(value(child))
    result["random_components"] = sorted(names["COMPONENT_CHECKS"])
    require(len(result) == 18, "publisher case group count changed; review contract")
    return result


def template():
    return {"schema": SCHEMA, "status": "PENDING", "expected_run_id": None,
            "additional_run_ids": [], "expected_tree_sha256": None,
            "expected_version": None, "manifest": {"path": None, "sha256": None},
            "interface_sources": interface_sources(), "world_ids": [], "roles": {},
            "tasks": [], "suggested_semantic_roles": ROLE_GROUPS,
            "role_format": {"kind": "native_ui_save|native_autosave",
                            "save": {"path": None, "sha256": None},
                            "receipt": {"path": None, "sha256": None},
                            "audit": {"path": None, "sha256": None},
                            "manifest": "optional exact reference for another declared run"},
            "task_formats": [
                {"id": "unique", "kind": "compare|no-settlement|settlement",
                 "before": "actual role", "after": "actual role",
                 "reload": "optional actual role", "case": "original checker case object"},
                {"id": "unique", "kind": "mother|growth", "role": "actual role",
                 "expected_c": "optional explicit finite number for growth"}],
            "final_case_matrix": {name: {"status": "PENDING", "checks": {k: None for k in keys}}
                                  for name, keys in case_contract().items()}}


def package(manifest_ref, intake):
    path = reference(manifest_ref)
    manifest = read(path)
    run_ids = [intake["expected_run_id"], *intake.get("additional_run_ids", [])]
    require(manifest.get("run_id") in run_ids, "manifest run not explicitly declared")
    require(manifest.get("schema") == "xenoamess.stellaris.acceptance-run.v1",
            "native run manifest schema differs")
    require(manifest.get("repository_mod_tree_sha256") == intake["expected_tree_sha256"]
            == manifest.get("copied_mod_tree_sha256"), "candidate tree differs")
    require(manifest.get("language") == "l_simp_chinese", "Chinese native runtime required")
    require(manifest.get("game_exe_sha256") == EXE_SHA, "native EXE differs")
    require(manifest.get("static_gate", {}).get("status") == "PASS"
            and manifest["static_gate"].get("version") == intake["expected_version"],
            "native run static gate/version differs")
    require(manifest.get("profile_id") == "eep-0.4.0-single-production-mod"
            and manifest.get("enabled_mods") == ["mod/ugc_eep-1019.mod"],
            "single-production-mod profile differs")
    return path, manifest


def validate_role(role, intake):
    manifest_path, manifest = package(role.get("manifest", intake["manifest"]), intake)
    save, receipt_path, audit_path = (reference(role[key]) for key in ("save", "receipt", "audit"))
    receipt, audit = read(receipt_path), read(audit_path)
    require(save.parent == manifest_path.parent, "original observer requires colocated run manifest")
    require(Path(receipt.get("archived", "")).resolve() == save,
            "role receipt must name this exact archived SAV, not another equal-SHA save")
    require(receipt.get("sha256") == role["save"]["sha256"], "receipt SAV SHA differs")
    require(re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", receipt.get("date", "")), "native receipt date missing")
    kind = role.get("kind")
    if kind == "native_ui_save":
        require(all(isinstance(receipt.get(k), str) and receipt[k] for k in ("written_at", "history")),
                "actual UI-save receipt required")
    elif kind == "native_autosave":
        require(isinstance(receipt.get("source"), str) and receipt["source"], "autosave source required")
        start, mtime = receipt.get("command_started_ns"), receipt.get("source_mtime_ns")
        require(type(start) is int and type(mtime) is int and mtime > start > 0,
                "autosave must be newer than the real advance command")
        require(receipt.get("native_ui_save") is not True, "autosave cannot claim native UI save")
    else:
        raise ValueError("explicit native_ui_save/native_autosave receipt kind required")
    require(audit.get("save_sha256") == role["save"]["sha256"]
            and Path(audit.get("save", "")).resolve() == save
            and audit.get("date") == receipt["date"], "audit does not bind this exact SAV/date")
    return {"save": save, "receipt": receipt_path, "audit": audit_path,
            "manifest": manifest_path, "run_id": manifest["run_id"], "date": receipt["date"],
            "save_sha256": role["save"]["sha256"], "manifest_sha256": digest(manifest_path)}


def cached_observation(bound, worlds, cache_dir, observe=None):
    identity = {"save_sha256": bound["save_sha256"], "manifest_sha256": bound["manifest_sha256"],
                "world_ids": worlds, "checker_sha256": CHECKER_SHA, "inspector_sha256": INSPECTOR_SHA}
    path = Path(cache_dir) / (content_hash(identity) + ".json")
    if path.exists():
        envelope = read(path)
        require(envelope.get("schema") == "eep.1019.functional-observation-cache.v1"
                and envelope.get("identity") == identity
                and envelope.get("observation_sha256") == content_hash(envelope.get("observation")),
                "observation cache changed; refusing to overwrite: " + str(path))
        observation = envelope["observation"]
        cached = True
    else:
        observation = (observe or original.n.observe)(bound["save"], worlds)
        envelope = {"schema": "eep.1019.functional-observation-cache.v1", "identity": identity,
                    "observation_sha256": content_hash(observation), "observation": observation}
        cached = False
    require(observation.get("status") == "OBSERVATION_ONLY"
            and observation.get("save_sha256") == bound["save_sha256"]
            and observation.get("manifest_sha256") == bound["manifest_sha256"]
            and observation.get("date") == bound["date"], "observation source/date differs")
    require(all(str(world) in observation.get("worlds_1019", {}) for world in worlds),
            "requested physical world missing from native observation")
    if not cached:
        write_new(path, envelope)
    return observation, {"path": str(path.resolve()), "sha256": digest(path),
                         "observation_sha256": envelope["observation_sha256"], "reused": cached}


def order_readings(observation):
    records = []
    for fleet_id, fleet in original.mother_records(observation).items():
        records.append({"fleet_id": fleet_id, "native": fleet["native"],
                        "variables": fleet["variables"], "movement": fleet["movement"],
                        "current_order_raw": original.a.block(fleet["raw"], "current_order"),
                        "ships": {key: {"native": ship["native"], "implementation": ship["implementation"],
                                        "flags": ship["flags"], "variables": ship["variables"]}
                                  for key, ship in fleet["ships"].items()}})
    return records


def execute_task(task, observations, bindings):
    kind = task.get("kind")
    if kind in ("mother", "growth"):
        state = observations[task["role"]]
        return original.mother(state) if kind == "mother" else original.growth(state, task.get("expected_c"))
    require(kind in ("compare", "no-settlement", "settlement"), "unknown task kind")
    before, after = observations[task["before"]], observations[task["after"]]
    if kind == "compare":
        return original.compare(before, after)
    case = dict(task["case"])
    for key in ("source_world", "core_world"):
        require(type(case.get(key)) is int and case[key] >= 0, "explicit physical " + key + " required")
        require(all(str(case[key]) in state["worlds_1019"] for state in (before, after)),
                "task world absent from intake world_ids")
    case.update(before=str(bindings[task["before"]]["save"]), after=str(bindings[task["after"]]["save"]))
    if kind == "no-settlement":
        return original.no_settlement(case, before, after)
    reload_state = observations[task["reload"]] if task.get("reload") else None
    if reload_state is not None:
        case["reload"] = str(bindings[task["reload"]]["save"])
    return original.settlement(case, before, after, reload_state)


def receive(intake, cache_dir):
    require(intake.get("schema") == SCHEMA, "explicit functional intake schema required")
    require(isinstance(intake.get("expected_run_id"), str) and intake["expected_run_id"], "actual run required")
    extra_runs = intake.get("additional_run_ids", [])
    require(isinstance(extra_runs, list) and all(isinstance(x, str) and x for x in extra_runs)
            and len(set([intake["expected_run_id"], *extra_runs])) == len(extra_runs) + 1,
            "additional runs must be explicit unique IDs")
    require(isinstance(intake.get("expected_tree_sha256"), str)
            and re.fullmatch(r"[0-9a-f]{64}", intake["expected_tree_sha256"]), "actual frozen tree required")
    require(isinstance(intake.get("expected_version"), str)
            and re.fullmatch(r"0\.4\.0-rc\.\d+", intake["expected_version"]), "explicit candidate version required")
    sources = interface_sources()
    require(sources["checker"]["sha256"] == CHECKER_SHA
            and sources["inspector"]["sha256"] == INSPECTOR_SHA, "original read-only tools changed")
    require(intake.get("interface_sources") == sources, "intake interface sources changed; review and rebind")
    package(intake["manifest"], intake)
    worlds = intake.get("world_ids")
    require(isinstance(worlds, list) and worlds and all(type(x) is int and x >= 0 for x in worlds)
            and len(worlds) == len(set(worlds)), "explicit unique physical world_ids required")
    worlds = sorted(worlds)
    roles = intake.get("roles")
    require(isinstance(roles, dict) and roles, "actual immutable roles required")
    bindings = {name: validate_role(role, intake) for name, role in roles.items()}
    observations, observation_refs = {}, {}
    for name, bound in bindings.items():
        state, ref = cached_observation(bound, worlds, cache_dir)
        require(state["production_tree_sha256"] == intake["expected_tree_sha256"]
                and state["provenance_1019"]["version"] == intake["expected_version"]
                and state["provenance_1019"]["run_id"] == bound["run_id"], "observed candidate/run differs")
        observations[name], observation_refs[name] = state, ref
    tasks = intake.get("tasks", [])
    require(isinstance(tasks, list), "tasks must be an explicit list")
    results = {}
    for task in tasks:
        task_id = task.get("id")
        require(isinstance(task_id, str) and task_id and task_id not in results, "unique task id required")
        try:
            results[task_id] = execute_task(task, observations, bindings)
        except (ValueError, KeyError, TypeError, OSError) as error:
            results[task_id] = {"status": "FAIL", "scope": "original checker task prerequisite",
                                "error_type": type(error).__name__, "error": str(error)}
    return {"schema": "eep.1019.functional-receive-report.v1",
            "status": "INCOMPLETE" if any(x["status"] == "FAIL" for x in results.values()) else "OBSERVATION_ONLY",
            "scope": "Exact native roles and unchanged checker tasks only; no final case certification.",
            "production_tree_sha256": intake["expected_tree_sha256"], "version": intake["expected_version"],
            "run_ids": sorted({x["run_id"] for x in bindings.values()}), "sources": sources,
            "roles": {name: {"binding": {k: str(v) if isinstance(v, Path) else v for k, v in bound.items()},
                             "observation": observation_refs[name], "actual_date": observations[name]["date"],
                             "mother_orders": order_readings(observations[name])} for name, bound in bindings.items()},
            "tasks": results,
            "final_case_matrix": {name: {"status": "PENDING", "checks": {k: None for k in keys}}
                                  for name, keys in case_contract().items()},
            "limitations": ["Task PASS does not prove native input, war/no-army, guard prerequisites, population attribution, or restart.",
                            "Historical RC6 results are not promoted to the supplied candidate tree.",
                            "No UI, runtime, active logs, source SAV or old tools are modified."],
            "created_at_utc": datetime.now(timezone.utc).isoformat()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("template")
    make.add_argument("--output", type=Path, required=True)
    accept = commands.add_parser("receive")
    accept.add_argument("--intake", type=Path, required=True)
    accept.add_argument("--cache-dir", type=Path, required=True)
    accept.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.exists():
        raise FileExistsError("refusing to overwrite evidence: " + str(args.output))
    try:
        result = template() if args.command == "template" else receive(read(args.intake), args.cache_dir)
    except (ValueError, KeyError, TypeError, OSError, original.zipfile.BadZipFile) as error:
        result = {"schema": "eep.1019.functional-receive-report.v1", "status": "INCOMPLETE",
                  "scope": "native intake prerequisite", "error_type": type(error).__name__, "error": str(error)}
    if args.command == "receive":
        result["intake"] = {"path": str(args.intake.resolve()),
                            "sha256": digest(args.intake) if args.intake.is_file() else None}
    result["receiver_sha256"] = digest(Path(__file__))
    write_new(args.output, result)
    print(json.dumps({"status": result["status"], "output": str(args.output), "error": result.get("error")}))
    return 2 if result["status"] == "INCOMPLETE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
