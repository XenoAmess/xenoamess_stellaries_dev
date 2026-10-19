"""Second-process archive verification: no full SAV parsing, UI or log access."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import zipfile

PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT / "tools"))
import publish_1019 as gate


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main(branch):
    folder = PROJECT / "docs/evidence/1019-rc6-economy" / branch
    output = folder / "byte-verification-v1.json"
    if output.exists():
        raise FileExistsError(output)
    index_path = folder / "archive-index.json"
    index = load(index_path)
    checks = {"all_original_source_and_archive_bytes_match": all(
        sha(Path(f["source"])) == f["sha256"] == sha(folder / f["path"]) and (folder / f["path"]).stat().st_size == f["bytes"] for f in index["files"])}
    metadata = {".gitattributes", "archive-index.json", "native-branch-report.json", "payload-proposal.json"}
    payload_path = folder / "payload-proposal.json"
    report_path = folder / "native-branch-report.json"
    supplement = folder / "archive-supplement-v2.json"
    if supplement.exists():
        metadata |= {"archive-supplement-v2.json", "native-branch-report-v2.json", "payload-proposal-v2.json", "native-economic-categories-primary.txt"}
        original, revised, extra = load(report_path), load(folder / "native-branch-report-v2.json"), load(supplement)
        checks["original_FAIL_retained"] = original["status"] == "FAIL" and original["startup_checks"]["normal_upkeep"] is False
        checks["upkeep_correction_preserves_all_raw_states_and_budgets"] = original["native_states"] == revised["native_states"] and original["economy_checks"] == revised["economy_checks"]
        checks["supplement_references_match"] = all(gate.reference_path(extra[k], PROJECT).is_file() for k in ["original_index", "original_FAIL", "corrected_report", "corrected_payload", "primary", "collector"])
        payload_path, report_path = folder / "payload-proposal-v2.json", folder / "native-branch-report-v2.json"
    expected = metadata | {f["path"] for f in index["files"]}
    checks["exact_completed_archive_file_set"] = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()} == expected
    checks["raw_byte_text_attribute"] = (folder / ".gitattributes").read_bytes() == b"* -text\n"
    save_rows = []
    for f in index["files"]:
        path = folder / f["path"]
        if path.suffix != ".sav":
            continue
        audit = load(path.with_suffix(".audit.json"))
        receipt_path = path.with_suffix(".native-save.json")
        if not receipt_path.exists():
            receipt_path = folder / (path.stem + "-receipt.json")
        receipt = load(receipt_path)
        with zipfile.ZipFile(path) as archive:
            crc = archive.testzip() is None
            gamestate_sha = hashlib.sha256(archive.read("gamestate")).hexdigest()
        save_rows.append({"path": path.name, "date": audit["date"], "bound": crc and sha(path) == audit["save_sha256"] == receipt["sha256"] and
                          gamestate_sha == audit["gamestate_sha256"] and audit["date"] == receipt["date"]})
    checks["all14_native_zip_audit_receipt_sets_bound"] = len(save_rows) == 14 and all(row["bound"] for row in save_rows)
    payload = load(payload_path)
    report = load(report_path)
    checks["exact_startup_and_economy_schema_check_names"] = all(set(case["checks"]) == gate.CASE_CHECKS[name] for name, case in payload["cases"].items())
    checks["case_statuses_still_PENDING"] = all(case["status"] == "PENDING" for case in payload["cases"].values())
    checks["four_operation_constraints_not_fabricated"] = all(payload["cases"][branch + "_economy"]["checks"][key] is None
        for key in ["no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband"])
    checks["portable_case_evidence_sources_match"] = all(gate.reference_path(e, PROJECT).is_file() for case in payload["cases"].values() for e in case["evidence"])
    for role in ["baseline_months", "candidate_months"]:
        rows = payload["economy"][branch][role]
        checks[role + "_12_actual_dates_and_references"] = len(rows) == 12 and all(
            row["date"] == f"{2200 + i // 12:04}.{i % 12 + 1:02}.01" and type(row["net_energy"]) in [int, float] and math.isfinite(row["net_energy"]) and
            row["evidence"]["kind"] == "native_save" and gate.reference_path(row["evidence"], PROJECT).is_file() for i, row in enumerate(rows, 1))
    checks["report_is_scoped_and_budget_facts_pass"] = report["status"] == "PASS_SCOPED" and all(report["startup_checks"].values()) and report["economy_checks"]["all_net_energy_nonnegative"] is True
    result = {"schema": "eep.rc6.economy_thin_archive_verify.v1", "status": "PASS_BYTES_AND_SCOPED_PAYLOAD" if all(checks.values()) else "FAIL",
              "branch": branch, "checks": checks, "native_saves": save_rows, "index_sha256": sha(index_path),
              "report_sha256": sha(report_path), "payload_sha256": sha(payload_path), "verifier_sha256": sha(Path(__file__)),
              "scope": "Original bytes, native ZIP/receipts and portable scoped payload only; no UI/action/log review or whole-case acceptance"}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "failures": [k for k, v in checks.items() if not v], "output_sha256": sha(output)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", choices=["purifier", "hive", "machine"], required=True)
    main(parser.parse_args().branch)
