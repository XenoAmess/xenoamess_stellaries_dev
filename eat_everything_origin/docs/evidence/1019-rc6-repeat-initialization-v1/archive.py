"""Freeze completed r6mcinit2 only; never access live logs or UI."""
from datetime import datetime, timezone
from hashlib import sha256
import copy
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
RUN = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T150008Z")
BASE = "docs/evidence/1019-requirements/rc6-runtime-progress-v1.json"
BASE_SHA = "94ed603301ae0913d2c3eb602e4b6a2b21eeeadf4f23443000cd2bb77b9016aa"
SAVE_SHA = "bd4104dd2e31cfff0d2f76abf55e2eb303709ec86ca3118ec0d9fb6a59a3a696"
REPORT_SHA = "d2ad24b26236b28b2d4f472da0047a3455cc3ef0c7730a759628878f9fd2cc66"
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
sys.path.insert(0, str(ROOT / "tools"))
import publish_1019 as release
import runtime_index_1019 as helper


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def ref(path, kind="analysis"):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "kind": kind}


def kind(path):
    if path.suffix == ".sav": return "native_save"
    if path.suffix in (".jpg", ".png"): return "screenshot"
    if path.name.endswith((".action.json", ".native-save.json")): return "actions"
    return "analysis"


def main():
    assert not (OUT / "index.json").exists(), "Archive already sealed"
    assert digest(ROOT / BASE) == BASE_SHA
    originals = sorted(p for p in RUN.glob("r6mcinit2*") if p.is_file())
    assert len(originals) == 38
    assert all(p.suffix in (".jpg", ".json", ".sav") for p in originals)
    authored = [
        "docs/evidence/1019-analysis/rc6-r6mc-repeat-initialization-intake-v1.json",
        "docs/evidence/1019-analysis/rc6-r6mc-repeat-initialization-report-v1.json",
        "docs/evidence/1019-analysis/rc6-r6mc-repeat-initialization-case-proposal-v1.json",
        "docs/evidence/1019-analysis/rc6-r6mcyearui-repeat-initialization-observation-v1.json",
        "docs/evidence/1019-analysis/rc6-r6mcinit2-repeat-initialization-observation-v1.json",
        "docs/rc6-repeat-initialization-analysis-1019.md",
    ]
    source_pairs = [(p, OUT / "run" / p.name) for p in originals]
    source_pairs += [(ROOT / p, OUT / "authored" / Path(p).name) for p in authored]
    selection = {"schema": "eep.rc6.repeat-init-archive-selection.v1", "run_id": "20261019T150008Z",
        "source_pairs": [{"source": str(src), "path": dst.relative_to(OUT).as_posix(),
                          "bytes": src.stat().st_size, "sha256": digest(src)} for src, dst in source_pairs],
        "excluded": ["before SAV duplicate", "growth r6g", "live logs", "other run stages", "existing sealed progress and UI packets"],
        "role_rule": "Exact r6mcinit2.native-save.json for after; never select receipts by shared SAV SHA"}
    write(OUT / "selection.json", selection)
    files = []
    for row, (src, dst) in zip(selection["source_pairs"], source_pairs):
        dst.parent.mkdir(parents=True, exist_ok=True)
        payload = src.read_bytes()
        assert len(payload) == row["bytes"] and sha256(payload).hexdigest() == row["sha256"]
        with dst.open("xb") as stream: stream.write(payload)
        assert src.read_bytes() == dst.read_bytes()
        files.append({**row, "kind": kind(dst)})

    canonical_paths = [
        "docs/evidence/1019-rc6-economy/machine/r6mcyearui.sav",
        "docs/evidence/1019-rc6-economy/machine/r6mcyearui.audit.json",
        "docs/evidence/1019-rc6-economy/machine/r6mcyearui.native-save.json",
        "docs/evidence/1019-rc6-economy/machine/archive-index.json",
        "docs/evidence/1019-rc6-economy/machine/byte-verification-v1.json",
        "docs/evidence/1019-rc6-migration-checkpoint-v1/run/manifest.json",
        "docs/evidence/1019-rc6-migration-checkpoint-v1/index.json",
        "docs/evidence/1019-rc6-migration-checkpoint-v1/verify.json",
        "docs/evidence/1019-rc6-static/candidate-rc6-open-kaishek.json",
        "docs/evidence/1019-rc6-static/candidate-rc6-gate.json",
        "docs/evidence/1019-rc6-static/source-index.json",
        "docs/rc6-repeat-initialization-execution-1019.md",
    ]
    tools_root = ROOT / "docs/evidence/1019-rc6-migration-checkpoint-v1/source-tools"
    canonical_paths += [p.relative_to(ROOT).as_posix() for p in sorted(tools_root.rglob("*")) if p.is_file()]
    canonical = [ref(ROOT / p, kind(ROOT / p)) for p in canonical_paths]
    assert len(canonical) == 25
    report = json.loads((OUT / "authored/rc6-r6mc-repeat-initialization-report-v1.json").read_text(encoding="utf-8"))
    assert digest(OUT / "authored/rc6-r6mc-repeat-initialization-report-v1.json") == REPORT_SHA
    author_proposal = json.loads((OUT / "authored/rc6-r6mc-repeat-initialization-case-proposal-v1.json").read_text(encoding="utf-8"))
    assert len(report["checks"]) == 41 and all(v is True for v in report["checks"].values())
    assert report["strict_comparison"]["differences"] == []

    roles = {}
    for role, directory, prefix in (("before", ROOT / "docs/evidence/1019-rc6-economy/machine", "r6mcyearui"),
                                    ("after", OUT / "run", "r6mcinit2")):
        roles[role] = {"save": ref(directory / (prefix + ".sav"), "native_save"),
            "audit": ref(directory / (prefix + ".audit.json")),
            "native_ui_save_receipt": ref(directory / (prefix + ".native-save.json"), "actions"),
            "date": "2201.01.01", "role_selection": "exact prefix and receipt path, not SHA discovery"}
        receipt = json.loads((directory / (prefix + ".native-save.json")).read_text(encoding="utf-8"))
        assert Path(receipt["archived"]).name == prefix + ".sav" and receipt["sha256"] == SAVE_SHA
        assert digest(directory / (prefix + ".sav")) == SAVE_SHA

    images = []
    for row in files:
        if not row["path"].endswith(".ocr.json"): continue
        ocr = json.loads((OUT / row["path"]).read_text(encoding="utf-8"))
        image_path = OUT / "run" / Path(ocr["image"]).name
        assert digest(image_path) == ocr["image_sha256"]
        images.append({"ocr": ref(OUT / row["path"]), "image": ref(image_path, "screenshot"),
            "capture": ocr["capture"], "pid": ocr["pid"], "captured_at_utc": ocr["captured_at_utc"]})
    index = {"schema": "eep.rc6.repeat-init-archive-index.v1", "status": "PENDING_CASE_RAW_ARCHIVED",
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T150008Z",
        "production_tree_sha256": TREE, "payload_files": len(files), "payload_bytes": sum(r["bytes"] for r in files),
        "native_after_save_count": 1, "before_save_not_copied": True, "authored_file_count": 6,
        "selection": ref(OUT / "selection.json"), "files": files, "canonical_references": canonical,
        "native_roles": roles, "image_ocr_bindings": images,
        "author_report": ref(OUT / "authored/rc6-r6mc-repeat-initialization-report-v1.json"),
        "author_report_scoped_checks": {"true": 41, "false": 0, "null": 0},
        "initial_driver_failure": {"field": "government_raw", "exception": "KeyError", "before_any_physical_input": True,
            "evidence_scope": "root handoff and unchanged execution/analysis documentation, not recreated raw exception",
            "raw_exception_file_available": False, "game_or_Mod_failure": False},
        "source_scope": "Reuse previously frozen checkpoint sources as on-disk evidence; no process-memory source attestation",
        "existing_progress_index_unchanged": {"path": BASE, "sha256": BASE_SHA},
        "case_status_promoted": False, "final_result_written": False, "growth_or_logs_read": False,
        "UI_or_Git_operations": False}
    write(OUT / "index.json", index)
    evidence = [ref(OUT / row["path"], row["kind"]) for row in files]
    for row in roles["before"].values():
        if isinstance(row, dict) and "path" in row: evidence.append(row)
    for row in canonical:
        if row not in evidence: evidence.append(row)
    evidence.append(ref(OUT / "index.json"))
    case = {"status": "PENDING", "checks": author_proposal["checks"], "evidence": evidence,
            "run_ids": ["20261019T150008Z"], "production_tree_sha256": TREE}
    proposal = {"schema": "eep.1019.repeat-initialization-case-proposal.v2", "status": "PENDING",
        "case_id": "repeat_initialization", "case_payload": case, "native_roles": roles,
        "author_report": index["author_report"], "check_basis": author_proposal["check_basis"],
        "scope": author_proposal["scope"], "sample_collection_complete": True,
        "remaining": ["root review of scoped observations and exact roles", "final stopped-run logs"],
        "initial_driver_failure": index["initial_driver_failure"], "final_result_written": False,
        "limits": author_proposal["limitations"]}
    dest = ROOT / "docs/evidence/1019-requirements/rc6-repeat-initialization-case-proposal-v2.json"
    write(dest, proposal)

    _, data = helper.load_progress(ROOT / BASE, ROOT)
    before = copy.deepcopy(data)
    helper.bind_run(data, "docs/evidence/1019-rc6-migration-checkpoint-v1/run/manifest.json", ROOT, ["repeat_initialization"])
    for entry in evidence:
        helper.attach(data, "repeat_initialization", "20261019T150008Z", entry["kind"], entry["path"], ROOT)
    for check, result in case["checks"].items():
        helper.observe_check(data, "repeat_initialization", check, result, index["author_report"]["path"], "20261019T150008Z", ROOT)
    assert all(c["status"] == "PENDING" for c in data["cases"].values())
    missing = helper.missing(data)
    assert missing["cases"]["repeat_initialization"]["missing_evidence_kinds"] == ["log"]
    assert missing["cases"]["repeat_initialization"]["missing_or_failed_checks"] == []
    patch = {"schema": "eep.rc6.pending-progress-supplement-proposal.v1", "status": "PENDING_NOT_APPLIED",
        "base_index": {"path": BASE, "sha256": BASE_SHA}, "proposal": ref(dest),
        "only_case_to_merge": "repeat_initialization", "before_case": before["cases"]["repeat_initialization"],
        "proposed_case": data["cases"]["repeat_initialization"], "missing_after_proposed_merge": missing["cases"]["repeat_initialization"],
        "all_cases_remain_PENDING": True, "base_index_written": False, "final_result_written": False}
    write(ROOT / "docs/evidence/1019-requirements/rc6-runtime-progress-v1-repeat-initialization-patch-proposal.json", patch)
    write(ROOT / "docs/evidence/1019-requirements/rc6-runtime-progress-v1-repeat-initialization-supplement-missing.json", missing)
    assert digest(ROOT / BASE) == BASE_SHA
    print(json.dumps({"status": "PENDING", "payload_files": len(files), "payload_bytes": index["payload_bytes"],
        "canonical_refs": len(canonical), "image_ocr_pairs": len(images), "index_sha256": digest(OUT / "index.json")}))


if __name__ == "__main__": main()
