"""Freeze an explicit tool-source supplement, without importing game/UI modules."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
MOD = REPO / "eat_everything_origin"
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T133314Z")
BASE = OUT.parent / "1019-rc4-pk2-duration"
OLD = "91b831241440a04ffa55d7226c7e2eb158907ebdc62054a906ff51e9f5e77adf"
NEW = "84b7fdda9489392f5abab5fc71c9bd61bcc5933185a02f7c6c479d703b155ffc"
TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"
SEEDS = (
    "tools/runtime.py", "tools/runtime_single_homeworld.py", "tools/runtime_1019.py", "tools/runtime_1015.py",
    "tools/runtime_growth_1019.py", "tools/audit_save.py", "tools/check_1019.py", "tools/check_growth_1019.py",
    "tools/check_single_homeworld.py", "testing/inspect_1015.py", "testing/inspect_1019.py")
RELEASE = (
    "testing/test_runtime_screenshot_scan.py", "docs/ocr-session-reuse-1019.md",
    "docs/evidence/1019-analysis/ocr-screenshot-scan-benchmark-v1.py",
    "docs/evidence/1019-analysis/ocr-screenshot-scan-benchmark-v1.json",
    "docs/evidence/1019-analysis/ocr-session-reuse-benchmark-v1.py",
    "docs/evidence/1019-analysis/ocr-session-reuse-benchmark-v1.json",
    "docs/evidence/1019-analysis/ocr-capture-readonly-cost-v1.json")


def fp(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def closure():
    directories = (MOD / "tools", MOD / "testing", REPO / "tools")
    pending = [MOD / name for name in SEEDS] + [REPO / "tools/stellaris_acceptance.py"]
    found, edges = set(), []
    while pending:
        path = pending.pop().resolve()
        if path in found:
            continue
        found.add(path)
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
        for module in sorted(modules):
            matches = [d / (module + ".py") for d in directories if (d / (module + ".py")).is_file()]
            if matches:
                assert len(matches) == 1, (path, module, matches)
                target = matches[0].resolve()
                edges.append({"from": path.relative_to(REPO).as_posix(), "module": module,
                              "to": target.relative_to(REPO).as_posix()})
                pending.append(target)
    return sorted(found), sorted(edges, key=lambda e: (e["from"], e["module"]))


def main():
    assert not (OUT / "index.json").exists(), "Existing supplement is immutable"
    sources, edges = closure()
    assert len(sources) == 18
    files = {"current-source/" + p.relative_to(REPO).as_posix(): p for p in sources}
    files["old-source/runtime.py"] = BASE / "execution_sources/runtime.py"
    for name in RELEASE:
        files["release-evidence/" + name] = MOD / name
    files["plans/native-relic-health-calibration-1019.md"] = MOD / "docs/native-relic-health-calibration-1019.md"
    for name in ("manifest.json", "process.json"):
        files["original-run/" + name] = RUN / name
    names = ["nrel-source-import-receipt.json"]
    names += ["nrel-source-load-" + label + ".action.json" for label in ("esc-0", "open", "row", "load")]
    for stem in ("nrel-source-load-menu-0", "nrel-source-load-menu-1", "nrel-source-load-load-window",
                 "nrel-source-load-loaded", "nrel-load-hud-recheck",
                 "nrel-play-country-zero-console-state", "nrel-play-country-zero-console-ready",
                 "nrel-play-country-zero-retry-console-state", "nrel-play-country-zero-retry-console-ready"):
        names.extend(stem + suffix for suffix in (".jpg", ".ocr.json", "-f12.action.json"))
    names.extend(("nrel-play-country-zero-open.action.json", "nrel-play-country-zero-retry-open.action.json"))
    assert len(names) == len(set(names)) == 34
    for name in names:
        files["nrel-failed-attempts/" + name] = RUN / name
    files = dict(sorted(files.items()))
    rows = [{"path": name, "source": str(path.resolve()), **fp(path)} for name, path in files.items()]
    selection = {"schema": "eep.rc4.midrun-tool-source-selection.v1", "run_id": "20261019T133314Z",
                 "scope": "midrun UI-capture-tool supplement", "created_at_utc": datetime.now(timezone.utc).isoformat(),
                 "source_closure_seed_mod_relative_paths": SEEDS, "source_closure_shared_seed": "tools/stellaris_acceptance.py",
                 "closure_method": "AST import and import-from; unique local module.py in mod/tools, mod/testing, repository/tools; never execute modules",
                 "closure_limit": "Static available local Python dependencies only; not proof every function/module executed by a worker; dynamic imports/third-party binary dependency closure is outside this supplement",
                 "local_import_edges": edges, "nrel_fixed_filenames": names, "files": rows,
                 "exclusions": ["all active/final logs", "Mod tree files", "SAV copies", "later direct probes", "invented worker source file", "invented successful load/failed-helper receipt"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        target = OUT / row["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    assert fp(OUT / "old-source/runtime.py")["sha256"] == OLD
    assert fp(OUT / "current-source/eat_everything_origin/tools/runtime.py")["sha256"] == NEW
    manifest = json.loads((OUT / "original-run/manifest.json").read_bytes())
    process = json.loads((OUT / "original-run/process.json").read_bytes())
    assert manifest["run_id"] == "20261019T133314Z" and process["pid"] == 36912
    assert manifest["copied_mod_tree_sha256"] == manifest["repository_mod_tree_sha256"] == TREE
    baselines = {
        "eat_everything_origin/tools/runtime.py": "execution_sources/runtime.py",
        "eat_everything_origin/tools/runtime_single_homeworld.py": "execution_sources/runtime_single_homeworld.py",
        "eat_everything_origin/tools/runtime_1019.py": "execution_sources/runtime_1019.py",
        "eat_everything_origin/tools/runtime_1015.py": "execution_sources/runtime_1015.py",
        "tools/stellaris_acceptance.py": "execution_sources/stellaris_acceptance.py",
        "eat_everything_origin/tools/audit_save.py": "analysis_tools/audit_save.py",
        "eat_everything_origin/tools/check_1019.py": "analysis_tools/check_1019.py",
        "eat_everything_origin/testing/inspect_1015.py": "analysis_tools/inspect_1015.py",
        "eat_everything_origin/testing/inspect_1019.py": "analysis_tools/inspect_1019.py"}
    comparisons = []
    for source in sources:
        rel = source.relative_to(REPO).as_posix()
        oldpath = BASE / baselines[rel] if rel in baselines else None
        comparisons.append({"current_path": "current-source/" + rel, "current": fp(source),
                            "old_canonical_source": str(oldpath.resolve()) if oldpath else None,
                            "old": fp(oldpath) if oldpath else None,
                            "status": ("UNCHANGED_FROM_CANONICAL" if fp(source) == fp(oldpath) else "CHANGED_FROM_CANONICAL") if oldpath else "NO_CANONICAL_BASELINE_IN_THIS_SUPPLEMENT"})
    previous = OUT.parent / "1019-rc4-phase-b-migration-checkpoint-v1"
    refs = [BASE / "archive-index-v3.json", BASE / "archive-verification-v3.json", BASE / "source_snapshot/source-copy.json",
            BASE / "source_snapshot/gate.json", BASE / "source_snapshot/open-kaishek.json",
            previous / "index.json", previous / "verify.json", previous / "run/rfleetsync-close-menu.action.json",
            previous / "run/rfleetsync-menu-1.ocr.json", previous / "run/rfleetsync-menu-1.jpg"]
    refs += [BASE / name for name in baselines.values()]
    refs = sorted(set(refs))
    index = {"schema": "eep.rc4.midrun-capture-tool-supplement.v1", "status": "BYTE_IDENTICAL_SOURCE_AND_FAILED_ATTEMPTS_ONLY",
             "scope": selection["scope"], "run_id": manifest["run_id"], "game_pid": process["pid"], "mod_tree_sha256": TREE,
             "final_run_freeze": False, "mod_acceptance_pass": False,
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "old_runtime_sha256": OLD, "new_runtime_sha256": NEW,
             "worker_boundary_root_handoff": {"source": "root collaboration handoff; no process-memory loaded-source capture",
                 "worker_session_id": 86592, "not_claimed_to_be_game_or_windows_process_pid": True,
                 "approximate_start_local": "2026-10-19 22:25 Asia/Shanghai", "approximate_start_utc": "2026-10-19T14:25:00Z",
                 "execution_form": "exec_command PowerShell inline here-string piped into python -; no pre-existing saved worker script",
                 "reported_sequence": ["sys.path insert tools", "import runtime1019", "regex extract three commands from native-relic-health-calibration plan", "b.r.native_load('nrelsrc', 'nrel-source-load')"],
                 "failure": "native_load HUD date verification exception; planned injure/save/export never executed",
                 "later_worker_session_ids": [25428, 36308], "later_worker_result": "Both b.console play0 attempts rejected by console-visible-open guard; play0 was not typed",
                 "new_source_sealed_before_import": "root and release-agent handoff; archived on-disk bytes independently hashed",
                 "memory_loaded_source_proof": False, "actual_worker_source_path": None,
                 "do_not_retrofit_other_midrun_samples": True},
             "selection_sha256": fp(OUT / "selection.json")["sha256"], "payload_file_count": len(rows),
             "payload_bytes": sum(x["bytes"] for x in rows), "source_closure_file_count": len(sources),
             "baseline_comparisons": comparisons, "canonical_references_not_copied": [{"path": str(p.resolve()), **fp(p)} for p in refs],
             "files": rows, "limits": ["No new successful load receipt or injury/save sample", "No active/final logs read", "Original manifest, gate, source-copy, previous checkpoint and receipts unmodified", "Working RC5 Mod was not loaded into this RC4 process", "No claim that on-disk hashes prove historic in-memory Python source", "Tool benchmark/static PASS is not Mod acceptance"]}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("current-source/** -text\nold-source/** -text\nrelease-evidence/** -text\nplans/** -text\noriginal-run/** -text\nnrel-failed-attempts/** -text\n", encoding="ascii")
    print(json.dumps({"payload_files": len(rows), "payload_bytes": index["payload_bytes"], "index_sha256": fp(OUT / "index.json")["sha256"]}))


if __name__ == "__main__":
    main()
