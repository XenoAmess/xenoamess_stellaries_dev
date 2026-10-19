"""Freeze stopped run133314Z logs and completed incremental probe evidence."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T133314Z")
USERDIR = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T133314Z")
TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"
CUTOFF = datetime.fromisoformat("2026-10-19T14:07:39.920141+00:00")
REPORTS = ("rc4-rsizeonly-observation-v1.json", "rc4-mobile-starbase-size-probe-report-v1.json",
           "native-relic-health-calibration-source-v1.json", "rc4-migration-unset-variable-log-report-v1.json")
PLANS = ("native-relic-health-calibration-1019.md", "armor-damage-migration-probe-1019.md",
         "mothership-migration-damage-queue-review-1019.md")


def fp(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def select(stop):
    files = {}
    for path in sorted((USERDIR / "logs").rglob("*")):
        if path.is_file():
            files["logs/" + path.relative_to(USERDIR / "logs").as_posix()] = path
    for name in ("manifest.json", "process.json", "stop.json"):
        files[name] = RUN / name
    for path in sorted(RUN.iterdir()):
        if path.is_file() and path.name.startswith(("rsizeonly", "nrel")):
            assert path.suffix in (".sav", ".json", ".jpg", ".png")
            files["run/" + path.name] = path
        elif path.is_file() and path.name.startswith("press-") and path.suffix == ".json":
            when = datetime.fromisoformat(json.loads(path.read_bytes())["at_utc"])
            if CUTOFF < when <= datetime.fromisoformat(stop["stopped_at_utc"]):
                files["run/" + path.name] = path
    for name in REPORTS:
        files["analysis/" + name] = OUT.parent / "1019-analysis" / name
    for name in PLANS:
        files["plans/" + name] = DOCS / name
    return dict(sorted(files.items()))


def main():
    assert not (OUT / "index.json").exists(), "Existing final run archive is immutable"
    independent = json.loads((OUT / "process-independent.json").read_text(encoding="utf-8-sig"))
    assert independent["status"] == "ABSENT" and independent["expected_pid"] == 36912
    stop = json.loads((RUN / "stop.json").read_bytes())
    process = json.loads((RUN / "process.json").read_bytes())
    manifest = json.loads((RUN / "manifest.json").read_bytes())
    assert stop["pid"] == process["pid"] == 36912 and not stop["forced"] and not stop["running_after"]
    assert manifest["run_id"] == "20261019T133314Z"
    assert manifest["copied_mod_tree_sha256"] == manifest["repository_mod_tree_sha256"] == TREE
    assert datetime.fromisoformat(independent["checked_at_utc"]) > datetime.fromisoformat(stop["stopped_at_utc"])
    files = select(stop)
    rows = [{"path": rel, "source": str(path.resolve()), **fp(path)} for rel, path in files.items()]
    saves = [row for row in rows if row["path"].endswith(".sav")]
    assert len(saves) == 1 and saves[0]["path"] == "run/rsizeonly.sav"
    selection = {"schema": "eep.rc4.phase-b.final-run-selection.v1", "run_id": manifest["run_id"],
                 "created_at_utc": datetime.now(timezone.utc).isoformat(), "status": "STOPPED_FINAL_LOGS_AND_INCREMENTAL_PROBES",
                 "fixed_source_artifact_directory": str(RUN), "fixed_userdir": str(USERDIR),
                 "all_logs_recursive": True, "incremental_prefixes": ["rsizeonly", "nrel"],
                 "unprefixed_press_lower_bound_exclusive_utc": CUTOFF.isoformat(),
                 "unprefixed_press_upper_bound_inclusive_utc": stop["stopped_at_utc"],
                 "report_names": REPORTS, "plan_names": PLANS, "files": rows,
                 "exclusions": ["duplicate 11 phase-B SAV and previous 462 payload", "duplicate 59 Mod files", "working RC5", "other/new run logs", "invented nrelbefore/nrelset/nrelload files"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        target = OUT / row["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    assert files == select(stop), "Stopped source file set changed"
    canonical = OUT.parent / "1019-rc4-pk2-duration"
    phase_b = OUT.parent / "1019-rc4-phase-b-migration-checkpoint-v1"
    supplement = OUT.parent / "1019-rc4-midrun-capture-tool-supplement-v1"
    relic = OUT.parent / "1019-rc4-relic-jump-native-control-v1"
    refs = [phase_b / name for name in ("index.json", "verify.json", "selection.json")]
    refs += [supplement / name for name in ("index.json", "verify.json", "selection.json")]
    refs += [canonical / name for name in ("archive-index-v3.json", "archive-verification-v3.json", "source_snapshot/source-copy.json", "source_snapshot/gate.json", "source_snapshot/open-kaishek.json", "copied_mod/common/scripted_effects/eep_mothership_effects.txt")]
    refs += [relic / "raw" / name for name in ("r4relic6.sav", "r4relic6.native-save.json", "r4relic6.audit.json")]
    import_receipt = json.loads((OUT / "run/nrel-source-import-receipt.json").read_bytes())
    refs += [Path(import_receipt["source"]["save"]), Path(import_receipt["alias"])]
    refs += [OUT.parent / "1019-rc4-phase-a-final-logs/review.json", OUT.parent / "1019-native-cracker-control/analysis.json"]
    refs = sorted(set(refs))
    log_rows = [row for row in rows if row["path"].startswith("logs/")]
    index = {"schema": "eep.rc4.phase-b.final-run-index.v1", "status": "BYTE_IDENTICAL_STOPPED_RUN_WITH_FAILURES",
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": manifest["run_id"], "pid": process["pid"],
             "stop": stop, "process_independent_sha256": fp(OUT / "process-independent.json")["sha256"],
             "source_process_confirmed_stopped_before_copy": True, "source_mod_tree_sha256": TREE,
             "selection_sha256": fp(OUT / "selection.json")["sha256"], "payload_file_count": len(rows),
             "payload_bytes": sum(row["bytes"] for row in rows), "log_file_count": len(log_rows),
             "log_bytes": sum(row["bytes"] for row in log_rows),
             "script_documentation_files": [row["path"] for row in log_rows if row["path"].startswith("logs/script_documentation/")],
             "native_sav_count": 1, "native_sav_names": ["rsizeonly"],
             "canonical_references_not_copied": [{"path": str(p.resolve()), **fp(p)} for p in refs],
             "files": rows, "limitations": ["Evidence-byte completeness only, not Mod acceptance", "Migration and rsizeonly failures remain failures", "nrel HUD date guard failed; no injury/save/export; play0 guard attempts did not type play0", "Earlier phase-B and tool-source supplement remain independent unchanged canonical archives", "No Mod tree or RC5 files copied", "Historical nomads.94 remains unexplained regardless of this run's log contents"]}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("logs/** -text\nrun/** -text\nanalysis/** -text\nplans/** -text\nmanifest.json -text\nprocess.json -text\nstop.json -text\n", encoding="ascii")
    print(json.dumps({k: index[k] for k in ("status", "payload_file_count", "payload_bytes", "log_file_count", "log_bytes", "native_sav_count")}))


if __name__ == "__main__":
    main()
