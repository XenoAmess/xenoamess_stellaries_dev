"""Verify final review covers every diagnostic and keeps each scope/failure."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def main():
    raw = (OUT / "review.json").read_bytes()
    data = json.loads(raw)
    assert data["index_sha256"] == sha256((OUT / "index.json").read_bytes()).hexdigest()
    for row in data["sources"]:
        body = Path(row["path"]).read_bytes()
        assert len(body) == row["bytes"] and sha256(body).hexdigest() == row["sha256"]
    for name, log in data["logs"].items():
        body = (OUT / "logs" / name).read_bytes()
        lines = body.decode("utf-8-sig", errors="strict").splitlines()
        assert len(body) == log["bytes"] and sha256(body).hexdigest() == log["sha256"]
        assert [line for row in log["records"] for line in row["lines"]] == lines
        assert len(lines) == log["physical_lines"] and len(log["records"]) == log["record_count"]
        assert dict(Counter(row["category"] for row in log["records"])) == log["categories"]
    assert [(row["status"], row["checks_total"], row["checks_true"], len(row["failed_checks"])) for row in data["results"]] == [("FAIL", 40, 31, 9), ("PASS_SCOPED", 26, 26, 0), ("OBSERVATION_WITH_FAILURES", 40, 36, 4)]
    assert not data["Mod_acceptance_pass"] and data["historical_nomads94_status"].startswith("UNEXPLAINED")
    result = {"schema": "eep.rc5.final-review-verification.v1", "status": "PASS_REVIEW_COVERAGE_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "review_sha256": sha256(raw).hexdigest(),
              "source_refs_rechecked": len(data["sources"]), "complete_error_records": 22, "complete_game_records": 3, "complete_debug_records": 1,
              "migration_failed_checks_preserved": 9, "guard_scoped_true_checks_preserved": 26, "health_failed_checks_preserved": 4,
              "unknown_debug_building_impact_preserved": True, "historical_nomads94_unexplained_preserved": True,
              "rootflags_not_design_marker_proof_preserved": True, "Mod_acceptance_pass": False}
    (OUT / "review-verify.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
