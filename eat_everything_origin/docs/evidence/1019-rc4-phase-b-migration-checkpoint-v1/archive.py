"""Archive a fixed whitelist of completed phase-B stages, never the active logs."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import shutil

OUT = Path(__file__).resolve().parent
EVIDENCE = OUT.parent
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T133314Z")
USERDIR = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T133314Z")
STAGES = ("m031load", "m031sync", "m031reload", "mpaidload", "mpaidsync", "mpaidreload", "rdesignsync", "rdesignreload", "rnamesync", "rnameload", "rfleetsync")
PREFIXES = ("m031", "mpaid", "rdesign", "rname", "rfleet", "phaseb-")
CUTOFF = datetime.fromisoformat("2026-10-19T14:07:39.920141+00:00")
ANALYSIS = tuple("rc4-" + x + "-observation-v1.json" for x in STAGES) + (
    "rc4-m031-native-health-raw-source-v1.json", "rc4-m031-old-before-to-load-report-v1.json", "rc4-m031-reload-persistence-raw-source-v1.json",
    "rc4-public031-fraction-migration-sync-case-v1.json", "rc4-public031-fraction-migration-sync-check-v1.json",
    "rc4-public031-fraction-migration-complete-case-v1.json", "rc4-public031-fraction-migration-complete-check-v1.json", "rc4-public031-fraction-migration-series-report-v1.json",
    "rc4-paid-fraction-migration-complete-case-v1.json", "rc4-paid-fraction-migration-complete-check-v1.json", "rc4-paid-fraction-migration-series-report-v1.json",
    "rc4-mpaid-reload-persistence-raw-source-v1.json", "rc4-design-registration-probe-report-v1.json", "rc4-design-name-binding-probe-report-v1.json",
    "rc4-design-name-binding-probe-report-v2.json", "rc4-fleet-scope-design-probe-report-v1.json", "rc4-mobile-starbase-design-pointer-source-v1.json")
TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def select():
    files = {}
    for path in RUN.iterdir():
        if not path.is_file():
            continue
        if path.name.startswith(PREFIXES):
            assert not path.name.startswith("rsizeonly") and path.suffix in (".json", ".jpg", ".png", ".sav")
            if path.suffix == ".sav":
                assert path.stem in STAGES
            files["run/" + path.name] = path
        elif path.name.startswith("press-") and path.suffix == ".json":
            data = json.loads(path.read_bytes())
            if datetime.fromisoformat(data["at_utc"]) <= CUTOFF:
                files["run/" + path.name] = path
    for name in ("manifest.json", "process.json", "candidate-phase-b-imports.json"):
        files[name] = RUN / name
    for name in ANALYSIS:
        files["analysis/" + name] = EVIDENCE / "1019-analysis" / name
    canonical = EVIDENCE / "1019-rc4-pk2-duration/source_snapshot"
    for name in ("source-copy.json", "gate.json", "open-kaishek.json"):
        files["source_snapshot/" + name] = canonical / name
    files["runtime-input/user_empire_designs_v3.4.txt"] = USERDIR / "user_empire_designs_v3.4.txt"
    return dict(sorted(files.items()))


def main():
    assert not (OUT / "index.json").exists(), "Do not replace an existing checkpoint"
    manifest = json.loads((RUN / "manifest.json").read_bytes())
    process = json.loads((RUN / "process.json").read_bytes())
    assert manifest["run_id"] == "20261019T133314Z" and process["pid"] == 36912
    assert manifest["copied_mod_tree_sha256"] == manifest["repository_mod_tree_sha256"] == TREE
    files = select()
    assert {p.stem for p in files.values() if p.suffix == ".sav"} == set(STAGES)
    assert len(ANALYSIS) == 28
    before = [{"path": name, "source": str(path.resolve()), **fingerprint(path)} for name, path in files.items()]
    selection = {"schema": "eep.rc4.phase-b.raw-checkpoint-selection.v1", "run_id": manifest["run_id"],
                 "created_at_utc": datetime.now(timezone.utc).isoformat(), "status": "FIXED_WHITELIST_NOT_FINAL_RUN",
                 "stages": STAGES, "ui_prefixes": PREFIXES, "unprefixed_press_cutoff_utc": CUTOFF.isoformat(),
                 "analysis_names": ANALYSIS, "files": before,
                 "explicit_exclusions": ["active logs directory and all live-log files", "stop proof", "rsizeonly", "later stages", "duplicate old-source archive", "duplicate canonical Mod tree"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for entry in before:
        target = OUT / entry["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(entry["source"]), target)
    assert files == select(), "Selected stable file set changed during copy"
    for entry in before:
        expected = {"bytes": entry["bytes"], "sha256": entry["sha256"]}
        assert fingerprint(Path(entry["source"])) == fingerprint(OUT / entry["path"]) == expected
    old = EVIDENCE / "1019-legacy-damage-run-final"
    canonical = EVIDENCE / "1019-rc4-pk2-duration"
    refs = [old / "index.json", old / "verify.json", old / "run/p031before.sav", old / "run/ppaidbefore.sav",
            canonical / "archive-index-v3.json", canonical / "archive-verification-v3.json",
            canonical / "phase3/pk2dupereload.sav", canonical / "phase2/pk2cancel.sav",
            EVIDENCE / "1019-analysis/rc4-migration-unset-variable-log-report-v1.json"]
    references = [{"path": str(p.resolve()), **fingerprint(p)} for p in refs]
    source_copy = json.loads((OUT / "source_snapshot/source-copy.json").read_bytes())
    mod_refs = []
    for entry in source_copy["files"]:
        path = canonical / "copied_mod" / entry["path"]
        assert fingerprint(path) == {"bytes": entry["bytes"], "sha256": entry["sha256"]}
        mod_refs.append({"path": str(path.resolve()), "mod_relative_path": entry["path"], **fingerprint(path)})
    assert len(mod_refs) == 59
    index = {"schema": "eep.rc4.phase-b.raw-checkpoint-index.v1", "status": "BYTE_IDENTICAL_COMPLETED_STAGES_WITH_FAILURES",
             "run_id": manifest["run_id"], "process_still_active": True, "pid": 36912,
             "copied_at_utc": datetime.now(timezone.utc).isoformat(), "mod_tree_sha256": TREE,
             "selection_sha256": sha256((OUT / "selection.json").read_bytes()).hexdigest(),
             "payload_file_count": len(before), "payload_bytes": sum(x["bytes"] for x in before), "native_save_count": len(STAGES),
             "analysis_json_count": len(ANALYSIS), "files": before, "canonical_references_not_copied": references,
             "canonical_Mod_59_files_referenced_not_duplicated": mod_refs,
             "active_logs_copied": False, "complete_run_freeze": False, "rsizeonly_included": False,
             "migration_acceptance": "FAILURES_PRESERVED_NOT_COMPLETE", "release_status": "PENDING"}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: index[k] for k in ("status", "payload_file_count", "payload_bytes", "native_save_count", "analysis_json_count", "active_logs_copied", "complete_run_freeze")}, indent=2))


if __name__ == "__main__":
    main()
