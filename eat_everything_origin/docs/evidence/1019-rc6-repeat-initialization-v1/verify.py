"""Independent bytes/roles/input binding verification; no game operations."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]


def digest(path): return sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding="utf-8"))


def main():
    index = read(OUT / "index.json")
    assert index["status"] == "PENDING_CASE_RAW_ARCHIVED"
    checks = {}
    for entry in index["files"]:
        src, dst = Path(entry["source"]), OUT / entry["path"]
        assert dst.is_relative_to(OUT) and dst.read_bytes() == src.read_bytes()
        assert dst.stat().st_size == entry["bytes"] and digest(dst) == entry["sha256"]
    assert len(index["files"]) == 44
    checks["44_payload_source_copy_bytes_SHA_exact"] = True
    for entry in index["canonical_references"]:
        path = ROOT / entry["path"]
        assert path.is_relative_to(ROOT) and digest(path) == entry["sha256"]
    assert len(index["canonical_references"]) == 25
    checks["25_canonical_refs_SHA_exact"] = True
    assert sum(row["bytes"] for row in index["files"]) == index["payload_bytes"]
    assert len([r for r in index["files"] if r["path"].endswith(".sav")]) == 1
    assert len([r for r in index["files"] if r["path"].startswith("authored/")]) == 6
    checks["only_after_SAV_copied_and_six_authored_files_preserved"] = True
    roles = index["native_roles"]
    for role, prefix in (("before", "r6mcyearui"), ("after", "r6mcinit2")):
        row = roles[role]
        assert Path(row["save"]["path"]).name == prefix + ".sav"
        assert Path(row["native_ui_save_receipt"]["path"]).name == prefix + ".native-save.json"
        for key in ("save", "audit", "native_ui_save_receipt"):
            assert digest(ROOT / row[key]["path"]) == row[key]["sha256"]
        receipt = read(ROOT / row["native_ui_save_receipt"]["path"])
        assert Path(receipt["archived"]).name == prefix + ".sav"
        assert receipt["sha256"] == row["save"]["sha256"] and receipt["date"] == row["date"]
    assert roles["before"]["native_ui_save_receipt"]["path"] != roles["after"]["native_ui_save_receipt"]["path"]
    checks["exact_before_after_receipt_role_binding_no_SHA_discovery"] = True
    before = ROOT / roles["before"]["save"]["path"]
    after = ROOT / roles["after"]["save"]["path"]
    assert before.read_bytes() == after.read_bytes()
    with zipfile.ZipFile(before) as a, zipfile.ZipFile(after) as b:
        assert a.namelist() == b.namelist() == ["gamestate", "meta"]
        for name in a.namelist():
            assert a.read(name) == b.read(name)
            metadata = ("CRC", "compress_type", "file_size", "compress_size", "date_time", "flag_bits", "extra", "comment", "external_attr", "internal_attr", "create_system", "create_version", "extract_version", "header_offset")
            assert all(getattr(a.getinfo(name), field) == getattr(b.getinfo(name), field) for field in metadata)
    checks["native_ZIP_and_each_member_bytes_equal"] = True
    command = read(OUT / "run/r6mcinit2-effect-command.action.json")
    assert command["text"] == "effect root={eep_initialize=yes eep_startup=yes eep_sync_mothership=yes eep_initialize=yes eep_startup=yes eep_sync_mothership=yes}"
    assert command["submitted"] is True
    enter = read(OUT / "run/r6mcinit2-effect-command-enter.action.json")
    assert enter["scan_code"] == 28 and enter["repeat"] == 1
    assert command["typed_at_utc"] < enter["at_utc"]
    checks["two_full_rounds_actual_command_and_physical_Enter"] = True
    report = read(ROOT / index["author_report"]["path"])
    assert len(report["checks"]) == 41 and all(v is True for v in report["checks"].values())
    assert report["strict_comparison"]["differences"] == []
    for key, name in (("command", "r6mcinit2-effect-command.action.json"), ("physical_enter", "r6mcinit2-effect-command-enter.action.json")):
        assert digest(OUT / "run" / name) == report["command_evidence"][key]["sha256"]
    checks["author_41_of_41_and_strict_zero_bound_to_real_command"] = True
    assert len(index["image_ocr_bindings"]) == 8
    for row in index["image_ocr_bindings"]:
        ocr = read(ROOT / row["ocr"]["path"])
        assert digest(ROOT / row["ocr"]["path"]) == row["ocr"]["sha256"]
        assert digest(ROOT / row["image"]["path"]) == ocr["image_sha256"] == row["image"]["sha256"]
        assert ocr["capture"] == "fresh Steam F12 GPU backbuffer"
    response = read(OUT / "run/r6mcinit2-effect-before.ocr.json")
    hud = read(OUT / "run/r6mcinit2-effect-after.ocr.json")
    assert enter["at_utc"] < response["captured_at_utc"] < hud["captured_at_utc"]
    assert response["pid"] == hud["pid"] == 30812
    assert any("Executing effect script." in row["text"] for row in response["rows"])
    checks["eight_GPU_OCR_pairs_and_post_Enter_execution_response"] = True
    proposal = read(ROOT / "docs/evidence/1019-requirements/rc6-repeat-initialization-case-proposal-v2.json")
    assert proposal["status"] == proposal["case_payload"]["status"] == "PENDING"
    assert len(proposal["case_payload"]["checks"]) == 4 and all(v is True for v in proposal["case_payload"]["checks"].values())
    for row in proposal["case_payload"]["evidence"]:
        assert digest(ROOT / row["path"]) == row["sha256"]
    patch = read(ROOT / "docs/evidence/1019-requirements/rc6-runtime-progress-v1-repeat-initialization-patch-proposal.json")
    assert patch["status"] == "PENDING_NOT_APPLIED" and patch["base_index_written"] is False
    assert patch["proposed_case"]["status"] == "PENDING"
    assert patch["missing_after_proposed_merge"]["missing_evidence_kinds"] == ["log"]
    assert patch["missing_after_proposed_merge"]["missing_or_failed_checks"] == []
    assert digest(ROOT / patch["base_index"]["path"]) == patch["base_index"]["sha256"]
    checks["new_proposal_PENDING_existing_progress_unchanged_only_final_log_missing"] = True
    assert index["initial_driver_failure"]["before_any_physical_input"] is True
    assert index["initial_driver_failure"]["raw_exception_file_available"] is False
    assert not any("r6g" in row["path"] or row["path"].endswith(".log") for row in index["files"])
    checks["preinput_driver_failure_documented_no_fabricated_raw_no_growth_logs"] = True
    result = {"schema": "eep.rc6.repeat-init-archive-byte-verification.v1",
        "status": "PASS_BYTES_ROLES_AND_INPUT_BINDING_CASE_STILL_PENDING", "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "index_sha256": digest(OUT / "index.json"), "payload_files_rechecked": 44,
        "payload_bytes": index["payload_bytes"], "canonical_refs_rechecked": 25,
        "checks": checks, "case_status": "PENDING", "final_result_written": False,
        "active_logs_growth_UI_Git_accessed": False}
    with (OUT / "verify.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "verify_sha256": digest(OUT / "verify.json")}))


if __name__ == "__main__": main()
