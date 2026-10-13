"""Authorize exactly one native day across the mineral-paid shipyard boundary."""
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
before = "terravore-kira39-shipyard-precompletion-native-22881224"
guard = "terravore-kira39-shipyard-precompletion-guard-v2-22881224"
stage = "terravore-kira39-shipyard-birth-review-22881224"
out = run / (stage + "-review.json")
assert not out.exists()
s = read_state(run, before)
p = json.loads((run / (guard + "-proof.json")).read_text("utf-8-sig"))
execution = json.loads((run / (guard + "-execution.json")).read_text("utf-8-sig"))
fleet = s["fleets"]["166"]
item = s["items"]["704643085"]
checks = {
    "precompletion_five_pass_actual0_source_original_save":
        p["status"] == "PASS_NATIVE_KIRA39_SHIPYARD_PRECOMPLETION"
        and all(p["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and p["after_sha256"] == s["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "exact_single_day_paused_chinese_no_pending_error":
        s["audit"]["date"] == "2288.12.24"
        and meta["language"] == "l_simp_chinese"
        and s["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "mineral_paid_original_queue_one_work_step_from_finish":
        q.scalars(item)["progress"] == 58.5
        and q.scalars(item)["progress_needed"] == 60
        and q.scalars(q.block(item, "resources")) == {"minerals": 412.5}
        and q.ids(q.block(s["queues"]["3"], "items")) == [704643085]
        and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8
        and len(s["ships"]) == 74,
    "science166_safe_reachable_to39":
        q.scalars(q.block(q.block(fleet, "movement_manager"), "coordinate"))["origin"] == 97
        and q.scalars(q.block(q.block(fleet, "movement_manager"), "target_coordinate"))["origin"] == 39
        and "can_reach=yes" in q.block(fleet, "current_order"),
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": p["after_sha256"],
    "after_sha256": p["after_sha256"],
    "start_date": "2288.12.24",
    "end_date": "2288.12.25",
    "days": 1,
    "maximum_days": 1,
    "allowed_boundaries": [],
    "reviewed_boundaries": ["paid_crisis_destroyer_shipyard_completion_or_next_work_step"],
    "execution_stage": stage,
    "scope": "One day only, then inspect actual item, new ship IDs, reinforcement routing and costs.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
