"""Guard five native FTL wind-up days before crossing into Kira 39."""
import json
import logging
import math
import sys
from pathlib import Path

before, after, stage, prior_proof_file, review_stage = sys.argv[1:]
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
out = run / (stage + "-proof.json")
assert not out.exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
prior, review = load(prior_proof_file), load(review_stage + "-review.json")
calendar, execution = load(after + "-calendar-receipt.json"), load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
old, new = (s["fleets"]["166"] for s in (b, a))
old_move, new_move = (q.block(f, "movement_manager") for f in (old, new))
old_pos, new_pos = (q.scalars(q.block(m, "coordinate")) for m in (old_move, new_move))
entrance = q.scalars(q.block(q.block(q.block(new_move, "path"), "node"), "coordinate"))
distance = lambda p: math.hypot(p["x"]-entrance["x"], p["y"]-entrance["y"])
cash_keys = ["energy", "minerals", "food", "influence", "unity", "trade", "alloys", "rare_crystals", "menace"]
reinforcement = a["fleets"]["50331731"]
checks = {
    "prior_review_calendar_receipt_actual0_exact_sav_chain":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == 5
        and (calendar["start_date"], calendar["date"])
            == (b["audit"]["date"], a["audit"]["date"])
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and prior["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "same_month_cash_stable_research_grows":
        all(ac["effective_stockpile"].get(k) == bc["effective_stockpile"].get(k)
            for k in cash_keys)
        and all(ac["effective_stockpile"].get(k, 0) >= bc["effective_stockpile"].get(k, 0)
                for k in ("physics_research", "society_research", "engineering_research"))
        and ac["budget_categories"]["current_month"] == bc["budget_categories"]["current_month"],
    "science_ship_ftl_windup_exact_progress_without_jump":
        old_pos["origin"] == new_pos["origin"] == 164
        and entrance["origin"] == 164
        and q.scalars(q.block(new_move, "target_coordinate"))["origin"] == 39
        and distance(new_pos) == distance(old_pos)
        and q.scalars(old_move)["state"] == q.scalars(new_move)["state"] == "move_wind_up"
        and q.scalars(new_move)["ftl_total_windup"] == q.scalars(old_move)["ftl_total_windup"] == 112
        and q.scalars(new_move)["ftl_windup"] - q.scalars(old_move)["ftl_windup"] == 100
        and q.scalars(new_move)["ftl_windup"] < 112
        and q.block(new, "current_order") == q.block(old, "current_order")
        and "can_reach=yes" in q.block(new, "current_order")
        and q.ids(q.block(new, "ships")) == [1049]
        and q.block(q.block(b["roots"]["planets"], "planet"), "544")
            == q.block(q.block(a["roots"]["planets"], "planet"), "544"),
    "mineral_reinforcement_and_all_ship_membership_safe":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and q.scalars(q.block(q.block(reinforcement, "current_order"),
                              "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships")) for k in b["fleets"]),
    "eep_pending_messages_error_stable":
        all(ac["variables"].get(k) == bc["variables"].get(k)
            for k in ("eep_c", "eep_d", "eep_stage", "eep_crisis"))
        and a["pending"] == b["pending"] == []
        and a["messages"] == b["messages"] == []
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_FTL_WINDUP_FIVE_DAYS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "old_coordinate": old_pos,
    "new_coordinate": new_pos,
    "remaining_distance": distance(new_pos),
    "scope": "Five non-month FTL wind-up days; crossing or survey needs a separate boundary guard.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
