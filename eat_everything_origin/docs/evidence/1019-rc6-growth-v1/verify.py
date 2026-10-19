"""Verify fixed archived RC6 evidence; successful bytes do not accept growth."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]


def digest(path): return sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def check_ref(row):
    path = ROOT / row["path"]
    assert path.is_relative_to(ROOT) and digest(path) == row["sha256"]


def main():
    assert not (OUT / "verify.json").exists(), "Preserve sealed verification"
    index = read(OUT / "index.json")
    checks = {}
    source_advanced = []
    for row in index["files"]:
        original, copied = Path(row["source"]), OUT / row["path"]
        assert copied.is_relative_to(OUT)
        assert copied.stat().st_size == row["bytes"] and digest(copied) == row["sha256"]
        if copied.read_bytes() != original.read_bytes():
            assert row["path"] in ("authored/rc6-high-growth-export-budget-probe-1020.md", "source/check_growth_1019.py")
            source_advanced.append({"path": row["path"], "original": row["source"], "snapshot_sha256": row["sha256"],
                "source_now_sha256": digest(original), "classification": "working_source_advanced_after_earlier_exact_copy_assertion"})
    assert len(index["files"]) == 473 and sum(row["bytes"] for row in index["files"]) == index["payload_bytes"]
    assert len(source_advanced) == 2
    checks["473_frozen_payload_SHA_exact_471_current_source_bytes_exact_2_drift_recorded"] = True
    for row in index["canonical_references"]: check_ref(row)
    assert len(index["canonical_references"]) == 18
    checks["18_canonical_references_SHA_exact"] = True
    savs = list((OUT / "run").glob("*.sav"))
    assert len(savs) == 22
    for path in savs:
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None and set(archive.namelist()) == {"gamestate", "meta"}
    checks["22_original_native_ZIPs_CRC_valid"] = True
    receipt = read(OUT / "run/r6g-growth-receipt.json")
    assert len(receipt["snapshots"]) == 18 and len(receipt["commands"]) == 36
    for snapshot in receipt["snapshots"]:
        prefix = Path(snapshot["archived"]).stem
        assert digest(OUT / "run" / (prefix + ".sav")) == snapshot["sha256"]
        obs = read(OUT / "run" / (prefix + ".growth-observation.json"))
        assert obs["save_sha256"] == snapshot["sha256"] and obs["date"] == snapshot["date"]
        assert (OUT / "run" / (prefix + ".audit.json")).is_file()
        assert digest(OUT / "run" / Path(snapshot["hud"]["image"]).name) == snapshot["hud"]["image_sha256"]
    checks["all_18_matrix_samples_receipt_audit_observation_HUD_bound"] = True
    for command in receipt["commands"]:
        action = command["input_action"]
        action_file = OUT / "run" / (action["stage"] + ".action.json")
        assert read(action_file) == action and action["submitted"] is True and command["command"] == action["text"]
        enter = read(OUT / "run" / (action["stage"] + "-enter.action.json"))
        assert enter["scan_code"] == 28 and enter["repeat"] == 1 and action["typed_at_utc"] < enter["at_utc"]
        assert digest(OUT / "run" / Path(command["console_frame"]).name) == command["console_frame_sha256"]
    assert sum(c["command"] == "fast_forward 30" for c in receipt["commands"]) == 18
    checks["36_matrix_commands_with_physical_Enter_and_18_FF30"] = True
    assert len(index["image_ocr_bindings"]) == 72
    for binding in index["image_ocr_bindings"]:
        check_ref(binding["image"]); check_ref(binding["ocr"])
        ocr = read(ROOT / binding["ocr"]["path"])
        assert ocr["image_sha256"] == binding["image"]["sha256"]
        assert ocr["capture"] == "fresh Steam F12 GPU backbuffer"
    checks["72_GPU_OCR_original_image_bindings"] = True
    for prefix, row in index["post_matrix_roles"].items():
        for key in ("save", "audit", "exact_native_save_receipt"): check_ref(row[key])
        save_receipt = read(ROOT / row["exact_native_save_receipt"]["path"])
        assert Path(save_receipt["archived"]).name == prefix + ".sav"
        assert save_receipt["sha256"] == row["save"]["sha256"] and save_receipt["date"] == row["date"]
    load = read(OUT / "run/r6gload.load.json")
    assert Path(load["source"]).name == "r6grepeat.sav"
    assert load["source_sha256"] == index["post_matrix_roles"]["r6grepeat"]["save"]["sha256"]
    assert load["ui_date_verified"] is True and load["state_verified"] is False
    checks["four_precise_native_save_roles_and_actual_repeat_source_load_receipt"] = True
    for name in ("r6grepeat", "r6gexport1", "r6gbudget"):
        action = read(OUT / "run" / (name + "-effect-command.action.json"))
        enter = read(OUT / "run" / (name + "-effect-command-enter.action.json"))
        assert action["submitted"] is True and enter["scan_code"] == 28
        assert action["typed_at_utc"] < enter["at_utc"]
    budget_action = read(OUT / "run/r6gbudget-effect-command.action.json")
    assert budget_action["text"] == "effect root={set_variable={which=eep_c value=20500} eep_sync_mothership=yes}"
    checks["repeat_reexport_budget_real_command_Enter_records"] = True
    failures = []
    for row in index["original_pair_reports"]:
        check_ref(row["report"])
        report = read(ROOT / row["report"]["path"])
        assert report["status"] == "FAIL_OBSERVATION"
        assert report["failure_count"] == len(report["failed_checks"]) == row["failure_count"]
        failures.extend(report["failed_checks"])
        for source in report["sources"]:
            assert digest(OUT / "run" / Path(source["path"]).name) == source["sha256"]
    assert len(failures) == 24
    assert len(index["preserved_failure"]["n08_original_seven_exports"]) == 7
    checks["nine_original_FAIL_reports_and_all_24_failed_checks_unchanged"] = True
    post = read(OUT / "post-matrix-observation-v1.json")
    check_ref(post["archive_index"]); check_ref(post["parser"]); check_ref(post["extractor"])
    for state in post["raw"].values(): check_ref(state["save"])
    assert all(c["passed"] for c in post["later_reexport_10_channels"])
    budget = post["single_sync_budget"]
    assert budget["status"] == "FAIL" and (budget["actual_R"], budget["actual_pending"], budget["expected_R"], budget["expected_pending"]) == (300, 110, 400, 10)
    assert post["repeat_ZIP_equals_original_n08_final"] is True and post["repeat_reload_ZIP_equal"] is False
    checks["later_probe_observations_preserve_original_and_budget_FAILURES"] = True
    assert index["whole_growth_or_Mod_PASS"] is False and index["final_logs_not_in_this_package"] is True
    assert not any(row["path"].endswith(".log") for row in index["files"])
    checks["no_logs_RC7_UI_Git_or_acceptance_claim"] = True
    result = {"schema": "eep.rc6.growth-raw-independent-verification.v1", "status": "PASS_BYTES_INPUT_BINDING_KNOWN_RC6_FAILURES_RETAINED",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": digest(OUT / "index.json"),
        "post_matrix_observation_sha256": digest(OUT / "post-matrix-observation-v1.json"),
        "payload_files_rechecked": 473, "payload_bytes": index["payload_bytes"], "canonical_refs_rechecked": 18,
        "image_ocr_pairs": 72, "checks": checks, "original_failed_checks_retained": len(failures),
        "working_sources_advanced_after_capture": source_advanced,
        "first_verification_attempt": {"status": "FAILED_AT_CURRENT_SOURCE_COPY_COMPARISON", "error": "AssertionError at verify.py original line26",
            "scope": "Observed first offline verification call; no native game error; not a fabricated root pre-input exception file",
            "preserved_snapshot_expected_SHA_matches": True, "new_RC7_checker_not_copied": True},
        "growth_or_Mod_acceptance": "NOT_PASSED_RC6_SINGLE_SYNC_BUDGET_FAIL", "UI_Git_Production_changes": False}
    with (OUT / "verify.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "verify_sha256": digest(OUT / "verify.json")}))


if __name__ == "__main__": main()
