"""One-day May-to-June budget and direct Vermilion 544 survey approach guard."""
import json
import logging
import math
import re
import sys
from decimal import Decimal as D
from pathlib import Path

before, after, raw_days, stage, prior_proof_file, review_stage = sys.argv[1:]
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
out = run / (stage + "-proof.json")
assert not out.exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
prior = load(prior_proof_file)
review = load(review_stage + "-review.json")
calendar = load(after + "-calendar-receipt.json")
execution = load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
cur = ac["budget_categories"]["current_month"]
cash = ["energy", "minerals", "alloys", "unity", "rare_crystals"]
actual = {k: D(str(ac["effective_stockpile"].get(k, 0)))
          - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
net = {k: sum((D(str(v.get(k, 0))) for v in cur["income"].values()), D(0))
       - sum((D(str(v.get(k, 0))) for v in cur["expenses"].values()), D(0))
       for k in cash}
residual = {k: actual[k] - net[k] for k in cash}
science = a["fleets"]["166"]
move = q.block(science, "movement_manager")
route = [97, 80, 71, 164, 39]
old_origin = q.scalars(q.block(q.block(b["fleets"]["166"], "movement_manager"), "coordinate"))["origin"]
old_pos = q.scalars(q.block(q.block(b["fleets"]["166"], "movement_manager"), "coordinate"))
new_pos = q.scalars(q.block(move, "coordinate"))
target = q.scalars(q.block(move, "target_coordinate"))
origin = q.scalars(q.block(move, "coordinate"))["origin"]
path_raw = q.block(move, "path")
path_origins = [int(x) for x in re.findall(r"\borigin=(\d+)", path_raw)]
path_systems = []
for x in path_origins:
    if not path_systems or path_systems[-1] != x:
        path_systems.append(x)
reinforcement = a["fleets"]["50331731"]
checks = {
    "prior_review_native_calendar_saves_exact_sha_chain":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == days
        and calendar["start_date"] == b["audit"]["date"]
        and calendar["date"] == a["audit"]["date"]
        and prior["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "native_monthly_five_cash_deltas_equal_new_budget_net":
        all(abs(v) <= D("0.00002") for v in residual.values())
        and ac["budget_categories"]["last_month"]
            == bc["budget_categories"]["current_month"],
    "science_166_approaches_544_inside_39_without_survey_start":
        days == 1 and old_origin == origin == 39
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 39
        and "id=544" in q.block(science, "current_order")
        and "progress=0" in q.block(science, "current_order")
        and "can_reach=yes" in q.block(science, "current_order")
        and q.block(b["fleets"]["166"], "current_order")
            == q.block(science, "current_order")
        and path_systems == [39]
        and math.hypot(new_pos["x"]-target["x"], new_pos["y"]-target["y"])
            < math.hypot(old_pos["x"]-target["x"], old_pos["y"]-target["y"])
        and q.ids(q.block(science, "ships")) == [1049]
        and q.block(q.block(b["roots"]["planets"], "planet"), "544")
            == q.block(q.block(a["roots"]["planets"], "planet"), "544"),
    "mineral_destroyer_mia_merge_original_fleet_and_75_ships_safe":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and q.scalars(q.block(q.block(reinforcement, "current_order"),
                              "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and q.ids(q.block(a["queues"]["3"], "items")) == []
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and all(q.scalars(v).get("hitpoints", 0) > 0
                and q.scalars(v).get("killed") != "yes"
                for v in a["ships"].values()),
    "eep_message_pending_error_unchanged":
        all(ac["variables"].get(k) == bc["variables"].get(k)
                for k in ["eep_c", "eep_d", "eep_stage", "eep_crisis"])
        and b["messages"] == a["messages"]
        and b["pending"] == a["pending"] == []
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_VERMILION_JUNE_BUDGET_AND_APPROACH" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "route_origin_before": old_origin,
    "route_origin_after": origin,
    "route_remaining": path_systems,
    "cash_residuals": {k: str(v) for k, v in residual.items()},
    "scope": "One native May 30 to June 1 settlement and 544 approach; survey start still needs a separate guard.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
