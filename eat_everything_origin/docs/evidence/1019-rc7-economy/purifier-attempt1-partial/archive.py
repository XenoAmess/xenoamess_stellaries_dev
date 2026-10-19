"""Keep the ended r7pu foreground-error attempt without accepting its year."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
RUN = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T164112Z")


def digest(p): return sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p, value):
    with p.open("x", encoding="utf-8", newline="\n") as f: f.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
def ref(p): return {"path": p.relative_to(ROOT).as_posix(), "sha256": digest(p)}


def main():
    assert not (OUT / "index.json").exists()
    total = RUN / "r7pu-economy-receipt.json"
    assert digest(total) == "496323a628d8949410425de14cd4c3eb99446ee0059e9935cfa8614b20238625"
    receipt = read(total)
    assert receipt["state"] == "CLEANUP_REQUIRED" and len(receipt["snapshots"]) == len(receipt["commands"]) == 4
    originals = sorted(p for p in RUN.iterdir() if re.match(r"r7pu(?:-|m0[0-4](?:[-.]|$))", p.name) and p.is_file())
    assert len(originals) == 144 and sum(p.stat().st_size for p in originals) == 8430760
    assert len([p for p in originals if p.suffix == ".sav"]) == 5
    source = ROOT / "tools/runtime_economy_1019.py"
    assert digest(source) == receipt["collector_sha256"]
    pairs = [(p, OUT / "run" / p.name) for p in originals]
    pairs += [(RUN / "manifest.json", OUT / "run/manifest.json"), (source, OUT / "source/runtime_economy_1019.py")]
    files = []
    for src, dst in pairs:
        content = src.read_bytes()
        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open("xb") as f: f.write(content)
        assert src.read_bytes() == dst.read_bytes()
        files.append({"source": str(src), "path": dst.relative_to(OUT).as_posix(), "bytes": len(content), "sha256": sha256(content).hexdigest()})
    images = []
    for src in originals:
        if not src.name.endswith(".ocr.json"): continue
        ocr = read(OUT / "run" / src.name)
        image = OUT / "run" / Path(ocr["image"]).name
        assert digest(image) == ocr["image_sha256"]
        images.append({"ocr": ref(OUT / "run" / src.name), "image": ref(image)})
    canonical = [ref(ROOT / name) for name in ("docs/evidence/1019-rc7-growth-v1/index.json", "docs/evidence/1019-rc7-growth-v1/verify.json",
        "docs/evidence/1019-rc7-static/source-index.json", "docs/evidence/1019-rc7-static/candidate-rc7-open-kaishek.json",
        "docs/evidence/1019-baseline-reference-map/baseline-031-economy-map-v1.json")]
    result = {"schema": "eep.rc7.purifier-partial-attempt-archive.v1", "status": "COLLECTOR_FOREGROUND_FAILURE_YEAR_PENDING",
        "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T164112Z", "prefix": "r7pu", "root_worker_reference": 37801,
        "files": files, "payload_files": len(files), "payload_bytes": sum(x["bytes"] for x in files),
        "image_ocr_bindings": images, "canonical_references": canonical,
        "original_total_receipt": ref(OUT / "run/r7pu-economy-receipt.json"),
        "collector_state": receipt["state"], "error_type": receipt["error_type"], "error": receipt["error"], "cleanup_errors": receipt["cleanup_errors"],
        "completed_months": 4, "existing_native_samples": ["r7pum00", "r7pum01", "r7pum02", "r7pum03", "r7pum04"],
        "missing_months": ["r7pum" + str(i).zfill(2) for i in range(5, 13)], "yearUI": "NOT_GENERATED",
        "case_status": "PENDING", "four_operation_checks": {"no_resource_injection": None, "no_trade_subsidy": None, "no_job_closure": None, "no_ship_disband": None},
        "failure_scope": "Windows foreground call and cleanup failure; not a native Mod economy failure or completed 12-month case",
        "post_media_or_live_logs_or_other_branch_read": False, "UI_Git_Mod_tool_operations": False, "final_result_written": False}
    write(OUT / "index.json", result)
    print(json.dumps({"status": result["status"], "payload_files": len(files), "payload_bytes": result["payload_bytes"],
        "image_pairs": len(images), "index_sha256": digest(OUT / "index.json")}))


if __name__ == "__main__": main()
