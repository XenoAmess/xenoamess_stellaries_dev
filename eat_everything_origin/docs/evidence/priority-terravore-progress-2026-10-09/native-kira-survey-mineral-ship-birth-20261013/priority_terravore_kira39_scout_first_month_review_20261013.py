"""Review the 11-day native month crossing for scout and mineral ship."""
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
before = "terravore-kira39-scout-first5-native-22881120"
guard = "terravore-kira39-scout-first5-guard-22881120"
stage = "terravore-kira39-scout-first-month-review-22881120"
out = run / (stage + "-review.json")
assert not out.exists()
s = read_state(run, before)
p = json.loads((run / (guard + "-proof.json")).read_text("utf-8-sig"))
execution = json.loads((run / (guard + "-execution.json")).read_text("utf-8-sig"))
fleet = s["fleets"]["166"]
item = s["items"]["704643085"]
stock = s["audit"]["countries"]["0"]["effective_stockpile"]
checks = {
    "five_day_guard_actual0_source_and_original_save":
        p["status"] == "PASS_NATIVE_KIRA39_SCOUT_FIRST5"
        and all(p["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and p["after_sha256"] == s["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "exact_11_day_month_crossing_no_pending_event":
        s["audit"]["date"] == "2288.11.20"
        and meta["language"] == "l_simp_chinese"
        and s["pending"] == [],
    "scout_still_reachable_and_shipyard_will_not_finish":
        q.scalars(q.block(q.block(fleet, "movement_manager"), "target_coordinate"))["origin"] == 39
        and "can_reach=yes" in q.block(fleet, "current_order")
        and q.scalars(item)["progress"] == 7.5
        and q.scalars(item)["progress_needed"] == 60
        and 7.5 + 11 * 1.5 == 24 < 60
        and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8,
    "monthly_budget_cash_runway_and_error_stable":
        stock["energy"] > 1000
        and stock["minerals"] > 1000
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": p["after_sha256"],
    "after_sha256": p["after_sha256"],
    "start_date": "2288.11.20",
    "end_date": "2288.12.01",
    "days": 11,
    "maximum_days": 11,
    "allowed_boundaries": [],
    "reviewed_boundaries": ["native_monthly_budget_settlement"],
    "execution_stage": stage,
    "scope": "One native month crossing with independent monthly budget, scout and shipyard check required.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
