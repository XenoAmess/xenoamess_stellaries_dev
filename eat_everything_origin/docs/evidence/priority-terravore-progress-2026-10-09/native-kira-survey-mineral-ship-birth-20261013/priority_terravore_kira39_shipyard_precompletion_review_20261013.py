"""Bound native Dec 1-24 travel before expected paid reinforcement birth."""
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
before = "terravore-kira39-scout-first-month-native-22881201"
guard = "terravore-kira39-scout-first-month-guard-v2-22881201"
stage = "terravore-kira39-shipyard-precompletion-review-22881201"
out = run / (stage + "-review.json")
assert not out.exists()
s = read_state(run, before)
p = json.loads((run / (guard + "-proof.json")).read_text("utf-8-sig"))
execution = json.loads((run / (guard + "-execution.json")).read_text("utf-8-sig"))
fleet = s["fleets"]["166"]
item = s["items"]["704643085"]
stock = s["audit"]["countries"]["0"]["effective_stockpile"]
checks = {
    "previous_six_pass_actual0_and_exact_native_save":
        p["status"] == "PASS_NATIVE_KIRA39_SCOUT_FIRST_MONTH"
        and all(p["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and p["after_sha256"] == s["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "date_language_no_pending_or_new_error":
        s["audit"]["date"] == "2288.12.01"
        and meta["language"] == "l_simp_chinese"
        and s["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "scout_reachable_mineral_ship_paid_and_precompletion_bound":
        q.scalars(q.block(q.block(fleet, "movement_manager"), "target_coordinate"))["origin"] == 39
        and "can_reach=yes" in q.block(fleet, "current_order")
        and q.scalars(item)["progress"] == 24
        and q.scalars(item)["progress_needed"] == 60
        and q.scalars(item)["paying_country"] == 0
        and q.ids(q.block(s["queues"]["3"], "items")) == [704643085]
        and 24 + 23 * 1.5 == 58.5 < 60
        and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8,
    "cash_and_fleet_runway":
        stock["energy"] > 1000 and stock["minerals"] > 1000
        and len(s["ships"]) == 74,
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": p["after_sha256"],
    "after_sha256": p["after_sha256"],
    "start_date": "2288.12.01",
    "end_date": "2288.12.24",
    "days": 23,
    "maximum_days": 23,
    "allowed_boundaries": [],
    "reviewed_boundaries": ["paid_reinforcement_construction_near_completion"],
    "execution_stage": stage,
    "scope": "One precompletion interval only; verify actual shipyard/scout/event state before Dec 25.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
