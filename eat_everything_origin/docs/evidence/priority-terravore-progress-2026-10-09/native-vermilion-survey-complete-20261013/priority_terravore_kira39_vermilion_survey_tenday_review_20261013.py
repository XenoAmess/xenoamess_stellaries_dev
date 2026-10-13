"""Ten-day native survey observation for Vermilion 544."""
import json
import logging
import sys
from pathlib import Path

before, end, raw_days, stage, prior_proof_file, prior_execution_stage = sys.argv[1:]
days = int(raw_days)
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
out = run / (stage + "-review.json")
assert not out.exists()
s = read_state(run, before)
prior = json.loads((run / prior_proof_file).read_text("utf-8-sig"))
execution = json.loads((run / (prior_execution_stage + "-execution.json")).read_text("utf-8-sig"))
science = s["fleets"]["166"]
move = q.block(science, "movement_manager")
reinforcement = s["fleets"]["50331731"]
cash = s["audit"]["countries"]["0"]["effective_stockpile"]
route = [97, 80, 71, 164, 39]
origin = q.scalars(q.block(move, "coordinate"))["origin"]
checks = {
    "prior_pass_actual0_source_and_exact_start_sav":
        prior["status"].startswith("PASS")
        and prior["checks"] and all(prior["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and prior["after_sha256"] == s["audit"]["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "one_month_or_shorter_native_interval_no_pending_error":
        1 <= days <= 30
        and meta["language"] == "l_simp_chinese"
        and s["pending"] == []
        and (run / (before + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes(),
    "science_ship_in_39_direct_survey_544_reachable":
        origin == 39
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 4294967295
        and q.scalars(move)["state"] == "move_idle"
        and "0=166" in q.block(q.block(s["roots"]["planets"], "planet"), "544")
        and "id=544" in q.block(science, "current_order")
        and "progress=1.1" in q.block(science, "current_order")
        and "can_reach=yes" in q.block(science, "current_order")
        and q.ids(q.block(science, "ships")) == [1049],
    "paid_crisis_destroyer_remains_mia_not_due":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and len(q.ids(q.block(s["fleets"]["917"], "ships"))) == 8
        and len(s["ships"]) == 75,
    "cash_runway":
        cash["energy"] > 1000 and cash["minerals"] > 500 and days == 10,
}
proof = {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": prior["after_sha256"],
    "after_sha256": prior["after_sha256"],
    "start_date": s["audit"]["date"],
    "end_date": end,
    "days": days,
    "maximum_days": days,
    "allowed_boundaries": [],
    "reviewed_boundaries": ["native_monthly_budget", "scout_route_or_survey", "mia_reinforcement"],
    "execution_stage": stage,
    "route_origin": origin,
    "scope": "Ten same-month days during active 544 survey; completion or event needs an independent postcheck.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
