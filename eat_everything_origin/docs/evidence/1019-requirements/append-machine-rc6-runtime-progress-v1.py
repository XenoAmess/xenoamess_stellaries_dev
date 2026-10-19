"""Append sealed Machine economy, retaining the earlier P/H PENDING snapshot."""
from datetime import datetime, timezone
from hashlib import sha256
import copy
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import publish_1019 as release
import runtime_index_1019 as helper

OUT = ROOT / "docs/evidence/1019-requirements/rc6-runtime-progress-v1.json"
SNAPSHOT = OUT.with_name("rc6-runtime-progress-v1-before-machine.json")
AUDIT = OUT.with_name("rc6-runtime-progress-v1-byte-audit.json")
RUN = "20261019T150008Z"
PACKET = "docs/evidence/1019-rc6-machine-economy-worker-ui-v1"
BASE = "docs/evidence/1019-rc6-economy"


def mutate(data):
    payload = release.read_json(ROOT / BASE / "three-branch-payload-proposal-v1.json")
    assert payload["status"] == "PENDING_CASE_EVIDENCE_ASSEMBLY"
    for name, item in payload["cases"].items():
        assert item["status"] == "PENDING" and item["production_tree_sha256"] == data["production_tree_sha256"]
        helper.bind_run(data, "docs/evidence/1019-rc6-migration-checkpoint-v1/run/manifest.json", ROOT, (name,))
        analysis = next(row["path"] for row in item["evidence"] if row["kind"] == "analysis")
        for check, value in item["checks"].items():
            if value is not None: helper.observe_check(data, name, check, value, analysis, RUN, ROOT)
        for row in item["evidence"]:
            release.reference_path(row, ROOT); helper.attach(data, name, RUN, row["kind"], row["path"], ROOT)
        helper.attach(data, name, RUN, "analysis", BASE + "/three-branch-native-summary-v1.json", ROOT)
    for branch, months in payload["economy"].items():
        if branch != "machine": assert data["economy"][branch] == months
        data["economy"][branch] = copy.deepcopy(months)
        for row in months["candidate_months"]:
            release.reference_path(row["evidence"], ROOT)
            helper.attach(data, branch + "_economy", RUN, "native_save", row["evidence"]["path"], ROOT)
        for row in months["baseline_months"]:
            release.reference_path(row["evidence"], ROOT); helper.add_reference(data["archives"], row["evidence"])
        assert all(data["cases"][branch + "_economy"]["checks"][key] is None for key in ("no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband"))
    packet = release.read_json(ROOT / PACKET / "index.json")
    for row in packet["files"]:
        if not row["path"].startswith("machine/"): continue
        name = Path(row["path"]).name
        kind = "screenshot" if name.endswith((".jpg", ".png")) else "actions" if name.endswith(".action.json") else "analysis"
        helper.attach(data, "machine_economy", RUN, kind, PACKET + "/" + row["path"], ROOT)
        if name.startswith(("r6mc-newgame", "r6mc-empire", "r6mc-select", "r6mc-galaxy", "r6mc-start", "r6mc-intro", "r6mc-initial", "r6mcm00")):
            helper.attach(data, "machine_startup", RUN, kind, PACKET + "/" + row["path"], ROOT)
    for case in ("machine_startup", "machine_economy"):
        for name in ("index.json", "verify.json"): helper.attach(data, case, RUN, "analysis", PACKET + "/" + name, ROOT)
    for path in (BASE + "/three-branch-native-summary-v1.json", BASE + "/three-branch-payload-proposal-v1.json", BASE + "/machine/archive-index.json", BASE + "/machine/byte-verification-v1.json", PACKET + "/index.json", PACKET + "/verify.json"):
        helper.add_reference(data["archives"], release.collect_reference({"path": path, "kind": "analysis"}, ROOT))
    limits = data["_progress"]["scope_limits"]
    limits[-1] = "Machine completed-year notification authorized only its sealed startup/economy chain; separate r6mcinit2 and active r6g growth/logs remain unread and unmerged"
    data["_progress"]["root_review_required_economy_checks"]["machine"] = ["no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband"]
    data["_progress"]["pre_machine_pending_snapshot"] = release.collect_reference(SNAPSHOT.relative_to(ROOT).as_posix(), ROOT)


def main():
    assert not SNAPSHOT.exists() and not AUDIT.exists()
    original = OUT.read_bytes(); shutil.copyfile(OUT, SNAPSHOT); assert SNAPSHOT.read_bytes() == original
    result = helper.update_progress(OUT, ROOT, {"command": "append_sealed_Machine_and_three_branch_proposal", "scope": "Twelve operation constraints await root; init2/growth excluded"}, mutate)
    _, data = helper.load_progress(OUT, ROOT)
    assert len(data["cases"]) == 18 and all(row["status"] == "PENDING" for row in data["cases"].values())
    missing = helper.missing(data)
    OUT.with_name("rc6-runtime-progress-v1-missing.json").write_text(json.dumps(missing, indent=2) + "\n", encoding="utf-8")
    refs = {}; objects = 0
    def check(value):
        nonlocal objects
        if isinstance(value, list):
            for row in value: check(row)
        elif isinstance(value, dict):
            if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
                objects += 1
                if value["path"] not in refs:
                    path = release.reference_path(value, ROOT)
                    assert "r6mcinit2" not in str(path) and not any(part.startswith("r6g") for part in path.parts)
                    refs[value["path"]] = {"path": value["path"], "sha256": value["sha256"], "bytes": path.stat().st_size}
                else: assert refs[value["path"]]["sha256"] == value["sha256"]
            for row in value.values(): check(row)
    check(data)
    runs = {release.read_json(release.reference_path(ref, ROOT))["run_id"]: ref["sha256"] for ref in data["runs"]}
    assert list(runs) == [RUN]
    release.validate_migration_contract(data["cases"]["old_save_migration"], data["production_tree_sha256"], ROOT, runs)
    assert all(len(data["economy"][branch][role + "_months"]) == 12 for branch in ("hive", "machine", "purifier") for role in ("baseline", "candidate"))
    counts = {name: {"true": sum(v is True for v in case["checks"].values()), "false": sum(v is False for v in case["checks"].values()), "null": sum(v is None for v in case["checks"].values())} for name, case in data["cases"].items()}
    audit = {"schema": "eep.rc6.pending-runtime-progress-byte-audit.v1", "status": "PENDING_REFERENCES_VERIFIED_NO_ACCEPTANCE",
             "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": sha256(OUT.read_bytes()).hexdigest(),
             "pre_machine_snapshot_sha256": sha256(original).hexdigest(), "helper_result": result,
             "all_18_case_statuses_PENDING": True, "component_and_top_PENDING": True, "unique_run_count": 1,
             "reference_objects_verified": objects, "unique_references_verified": len(refs), "references": sorted(refs.values(), key=lambda row: row["path"]),
             "case_check_counts": counts, "three_branches_each_12_baseline_12_candidate": True,
             "twelve_operation_checks_remain_null": True, "original_v1_damage_FALSE_retained": True,
             "migration_v2_scope_validator": "VALIDATED_CASE_STILL_PENDING", "active_growth_init2_or_logs_read": False,
             "system_wide_input_audit_claim": False, "final_result_written": False, "UI_or_Git_operations": False}
    AUDIT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    lines = ["# RC6 PENDING进度缺口", "", "18组均PENDING；表中数量为已记录单项观察，不是case验收。全部组仍缺最终运行log；缺项详细原名见相邻missing JSON。", "", "| Case | true | false | null | 缺少证据类型 |", "|---|---:|---:|---:|---|"]
    for name, case in data["cases"].items():
        c = counts[name]; kinds = ", ".join(missing["cases"][name]["missing_evidence_kinds"])
        lines.append(f"| {name} | {c['true']} | {c['false']} | {c['null']} | {kinds or '-'} |")
    lines += ["", "三分支startup各7项true，需root对完整证据和PENDING状态作最终review；经济各3项true、4项null，后四项仅受控worker链等待root审查，不能称系统输入审计。", "", "母舰仅维护观察、源推算power非负、22大防御槽三项true；同国同日Relic参考、实际跃迁、10船坞、技术/其它主宰负对照等仍待独立证据或review。source-derived+9743不是UI供电数值。", "", "迁移原严格damage_preserved=false保留，独立v2预算true；其它11项顶层映射尚待root审核，底层174/158 scoped报告和真实重复样本已在合同中。缺口不等于必须重做已有样本。", "", "其余成长/RNG、三组巨像、共用结算、普通拆解、Lithoid首月、候选restart/reload与repeat初始化等当前未合并证据/观察。活动r6g、独立r6mcinit2和最终日志没有读取，待各线程封口后另追加。", "", "所有缺结果保留null；未生成final-result、未将任何case改PASS。"]
    OUT.with_name("rc6-runtime-progress-v1-missing.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in audit.items() if k not in ("references", "case_check_counts")}, indent=2))
    print(json.dumps(counts))


if __name__ == "__main__": main()
