"""Independent bytes/receipt verification of an ended partial attempt."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]


def digest(p): return sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding="utf-8"))


def main():
    assert not (OUT / "verify.json").exists()
    index = read(OUT / "index.json")
    checks = {}
    for row in index["files"]:
        path = OUT / row["path"]
        assert path.is_relative_to(OUT) and path.read_bytes() == Path(row["source"]).read_bytes()
        assert digest(path) == row["sha256"] and path.stat().st_size == row["bytes"]
    assert len(index["files"]) == 146
    checks["146_source_copy_bytes_SHA_exact"] = True
    for row in index["canonical_references"]: assert digest(ROOT / row["path"]) == row["sha256"]
    checks["five_canonical_references_match"] = True
    receipt = read(OUT / "run/r7pu-economy-receipt.json")
    assert receipt["state"] == "CLEANUP_REQUIRED" and len(receipt["snapshots"]) == len(receipt["commands"]) == 4
    assert receipt["error_type"] == "error" and "SetForegroundWindow" in receipt["error"]
    assert len(receipt["cleanup_errors"]) == 2 and all("SetForegroundWindow" in e for e in receipt["cleanup_errors"])
    for sample in receipt["snapshots"]:
        prefix = Path(sample["archived"]).stem
        assert digest(OUT / "run" / (prefix + ".sav")) == sample["sha256"]
        assert digest(OUT / "run" / (prefix + ".audit.json")) == sample["audit_sha256"]
    for command in receipt["commands"]:
        action = command["input_action"]
        assert command["command"] == action["text"] == "fast_forward 30"
        assert read(OUT / "run" / (action["stage"] + ".action.json")) == action
        assert read(OUT / "run" / (action["stage"] + "-enter.action.json"))["scan_code"] == 28
    checks["four_completed_months_commands_Enter_and_original_failure_preserved"] = True
    savs = list((OUT / "run").glob("*.sav"))
    assert len(savs) == 5
    for path in savs:
        with zipfile.ZipFile(path) as archive: assert archive.testzip() is None
    checks["five_unedited_native_ZIPs_CRC_valid"] = True
    assert len(index["image_ocr_bindings"]) == 30
    for row in index["image_ocr_bindings"]:
        image, ocr = ROOT / row["image"]["path"], ROOT / row["ocr"]["path"]
        assert digest(image) == row["image"]["sha256"] == read(ocr)["image_sha256"] and digest(ocr) == row["ocr"]["sha256"]
    checks["30_GPU_OCR_image_SHA_bindings"] = True
    assert index["case_status"] == "PENDING" and all(v is None for v in index["four_operation_checks"].values())
    assert index["yearUI"] == "NOT_GENERATED" and len(index["missing_months"]) == 8
    checks["year_and_four_checks_still_PENDING_no_generated_missing_samples"] = True
    result = {"schema": "eep.rc7.purifier-partial-independent-byte-verify.v1", "status": "PASS_BYTES_CALLER_FAILURE_YEAR_PENDING",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": digest(OUT / "index.json"),
        "checks": checks, "payload_files_rechecked": 146, "case_status": "PENDING", "UI_Git_or_Mod_operations": False}
    with (OUT / "verify.json").open("x", encoding="utf-8", newline="\n") as f: f.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "verify_sha256": digest(OUT / "verify.json")}))


if __name__ == "__main__": main()
