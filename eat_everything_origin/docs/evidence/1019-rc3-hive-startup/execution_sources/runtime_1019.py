"""Isolated 0.4.0 runtime; preserve earlier baseline and intermediate evidence."""
from pathlib import Path
import json
import re
import sys

import runtime_single_homeworld as base

base.ARTIFACTS = (Path.home() / "AppData/Local/xenoamess_stellaries_dev"
                  / "artifacts/1019-implementation")
base.h.RUNTIME_ROOT = base.ARTIFACTS / "runs"
base.h.CURRENT_RUN = base.ARTIFACTS / "current-run.json"
base.h.WORKSHOP_ID = "eep-1019"
base.h.PROFILE_ID = "eep-0.4.0-single-production-mod"
original_prepare = base.prepare


def prepare_1019(role, seed=None):
    gate = json.loads((base.ARTIFACTS / (role + "-gate.json")).read_text(encoding="utf-8"))
    report = json.loads(Path(gate["report"]).read_text(encoding="utf-8"))
    if (report.get("weapon_csv_applicability") != "checked"
            or report.get("weapon_csv_files", 0) < 1 or report.get("weapon_csv_keys", 0) < 1):
        raise RuntimeError("0.4.0 requires the repaired weapon CSV acceptance gate")
    component_count = report.get("planet_killer_components", 0)
    callback_count = report.get("planet_killer_callbacks_required", 0)
    if (report.get("planet_killer_callback_contract") != "native_completed_queued_unqueued_v1"
            or report.get("planet_killer_callback_applicability") != "checked"
            or component_count < 1 or callback_count != component_count * 3
            or report.get("planet_killer_callbacks_resolved") != callback_count):
        raise RuntimeError("0.4.0 requires completed/queued/unqueued native callback checks")
    result = original_prepare(role, seed)
    path = Path(result["artifact_dir"]) / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["scope"] = ("0.4.0 single-homeworld economy, mothership configuration/evolution, "
                         "native planet-killer and save compatibility; Chinese runtime only; "
                         "stopped Terravore campaign untouched")
    base.h.write_json(path, manifest)
    return result


base.prepare = prepare_1019

original_console_visible = base.console_visible


def console_visible_1019(captured):
    # Native console history can scroll the initial help/fast-forward lines away.
    markers = ("Executing effect script.", "Effect description:", "You are now playing ")
    return original_console_visible(captured) or any(
        any(marker in row["text"] for marker in markers)
        for row in captured["rows"]
    )


base.console_visible = console_visible_1019


def command_open(command, stage):
    """Keep the observed native console open for consecutive physical inputs."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", stage) or "\n" in command or "\r" in command:
        raise ValueError("unsafe stage or multiline console command")
    ready = base.h.capture(stage + "-console-state")
    if not base.console_visible(ready):
        base.h.press_scan_code(0x29, stage + "-open", 1)
        ready = base.h.capture(stage + "-console-ready")
    if not base.console_visible(ready) or ready["resolution"] != [1024, 768]:
        raise RuntimeError("tested native console geometry not visible")
    base.h.click_point(120, 322, stage + "-focus-console-input")
    base.h.type_text(command, True, stage + "-command")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "console-open":
        command_open(sys.argv[2], sys.argv[3])
    else:
        base.main()
