"""Independent raw-byte, identity, completeness and classification audit."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent


def fp(path):
    raw = path.read_bytes()
    return len(raw), sha256(raw).hexdigest()


def main():
    assert not (OUT / "verify.json").exists(), "Sealed verification already exists"
    checks = {}
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    review = json.loads((OUT / "review.json").read_bytes())
    proof = json.loads((OUT / "process-independent.json").read_bytes())
    assert fp(OUT / "selection.json")[1] == index["selection_sha256"] and index["files"] == selection["files"]
    assert fp(OUT / "process-independent.json")[1] == index["process_independent_sha256"]
    assert fp(OUT / "archive.py")[1] == index["archive_script_sha256"]
    assert fp(OUT / "index.json")[1] == review["index_sha256"]
    assert fp(OUT / "review.py")[1] == review["review_script_sha256"]
    checks["index_selection_proof_and_scripts_bound"] = True
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"]), row["path"]
    assert len(index["files"]) == index["payload_file_count"] == 22
    assert sum(row["bytes"] for row in index["files"]) == index["payload_bytes"] == 5971299
    checks["all_22_payloads_match_source_bytes_and_sha256"] = True
    source_logs = Path(selection["fixed_userdir"]) / "logs"
    original_set = sorted(p.relative_to(source_logs).as_posix() for p in source_logs.rglob("*") if p.is_file())
    archived_set = sorted(p.relative_to(OUT / "logs").as_posix() for p in (OUT / "logs").rglob("*") if p.is_file())
    assert original_set == archived_set and len(original_set) == index["log_file_count"] == 19
    assert len([name for name in archived_set if name.startswith("script_documentation/")]) == 5
    assert sum((OUT / "logs" / name).stat().st_size for name in archived_set) == index["log_bytes"] == 5946297
    checks["complete_19_logs_and_5_script_documentation_files"] = True
    assert sorted(p.name for p in (OUT / "run").iterdir()) == ["manifest.json", "process.json", "stop.json"]
    assert not list(OUT.rglob("*.sav")) and all(row["path"].split("/")[0] in ("run", "logs") for row in index["files"])
    checks["only_three_run_metadata_no_sav_mod_or_growth_payload"] = True
    manifest = json.loads((OUT / "run/manifest.json").read_bytes())
    process = json.loads((OUT / "run/process.json").read_bytes())
    stop = json.loads((OUT / "run/stop.json").read_bytes())
    assert index["run_id"] == manifest["run_id"] == review["run_id"] == proof["run_id"] == "20261019T150008Z"
    assert index["pid"] == process["pid"] == process["launcher_pid"] == stop["pid"] == proof["expected_pid"] == 30812
    assert stop == index["stop"] and stop["stopped_at_utc"] == "2026-10-19T16:38:02.658777+00:00"
    assert stop["forced"] is False and stop["running_after"] is False
    assert process["command"] == manifest["launch_args"] and process["transport"] == "direct"
    assert Path(manifest["userdir"]) == Path(selection["fixed_userdir"])
    assert Path(manifest["artifact_dir"]) == Path(selection["fixed_artifact_path"])
    assert datetime.fromisoformat(manifest["prepared_at_utc"]) < datetime.fromisoformat(process["started_at_utc"]) < datetime.fromisoformat(stop["stopped_at_utc"]) < datetime.fromisoformat(proof["checked_at_utc"])
    assert proof["matched_processes"] == [] and proof["status"] == "ABSENT" and proof["query_exit_code"] == 0
    checks["normal_stop_manifest_process_identity_and_time_order"] = True
    query = ["powershell", "-NoProfile", "-NonInteractive", "-Command",
             "ConvertTo-Json -InputObject @(Get-CimInstance Win32_Process -Filter 'ProcessId=30812' -ErrorAction Stop | Select-Object ProcessId,Name,ExecutablePath,CommandLine,CreationDate) -Depth 4 -Compress"]
    response = subprocess.run(query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    assert json.loads(response.stdout.decode("utf-8-sig")) == [] and not response.stderr
    query_checked = datetime.now(timezone.utc).isoformat()
    checks["independent_second_os_query_confirms_pid_absent"] = True
    for row in index["canonical_references_not_copied"]:
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"]), row["path"]
    assert len(index["canonical_references_not_copied"]) == 8
    for name in ("manifest.json", "process.json"):
        assert fp(OUT / "run" / name) == fp(OUT.parent / "1019-rc6-migration-checkpoint-v1/run" / name)
    checks["eight_canonical_references_and_checkpoint_metadata_match"] = True
    static = OUT.parent / "1019-rc6-static"
    gate = json.loads((static / "candidate-rc6-gate.json").read_bytes())
    source_index = json.loads((static / "source-index.json").read_bytes())
    tree = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
    assert gate == manifest["static_gate"] and gate["source_tree_sha256"] == source_index["tree"] == index["source_tree_sha256"] == tree
    assert manifest["repository_mod_tree_sha256"] == manifest["copied_mod_tree_sha256"] == tree
    assert gate["files"] == manifest["repository_mod_files"] and len(gate["files"]) == 59
    assert gate["report_sha256"] == fp(static / "candidate-rc6-open-kaishek.json")[1]
    assert index["language"] == manifest["language"] == "l_simp_chinese"
    assert index["version"] == gate["version"] == "0.4.0-rc.6"
    checks["fixed_rc6_tree_and_static_metadata_bound_no_mod_recopied"] = True
    expected_counts = {
        "error.log": (24, 24, {"mod_discovery_missing_files": 21, "duplicate_decision_key_eep_override": 1, "missing_ui_portrait_container": 1, "eep_while_limit_100_abort": 1}),
        "game.log": (20, 20, {"version_information": 1, "defines_information": 2, "sync_response": 1, "world_generation_seed": 3, "event_selection": 13}),
        "system.log": (238, 220, {"graphics_adapter_device_and_capabilities": 21, "graphics_settings_and_capabilities": 7, "audio_device_driver_and_format": 8, "graphics_device_creation": 2, "display_mode_enumeration": 182}),
        "debug.log": (1, 1, {"building_category_lookup_failure": 1}),
    }
    complete_lines = {}
    for name, (physical, records, categories) in expected_counts.items():
        path = OUT / "logs" / name
        lines = path.read_bytes().decode("utf-8-sig", errors="strict").splitlines()
        complete_lines[name] = lines
        value = review["logs"][name]
        assert fp(path) == (value["bytes"], value["sha256"])
        assert len(lines) == physical == value["physical_lines"]
        assert len(value["records"]) == records == value["record_count"]
        assert dict(Counter(item["category"] for item in value["records"])) == value["categories"] == categories
        assert sum(bool(re.match(r"^\[\d\d:\d\d:\d\d\]", line)) for line in lines) == records
        assert [line for item in value["records"] for line in item["lines"]] == lines
        for item in value["records"]:
            assert item["lines"] == lines[item["line_start"] - 1:item["line_end"]]
    checks["all_283_physical_lines_and_265_records_reviewed_without_omission"] = True
    errors = complete_lines["error.log"]
    assert sum("Could not find files for mod:" in line for line in errors) == 21
    assert "decision_lithoid_swarm_consume_world already exists" in errors[21]
    assert 'Could not find containerWindowType "portrait_container"' in errors[22]
    assert "while effect limit never reached, aborting after 100 repetitions" in errors[23]
    assert "common/scripted_effects/eep_mothership_effects.txt:35" in errors[23]
    assert "eep_sync_mothership_components at common/scripted_effects/eep_mothership_effects.txt:195" in errors[23]
    assert len(review["eep_runtime_errors"]) == 1 and review["eep_runtime_errors"][0]["line_start"] == 24
    checks["all_error_classes_and_real_eep_while_abort_retained"] = True
    assert len(review["unresolved_diagnostic_records"]) == review["unresolved_diagnostic_record_count"] == 25
    assert sum(item["log"] == "error.log" for item in review["unresolved_diagnostic_records"]) == 24
    assert sum(item["log"] == "debug.log" for item in review["unresolved_diagnostic_records"]) == 1
    for item in review["unresolved_diagnostic_records"]:
        assert item["lines"] == complete_lines[item["log"]][item["line_start"] - 1:item["line_end"]]
    checks["all_25_diagnostics_remain_unresolved_or_unknown_impact"] = True
    assert not any("nomads" in line.lower() for lines in complete_lines.values() for line in lines)
    assert review["nomads_occurrences_in_four_reviewed_logs"] == []
    history = review["historical_nomads_reference"]
    assert fp(Path(history["path"])) == (history["bytes"], history["sha256"])
    old = json.loads(Path(history["path"]).read_bytes())
    assert old["status"] == "REVIEWED_WITH_NATIVE_ERRORS_UNRESOLVED" and old["raw_nomads_diagnostics"] == 2
    checks["historical_nomads_unresolved_status_preserved"] = True
    assert review["error_records_suppressed"] == 0 and not review["Mod_acceptance_pass"] and not index["Mod_acceptance_pass"]
    checks["no_filtered_errors_or_mod_acceptance_claim"] = True
    report = {"schema": "eep.rc6.final-logs-verification.v1", "status": "PASS_BYTE_IDENTITY_AND_REVIEW_COMPLETENESS_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "review_sha256": fp(OUT / "review.json")[1], "verifier_sha256": fp(Path(__file__))[1],
              "payload_files_rechecked": 22, "payload_bytes": 5971299, "complete_logs": 19,
              "complete_script_documentation": 5, "canonical_references_rechecked": 8,
              "reviewed_physical_lines": sum(v[0] for v in expected_counts.values()),
              "reviewed_records": sum(v[1] for v in expected_counts.values()),
              "diagnostic_records_retained": 25, "real_eep_while_abort_records": 1,
              "historical_nomads_still_unresolved": True, "checks": checks,
              "independent_process_query": {"command": query, "checked_at_utc": query_checked,
                                            "exit_code": response.returncode, "matched_processes": []},
              "Mod_acceptance_pass": False, "UI_invoked": False, "Git_invoked": False}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
