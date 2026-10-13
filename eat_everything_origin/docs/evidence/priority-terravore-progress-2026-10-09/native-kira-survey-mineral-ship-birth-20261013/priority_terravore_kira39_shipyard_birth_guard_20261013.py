"""Prove actual mineral-paid crisis destroyer birth and vanilla reinforcement MIA."""
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
before = "terravore-kira39-shipyard-precompletion-native-22881224"
after = "terravore-kira39-shipyard-birth-native-22881225"
prior = "terravore-kira39-shipyard-precompletion-guard-v2-22881224"
review_stage = "terravore-kira39-shipyard-birth-review-22881224"
stage = "terravore-kira39-shipyard-birth-guard-22881225"
assert not (run / (stage + "-proof.json")).exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
previous, review = (load(n + suffix) for n, suffix in
                    [(prior, "-proof.json"), (review_stage, "-review.json")])
calendar = load(after + "-calendar-receipt.json")
execution = load(after + "-execution.json")
ship = a["ships"]["50332133"]
fleet = a["fleets"]["50331731"]
ss = q.scalars(ship)
fs = q.scalars(fleet)
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
cash_except_research = lambda c: {k: v for k, v in c["effective_stockpile"].items()
                                  if k not in ("physics_research", "society_research",
                                               "engineering_research")}
owned_items = lambda s: {k for k, v in s["items"].items()
                         if q.scalars(v)["paying_country"] == 0}
checks = {
    "precompletion_review_one_native_day_exact_sav_sha_chain":
        previous["status"] == "PASS_NATIVE_KIRA39_SHIPYARD_PRECOMPLETION"
        and all(previous["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == 1
        and calendar["start_date"] == "2288.12.24"
        and calendar["date"] == "2288.12.25"
        and previous["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "exact_paid_queue_completion_one_new_ship_and_fleet":
        "704643085" in owned_items(b)
        and owned_items(b) - owned_items(a) == {"704643085"}
        and owned_items(a) - owned_items(b) == set()
        and q.ids(q.block(b["queues"]["3"], "items")) == [704643085]
        and q.ids(q.block(a["queues"]["3"], "items")) == []
        and set(a["ships"]) - set(b["ships"]) == {"50332133"}
        and set(b["ships"]) - set(a["ships"]) == set()
        and set(a["fleets"]) - set(b["fleets"]) == {"50331731"}
        and set(b["fleets"]) - set(a["fleets"]) == set(),
    "new_original_crisis_destroyer_paid_design_full_health":
        ss["fleet"] == 50331731
        and ss["construction_date"] == "2288.12.25"
        and q.scalars(q.block(ship, "ship_design_implementation"))["design"] == 83887141
        and "crisis_destroyer" in a["designs"]["83887141"]
        and ss["hitpoints"] == ss["max_hitpoints"] == 1500
        and ss["shield_hitpoints"] == ss["max_shield_hitpoints"] == 480
        and ss["armor_hitpoints"] == ss["max_armor_hitpoints"] == 765,
    "native_mia_reinforcement_order_to_original_fleet917_not_yet_merged":
        q.ids(q.block(fleet, "ships")) == [50332133]
        and q.scalars(q.block(q.block(fleet, "current_order"), "merge_fleet_order"))["target"] == 917
        and fs["original_merge_fleet_target"] == 917
        and fs["mia_type"] == "mia_reinforce"
        and fs["return_date"] == "2290.12.02"
        and q.scalars(q.block(fleet, "mia_from"))["origin"] == 0
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and q.ids(q.block(a["templates"]["268435546"], "all_queued")) == [],
    "no_second_payment_old_74_ships_preserved_eep_event_error_safe":
        cash_except_research(bc) == cash_except_research(ac)
        and bc["variables"] == ac["variables"]
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and b["messages"] == a["messages"]
        and b["pending"] == a["pending"] == []
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_MINERAL_CRISIS_DESTROYER_BIRTH" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "new_ship_id": 50332133,
    "new_reinforcement_fleet_id": 50331731,
    "return_date": fs["return_date"],
    "scope": "Actual paid crisis destroyer born into MIA merge reinforcement; target fleet still 8/9.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
