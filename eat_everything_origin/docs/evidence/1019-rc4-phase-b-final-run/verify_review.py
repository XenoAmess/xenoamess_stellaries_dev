"""Independently check complete review coverage, unchanged sources and failures."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def main():
    raw = (OUT / "review.json").read_bytes()
    review = json.loads(raw)
    assert review["index_sha256"] == sha256((OUT / "index.json").read_bytes()).hexdigest()
    for source in review["sources"]:
        body = Path(source["path"]).read_bytes()
        assert len(body) == source["bytes"] and sha256(body).hexdigest() == source["sha256"]
    for name, log in review["logs"].items():
        body = (OUT / "logs" / name).read_bytes()
        actual = body.decode("utf-8-sig", errors="strict").splitlines()
        assert len(body) == log["bytes"] and sha256(body).hexdigest() == log["sha256"]
        assert [line for row in log["records"] for line in row["lines"]] == actual
        assert len(actual) == log["physical_lines"] and len(log["records"]) == log["records_count"]
        assert dict(Counter(row["category"] for row in log["records"])) == log["categories"]
    assert review["logs"]["error.log"]["records_count"] == 39
    assert review["EEP_variable_warning_count"] == 17 and review["EEP_variable_warning_counts_by_native_clock"] == {"21:37:54": 12, "21:46:01": 5}
    assert review["nomads_94_diagnostic_count_this_run"] == 0 and review["historical_nomads_94_status"].startswith("UNEXPLAINED")
    assert review["rsizeonly_status"] == "FAIL" and len(review["rsizeonly_failed_checks"]) == 4
    assert review["Mod_acceptance"] == "NOT_PASSED"
    result = {"schema": "eep.rc4.phase-b.final-log-review-verification.v1", "status": "PASS_REVIEW_COVERAGE_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "review_sha256": sha256(raw).hexdigest(),
              "source_references_rechecked": len(review["sources"]), "error_records_fully_covered": 39,
              "game_records_fully_covered": 3, "debug_records_fully_covered": 1,
              "EEP_runtime_warnings_retained": 17, "rsizeonly_failed_checks_retained": 4,
              "historical_nomads94_unexplained_status_retained": True, "Mod_acceptance_pass": False}
    (OUT / "review-verify.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
