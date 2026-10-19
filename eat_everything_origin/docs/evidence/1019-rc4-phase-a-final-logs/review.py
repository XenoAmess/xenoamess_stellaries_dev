"""Classify every final phase-A error/game/debug line; keep unresolved context."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
ARTIFACT = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z")
STAMP = re.compile(r"^\[\d\d:\d\d:\d\d\]")
SOURCES = {}


def info(path):
    data = path.read_bytes()
    SOURCES[str(path.resolve())] = {"path": str(path.resolve()), "bytes": len(data), "sha256": sha256(data).hexdigest()}
    return SOURCES[str(path.resolve())]


def parsed(path):
    lines = path.read_bytes().decode("utf-8-sig", errors="strict").splitlines()
    records = []
    for number, line in enumerate(lines, 1):
        if STAMP.match(line) or not records:
            records.append({"line_start": number, "line_end": number, "lines": [line]})
        else:
            records[-1]["lines"].append(line)
            records[-1]["line_end"] = number
    assert sum(r["line_end"] - r["line_start"] + 1 for r in records) == len(lines)
    return lines, records


def main():
    error_lines, error_records = parsed(OUT / "logs/error.log")
    game_lines, game_records = parsed(OUT / "logs/game.log")
    debug_lines, debug_records = parsed(OUT / "logs/debug.log")
    baseline_path = DOCS / "evidence/1019-baseline/logs-final/error.log"
    baseline = baseline_path.read_text(encoding="utf-8-sig").splitlines()
    for number in range(22):
        assert STAMP.sub("", baseline[number]) == STAMP.sub("", error_lines[number])
    debug_baseline = DOCS / "evidence/1019-baseline/logs-final/debug.log"
    assert [STAMP.sub("", x) for x in debug_baseline.read_text(encoding="utf-8-sig").splitlines()] == [STAMP.sub("", x) for x in debug_lines]
    bad_path = ARTIFACT / "pk2-repeat-completion-twice-command.action.json"
    bad = json.loads(bad_path.read_text(encoding="utf-8"))
    assert bad["submitted"] is True and bad["text"].count("on_destroy_planet_with_EEP_PLANET_KILLER_DISMANTLE") == 2
    canonical = DOCS / "evidence/1019-rc4-pk2-duration"
    preserved_bad = canonical / "phase3/pk2-repeat-completion-twice-command.action.json"
    assert bad_path.read_bytes() == preserved_bad.read_bytes()
    control_path = DOCS / "evidence/1019-native-cracker-control/analysis.json"
    control = json.loads(control_path.read_text(encoding="utf-8"))
    stages = control["snapshots"]
    assert (OUT / "logs/error.log").read_bytes() == (ARTIFACT / "pk2nativecontrol-R-after-restore.error.log").read_bytes()
    assert [x["bytes"] for x in stages] == [3200, 3200, 3575, 3575]
    callback_records = stages[2]["delta_records"]
    assert len(callback_records) == 1 and callback_records[0]["category"] == "nomads_94_invalid_from"
    for row in error_records:
        text = row["lines"][0]
        if "Could not find files for mod:" in text:
            category = "baseline_mod_discovery_warning"
            reason = "Same Workshop-path message as baseline after removing timestamp only; manifest enables only the candidate Mod."
        elif "decision_lithoid_swarm_consume_world already exists" in text:
            category = "baseline_intentional_native_consume_override"
            reason = "Same baseline warning; engine uses common/decisions/zz_eep_native_decision.txt:2. Retained explicitly."
        elif "on_destroy_planet_with_EEP_PLANET_KILLER_DISMANTLE" in text:
            category = "proven_invalid_operator_DISMANTLE_trial_input"
            reason = "20:05:42 matches UTC12:05:41.730877 submitted receipt containing the wrong callback twice. Not the production DEVOURER name; the failed trial is not a successful dedup test."
        elif "[20:09:31]" in text and "nomads_events_1.txt line: 2268" in text:
            category = "native_nomads_error_after_EEP_actual_shot_branch"
            reason = "Present in the pre-control B prefix and v3 shot/next-day-cleanup branch evidence. Exact engine hook/causal propagation remains unresolved; retained, not declared harmless."
        elif "[20:20:06]" in text and "nomads_events_1.txt line: 2268" in text:
            category = "native_nomads_error_in_original_CRACKER_callback_control"
            reason = "Exact P-to-Q 375-byte interval after explicit original completion callback plus two days, Mother fleet FROM; not actual native weapon firing."
        else:
            category = "unknown_error_record_retained"
            reason = "No silent suppression; requires investigation."
        row.update(category=category, reason=reason)
    for row in game_records:
        text = row["lines"][0]
        category = ("version_information" if "Game Version:" in text else
                    "defines_information" if " defines loaded" in text else
                    "native_event_option_information" if "Event first_contact.1 added info about event selection." in text else
                    "unknown_game_record_retained")
        row.update(category=category, reason="Informational record, no functional acceptance inferred." if not category.startswith("unknown") else "Unclassified record retained in full.")
    for row in debug_records:
        row.update(category="baseline_native_building_category_warning_unidentified_object",
                   reason="Matches baseline after timestamp removal. Native building_type.cpp warning gives no building key; object identity and impact unresolved, not declared harmless.")
    source_paths = [baseline_path, debug_baseline, bad_path, preserved_bad, control_path,
                    DOCS / "evidence/1019-native-cracker-control/verify.json",
                    canonical / "archive-index-v3.json", canonical / "archive-verification-v3.json",
                    canonical / "phase3/analysis/rc4-pk2-native-duration-report-v2.json",
                    canonical / "phase3/analysis/rc4-pk2-valid-callback-reload-dedup-report-v1.json",
                    canonical / "phase3/analysis/rc4-pk2-complete-errorlog-sample-v1.json",
                    ARTIFACT / "pk2nativecontrol-log-receipt.json", ARTIFACT / "pk2nativecontrol-R-after-restore.error.log"]
    for path in source_paths:
        info(path)
    logs = {}
    for name, lines, records in (("error.log", error_lines, error_records), ("game.log", game_lines, game_records), ("debug.log", debug_lines, debug_records)):
        logs[name] = {**info(OUT / "logs" / name), "physical_lines": len(lines), "timestamped_records": len(records),
                      "categories": dict(Counter(x["category"] for x in records)), "records": records}
    report = {"schema": "eep.rc4.phase-a.final-log-review.v1", "status": "REVIEWED_WITH_NATIVE_ERRORS_UNRESOLVED",
              "reviewed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T112808Z",
              "index_sha256": sha256((OUT / "index.json").read_bytes()).hexdigest(),
              "scope": "Complete final error/game/debug semantic review; all 19 logs archived, other logs retained without semantic-acceptance claim",
              "logs": logs, "operator_failure_proof": {"source": info(bad_path), "receipt": bad},
              "final_error_bytes_equal_control_R": True,
              "new_error_bytes_after_control_R_through_process_stop": 0,
              "raw_nomads_diagnostics": 2, "unknown_error_records": sum(x["category"].startswith("unknown") for x in error_records),
              "unknown_game_records": sum(x["category"].startswith("unknown") for x in game_records),
              "unresolved_native_causal_errors": 2, "unidentified_baseline_building_warning": 1,
              "runtime_acceptance": "NOT_ASSIGNED", "sources": list(SOURCES.values()),
              "limitations": ["Native source path/baseline match does not prove harmlessness; nomads exact hook/propagation and debug building identity remain unresolved.",
                  "The wrong DISMANTLE input is a documented failed operator trial, not a successful production callback/dedup check.",
                  "Original CRACKER was a manual completion callback inside an enabled EEP candidate game, not a Mod-free or actual-native-weapon test.",
                  "Final error log adds no bytes after control R, but absence of new diagnostics is not a jump/Relic/migration/economy/growth or whole-Mod PASS.",
                  "RC3 timing FAIL and other historical evidence are unchanged; no old/public profile or subsequent process logs included."]}
    (OUT / "review.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "logs": {k: {"physical_lines": v["physical_lines"], "records": v["timestamped_records"], "categories": v["categories"]} for k, v in logs.items()},
                      "final_equals_R": True}, indent=2))


if __name__ == "__main__":
    main()
