"""Archive stopped RC5 run bytes; no UI, module execution, Git or RC6 inputs."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
REPO = DOCS.parent.parent
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T143452Z")
USERDIR = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T143452Z")
IMPL = RUN.parent.parent
STATIC = OUT.parent / "1019-rc5-static"
MIDRUN = OUT.parent / "1019-rc4-midrun-capture-tool-supplement-v1"
TREE = "1cc8b77c28f3d59b0d840982c7f039a209cb66f3e26d9c3280ad2dfa0f9dbd52"
STAGES = ("r5pautoload", "r5preload1", "r5coreguard1", "r5coreguard2", "nchealthbefore", "nchealthset", "nchealthload")
REPORTS = tuple("rc5-" + stage + "-observation-v1.json" for stage in STAGES) + (
    "rc5-public031-autoload-reload-report-v1.json", "rc5-six-core-layout-guard-report-v1.json",
    "native-current-ship-health-setter-calibration-report-v1.json",
    "native-current-ship-health-calibration-source-v1.json", "native-current-ship-health-setter-calibration-source-v1.json",
    "native-health-export-restoration-source-v1.json", "rc5-source-dependency-audit-v1.json", "economy-explicit-binding-rc5-v1.json")
PLANS = ("native-current-ship-health-setter-calibration-1019.md", "native-current-ship-health-calibration-1019.md",
         "rc5-autoload-design-repair-observation-1019.md", "native-six-core-layout-guard-probe-1019.md",
         "rc5-growth-source-contract-1019.md", "rc5-scope-revalidation-1019.md", "legacy-health-export-restoration-1019.md")
TOOLS = ("eat_everything_origin/tools/runtime.py", "eat_everything_origin/tools/runtime_single_homeworld.py",
         "eat_everything_origin/tools/runtime_1019.py", "eat_everything_origin/tools/runtime_1015.py",
         "tools/stellaris_acceptance.py", "eat_everything_origin/tools/audit_save.py",
         "eat_everything_origin/testing/inspect_1015.py", "eat_everything_origin/testing/inspect_1019.py",
         "eat_everything_origin/tools/check_1019.py")


def fp(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def choose():
    files = {}
    for p in RUN.rglob("*"):
        if p.is_file():
            files["run/" + p.relative_to(RUN).as_posix()] = p
    for p in (USERDIR / "logs").rglob("*"):
        if p.is_file():
            files["logs/" + p.relative_to(USERDIR / "logs").as_posix()] = p
    for name in REPORTS:
        files["analysis/" + name] = OUT.parent / "1019-analysis" / name
    for name in PLANS:
        files["plans/" + name] = DOCS / name
    for name in TOOLS:
        files["tools-hash-binding/" + name] = REPO / name
    for name in ("candidate-rc5-gate.json", "candidate-rc5-open-kaishek.json"):
        files["source_snapshot/" + name] = IMPL / name
    files["source_snapshot/canonical-source-index.json"] = STATIC / "source-index.json"
    return dict(sorted(files.items()))


def main():
    assert not (OUT / "index.json").exists(), "Existing run archive is immutable"
    independent = json.loads((OUT / "process-independent.json").read_text(encoding="utf-8-sig"))
    stop = json.loads((RUN / "stop.json").read_bytes())
    process = json.loads((RUN / "process.json").read_bytes())
    manifest = json.loads((RUN / "manifest.json").read_bytes())
    assert independent["status"] == "ABSENT" and independent["expected_pid"] == stop["pid"] == process["pid"] == 33260
    assert stop["forced"] is False and stop["running_after"] is False
    assert datetime.fromisoformat(independent["checked_at_utc"]) > datetime.fromisoformat(stop["stopped_at_utc"])
    assert manifest["run_id"] == "20261019T143452Z" and manifest["language"] == "l_simp_chinese"
    assert manifest["copied_mod_tree_sha256"] == manifest["repository_mod_tree_sha256"] == TREE
    assert manifest["static_gate"]["version"] == "0.4.0-rc.5"
    files = choose()
    rows = [{"path": name, "source": str(path.resolve()), **fp(path)} for name, path in files.items()]
    assert {Path(row["path"]).stem for row in rows if row["path"].endswith(".sav")} == set(STAGES)
    selection = {"schema": "eep.rc5.final-run-selection.v1", "run_id": manifest["run_id"],
                 "created_at_utc": datetime.now(timezone.utc).isoformat(), "fixed_artifact_path": str(RUN), "fixed_userdir": str(USERDIR),
                 "all_stopped_artifact_files_recursive": True, "all_stopped_log_files_recursive": True,
                 "stages": STAGES, "analysis_whitelist": REPORTS, "plan_whitelist": PLANS, "stable_tool_hash_binding_whitelist": TOOLS,
                 "files": rows, "exclusions": ["current-run pointer", "current ROOT Mod/RC6", "post-run v2 checker", "invented prepare execution-source snapshot", "unproven current indirect publish dependencies"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        target = OUT / row["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    assert files == choose(), "Stopped selected file set changed"
    source_inventory = json.loads((STATIC / "source-index.json").read_bytes())
    refs = []
    for item in source_inventory["files"]:
        source = STATIC / item["path"]
        assert fp(source) == {"bytes": item["bytes"], "sha256": item["sha256"]}
        refs.append({"path": str(source.resolve()), **fp(source)})
    digest = sha256()
    actual_mod_entries = []
    for p in sorted(p for p in (USERDIR / "mod/eep-1019").rglob("*") if p.is_file()):
        relative = p.relative_to(USERDIR / "mod/eep-1019").as_posix()
        body = p.read_bytes()
        digest.update(relative.encode("utf-8")); digest.update(b"\0"); digest.update(body)
        native = {"path": relative, **fp(p)}
        assert fp(STATIC / "candidate-rc5/mod" / relative) == {"bytes": native["bytes"], "sha256": native["sha256"]}
        actual_mod_entries.append(native)
    assert digest.hexdigest() == TREE and actual_mod_entries == manifest["repository_mod_files"]
    tools = []
    for name in TOOLS:
        old = MIDRUN / "current-source" / name
        copied = OUT / "tools-hash-binding" / name
        assert fp(old) == fp(copied)
        tools.append({"archived_path": "tools-hash-binding/" + name, "source": str((REPO / name).resolve()),
                      "matching_earlier_canonical": str(old.resolve()), **fp(copied)})
        refs.append({"path": str(old.resolve()), **fp(old)})
    extra_refs = [STATIC / "source-index.json", MIDRUN / "index.json", MIDRUN / "verify.json",
                  OUT.parent / "1019-legacy-damage-run-final/index.json", OUT.parent / "1019-legacy-damage-run-final/verify.json",
                  OUT.parent / "1019-legacy-damage-run-final/run/p031before.sav",
                  OUT.parent / "1019-legacy-damage-run-final/run/ppaidbefore.sav",
                  OUT.parent / "1019-rc4-phase-b-migration-checkpoint-v1/index.json",
                  OUT.parent / "1019-rc4-phase-b-final-run/index.json", OUT.parent / "1019-rc4-phase-b-final-run/verify.json",
                  OUT.parent / "1019-rc4-phase-a-final-logs/review.json", OUT.parent / "1019-native-cracker-control/analysis.json"]
    for p in extra_refs:
        refs.append({"path": str(p.resolve()), **fp(p)})
    bindings = {"schema": "eep.rc5.postrun-source-hash-binding.v1", "status": "POSTRUN_HASH_BINDING_NOT_PREPARE_EXECUTION_SNAPSHOT",
                "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": manifest["run_id"], "actual_mod_tree_sha256": TREE,
                "actual_mod_file_count": len(actual_mod_entries), "actual_mod_entries": actual_mod_entries,
                "canonical_mod_directory": str((STATIC / "candidate-rc5/mod").resolve()), "tools": tools,
                "prepare_execution_source_snapshot_existed": False, "memory_loaded_source_proof": False,
                "root_handoff": {"runtime_84b_sealed_before_prepare": True, "named_nine_tool_bytes_stable_for_run": True,
                    "indirect_publish_1019_changed_during_run": True, "publishing_and_growth_model_gate_called_by_native_UI_actions": False,
                    "historical_commit_reference_only_not_inspected": "d0ce2bc31", "new_health_v2_tool_developed_after_utc": "2026-10-19T15:00:00Z"},
                "limits": ["No fabricated prepare-time execution directory or in-memory source proof", "Do not equate current indirect publish module with every historical worker import", "Nine archived source bytes match earlier canonical and report hashes; root supplies timing/historical stability handoff", "New health v2 tool is excluded from RC5 execution source"]}
    (OUT / "source-binding.json").write_text(json.dumps(bindings, indent=2) + "\n", encoding="utf-8")
    logs = [row for row in rows if row["path"].startswith("logs/")]
    index = {"schema": "eep.rc5.final-run-index.v1", "status": "BYTE_IDENTICAL_STOPPED_RC5_WITH_MIGRATION_FAILURES",
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": manifest["run_id"], "pid": process["pid"], "stop": stop,
             "process_independent_sha256": fp(OUT / "process-independent.json")["sha256"], "source_binding_sha256": fp(OUT / "source-binding.json")["sha256"],
             "selection_sha256": fp(OUT / "selection.json")["sha256"], "source_tree_sha256": TREE, "version": "0.4.0-rc.5",
             "payload_file_count": len(rows), "payload_bytes": sum(row["bytes"] for row in rows), "log_file_count": len(logs),
             "log_bytes": sum(row["bytes"] for row in logs), "native_sav_count": 7, "native_sav_stages": STAGES,
             "canonical_references_not_copied": refs, "files": rows, "Mod_acceptance_pass": False,
             "limits": ["Autoload/reload report remains FAIL", "Identical-SAV coreguard PASS_SCOPED 26/26 has no native reload claim", "Native health setter OBSERVATION_WITH_FAILURES retains original 1e-6 failures", "Root flags do not prove design-local marker semantics", "No working RC6/new checker v2/other run evidence used", "No Git, UI, Steam, production or tool mutations"]}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("run/** -text\nlogs/** -text\nanalysis/** -text\nplans/** -text\ntools-hash-binding/** -text\nsource_snapshot/** -text\n", encoding="ascii")
    print(json.dumps({k: index[k] for k in ("status", "payload_file_count", "payload_bytes", "log_file_count", "log_bytes", "native_sav_count")}))


if __name__ == "__main__":
    main()
