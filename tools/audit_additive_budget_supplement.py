"""Read-only supplemental budget audit of the ecng native seven-branch matrix.

The reviewed primary report stays authoritative. No save is created or edited.
Source preparation and development inputs are never native acceptance evidence.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CORE_SHA = "2bee9c8460e07a228d8d0f577aa8245792e2ecc936497c975e6bd422be0173a1"
CORE_PATH = ROOT / "tools/audit_additive_runtime_matrix.py"
if hashlib.sha256(CORE_PATH.read_bytes()).hexdigest() != CORE_SHA:
    raise RuntimeError("reviewed primary audit identity changed; stop supplemental audit")
_SPEC = importlib.util.spec_from_file_location("supplement_reviewed_primary", CORE_PATH)
core = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = core
_SPEC.loader.exec_module(core)
D = core.D
BRANCHES, PHASES = core.BRANCHES, core.PHASES
RUN_ID = "20261015T113522Z"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def category_graph(game):
    definitions, files = {}, []
    paths = sorted((game / "common/economic_categories").glob("*.txt"))
    if not paths:
        raise core.native.AuditError("native economic category sources missing")
    for path in paths:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        doc = core.native.Document(text)
        files.append({"path": str(path.resolve()), "bytes": len(raw), "sha256": digest(raw)})
        for entry in doc.entries():
            if entry.key is None or not isinstance(entry.value, core.native.Block):
                raise core.native.AuditError("unknown category definition layout")
            parents = doc.values(entry.value, "parent")
            error = None
            if len(parents) > 1 or any(not isinstance(p, str) for p in parents):
                error = "ambiguous parent declaration"
            block = text[entry.value.start:entry.value.end]
            record = {"category": entry.key, "parent": parents[0] if len(parents) == 1 and isinstance(parents[0], str) else None,
                      "source": str(path.resolve()), "line": text.count("\n", 0, entry.value.start) + 1,
                      "file_sha256": digest(raw), "body_sha256": digest(block.encode("utf-8")), "error": error}
            definitions.setdefault(entry.key, []).append(record)
    return {"files": files, "definitions": definitions,
            "scope": "native declared category parent tree; dynamic channels and undisclosed Mod overrides are not inferred"}


def ancestry(category, graph):
    chain, evidence = [], []
    while category is not None:
        if category in chain:
            return {"status": "NOT COVERED", "chain": chain, "reason": "parent cycle", "evidence": evidence}
        chain.append(category)
        records = graph["definitions"].get(category, [])
        if len(records) != 1 or records[0]["error"]:
            return {"status": "NOT COVERED", "chain": chain, "reason": "unknown/duplicate category or ambiguous parent", "evidence": evidence}
        evidence.append(records[0])
        category = records[0]["parent"]
    return {"status": "PASS", "chain": chain, "evidence": evidence}


def classify(category, graph):
    found = ancestry(category, graph)
    if found["status"] != "PASS":
        return {**found, "kind": "unknown"}
    chain = found["chain"]
    if "planet_jobs" in chain:
        return {**found, "kind": "planet_jobs"}
    job_chain = ancestry("planet_jobs", graph)
    if job_chain["status"] != "PASS" or category in job_chain["chain"]:
        return {**found, "status": "NOT COVERED", "kind": "potential_mixed_ancestor"}
    roots = ("country_base", "planet_pops", "leader_officials", "leaders", "planet_buildings",
             "starbase_buildings", "planet_deposits", "station_gatherers", "station_researchers", "stations")
    family = next((name for name in roots if name in chain), "other_native_non_job")
    return {**found, "kind": "non_job", "family": family}


def observed_values(snapshots, period_kind, category, resource):
    values, missing = {}, []
    for branch in BRANCHES:
        table = snapshots[branch]["measured"]["budget"]["last_month"][period_kind]
        raw = table.get(category, {}).get(resource)
        if raw is None:
            missing.append({"branch": branch, "reason": "row absent; no zero substitution"})
        else:
            try:
                values[branch] = core.number(raw, category + "." + resource)
            except core.native.AuditError as error:
                missing.append({"branch": branch, "reason": str(error)})
    return values, missing


def row_keys(snapshots, kind):
    return sorted({(category, resource) for branch in BRANCHES
                   for category, resources in snapshots[branch]["measured"]["budget"]["last_month"][kind].items()
                   for resource in resources})


def invariant(values):
    return [core.comparison("FIXED_" + b, values[b], values["F00"]) for b in BRANCHES]


def raw_response(values):
    q0 = (values["F10"] - values["F00"]) / D(".4")
    q1 = (values["F11"] - values["F01"]) / D(".4")
    checks = [core.comparison("A40_RESPONSE_EQUAL", q1, q0),
              core.comparison("B_AT_A0", values["F01"] - values["F00"], D(".35") * q0),
              core.comparison("B_AT_A40", values["F11"] - values["F10"], D(".35") * q0),
              core.comparison("INTERACTION", (values["F11"] - values["F10"]) - (values["F01"] - values["F00"]), 0)]
    checks += [core.comparison("DUMMY_INCREMENT_" + b, values[b] - values["F11"], D(".05") * q0)
               for b in ("FP", "FN", "FH")]
    return {"Q0": str(q0), "Q1": str(q1), "checks": checks, "status": core.status_of(checks)}


def audit_rows(snapshots, graph, kind):
    rows = []
    for category, resource in row_keys(snapshots, kind):
        source = classify(category, graph)
        values, missing = observed_values(snapshots, kind, category, resource)
        row = {"category": category, "resource": resource, "budget_path": "budget.last_month." + kind + "." + category + "." + resource,
               "source": source, "values": {b: str(v) for b, v in values.items()}, "missing_or_invalid": missing}
        if missing:
            row.update(status="NOT COVERED", reason="all seven finite observations required")
        elif kind == "expenses":
            checks = invariant(values)
            row.update(checks=checks, arithmetic_status=core.status_of(checks), nonzero_observed=any(v != 0 for v in values.values()))
            row["status"] = row["arithmetic_status"]
            if source["status"] != "PASS" or (row["status"] == "PASS" and not row["nonzero_observed"]):
                row.update(status="NOT COVERED", reason="unknown source or only zero costs observed; no nonzero fee coverage")
        else:
            if any(v == 0 for v in values.values()):
                row.update(status="NOT COVERED", reason="all seven nonzero income observations required")
            else:
                response = raw_response(values)
                row.update(response=response, arithmetic_status=response["status"])
                if source["status"] != "PASS":
                    row.update(status="NOT COVERED", reason="income source unresolved; arithmetic is diagnostic")
                elif source["kind"] == "non_job":
                    checks = invariant(values)
                    row.update(invariance_checks=checks, status=core.status_of(checks), evidence_role="observed nonzero non-job negative control")
                elif core.close(response["Q0"], 0) and core.close(response["Q1"], 0):
                    row.update(invariance_checks=invariant(values), status="NOT COVERED", reason="zero A response cannot prove a job received +5%")
                    if response["status"] != "PASS":
                        row["status"] = response["status"]
                elif core.number(response["Q0"]) <= 0 or core.number(response["Q1"]) <= 0:
                    row.update(status="FAIL", reason="nonpositive measured job response")
                else:
                    row.update(status=response["status"], evidence_role="finite positive raw planet_jobs additive response; no assumed job base")
        rows.append(row)
    return rows


def derive(report, graph):
    """Pure development-testable derivation; no file or native identity claim."""
    snapshots = report["snapshots"]
    common = report["common_snapshot"]
    if common is None or any(set(snapshots[b]) != set(PHASES) for b in BRANCHES):
        raise core.native.AuditError("complete seven-by-three snapshots and common required")
    measured_reference = core.employment_signature(snapshots["F00"]["measured"])
    employment = []
    for branch in BRANCHES:
        for phase in PHASES:
            if not core.equivalent(core.employment_signature(snapshots[branch][phase]), measured_reference):
                employment.append(core.issue("INVALID", "NO_GROWTH_EMPLOYMENT_CHANGED", branch=branch, phase=phase))
    preserved = {"top": report["status"], "limited_economy": report["limited_economy"]["status"],
                 "strict_cache_audit": report["strict_cache_audit"]["status"], "setup_input_audit": report["setup_input_audit"]["status"]}
    source_status = core.status_of([core.issue(value, key) for key, value in preserved.items()] + employment)
    expenses = audit_rows(snapshots, graph, "expenses")
    income = audit_rows(snapshots, graph, "income")
    arithmetic = core.status_of(expenses + income, fallback="NOT COVERED" if not expenses or not income else "PASS")
    focus = {}
    for name, ancestor in (("population_upkeep", "planet_pops"), ("leader_officials", "leader_officials")):
        relevant = [r for r in expenses if ancestor in r["source"]["chain"]]
        focus[name] = {"status": core.status_of(relevant, fallback="PASS" if relevant else "NOT COVERED"),
                       "observed_rows": [{"category": r["category"], "resource": r["resource"], "status": r["status"]} for r in relevant],
                       "scope": "only listed actually present nonzero expense rows; unobserved fees not tested"}
    return {"status": source_status if source_status != "PASS" else arithmetic,
            "arithmetic_status": arithmetic, "primary_status_preserved": preserved,
            "source_acceptance_status": source_status, "additional_no_growth_employment_checks": employment,
            "expenses": expenses, "income": income, "focused_expense_coverage": focus,
            "scope": "observed measured.last_month rows only; missing/zero/unresolved sources are not broad fee or +5% coverage",
            "unobserved_categories_are_not_tested": True,
            "epsilon_rule": "reviewed primary max(0.0001,0.000001*max(abs(compared values)))"}


def provenance(report, game):
    path = Path(report["manifest"])
    raw = path.read_bytes()
    if path.name != "additive-no-growth-matrix-manifest.json" or digest(raw) != report["manifest_sha256"]:
        raise core.native.AuditError("no-growth native source manifest identity mismatch")
    manifest = json.loads(raw)
    def resolve(value):
        candidate = Path(value)
        return (path.parent / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    if resolve(manifest["sources"]["game_root"]) != game.resolve():
        raise core.native.AuditError("category game root differs from primary declared source")
    mod = resolve(manifest["sources"]["mod_root"])
    if list((mod / "common/economic_categories").glob("*.txt")):
        raise core.native.AuditError("Mod category overrides require separate reviewed resolution")
    identities = []
    for branch, phase, snapshot in [("common", None, report["common_snapshot"])] + [
            (b, p, report["snapshots"][b][p]) for b in BRANCHES for p in PHASES]:
        save = Path(snapshot["save"])
        declared = resolve(manifest["common"] if phase is None else manifest["branches"][branch][phase])
        if save.resolve() != declared or RUN_ID not in save.parts or (phase is not None and not save.name.lower().startswith("ecng")):
            raise core.native.AuditError("non-ecng or mixed-run native source rejected")
        data = save.read_bytes()
        if len(data) != snapshot["bytes"] or digest(data) != snapshot["sha256"]:
            raise core.native.AuditError("saved source identity changed since primary read")
        identities.append({"branch": branch, "phase": phase, "save": str(save), "sha256": snapshot["sha256"], "bytes": len(data), "date": snapshot["date"]})
    if report.get("native_execution") != "READ NATIVE SAVES; no game launch or UI certification":
        raise core.native.AuditError("primary report does not identify native-save read")
    return {"manifest": str(path.resolve()), "manifest_sha256": digest(raw), "mod_root": str(mod), "snapshots": identities}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--matrix-report", type=Path)
    choice.add_argument("--prepare-sources", action="store_true")
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "primary_tool_sha256": CORE_SHA,
              "supplement_tool_sha256": digest(Path(__file__).read_bytes()), "native_files_written": False}
    try:
        graph = category_graph(args.game)
        if args.prepare_sources:
            result.update(status="SOURCE_PREPARATION_ONLY", native_matrix="NOT RUN", source_graph=graph)
        else:
            raw = args.matrix_report.read_bytes()
            report = json.loads(raw)
            identity = provenance(report, args.game)
            result.update(derive(report, graph), source_graph=graph, native_source_identity=identity,
                          primary_report=str(args.matrix_report.resolve()), primary_report_sha256=digest(raw))
    except (core.native.AuditError, OSError, ValueError, TypeError, KeyError) as error:
        result.update(status="INVALID", diagnostics=[core.issue("INVALID", "SUPPLEMENT_UNINTERPRETABLE", message=str(error))])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "report": str(args.report)}, ensure_ascii=False))
    return 0 if result["status"] in ("PASS", "SOURCE_PREPARATION_ONLY") else 2


if __name__ == "__main__":
    raise SystemExit(main())
