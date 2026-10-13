"""Validate ten native days toward the first remaining Kira survey body 546."""
import json
import logging
import math
import re
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
old_target = q.scalars(q.block(old_move, "target_coordinate"))
new_target = q.scalars(q.block(new_move, "target_coordinate"))
cash_keys = ["energy", "minerals", "food", "influence", "unity", "trade", "alloys", "rare_crystals", "menace"]
reinforcement = a["fleets"]["50331731"]
old_planet = q.block(q.block(b["roots"]["planets"], "planet"), "546")
new_planet = q.block(q.block(a["roots"]["planets"], "planet"), "546")
orbital_line = "\t\t\t\t0=166\n"
old_545 = q.block(q.block(b["roots"]["planets"], "planet"), "545")
old_544 = q.block(q.block(b["roots"]["planets"], "planet"), "544")
new_545 = q.block(q.block(a["roots"]["planets"], "planet"), "545")
new_544 = q.block(q.block(a["roots"]["planets"], "planet"), "544")
checks = {
    "prior_review_calendar_actual0_exact_sav_chain":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and calendar["status"] == "CALENDAR_CONFIRMED" and calendar["days"] == 1
        and (calendar["start_date"], calendar["date"]) == (b["audit"]["date"], a["audit"]["date"])
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and prior["after_sha256"] == review["after_sha256"] == b["audit"]["save_sha256"]
        == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "science_ship_finishes_546_and_automatically_starts_545_route":
        old_pos["origin"] == new_pos["origin"] == 39
        and q.scalars(old_move)["state"] == "move_idle"
        and q.scalars(new_move)["state"] == "move_system"
        and new_target == {"x":-116.99614,"y":6.33,"origin":39}
        and math.hypot(new_pos["x"]-new_target["x"],new_pos["y"]-new_target["y"])
        < math.hypot(old_pos["x"]-new_target["x"],old_pos["y"]-new_target["y"])
        and "id=546" in q.block(old, "current_order")
        and "progress=29.7" in q.block(old, "current_order")
        and "id=545" in q.block(new, "current_order")
        and "progress=0" in q.block(new, "current_order")
        and "can_reach=yes" in q.block(new, "current_order")
        and re.findall(r"\bid=(\d+)", q.block(old, "order"))
        == ["545", "552", "553", "547", "543", "549", "554", "555", "550", "551", "548"]
        and re.findall(r"\bid=(\d+)", q.block(new, "order"))
        == ["552", "553", "547", "543", "549", "554", "555", "550", "551", "548"]
        and q.ids(q.block(new, "ships")) == [1049]
        and old_planet.count(orbital_line) == 1
        and old_planet.replace(orbital_line, "") == new_planet
        and old_545 == new_545 and old_544 == new_544,
    "same_month_cash_and_budget_stable_research_nonnegative":
        all(ac["effective_stockpile"].get(k) == bc["effective_stockpile"].get(k) for k in cash_keys)
        and all(ac["effective_stockpile"].get(k, 0) >= bc["effective_stockpile"].get(k, 0)
                for k in ("physics_research", "society_research", "engineering_research"))
        and ac["budget_categories"]["current_month"] == bc["budget_categories"]["current_month"],
    "mineral_reinforcement_all_ship_membership_safe":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and q.scalars(q.block(q.block(reinforcement, "current_order"), "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships")) == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"]),
    "eep_pending_messages_error_stable":
        all(ac["variables"].get(k) == bc["variables"].get(k)
            for k in ("eep_c", "eep_d", "eep_stage", "eep_crisis"))
        and a["pending"] == b["pending"] == []
        and a["messages"] == b["messages"] == []
        and (run / (after + "-error-before.log")).read_bytes()
        == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_546_TO_545_AUTO_TRANSITION" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "new_coordinate": new_pos,
    "survey_progress": q.scalars(q.block(q.block(new, "current_order"), "survey_planet_order"))["progress"],
    "scope": "First remaining body 546 completes, auto-queue moves to 545 with ten more bodies; full-system survey and outpost pending.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
