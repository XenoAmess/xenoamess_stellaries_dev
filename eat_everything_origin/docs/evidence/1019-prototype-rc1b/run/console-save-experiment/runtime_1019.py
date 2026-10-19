"""Isolated 0.4.0 runtime; preserve earlier baseline and intermediate evidence."""
from pathlib import Path
import json
import re
import sys
import time

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
    result = original_prepare(role, seed)
    path = Path(result["artifact_dir"]) / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["scope"] = ("0.4.0 single-homeworld economy, mothership configuration/evolution, "
                         "native planet-killer and save compatibility; Chinese runtime only; "
                         "stopped Terravore campaign untouched")
    base.h.write_json(path, manifest)
    return result


base.prepare = prepare_1019


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


def save_console(stage, expected_date, calibration=False):
    """Archive bytes written by the game; requires an independent UI calibration."""
    import audit_save

    artifacts, user, manifest = base.h.load_run()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", stage):
        raise ValueError("unsafe native save name")
    destination = artifacts / (stage + ".sav")
    if destination.exists():
        raise RuntimeError("refusing to overwrite archived native evidence")
    gate = artifacts / "console-save-calibration.json"
    if calibration:
        if stage != "console-save-probe" or gate.exists():
            raise RuntimeError("calibration can only create the first unique probe")
    else:
        data = json.loads(gate.read_text(encoding="utf-8"))
        if (data["status"] != "PASS_SCOPED" or data["manifest_sha256"] != base.h.sha256(artifacts / "manifest.json")
                or data["helper_sha256"] != base.h.sha256(Path(__file__))):
            raise RuntimeError("native console saving has no current verified UI calibration")
    save_root = (user / "save games").resolve()
    before = {str(p): p.stat().st_mtime_ns for p in save_root.rglob("*.sav")}
    command_open("save " + stage, stage)
    deadline = time.monotonic() + 20
    source = None
    while time.monotonic() < deadline:
        candidates = [p for p in save_root.rglob(stage + ".sav")
                      if p.stat().st_mtime_ns > before.get(str(p), 0)]
        if len(candidates) > 1:
            raise RuntimeError("native save name is ambiguous")
        if candidates:
            candidate = candidates[0]
            try:
                raw = candidate.read_bytes()
                if base.autosave_date(raw) == expected_date:
                    source = candidate
                    break
            except (OSError, ValueError, base.zipfile.BadZipFile, KeyError):
                pass
        time.sleep(.2)
    if source is None:
        base.h.capture(stage + "-console-save-failed")
        raise RuntimeError("native save command did not produce a valid fresh dated ZIP")
    destination.write_bytes(raw)
    result = audit_save.audit(destination, (0,))
    if result["date"] != expected_date or base.h.sha256(source) != result["save_sha256"]:
        raise RuntimeError("native save changed or has a different date")
    history = save_root / "eep-test-history" / source.name
    source.resolve().relative_to(save_root)
    history.resolve().relative_to(save_root)
    history.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != history.resolve():
        if history.exists():
            raise RuntimeError("refusing to overwrite native history")
        source.replace(history)
    base.h.write_json(artifacts / (stage + ".audit.json"), result)
    base.h.write_json(artifacts / (stage + ".native-save.json"), {
        "method": "native console save command, physical input",
        "written_at": str(source), "history": str(history), "archived": str(destination),
        "sha256": result["save_sha256"], "date": result["date"],
        "calibration": calibration, "production_tree_sha256": manifest["repository_mod_tree_sha256"],
    })
    return {"date": result["date"], "sha256": result["save_sha256"], "method": "native console"}


def calibrate_console_save(ui_stage):
    import check_single_homeworld as checks

    artifacts, _, _ = base.h.load_run()
    receipt = json.loads((artifacts / (ui_stage + ".native-save.json")).read_text(encoding="utf-8"))
    if "method" in receipt:
        raise RuntimeError("reference must be the existing Chinese native UI save path")
    result = save_console("console-save-probe", receipt["date"], calibration=True)
    comparison = checks.same_day(artifacts, ui_stage, "console-save-probe")
    comparison.update({"reference_ui_stage": ui_stage, "console_save": result,
                       "manifest_sha256": base.h.sha256(artifacts / "manifest.json"),
                       "helper_sha256": base.h.sha256(Path(__file__))})
    base.h.write_json(artifacts / "console-save-calibration.json", comparison)
    if comparison["status"] != "PASS_SCOPED":
        raise RuntimeError("native console save differs; retain FAIL and use native UI saving")
    return comparison


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "console-open":
        command_open(sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 1 and sys.argv[1] == "save-console":
        print(json.dumps(save_console(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "calibrate-console-save":
        print(json.dumps(calibrate_console_save(sys.argv[2]), ensure_ascii=False))
    else:
        base.main()
