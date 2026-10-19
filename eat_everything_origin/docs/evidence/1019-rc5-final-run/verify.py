"""Independently verify RC5 raw bytes and report bindings without UI or Git."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
STAGES = ("r5pautoload", "r5preload1", "r5coreguard1", "r5coreguard2", "nchealthbefore", "nchealthset", "nchealthload")


def fp(path):
    data = path.read_bytes()
    return len(data), sha256(data).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    assert index["files"] == selection["files"]
    assert fp(OUT / "selection.json")[1] == index["selection_sha256"]
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"]), row["path"]
    for row in index["canonical_references_not_copied"]:
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"]), row["path"]
    for category, source in (("run", Path(selection["fixed_artifact_path"])), ("logs", Path(selection["fixed_userdir"]) / "logs")):
        a = sorted(p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file())
        b = sorted(p.relative_to(OUT / category).as_posix() for p in (OUT / category).rglob("*") if p.is_file())
        assert a == b, category
    assert len(list((OUT / "logs").rglob("*.log"))) == index["log_file_count"] == 19
    assert len(list((OUT / "logs/script_documentation").glob("*.log"))) == 5
    stop = json.loads((OUT / "run/stop.json").read_bytes())
    process = json.loads((OUT / "run/process.json").read_bytes())
    manifest = json.loads((OUT / "run/manifest.json").read_bytes())
    proof = json.loads((OUT / "process-independent.json").read_text(encoding="utf-8-sig"))
    assert stop["pid"] == process["pid"] == index["pid"] == proof["expected_pid"] == 33260
    assert not stop["forced"] and not stop["running_after"] and proof["status"] == "ABSENT"
    assert fp(OUT / "process-independent.json")[1] == index["process_independent_sha256"]
    assert manifest["run_id"] == index["run_id"] == "20261019T143452Z"
    binding = json.loads((OUT / "source-binding.json").read_bytes())
    assert fp(OUT / "source-binding.json")[1] == index["source_binding_sha256"]
    assert not binding["prepare_execution_source_snapshot_existed"] and not binding["memory_loaded_source_proof"]
    canonical_mod = Path(binding["canonical_mod_directory"])
    copied_mod = Path(manifest["copied_mod"])
    digest = sha256()
    for entry in manifest["repository_mod_files"]:
        a, b = canonical_mod / entry["path"], copied_mod / entry["path"]
        assert fp(a) == fp(b) == (entry["bytes"], entry["sha256"])
        digest.update(entry["path"].encode("utf-8")); digest.update(b"\0"); digest.update(b.read_bytes())
    assert digest.hexdigest() == index["source_tree_sha256"] == manifest["copied_mod_tree_sha256"]
    gate = json.loads((OUT / "source_snapshot/candidate-rc5-gate.json").read_bytes())
    assert gate["status"] == "PASS" and gate["version"] == index["version"] == "0.4.0-rc.5"
    assert gate["source_tree_sha256"] == index["source_tree_sha256"] and gate["files"] == manifest["repository_mod_files"]
    for tool in binding["tools"]:
        assert fp(OUT / tool["archived_path"]) == fp(Path(tool["matching_earlier_canonical"])) == (tool["bytes"], tool["sha256"])
    checker = fp(OUT / "tools-hash-binding/eat_everything_origin/tools/check_1019.py")[1]
    inspector = fp(OUT / "tools-hash-binding/eat_everything_origin/testing/inspect_1019.py")[1]
    saves = []
    decoded = {}
    assert {p.stem for p in (OUT / "run").glob("*.sav")} == set(STAGES)
    for stage in STAGES:
        path = OUT / "run" / (stage + ".sav")
        receipt = json.loads(path.with_suffix(".native-save.json").read_bytes())
        audit = json.loads(path.with_suffix(".audit.json").read_bytes())
        observed = json.loads((OUT / "analysis" / ("rc5-" + stage + "-observation-v1.json")).read_bytes())
        assert fp(path)[1] == receipt["sha256"] == audit["save_sha256"] == observed["save_sha256"]
        assert observed["manifest_sha256"] == fp(OUT / "run/manifest.json")[1]
        assert observed["production_tree_sha256"] == index["source_tree_sha256"]
        assert observed["checker_sha256"] == checker and observed["inspector_sha256"] == inspector
        with zipfile.ZipFile(path) as pack:
            raw = pack.read("gamestate")
        decoded[stage] = raw.decode("utf-8-sig")
        assert sha256(raw).hexdigest() == audit["gamestate_sha256"] == observed["gamestate_sha256"]
        saves.append({"stage": stage, "date": receipt["date"], "sha256": receipt["sha256"], "gamestate_sha256": observed["gamestate_sha256"], "six_way_binding": True})
    assert fp(OUT / "run/r5coreguard1.sav") == fp(OUT / "run/r5coreguard2.sav")
    images = []
    for path in sorted((OUT / "run").rglob("*.ocr.json")):
        ocr = json.loads(path.read_bytes())
        image = OUT / "run" / Path(ocr["image"]).name
        assert fp(image)[1] == ocr["image_sha256"] and ocr["pid"] == 33260
        images.append({"stage": ocr["stage"], "captured_at_utc": ocr["captured_at_utc"], "image_sha256": ocr["image_sha256"], "ocr_sha256": fp(path)[1]})
    assert not (OUT / "run/rc5-welcome-close-click.action.json").exists()
    assert (OUT / "run/rc5-welcome-close-utf8-click.action.json").exists()
    imports = json.loads((OUT / "run/candidate-rc5-imports.json").read_bytes())
    for entry in imports["imports"]:
        assert fp(Path(entry["source"]))[1] == fp(Path(entry["destination"]))[1] == entry["sha256"]
    migration = json.loads((OUT / "analysis/rc5-public031-autoload-reload-report-v1.json").read_bytes())
    guard = json.loads((OUT / "analysis/rc5-six-core-layout-guard-report-v1.json").read_bytes())
    health = json.loads((OUT / "analysis/native-current-ship-health-setter-calibration-report-v1.json").read_bytes())
    assert migration["status"] == "FAIL" and sum(value is False for value in migration["checks"].values()) == 9
    assert guard["status"] == "PASS_SCOPED" and len(guard["checks"]) == 26 and all(guard["checks"].values())
    assert health["status"] == "OBSERVATION_WITH_FAILURES" and sum(value is False for value in health["checks"].values()) == 4
    for label, stage in (("autoload", "r5pautoload"), ("reload", "r5preload1")):
        assert migration["stages"][label]["provenance"]["save_sha256"] == fp(OUT / "run" / (stage + ".sav"))[1]
    health_values = {}
    for stage, value in health["stages"].items():
        assert value["provenance"]["save_sha256"] == fp(OUT / "run" / (stage + ".sav"))[1]
        assert value["raw_ship"] in decoded[stage]
        assert fp(OUT / "analysis" / Path(value["observation_path"]).name)[1] == value["observation_sha256"]
        health_values[stage] = {layer: {k: v[k] for k in ("current", "maximum", "native_export_actual")} for layer, v in value["health"].items()}
    assert health["checks"]["reload_target_current_max_exactly_preserved"]
    assert all(health["checks"]["setter." + layer + "_original_1e_6"] is False for layer in ("hull", "armor", "shield"))
    assert health["checks"]["nchealthload.other_owned_ship_raw_exactly_unchanged"] is False
    report = {"schema": "eep.rc5.final-run-verification.v1", "status": "PASS_BYTE_SOURCE_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "payload_files_rechecked": len(index["files"]), "payload_bytes": index["payload_bytes"],
              "payload_category_counts": dict(Counter(row["path"].split("/")[0] for row in index["files"])),
              "canonical_refs_rechecked": len(index["canonical_references_not_copied"]), "actual_and_canonical_mod_files_rechecked": 59,
              "independently_recomputed_Mod_tree_sha256": digest.hexdigest(), "complete_logs": 19, "complete_script_documentation": 5,
              "source_process_stopped_before_copy": True, "native_saves": saves, "image_ocr_bindings": images,
              "offline_imports_verified": len(imports["imports"]), "stable_named_tool_hash_bindings": 9,
              "Welcome_first_refusal": "Root-reported corrupted requested label; actual first image/OCR retained, no first-click receipt; second UTF8 click retained",
              "migration_result": "FAIL_9_CHECKS_RETAINED", "coreguard_result": "PASS_SCOPED_26_OF_26_NO_RELOAD_CLAIM",
              "health_result": "OBSERVATION_WITH_FAILURES_4_CHECKS_RETAINED", "health_values": health_values,
              "health_setter_original_1e_6_all_three_FAIL": True, "health_reload_target_current_max_exact": True,
              "root_flags_are_not_design_local_marker_proof": True, "new_checker_v2_in_execution_source": False,
              "prepare_execution_source_snapshot_existed": False, "memory_loaded_source_proof": False,
              "Git_invoked": False, "UI_invoked": False, "Mod_acceptance_pass": False}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("native_saves", "image_ocr_bindings", "health_values")}, indent=2))


if __name__ == "__main__":
    main()
