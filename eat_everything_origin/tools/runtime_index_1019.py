"""Collect real evidence into PENDING progress indexes; never accept a case."""
import argparse
import copy
import json
import math
from pathlib import Path
import re

import publish_1019 as release


def load_progress(path, root):
    path = Path(path)
    path = (root / path if not path.is_absolute() else path).resolve()
    try:
        path.relative_to((root / "docs/evidence").resolve())
        path.relative_to(root.resolve())
    except ValueError as error:
        raise RuntimeError("progress index must remain in project docs/evidence") from error
    if path.name.casefold() == "final-result.json":
        raise RuntimeError("this tool cannot modify a final acceptance index")
    data = release.read_json(path)
    if (data.get("schema") != "eep-1019-acceptance-v1" or data.get("status") != "PENDING"
            or data.get("component_rewards", {}).get("status") != "PENDING"
            or any(case.get("status") != "PENDING" for case in data.get("cases", {}).values())):
        raise RuntimeError("only wholly PENDING progress indexes can be updated")
    release.candidate_files(data)
    return path, data


def add_reference(entries, entry):
    for prior in entries:
        if prior["path"] == entry["path"]:
            if prior["sha256"] != entry["sha256"]:
                raise RuntimeError("evidence bytes changed; archive a new version instead")
            if prior.get("kind") and entry.get("kind") and prior["kind"] != entry["kind"]:
                raise RuntimeError("one evidence file cannot masquerade as multiple kinds")
            if not prior.get("kind") and entry.get("kind"):
                prior["kind"] = entry["kind"]
            return
    entries.append(entry)


def registered_runs(data, root):
    result = {}
    for entry in data["runs"]:
        run = release.read_json(release.reference_path(entry, root))
        result[run["run_id"]] = run
    return result


def bind_run(data, name, root, cases=()):
    entry = release.collect_reference(name, root)
    run = release.read_json(root / entry["path"])
    source_rows = run.get("repository_mod_files", [])
    source = {row["path"]: row["sha256"] for row in source_rows}
    static = run.get("static_gate", {})
    if (run.get("schema") != "xenoamess.stellaris.acceptance-run.v1"
            or run.get("profile_id") != release.PROFILE or run.get("language") != "l_simp_chinese"
            or run.get("game_exe_sha256") != release.update.EXE_SHA
            or run.get("enabled_mods") != release.ENABLED_MODS
            or run.get("repository_mod_tree_sha256") != data["production_tree_sha256"]
            or run.get("copied_mod_tree_sha256") != data["production_tree_sha256"]
            or len(source_rows) != len(source) or source != data["production_files"]
            or static.get("status") != "PASS" or static.get("version") != data["version"]
            or static.get("source_tree_sha256") != data["production_tree_sha256"]
            or static.get("report_sha256") != data["static_gate"]["report"]["sha256"]
            or not run.get("run_id")):
        raise RuntimeError("run does not bind this final candidate and static gate")
    for case in cases:
        if case not in data["cases"]:
            raise RuntimeError("unknown case: " + case)
    add_reference(data["runs"], entry)
    for case in cases:
        if run["run_id"] not in data["cases"][case]["run_ids"]:
            data["cases"][case]["run_ids"].append(run["run_id"])


def attach(data, case, run_id, kind, name, root):
    if case not in data["cases"] or kind not in release.EVIDENCE_KINDS:
        raise RuntimeError("unknown case or evidence kind")
    if run_id not in registered_runs(data, root):
        raise RuntimeError("register the actual candidate run first")
    entry = release.collect_reference({"path": name, "kind": kind}, root)
    add_reference(data["cases"][case]["evidence"], entry)
    if run_id not in data["cases"][case]["run_ids"]:
        data["cases"][case]["run_ids"].append(run_id)
    return entry


def observe_check(data, case, check, result, analysis, run_id, root):
    if case not in data["cases"] or check not in data["cases"][case]["checks"] or type(result) is not bool:
        raise RuntimeError("unknown check or non-boolean observation")
    entry = attach(data, case, run_id, "analysis", analysis, root)
    data["cases"][case]["checks"][check] = result
    history = data.setdefault("_progress", {}).setdefault("check_observations", [])
    record = {"case": case, "check": check, "result": result, "analysis": entry,
              "scope": "explicit individual observation; case remains PENDING"}
    if record not in history:
        history.append(record)


def add_budget(data, branch, role, analysis, save, root, run_id=None):
    if branch not in ("hive", "machine", "purifier") or role not in ("baseline", "candidate"):
        raise RuntimeError("unknown economy branch or role")
    source_ref = release.collect_reference({"path": analysis, "kind": "analysis"}, root)
    save_ref = release.collect_reference({"path": save, "kind": "native_save"}, root)
    report = release.read_json(root / source_ref["path"])
    if report.get("status") != "OBSERVATION_ONLY":
        raise RuntimeError("budget importer requires an original observation report")
    if "branches" in report:
        matches = [row for row in report["branches"].get(branch, []) if row.get("save_sha256") == save_ref["sha256"]]
        if len(matches) != 1:
            raise RuntimeError("aggregate budget does not identify this exact native save")
        date, net = matches[0].get("date"), matches[0].get("balance")
    else:
        if report.get("save_sha256") != save_ref["sha256"]:
            raise RuntimeError("budget observation save SHA differs")
        date, net = report.get("date"), report.get("energy", {}).get("current_month", {}).get("balance")
    if (not isinstance(date, str) or not re.fullmatch(r"\d{4}\.(0[1-9]|1[0-2])\.01", date)
            or type(net) not in (int, float) or not math.isfinite(net)):
        raise RuntimeError("finite observed monthly energy and native month date required")
    row = {"date": date, "net_energy": net, "evidence": save_ref, "observation": source_ref}
    rows = data["economy"][branch][role + "_months"]
    for prior in rows:
        if prior["date"] == date:
            if prior != row:
                raise RuntimeError("monthly observation already differs; preserve its original version")
            return
    if len(rows) >= 12:
        raise RuntimeError("twelve-month budget already full")
    if role == "candidate":
        attach(data, branch + "_economy", run_id, "native_save", save, root)
        attach(data, branch + "_economy", run_id, "analysis", analysis, root)
    else:
        add_reference(data["archives"], source_ref)
    rows.append(row)
    rows.sort(key=lambda entry: entry["date"])


def import_baseline(data, directory, root):
    directory = Path(directory).as_posix().rstrip("/")
    analysis = directory + "/baseline-economy-observations.json"
    report = release.read_json(release.project_evidence_path(analysis, root))
    for branch, stem in (("hive", "bhm"), ("machine", "bmm"), ("purifier", "bpm")):
        rows = report.get("branches", {}).get(branch, [])
        if len(rows) != 13 or rows[0].get("date") != "2200.01.01":
            raise RuntimeError("baseline import requires the archived startup plus twelve native months")
        for index in range(1, 13):
            add_budget(data, branch, "baseline", analysis, directory + f"/{stem}{index:02}.sav", root)
    add_reference(data["archives"], release.collect_reference(directory + "/manifest.json", root))


def missing(data):
    return {"status": "PENDING", "component_rewards": data["component_rewards"]["status"],
            "cases": {name: {"missing_or_failed_checks": [key for key, value in case["checks"].items() if value is not True],
                             "missing_evidence_kinds": sorted(release.EVIDENCE_KINDS - {e.get("kind") for e in case["evidence"]}),
                             "run_ids": case["run_ids"]} for name, case in data["cases"].items()},
            "months": {branch: {role: len(value[role + "_months"]) for role in ("baseline", "candidate")}
                       for branch, value in data["economy"].items()},
            "negative_candidate_months": {branch: [row["date"] for row in value["candidate_months"] if row["net_energy"] < 0]
                                          for branch, value in data["economy"].items()},
            "growth_observations": len(data["growth_samples"])}


def update_progress(path, root, operation, mutate):
    path, data = load_progress(path, root)
    before = copy.deepcopy(data)
    previous = release.update.digest(path.read_bytes())
    mutate(data)
    if data == before:
        return {"status": "PENDING", "changed": False}
    if (data["status"] != "PENDING" or data["component_rewards"]["status"] != "PENDING"
            or any(case["status"] != "PENDING" for case in data["cases"].values())):
        raise RuntimeError("progress operations cannot accept cases or component delivery")
    for field in ("schema", "version", "formal_version", "language", "game_exe_sha256", "profile_id",
                  "enabled_mods", "production_files", "candidate_descriptor", "production_tree_sha256", "static_gate"):
        if data[field] != before[field]:
            raise RuntimeError("progress operations cannot change frozen source bindings")
    data.get("_scaffold", {}).pop("generated_content_sha256", None)
    data.setdefault("_progress", {}).setdefault("history", []).append({"previous_index_sha256": previous, "operation": operation})
    release.update.base.write_json(path, data)
    return {"status": "PENDING", "changed": True, "sha256": release.update.digest(path.read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, type=Path, help="project-relative PENDING progress index")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("missing")
    run = sub.add_parser("add-run"); run.add_argument("--manifest", required=True); run.add_argument("--case", action="append", default=[])
    baseline = sub.add_parser("baseline"); baseline.add_argument("--directory", default="docs/evidence/1019-baseline")
    proof = sub.add_parser("attach")
    for name in ("case", "run-id", "kind", "file"): proof.add_argument("--" + name, required=True)
    check = sub.add_parser("observe-check")
    for name in ("case", "run-id", "check", "analysis"): check.add_argument("--" + name, required=True)
    check.add_argument("--result", choices=("true", "false"), required=True)
    budget = sub.add_parser("budget")
    for name in ("branch", "role", "analysis", "save"): budget.add_argument("--" + name, required=True)
    budget.add_argument("--run-id")
    args = parser.parse_args(); root = release.ROOT
    if args.command == "missing":
        print(json.dumps(missing(load_progress(args.index, root)[1]), ensure_ascii=False)); return
    operations = {"add-run": lambda d: bind_run(d, args.manifest, root, args.case),
        "baseline": lambda d: import_baseline(d, args.directory, root),
        "attach": lambda d: attach(d, args.case, args.run_id, args.kind, args.file, root),
        "observe-check": lambda d: observe_check(d, args.case, args.check, args.result == "true", args.analysis, args.run_id, root),
        "budget": lambda d: add_budget(d, args.branch, args.role, args.analysis, args.save, root, args.run_id)}
    operation = {"command": args.command, "parameters": {key: value for key, value in vars(args).items()
                                                       if key not in {"index", "command"}}}
    print(json.dumps(update_progress(args.index, root, operation, operations[args.command])))


if __name__ == "__main__":
    main()
