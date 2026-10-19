"""Independent raw bytes, source boundary, benchmarks and image bindings check."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent


def fp(path):
    raw = path.read_bytes()
    return len(raw), sha256(raw).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    assert index["selection_sha256"] == fp(OUT / "selection.json")[1]
    assert index["files"] == selection["files"]
    assert len(index["files"]) == index["payload_file_count"]
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"]), row["path"]
        assert Path(row["path"]).suffix not in (".sav", ".log")
    for row in index["canonical_references_not_copied"]:
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"])
    old = OUT / "old-source/runtime.py"
    new = OUT / "current-source/eat_everything_origin/tools/runtime.py"
    assert fp(old)[1] == index["old_runtime_sha256"] != index["new_runtime_sha256"] == fp(new)[1]
    assert index["source_closure_file_count"] == 18
    comparisons = Counter(row["status"] for row in index["baseline_comparisons"])
    assert comparisons == {"UNCHANGED_FROM_CANONICAL": 8, "CHANGED_FROM_CANONICAL": 1, "NO_CANONICAL_BASELINE_IN_THIS_SUPPLEMENT": 9}
    benchmarks = OUT / "release-evidence/docs/evidence/1019-analysis"
    scan = json.loads((benchmarks / "ocr-screenshot-scan-benchmark-v1.json").read_bytes())
    assert scan["runtime_tool_sha256"] == fp(new)[1]
    assert len(scan["rounds"]) == 3 and scan["all_rounds_file_mapping_stable"]
    for row in scan["rounds"]:
        assert row["reference_count"] == row["observed_count"] == 15003
        assert row["all_path_mtimes_exactly_equal"] and row["reference_mapping_sha256"] == row["observed_mapping_sha256"]
    images = []
    for path in sorted((OUT / "nrel-failed-attempts").glob("*.ocr.json")):
        ocr = json.loads(path.read_bytes())
        image = OUT / "nrel-failed-attempts" / Path(ocr["image"]).name
        assert fp(image)[1] == ocr["image_sha256"] and ocr["pid"] == index["game_pid"] == 36912
        images.append({"stage": ocr["stage"], "captured_at_utc": ocr["captured_at_utc"], "image_sha256": ocr["image_sha256"], "ocr_sha256": fp(path)[1]})
    assert len(images) == 9
    receipt = json.loads((OUT / "nrel-failed-attempts/nrel-source-import-receipt.json").read_bytes())
    assert receipt["status"] == "RAW_BYTE_IDENTICAL_IMPORT_ONLY"
    assert not (OUT / "nrel-failed-attempts/nrel-source-load.load.json").exists()
    # Git's stdin-paths attribute lookup requires forward-slash Windows paths.
    paths = [(OUT / row["path"]).resolve().as_posix() for row in index["files"]]
    lines = "\n".join(paths) + "\n"
    common = {"input": lines, "text": True, "encoding": "utf-8", "capture_output": True, "check": True}
    raw = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], **common).stdout.splitlines()
    filtered = subprocess.run(["git", "hash-object", "--stdin-paths"], **common).stdout.splitlines()
    attrs = subprocess.run(["git", "check-attr", "text", "--stdin"], **common).stdout.splitlines()
    assert len(raw) == len(filtered) == len(attrs) == len(paths) and raw == filtered
    assert all(line.endswith(": text: unset") for line in attrs)
    report = {"schema": "eep.rc4.midrun-tool-source-verification.v1", "status": "PASS_BYTE_SOURCE_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "payload_files_rechecked": len(paths), "payload_bytes": sum(row["bytes"] for row in index["files"]),
              "canonical_refs_rechecked": len(index["canonical_references_not_copied"]), "baseline_comparison_counts": dict(comparisons),
              "screenshot_scan_benchmark": {"archived_existing_result_only": True, "rounds": 3, "paths_each_round": 15003, "all_path_mtimes_exactly_equal": True, "runtime_sha256": scan["runtime_tool_sha256"]},
              "tool_tests": "Six tests PASS reported in archived release doc; not rerun here", "image_ocr_bindings": images,
              "earliest_archived_new_tool_output_utc": min(row["captured_at_utc"] for row in images),
              "memory_loaded_source_proof": False, "git_byte_preservation_files": len(paths), "final_run_freeze": False,
              "load_injury_result": "HUD_DATE_VERIFICATION_FAILED; injury/save/export NOT_EXECUTED; two play0 guards rejected before typing",
              "Mod_acceptance_pass": False}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "image_ocr_bindings"}, indent=2))


if __name__ == "__main__":
    main()
