"""Authorize only the first five native days after the Kira survey order."""
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
before = "terravore-kira39-science166-survey-ordered-native-v2-22881115"
guard = "terravore-kira39-science166-survey-order-guard-22881115"
stage = "terravore-kira39-scout-first5-review-22881115"
out = run / (stage + "-review.json")
assert not out.exists()
s = read_state(run, before)
p = json.loads((run / (guard + "-proof.json")).read_text("utf-8-sig"))
execution = json.loads((run / (guard + "-execution.json")).read_text("utf-8-sig"))
fleet = s["fleets"]["166"]
item = s["items"]["704643085"]
stock = s["audit"]["countries"]["0"]["effective_stockpile"]
checks = {
    "survey_order_guard_actual0_source_and_same_original_save":
        p["status"] == "PASS_NATIVE_KIRA39_SCIENCE166_SURVEY_ORDER"
        and all(p["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and p["after_sha256"] == s["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "five_days_before_month_boundary":
        s["audit"]["date"] == "2288.11.15"
        and meta["language"] == "l_simp_chinese"
        and len(s["pending"]) == 0,
    "science166_target39_reachable_not_arrived":
        q.scalars(q.block(q.block(fleet, "movement_manager"), "target_coordinate"))["origin"] == 39
        and "can_reach=yes" in q.block(fleet, "current_order")
        and q.scalars(q.block(q.block(fleet, "movement_manager"), "coordinate"))["origin"] == 37,
    "paid_mineral_ship_still_unbuilt":
        q.scalars(item)["progress"] == 0
        and q.scalars(item)["progress_needed"] == 60
        and q.ids(q.block(s["fleets"]["917"], "ships"))
            and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8,
    "cash_runway_and_no_new_error":
        stock["minerals"] > 1000
        and stock["energy"] > 1000
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": p["after_sha256"],
    "after_sha256": p["after_sha256"],
    "start_date": "2288.11.15",
    "end_date": "2288.11.20",
    "days": 5,
    "maximum_days": 5,
    "allowed_boundaries": [],
    "execution_stage": stage,
    "scope": "Five native days only; mandatory independent survey/shipyard/event review afterward.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
