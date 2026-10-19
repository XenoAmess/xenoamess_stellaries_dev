"""Classify every final RC6 error/game/system/debug record without exemptions."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
STAMP = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]")


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
    return lines, records


def classify(name, text):
    if name == "error.log":
        if "Could not find files for mod:" in text:
            return "mod_discovery_missing_files", "UNKNOWN_IMPACT", "Engine diagnostic retained; external path does not establish harmlessness or loaded state."
        if "decision_lithoid_swarm_consume_world already exists" in text:
            return "duplicate_decision_key_eep_override", "UNKNOWN_IMPACT", "EEP replacement path is explicit; intendedness does not resolve runtime impact."
        if 'Could not find containerWindowType "portrait_container"' in text:
            return "missing_ui_portrait_container", "UNEXPLAINED", "Native GUI path recorded; cause, owner and impact remain unknown."
        if "while effect limit never reached" in text:
            return "eep_while_limit_100_abort", "UNEXPLAINED_REAL_EEP_RUNTIME_ERROR", "100-iteration abort explicitly names EEP scripted effects; cause, triggering stage and outcome are not established here."
        return "unknown_error_record_retained", "UNEXPLAINED", "Original unclassified diagnostic retained."
    if name == "debug.log":
        return "building_category_lookup_failure" if "Failed to get any building category" in text else "unknown_debug_record_retained", "UNEXPLAINED", "Building object identity and runtime impact remain unknown."
    if name == "game.log":
        for token, category in (("Game Version:", "version_information"), (" defines loaded", "defines_information"),
                                (" interface defines loaded", "defines_information"), ("Sending sync response", "sync_response"),
                                ("Generating World! Specified Seed:", "world_generation_seed"), ("added info about event selection", "event_selection")):
            if token in text:
                return category, "OBSERVATION_ONLY", "Recorded game activity; no success or gameplay acceptance inferred."
        return "unknown_game_record_retained", "UNEXPLAINED", "Original unclassified record retained."
    if name == "system.log":
        for token, category in (("[gfx_dx9.cpp:", "graphics_adapter_device_and_capabilities"),
                                ("[graphicssettings.cpp:752]", "display_mode_enumeration"),
                                ("[graphicssettings.cpp:", "graphics_settings_and_capabilities"),
                                ("[pdx_audio_sdl.cpp:", "audio_device_driver_and_format"),
                                ("[graphics.cpp:", "graphics_device_creation")):
            if token in text:
                return category, "OBSERVATION_ONLY", "System initialization observation; no guarantee about later runtime or error impact."
        return "unknown_system_record_retained", "UNEXPLAINED", "Original unclassified record retained."
    raise AssertionError(name)


def main():
    assert not (OUT / "review.json").exists(), "Sealed review already exists"
    logs = {}
    unresolved = []
    for name in ("error.log", "game.log", "system.log", "debug.log"):
        path = OUT / "logs" / name
        lines, records = parse(path)
        assert [line for row in records for line in row["lines"]] == lines
        for row in records:
            text = "\n".join(row["lines"])
            category, resolution, reason = classify(name, text)
            row.update(category=category, resolution=resolution, reason=reason)
            if resolution not in ("OBSERVATION_ONLY",):
                unresolved.append({"log": name, "line_start": row["line_start"], "line_end": row["line_end"],
                                   "category": category, "resolution": resolution, "lines": row["lines"]})
        logs[name] = {**fp(path), "physical_lines": len(lines), "record_count": len(records),
                      "categories": dict(Counter(row["category"] for row in records)), "records": records}
    nomads = []
    for name, value in logs.items():
        nomads.extend({"log": name, "line": n, "text": line} for n, line in enumerate(
            (OUT / "logs" / name).read_bytes().decode("utf-8-sig").splitlines(), 1) if "nomads" in line.lower())
    report = {"schema": "eep.rc6.final-logs-review.v1", "status": "REVIEWED_WITH_UNRESOLVED_RUNTIME_DIAGNOSTICS",
              "reviewed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T150008Z",
              "index_sha256": fp(OUT / "index.json")["sha256"], "review_script_sha256": fp(Path(__file__))["sha256"],
              "scope": "Every physical line of complete final error/game/system/debug logs; all 19 original logs remain intact.",
              "logs": logs, "unresolved_diagnostic_records": unresolved, "unresolved_diagnostic_record_count": len(unresolved),
              "nomads_occurrences_in_four_reviewed_logs": nomads,
              "historical_nomads_status": "UNEXPLAINED; zero occurrences in these RC6 logs does not resolve historical diagnostics.",
              "historical_nomads_reference": fp(OUT.parent / "1019-rc4-phase-a-final-logs/review.json"),
              "eep_runtime_errors": [row for row in unresolved if row["category"] == "eep_while_limit_100_abort"],
              "source_attribution_limits": ["No timestamp-to-save or input-stage attribution is inferred from local clock stamps.",
                                            "No baseline comparison exempts, deletes or whitelists a diagnostic.",
                                            "The while diagnostic establishes an abort at the named EEP path, not a proven root cause or engine-wide loop rule.",
                                            "No language, UI, semantic or Mod acceptance is implied by byte preservation."],
              "error_records_suppressed": 0, "Mod_acceptance_pass": False}
    (OUT / "review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "logs": {name: {k: value[k] for k in ("physical_lines", "record_count", "categories")} for name, value in logs.items()}, "unresolved": len(unresolved), "nomads_occurrences": len(nomads)}, indent=2))


if __name__ == "__main__":
    main()
