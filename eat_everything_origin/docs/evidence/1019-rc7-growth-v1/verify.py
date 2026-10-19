"""Independent bytes and execution bindings; never operate the running game."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
REPO = ROOT.parent


def digest(path): return sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
def ref(path): return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}
def check_ref(entry):
    path = ROOT / entry["path"]
    assert path.is_relative_to(ROOT) and digest(path) == entry["sha256"]
def normalized(value):
    path = Path(value)
    if not path.is_absolute():
        path = (REPO if str(value).replace("\\", "/").startswith("eat_everything_origin/") else ROOT) / path
    return str(path.resolve()).casefold()


def main():
    assert not (OUT / "verify.json").exists(), "Never overwrite a sealed verification"
    index = read(OUT / "index.json")
    checks, drift = {}, []
    for entry in index["files"]:
        source, copied = Path(entry["source"]), OUT / entry["path"]
        assert copied.is_relative_to(OUT) and digest(copied) == entry["sha256"] and copied.stat().st_size == entry["bytes"]
        if source.read_bytes() != copied.read_bytes():
            assert entry["source_class"] in ("disk_source_no_historical_memory_attestation", "working_execution_plan_snapshot")
            drift.append({"source": str(source), "path": entry["path"], "captured_sha256": entry["sha256"], "source_now_sha256": digest(source),
                "scope": "Source advanced after exact capture comparison; first copied bytes preserved"})
    assert len(index["files"]) == 542 and sum(e["bytes"] for e in index["files"]) == index["payload_bytes"]
    checks["542_payload_SHA_exact_current_source_matches_or_explicit_drift"] = True
    for entry in index["canonical_references"]: check_ref(entry)
    assert len(index["canonical_references"]) == 73
    checks["73_canonical_refs_including_59_Mod_originals_not_recopied"] = True
    savs = list((OUT / "run").glob("*.sav"))
    assert len(savs) == 23
    for path in savs:
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None and set(archive.namelist()) == {"gamestate", "meta"}
    checks["23_native_ZIPs_CRC_valid"] = True
    manifest = read(OUT / "run/manifest.json")
    assert manifest["run_id"] == "20261019T164112Z" and manifest["copied_mod_tree_sha256"] == index["production_tree_sha256"]
    seed = manifest["seeded_save"]
    legacy = ROOT / "docs/evidence/1019-rc6-economy/machine/r6mcyearui.sav"
    assert digest(legacy) == seed["sha256"]
    c0load = read(OUT / "run/r7gloadc0b.load.json")
    assert c0load["source_sha256"] == seed["sha256"] and Path(c0load["source"]).name == "r6mcyearui.sav"
    assert c0load["ui_date_verified"] is True and c0load["state_verified"] is False
    checks["actual_imported_C0_manifest_and_load_roles_not_startup_year"] = True
    receipt = read(OUT / "run/r7mx-growth-receipt.json")
    assert len(receipt["snapshots"]) == 18 and len(receipt["commands"]) == 36
    assert Path(receipt["plan"]["anchor_receipt"]).name == "r7ganchor.native-save.json"
    for sample in receipt["snapshots"]:
        prefix = Path(sample["archived"]).stem
        save = OUT / "run" / (prefix + ".sav")
        obs = read(OUT / "run" / (prefix + ".growth-observation.json"))
        assert digest(save) == sample["sha256"] == obs["save_sha256"] and sample["date"] == obs["date"]
        assert (OUT / "run" / (prefix + ".audit.json")).is_file()
        assert digest(OUT / "run" / Path(sample["hud"]["image"]).name) == sample["hud"]["image_sha256"]
    checks["18_matrix_sample_roles_receipts_audits_observations_HUD"] = True
    for command in receipt["commands"]:
        action = command["input_action"]
        assert read(OUT / "run" / (action["stage"] + ".action.json")) == action
        assert action["submitted"] is True and action["text"] == command["command"]
        enter = read(OUT / "run" / (action["stage"] + "-enter.action.json"))
        assert enter["scan_code"] == 28 and enter["repeat"] == 1 and action["typed_at_utc"] < enter["at_utc"]
        assert digest(OUT / "run" / Path(command["console_frame"]).name) == command["console_frame_sha256"]
    assert sum(c["command"] == "fast_forward 30" for c in receipt["commands"]) == 18
    checks["36_matrix_commands_physical_Enter_18_FF30"] = True
    for prefix, role in index["native_roles"].items():
        for key in ("save", "audit", "exact_native_save_receipt"): check_ref(role[key])
        native = read(ROOT / role["exact_native_save_receipt"]["path"])
        assert Path(native["archived"]).name == prefix + ".sav" and native["sha256"] == role["save"]["sha256"]
    load = read(OUT / "run/r7gload.load.json")
    assert Path(load["source"]).name == "r7grepeat.sav" and load["source_sha256"] == index["native_roles"]["r7grepeat"]["save"]["sha256"]
    assert load["ui_date_verified"] is True and load["state_verified"] is False
    checks["five_exact_native_save_roles_and_two_load_receipts"] = True
    for name, expected in (("r7grepeat-effect-command", "effect root={eep_sync_mothership=yes eep_sync_mothership=yes}"),
        ("r7gbudget-effect-command", "effect root={set_variable={which=eep_c value=20500} eep_sync_mothership=yes}"),
        ("r7gbudget-monthly-command", "fast_forward 30")):
        action, enter = read(OUT / "run" / (name + ".action.json")), read(OUT / "run" / (name + "-enter.action.json"))
        assert action["text"] == expected and action["submitted"] is True and enter["scan_code"] == 28
        assert action["typed_at_utc"] < enter["at_utc"]
    checks["repeat_single_budget_then_monthly_commands_and_Enter"] = True
    assert len(index["image_ocr_bindings"]) == 84
    for pair in index["image_ocr_bindings"]:
        check_ref(pair["image"]); check_ref(pair["ocr"])
        ocr = read(ROOT / pair["ocr"]["path"])
        assert ocr["image_sha256"] == pair["image"]["sha256"] and ocr["capture"] == "fresh Steam F12 GPU backbuffer"
    checks["84_original_GPU_OCR_image_bindings"] = True
    report = read(ROOT / index["formal_report"]["path"])
    assert digest(ROOT / index["formal_report"]["path"]) == "4677e82c62ce30851f247691dad38703f52d6187ce26f2e63ea9fe0d7df9d1a3"
    assert report["status"] == "PASS_SCOPED" and report["startup_stability"]["status"] == "NOT_PROVIDED"
    assert sum(len(report[key]["checks"]) for key in index["formal_report_check_counts"]) == 1850
    assert all(c["passed"] is True for key in index["formal_report_check_counts"] for c in report[key]["checks"])
    assert report["repeat"]["strict_gamestate_equal"] is True and report["reload"]["strict_gamestate_equal"] is False
    assert (OUT / "run/r7grepeat.sav").read_bytes() == (OUT / "run/r7mx-n08-c10000-final.sav").read_bytes()
    assert (OUT / "run/r7grepeat.sav").read_bytes() != (OUT / "run/r7greload.sav").read_bytes()
    budget_rows = report["budget"]["checks"]
    assert [r["actual"] for r in budget_rows if r["check"] == "eep_component_rewards"] == [400, 410]
    assert [r["actual"] for r in budget_rows if r["check"] == "eep_component_pending"] == [10, 0]
    checks["formal_1850_checks_scoped_repeat_reload_and_budget_actuals"] = True
    summary = read(OUT / "authored/rc7-growth-matrix-independent-summary-v1.json")
    assert summary["check_count"] == 1558 and summary["failure_count"] == 0
    for row in summary["pair_reports"]:
        original = OUT / "authored" / Path(row["path"]).name
        assert digest(original) == row["sha256"] and read(original)["failure_count"] == 0
    checks["nine_pair_and_method_summary_originals_unchanged_1558_observations"] = True

    lookup = {normalized(e["source"]): ref(OUT / e["path"]) for e in index["files"]}
    lookup.update({normalized(ROOT / e["path"]): e for e in index["canonical_references"]})
    lookup[normalized(seed["source"])] = ref(legacy)
    lookup[normalized(seed["copied"])] = ref(legacy)
    original_refs = {}
    def walk(value):
        if isinstance(value, list):
            for item in value: walk(item)
        elif isinstance(value, dict):
            hash_value = value.get("sha256", value.get("save_sha256"))
            if isinstance(value.get("path"), str) and isinstance(hash_value, str) and re.fullmatch(r"[0-9a-f]{64}", hash_value):
                original_refs[(value["path"], hash_value)] = value
            for item in value.values(): walk(item)
    for entry in index["files"]:
        if entry["path"].startswith("authored/") and entry["path"].endswith(".json"): walk(read(OUT / entry["path"]))
    bindings, unresolved = [], []
    for (path, expected), _ in sorted(original_refs.items()):
        mapped = lookup.get(normalized(path))
        if mapped is None or mapped["sha256"] != expected:
            unresolved.append({"original_path": path, "sha256": expected})
        else:
            check_ref(mapped)
            bindings.append({"original_path": path, "sha256": expected, "project_reference": mapped})
    reference_map = {"schema": "eep.rc7.growth-original-reference-map.v1", "status": "ORIGINAL_JSON_BYTES_UNCHANGED_PATHS_MAPPED",
        "index": ref(OUT / "index.json"), "bindings": bindings, "unresolved": unresolved,
        "scope": "All structured path+SHA/save_SHA records in archived author JSON; original absolute strings preserved, no SHA-only SAV role discovery"}
    assert not unresolved, json.dumps(unresolved)
    write(OUT / "original-reference-map-v1.json", reference_map)
    checks["all_structured_original_author_path_SHA_records_bound_to_projects"] = True
    assert not any(e["path"].endswith(".log") or "r7ev" in e["path"] for e in index["files"])
    assert index["final_result_written"] is False
    checks["no_active_branch_logs_final_result_or_startup_claim"] = True
    result = {"schema": "eep.rc7.growth-independent-byte-verification.v1", "status": "PASS_BYTES_BINDINGS_SCOPED_REPORT_NOT_MOD_ACCEPTANCE",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": digest(OUT / "index.json"),
        "payload_files_rechecked": 542, "payload_bytes": index["payload_bytes"], "canonical_refs_rechecked": 73,
        "original_reference_map": ref(OUT / "original-reference-map-v1.json"), "original_path_SHA_records_bound": len(bindings),
        "source_drift_after_first_copy": drift, "current_sources_equal_at_verification": 542 - len(drift),
        "source_time_limit": "Disk bytes; no proof of historical loaded process memory; active process logs are excluded",
        "checks": checks, "startup_stability": "NOT_PROVIDED_IMPORTED_C0", "final_result_written": False, "Mod_acceptance": "PENDING"}
    write(OUT / "verify.json", result)
    print(json.dumps({"status": result["status"], "checks": len(checks), "original_refs": len(bindings), "source_drift": len(drift), "verify_sha256": digest(OUT / "verify.json")}))


if __name__ == "__main__": main()
