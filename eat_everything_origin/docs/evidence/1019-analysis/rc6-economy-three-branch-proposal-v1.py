"""Combine completed immutable proposals; never promotes a case to PASS."""
import hashlib
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
BASE = PROJECT / "docs/evidence/1019-rc6-economy"
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def ref(path):
    return {"path": path.relative_to(PROJECT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "kind": "analysis"}


def write(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    targets = {"purifier": ("r6pu", "-v2"), "hive": ("r6hvc", ""), "machine": ("r6mc", "")}
    missing = [branch for branch in targets if not (BASE / branch / "byte-verification-v1.json").exists()]
    if missing:
        print(json.dumps({"status": "PENDING", "missing_complete_verified_branches": missing}))
        return
    cases, economies, summaries, proofs = {}, {}, {}, {}
    for branch, (prefix, suffix) in targets.items():
        folder = BASE / branch
        report_path, payload_path = folder / ("native-branch-report" + suffix + ".json"), folder / ("payload-proposal" + suffix + ".json")
        report, payload, verification = load(report_path), load(payload_path), load(folder / "byte-verification-v1.json")
        assert verification["status"] == "PASS_BYTES_AND_SCOPED_PAYLOAD" and all(verification["checks"].values())
        assert verification["report_sha256"] == ref(report_path)["sha256"] and verification["payload_sha256"] == ref(payload_path)["sha256"]
        assert report["run_id"] == "20261019T150008Z" and report["version"] == "0.4.0-rc.6" and report["production_tree_sha256"] == TREE and report["prefix"] == prefix
        assert report["status"] == "PASS_SCOPED"
        assert all(case["status"] == "PENDING" for case in payload["cases"].values())
        cases.update(payload["cases"])
        economies.update(payload["economy"])
        states = report["native_states"]
        summaries[branch] = {"prefix": prefix, "initial_energy": states[0]["country"]["stockpile"].get("energy"),
            "final_energy": states[12]["country"]["stockpile"].get("energy"), "first_month_net": states[1]["energy"]["net"],
            "last_month_net": states[12]["energy"]["net"], "minimum_monthly_net": min(s["energy"]["net"] for s in states[1:13]),
            "baseline_delta_min": min(row["difference"] for row in report["monthly_baseline_delta"]),
            "baseline_delta_max": max(row["difference"] for row in report["monthly_baseline_delta"]),
            "initial_core_population": states[0]["core_population"], "first_month_generator_jobs": report["first_month_generator_jobs"],
            "startup_checks": report["startup_checks"], "native_constraints": report["observed_constraints"],
            "auto_ui_fields_equal": report["auto_ui_comparison"]["all_fields_equal"]}
        proofs[branch] = {"report": ref(report_path), "payload": ref(payload_path), "original_archive_index": ref(folder / "archive-index.json"),
                         "byte_verification": ref(folder / "byte-verification-v1.json")}
    assert len(cases) == 6 and len(economies) == 3
    result = {"schema": "eep.rc6.three_branch_startup_economy_payload.v1", "status": "PENDING_CASE_EVIDENCE_ASSEMBLY",
              "run_id": "20261019T150008Z", "version": "0.4.0-rc.6", "production_tree_sha256": TREE,
              "cases": cases, "economy": economies, "source_proposals": proofs,
              "limitations": ["Only six startup/economy case proposals; no eighteen-case final result.",
                  "All case statuses remain PENDING, and four operational economic flags per branch remain null pending recorded-input review.",
                  "No UI, screenshot, action-chain, final-log review or release PASS is synthesized."]}
    write(BASE / "three-branch-payload-proposal-v1.json", result)
    summary = {"schema": "eep.rc6.three_branch_startup_economy_summary.v1", "status": "PASS_SCOPED_NATIVE_FACTS_ONLY",
               "branches": summaries, "evidence": proofs, "combined_payload": ref(BASE / "three-branch-payload-proposal-v1.json"),
               "collector": ref(Path(__file__)), "complete_cases": "PENDING"}
    write(BASE / "three-branch-native-summary-v1.json", summary)
    print(json.dumps({"status": summary["status"], "summary": ref(BASE / "three-branch-native-summary-v1.json"),
                      "payload": summary["combined_payload"]}, indent=2))


if __name__ == "__main__":
    main()
