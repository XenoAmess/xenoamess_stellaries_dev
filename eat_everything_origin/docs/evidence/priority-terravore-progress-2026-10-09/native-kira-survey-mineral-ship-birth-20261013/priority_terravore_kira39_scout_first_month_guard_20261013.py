"""Verify native monthly ledger, scout travel and paid shipyard work."""
import json
import logging
import sys
from decimal import Decimal as D
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
after = "terravore-kira39-scout-first-month-native-22881201"
prior = "terravore-kira39-scout-first5-guard-22881120"
review_stage = "terravore-kira39-scout-first-month-review-22881120"
stage = "terravore-kira39-scout-first-month-guard-22881201"
assert not (run / (stage + "-proof.json")).exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
previous = load(prior + "-proof.json")
review = load(review_stage + "-review.json")
calendar = load(after + "-calendar-receipt.json")
execution = load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
categories = ac["budget_categories"]["current_month"]
cash = ["energy", "minerals", "alloys", "unity", "rare_crystals"]
actual = {k: D(str(ac["effective_stockpile"].get(k, 0)))
          - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
net = {k: sum((D(str(row.get(k, 0))) for row in categories["income"].values()), D(0))
       - sum((D(str(row.get(k, 0))) for row in categories["expenses"].values()), D(0))
       for k in cash}
residual = {k: actual[k] - net[k] for k in cash}
f = a["fleets"]["166"]
move = q.block(f, "movement_manager")
item_before, item_after = (s["items"]["704643085"] for s in (b, a))
checks = {
    "review_calendar_two_polls_native_save_exact_sha_chain":
        previous["status"] == "PASS_NATIVE_KIRA39_SCOUT_FIRST5"
        and all(previous["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and review["reviewed_boundaries"] == ["native_monthly_budget_settlement"]
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == 11
        and calendar["start_date"] == "2288.11.20"
        and calendar["date"] == "2288.12.01"
        and previous["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "five_conventional_stock_deltas_equal_new_current_month_net":
        all(abs(value) <= D("0.0001") for value in residual.values())
        and ac["budget_categories"]["last_month"]
            == bc["budget_categories"]["current_month"]
        and actual["minerals"] == D("-85.53002")
        and actual["alloys"] == D("-6.71933")
        and categories["expenses"]["ships"]["minerals"] == 68.63352,
    "same_mineral_paid_shipyard_queue_progress24_no_ship_birth":
        set(a["items"]) == set(b["items"])
        and q.scalars(item_before)["progress"] == 7.5
        and q.scalars(item_after)["progress"] == 24
        and q.scalars(item_after)["progress_needed"] == 60
        and q.ids(q.block(a["queues"]["3"], "items")) == [704643085]
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8,
    "science166_continues_valid_kira_route_planet544_undisturbed":
        q.scalars(q.block(move, "coordinate"))["origin"] == 37
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 39
        and q.scalars(move)["state"] == "move_system"
        and "can_reach=yes" in q.block(f, "current_order")
        and q.block(q.block(b["roots"]["planets"], "planet"), "544")
            == q.block(q.block(a["roots"]["planets"], "planet"), "544"),
    "all_74_original_ships_alive_fleet_rosters_and_eep_unchanged":
        len(a["ships"]) == 74
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and all(q.scalars(v).get("hitpoints", 0) > 0
                and q.scalars(v).get("killed") != "yes"
                for v in a["ships"].values())
        and all(ac["variables"].get(k) == bc["variables"].get(k)
                for k in ["eep_c", "eep_d", "eep_stage", "eep_crisis"]),
    "no_new_message_pending_event_or_error":
        b["messages"] == a["messages"]
        and b["pending"] == a["pending"] == []
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_SCOUT_FIRST_MONTH" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "cash_deltas": {k: str(v) for k, v in actual.items()},
    "cash_residuals": {k: str(v) for k, v in residual.items()},
    "shipyard_work": q.scalars(item_after)["progress"],
    "scope": "First native post-battle monthly budget and construction; no single-ship maintenance attribution, birth or survey completion.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
