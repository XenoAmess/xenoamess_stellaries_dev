"""Independently reread all stopped-run payload, save provenance and UI bindings."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import zipfile

OUT = Path(__file__).resolve().parent
SAVES = {
    "ld031clean": "7dcff806a7f6c20cd9a2a607c646f2d96ec2b31d07f88ebbaa5fc9086d6838fd",
    "ld031hurt": "f2d2742aa321b43ec153aa56fd210bce5f3c3828518e4fc63be3987d37f18ebd",
    "ldpaidclean": "5290bdd14f078a5b3b75902bb9231a94dce793ae8363e65066a5e235cd7f2360",
    "ldpaidhurt": "fa0bceedd33ef8957bf200d8ccd97cdde23cbf2e43f2984099f891ae22eb21a0",
    "ldpaidarmor": "4391254b50c1e1fabe975dbcaf9bf30caf0d17ece14bb8d8e9ff8b2c63c67373",
    "p031before": "d5921823d723d4eb0dec5d912ae0e586aac5b903643472d44062229b66b0b1e2",
    "ppaidbefore": "40c8f8dac9530594d501143132d55fef1205346d7f679f16c8858058ed392ff1",
}


def digest(path):
    data = path.read_bytes()
    return len(data), sha256(data).hexdigest()


def main():
    index_bytes = (OUT / "index.json").read_bytes()
    index = json.loads(index_bytes)
    source_root = Path(index["source_artifact_dir"])
    source_logs = Path(index["source_userdir"]) / "logs"
    expected = {x["path"]: x for x in index["files"]}
    for name, item in expected.items():
        assert digest(OUT / name) == (item["bytes"], item["sha256"]), name
        assert digest(Path(item["source"])) == (item["bytes"], item["sha256"]), item["source"]
    assert {x.removeprefix("logs/") for x in expected if x.startswith("logs/")} == {p.relative_to(source_logs).as_posix() for p in source_logs.rglob("*") if p.is_file()}
    assert {x.removeprefix("run/") for x in expected if x.startswith("run/")} | {"manifest.json", "process.json", "stop.json"} == {p.name for p in source_root.iterdir() if p.is_file()}
    assert {p.stem for p in (OUT / "run").glob("*.sav")} == set(SAVES)
    assert not (OUT / "run/ld031armor.sav").exists()
    for ref in index["canonical_refs_not_copied"]:
        assert digest(Path(ref["source"])) == (ref["bytes"], ref["sha256"])
    stop = json.loads((OUT / "stop.json").read_bytes())
    process = json.loads((OUT / "process.json").read_bytes())
    manifest = json.loads((OUT / "manifest.json").read_bytes())
    assert stop["pid"] == process["pid"] == 5216 and stop["forced"] is False and stop["running_after"] is False
    assert manifest["run_id"] == "20261019T130448Z"
    assert manifest["copied_mod_tree_sha256"] == "abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8"
    command = "$taskProcess = Get-Process -Id 5216 -ErrorAction SilentlyContinue; if ($null -ne $taskProcess) { exit 1 }; Write-Output 'ABSENT'; exit 0"
    probe = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", command], capture_output=True, text=True)
    assert probe.returncode == 0 and probe.stdout.strip() == "ABSENT" and not probe.stderr.strip()
    save_checks = []
    for name, expected_sha in SAVES.items():
        path = OUT / "run" / (name + ".sav")
        receipt = json.loads(path.with_suffix(".native-save.json").read_bytes())
        audit = json.loads(path.with_suffix(".audit.json").read_bytes())
        assert digest(path)[1] == receipt["sha256"] == audit["save_sha256"] == expected_sha
        with zipfile.ZipFile(path) as archive:
            native = archive.read("gamestate")
        assert sha256(native).hexdigest() == audit["gamestate_sha256"]
        save_checks.append({"stage": name, "sha256": expected_sha, "date": receipt["date"], "save_receipt_audit_gamestate_match": True})
    aliases = json.loads((OUT / "run/partial-source-aliases.json").read_bytes())
    for item in aliases["copies"]:
        assert digest(Path(item["original"]))[1] == digest(Path(item["alias"]))[1] == item["sha256"]
    bindings = 0
    failure_metadata = []
    for p in (OUT / "run").glob("*.ocr.json"):
        ocr = json.loads(p.read_bytes())
        if ocr.get("image") and ocr.get("image_sha256"):
            image = OUT / "run" / Path(ocr["image"]).name
            assert digest(image)[1] == ocr["image_sha256"], p.name
            assert ocr["pid"] == 5216, p.name
            bindings += 1
        else:
            failure_metadata.append({"file": p.name, "keys": list(ocr), "preserved_without_success_claim": True})
    fixture_before = (OUT / "eep05-fixture/fixture-before-gender-repair.txt").read_bytes()
    fixture_after = (OUT / "eep05-fixture/fixture-after-gender-repair.txt").read_bytes()
    repair = json.loads((OUT / "eep05-fixture/fixture-gender-repair-v1.json").read_bytes())
    assert sha256(fixture_before).hexdigest() == repair["before_sha256"] == "b3cee1d3c3475ea6fa9b54cc09eb0f75e848f565a02326bf70c59db0c9ed0e90"
    assert sha256(fixture_after).hexdigest() == repair["after_sha256"] == "4ce9d9217a7ed804776a41e8ac73410bd70d5073bc3379aa55c2c46181938646"
    transformed, count = re.subn(rb"(ruler=\s*\{\s*gender=)not_set", rb"\1female", fixture_before)
    assert count == 1 and transformed == fixture_after
    assert (OUT / "runtime-input/user_empire_designs_v3.4.txt").read_bytes() == fixture_before
    tooltip = OUT / "run/eep05-error-tooltip.ocr.json"
    assert digest(tooltip)[1] == repair["tooltip_sha256"]
    assert digest(OUT / "run/eep05-error-tooltip.jpg")[1] == repair["tooltip_image_sha256"]
    text = json.loads(tooltip.read_bytes())
    exact = "\u7edf\u6cbb\u8005\u6027\u522b\u672a\u9009\u5b9a\u3002"
    assert any(x["text"] == exact for x in text["rows"])
    assert not any(p.name in ("mod", "copied_mod", "public031") for p in OUT.iterdir())
    report = {"schema": "eep.legacy-damage.final-run-verification.v1", "status": "PASS_BYTE_PROVENANCE_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": sha256(index_bytes).hexdigest(),
              "payload_files_rechecked": len(expected), "source_files_rechecked": len(expected),
              "canonical_references_rechecked": len(index["canonical_refs_not_copied"]),
              "native_saves": save_checks, "aliases_verified_not_new_saves": len(aliases["copies"]),
              "ocr_image_gpu_bindings_verified": bindings, "ocr_records_without_image_binding": failure_metadata,
              "ocr_engine_success_does_not_imply_caller_label_lookup_success": True,
              "eep05_exact_missing_gender_tooltip_verified": True, "fixture_repair_single_field_only": True,
              "old_run_preset_unchanged_before_hash": True, "pid_probe": {"pid": 5216, "stdout": probe.stdout.strip(), "returncode": probe.returncode},
              "migration_acceptance": "PENDING_NOT_ASSIGNED", "repaired_fixture_native_validation": "PENDING_NOT_ASSIGNED"}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("native_saves", "ocr_records_without_image_binding")}, indent=2))


if __name__ == "__main__":
    main()
