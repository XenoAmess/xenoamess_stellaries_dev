"""Freeze completed RC7 growth only; leave the active r7ev branch untouched."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
REPO = ROOT.parent
RUN = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z")
TREE = "61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0"
EXPECTED = {"tools/check_growth_1019.py": "a8d70f1015b6f1f4026ae811c38653997fd41a55bbca9b9b8fba391fb4070bf5",
    "tools/runtime_growth_1019.py": "cab98ce18119f27838456dd6118001cc7fee5254b3150c5e5c8fcf5365f7e747",
    "tools/publish_1019.py": "06c60c0a9bd406580314999ae6649365bb5c1fa6c7152c0b0a7fb5a420e06918"}
MATTERS = (0, 9, 10, 19, 20, 49, 50, 200, 10000)


def digest(path): return sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
def kind(path):
    if path.suffix == ".sav": return "native_save"
    if path.suffix in (".jpg", ".png"): return "screenshot"
    if path.name.endswith((".action.json", ".native-save.json", ".load.json")): return "actions"
    return "analysis"
def ref(path): return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "kind": kind(path)}


def local_source_closure():
    queue = [ROOT / name for name in EXPECTED]
    seen = set()
    while queue:
        file = queue.pop(0).resolve()
        if file in seen: continue
        seen.add(file)
        syntax = ast.parse(file.read_text(encoding="utf-8-sig"))
        names = set()
        for node in ast.walk(syntax):
            if isinstance(node, ast.Import): names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module: names.add(node.module.split(".")[0])
        for name in sorted(names):
            for parent in (file.parent, ROOT / "tools", ROOT / "testing", REPO / "tools"):
                candidate = parent / (name + ".py")
                if candidate.is_file():
                    queue.append(candidate)
                    break
    return sorted(seen)


def main():
    assert not (OUT / "index.json").exists(), "Do not overwrite this immutable package"
    for path, expected in EXPECTED.items(): assert digest(ROOT / path) == expected
    raw = sorted(p for p in RUN.iterdir() if p.is_file() and p.name.startswith(("r7mx", "r7g")))
    assert len(raw) == 500 and sum(p.stat().st_size for p in raw) == 27845352
    assert len([p for p in raw if p.suffix == ".sav"]) == 23
    boot = sorted(p for p in RUN.glob("r7-boot-*") if p.is_file())
    assert len(boot) == 6
    author = [f"docs/evidence/1019-analysis/rc7-growth-pair-n{i:02d}-c{c}-observation-v1.json" for i, c in enumerate(MATTERS)]
    author += ["docs/evidence/1019-analysis/rc7-growth-observer-method-v1.json",
        "docs/evidence/1019-analysis/rc7-growth-matrix-independent-summary-v1.json",
        "docs/rc7-growth-pair-observation-1020.md",
        "docs/evidence/1019-analysis/rc7-growth-native-report-v1.json",
        "docs/rc7-growth-supplements-report-1020.md",
        "docs/rc7-explicit-growth-budget-execution-1020.md"]
    assert len(author) == 15
    source = local_source_closure()
    pairs = [(p, OUT / "run" / p.name, "immutable_growth_raw") for p in raw]
    pairs += [(p, OUT / "preflight" / p.name, "completed_initial_GPU_capture") for p in boot]
    pairs += [(RUN / name, OUT / "run" / name, "active_run_immutable_prepare_metadata_not_final_stop") for name in ("manifest.json", "process.json")]
    pairs += [(ROOT / name, OUT / "authored" / Path(name).name, "sealed_author" if not name.endswith("rc7-explicit-growth-budget-execution-1020.md") else "working_execution_plan_snapshot") for name in author]
    pairs += [(p, OUT / "source" / p.relative_to(REPO), "disk_source_no_historical_memory_attestation") for p in source]
    selected = [{"source": str(src), "path": dst.relative_to(OUT).as_posix(), "bytes": src.stat().st_size,
                 "sha256": digest(src), "kind": kind(src), "source_class": source_class} for src, dst, source_class in pairs]
    write(OUT / "selection.json", {"schema": "eep.rc7.growth-selection.v1", "run_id": "20261019T164112Z",
        "worker_exit_confirmed_by_root": {"worker": 83762, "exit_code": 0},
        "files": selected, "excluded": ["r7ev* active branch", "live logs", "current-run pointer", "duplicate 59 Mod source files"],
        "three_declared_source_hashes": EXPECTED})
    for row, (src, dst, _) in zip(selected, pairs):
        content = src.read_bytes()
        assert sha256(content).hexdigest() == row["sha256"] and len(content) == row["bytes"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open("xb") as stream: stream.write(content)
        assert src.read_bytes() == dst.read_bytes()
    canonical_names = ["docs/evidence/1019-rc7-static/" + n for n in ("source-index.json", "byte-verification-v1.json", "candidate-rc7-gate.json", "candidate-rc7-open-kaishek.json")]
    static = read(ROOT / canonical_names[0])
    mod_rows = [r for r in static["files"] if r["path"].startswith("candidate-rc7/mod/")]
    assert len(mod_rows) == 59
    for row in mod_rows:
        path = ROOT / "docs/evidence/1019-rc7-static" / row["path"]
        assert digest(path) == row["sha256"]
        canonical_names.append(path.relative_to(ROOT).as_posix())
    canonical_names += [f"docs/evidence/1019-analysis/six-core-source-expectations-v{i}.json" for i in range(1, 6)]
    canonical_names += ["docs/evidence/1019-rc6-economy/machine/r6mcyearui" + s for s in (".sav", ".audit.json", ".native-save.json")]
    canonical_names += ["docs/evidence/1019-rc6-growth-v1/" + n for n in ("index.json", "verify.json")]
    canonical = [ref(ROOT / name) for name in canonical_names]
    manifest = read(OUT / "run/manifest.json")
    assert manifest["run_id"] == "20261019T164112Z" and manifest["copied_mod_tree_sha256"] == TREE
    assert manifest["language"] == "l_simp_chinese" and len(manifest["repository_mod_files"]) == 59
    imported = manifest["seeded_save"]
    assert Path(imported["source"]).name == "r6mcyearui.sav"
    assert digest(ROOT / "docs/evidence/1019-rc6-economy/machine/r6mcyearui.sav") == imported["sha256"]
    receipt = read(OUT / "run/r7mx-growth-receipt.json")
    assert len(receipt["snapshots"]) == 18 and receipt["collector_sha256"] == EXPECTED["tools/runtime_growth_1019.py"]
    stages = []
    for row in receipt["snapshots"]:
        prefix = Path(row["archived"]).stem
        save, obs = OUT / "run" / (prefix + ".sav"), OUT / "run" / (prefix + ".growth-observation.json")
        assert digest(save) == row["sha256"] == read(obs)["save_sha256"]
        stages.append({"prefix": prefix, "C": row["C"], "phase": row["phase"], "date": row["date"],
            "save": ref(save), "audit": ref(OUT / "run" / (prefix + ".audit.json")), "observation": ref(obs)})
    roles = {}
    for prefix in ("r7ganchor", "r7grepeat", "r7greload", "r7gbudget1", "r7gbudget2"):
        original = read(OUT / "run" / (prefix + ".native-save.json"))
        assert Path(original["archived"]).name == prefix + ".sav"
        assert digest(OUT / "run" / (prefix + ".sav")) == original["sha256"]
        roles[prefix] = {"save": ref(OUT / "run" / (prefix + ".sav")), "audit": ref(OUT / "run" / (prefix + ".audit.json")),
            "exact_native_save_receipt": ref(OUT / "run" / (prefix + ".native-save.json")), "date": original["date"]}
    images = []
    for src in raw + boot:
        if not src.name.endswith(".ocr.json"): continue
        folder = "preflight" if src in boot else "run"
        ocr = read(OUT / folder / src.name)
        image = OUT / folder / Path(ocr["image"]).name
        assert digest(image) == ocr["image_sha256"]
        images.append({"ocr": ref(OUT / folder / src.name), "image": ref(image), "capture": ocr["capture"],
                       "pid": ocr["pid"], "captured_at_utc": ocr["captured_at_utc"]})
    report_path = OUT / "authored/rc7-growth-native-report-v1.json"
    assert digest(report_path) == "4677e82c62ce30851f247691dad38703f52d6187ce26f2e63ea9fe0d7df9d1a3"
    report = read(report_path)
    assert report["status"] == "PASS_SCOPED" and report["startup_stability"]["status"] == "NOT_PROVIDED"
    counts = {name: len(report[name]["checks"]) for name in ("matrix", "ordinary_controls", "repeat", "reload", "budget")}
    assert counts == {"matrix": 1125, "ordinary_controls": 616, "repeat": 20, "reload": 20, "budget": 69}
    assert all(row["passed"] is True for name in counts for row in report[name]["checks"])
    assert report["repeat"]["strict_gamestate_equal"] is True and report["reload"]["strict_gamestate_equal"] is False
    index = {"schema": "eep.rc7.growth-archive-index.v1", "status": "GROWTH_SCOPED_REPORT_AND_RAW_ARCHIVED_FINAL_ACCEPTANCE_PENDING",
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T164112Z", "production_tree_sha256": TREE,
        "run_still_active_not_final_freeze": True, "payload_files": len(selected), "payload_bytes": sum(r["bytes"] for r in selected),
        "growth_raw_files": 500, "growth_raw_bytes": 27845352, "preflight_GPU_raw_files": 6, "native_sav_count": 23,
        "matrix_native_samples": 18, "authored_files": 15, "AST_local_source_files": len(source),
        "files": selected, "canonical_references": canonical, "stages": stages, "native_roles": roles, "image_ocr_bindings": images,
        "imported_C0": {"original_source": ref(ROOT / "docs/evidence/1019-rc6-economy/machine/r6mcyearui.sav"),
            "actual_load": ref(OUT / "run/r7gloadc0b.load.json"), "anchor": roles["r7ganchor"], "not_RC7_new_game_or_year": True},
        "formal_report": ref(report_path), "formal_report_check_counts": counts, "formal_report_total_checks": 1850,
        "formal_report_startup_stability": "NOT_PROVIDED", "repeat_ZIP_equal_final": (OUT / "run/r7grepeat.sav").read_bytes() == (OUT / "run/r7mx-n08-c10000-final.sav").read_bytes(),
        "reload_full_bytes_equal_claim": False, "historical_RC6_failure_unchanged": True,
        "preserved_preflight_failures": [{"failure": "Windows SetForegroundWindow rejected initial load", "raw_attempt_file_available": False,
            "evidence": "unchanged authored rc7-explicit-growth-budget-execution-1020.md and root handoff; successful retry separate r7gloadc0b"},
            {"failure": "r7g collector prefix collided with existing anchor files", "before_matrix_input": True, "raw_exception_file_available": False,
             "evidence": "unchanged authored execution plan; actual successful matrix uses r7mx"}],
        "source_boundary": "Three required tool bytes a8/cab/06 and statically resolved local dependencies captured from disk; exact source/copy checked at capture. No historical process-memory attestation. Preserve later source drift, never replace this copy.",
        "r7ev_or_live_logs_or_current_pointer_read": False, "UI_Git_Mod_tools_modified": False, "final_result_written": False}
    assert index["repeat_ZIP_equal_final"] is True
    write(OUT / "index.json", index)
    print(json.dumps({"status": index["status"], "payload_files": len(selected), "payload_bytes": index["payload_bytes"],
        "tool_closure_files": len(source), "image_pairs": len(images), "canonical_refs": len(canonical), "index_sha256": digest(OUT / "index.json")}))


if __name__ == "__main__": main()
