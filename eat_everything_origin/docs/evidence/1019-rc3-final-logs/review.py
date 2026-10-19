"""Account for every line of the frozen error/game logs without suppression."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
GAME = Path(r"C:\SteamLibrary\steamapps\common\Stellaris")
STAMP = re.compile(r"^\[\d\d:\d\d:\d\d\]")


def file_info(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": sha256(data).hexdigest()}


def excerpt(path, lo, hi):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    return {**file_info(path), "line_start": lo, "line_end": hi,
            "lines": [{"line": i + 1, "text": lines[i]} for i in range(lo - 1, hi)]}


def records(path):
    lines = path.read_bytes().decode("utf-8-sig", errors="strict").splitlines()
    output = []
    for number, line in enumerate(lines, 1):
        if STAMP.match(line) or not output:
            output.append({"line_start": number, "line_end": number, "lines": [line]})
        else:
            output[-1]["line_end"] = number
            output[-1]["lines"].append(line)
    assert sum(r["line_end"] - r["line_start"] + 1 for r in output) == len(lines)
    return lines, output


def main():
    baseline = DOCS / "evidence/1019-baseline/logs-final/error.log"
    baseline_lines = baseline.read_text(encoding="utf-8-sig").splitlines()
    error_lines, error_records = records(OUT / "logs/error.log")
    game_lines, game_records = records(OUT / "logs/game.log")
    baseline_matches = []
    for i in range(23):
        assert STAMP.sub("", baseline_lines[i]) == STAMP.sub("", error_lines[i]), i + 1
        baseline_matches.append({"rc3_line": i + 1, "baseline_line": i + 1})
    for record in error_records:
        text = record["lines"][0]
        if "[dlc.cpp:1847]: Could not find files for mod:" in text:
            category = "baseline_mod_discovery_warning"
            reason = "Same message and Workshop path as baseline; manifest enables only mod/ugc_eep-1019.mod. Not evidence those missing Workshop mods were loaded."
        elif "Object with key: decision_lithoid_swarm_consume_world already exists" in text:
            category = "baseline_intentional_native_decision_override"
            reason = "Matches baseline; engine explicitly selects common/decisions/zz_eep_native_decision.txt:2. Warning retained, not silently filtered."
        elif 'Could not find containerWindowType "portrait_container"' in text:
            category = "baseline_native_empire_picker_warning"
            reason = "Matches baseline native interface/select_empire_design.gui user_empire_design_entry_narrow warning; not proof of the separate EEP05 design-validity cause."
        elif "failed for missing args: export_modifier_to_variable, modifier, variable" in text:
            category = "recorded_hw0_manual_diagnostic_failure"
            reason = "UTC09:43:35 submitted diagnostic receipt uses unsupported every_ship; paired compiler failure. No successful hw0 diagnostic export claimed."
        elif "Invalid scripted effect: every_ship" in text:
            category = "recorded_hw0_manual_diagnostic_failure"
            reason = "Exact unsupported token occurs in hw0-export-command.action.json; recorded in acceptance-1019-plan.md. No file path, line1 means console fragment here."
        elif "Invalid context switch [from]" in text and "events/nomads_events_1.txt line: 2268" in text:
            category = "new_native_event_error_cause_unresolved"
            reason = "Native nomads.94 trigger switches to from; captured from country id is 4294967295. Native source proven, causal relationship to EEP/PK and gameplay impact unresolved. Do not call harmless or exclude from acceptance."
        else:
            category = "unknown_error_record"
            reason = "Unclassified record retained in full; requires investigation."
        record.update(category=category, reason=reason)
    for record in game_records:
        text = record["lines"][0]
        if "Game Version: Cygnus v4.5.2" in text:
            category = "native_version_information"
        elif " defines loaded" in text:
            category = "native_defines_information"
        elif "Sending sync response, machine id:" in text:
            category = "native_sync_information"
        elif "Generating World! Specified Seed:" in text:
            category = "native_world_generation_information"
        elif "[eventcommands.cpp:88]: Event eep.10 added info about event selection." in text:
            category = "eep_event_option_selection_information"
        elif "[eventcommands.cpp:88]: Event " in text and " added info about event selection." in text:
            category = "native_event_option_selection_information"
        else:
            category = "unknown_game_record"
        record.update(category=category,
                      reason="Retained informational record; event selection/generation alone does not prove event effects, branch identity or a complete case passed."
                      if not category.startswith("unknown") else "Unclassified game record retained in full.")
    manual = DOCS / "evidence/1019-rc3-hardware/hw0-export-command.action.json"
    assert manual.is_file(), manual
    manual_json = json.loads(manual.read_text(encoding="utf-8"))
    assert "every_ship" in manual_json["text"] and manual_json["submitted"] is True
    review = {"schema": "eep.rc3.final-log-review.v1", "status": "REVIEWED_WITH_UNRESOLVED_NATIVE_ERROR",
              "reviewed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T092935Z",
              "scope": "Complete error.log and game.log; all 19 logs archived, other 17 retained without a claim of semantic review",
              "archive_index_sha256": sha256((OUT / "index.json").read_bytes()).hexdigest(),
              "error_log": {**file_info(OUT / "logs/error.log"), "physical_lines": len(error_lines),
                            "timestamped_records": len(error_records), "records": error_records,
                            "categories": dict(Counter(x["category"] for x in error_records))},
              "game_log": {**file_info(OUT / "logs/game.log"), "physical_lines": len(game_lines),
                           "timestamped_records": len(game_records), "records": game_records,
                           "categories": dict(Counter(x["category"] for x in game_records))},
              "baseline_comparison": {**file_info(baseline), "comparison": "Timestamp prefix removed only; all other characters identical", "matches": baseline_matches},
              "manual_diagnostic_proof": {**file_info(manual), "receipt": manual_json,
                                         "existing_document": "docs/acceptance-1019-plan.md:223"},
              "native_source_evidence": [excerpt(GAME / "events/nomads_events_1.txt", 2256, 2275),
                                         excerpt(GAME / "common/on_actions/00_on_actions.txt", 2627, 2641),
                                         excerpt(GAME / "common/on_actions/00_on_actions.txt", 4496, 4503)],
              "new_diagnostics_naming_eep_script_files_beyond_baseline": [],
              "unknown_error_records": [x for x in error_records if x["category"] == "unknown_error_record"],
              "unknown_game_records": [x for x in game_records if x["category"] == "unknown_game_record"],
              "unresolved_native_error_count": sum(x["category"] == "new_native_event_error_cause_unresolved" for x in error_records),
              "acceptance_status": {"pk_90_day_charge_30_day_fire": "FAIL_UNCHANGED", "Machine_final_case": "PENDING", "Hive_final_case": "PENDING"},
              "limitations": ["No clean/zero-error claim: new native nomads.94 context error remains unresolved.",
                              "Absence of diagnostics naming EEP scripts cannot prove absence of EEP logic or timing defects.",
                              "Logs from multiple new games share this run; do not assign every record to Machine/Hive solely from log timing.",
                              "No game launch, UI interaction, savegame copy, Steam action or Mod modification performed."]}
    (OUT / "review.json").write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": review["status"], "error_categories": review["error_log"]["categories"],
                      "game_categories": review["game_log"]["categories"],
                      "error_lines": len(error_lines), "game_lines": len(game_lines),
                      "unresolved_native_errors": review["unresolved_native_error_count"]}, indent=2))


if __name__ == "__main__":
    main()
