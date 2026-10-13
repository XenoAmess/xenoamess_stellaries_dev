"""Prove Dec 24 paid shipyard is one work-day short of reinforcement."""
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
after = "terravore-kira39-shipyard-precompletion-native-22881224"
prior = "terravore-kira39-scout-first-month-guard-v2-22881201"
review_stage = "terravore-kira39-shipyard-precompletion-review-22881201"
stage = "terravore-kira39-shipyard-precompletion-guard-v2-22881224"
assert not (run / (stage + "-proof.json")).exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
previous, review = (load(n + suffix) for n, suffix in
                    [(prior, "-proof.json"), (review_stage, "-review.json")])
calendar = load(after + "-calendar-receipt.json")
execution = load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
item_b, item_a = (s["items"]["704643085"] for s in (b, a))
f = a["fleets"]["166"]
move = q.block(f, "movement_manager")
owned = lambda s: {k for k, v in s["items"].items()
                   if q.scalars(v)["paying_country"] == 0}
checks = {
    "source_review_calendar_native_saves_sha_bound":
        previous["status"] == "PASS_NATIVE_KIRA39_SCOUT_FIRST_MONTH"
        and all(previous["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == 23
        and calendar["start_date"] == "2288.12.01"
        and calendar["date"] == "2288.12.24"
        and previous["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "exact_original_paid_mineral_ship_one_day_short_still_8_of_9":
        q.scalars(item_b)["progress"] == 24
        and q.scalars(item_a)["progress"] == 58.5
        and q.scalars(item_a)["progress_needed"] == 60
        and q.scalars(q.block(item_a, "resources")) == {"minerals": 412.5}
        and q.ids(q.block(a["queues"]["3"], "items")) == [704643085]
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and len(a["ships"]) == 74,
    "science_ship_reaches_97_on_reachable_kira_survey_route":
        q.scalars(q.block(move, "coordinate"))["origin"] == 97
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 39
        and q.scalars(move)["state"] == "move_system"
        and "can_reach=yes" in q.block(f, "current_order"),
    "previously_paid_mother_hive_district_completes_exactly_once":
        "117440553" in owned(b)
        and owned(b) - owned(a) == {"117440553"}
        and owned(a) - owned(b) == set()
        and q.scalars(b["items"]["117440553"])["progress"] == 463.4
        and q.scalars(q.block(b["roots"]["districts"], "1"))["level"] == 8
        and q.scalars(q.block(a["roots"]["districts"], "1"))["level"] == 9
        and b["audit"]["colonies"]["0"]["total_housing"] == 16800
        and a["audit"]["colonies"]["0"]["total_housing"] == 17700,
    "same_month_stock_eep_fleet_rosters_and_no_new_event_error":
        {k:v for k,v in bc["effective_stockpile"].items() if k not in ("physics_research","society_research","engineering_research")} == {k:v for k,v in ac["effective_stockpile"].items() if k not in ("physics_research","society_research","engineering_research")} and all(ac["effective_stockpile"][k] >= bc["effective_stockpile"][k] for k in ("physics_research","society_research","engineering_research"))
        and bc["variables"] == ac["variables"]
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and b["messages"] == a["messages"]
        and b["pending"] == a["pending"] == []
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_SHIPYARD_PRECOMPLETION" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "shipyard_work": q.scalars(item_a)["progress"],
    "scope": "One day before predicted crisis destroyer birth; no actual ship birth or fleet reinforcement claim.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
