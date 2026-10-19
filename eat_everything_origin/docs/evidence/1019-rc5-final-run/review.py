"""Review complete stopped RC5 diagnostics and preserve scoped result limits."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
STAMP = re.compile(r"^\[\d\d:\d\d:\d\d\]")


def fp(path):
    body = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(body), "sha256": sha256(body).hexdigest()}


def parse(path):
    lines = path.read_bytes().decode("utf-8-sig", errors="strict").splitlines()
    records = []
    for n, line in enumerate(lines, 1):
        if STAMP.match(line) or not records:
            records.append({"line_start": n, "line_end": n, "lines": [line]})
        else:
            records[-1]["lines"].append(line)
            records[-1]["line_end"] = n
    assert [line for row in records for line in row["lines"]] == lines
    return lines, records


def main():
    baseline = OUT.parent / "1019-baseline/logs-final"
    error_lines, errors = parse(OUT / "logs/error.log")
    game_lines, games = parse(OUT / "logs/game.log")
    debug_lines, debugs = parse(OUT / "logs/debug.log")
    assert [STAMP.sub("", x) for x in error_lines] == [STAMP.sub("", x) for x in (baseline / "error.log").read_text(encoding="utf-8-sig").splitlines()[:22]]
    assert [STAMP.sub("", x) for x in debug_lines] == [STAMP.sub("", x) for x in (baseline / "debug.log").read_text(encoding="utf-8-sig").splitlines()]
    for row in errors:
        text = "\n".join(row["lines"])
        category = ("baseline_mod_discovery_warning" if "Could not find files for mod:" in text else
                    "baseline_intentional_native_consume_override" if "decision_lithoid_swarm_consume_world already exists" in text else "unknown_error_record_retained")
        row.update(category=category, reason="Exact baseline message after timestamp removal; preserved, no runtime PASS inferred." if not category.startswith("unknown") else "Unclassified original retained.")
    for row in games:
        text = "\n".join(row["lines"])
        category = "version_information" if "Game Version:" in text else "defines_information" if " defines loaded" in text else "unknown_game_record_retained"
        row.update(category=category, reason="Informational only; no runtime acceptance inferred.")
    for row in debugs:
        row.update(category="baseline_native_building_category_warning_unidentified_object", reason="Same baseline native warning; specific building key and impact remain UNKNOWN.")
    logs = {}
    for name, lines, rows in (("error.log", error_lines, errors), ("game.log", game_lines, games), ("debug.log", debug_lines, debugs)):
        logs[name] = {**fp(OUT / "logs" / name), "physical_lines": len(lines), "record_count": len(rows),
                      "categories": dict(Counter(row["category"] for row in rows)), "records": rows}
    report_paths = [OUT / "analysis" / name for name in ("rc5-public031-autoload-reload-report-v1.json", "rc5-six-core-layout-guard-report-v1.json", "native-current-ship-health-setter-calibration-report-v1.json")]
    results = []
    for path in report_paths:
        data = json.loads(path.read_bytes())
        results.append({**fp(path), "status": data["status"], "scope": data["scope"], "checks_total": len(data["checks"]),
                        "checks_true": sum(value is True for value in data["checks"].values()),
                        "failed_checks": [key for key, value in data["checks"].items() if value is False]})
    sources = report_paths + [baseline / "error.log", baseline / "debug.log", OUT / "source-binding.json", OUT / "verify.json",
                             OUT.parent / "1019-rc4-phase-a-final-logs/review.json", OUT.parent / "1019-native-cracker-control/analysis.json",
                             OUT.parent / "1019-rc4-phase-b-final-run/review.json"]
    report = {"schema": "eep.rc5.final-log-and-results-review.v1", "status": "LOGS_REVIEWED_RC5_MIGRATION_FAIL_RETAINED",
              "reviewed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T143452Z",
              "index_sha256": fp(OUT / "index.json")["sha256"], "logs": logs, "results": results,
              "scope": "Complete error/game/debug review; 19 final logs preserved; baseline-only diagnostics do not validate gameplay",
              "unknown_error_records": sum(row["category"].startswith("unknown") for row in errors),
              "unknown_game_records": sum(row["category"].startswith("unknown") for row in games),
              "new_EEP_error_records_this_run": sum("eep_" in "\n".join(row["lines"]) and row["category"].startswith("unknown") for row in errors),
              "nomads94_diagnostics_this_run": sum("nomads_events_1.txt line: 2268" in "\n".join(row["lines"]) for row in errors),
              "historical_nomads94_status": "UNEXPLAINED; historical EEP actual-shot branch and manual original-CRACKER callback control remain intact",
              "rootflags_marker_limit": "Root flags occurrence does not establish a design-local marker or universal shared design-flag mechanism",
              "Welcome_first_attempt": "Root-reported corrupted requested Chinese label; no click submitted; first original image/OCR preserved; UTF8 retry click preserved",
              "native_health_scope": "Only actual ordinary ship3 corvette -> NAME_Relic setter and native reload; target current/max exact after reload; setter 1e-6 three-layer failures and Mother reversion remain failures",
              "not_executed": ["talon health branch", "old nrelsrc Relic health branch"],
              "source_boundary": "RC5 copied tree1cc8b and original runtime84b; nine postrun hash-bound tools; no prepare execution-source directory or memory loaded-source proof; changing indirect publish dependencies not retrofitted; new health v2 excluded",
              "sources": [fp(p) for p in sources], "Mod_acceptance_pass": False,
              "limits": ["No EEP diagnostics here does not override the 9 migration/reload FAIL checks.", "The identical guard SAV 26/26 result has no actual native reload guarantee.", "Health 36/40 observations do not establish universal engine arithmetic precision or Mother repair success.", "Native baseline debug warning's object identity and impact remain UNKNOWN.", "No RC6/new-run/current ROOT Mod data or revised v2 thresholds used."]}
    (OUT / "review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "logs": {name: {k: value[k] for k in ("physical_lines", "record_count", "categories")} for name, value in logs.items()}, "results": [{"status": row["status"], "checks": row["checks_total"], "true": row["checks_true"], "false": len(row["failed_checks"])} for row in results]}, indent=2))


if __name__ == "__main__":
    main()
