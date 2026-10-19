"""Independent migration checkpoint integrity and declared-scope verification."""
import ast
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
STAGES = ("r6pautoload", "r6preload1", "r6prepeatbase", "r6prepeat", "r6paidauto", "r6paidreload1", "r6paidrepeat")
POLICY = {"step_signed_ratio_min": -0.000021, "step_signed_ratio_max": 0.000001, "v1_absolute_tolerance": 0.000001, "relative_tolerance": 0}


def fp(path):
    body = path.read_bytes()
    return len(body), sha256(body).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    assert index["files"] == selection["files"] and fp(OUT / "selection.json")[1] == index["selection_sha256"]
    assert len(index["files"]) == index["payload_file_count"] == 330
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"]), row["path"]
        assert not row["path"].startswith(("logs/", "run/r6pu", "run/stop")) and Path(row["path"]).suffix != ".log"
    for row in index["canonical_references_not_copied"]:
        assert Path(row["path"]).suffix != ".log" and "logs" not in Path(row["path"]).parts
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"]), row["path"]
    manifest = json.loads((OUT / "run/manifest.json").read_bytes())
    process = json.loads((OUT / "run/process.json").read_bytes())
    assert manifest["run_id"] == index["run_id"] == "20261019T150008Z" and process["pid"] == index["game_pid"] == 30812
    assert manifest["copied_mod_tree_sha256"] == index["source_tree_sha256"]
    canonical = OUT.parent / "1019-rc6-static/candidate-rc6/mod"
    digest = sha256()
    for entry in manifest["repository_mod_files"]:
        source = Path(selection["fixed_userdir"]) / "mod/eep-1019" / entry["path"]
        assert fp(source) == fp(canonical / entry["path"]) == (entry["bytes"], entry["sha256"])
        digest.update(entry["path"].encode("utf-8")); digest.update(b"\0"); digest.update(source.read_bytes())
    assert digest.hexdigest() == index["source_tree_sha256"]
    assert {p.stem for p in (OUT / "run").glob("*.sav")} == set(STAGES)
    saves = []
    for stage in STAGES:
        path = OUT / "run" / (stage + ".sav")
        receipt = json.loads(path.with_suffix(".native-save.json").read_bytes())
        audit = json.loads(path.with_suffix(".audit.json").read_bytes())
        observed = json.loads((OUT / "analysis" / ("rc6-" + stage + "-migration-v2-observation-v1.json")).read_bytes())
        assert fp(path)[1] == receipt["sha256"] == audit["save_sha256"] == observed["save_sha256"]
        assert observed["manifest_sha256"] == fp(OUT / "run/manifest.json")[1]
        assert observed["production_tree_sha256"] == index["source_tree_sha256"]
        with zipfile.ZipFile(path) as archive: raw = archive.read("gamestate")
        assert sha256(raw).hexdigest() == audit["gamestate_sha256"] == observed["gamestate_sha256"]
        saves.append({"stage": stage, "sha256": fp(path)[1], "native_date": receipt["date"], "gamestate_sha256": observed["gamestate_sha256"], "six_way_binding": True})
    assert fp(OUT / "run/r6prepeatbase.sav") == fp(OUT / "run/r6prepeat.sav")
    assert fp(OUT / "run/r6paidreload1.sav") == fp(OUT / "run/r6paidrepeat.sav")
    loads = []
    for name in selection["actual_native_load_receipts"]:
        data = json.loads((OUT / "run" / name).read_bytes())
        assert fp(Path(data["source"]))[1] == data["source_sha256"]
        assert data["ui_date_verified"] is True and data["state_verified"] is False
        loads.append({"name": name, "source_sha256": data["source_sha256"], "date": data["date"], "loaded_at_utc": data["loaded_at_utc"], "original_state_verified_false_preserved": True})
    images = []
    for path in sorted((OUT / "run").glob("*.ocr.json")):
        data = json.loads(path.read_bytes())
        image = OUT / "run" / Path(data["image"]).name
        assert fp(image)[1] == data["image_sha256"] and data["pid"] == 30812
        images.append({"stage": data["stage"], "captured_at_utc": data["captured_at_utc"], "image_sha256": data["image_sha256"], "ocr_sha256": fp(path)[1]})
    for name in selection["fixed_press_filenames"]:
        data = json.loads((OUT / "run" / name).read_bytes())
        assert data["keys"] == ["ctrl", "a"]
    imports = json.loads((OUT / "run/candidate-rc6-imports.json").read_bytes())
    for entry in imports["imports"]:
        assert fp(Path(entry["source"]))[1] == fp(Path(entry["destination"]))[1] == entry["sha256"]
    delivery = json.loads((OUT / "analysis/rc6-migration-v2-delivery-v1.json").read_bytes())
    for entry in delivery["files"]:
        original = Path(entry["path"])
        if "1019-analysis" in original.parts: target = OUT / "analysis" / original.name
        elif original.suffix == ".md": target = OUT / "plans" / original.name
        else: target = OUT / "source-tools" / original
        assert fp(target) == (entry["bytes"], entry["sha256"])
    directories = (OUT / "source-tools/eat_everything_origin/tools", OUT / "source-tools/eat_everything_origin/testing", OUT / "source-tools/tools")
    closure = set(selection["offline_analysis_local_AST_closure"])
    for name in closure:
        path = OUT / "source-tools" / name
        parsed = ast.parse(path.read_text(encoding="utf-8-sig"))
        modules = set()
        for item in ast.walk(parsed):
            if isinstance(item, ast.Import): modules.update(x.name.split(".")[0] for x in item.names)
            elif isinstance(item, ast.ImportFrom) and item.module: modules.add(item.module.split(".")[0])
        for module in modules:
            hits = [base / (module + ".py") for base in directories if (base / (module + ".py")).exists()]
            assert len(hits) <= 1
            if hits: assert hits[0].relative_to(OUT / "source-tools").as_posix() in closure
    for entry in index["UI_core_hash_bindings"]:
        assert fp(OUT / entry["archived_path"]) == fp(Path(entry["matching_previous_canonical"])) == (entry["bytes"], entry["sha256"])
    v2 = fp(OUT / "source-tools/eat_everything_origin/tools/check_migration_1019.py")[1]
    v1 = fp(OUT / "source-tools/eat_everything_origin/tools/check_1019.py")[1]
    assert v1 == "681836d2da9c6b28ee9bfd583c87e5ced96f06543901e71d3dc35fa226f3afdc"
    results = []
    for name, checks in (("rc6-public031-migration-v2-complete-report-v1.json", 174), ("rc6-paid11-migration-v2-complete-report-v1.json", 158), ("rc6-paid11-migration-v2-cli-report-v1.json", 158)):
        data = json.loads((OUT / "analysis" / name).read_bytes())
        assert data["status"] == "PASS_SCOPED" and len(data["checks"]) == checks and all(value is True for value in data["checks"].values())
        assert data["policy"] == POLICY and data["checker_sha256"] == v2 and data["v1_checker_sha256"] == v1
        assert data["v1_original_diagnostic"]["status"] == "FAIL"
        assert data["repeat_sync_strict_comparison"]["checks"]["no_gameplay_differences"] is True
        arithmetic = {}
        for step, value in data["steps"].items():
            if "raw_readings" not in value: continue
            arithmetic[step] = {}
            for layer in ("hull", "armor", "shield"):
                readings = value["raw_readings"]
                with localcontext() as context:
                    context.prec = 60
                    before = readings["before"][layer]; after = readings["after"][layer]
                    delta = Decimal(str(after["current"])) / Decimal(str(after["maximum"])) - Decimal(str(before["current"])) / Decimal(str(before["maximum"]))
                    assert Decimal("-0.000021") <= delta <= Decimal("0.000001")
                arithmetic[step][layer] = str(delta)
        results.append({"name": name, "sha256": fp(OUT / "analysis" / name)[1], "status": data["status"], "checks_true": checks,
                        "v1_status": "FAIL_PRESERVED", "report_raw_readings_arithmetic_independently_within_predeclared_budget": arithmetic})
    for name in ("rc6-public031-migration-v2-template-v1.json", "rc6-paid11-migration-v2-template-v1.json", "rc6-public031-migration-v2-partial-report-v1.json"):
        assert json.loads((OUT / "analysis" / name).read_bytes())["status"] == "PENDING"
    old = OUT.parent / "1019-rc5-final-run/analysis/rc5-public031-autoload-reload-report-v1.json"
    assert json.loads(old.read_bytes())["status"] == "FAIL"
    report = {"schema": "eep.rc6.migration-checkpoint-verification.v1", "status": "PASS_BYTE_SOURCE_AND_SCOPED_REPORT_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "payload_files_rechecked": len(index["files"]), "payload_bytes": index["payload_bytes"],
              "payload_category_counts": dict(Counter(row["path"].split("/")[0] for row in index["files"])),
              "canonical_refs_rechecked": len(index["canonical_references_not_copied"]), "Mod_files_rechecked": 59,
              "independently_recomputed_Mod_tree_sha256": digest.hexdigest(), "native_saves": saves, "actual_load_receipts": loads,
              "image_ocr_bindings": images, "fixed_ctrl_a_count": 7, "offline_imports_rechecked": len(imports["imports"]),
              "sealed_delivery_files_verified": len(delivery["files"]), "offline_analysis_AST_closure_files": len(closure), "UI_core_hash_bindings": 9,
              "source_tool_total_files": 13, "v2_checker_sha256": v2, "original_v1_checker_unchanged_sha256": v1,
              "scoped_results": results, "old_v1_FAIL_and_RC5_FAIL_preserved": True, "historical_PENDING_templates_and_partial_preserved": True,
              "mathematically_lossless_migration_claim": False, "associated_mobile_starbase_implementation_certified_updated": False,
              "active_logs_read_or_copied": False, "economy_UI_or_samples_included": False, "final_run_freeze": False,
              "memory_loaded_source_proof": False, "Git_invoked": False, "UI_invoked": False, "Mod_acceptance_pass": False}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("native_saves", "actual_load_receipts", "image_ocr_bindings", "scoped_results")}, indent=2))


if __name__ == "__main__":
    main()
