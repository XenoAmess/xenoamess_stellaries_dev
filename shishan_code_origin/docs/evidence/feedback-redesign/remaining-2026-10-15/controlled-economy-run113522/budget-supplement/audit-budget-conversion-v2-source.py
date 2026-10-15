"""Supplement v2: keep ordinary budget controls and verify trade conversion.

Only the independently sourced default trade policy is a derived conversion.
The original v1 FAIL and every observed row stay available unchanged.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location("budget_supplement_v1_frozen", ROOT / "tools/audit_additive_budget_supplement.py")
v1 = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = v1
_SPEC.loader.exec_module(v1)
V1_SHA = "7ef4d92d285d711ec854e2fb7745ac3b3275f180b2bcd3ae65e99965c0280b92"
if v1.digest(Path(_SPEC.origin).read_bytes()) != V1_SHA:
    raise RuntimeError("v1 baseline identity changed")
core, D = v1.core, v1.D
POLICY_SHA = "3638e072772adf7e1987b9f065976cb3151544bd365c3504d5bf7664051f2042"


def conversion_source(game, graph):
    path = game / "common/policies/00_policies.txt"
    raw = path.read_bytes()
    if v1.digest(raw) != POLICY_SHA:
        raise core.native.AuditError("default policy source identity is unreviewed")
    doc = core.native.Document(raw.decode("utf-8-sig"))
    policy = doc.section(doc.root, "trade_policy")
    options = [b for b in doc.values(policy, "option") if isinstance(b, core.native.Block)
               and doc.scalar(b, "name") == "trade_policy_default"]
    if len(options) != 1:
        raise core.native.AuditError("default trade option is not unique")
    enabled = doc.section(options[0], "on_enabled")
    hidden = doc.section(enabled, "hidden_effect")
    table = doc.section(hidden, "set_trade_conversions")
    if len(doc.entries(enabled)) != 1 or len(doc.entries(hidden)) != 1:
        raise core.native.AuditError("additional default conversion effects unreviewed")
    coefficients = core.resource_table(doc, table)
    if set(coefficients) != {"trade", "energy"}:
        raise core.native.AuditError("default conversion outputs changed")
    record = graph["definitions"].get("trade_policy", [])
    if len(record) != 1 or record[0]["error"] or record[0]["parent"] is not None:
        raise core.native.AuditError("trade policy category source ambiguous")
    category_doc = core.native.Document(Path(record[0]["source"]).read_text(encoding="utf-8-sig"))
    if category_doc.entries(category_doc.section(category_doc.root, "trade_policy")):
        raise core.native.AuditError("trade policy economic category is no longer the reviewed empty root")
    return {"status": "PASS", "option": "trade_policy_default", "coefficients": coefficients,
            "source": str(path.resolve()), "sha256": v1.digest(raw),
            "policy_line": doc.text.count("\n", 0, policy.start) + 1,
            "option_line": doc.text.count("\n", 0, options[0].start) + 1,
            "conversion_line": doc.text.count("\n", 0, table.start) + 1,
            "category": record[0]}


def selected_trade(snapshot):
    values = []
    for row in snapshot["context"]["policies"]:
        fields = {}
        for entry in row:
            if entry["key"] in fields:
                raise core.native.AuditError("duplicate saved policy field")
            fields[entry["key"]] = entry["value"]
        if fields.get("policy") == "trade_policy":
            values.append(fields.get("selected"))
    return values


def verify_conversion(report, graph, source):
    snapshots = report["snapshots"]
    try:
        if source["status"] != "PASS" or selected_trade(report["common_snapshot"]) != [source["option"]]:
            raise core.native.AuditError("common default policy not established")
        for branch in v1.BRANCHES:
            for phase in v1.PHASES:
                if selected_trade(snapshots[branch][phase]) != [source["option"]]:
                    raise core.native.AuditError("default policy changed or missing")
        trade_sources = sorted(c for c, r in v1.row_keys(snapshots, "income") if r == "trade" and c != "trade_policy")
        if not trade_sources:
            raise core.native.AuditError("no observed upstream trade")
        job_total = {b: D(0) for b in v1.BRANCHES}
        nonjob_total = {b: D(0) for b in v1.BRANCHES}
        upstream = []
        for category in trade_sources:
            classification = v1.classify(category, graph)
            values, missing = v1.observed_values(snapshots, "income", category, "trade")
            if missing or classification["status"] != "PASS":
                raise core.native.AuditError("upstream trade source missing or unresolved")
            into = job_total if classification["kind"] == "planet_jobs" else nonjob_total
            for branch in v1.BRANCHES:
                into[branch] += values[branch]
            upstream.append({"category": category, "values": {b: str(v) for b, v in values.items()}, "source": classification})
        expected_outputs = set(source["coefficients"])
        for branch in v1.BRANCHES:
            budget = snapshots[branch]["measured"]["budget"]["last_month"]
            if set(budget["income"].get("trade_policy", {})) != expected_outputs:
                raise core.native.AuditError("missing or extra conversion output resource")
            if set(budget["expenses"].get("trade_policy", {})) != {"trade"}:
                raise core.native.AuditError("missing or extra conversion input resource")
            if any(c != "trade_policy" and "trade" in resources for c, resources in budget["expenses"].items()):
                raise core.native.AuditError("additional trade-consuming channels unreviewed")
        coefficients = {k: core.number(v) for k, v in source["coefficients"].items()}
        checks = [core.comparison("OUTPUT_SHARES_SUM", sum(coefficients.values()), 1)]
        inputs, missing = v1.observed_values(snapshots, "expenses", "trade_policy", "trade")
        if missing:
            raise core.native.AuditError("conversion expense unavailable")
        outputs = {}
        for resource in coefficients:
            values, missing = v1.observed_values(snapshots, "income", "trade_policy", resource)
            if missing:
                raise core.native.AuditError("conversion output unavailable")
            outputs[resource] = values
        per_branch = []
        for branch in v1.BRANCHES:
            total = job_total[branch] + nonjob_total[branch]
            checks.append(core.comparison("UPSTREAM_EQUALS_POLICY_INPUT_" + branch, inputs[branch], total))
            for resource, coefficient in coefficients.items():
                checks.append(core.comparison("CONVERSION_SHARE_" + branch + "_" + resource, outputs[resource][branch], total * coefficient))
            checks.append(core.comparison("OUTPUTS_RETURN_INPUT_" + branch, sum(v[branch] for v in outputs.values()), inputs[branch]))
            per_branch.append({"branch": branch, "job_trade": str(job_total[branch]), "nonjob_trade": str(nonjob_total[branch]),
                               "upstream_sum": str(total), "policy_trade_expense": str(inputs[branch]),
                               "policy_income": {r: str(v[branch]) for r, v in outputs.items()}})
        job_response = v1.raw_response(job_total)
        checks += job_response["checks"] + v1.invariant(nonjob_total)
        output_responses = {}
        for resource, values in outputs.items():
            response = v1.raw_response(values)
            checks += response["checks"]
            checks.append(core.comparison("OUTPUT_Q_SHARE_" + resource, response["Q0"], core.number(job_response["Q0"]) * coefficients[resource]))
            output_responses[resource] = response
        if core.number(job_response["Q0"]) <= core.epsilon(job_response["Q0"]):
            return {"status": "NOT COVERED", "reason": "no positive upstream job trade response", "checks": checks}
        return {"status": core.status_of(checks), "source": source, "upstream_sources": upstream,
                "branches": per_branch, "checks": checks, "job_trade_response": job_response,
                "output_responses": output_responses, "role": "conversion throughput and returned resources; not ordinary upkeep or an independent non-job negative control"}
    except (core.native.AuditError, KeyError, TypeError) as error:
        return {"status": "NOT COVERED", "reason": str(error)}


def derive_v2(report, graph, source):
    first = v1.derive(report, graph)
    ordinary_expenses = [r for r in first["expenses"] if r["category"] != "trade_policy"]
    ordinary_income = [r for r in first["income"] if r["category"] != "trade_policy"]
    conversion = verify_conversion(report, graph, source)
    checks = ordinary_expenses + ordinary_income + [core.issue(conversion["status"], "DERIVED_CONVERSION")]
    arithmetic = core.status_of(checks)
    source_status = first["source_acceptance_status"]
    return {"status": source_status if source_status != "PASS" else arithmetic,
            "arithmetic_status": arithmetic, "primary_status_preserved": first["primary_status_preserved"],
            "source_acceptance_status": source_status, "additional_no_growth_employment_checks": first["additional_no_growth_employment_checks"],
            "ordinary_expenses": ordinary_expenses, "ordinary_income": ordinary_income,
            "focused_expense_coverage": first["focused_expense_coverage"], "derived_conversion": conversion,
            "v1_status_preserved": first["status"],
            "trade_policy_v1_rows_preserved": [r for r in first["expenses"] + first["income"] if r["category"] == "trade_policy"],
            "scope": "observed finite rows; only independently verified default policy is classified as derived conversion; no exemption for other non-job sources"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix-report", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "primary_tool_sha256": v1.CORE_SHA,
              "v1_tool_sha256": V1_SHA, "v2_tool_sha256": v1.digest(Path(__file__).read_bytes()), "native_files_written": False}
    try:
        raw = args.matrix_report.read_bytes()
        report = json.loads(raw)
        identity = v1.provenance(report, args.game)
        if list((Path(identity["mod_root"]) / "common/policies").glob("*.txt")):
            raise core.native.AuditError("policy overrides require additional review")
        graph = v1.category_graph(args.game)
        source = conversion_source(args.game, graph)
        result.update(derive_v2(report, graph, source), native_source_identity=identity, source_graph=graph,
                      primary_report=str(args.matrix_report.resolve()), primary_report_sha256=v1.digest(raw))
    except (core.native.AuditError, OSError, KeyError, ValueError, TypeError) as error:
        result.update(status="INVALID", diagnostics=[core.issue("INVALID", "CONVERSION_SUPPLEMENT_UNINTERPRETABLE", message=str(error))])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "report": str(args.report)}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
