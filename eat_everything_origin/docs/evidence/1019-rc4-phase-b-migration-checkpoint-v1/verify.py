"""Verify the immutable phase-B whitelist without reading active logs."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import zipfile

OUT = Path(__file__).resolve().parent
STAGES = ("m031load", "m031sync", "m031reload", "mpaidload", "mpaidsync", "mpaidreload", "rdesignsync", "rdesignreload", "rnamesync", "rnameload", "rfleetsync")


def fp(path):
    data = path.read_bytes()
    return len(data), sha256(data).hexdigest()


def main():
    index_bytes = (OUT / "index.json").read_bytes()
    index = json.loads(index_bytes)
    selection = json.loads((OUT / "selection.json").read_bytes())
    assert sha256((OUT / "selection.json").read_bytes()).hexdigest() == index["selection_sha256"]
    assert selection["files"] == index["files"]
    assert len(index["files"]) == index["payload_file_count"] == 462
    for entry in index["files"]:
        assert fp(OUT / entry["path"]) == fp(Path(entry["source"])) == (entry["bytes"], entry["sha256"]), entry["path"]
        assert "rsizeonly" not in entry["path"]
        assert entry["path"] != "stop.json" and not entry["path"].startswith("logs/")
        assert Path(entry["path"]).suffix != ".log"
    for ref in index["canonical_references_not_copied"] + index["canonical_Mod_59_files_referenced_not_duplicated"]:
        assert fp(Path(ref["path"])) == (ref["bytes"], ref["sha256"]), ref["path"]
    assert len(index["canonical_Mod_59_files_referenced_not_duplicated"]) == 59
    assert {p.stem for p in (OUT / "run").glob("*.sav")} == set(STAGES)
    manifest_hash = fp(OUT / "manifest.json")[1]
    save_rows = []
    for stage in STAGES:
        path = OUT / "run" / (stage + ".sav")
        receipt = json.loads(path.with_suffix(".native-save.json").read_bytes())
        audit = json.loads(path.with_suffix(".audit.json").read_bytes())
        observed = json.loads((OUT / "analysis" / ("rc4-" + stage + "-observation-v1.json")).read_bytes())
        assert fp(path)[1] == receipt["sha256"] == audit["save_sha256"] == observed["save_sha256"]
        assert observed["manifest_sha256"] == manifest_hash
        assert observed["production_tree_sha256"] == index["mod_tree_sha256"]
        with zipfile.ZipFile(path) as archive:
            data = archive.read("gamestate")
        assert sha256(data).hexdigest() == audit["gamestate_sha256"] == observed["gamestate_sha256"]
        save_rows.append({"stage": stage, "date": receipt["date"], "sha256": receipt["sha256"], "receipt_audit_observer_gamestate_match": True})
    imports = json.loads((OUT / "candidate-phase-b-imports.json").read_bytes())
    for item in imports["copies"]:
        assert fp(Path(item["original"]))[1] == fp(Path(item["alias"]))[1] == item["sha256"]
    cutoff = datetime.fromisoformat(selection["unprefixed_press_cutoff_utc"])
    for p in (OUT / "run").glob("press-*.json"):
        assert datetime.fromisoformat(json.loads(p.read_bytes())["at_utc"]) <= cutoff
    image_bindings = 0
    for path in (OUT / "run").glob("*.ocr.json"):
        ocr = json.loads(path.read_bytes())
        if "image" in ocr and "image_sha256" in ocr:
            image = OUT / "run" / Path(ocr["image"]).name
            assert fp(image)[1] == ocr["image_sha256"]
            assert ocr["pid"] == 36912
            image_bindings += 1
    failure = json.loads((OUT / "run/phaseb-startup-failure-2.json").read_bytes())
    assert failure["status"] == "NOT_READY"
    assert fp(OUT / "runtime-input/user_empire_designs_v3.4.txt")[1] == "4ce9d9217a7ed804776a41e8ac73410bd70d5073bc3379aa55c2c46181938646"
    reports = []
    for p in sorted((OUT / "analysis").glob("*.json")):
        data = json.loads(p.read_bytes())
        if data.get("status"):
            checks = data.get("checks", {})
            reports.append({"name": p.name, "status": data["status"], "scope": data.get("scope"),
                            "failed_checks": [k for k, v in checks.items() if v is False] if isinstance(checks, dict) else [],
                            "sha256": fp(p)[1]})
    for name in ("rc4-public031-fraction-migration-complete-check-v1.json", "rc4-paid-fraction-migration-complete-check-v1.json",
                 "rc4-design-registration-probe-report-v1.json", "rc4-design-name-binding-probe-report-v1.json",
                 "rc4-design-name-binding-probe-report-v2.json", "rc4-fleet-scope-design-probe-report-v1.json"):
        assert json.loads((OUT / "analysis" / name).read_bytes())["status"] == "FAIL", name
    report = {"schema": "eep.rc4.phase-b.raw-checkpoint-verification.v1", "status": "PASS_BYTE_SOURCE_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": sha256(index_bytes).hexdigest(),
              "payload_files_rechecked": len(index["files"]), "payload_bytes": index["payload_bytes"],
              "canonical_refs_rechecked": len(index["canonical_references_not_copied"]), "canonical_mod_files_rechecked_not_copied": 59,
              "native_saves": save_rows, "import_aliases_verified": len(imports["copies"]), "gpu_image_ocr_bindings": image_bindings,
              "startup_NOT_READY_failure_preserved": failure, "reports_preserved": reports,
              "report_status_counts": dict(Counter(x["status"] for x in reports)),
              "rsizeonly_included": False, "live_logs_read_or_copied": False, "final_run_freeze": False,
              "migration_acceptance": "FAILURES_PRESERVED_NOT_COMPLETE"}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("native_saves", "reports_preserved")}, indent=2))


if __name__ == "__main__":
    main()
