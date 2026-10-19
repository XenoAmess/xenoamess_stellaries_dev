"""Verify only sealed Purifier UI/canonical sources; never open active logs/Hive."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import zipfile

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
ECON = OUT.parent / "1019-rc6-economy/purifier"
POWER = OUT.parent / "1019-rc6-power-source"


def fp(path):
    body = path.read_bytes()
    return len(body), sha256(body).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    author = json.loads((OUT / "author-selection.json").read_bytes())
    typed = json.loads((OUT / "typed-references.json").read_bytes())
    assert fp(OUT / "selection.json")[1] == index["selection_sha256"]
    assert fp(OUT / "author-selection.json")[1] == index["author_selection_sha256"]
    assert fp(OUT / "typed-references.json")[1] == index["typed_references_sha256"]
    assert selection["files"] == index["files"] and len(index["files"]) == index["payload_file_count"] == 85
    for row in index["files"]:
        assert row["path"].startswith("raw/r6pu-") and Path(row["path"]).suffix not in (".sav", ".log")
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"])
        assert "r6hvc" not in row["path"].lower()
    for row in index["canonical_references_not_copied"]:
        path = Path(row["path"])
        assert path.is_relative_to(REPO) and "r6hvc" not in str(path).lower()
        # The single .log is an already sealed generated static catalog in POWER.
        if path.suffix == ".log":
            assert path == POWER / "source/run/logs/script_documentation/modifiers.log"
        assert fp(path) == (row["bytes"], row["sha256"])
    for row in typed["references"]:
        path = REPO / row["path"]
        assert not Path(row["path"]).is_absolute() and path.resolve().is_relative_to(REPO)
        assert row["kind"] in ("native_save", "screenshot", "actions", "analysis")
        assert fp(path) == (row["bytes"], row["sha256"])
    images = []
    for path in sorted((OUT / "raw").glob("*.ocr.json")):
        ocr = json.loads(path.read_bytes())
        picture = OUT / "raw" / Path(ocr["image"]).name
        assert fp(picture)[1] == ocr["image_sha256"] and ocr["pid"] == 30812 and ocr["resolution"] == [1024, 768]
        assert datetime.fromisoformat(ocr["captured_at_utc"]) > datetime.fromisoformat(selection["post_m12_observed_at_utc"])
        images.append({"stage": ocr["stage"], "captured_at_utc": ocr["captured_at_utc"], "image_sha256": ocr["image_sha256"], "ocr_sha256": fp(path)[1]})
    images.sort(key=lambda row: row["captured_at_utc"])
    assert len(images) == 22
    save = ECON / "r6puyearui.sav"
    receipt = json.loads((ECON / "r6puyearui.native-save.json").read_bytes())
    audit = json.loads((ECON / "r6puyearui.audit.json").read_bytes())
    manifest = json.loads((ECON / "manifest.json").read_bytes())
    with zipfile.ZipFile(save) as packed: gamestate = packed.read("gamestate")
    assert fp(save)[1] == receipt["sha256"] == audit["save_sha256"] == index["yearUI_sha256"] == fp(ECON / "r6pum12.sav")[1]
    assert sha256(gamestate).hexdigest() == audit["gamestate_sha256"] and receipt["date"] == "2201.01.01"
    delivery = json.loads((POWER / "delivery-index-v1.json").read_bytes())
    assert len(delivery["files"]) == 31 and len(author["canonical_references"]) == 32
    for row in delivery["files"]:
        path = REPO / "eat_everything_origin" / row["path"]
        assert fp(path) == (row["bytes"], row["sha256"])
    power = json.loads((POWER / "power-inventory-report-v1.json").read_bytes())
    assert power["status"] == "SOURCE_DERIVED_NOT_UI_MEASURED"
    assert power["native_save"]["sha256"] == fp(save)[1] and power["native_receipt"]["sha256"] == fp(ECON / "r6puyearui.native-save.json")[1]
    assert power["gamestate_sha256"] == audit["gamestate_sha256"] and power["mod_tree_sha256"] == manifest["copied_mod_tree_sha256"]
    assert power["actual_identity"] == {"country": 0, "fleet": 150, "ship": 1077, "actual_design": 1918, "growth_stage": 0, "ship_size": "juggernaut", "slots": 50, "required": 6}
    assert len(power["inventory"]) == 56 and len(power["grouped_inventory"]) == 22
    assert sum(row["kind"] == "slot" for row in power["inventory"]) == 50
    assert sum(row["kind"] == "required" for row in power["inventory"]) == 6
    assert all(type(row["signed_power"]) in (int, float) for row in power["inventory"])
    produced = sum(row["signed_power"] for row in power["inventory"] if row["signed_power"] > 0)
    consumed = -sum(row["signed_power"] for row in power["inventory"] if row["signed_power"] < 0)
    assert (produced, consumed, produced - consumed) == (14300, 4557, 9743)
    assert power["arithmetic"]["unresolved_component_power_fields"] == [] and power["power_modifier_review"]["actual_power_declaration_count"] == 0
    assert len(power["sources"]) == 26
    for row in power["sources"].values():
        # Read the author's already sealed project copy, never its active-run origin.
        path = REPO / "eat_everything_origin" / row["archived"]
        assert path.is_relative_to(POWER) and fp(path) == (row["bytes"], row["sha256"])
    normalized_state = gamestate.decode("utf-8-sig").replace("\r\n", "\n")
    design = (POWER / "actual-design-1918.txt").read_text(encoding="utf-8-sig")
    assert design in normalized_state
    excerpts = json.loads((POWER / "actual-native-state-excerpts.txt").read_bytes())
    raw_count = 0
    for rows in excerpts.values():
        for row in rows:
            assert row["raw"] in normalized_state
            raw_count += 1
    country_variables = next(row["raw"] for row in excerpts["country0"] if row["key"] == "variables")
    assert re.search(r"\beep_c=0(?:\s|$)", country_variables)
    maintenance = power["maintenance_UI"]
    for key, local in (("image", "r6pu-ship-maintenance-hover.jpg"), ("ocr", "r6pu-ship-maintenance-hover.ocr.json"), ("hover_action", "r6pu-ship-maintenance-hover.action.json")):
        assert fp(OUT / "raw" / local)[1] == maintenance[key]["sha256"]
    early = json.loads((OUT / "raw/r6pu-actual-designer-result.ocr.json").read_bytes())
    post = json.loads((OUT / "raw/r6pu-verified-designer-result.ocr.json").read_bytes())
    tooltip = json.loads((OUT / "raw/r6pu-ship-maintenance-hover.ocr.json").read_bytes())
    notice = "\u5efa\u8bae\u521d\u59cb\u5316\u5b8c\u6bd5"
    assert any(notice in row["text"] for row in early["rows"])
    assert not any(notice in row["text"] for row in post["rows"])
    assert any("10.072.88" in row["text"] for row in tooltip["rows"]) and any(row["text"] == "115/66" for row in tooltip["rows"])
    click = json.loads((OUT / "raw/r6pu-verified-designer-click.action.json").read_bytes())
    assert click["client_point"] == [401, 602]
    observations = {"schema": "eep.rc6.purifier-mothership-ui-observations.v1", "status": "OBSERVATION_ONLY",
                    "run_id": index["run_id"], "date": "2201.01.01", "yearUI_sha256": index["yearUI_sha256"],
                    "actual_mother_identity_from_source_bound_SAV_report": power["actual_identity"],
                    "maintenance": {"method": "Independent visual inspection of original archived local image; original OCR preserved", "energy_displayed": "10.07", "alloys_displayed": "2.88", "naval_used": 115, "naval_capacity": 66, "raw_OCR_combined_number": "10.072.88", "scope": "Only this Purifier date/state, not universal base upkeep"},
                    "designer_attempts": {"early_actual_designer_result": "tutorial notice visibly overlays details; not diagnostic of editor behavior", "verified_posttutorial_hover_and_click_result": "unobscured ship-details window remains, no editor observed in captured result", "posttutorial_click_client_point": [401, 602], "scope": "Observed captured frames only; no hidden cause inferred"},
                    "power": {"status": power["status"], "produced": produced, "consumed": consumed, "source_derived_balance": produced - consumed, "inventory_rows": 56, "distinct_components": 22, "UI_power_measured": False},
                    "typed_references_sha256": index["typed_references_sha256"], "Mod_acceptance_pass": False}
    (OUT / "observations.json").write_text(json.dumps(observations, indent=2) + "\n", encoding="utf-8")
    result = {"schema": "eep.rc6.purifier-mothership-ui-verification.v1", "status": "PASS_BYTE_SOURCE_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "payload_files_rechecked": 85, "payload_bytes": index["payload_bytes"], "canonical_refs_rechecked": len(index["canonical_references_not_copied"]),
              "typed_project_relative_refs_rechecked": len(typed["references"]), "image_ocr_bindings": images,
              "yearUI_SAV_receipt_audit_gamestate_m12_bound": True, "power_delivery_files_plus_index_rechecked": 32,
              "sealed_source_copies_rechecked": 26, "state_excerpt_fragments_found_in_SAV": raw_count,
              "actual_design_excerpt_found_in_SAV_after_newline_normalization_only": True, "C0_raw_variable_verified": True,
              "power_arithmetic_independently_recomputed": {"produced": produced, "consumed": consumed, "balance": produced - consumed},
              "source_power_status": "SOURCE_DERIVED_NOT_UI_MEASURED", "observations_sha256": fp(OUT / "observations.json")[1],
              "active_run_logs_or_Hive_read": False, "catalog_read": "Only root-approved already sealed project generated-static-documentation copy; RC5 catalog not treated as same SHA",
              "UI_Git_Steam_operations": False, "final_run_freeze": False, "Mod_acceptance_pass": False}
    (OUT / "verify.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "image_ocr_bindings"}, indent=2))


if __name__ == "__main__":
    main()
