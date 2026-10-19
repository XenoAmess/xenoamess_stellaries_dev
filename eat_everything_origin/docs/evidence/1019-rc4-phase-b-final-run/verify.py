"""Independent final log/probe raw-source, SAV, image and Git-byte verification."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import zipfile

OUT = Path(__file__).resolve().parent


def fp(path):
    data = path.read_bytes()
    return len(data), sha256(data).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    assert index["files"] == selection["files"]
    assert fp(OUT / "selection.json")[1] == index["selection_sha256"]
    assert len(index["files"]) == index["payload_file_count"]
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"]), row["path"]
    for row in index["canonical_references_not_copied"]:
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"]), row["path"]
    source_logs = Path(selection["fixed_userdir"]) / "logs"
    source_names = sorted(p.relative_to(source_logs).as_posix() for p in source_logs.rglob("*") if p.is_file())
    copy_names = sorted(p.relative_to(OUT / "logs").as_posix() for p in (OUT / "logs").rglob("*") if p.is_file())
    assert source_names == copy_names and len(copy_names) == index["log_file_count"] == 19
    assert len(index["script_documentation_files"]) == 5
    stop = json.loads((OUT / "stop.json").read_bytes())
    process = json.loads((OUT / "process.json").read_bytes())
    manifest = json.loads((OUT / "manifest.json").read_bytes())
    independent = json.loads((OUT / "process-independent.json").read_text(encoding="utf-8-sig"))
    assert stop["pid"] == process["pid"] == index["pid"] == 36912
    assert stop["forced"] is False and stop["running_after"] is False and independent["status"] == "ABSENT"
    assert fp(OUT / "process-independent.json")[1] == index["process_independent_sha256"]
    assert manifest["run_id"] == index["run_id"] == "20261019T133314Z"
    assert manifest["copied_mod_tree_sha256"] == index["source_mod_tree_sha256"]
    saves = list((OUT / "run").glob("*.sav"))
    assert len(saves) == 1 and saves[0].name == "rsizeonly.sav"
    save = saves[0]
    receipt = json.loads(save.with_suffix(".native-save.json").read_bytes())
    audit = json.loads(save.with_suffix(".audit.json").read_bytes())
    observer = json.loads((OUT / "analysis/rc4-rsizeonly-observation-v1.json").read_bytes())
    assert fp(save)[1] == receipt["sha256"] == audit["save_sha256"] == observer["save_sha256"]
    with zipfile.ZipFile(save) as packed:
        gamestate = packed.read("gamestate")
    assert sha256(gamestate).hexdigest() == audit["gamestate_sha256"] == observer["gamestate_sha256"]
    assert observer["manifest_sha256"] == fp(OUT / "manifest.json")[1]
    assert observer["production_tree_sha256"] == index["source_mod_tree_sha256"]
    assert observer["date"] == receipt["date"] == "2200.01.12"
    images = []
    for path in sorted((OUT / "run").glob("*.ocr.json")):
        ocr = json.loads(path.read_bytes())
        image = OUT / "run" / Path(ocr["image"]).name
        assert fp(image)[1] == ocr["image_sha256"] and ocr["pid"] == 36912
        images.append({"stage": ocr["stage"], "captured_at_utc": ocr["captured_at_utc"], "image_sha256": ocr["image_sha256"], "ocr_sha256": fp(path)[1]})
    imported = json.loads((OUT / "run/nrel-source-import-receipt.json").read_bytes())
    assert imported["status"] == "RAW_BYTE_IDENTICAL_IMPORT_ONLY"
    assert fp(Path(imported["source"]["save"]))[1] == fp(Path(imported["alias"]))[1] == imported["alias_sha256"] == imported["source"]["save_sha256"]
    assert not any((OUT / "run").glob("nrel*.sav"))
    assert not (OUT / "run/nrel-source-load.load.json").exists()
    size = json.loads((OUT / "analysis/rc4-mobile-starbase-size-probe-report-v1.json").read_bytes())
    assert size["status"] == "FAIL" and any(value is False for value in size["checks"].values())
    paths = [(OUT / row["path"]).resolve().as_posix() for row in index["files"]]
    common = {"input": "\n".join(paths) + "\n", "text": True, "encoding": "utf-8", "capture_output": True, "check": True}
    a = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], **common).stdout.splitlines()
    b = subprocess.run(["git", "hash-object", "--stdin-paths"], **common).stdout.splitlines()
    c = subprocess.run(["git", "check-attr", "text", "--stdin"], **common).stdout.splitlines()
    assert len(a) == len(b) == len(c) == len(paths) and a == b and all(row.endswith(": text: unset") for row in c)
    report = {"schema": "eep.rc4.phase-b.final-run-verification.v1", "status": "PASS_BYTE_SOURCE_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "payload_files_rechecked": len(paths), "payload_bytes": index["payload_bytes"],
              "canonical_refs_rechecked": len(index["canonical_references_not_copied"]), "all_final_logs_rechecked": 19,
              "script_documentation_files_rechecked": 5, "source_process_stopped_before_copy": True,
              "native_sav_count": 1, "native_sav_sha256": fp(save)[1], "native_date": receipt["date"],
              "SAV_receipt_audit_observer_manifest_gamestate_all_bound": True, "image_ocr_bindings": images,
              "git_byte_preservation_files": len(paths), "rsizeonly_result": "FAIL_PRESERVED",
              "nrel_result": "SOURCE_IMPORT_ONLY; HUD_DATE_GUARD_FAILED; no injury/save/export; no play0 typed",
              "Mod_acceptance_pass": False, "old_archives_or_manifests_rewritten": False}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "image_ocr_bindings"}, indent=2))


if __name__ == "__main__":
    main()
