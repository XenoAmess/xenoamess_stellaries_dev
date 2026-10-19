"""Review every stopped error/game/debug record; retain all unresolved warnings."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
STAMP = re.compile(r"^\[\d\d:\d\d:\d\d\]")


def fp(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "sha256": sha256(data).hexdigest()}


def records(path):
    lines = path.read_bytes().decode("utf-8-sig", errors="strict").splitlines()
    result = []
    for n, line in enumerate(lines, 1):
        if STAMP.match(line) or not result:
            result.append({"line_start": n, "line_end": n, "lines": [line]})
        else:
            result[-1]["lines"].append(line)
            result[-1]["line_end"] = n
    assert sum(x["line_end"] - x["line_start"] + 1 for x in result) == len(lines)
    return lines, result


def main():
    baseline = OUT.parent / "1019-baseline/logs-final"
    error_lines, errors = records(OUT / "logs/error.log")
    game_lines, games = records(OUT / "logs/game.log")
    debug_lines, debugs = records(OUT / "logs/debug.log")
    base_error = (baseline / "error.log").read_text(encoding="utf-8-sig").splitlines()
    assert [STAMP.sub("", x) for x in error_lines[:22]] == [STAMP.sub("", x) for x in base_error[:22]]
    assert [STAMP.sub("", x) for x in debug_lines] == [STAMP.sub("", x) for x in (baseline / "debug.log").read_text(encoding="utf-8-sig").splitlines()]
    variable_records = []
    for row in errors:
        text = "\n".join(row["lines"])
        if "Could not find files for mod:" in text:
            category = "baseline_mod_discovery_warning"
            reason = "Same baseline Workshop-path message after timestamp removal; retained, not evidence of another enabled Mod."
        elif "decision_lithoid_swarm_consume_world already exists" in text:
            category = "baseline_intentional_native_consume_override"
            reason = "Same baseline duplicate decision warning; engine uses zz_eep_native_decision.txt:2."
        elif "[variable_values.cpp:236]" in text and "common/scripted_effects/eep_mothership_effects.txt" in text:
            category = "EEP_migration_sync_unset_variable_runtime_warning"
            reason = "EEP execution stack explicitly resolves a missing variable during migration sync; actual cause remains UNKNOWN. Raw serialized zeros in later SAV do not disprove the runtime warning."
            match = re.search(r"Variable (\S+) is not set for scoped (country|fleet) '([^']+)'", text)
            assert match
            row["variable"] = match.group(1)
            row["native_scope"] = match.group(2)
            row["native_scope_name"] = match.group(3)
            row["stack_source_lines"] = [int(x) for x in re.findall(r"eep_mothership_effects\.txt:(\d+)", text)]
            variable_records.append(row)
        else:
            category = "unknown_error_record_retained"
            reason = "No silent suppression; original text remains for further investigation."
        row.update(category=category, reason=reason)
    for row in games:
        text = "\n".join(row["lines"])
        category = ("version_information" if "Game Version:" in text else "defines_information" if " defines loaded" in text else "unknown_game_record_retained")
        row.update(category=category, reason="Information only; no acceptance inferred." if not category.startswith("unknown") else "Unclassified original retained.")
    for row in debugs:
        row.update(category="baseline_native_building_category_warning_unidentified_object",
                   reason="Same baseline native building_type.cpp warning after timestamp removal; no object key provided, object identity and impact unresolved.")
    observed = json.loads((OUT / "analysis/rc4-migration-unset-variable-log-report-v1.json").read_bytes())
    assert observed["log_sha256"] == fp(OUT / "logs/error.log")["sha256"] and observed["log_bytes"] == len((OUT / "logs/error.log").read_bytes())
    assert observed["findings"]["execution_time_variable_resolution_cause"] == "UNKNOWN"
    size = json.loads((OUT / "analysis/rc4-mobile-starbase-size-probe-report-v1.json").read_bytes())
    assert size["status"] == "FAIL"
    sources = [baseline / "error.log", baseline / "debug.log", OUT / "analysis/rc4-migration-unset-variable-log-report-v1.json",
               OUT / "analysis/rc4-mobile-starbase-size-probe-report-v1.json", OUT / "analysis/native-relic-health-calibration-source-v1.json",
               OUT.parent / "1019-rc4-phase-a-final-logs/review.json", OUT.parent / "1019-native-cracker-control/analysis.json",
               OUT.parent / "1019-rc4-midrun-capture-tool-supplement-v1/index.json",
               OUT.parent / "1019-rc4-phase-b-migration-checkpoint-v1/index.json",
               OUT.parent / "1019-rc4-pk2-duration/copied_mod/common/scripted_effects/eep_mothership_effects.txt"]
    sources += [Path(item["path"]) for item in observed["snapshot_files"]]
    logs = {}
    for name, lines, rows in (("error.log", error_lines, errors), ("game.log", game_lines, games), ("debug.log", debug_lines, debugs)):
        logs[name] = {**fp(OUT / "logs" / name), "physical_lines": len(lines), "records_count": len(rows),
                      "categories": dict(Counter(row["category"] for row in rows)), "records": rows}
    report = {"schema": "eep.rc4.phase-b.final-log-review.v1", "status": "REVIEWED_WITH_EEP_WARNINGS_AND_FAILURES_UNRESOLVED",
              "reviewed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T133314Z",
              "index_sha256": fp(OUT / "index.json")["sha256"], "logs": logs,
              "scope": "Complete error/game/debug semantic review; all 19 final log files archived; other logs retained without semantic PASS",
              "EEP_variable_warning_count": len(variable_records),
              "EEP_variable_warning_counts_by_native_clock": dict(Counter(row["lines"][0][1:9] for row in variable_records)),
              "baseline_portrait_container_diagnostic_present_in_this_run": "portrait_container" in "\n".join(error_lines),
              "nomads_94_diagnostic_count_this_run": sum("nomads_events_1.txt line: 2268" in "\n".join(row["lines"]) for row in errors),
              "historical_nomads_94_status": "UNEXPLAINED; EEP shot branch and native CRACKER callback calibration remain preserved independently",
              "unknown_error_records": sum(row["category"].startswith("unknown") for row in errors),
              "unknown_game_records": sum(row["category"].startswith("unknown") for row in games),
              "baseline_building_object_identity_and_impact": "UNKNOWN",
              "earlier_readonly_warning_snapshot_equals_final_error_bytes": True,
              "rsizeonly_status": size["status"], "rsizeonly_failed_checks": [key for key, value in size["checks"].items() if value is False],
              "nrel_status": "SOURCE_IMPORT_ONLY; native_load HUD date guard failed, planned injury/save/export NOT_EXECUTED; play0 attempts guard-rejected before typing",
              "sources": [fp(p) for p in sorted(set(sources))], "Mod_acceptance": "NOT_PASSED",
              "limits": ["17 EEP runtime warnings are not baseline and are not ignored; saved zeros do not establish execution-time resolution order or cause.", "No nomads.94 diagnostic in this run does not resolve its historical cause or prove harmlessness.", "No new error bytes after the prior bounded warning snapshot does not prove the failed HUD load or direct probes passed.", "Original no-success-load/no-injury evidence remains intact; source import is not a native health calibration.", "Migration/size failures remain failures, tool source/benchmark acceptance is separate, RC3 timing FAIL is unchanged."]}
    (OUT / "review.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "logs": {name: {k: value[k] for k in ("physical_lines", "records_count", "categories")} for name, value in logs.items()}, "warning_clock_counts": report["EEP_variable_warning_counts_by_native_clock"], "nomads_this_run": report["nomads_94_diagnostic_count_this_run"], "rsizeonly_failed_checks": report["rsizeonly_failed_checks"]}, indent=2))


if __name__ == "__main__":
    main()
