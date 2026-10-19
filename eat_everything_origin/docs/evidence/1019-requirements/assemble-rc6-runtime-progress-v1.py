"""Merge immutable observed evidence through the existing PENDING helper only."""
import copy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import publish_1019 as release
import runtime_index_1019 as helper

OUTPUT = ROOT / "docs/evidence/1019-requirements/rc6-runtime-progress-v1.json"
AUDIT = OUTPUT.with_name("rc6-runtime-progress-v1-assembly.json")
RUN = "20261019T150008Z"
MANIFEST = "docs/evidence/1019-rc6-migration-checkpoint-v1/run/manifest.json"
WORKER = "docs/evidence/1019-rc6-economy-worker-ui-v1"
MOTHER = "docs/evidence/1019-rc6-purifier-mothership-ui-v1"
POWER = "docs/evidence/1019-rc6-power-source/power-inventory-report-v1.json"
MIGRATION = "docs/evidence/1019-requirements/rc6-migration-v2-scope-pending-v1.json"
FOUR = ("no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband")


def read(name): return release.read_json(ROOT / name)


def attach_ref(data, case, ref):
    release.reference_path(ref, ROOT)
    helper.attach(data, case, RUN, ref["kind"], ref["path"], ROOT)


def mutate(data):
    migration = read(MIGRATION)
    assert migration["status"] == "PENDING" and migration["production_tree_sha256"] == data["production_tree_sha256"]
    helper.bind_run(data, MANIFEST, ROOT, ("old_save_migration", "mothership_configuration"))
    target = data["cases"]["old_save_migration"]
    proposal = migration["cases"]["old_save_migration"]
    target["checks"].update(copy.deepcopy(proposal["checks"]))
    target["migration_contract"] = copy.deepcopy(proposal["migration_contract"])
    for ref in proposal["evidence"]: attach_ref(data, "old_save_migration", ref)
    helper.add_reference(data["archives"], release.collect_reference({"path": MIGRATION, "kind": "analysis"}, ROOT))
    worker_index = read(WORKER + "/index.json")
    for branch, prefix, filename in (("purifier", "r6pu", "payload-proposal-v2.json"), ("hive", "r6hvc", "payload-proposal.json")):
        base = "docs/evidence/1019-rc6-economy/" + branch
        payload = read(base + "/" + filename)
        names = (branch + "_startup", branch + "_economy")
        helper.bind_run(data, MANIFEST, ROOT, names)
        for name in names:
            item = payload["cases"][name]
            assert item["status"] == "PENDING" and item["production_tree_sha256"] == data["production_tree_sha256"]
            source = next(ref["path"] for ref in item["evidence"] if ref["kind"] == "analysis")
            for check, result in item["checks"].items():
                if result is not None: helper.observe_check(data, name, check, result, source, RUN, ROOT)
            for ref in item["evidence"]: attach_ref(data, name, ref)
        data["economy"][branch] = copy.deepcopy(payload["economy"][branch])
        for row in data["economy"][branch]["candidate_months"]: attach_ref(data, branch + "_economy", row["evidence"])
        for row in data["economy"][branch]["baseline_months"]:
            release.reference_path(row["evidence"], ROOT); helper.add_reference(data["archives"], row["evidence"])
        for row in worker_index["files"]:
            if not row["path"].startswith(branch + "/"): continue
            name = Path(row["path"]).name
            kind = "screenshot" if name.endswith((".jpg", ".png")) else "actions" if name.endswith(".action.json") else "analysis"
            path = WORKER + "/" + row["path"]
            helper.attach(data, branch + "_economy", RUN, kind, path, ROOT)
            startup = (prefix + "-newgame", prefix + "-empire", prefix + "-select", prefix + "-galaxy", prefix + "-start", prefix + "-intro", prefix + "-initial", prefix + "m00")
            if name.startswith(startup): helper.attach(data, branch + "_startup", RUN, kind, path, ROOT)
        for name in names:
            for suffix in ("index.json", "verify.json"):
                helper.attach(data, name, RUN, "analysis", WORKER + "/" + suffix, ROOT)
        for check in FOUR: assert data["cases"][branch + "_economy"]["checks"][check] is None
        helper.add_reference(data["archives"], release.collect_reference({"path": base + "/" + filename, "kind": "analysis"}, ROOT))
    for path in ("docs/evidence/1019-rc6-economy/purifier/native-branch-report.json", "docs/evidence/1019-rc6-economy/purifier/archive-supplement-v2.json"):
        helper.add_reference(data["archives"], release.collect_reference({"path": path, "kind": "analysis"}, ROOT))
    typed = read(MOTHER + "/typed-references.json")
    for ref in typed["references"]:
        name = ref["path"].removeprefix("eat_everything_origin/")
        helper.attach(data, "mothership_configuration", RUN, ref["kind"], name, ROOT)
    observations = MOTHER + "/observations.json"
    helper.observe_check(data, "mothership_configuration", "upkeep_observed", True, observations, RUN, ROOT)
    helper.observe_check(data, "mothership_configuration", "power_nonnegative", True, POWER, RUN, ROOT)
    power = read(POWER)
    assert power["status"] == "SOURCE_DERIVED_NOT_UI_MEASURED" and power["arithmetic"]["source_derived_balance"] == 9743
    large = [row for row in power["inventory"] if row["kind"] == "slot" and row["slot"].startswith("LARGE_UTILITY_")]
    assert len(large) == 22
    helper.observe_check(data, "mothership_configuration", "twenty_two_large_defense_slots", True, POWER, RUN, ROOT)
    data.setdefault("_progress", {})["scope_limits"] = [
        "All 18 case/component/top statuses remain PENDING; no final-result created",
        "Migration v2 bounded engineering allowance is separate from retained original damage_preserved=false/v1 FAIL",
        "Two economy four-check groups remain null pending root review; controlled worker chain is not system-wide input audit",
        "Mother power_nonnegative is source-derived +9743, not native UI power measurement; upkeep is date/state-specific10.07/2.88 at115/66",
        "Other Mother configuration checks need independent review/evidence; 50+6 actual identity alone is not all configuration acceptance",
        "Machine r6mc was neither read nor filled; active logs are not included"]
    data["_progress"]["root_review_required_economy_checks"] = {branch: list(FOUR) for branch in ("hive", "purifier")}
    data["_progress"]["mother_partial_identity"] = power["actual_identity"]
    for suffix in ("index.json", "verify.json"):
        helper.add_reference(data["archives"], release.collect_reference({"path": WORKER + "/" + suffix, "kind": "analysis"}, ROOT))
    assert data["status"] == data["component_rewards"]["status"] == "PENDING" and len(data["cases"]) == 18
    assert all(case["status"] == "PENDING" for case in data["cases"].values())
    assert data["economy"]["machine"] == {"baseline_months": [], "candidate_months": []}


def main():
    assert not AUDIT.exists(), "Sealed progress v1 cannot be overwritten"
    result = helper.update_progress(OUTPUT, ROOT, {"command": "merge_sealed_RC6_pending_proposals", "scope": "No case promotion; four economy checks await root"}, mutate)
    _, data = helper.load_progress(OUTPUT, ROOT)
    runs = {release.read_json(release.reference_path(row, ROOT))["run_id"]: row["sha256"] for row in data["runs"]}
    assert list(runs) == [RUN]
    release.validate_migration_contract(data["cases"]["old_save_migration"], data["production_tree_sha256"], ROOT, runs)
    missing = helper.missing(data)
    OUTPUT.with_name("rc6-runtime-progress-v1-missing.json").write_text(json.dumps(missing, indent=2) + "\n", encoding="utf-8")
    refs, reference_objects = {}, 0
    def verify_refs(value):
        nonlocal reference_objects
        if isinstance(value, list):
            for item in value: verify_refs(item)
        elif isinstance(value, dict):
            if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
                reference_objects += 1
                if value["path"] not in refs:
                    path = release.reference_path(value, ROOT)
                    assert "r6mc" not in str(path) and not str(path).endswith("/logs/error.log")
                    refs[value["path"]] = {"path": value["path"], "sha256": value["sha256"], "bytes": path.stat().st_size}
                else: assert refs[value["path"]]["sha256"] == value["sha256"]
            for item in value.values(): verify_refs(item)
    verify_refs(data)
    report = {"schema": "eep.rc6.pending-runtime-progress-assembly.v1", "status": "PENDING_EVIDENCE_REFERENCES_VERIFIED",
              "created_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
              "helper_result": result, "case_count": 18, "all_case_statuses_PENDING": True, "unique_run_count": len(runs),
              "reference_objects_verified": reference_objects, "unique_references_verified": len(refs), "references": sorted(refs.values(), key=lambda row: row["path"]),
              "case_check_counts": {name: {"true": sum(value is True for value in case["checks"].values()), "false": sum(value is False for value in case["checks"].values()), "null": sum(value is None for value in case["checks"].values())} for name, case in data["cases"].items()},
              "migration_v2_contract_readonly_validation": "VALIDATED_SCOPE_ONLY_CASE_PENDING", "original_damage_preserved_false_retained": True,
              "four_economy_checks_each_branch_null": True, "Machine_or_active_logs_read": False, "final_result_written": False,
              "tools": [{"path": "tools/" + name, "sha256": sha256((ROOT / "tools" / name).read_bytes()).hexdigest()} for name in ("publish_1019.py", "runtime_index_1019.py")]}
    AUDIT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key not in ("references", "case_check_counts")}, indent=2))


if __name__ == "__main__": main()
