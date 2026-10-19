"""Freeze only completed RC6 migration samples; never read active logs or UI."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
REPO = DOCS.parent.parent
MOD = REPO / "eat_everything_origin"
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")
USERDIR = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T150008Z")
STATIC = OUT.parent / "1019-rc6-static"
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
TOOL = "08b57969060c037c4e03829f0075f8e7314f262527215e991595bd4778456d38"
STAGES = ("r6pautoload", "r6preload1", "r6prepeatbase", "r6prepeat", "r6paidauto", "r6paidreload1", "r6paidrepeat")
EXTRA = ("r6-public-repeat-load", "rc6-load-menu-retry")
PRESS = tuple("press-" + stamp + ".json" for stamp in ("1792422527999", "1792422611212", "1792422707347", "1792422791563", "1792422918828", "1792423002932", "1792423082023"))
LOADS = ("r6pautoload-native-load2.load.json", "r6preload1-native-load2.load.json", "r6paidauto-native-load2.load.json", "r6paidreload1-native-load2.load.json", "r6-public-repeat-load.load.json")
REPORTS = tuple("rc6-" + x + "-migration-v2-observation-v1.json" for x in STAGES)
REPORTS += tuple("rc6-" + kind + "-" + stage + "-migration-v2-observation-v1.json" for kind in ("public031", "paid11") for stage in ("fixture_source", "before"))
REPORTS += tuple("rc6-" + kind + "-migration-v2-template-v1.json" for kind in ("public031", "paid11"))
REPORTS += ("rc6-public031-migration-v2-partial-case-v1.json", "rc6-public031-migration-v2-partial-report-v1.json",
            "rc6-public031-migration-v2-complete-case-v1.json", "rc6-public031-migration-v2-complete-report-v1.json",
            "rc6-paid11-migration-v2-complete-case-v1.json", "rc6-paid11-migration-v2-complete-report-v1.json", "rc6-paid11-migration-v2-cli-report-v1.json")
REPORTS += ("rc6-migration-v2-delivery-v1.json",)
UI_TOOLS = ("eat_everything_origin/tools/runtime.py", "eat_everything_origin/tools/runtime_single_homeworld.py",
            "eat_everything_origin/tools/runtime_1019.py", "eat_everything_origin/tools/runtime_1015.py", "tools/stellaris_acceptance.py",
            "eat_everything_origin/tools/audit_save.py", "eat_everything_origin/testing/inspect_1015.py",
            "eat_everything_origin/testing/inspect_1019.py", "eat_everything_origin/tools/check_1019.py")
PLANS = ("native-migration-roundoff-contract-1019.md", "rc6-migration-v2-evidence-mapping-1019.md")


def fp(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def analysis_closure():
    directories = (MOD / "tools", MOD / "testing", REPO / "tools")
    pending = [MOD / "tools/check_migration_1019.py", MOD / "testing/test_check_migration_1019.py"]
    found, edges = set(), []
    while pending:
        path = pending.pop().resolve()
        if path in found:
            continue
        found.add(path)
        root = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        names = set()
        for item in ast.walk(root):
            if isinstance(item, ast.Import): names.update(x.name.split(".")[0] for x in item.names)
            elif isinstance(item, ast.ImportFrom) and item.module: names.add(item.module.split(".")[0])
        for name in sorted(names):
            hits = [base / (name + ".py") for base in directories if (base / (name + ".py")).is_file()]
            if hits:
                assert len(hits) == 1
                target = hits[0].resolve()
                edges.append({"from": path.relative_to(REPO).as_posix(), "module": name, "to": target.relative_to(REPO).as_posix()})
                pending.append(target)
    return sorted(found), sorted(edges, key=lambda x: (x["from"], x["module"]))


def matched(name, prefix):
    return name.startswith(prefix + "-") or name.startswith(prefix + ".")


def choose():
    files = {}
    for p in RUN.iterdir():
        if p.is_file() and (any(matched(p.name, prefix) for prefix in STAGES + EXTRA) or p.name in PRESS):
            assert p.suffix in (".json", ".jpg", ".sav", ".png") and not p.name.startswith("r6pu")
            files["run/" + p.name] = p
    for name in ("manifest.json", "process.json", "candidate-rc6-imports.json"):
        files["run/" + name] = RUN / name
    for name in REPORTS:
        files["analysis/" + name] = OUT.parent / "1019-analysis" / name
    for name in PLANS:
        files["plans/" + name] = DOCS / name
    offline, edges = analysis_closure()
    tools = set(offline) | {(REPO / name).resolve() for name in UI_TOOLS}
    for path in sorted(tools):
        files["source-tools/" + path.relative_to(REPO).as_posix()] = path
    for name in ("candidate-rc6-gate.json", "candidate-rc6-open-kaishek.json", "source-index.json"):
        files["source_snapshot/" + name] = STATIC / name
    return dict(sorted(files.items())), offline, edges


def collect_report_refs(value, refs):
    if isinstance(value, list):
        for item in value: collect_report_refs(item, refs)
    elif isinstance(value, dict):
        for pathkey, hashkey in (("path", "sha256"), ("save", "save_sha256"), ("manifest", "manifest_sha256"),
                                 ("audit", "audit_sha256"), ("observation_path", "observation_sha256")):
            name, expected = value.get(pathkey), value.get(hashkey)
            if isinstance(name, str) and isinstance(expected, str) and len(expected) == 64:
                p = Path(name)
                if not p.is_absolute(): p = REPO / p
                assert p.suffix != ".log" and "logs" not in p.parts, "No active logs may be read"
                assert p.is_file(), str(p)
                assert fp(p)["sha256"] == expected, str(p)
                refs[str(p.resolve())] = {"path": str(p.resolve()), **fp(p)}
        for item in value.values(): collect_report_refs(item, refs)


def main():
    assert not (OUT / "index.json").exists(), "Existing checkpoint is immutable"
    manifest = json.loads((RUN / "manifest.json").read_bytes())
    process = json.loads((RUN / "process.json").read_bytes())
    assert manifest["run_id"] == "20261019T150008Z" and process["pid"] == 30812
    assert manifest["copied_mod_tree_sha256"] == manifest["repository_mod_tree_sha256"] == TREE
    files, offline, edges = choose()
    assert len(REPORTS) == 21
    rows = [{"path": name, "source": str(path.resolve()), **fp(path)} for name, path in files.items()]
    assert {Path(x["path"]).stem for x in rows if x["path"].endswith(".sav")} == set(STAGES)
    assert all("run/" + name in files for name in LOADS)
    selection = {"schema": "eep.rc6.migration-checkpoint-selection.v1", "status": "COMPLETED_MIGRATION_ONLY_NOT_FINAL_RUN",
                 "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": manifest["run_id"], "fixed_artifact_directory": str(RUN),
                 "fixed_userdir": str(USERDIR), "stages": STAGES, "completed_extra_load_prefixes": EXTRA, "fixed_press_filenames": PRESS,
                 "actual_native_load_receipts": LOADS, "analysis_whitelist": REPORTS, "plan_whitelist": PLANS,
                 "offline_analysis_local_AST_closure": [p.relative_to(REPO).as_posix() for p in offline], "offline_analysis_local_AST_edges": edges,
                 "UI_core_hash_binding_whitelist": UI_TOOLS, "files": rows,
                 "exclusions": ["active or final logs; no log reads", "stop proof", "r6pu/economy/other active UI", "future samples", "current ROOT Mod", "unproven changing indirect UI publish dependencies", "overwriting old v1/RC5 failure evidence"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        target = OUT / row["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    assert files == choose()[0]
    assert fp(OUT / "source-tools/eat_everything_origin/tools/check_migration_1019.py")["sha256"] == TOOL
    refs = {}
    for name in REPORTS:
        collect_report_refs(json.loads((OUT / "analysis" / name).read_bytes()), refs)
    static_index = json.loads((STATIC / "source-index.json").read_bytes())
    for item in static_index["files"]:
        p = STATIC / item["path"]
        assert fp(p) == {"bytes": item["bytes"], "sha256": item["sha256"]}
        refs[str(p.resolve())] = {"path": str(p.resolve()), **fp(p)}
    digest = sha256()
    for entry in manifest["repository_mod_files"]:
        p = USERDIR / "mod/eep-1019" / entry["path"]
        canonical = STATIC / "candidate-rc6/mod" / entry["path"]
        assert fp(p) == fp(canonical) == {"bytes": entry["bytes"], "sha256": entry["sha256"]}
        digest.update(entry["path"].encode("utf-8")); digest.update(b"\0"); digest.update(p.read_bytes())
    assert digest.hexdigest() == TREE
    old = OUT.parent / "1019-rc5-final-run"
    for name in ("index.json", "verify.json", "review.json", "analysis/rc5-public031-autoload-reload-report-v1.json", "analysis/native-current-ship-health-setter-calibration-report-v1.json"):
        p = old / name
        refs[str(p.resolve())] = {"path": str(p.resolve()), **fp(p)}
    bindings = []
    for name in UI_TOOLS:
        current = OUT / "source-tools" / name
        canonical = old / "tools-hash-binding" / name
        assert fp(current) == fp(canonical)
        refs[str(canonical.resolve())] = {"path": str(canonical.resolve()), **fp(canonical)}
        bindings.append({"archived_path": "source-tools/" + name, "matching_previous_canonical": str(canonical.resolve()), **fp(current)})
    index = {"schema": "eep.rc6.migration-checkpoint-index.v1", "status": "BYTE_IDENTICAL_COMPLETED_MIGRATION_SCOPED_V2_WITH_V1_FAIL_PRESERVED",
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": manifest["run_id"], "game_pid": process["pid"],
             "final_run_freeze": False, "active_logs_read_or_copied": False, "Mod_acceptance_pass": False, "source_tree_sha256": TREE,
             "selection_sha256": fp(OUT / "selection.json")["sha256"], "payload_file_count": len(rows), "payload_bytes": sum(x["bytes"] for x in rows),
             "native_sav_count": 7, "stages": STAGES, "actual_native_load_receipt_count": 5, "source_tool_files": len([x for x in rows if x["path"].startswith("source-tools/")]),
             "offline_analysis_local_AST_closure_count": len(offline), "UI_core_hash_bindings": bindings,
             "prepare_execution_source_snapshot_or_memory_proof_claimed": False,
             "source_boundary": "Complete static local Python closure for offline v2 analysis/test only; UI nine core bytes bound to prior canonical; changing indirect publish modules not claimed captured historical execution",
             "canonical_references_not_copied": sorted(refs.values(), key=lambda x: x["path"]), "files": rows,
             "limits": ["Active run and economy UI remain root-owned; no logs read", "v2 PASS_SCOPED is not v1 PASS or mathematically lossless migration", "Each real load may incur bounded small loss; extra public return load is explicit", "Associated mobile-starbase implementation remains raw/unverified", "Root flags are not design-local marker proof", "Templates and partial reports keep historical PENDING", "No Git/UI/production/tool mutations"]}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("run/** -text\nanalysis/** -text\nplans/** -text\nsource-tools/** -text\nsource_snapshot/** -text\n", encoding="ascii")
    print(json.dumps({k: index[k] for k in ("status", "payload_file_count", "payload_bytes", "native_sav_count", "actual_native_load_receipt_count", "source_tool_files", "offline_analysis_local_AST_closure_count")}))


if __name__ == "__main__":
    main()
