"""Review first native month close after mineral crisis destroyer birth."""
import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-kira39-shipyard-birth-native-22881225"
guard = "terravore-kira39-shipyard-birth-guard-22881225"
stage = "terravore-kira39-postbirth-month-review-22881225"
out = run / (stage + "-review.json")
assert not out.exists()
s = read_state(run, before)
p = json.loads((run / (guard + "-proof.json")).read_text("utf-8-sig"))
execution = json.loads((run / (guard + "-execution.json")).read_text("utf-8-sig"))
science = s["fleets"]["166"]
reinforcement = s["fleets"]["50331731"]
cash = s["audit"]["countries"]["0"]["effective_stockpile"]
checks = {
    "birth_five_pass_actual0_source_original_save":
        p["status"] == "PASS_NATIVE_KIRA39_MINERAL_CRISIS_DESTROYER_BIRTH"
        and all(p["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and p["after_sha256"] == s["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "first_six_days_to_month_boundary_safe_and_chinese":
        s["audit"]["date"] == "2288.12.25"
        and meta["language"] == "l_simp_chinese"
        and s["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "science_can_reach_and_new_ship_mia_merge_not_due":
        q.scalars(q.block(q.block(science, "movement_manager"), "coordinate"))["origin"] == 97
        and q.scalars(q.block(q.block(science, "movement_manager"), "target_coordinate"))["origin"] == 39
        and "can_reach=yes" in q.block(science, "current_order")
        and q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.scalars(q.block(q.block(reinforcement, "current_order"), "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8,
    "cash_runway_no_other_owned_queued_reinforcement":
        cash["energy"] > 1000 and cash["minerals"] > 1000
        and q.ids(q.block(s["queues"]["3"], "items")) == [],
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": p["after_sha256"],
    "after_sha256": p["after_sha256"],
    "start_date": "2288.12.25",
    "end_date": "2289.01.01",
    "days": 6,
    "maximum_days": 6,
    "allowed_boundaries": [],
    "reviewed_boundaries": ["native_monthly_budget_after_mia_reinforcement_birth"],
    "execution_stage": stage,
    "scope": "One month close; inspect actual scout progress, MIA merge and budget before continuing.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
