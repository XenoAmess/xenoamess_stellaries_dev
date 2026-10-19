"""Append one native-category correction; preserve v1 FAIL and all original bytes."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rc6_economy_analysis_v2", HERE / "rc6-economy-analysis-v2.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def main():
    folder = analysis.PROJECT / "docs/evidence/1019-rc6-economy/purifier"
    original = folder / "native-branch-report.json"
    assert analysis.sha(original) == "ded9e3d1981be029663bd9fa1aae45d2ac460e5a699a97c18696a4a5869fa9b4"
    old = analysis.load(original)
    index = analysis.load(folder / "archive-index.json")
    assert all(analysis.sha(Path(row["source"])) == row["sha256"] == analysis.sha(folder / row["path"]) for row in index["files"])
    normal, rows, primary = analysis.upkeep_costs(old["native_states"][1:13])
    assert normal is True and old["startup_checks"]["normal_upkeep"] is False
    assert old["upkeep"]["old_mother_discount"] == old["upkeep"]["new_mother_discount"]
    for state in old["native_states"]:
        assert "eep_mothership" not in [m["modifier"] for m in state["country_modifiers"]]
        assert all(("eep_mothership" in [m["modifier"] for m in mods]) == (fid == state["mother"]["fleet"])
                   for fid, mods in state["fleet_modifiers"].items())
    report = copy.deepcopy(old)
    report["status"] = "PASS_SCOPED"
    report["startup_checks"]["normal_upkeep"] = True
    report["upkeep"].update(normal_costs_present=True, normal_cost_category_rows=rows, native_district_family_source=primary)
    report["correction"] = {"original_FAIL": analysis.ref(original), "scope": "only normal_upkeep aggregation now follows native planet_districts parent categories",
                            "unchanged_fields": "all raw native states, economic rows, other six startup checks, all economy checks and constraints",
                            "source": analysis.ref(Path(__file__)), "rule_source": analysis.ref(HERE / "rc6-economy-analysis-v2.py")}
    assert {k: v for k, v in report["startup_checks"].items() if k != "normal_upkeep"} == {
        k: v for k, v in old["startup_checks"].items() if k != "normal_upkeep"}
    assert all(report["startup_checks"].values())
    assert report["native_states"] == old["native_states"] and report["economy_checks"] == old["economy_checks"]
    out = folder / "native-branch-report-v2.json"
    analysis.write(out, report)
    payload = analysis.load(folder / "payload-proposal.json")
    assert payload["cases"]["purifier_startup"]["checks"]["normal_upkeep"] is False
    payload["cases"]["purifier_startup"]["checks"]["normal_upkeep"] = True
    for case in payload["cases"].values():
        assert case["status"] == "PENDING"
        case["evidence"] = [analysis.ref(out) if e["path"].endswith("/native-branch-report.json") else e for e in case["evidence"]]
    analysis.write(folder / "payload-proposal-v2.json", payload)
    primary_path = Path(primary["path"])
    primary_copy = folder / "native-economic-categories-primary.txt"
    with primary_copy.open("xb") as stream:
        stream.write(primary_path.read_bytes())
    assert analysis.sha(primary_copy) == primary["sha256"]
    supplement = {"schema": "eep.rc6.purifier_upkeep_category_correction.v1", "status": "PASS_SCOPED_CORRECTION_ONLY",
                  "original_index": analysis.ref(folder / "archive-index.json"), "original_FAIL": analysis.ref(original),
                  "corrected_report": analysis.ref(out), "corrected_payload": analysis.ref(folder / "payload-proposal-v2.json"),
                  "primary": analysis.ref(primary_copy), "source_primary": primary, "collector": analysis.ref(Path(__file__)),
                  "checks": {"all_original_payload_bytes_unchanged": True, "native_parent_family_has_positive_costs_every_month": normal,
                             "only_normal_upkeep_check_corrected": True, "all_other_native_and_budget_data_unchanged": True,
                             "case_statuses_remain_PENDING": True}}
    analysis.write(folder / "archive-supplement-v2.json", supplement)
    print(json.dumps({"status": report["status"], "report": analysis.ref(out), "payload": supplement["corrected_payload"],
                      "supplement": analysis.ref(folder / "archive-supplement-v2.json")}, indent=2))


if __name__ == "__main__":
    main()
