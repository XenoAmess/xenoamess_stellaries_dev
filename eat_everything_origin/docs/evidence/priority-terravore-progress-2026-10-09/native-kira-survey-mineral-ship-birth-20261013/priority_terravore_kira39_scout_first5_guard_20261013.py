"""Check first five native scout and paid reinforcement construction days."""
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
after = "terravore-kira39-scout-first5-native-22881120"
pre = "terravore-kira39-scout-first5-review-22881115"
prior = "terravore-kira39-science166-survey-order-guard-22881115"
stage = "terravore-kira39-scout-first5-guard-22881120"
assert not (run / (stage + "-proof.json")).exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
review = load(pre + "-review.json")
previous = load(prior + "-proof.json")
calendar = load(after + "-calendar-receipt.json")
execution = load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
f = a["fleets"]["166"]
move = q.block(f, "movement_manager")
item_before, item_after = (s["items"]["704643085"] for s in (b, a))
ship_ids = set(b["ships"])
checks = {
    "source_guard_review_native_calendar_and_sha_bound":
        previous["status"] == "PASS_NATIVE_KIRA39_SCIENCE166_SURVEY_ORDER"
        and all(previous["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == 5
        and calendar["start_date"] == "2288.11.15"
        and calendar["date"] == "2288.11.20"
        and previous["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "same_paid_shipyard_item_progresses_7point5_without_ship_birth":
        set(a["items"]) == set(b["items"])
        and q.scalars(item_before)["progress"] == 0
        and q.scalars(item_after)["progress"] == 7.5
        and q.scalars(item_after)["progress_needed"] == 60
        and q.scalars(item_after)["paying_country"] == 0
        and q.ids(q.block(a["queues"]["3"], "items")) == [704643085]
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and len(a["ships"]) == 74,
    "science166_moving_reachably_no_false_survey_completion":
        q.scalars(q.block(move, "coordinate"))["origin"] == 37
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 39
        and q.scalars(move)["state"] == "move_system"
        and q.scalars(q.block(q.block(f, "current_order"),
                              "survey_planet_order"))["progress"] == 0
        and "can_reach=yes" in q.block(f, "current_order")
        and q.block(q.block(b["roots"]["planets"], "planet"), "544")
            == q.block(q.block(a["roots"]["planets"], "planet"), "544"),
    "all_original_ships_alive_and_fleet_rosters_preserved":
        set(a["ships"]) == ship_ids
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and all(q.scalars(v).get("hitpoints", 0) > 0
                and q.scalars(v).get("killed") != "yes"
                for v in a["ships"].values()),
    "no_monthly_settlement_unchanged_stock_budget_eep_and_messages":
        bc["effective_stockpile"] == ac["effective_stockpile"]
        and bc["budget_categories"] == ac["budget_categories"]
        and bc["variables"] == ac["variables"]
        and b["messages"] == a["messages"]
        and b["pending"] == a["pending"] == [],
    "no_new_error":
        (run / (after + "-error-before.log")).read_bytes()
        == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_SCOUT_FIRST5" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "shipyard_work": q.scalars(item_after)["progress"],
    "scope": "Only first five days of scout travel and mineral-paid construction; no monthly bill or arrival.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
