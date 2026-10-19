"""Archive only completed RC6 r6g evidence and unchanged authored records."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
RUN = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T150008Z")
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
COLLECTOR = "cab98ce18119f27838456dd6118001cc7fee5254b3150c5e5c8fcf5365f7e747"
CHECKER = "0c31f76491c39aff56fb054088d2a8fa4b592eb7f0ad186c5f1ec0c6625832bd"
MATTERS = [0, 9, 10, 19, 20, 49, 50, 200, 10000]


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
def ref(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "kind": kind(path)}


def main():
    assert not (OUT / "index.json").exists(), "Do not overwrite sealed archive"
    raw = sorted(p for p in RUN.glob("r6g*") if p.is_file())
    assert len(raw) == 455 and sum(p.stat().st_size for p in raw) == 26146209
    assert len([p for p in raw if p.suffix == ".sav"]) == 22
    assert all(p.suffix in (".json", ".sav", ".jpg", ".png") for p in raw)
    assert digest(ROOT / "tools/runtime_growth_1019.py") == COLLECTOR
    assert digest(ROOT / "tools/check_growth_1019.py") == CHECKER
    author_names = [f"docs/evidence/1019-analysis/rc6-growth-pair-n{i:02d}-c{c}-observation-v1.json" for i, c in enumerate(MATTERS)]
    author_names += ["docs/evidence/1019-analysis/rc6-growth-c10000-cache-while-diagnosis-v1.json",
        "docs/evidence/1020-component-budget-native-probes-v1.json",
        "docs/evidence/1020-native-while-primary-evidence-v1.json",
        "docs/rc6-growth-pair-observation-1020.md", "docs/rc6-high-growth-export-budget-probe-1020.md",
        "docs/rc6-growth-execution-plan-1019.md", "docs/rc6-growth-execution-plan-1019.json"]
    assert len(author_names) == 16
    pairs = [(p, OUT / "run" / p.name) for p in raw]
    pairs += [(ROOT / p, OUT / "authored" / Path(p).name) for p in author_names]
    pairs += [(ROOT / "tools" / name, OUT / "source" / name) for name in ("runtime_growth_1019.py", "check_growth_1019.py")]
    selection = {"schema": "eep.rc6.growth-raw-selection.v1", "fixed_run_id": "20261019T150008Z",
        "raw_prefix": "r6g*", "completed_after_normal_stop": "2026-10-19T16:38:02.658777+00:00",
        "excluded": ["logs, including live or final error/game/system", "RC7/current-run pointer", "other economy raw saves", "Mod and tools mutations"],
        "files": [{"source": str(a), "path": b.relative_to(OUT).as_posix(), "bytes": a.stat().st_size, "sha256": digest(a), "kind": kind(a)} for a, b in pairs]}
    write(OUT / "selection.json", selection)
    for row, (source, dest) in zip(selection["files"], pairs):
        content = source.read_bytes()
        assert len(content) == row["bytes"] and sha256(content).hexdigest() == row["sha256"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as stream: stream.write(content)
        assert source.read_bytes() == dest.read_bytes()

    canonical_paths = ["docs/evidence/1019-rc6-economy/machine/r6mcyearui" + suffix for suffix in (".sav", ".audit.json", ".native-save.json")]
    canonical_paths += ["docs/evidence/1019-rc6-migration-checkpoint-v1/" + name for name in ("run/manifest.json", "index.json", "verify.json")]
    canonical_paths += ["docs/evidence/1019-rc6-static/" + name for name in ("candidate-rc6-gate.json", "candidate-rc6-open-kaishek.json", "source-index.json")]
    canonical_paths += [f"docs/evidence/1019-analysis/six-core-source-expectations-v{i}.json" for i in range(1, 5)]
    canonical_paths += ["docs/evidence/1020-growth-government-identity/" + name for name in ("old-tool/check_growth_1019.py", "original-evidence-index.json", "fixed-native-pairs-supplement-v1.json", "verification-v1.json")]
    canonical_paths += ["docs/evidence/1019-rc6-migration-checkpoint-v1/source-tools/eat_everything_origin/tools/audit_save.py"]
    canonical = [ref(ROOT / p) for p in canonical_paths]
    receipt = read(OUT / "run/r6g-growth-receipt.json")
    assert receipt["collector_sha256"] == COLLECTOR and len(receipt["snapshots"]) == 18
    stages = []
    for row in receipt["snapshots"]:
        prefix = Path(row["archived"]).stem
        save = OUT / "run" / (prefix + ".sav")
        observation = OUT / "run" / (prefix + ".growth-observation.json")
        assert digest(save) == row["sha256"] == read(observation)["save_sha256"]
        stages.append({"prefix": prefix, "C": row["C"], "phase": row["phase"], "date": row["date"],
            "save": ref(save), "audit": ref(OUT / "run" / (prefix + ".audit.json")), "observation": ref(observation)})
    roles = {}
    for prefix in ("r6grepeat", "r6greload", "r6gexport1", "r6gbudget1"):
        original = read(OUT / "run" / (prefix + ".native-save.json"))
        assert Path(original["archived"]).name == prefix + ".sav"
        assert digest(OUT / "run" / (prefix + ".sav")) == original["sha256"]
        roles[prefix] = {"save": ref(OUT / "run" / (prefix + ".sav")),
            "audit": ref(OUT / "run" / (prefix + ".audit.json")),
            "exact_native_save_receipt": ref(OUT / "run" / (prefix + ".native-save.json")), "date": original["date"]}
    load = read(OUT / "run/r6gload.load.json")
    assert Path(load["source"]).name == "r6grepeat.sav" and load["source_sha256"] == roles["r6grepeat"]["save"]["sha256"]
    images = []
    for file in raw:
        if not file.name.endswith(".ocr.json"): continue
        ocr = read(OUT / "run" / file.name)
        image = OUT / "run" / Path(ocr["image"]).name
        assert image.is_file() and digest(image) == ocr["image_sha256"]
        images.append({"ocr": ref(OUT / "run" / file.name), "image": ref(image),
            "capture": ocr["capture"], "captured_at_utc": ocr["captured_at_utc"], "pid": ocr["pid"]})
    findings = []
    for i, c in enumerate(MATTERS):
        p = OUT / "authored" / f"rc6-growth-pair-n{i:02d}-c{c}-observation-v1.json"
        data = read(p)
        findings.append({"C": c, "report": ref(p), "status": data["status"], "check_count": data["check_count"],
            "failure_count": data["failure_count"], "failed_check_names": [v["check"] for v in data["failed_checks"]]})
    n08 = read(OUT / "authored/rc6-growth-pair-n08-c10000-observation-v1.json")
    exports = [row for row in n08["failed_checks"] if " export " in row["check"]]
    assert len(exports) == 7
    probe = read(OUT / "authored/1020-component-budget-native-probes-v1.json")
    assert probe["single_sync_C20500"]["intended_200_reward_budget_met"] is False
    index = {"schema": "eep.rc6.growth-raw-archive-index.v1", "status": "ARCHIVED_WITH_KNOWN_RC6_FAILURES_NO_ACCEPTANCE",
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T150008Z", "production_tree_sha256": TREE,
        "payload_files": len(pairs), "payload_bytes": sum(row["bytes"] for row in selection["files"]),
        "raw_files": 455, "raw_bytes": 26146209, "native_sav_count": 22, "original_matrix_samples": 18,
        "authored_files": 16, "source_snapshots": 2, "files": selection["files"], "canonical_references": canonical,
        "stages": stages, "post_matrix_roles": roles, "load_role": {"receipt": ref(OUT / "run/r6gload.load.json"), "exact_source_role": "r6grepeat", "native_state_verified_at_load": load["state_verified"]},
        "image_ocr_bindings": images, "original_pair_reports": findings,
        "preserved_failure": {"n08_original_seven_exports": exports, "later_reexport_does_not_replace_original": True,
            "single_call_reward_budget": {"actual_R": 300, "actual_pending": 110, "expected_R": 400, "expected_pending": 10, "status": "FAIL"}},
        "source_boundary": "Exact collector hash matches original receipt; corrected checker hash matches sealed diagnostic author report; disk source closure does not attest historical process memory. Original a66 reports and identity-only supplement unchanged.",
        "final_logs_not_in_this_package": True, "RC7_or_current_pointer_read": False,
        "whole_growth_or_Mod_PASS": False, "UI_Git_Mod_tool_changes": False}
    write(OUT / "index.json", index)
    print(json.dumps({"status": index["status"], "payload_files": len(pairs), "payload_bytes": index["payload_bytes"],
        "canonical_refs": len(canonical), "image_pairs": len(images), "index_sha256": digest(OUT / "index.json")}))


if __name__ == "__main__": main()
